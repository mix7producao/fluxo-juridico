#!/usr/bin/env python3
"""Registra a revisão integral de uma extração de PDF somente após confirmação expressa."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
from urllib.parse import quote
from uuid import uuid4


PASTA_PROCESSO = "03 - PROCESSO JUDICIAL EM MARKDOWN"
INDICE_PROCESSO = "INDICE-DO-PROCESSO.md"
RELATORIO_EXTRACAO = "RELATORIO-DA-EXTRACAO.json"
REGISTRO_REVISAO = "REGISTRO-DA-REVISAO.md"
ANCORA_PAGINA = re.compile(r'<a id="pdf-pagina-(\d{4,})"></a>')
RESULTADOS_PENDENCIA = {"PAGINA_VAZIA_CONFIRMADA", "OCR_CONFERIDO"}


def gravar_atomico(caminho: Path, conteudo: str) -> None:
    temporario = caminho.with_name(f".{caminho.name}.{uuid4().hex}.tmp")
    temporario.write_text(conteudo, encoding="utf-8", newline="\n")
    os.replace(temporario, caminho)


def campo_unico(valor: str, nome: str) -> str:
    normalizado = " ".join(valor.replace("\r", " ").replace("\n", " ").split())
    if not normalizado:
        raise SystemExit(f"Informe {nome}.")
    return normalizado


def texto_tabela(valor: object) -> str:
    return str(valor).replace("\r", " ").replace("\n", " ").replace("|", "\\|").strip()


def interpretar_resolucoes(itens: list[str], pendentes: list[int]) -> dict[int, str]:
    resolucoes: dict[int, str] = {}
    for item in itens:
        if "=" not in item:
            raise SystemExit(f"Resolução inválida: {item}. Use PAGINA=RESULTADO.")
        pagina_texto, resultado = item.split("=", 1)
        if not pagina_texto.strip().isdigit():
            raise SystemExit(f"Número de página inválido na resolução: {item}")
        pagina = int(pagina_texto.strip())
        resultado = resultado.strip().upper()
        if resultado not in RESULTADOS_PENDENCIA:
            permitidos = ", ".join(sorted(RESULTADOS_PENDENCIA))
            raise SystemExit(f"Resultado inválido para a página {pagina}. Use: {permitidos}.")
        if pagina in resolucoes:
            raise SystemExit(f"A página {pagina} recebeu mais de uma resolução.")
        resolucoes[pagina] = resultado

    faltantes = sorted(set(pendentes) - set(resolucoes))
    excedentes = sorted(set(resolucoes) - set(pendentes))
    if faltantes or excedentes:
        raise SystemExit(
            "As páginas originalmente pendentes exigem resolução individual. "
            f"Sem resolução: {faltantes}; não estavam pendentes: {excedentes}."
        )
    return resolucoes


def bloco_da_pagina(pasta: Path, relatorio: dict, pagina: int) -> str:
    ancora = f'<a id="pdf-pagina-{pagina:04d}"></a>'
    for item in relatorio.get("arquivos_markdown", []):
        parte = caminho_interno(pasta, item.get("arquivo", ""))
        texto = parte.read_text(encoding="utf-8")
        inicio = texto.find(ancora)
        if inicio < 0:
            continue
        proxima = texto.find('<a id="pdf-pagina-', inicio + len(ancora))
        return texto[inicio:] if proxima < 0 else texto[inicio:proxima]
    raise SystemExit(f"Não foi possível localizar o conteúdo Markdown da página {pagina}.")


def caminho_interno(pasta: Path, relativo_bruto: object) -> Path:
    relativo = Path(str(relativo_bruto))
    if relativo.is_absolute() or ".." in relativo.parts:
        raise SystemExit(f"Caminho de parte inválido no relatório: {relativo}")
    caminho = (pasta / relativo).resolve()
    try:
        caminho.relative_to(pasta)
    except ValueError as erro:
        raise SystemExit(f"Parte indicada fora da extração: {relativo}") from erro
    return caminho


def validar_cobertura(pasta: Path, relatorio: dict) -> tuple[int, list[int]]:
    try:
        total = int(relatorio.get("total_paginas_pdf", 0))
    except (TypeError, ValueError) as erro:
        raise SystemExit("Total de páginas inválido no relatório da extração.") from erro
    if total < 1:
        raise SystemExit("O relatório não informa um total válido de páginas.")

    arquivos = relatorio.get("arquivos_markdown")
    if not isinstance(arquivos, list) or not arquivos:
        raise SystemExit("O relatório não contém a lista de arquivos Markdown da extração.")

    paginas_encontradas: list[int] = []
    for item in arquivos:
        if not isinstance(item, dict):
            raise SystemExit("Há uma entrada inválida na lista de arquivos Markdown.")
        parte = caminho_interno(pasta, item.get("arquivo", ""))
        if not parte.is_file():
            raise SystemExit(f"Parte da extração não encontrada: {parte}")
        try:
            texto = parte.read_text(encoding="utf-8")
        except UnicodeDecodeError as erro:
            raise SystemExit(f"Parte da extração não está em UTF-8: {parte}") from erro
        paginas_do_arquivo = [int(numero) for numero in ANCORA_PAGINA.findall(texto)]

        try:
            pagina_inicial = int(item.get("pagina_inicial"))
            pagina_final = int(item.get("pagina_final"))
        except (TypeError, ValueError) as erro:
            raise SystemExit(f"Faixa inválida registrada para: {parte}") from erro
        faixa_esperada = list(range(pagina_inicial, pagina_final + 1))
        if paginas_do_arquivo != faixa_esperada:
            raise SystemExit(
                f"Cobertura divergente em {parte.name}: esperada {faixa_esperada}, "
                f"encontrada {paginas_do_arquivo}."
            )
        paginas_encontradas.extend(paginas_do_arquivo)

    esperado = list(range(1, total + 1))
    if paginas_encontradas != esperado:
        raise SystemExit(
            "A revisão não pode ser registrada: há página ausente, repetida ou fora de ordem. "
            f"Esperado: {esperado}. Encontrado: {paginas_encontradas}."
        )

    marcadores_declarados = relatorio.get("total_marcadores_markdown")
    try:
        marcadores_declarados = int(marcadores_declarados)
    except (TypeError, ValueError) as erro:
        raise SystemExit("Total de marcadores inválido no relatório da extração.") from erro
    if marcadores_declarados != total:
        raise SystemExit(
            f"O relatório declara {marcadores_declarados} marcadores, mas o PDF tem {total} páginas."
        )

    return total, paginas_encontradas


def atualizar_indice_da_extracao(
    indice: Path,
    data: str,
    responsavel: str,
    observacao: str,
    total: int,
    paginas_ocr: list[int],
    pendentes_originais: list[int],
    resolucoes: dict[int, str],
) -> str:
    if not indice.is_file():
        raise SystemExit(f"Índice da extração não encontrado: {indice}")
    try:
        conteudo = indice.read_text(encoding="utf-8")
    except UnicodeDecodeError as erro:
        raise SystemExit(f"O índice da extração não está em UTF-8: {indice}") from erro
    if "## Registro da revisão visual e do tratamento de OCR" in conteudo:
        raise SystemExit("A extração já possui registro de revisão no índice.")

    linhas = conteudo.splitlines()
    encontrou_pendencias = False
    encontrou_status = False
    for posicao, linha in enumerate(linhas):
        if linha.startswith("- Páginas que exigem OCR ou revisão visual:"):
            linhas[posicao] = "- Páginas pendentes após a revisão: Nenhuma"
            encontrou_pendencias = True
        elif linha.startswith("- Status:"):
            linhas[posicao] = "- Status: REVISÃO VISUAL E TRATAMENTO DE OCR CONCLUÍDOS"
            encontrou_status = True
    if not encontrou_pendencias or not encontrou_status:
        raise SystemExit("O índice da extração não contém os campos de pendência e status esperados.")

    paginas_ocr_texto = ", ".join(map(str, paginas_ocr)) if paginas_ocr else "Nenhuma"
    pendentes_texto = (
        ", ".join(map(str, pendentes_originais)) if pendentes_originais else "Nenhuma"
    )
    linhas.extend(
        [
            "",
            "## Registro da revisão visual e do tratamento de OCR",
            "",
            f"- Data do registro: {data}",
            f"- Responsável: {responsavel}",
            f"- Cobertura conferida: páginas 1 a {total}, sem lacunas ou duplicidades",
            f"- Páginas originalmente pendentes: {pendentes_texto}",
            f"- Páginas que receberam OCR: {paginas_ocr_texto}",
            "- Resoluções das páginas originalmente pendentes: "
            + (", ".join(f"{pagina}={resultado}" for pagina, resultado in sorted(resolucoes.items())) or "Nenhuma"),
            f"- Observação: {observacao}",
            "",
        ]
    )
    return "\n".join(linhas)


def atualizar_indice_principal(pasta: Path, relatorio: dict, total: int) -> bool:
    pasta_principal = pasta.parent
    if pasta_principal.name != PASTA_PROCESSO:
        return False
    indice = pasta_principal / INDICE_PROCESSO
    if not indice.is_file():
        return False
    try:
        conteudo = indice.read_text(encoding="utf-8")
    except UnicodeDecodeError as erro:
        raise SystemExit(f"O índice principal não está em UTF-8: {indice}") from erro

    relativo = (pasta / INDICE_PROCESSO).relative_to(pasta_principal).as_posix()
    link = quote(relativo, safe="/-._~")
    titulo = texto_tabela(relatorio.get("titulo") or pasta.name)
    id_prova = texto_tabela(relatorio.get("id_prova") or "[A CONFIRMAR]")
    nome_pdf = texto_tabela(relatorio.get("nome_pdf_original") or "[A CONFIRMAR]")
    nova_linha = (
        f"| {id_prova} | {titulo} | {nome_pdf} | {total} | Nenhuma | "
        f"REVISÃO VISUAL E TRATAMENTO DE OCR CONCLUÍDOS | [Abrir índice]({link}) |"
    )

    linhas = conteudo.splitlines()
    for posicao, linha in enumerate(linhas):
        if f"]({link})" in linha:
            linhas[posicao] = nova_linha
            gravar_atomico(indice, "\n".join(linhas) + "\n")
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Registra revisão visual integral e tratamento de OCR depois de validar a cobertura "
            "de todas as páginas da extração."
        )
    )
    parser.add_argument("pasta_da_extracao")
    parser.add_argument("--responsavel", required=True)
    parser.add_argument("--observacao", required=True)
    parser.add_argument(
        "--resolver",
        action="append",
        default=[],
        help=(
            "Resolução individual de página originalmente pendente. Repita para cada página, "
            "por exemplo: --resolver 3=PAGINA_VAZIA_CONFIRMADA ou --resolver 4=OCR_CONFERIDO."
        ),
    )
    parser.add_argument(
        "--confirmo-revisao-integral",
        action="store_true",
        help="Confirma expressamente que todas as páginas foram revisadas e o OCR necessário foi tratado.",
    )
    args = parser.parse_args()

    if not args.confirmo_revisao_integral:
        raise SystemExit(
            "Nada foi alterado. Use --confirmo-revisao-integral somente depois de revisar "
            "visualmente todas as páginas e tratar o OCR necessário."
        )

    responsavel = campo_unico(args.responsavel, "o responsável pela revisão")
    observacao = campo_unico(args.observacao, "uma observação sobre a revisão")
    pasta = Path(args.pasta_da_extracao).expanduser().resolve()
    if not pasta.is_dir():
        raise SystemExit(f"Pasta da extração não encontrada: {pasta}")

    caminho_relatorio = pasta / RELATORIO_EXTRACAO
    if not caminho_relatorio.is_file():
        raise SystemExit(f"Relatório da extração não encontrado: {caminho_relatorio}")
    try:
        relatorio = json.loads(caminho_relatorio.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as erro:
        raise SystemExit(f"Relatório da extração inválido: {caminho_relatorio}: {erro}") from erro
    if not isinstance(relatorio, dict):
        raise SystemExit("O relatório da extração deve conter um objeto JSON.")
    if relatorio.get("revisao_visual_concluida"):
        raise SystemExit("A revisão visual já está registrada como concluída. Nada foi alterado.")

    total, paginas_conferidas = validar_cobertura(pasta, relatorio)
    pendentes_brutos = relatorio.get("paginas_pendentes_de_ocr_ou_revisao", [])
    if not isinstance(pendentes_brutos, list):
        raise SystemExit("A lista de páginas pendentes no relatório é inválida.")
    try:
        pendentes_originais = sorted({int(numero) for numero in pendentes_brutos})
    except (TypeError, ValueError) as erro:
        raise SystemExit("A lista de páginas pendentes contém valor inválido.") from erro
    if any(numero < 1 or numero > total for numero in pendentes_originais):
        raise SystemExit("A lista de páginas pendentes contém página fora da cobertura do PDF.")
    resolucoes = interpretar_resolucoes(args.resolver, pendentes_originais)
    paginas_ocr = sorted(
        pagina for pagina, resultado in resolucoes.items() if resultado == "OCR_CONFERIDO"
    )
    for pagina in paginas_ocr:
        if "[PÁGINA SEM TEXTO DETECTÁVEL." in bloco_da_pagina(pasta, relatorio, pagina):
            raise SystemExit(
                f"A página {pagina} ainda contém o marcador de ausência de texto. "
                "Insira e confira o OCR no Markdown antes de registrar OCR_CONFERIDO."
            )

    data = datetime.now(timezone.utc).isoformat(timespec="seconds")
    indice_extracao = pasta / INDICE_PROCESSO
    indice_atualizado = atualizar_indice_da_extracao(
        indice=indice_extracao,
        data=data,
        responsavel=responsavel,
        observacao=observacao,
        total=total,
        paginas_ocr=paginas_ocr,
        pendentes_originais=pendentes_originais,
        resolucoes=resolucoes,
    )

    registro = "\n".join(
        [
            "# Registro da revisão visual e do tratamento de OCR",
            "",
            "- Status: CONCLUÍDO",
            f"- Data do registro: {data}",
            f"- Responsável: {responsavel}",
            f"- Total de páginas conferidas: {total}",
            f"- Páginas originalmente pendentes: {', '.join(map(str, pendentes_originais)) if pendentes_originais else 'Nenhuma'}",
            f"- Páginas que receberam OCR: {', '.join(map(str, paginas_ocr)) if paginas_ocr else 'Nenhuma'}",
            "- Resoluções das páginas originalmente pendentes: "
            + (", ".join(f"{pagina}={resultado}" for pagina, resultado in sorted(resolucoes.items())) or "Nenhuma"),
            f"- Observação: {observacao}",
            "",
            "A cobertura técnica foi validada. Este registro não substitui o PDF original.",
            "",
        ]
    )
    caminho_registro = pasta / REGISTRO_REVISAO
    if caminho_registro.exists():
        raise SystemExit(f"Já existe um registro de revisão, que foi preservado: {caminho_registro}")

    indice_principal_atualizado = atualizar_indice_principal(pasta, relatorio, total)

    relatorio["paginas_originalmente_pendentes_de_ocr_ou_revisao"] = pendentes_originais
    relatorio["paginas_pendentes_de_ocr_ou_revisao"] = []
    relatorio["paginas_com_ocr"] = paginas_ocr
    relatorio["resolucoes_das_paginas_pendentes"] = {
        str(pagina): resultado for pagina, resultado in sorted(resolucoes.items())
    }
    relatorio["revisao_visual_concluida"] = True
    relatorio["tratamento_de_ocr_concluido"] = True
    relatorio["cobertura_validada"] = True
    relatorio["total_paginas_conferidas"] = len(paginas_conferidas)
    relatorio["data_revisao"] = data
    relatorio["responsavel_revisao"] = responsavel
    relatorio["observacao_revisao"] = observacao
    relatorio["indice_principal_atualizado_na_revisao"] = indice_principal_atualizado
    relatorio["status"] = "REVISAO_VISUAL_E_TRATAMENTO_DE_OCR_CONCLUIDOS"

    gravar_atomico(indice_extracao, indice_atualizado)
    gravar_atomico(caminho_registro, registro)
    gravar_atomico(
        caminho_relatorio,
        json.dumps(relatorio, ensure_ascii=False, indent=2) + "\n",
    )

    print(
        json.dumps(
            {
                "status": relatorio["status"],
                "pasta_da_extracao": str(pasta),
                "total_paginas_conferidas": len(paginas_conferidas),
                "paginas_com_ocr": paginas_ocr,
                "responsavel_revisao": responsavel,
                "registro": str(caminho_registro),
                "indice_principal_atualizado": indice_principal_atualizado,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
