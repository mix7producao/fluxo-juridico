#!/usr/bin/env python3
"""Extrai todas as páginas textuais de um PDF para blocos Markdown auditáveis."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from urllib.parse import quote
from uuid import uuid4

try:
    from pypdf import PdfReader
except ImportError as erro:
    raise SystemExit(
        "Dependência ausente: pypdf. No Codex Desktop, carregue as dependências do espaço de trabalho, "
        "use o Python retornado com -X utf8 e consulte references/execucao-local-e-dependencias.md."
    ) from erro


PASTA_PROCESSO = "03 - PROCESSO JUDICIAL EM MARKDOWN"
INDICE_PROCESSO = "INDICE-DO-PROCESSO.md"
INICIO_EXTRACOES = "<!-- INICIO DAS EXTRACOES AUTOMATICAS -->"
FIM_EXTRACOES = "<!-- FIM DAS EXTRACOES AUTOMATICAS -->"
PADRAO_ID = re.compile(r"^PROVA-\d+$")


def sha256(caminho: Path) -> str:
    digest = hashlib.sha256()
    with caminho.open("rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(1024 * 1024), b""):
            digest.update(bloco)
    return digest.hexdigest()


def gravar_atomico(caminho: Path, conteudo: str) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    temporario = caminho.with_name(f".{caminho.name}.{uuid4().hex}.tmp")
    temporario.write_text(conteudo, encoding="utf-8", newline="\n")
    os.replace(temporario, caminho)


def preparar_texto(texto: str) -> str:
    return texto.replace("\r\n", "\n").replace("\r", "\n").strip()


def texto_tabela(valor: object) -> str:
    return str(valor).replace("\r", " ").replace("\n", " ").replace("|", "\\|").strip()


def atualizar_indice_principal(
    saida: Path,
    id_prova: str,
    titulo: str,
    nome_pdf: str,
    total_paginas: int,
    paginas_pendentes: list[int],
) -> Path | None:
    """Acrescenta a extração ao índice da pasta principal sem apagar entradas anteriores."""

    pasta_principal = saida.parent
    if pasta_principal.name != PASTA_PROCESSO:
        return None

    indice_principal = pasta_principal / INDICE_PROCESSO
    if indice_principal.exists() and not indice_principal.is_file():
        raise SystemExit(f"O índice principal existe e não é um arquivo: {indice_principal}")

    if indice_principal.exists():
        try:
            conteudo = indice_principal.read_text(encoding="utf-8")
        except UnicodeDecodeError as erro:
            raise SystemExit(
                f"O índice principal não está em UTF-8 e foi preservado sem alteração: {indice_principal}"
            ) from erro
    else:
        conteudo = "# Índice do processo judicial em Markdown\n"

    relativo = (saida / INDICE_PROCESSO).relative_to(pasta_principal).as_posix()
    link = quote(relativo, safe="/-._~")
    if f"]({link})" in conteudo:
        return indice_principal

    tem_inicio = INICIO_EXTRACOES in conteudo
    tem_fim = FIM_EXTRACOES in conteudo
    if tem_inicio != tem_fim:
        raise SystemExit(
            "O índice principal contém marcadores automáticos incompletos e foi preservado sem alteração: "
            f"{indice_principal}"
        )

    pendencias = ", ".join(map(str, paginas_pendentes)) if paginas_pendentes else "Nenhuma detectada"
    status = (
        "PENDENTE DE OCR E REVISÃO VISUAL"
        if paginas_pendentes
        else "PENDENTE DE REVISÃO VISUAL"
    )
    linha = (
        f"| {id_prova} | {texto_tabela(titulo)} | {texto_tabela(nome_pdf)} | {total_paginas} | "
        f"{texto_tabela(pendencias)} | {status} | [Abrir índice]({link}) |"
    )

    if tem_inicio:
        posicao = conteudo.index(FIM_EXTRACOES)
        antes = conteudo[:posicao].rstrip()
        depois = conteudo[posicao:]
        atualizado = f"{antes}\n{linha}\n{depois}"
    else:
        placeholder = "Nenhum processo foi extraído até o momento."
        conteudo = conteudo.replace(placeholder, "").rstrip()
        secao = "\n".join(
            [
                "## Extrações disponíveis",
                "",
                INICIO_EXTRACOES,
                "| Prova | Extração | PDF original | Páginas | Páginas pendentes | Status | Índice detalhado |",
                "|---|---|---|---:|---|---|---|",
                linha,
                FIM_EXTRACOES,
            ]
        )
        atualizado = f"{conteudo}\n\n{secao}\n"

    gravar_atomico(indice_principal, atualizado)
    return indice_principal


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extrai um PDF integral para Markdown com um marcador por página."
    )
    parser.add_argument("pdf")
    parser.add_argument("pasta_de_saida")
    parser.add_argument("--paginas-por-arquivo", type=int, default=50)
    parser.add_argument("--titulo", help="Título exibido no índice.")
    parser.add_argument("--id-prova", required=True, help="Identificador permanente do PDF, por exemplo PROVA-0003.")
    args = parser.parse_args()

    if not PADRAO_ID.fullmatch(args.id_prova):
        raise SystemExit("O ID da prova deve usar o formato PROVA-0001.")

    if args.paginas_por_arquivo < 1 or args.paginas_por_arquivo > 200:
        raise SystemExit("Use de 1 a 200 páginas por arquivo.")

    pdf = Path(args.pdf).expanduser().resolve()
    if not pdf.is_file():
        raise SystemExit(f"PDF não encontrado: {pdf}")

    saida = Path(args.pasta_de_saida).expanduser().resolve()
    if saida.exists() and not saida.is_dir():
        raise SystemExit(f"A saída existe e não é uma pasta: {saida}")
    if saida.exists() and any(saida.iterdir()):
        raise SystemExit(f"A pasta de saída precisa estar vazia: {saida}")
    saida.mkdir(parents=True, exist_ok=True)

    try:
        leitor = PdfReader(str(pdf), strict=False)
    except Exception as erro:
        raise SystemExit(f"Não foi possível abrir o PDF: {erro}") from erro

    if leitor.is_encrypted:
        try:
            resultado = leitor.decrypt("")
        except Exception as erro:
            raise SystemExit(f"PDF protegido. Não foi possível ler sem senha: {erro}") from erro
        if resultado == 0:
            raise SystemExit("PDF protegido por senha. Solicite uma cópia acessível.")

    total = len(leitor.pages)
    if total == 0:
        raise SystemExit("O PDF não contém páginas.")

    paginas: list[dict] = []
    pendentes: list[int] = []
    for indice, pagina in enumerate(leitor.pages, 1):
        erro_extracao = None
        try:
            texto = preparar_texto(pagina.extract_text() or "")
        except Exception as erro:
            texto = ""
            erro_extracao = str(erro)

        util = len("".join(texto.split())) >= 20
        if not util:
            pendentes.append(indice)
        paginas.append(
            {
                "pagina": indice,
                "texto": texto,
                "metodo": "texto nativo",
                "status": "OK" if util else "REVISÃO OU OCR NECESSÁRIO",
                "erro": erro_extracao,
            }
        )

    arquivos: list[dict] = []
    for inicio_zero in range(0, total, args.paginas_por_arquivo):
        bloco = paginas[inicio_zero : inicio_zero + args.paginas_por_arquivo]
        inicio = bloco[0]["pagina"]
        fim = bloco[-1]["pagina"]
        nome = f"PAGINAS-{inicio:04d}-A-{fim:04d}.md"
        linhas = [
            f"# Processo em Markdown: páginas {inicio:04d} a {fim:04d}",
            "",
            f"Fonte: `{pdf.name}`",
            "",
            "Este texto é derivado para consulta. O PDF original prevalece para conferência.",
            "",
        ]
        for item in bloco:
            numero = item["pagina"]
            linhas.extend(
                [
                    f'<a id="pdf-pagina-{numero:04d}"></a>',
                    "",
                    f"## Página {numero:04d}",
                    "",
                    f"Método de extração: {item['metodo']}",
                    "",
                ]
            )
            if item["texto"]:
                linhas.extend([item["texto"], ""])
            else:
                linhas.extend(
                    [
                        "[PÁGINA SEM TEXTO DETECTÁVEL. O original foi preservado. Revisão visual ou OCR necessário.]",
                        "",
                    ]
                )
            if item["erro"]:
                linhas.extend([f"[ERRO DE EXTRAÇÃO: {item['erro']}]", ""])
        gravar_atomico(saida / nome, "\n".join(linhas))
        arquivos.append({"arquivo": nome, "pagina_inicial": inicio, "pagina_final": fim})

    titulo = (args.titulo or pdf.stem).replace("\n", " ").replace("\r", " ")
    indice = [
        f"# Índice do processo: {titulo}",
        "",
        f"- Prova permanente: `{args.id_prova}`",
        f"- PDF original: `{pdf.name}`",
        f"- Total de páginas do PDF: {total}",
        f"- Total de páginas representadas em Markdown: {total}",
        f"- Páginas que exigem OCR ou revisão visual: {', '.join(map(str, pendentes)) if pendentes else 'Nenhuma detectada'}",
        f"- Status: {'PENDENTE DE OCR E REVISÃO VISUAL' if pendentes else 'PENDENTE DE REVISÃO VISUAL'}",
        "",
        "| Faixa | Arquivo |",
        "|---|---|",
    ]
    for item in arquivos:
        indice.append(
            f"| {item['pagina_inicial']} a {item['pagina_final']} | [{item['arquivo']}]({item['arquivo']}) |"
        )
    indice.extend(
        [
            "",
            "A conclusão textual não dispensa a conferência de citações decisivas no PDF original.",
            "",
        ]
    )
    gravar_atomico(saida / INDICE_PROCESSO, "\n".join(indice))

    indice_principal = atualizar_indice_principal(
        saida=saida,
        id_prova=args.id_prova,
        titulo=titulo,
        nome_pdf=pdf.name,
        total_paginas=total,
        paginas_pendentes=pendentes,
    )

    relatorio = {
        "nome_pdf_original": pdf.name,
        "id_prova": args.id_prova,
        "titulo": titulo,
        "caminho_pdf_no_momento_da_extracao": str(pdf),
        "sha256": sha256(pdf),
        "total_paginas_pdf": total,
        "total_marcadores_markdown": total,
        "paginas_por_arquivo": args.paginas_por_arquivo,
        "arquivos_markdown": arquivos,
        "paginas_pendentes_de_ocr_ou_revisao": pendentes,
        "revisao_visual_concluida": False,
        "status": "PENDENTE_DE_OCR_E_REVISAO_VISUAL" if pendentes else "PENDENTE_DE_REVISAO_VISUAL",
        "indice_principal": str(indice_principal) if indice_principal else None,
    }
    gravar_atomico(
        saida / "RELATORIO-DA-EXTRACAO.json",
        json.dumps(relatorio, ensure_ascii=False, indent=2) + "\n",
    )

    print(json.dumps(relatorio, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
