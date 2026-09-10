#!/usr/bin/env python3
"""Valida estrutura, integridade, UTF-8, links e cobertura de PDFs do caso."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote
from uuid import uuid4


PASTAS = [
    "00 - ORIGINAIS RECEBIDOS - NAO ALTERAR",
    "01 - PROVAS ORGANIZADAS",
    "02 - TRANSCRICOES DE AUDIOS VIDEOS E CONVERSAS",
    "03 - PROCESSO JUDICIAL EM MARKDOWN",
    "04 - INDICE E CRONOLOGIA",
    "05 - PERGUNTAS E PENDENCIAS",
    "06 - ANALISE JURIDICA",
    "07 - PECAS EM ELABORACAO",
    "08 - PECAS FINALIZADAS E PROTOCOLOS",
]
ARQUIVOS = [
    "LEIA-PRIMEIRO.md",
    "04 - INDICE E CRONOLOGIA/INVENTARIO-DE-PROVAS.md",
    "04 - INDICE E CRONOLOGIA/LINHA-DO-TEMPO.md",
    "04 - INDICE E CRONOLOGIA/MAPA-DE-FATOS-E-PROVAS.md",
    "04 - INDICE E CRONOLOGIA/RESUMO-OBJETIVO-DO-CASO.md",
    "04 - INDICE E CRONOLOGIA/RELATORIO-DE-CONFERENCIA.md",
    "05 - PERGUNTAS E PENDENCIAS/PENDENCIAS-ATUAIS.md",
]
MOJIBAKE = ("Ã©", "Ã§", "Ã£", "Ã¡", "Ã³", "Ã­", "Ãª", "Ãº", "Ã¢", "Ã´", "�")
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
ID = re.compile(r"^PROVA-\d+$")
ID_NO_NOME = re.compile(r"^(PROVA-\d+)_")
ANCORA_PAGINA = re.compile(r'<a id="pdf-pagina-(\d{4,})"></a>')
ID_TABELA = re.compile(r"^\|\s*(PROVA-\d+)\s*\|", re.MULTILINE)
MARCA_TEMPO = re.compile(r"\[(?:\d{2}:){2}\d{2}\]")
INICIO_PENDENCIAS = "<!-- INICIO: PENDENCIAS TECNICAS AUTOMATICAS -->"
FIM_PENDENCIAS = "<!-- FIM: PENDENCIAS TECNICAS AUTOMATICAS -->"


def sha256(caminho: Path) -> str:
    digest = hashlib.sha256()
    with caminho.open("rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(1024 * 1024), b""):
            digest.update(bloco)
    return digest.hexdigest()


def ler_jsonl(caminho: Path, erros: list[str]) -> list[dict]:
    if not caminho.is_file():
        erros.append(f"Controle técnico ausente: {caminho}")
        return []
    saida = []
    try:
        linhas = caminho.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError as erro:
        erros.append(f"Controle técnico não está em UTF-8: {caminho}: {erro}")
        return []
    for numero, linha in enumerate(linhas, 1):
        if not linha.strip():
            continue
        try:
            item = json.loads(linha)
        except json.JSONDecodeError as erro:
            erros.append(f"JSON inválido em {caminho}, linha {numero}: {erro}")
            continue
        if not isinstance(item, dict):
            erros.append(f"Registro não é um objeto JSON em {caminho}, linha {numero}.")
            continue
        saida.append(item)
    return saida


def gravar_atomico(caminho: Path, conteudo: str) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    temporario = caminho.with_name(f".{caminho.name}.{uuid4().hex}.tmp")
    temporario.write_text(conteudo, encoding="utf-8", newline="\n")
    os.replace(temporario, caminho)


def atualizar_pendencias(caminho: Path, erros: list[str], avisos: list[str]) -> None:
    if not caminho.is_file():
        return
    texto = caminho.read_text(encoding="utf-8")
    bloco_anterior = re.compile(
        re.escape(INICIO_PENDENCIAS) + r".*?" + re.escape(FIM_PENDENCIAS),
        re.DOTALL,
    )
    texto = bloco_anterior.sub("", texto).rstrip()
    linhas = [INICIO_PENDENCIAS, "", "## Pendências técnicas automáticas", ""]
    itens = [*(f"ERRO: {item}" for item in erros), *avisos]
    if itens:
        linhas.extend(f"- [ ] {item}" for item in itens)
    else:
        linhas.append("Nenhuma pendência técnica automática foi identificada.")
    linhas.extend(["", FIM_PENDENCIAS, ""])
    gravar_atomico(caminho, texto + "\n\n" + "\n".join(linhas))


def atualizar_relatorio(
    caminho: Path,
    status: str,
    arquivos_recebidos: int,
    registros: list[dict],
    relatorios_pdf: list[Path],
    erros: list[str],
    avisos: list[str],
) -> None:
    if not caminho.is_file():
        return
    duplicados = sum(1 for item in registros if item.get("duplicado_exato_de"))
    total_paginas = 0
    for relatorio in relatorios_pdf:
        try:
            total_paginas += int(json.loads(relatorio.read_text(encoding="utf-8")).get("total_paginas_pdf", 0))
        except Exception:
            pass
    linhas = [
        "# Relatório de conferência da organização",
        "",
        f"- Status: {status}",
        f"- Atualizado em UTC: {datetime.now(timezone.utc).isoformat()}",
        f"- Arquivos recebidos: {arquivos_recebidos}",
        f"- Provas registradas: {len(registros)}",
        f"- Duplicados exatos: {duplicados}",
        f"- PDFs de processo extraídos: {len(relatorios_pdf)}",
        f"- Páginas de processo representadas: {total_paginas}",
        f"- Erros de integridade: {len(erros)}",
        f"- Pendências técnicas: {len(avisos)}",
        (
            "- Próxima etapa e modelo: iniciar a análise jurídica com Sol ou equivalente de alto raciocínio."
            if status == "APROVADO"
            else "- Próxima etapa e modelo: continuar a organização com Terra ou equivalente até corrigir erros e pendências."
        ),
        "",
    ]
    gravar_atomico(caminho, "\n".join(linhas))


def validar_links(caminho: Path, texto: str, erros: list[str]) -> None:
    for alvo in LINK.findall(texto):
        alvo = alvo.strip().strip("<>")
        if not alvo or alvo.startswith(("http://", "https://", "mailto:", "#")):
            continue
        sem_ancora = unquote(alvo.split("#", 1)[0])
        if not sem_ancora:
            continue
        destino = (caminho.parent / sem_ancora).resolve()
        if not destino.exists():
            erros.append(f"Link local quebrado em {caminho}: {alvo}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida a organização de um caso jurídico.")
    parser.add_argument("pasta_do_caso")
    args = parser.parse_args()

    raiz = Path(args.pasta_do_caso).expanduser().resolve()
    erros: list[str] = []
    avisos: list[str] = []

    if not raiz.is_dir():
        raise SystemExit(f"Pasta do caso não encontrada: {raiz}")
    for relativo in PASTAS:
        if not (raiz / relativo).is_dir():
            erros.append(f"Pasta obrigatória ausente: {relativo}")
    for relativo in ARQUIVOS:
        if not (raiz / relativo).is_file():
            erros.append(f"Arquivo obrigatório ausente: {relativo}")

    controle = raiz / "04 - INDICE E CRONOLOGIA" / "CONTROLE-TECNICO-DE-INTEGRIDADE.jsonl"
    registros = [
        item
        for item in ler_jsonl(controle, erros)
        if item.get("tipo_registro") == "ARQUIVO_RECEBIDO"
    ]
    ids = [str(item.get("id", "")) for item in registros]
    if len(ids) != len(set(ids)):
        erros.append("Existem identificadores de prova repetidos no controle técnico.")
    for identificador in ids:
        if not ID.fullmatch(identificador):
            erros.append(f"Identificador inválido: {identificador}")

    caminhos_registrados = [str(item.get("caminho_original", "")) for item in registros]
    if len(caminhos_registrados) != len(set(caminhos_registrados)):
        erros.append("Existem dois registros para o mesmo caminho original.")

    originais_por_id: dict[str, dict] = {}
    for item in registros:
        identificador = item.get("id")
        originais_por_id[identificador] = item
        relativo = Path(str(item.get("caminho_original", "")))
        original = (raiz / relativo).resolve()
        try:
            original.relative_to((raiz / "00 - ORIGINAIS RECEBIDOS - NAO ALTERAR").resolve())
        except ValueError:
            erros.append(f"Origem fora da pasta permitida: {relativo}")
            continue
        if not original.is_file():
            erros.append(f"Original registrado não existe: {relativo}")
            continue
        if sha256(original) != item.get("sha256"):
            erros.append(f"Original alterado após registro: {relativo}")

    pasta_originais = (raiz / "00 - ORIGINAIS RECEBIDOS - NAO ALTERAR").resolve()
    arquivos_originais = [arquivo for arquivo in pasta_originais.rglob("*") if arquivo.is_file()]
    caminhos_reais = {arquivo.relative_to(raiz).as_posix() for arquivo in arquivos_originais}
    caminhos_controle = set(caminhos_registrados)
    for relativo in sorted(caminhos_reais - caminhos_controle):
        erros.append(f"Original ainda não inventariado: {relativo}")

    estado = raiz / "04 - INDICE E CRONOLOGIA" / "ESTADO-DA-NUMERACAO.json"
    if not estado.is_file():
        erros.append(f"Estado da numeração ausente: {estado.relative_to(raiz)}")
    else:
        try:
            dados_estado = json.loads(estado.read_text(encoding="utf-8"))
            utilizados = set(map(str, dados_estado.get("identificadores_ja_utilizados", [])))
            if not set(ids).issubset(utilizados):
                erros.append("O estado da numeração não contém todos os identificadores já usados.")
            numeros = [int(item.split("-", 1)[1]) for item in ids if ID.fullmatch(item)]
            proximo = int(dados_estado.get("proximo_id", 0))
            if numeros and proximo <= max(numeros):
                erros.append("O próximo número de prova não é maior que todos os IDs existentes.")
        except Exception as erro:
            erros.append(f"Estado da numeração inválido: {erro}")

    organizadas = raiz / "01 - PROVAS ORGANIZADAS"
    arquivos_por_id: dict[str, list[Path]] = {}
    if organizadas.is_dir():
        for arquivo in organizadas.rglob("*"):
            if not arquivo.is_file():
                continue
            encontrado = ID_NO_NOME.match(arquivo.name)
            if not encontrado:
                erros.append(f"Cópia organizada sem identificador no nome: {arquivo.relative_to(raiz)}")
                continue
            identificador = encontrado.group(1)
            arquivos_por_id.setdefault(identificador, []).append(arquivo)
            original = originais_por_id.get(identificador)
            if not original:
                erros.append(f"Cópia organizada sem original registrado: {arquivo.relative_to(raiz)}")
                continue
            if sha256(arquivo) != original.get("sha256"):
                erros.append(f"Cópia organizada diverge do original: {arquivo.relative_to(raiz)}")

    for identificador in sorted(ids):
        quantidade = len(arquivos_por_id.get(identificador, []))
        if quantidade == 0:
            erros.append(f"Prova registrada ainda não possui cópia organizada: {identificador}")
        elif quantidade > 1:
            caminhos = [str(item.relative_to(raiz)) for item in arquivos_por_id[identificador]]
            erros.append(f"Prova possui mais de uma cópia organizada: {identificador}: {caminhos}")

    controle_copias = raiz / "04 - INDICE E CRONOLOGIA" / "CONTROLE-DAS-COPIAS-ORGANIZADAS.jsonl"
    registros_copias = (
        [
            item
            for item in ler_jsonl(controle_copias, erros)
            if item.get("tipo_registro") == "COPIA_ORGANIZADA"
        ]
        if controle_copias.exists()
        else []
    )
    copias_por_id: dict[str, list[dict]] = {}
    for item in registros_copias:
        copias_por_id.setdefault(str(item.get("id", "")), []).append(item)
    for identificador in sorted(set(copias_por_id) - set(ids)):
        erros.append(f"Controle de cópias possui ID sem original registrado: {identificador}")
    for identificador in sorted(ids):
        quantidade_arquivos = len(arquivos_por_id.get(identificador, []))
        quantidade_registros = len(copias_por_id.get(identificador, []))
        if quantidade_arquivos and quantidade_registros != 1:
            erros.append(
                f"Controle de cópias inconsistente para {identificador}: "
                f"{quantidade_arquivos} arquivo(s) e {quantidade_registros} registro(s)."
            )
            continue
        if quantidade_registros == 1 and quantidade_arquivos == 1:
            evento = copias_por_id[identificador][0]
            esperado = (raiz / Path(str(evento.get("caminho_copia_organizada", "")))).resolve()
            real = arquivos_por_id[identificador][0].resolve()
            if esperado != real:
                erros.append(f"Registro de cópia aponta para caminho diferente do arquivo de {identificador}.")
            original = originais_por_id.get(identificador, {})
            if evento.get("sha256_copia") != original.get("sha256"):
                erros.append(f"Hash do registro de cópia diverge do original de {identificador}.")

    inventario_visivel = raiz / "04 - INDICE E CRONOLOGIA" / "INVENTARIO-DE-PROVAS.md"
    if inventario_visivel.is_file():
        texto_inventario = inventario_visivel.read_text(encoding="utf-8")
        ids_inventario = ID_TABELA.findall(texto_inventario)
        linhas_inventario = {
            encontrado.group(1): linha
            for linha in texto_inventario.splitlines()
            if (encontrado := ID_TABELA.match(linha))
        }
        if len(ids_inventario) != len(set(ids_inventario)):
            erros.append("Há identificador repetido no inventário visível de provas.")
        if set(ids_inventario) != set(ids):
            faltantes = sorted(set(ids) - set(ids_inventario))
            excedentes = sorted(set(ids_inventario) - set(ids))
            erros.append(
                f"Inventário visível não corresponde ao controle técnico. "
                f"Faltantes: {faltantes}; excedentes: {excedentes}."
            )
        for identificador, eventos in copias_por_id.items():
            if len(eventos) == 1:
                caminho_copia = str(eventos[0].get("caminho_copia_organizada", ""))
                linha = linhas_inventario.get(identificador, "")
                if caminho_copia and caminho_copia not in linha:
                    erros.append(
                        f"Inventário visível não contém o caminho da cópia organizada de {identificador}."
                    )
                if not linha.rstrip().endswith("| CÓPIA ORGANIZADA |"):
                    erros.append(
                        f"Inventário visível não registra a situação correta da cópia de {identificador}."
                    )

    for markdown in raiz.rglob("*.md"):
        try:
            markdown.resolve().relative_to(pasta_originais)
            continue
        except ValueError:
            pass
        try:
            texto = markdown.read_text(encoding="utf-8")
        except UnicodeDecodeError as erro:
            erros.append(f"Markdown não está em UTF-8: {markdown.relative_to(raiz)}: {erro}")
            continue
        if any(marca in texto for marca in MOJIBAKE):
            erros.append(f"Possível erro de codificação em: {markdown.relative_to(raiz)}")
        validar_links(markdown, texto, erros)

    relatorios_pdf = list((raiz / "03 - PROCESSO JUDICIAL EM MARKDOWN").rglob("RELATORIO-DA-EXTRACAO.json"))
    hashes_pdf_extraidos: set[str] = set()
    for relatorio in relatorios_pdf:
        try:
            dados = json.loads(relatorio.read_text(encoding="utf-8"))
        except Exception as erro:
            erros.append(f"Relatório de PDF inválido: {relatorio}: {erro}")
            continue
        hashes_pdf_extraidos.add(str(dados.get("sha256", "")))
        id_pdf = str(dados.get("id_prova", ""))
        if not ID.fullmatch(id_pdf):
            erros.append(f"Relatório de PDF sem ID de prova válido: {relatorio.relative_to(raiz)}")
        elif id_pdf not in originais_por_id:
            erros.append(f"Relatório de PDF aponta para prova não registrada: {id_pdf}")
        elif dados.get("sha256") != originais_por_id[id_pdf].get("sha256"):
            erros.append(f"Relatório de PDF não corresponde aos bytes registrados de {id_pdf}.")
        try:
            total = int(dados.get("total_paginas_pdf", 0))
        except (TypeError, ValueError):
            erros.append(f"Total de páginas inválido no relatório: {relatorio.relative_to(raiz)}")
            continue
        paginas: list[int] = []
        for item in dados.get("arquivos_markdown", []):
            if not isinstance(item, dict):
                erros.append(f"Entrada de parte inválida no relatório: {relatorio.relative_to(raiz)}")
                continue
            parte = (relatorio.parent / Path(str(item.get("arquivo", "")))).resolve()
            try:
                parte.relative_to(relatorio.parent.resolve())
            except ValueError:
                erros.append(f"Parte do processo aponta para fora da extração: {parte}")
                continue
            if not parte.is_file():
                erros.append(f"Parte do processo ausente: {parte}")
                continue
            try:
                texto_parte = parte.read_text(encoding="utf-8")
            except UnicodeDecodeError as erro:
                erros.append(f"Parte do processo não está em UTF-8: {parte}: {erro}")
                continue
            paginas.extend(int(valor) for valor in ANCORA_PAGINA.findall(texto_parte))
        esperado = list(range(1, total + 1))
        if sorted(paginas) != esperado:
            erros.append(f"Cobertura de páginas divergente em: {relatorio.parent}")
        pendentes = dados.get("paginas_pendentes_de_ocr_ou_revisao", [])
        if pendentes:
            avisos.append(f"PDF com páginas pendentes de OCR ou revisão: {relatorio.parent}: {pendentes}")
        revisao_concluida = bool(dados.get("revisao_visual_concluida", False))
        registro_revisao = relatorio.parent / "REGISTRO-DA-REVISAO.md"
        if not revisao_concluida:
            avisos.append(f"PDF ainda sem revisão visual registrada: {relatorio.parent}")
            if registro_revisao.exists():
                erros.append(f"Há registro de revisão, mas o relatório ainda indica pendência: {registro_revisao}")
        else:
            if not registro_revisao.is_file():
                erros.append(f"Registro da revisão do PDF ausente: {registro_revisao}")
            else:
                texto_registro = registro_revisao.read_text(encoding="utf-8").strip()
                responsavel = str(dados.get("responsavel_revisao", "")).strip()
                if not texto_registro or not responsavel or responsavel not in texto_registro:
                    erros.append(f"Registro da revisão do PDF está vazio ou inconsistente: {registro_revisao}")

    indice_principal = raiz / "03 - PROCESSO JUDICIAL EM MARKDOWN" / "INDICE-DO-PROCESSO.md"
    if relatorios_pdf and indice_principal.is_file():
        texto_indice_principal = indice_principal.read_text(encoding="utf-8")
        texto_indice_decodificado = unquote(texto_indice_principal)
        if "Nenhum processo foi extraído até o momento" in texto_indice_principal:
            erros.append("O índice principal do processo ainda contém o texto inicial, apesar de haver extração.")
        for relatorio in relatorios_pdf:
            link_esperado = (relatorio.parent / "INDICE-DO-PROCESSO.md").relative_to(
                indice_principal.parent
            ).as_posix()
            if relatorio.parent != indice_principal.parent and link_esperado not in texto_indice_decodificado:
                erros.append(
                    f"O índice principal não aponta para a extração: {relatorio.parent.relative_to(raiz)}"
                )

    pasta_documentos = organizadas / "DOCUMENTOS"
    if pasta_documentos.is_dir():
        for arquivo in pasta_documentos.glob("*.pdf"):
            nome = arquivo.name.upper()
            if "_PROCESSO_" in nome or "_AUTOS_" in nome:
                if sha256(arquivo) not in hashes_pdf_extraidos:
                    avisos.append(
                        f"PDF identificado como processo ainda sem extração integral localizada: {arquivo.relative_to(raiz)}"
                    )

    for categoria in ("AUDIOS", "VIDEOS"):
        pasta = organizadas / categoria
        if not pasta.is_dir():
            continue
        for arquivo in pasta.iterdir():
            if not arquivo.is_file():
                continue
            encontrado = ID_NO_NOME.match(arquivo.name)
            if not encontrado:
                continue
            identificador = encontrado.group(1)
            transcricoes = list(
                (raiz / "02 - TRANSCRICOES DE AUDIOS VIDEOS E CONVERSAS").glob(f"{identificador}_*.md")
            )
            if not transcricoes:
                avisos.append(f"Mídia sem transcrição localizada: {arquivo.relative_to(raiz)}")
                continue
            transcricoes_validas = []
            for transcricao in transcricoes:
                try:
                    texto_transcricao = transcricao.read_text(encoding="utf-8").strip()
                except UnicodeDecodeError:
                    continue
                if texto_transcricao and MARCA_TEMPO.search(texto_transcricao):
                    transcricoes_validas.append(transcricao)
            if not transcricoes_validas:
                avisos.append(
                    f"Mídia possui arquivo de transcrição vazio ou sem marcação de tempo: {arquivo.relative_to(raiz)}"
                )

    pasta_conversas = organizadas / "CONVERSAS E EMAILS"
    ids_zip_organizados: set[str] = set()
    if pasta_conversas.is_dir():
        for arquivo in pasta_conversas.iterdir():
            if not arquivo.is_file() or arquivo.suffix.casefold() not in {".zip", ".txt"}:
                continue
            encontrado = ID_NO_NOME.match(arquivo.name)
            if not encontrado:
                continue
            identificador = encontrado.group(1)
            if arquivo.suffix.casefold() == ".zip":
                ids_zip_organizados.add(identificador)
            conversas_md = list(
                (raiz / "02 - TRANSCRICOES DE AUDIOS VIDEOS E CONVERSAS").rglob(
                    f"{identificador}_CONVERSA-INTEGRAL*.md"
                )
            )
            pendencias_zip = list(
                (raiz / "02 - TRANSCRICOES DE AUDIOS VIDEOS E CONVERSAS").rglob(
                    f"{identificador}_PENDENCIA-CONVERSAO-WHATSAPP.md"
                )
            )
            if not conversas_md and not pendencias_zip:
                avisos.append(
                    f"Conversa sem Markdown integral ou pendência persistida: {arquivo.relative_to(raiz)}"
                )
            elif conversas_md:
                validas = []
                for conversa_md in conversas_md:
                    try:
                        if conversa_md.read_text(encoding="utf-8").strip():
                            validas.append(conversa_md)
                    except UnicodeDecodeError:
                        pass
                if not validas:
                    avisos.append(
                        f"Conversa possui Markdown vazio ou inválido: {arquivo.relative_to(raiz)}"
                    )

    manifestos_por_id: dict[str, list[Path]] = {}
    for manifesto in (raiz / "02 - TRANSCRICOES DE AUDIOS VIDEOS E CONVERSAS").rglob(
        "MANIFESTO-DA-EXTRACAO.json"
    ):
        try:
            dados_manifesto = json.loads(manifesto.read_text(encoding="utf-8"))
        except Exception as erro:
            erros.append(f"Manifesto de ZIP inválido: {manifesto.relative_to(raiz)}: {erro}")
            continue
        id_zip = str(dados_manifesto.get("id_prova_zip", ""))
        manifestos_por_id.setdefault(id_zip, []).append(manifesto)
        if not ID.fullmatch(id_zip):
            erros.append(f"Manifesto de WhatsApp sem ID de prova válido: {manifesto.relative_to(raiz)}")
        elif id_zip not in originais_por_id:
            erros.append(f"Manifesto de WhatsApp aponta para prova não registrada: {id_zip}")
        elif dados_manifesto.get("sha256_zip_original") != originais_por_id[id_zip].get("sha256"):
            erros.append(f"ZIP extraído não corresponde aos bytes registrados de {id_zip}.")
        saidas = list(dados_manifesto.get("conversas_markdown", []))
        conversoes = dados_manifesto.get("conversoes", [])
        if not isinstance(conversoes, list):
            erros.append(f"Lista de conversões inválida no manifesto: {manifesto.relative_to(raiz)}")
            conversoes = []
        pendencia = dados_manifesto.get("pendencia_conversao")
        if not saidas and not pendencia:
            erros.append(
                f"Extração de WhatsApp sem conversa Markdown nem pendência registrada: {manifesto.relative_to(raiz)}"
            )
        if pendencia:
            avisos.append(
                f"Conversão do WhatsApp possui pendência registrada: {manifesto.parent / str(pendencia)}"
            )
        markdown_declarados: set[str] = set()
        for conversao in conversoes:
            if not isinstance(conversao, dict):
                erros.append(f"Conversão inválida no manifesto: {manifesto.relative_to(raiz)}")
                continue
            relativo_txt = str(conversao.get("txt_extraido", ""))
            relativo_md = str(conversao.get("markdown_gerado", ""))
            markdown_declarados.add(relativo_md)
            for relativo_item, campo_hash, rotulo in (
                (relativo_txt, "sha256_txt_extraido", "TXT extraído"),
                (relativo_md, "sha256_markdown_gerado", "Markdown da conversa"),
            ):
                destino = (manifesto.parent / Path(relativo_item)).resolve()
                try:
                    destino.relative_to(manifesto.parent.resolve())
                except ValueError:
                    erros.append(f"{rotulo} aponta para fora da extração: {relativo_item}")
                    continue
                if not destino.is_file():
                    erros.append(f"{rotulo} declarado não existe: {destino}")
                    continue
                if sha256(destino) != conversao.get(campo_hash):
                    erros.append(f"{rotulo} foi alterado após a conversão: {destino}")
                if rotulo == "Markdown da conversa":
                    try:
                        texto_conversa = destino.read_text(encoding="utf-8").strip()
                    except UnicodeDecodeError:
                        texto_conversa = ""
                    if not texto_conversa:
                        erros.append(f"Markdown da conversa está vazio ou não está em UTF-8: {destino}")
        if set(map(str, saidas)) != markdown_declarados:
            erros.append(
                f"Lista de Markdown não corresponde aos registros de conversão: {manifesto.relative_to(raiz)}"
            )
        for relativo in [*saidas, *([pendencia] if pendencia else [])]:
            destino_manifesto = (manifesto.parent / Path(str(relativo))).resolve()
            try:
                destino_manifesto.relative_to(manifesto.parent.resolve())
            except ValueError:
                erros.append(
                    f"Saída declarada no manifesto aponta para fora da extração: {manifesto.relative_to(raiz)}: {relativo}"
                )
                continue
            if not destino_manifesto.is_file():
                erros.append(
                    f"Saída declarada no manifesto não existe: {manifesto.relative_to(raiz)}: {relativo}"
                )
        if dados_manifesto.get("revisao_humana_concluida"):
            registro_relativo = dados_manifesto.get("registro_revisao", "REGISTRO-DA-CONFERENCIA-WHATSAPP.md")
            registro = (manifesto.parent / Path(str(registro_relativo))).resolve()
            if not registro.is_file() or not registro.read_text(encoding="utf-8").strip():
                erros.append(f"Registro da conferência do WhatsApp ausente ou vazio: {registro}")

    for identificador, manifestos in manifestos_por_id.items():
        if identificador and len(manifestos) > 1:
            erros.append(f"Há mais de uma extração de WhatsApp para {identificador}: {manifestos}")
    for identificador in sorted(ids_zip_organizados - set(manifestos_por_id)):
        avisos.append(f"ZIP de WhatsApp ainda sem extração segura registrada: {identificador}")

    pendencias_path = raiz / "05 - PERGUNTAS E PENDENCIAS" / "PENDENCIAS-ATUAIS.md"
    if registros and pendencias_path.is_file():
        texto_pendencias = pendencias_path.read_text(encoding="utf-8")
        if "As perguntas serão produzidas depois da leitura do acervo." in texto_pendencias:
            avisos.append("As perguntas específicas pós-leitura ainda não foram produzidas.")

    leia_primeiro = raiz / "LEIA-PRIMEIRO.md"
    if registros and leia_primeiro.is_file():
        texto_leia = leia_primeiro.read_text(encoding="utf-8")
        if "- Organização: NÃO INICIADA" in texto_leia:
            avisos.append("O LEIA-PRIMEIRO.md ainda indica que a organização não foi iniciada.")

    arquivos_navegacao = [
        raiz / "04 - INDICE E CRONOLOGIA" / "RESUMO-OBJETIVO-DO-CASO.md",
        raiz / "04 - INDICE E CRONOLOGIA" / "LINHA-DO-TEMPO.md",
        raiz / "04 - INDICE E CRONOLOGIA" / "MAPA-DE-FATOS-E-PROVAS.md",
    ]
    if registros:
        for caminho in arquivos_navegacao:
            if caminho.is_file() and "[A PREENCHER APÓS A LEITURA]" in caminho.read_text(encoding="utf-8"):
                avisos.append(f"Arquivo de navegação ainda não preenchido após a leitura: {caminho.relative_to(raiz)}")

    status = "REPROVADO" if erros else "INCOMPLETO_COM_PENDENCIAS" if avisos else "APROVADO"
    resultado = {
        "status": status,
        "erros": erros,
        "pendencias": avisos,
        "provas_registradas": len(registros),
        "relatorios_de_pdf": len(relatorios_pdf),
    }
    try:
        atualizar_pendencias(pendencias_path, erros, avisos)
        atualizar_relatorio(
            raiz / "04 - INDICE E CRONOLOGIA" / "RELATORIO-DE-CONFERENCIA.md",
            status,
            len(arquivos_originais),
            registros,
            relatorios_pdf,
            erros,
            avisos,
        )
    except Exception as erro:
        resultado["status"] = "REPROVADO"
        resultado["erros"].append(f"Não foi possível persistir pendências e relatório: {erro}")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 2 if resultado["erros"] else 1 if avisos else 0


if __name__ == "__main__":
    raise SystemExit(main())
