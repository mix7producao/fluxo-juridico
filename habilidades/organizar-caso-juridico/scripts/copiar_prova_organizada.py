#!/usr/bin/env python3
"""Cria e confere uma cópia organizada de uma prova já inventariada."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import unicodedata
from datetime import date, datetime, timezone
from pathlib import Path
from uuid import uuid4

sys.dont_write_bytecode = True
from inventariar_originais import escrever_atomico, gerar_inventario_visivel, ler_jsonl


CONTROLE = Path("04 - INDICE E CRONOLOGIA/CONTROLE-TECNICO-DE-INTEGRIDADE.jsonl")
COPIAS = Path("04 - INDICE E CRONOLOGIA/CONTROLE-DAS-COPIAS-ORGANIZADAS.jsonl")
CATEGORIAS = {
    "documento": "DOCUMENTOS",
    "conversa": "CONVERSAS E EMAILS",
    "audio": "AUDIOS",
    "video": "VIDEOS",
    "imagem": "FOTOS E CAPTURAS DE TELA",
    "outro": "OUTROS",
}


def sha256(caminho: Path) -> str:
    digest = hashlib.sha256()
    with caminho.open("rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(1024 * 1024), b""):
            digest.update(bloco)
    return digest.hexdigest()


def slug(texto: str) -> str:
    normalizado = unicodedata.normalize("NFKD", texto)
    ascii_texto = normalizado.encode("ascii", "ignore").decode("ascii").upper()
    seguro = re.sub(r"[^A-Z0-9]+", "-", ascii_texto).strip("-")
    if not seguro:
        raise SystemExit("O tipo e o assunto precisam conter letras ou números.")
    return seguro[:80].rstrip("-")


def ler_registros(caminho: Path) -> list[dict]:
    if not caminho.is_file():
        raise SystemExit(f"Controle técnico não encontrado: {caminho}")
    registros = []
    for numero, linha in enumerate(caminho.read_text(encoding="utf-8").splitlines(), 1):
        if not linha.strip():
            continue
        try:
            item = json.loads(linha)
        except json.JSONDecodeError as erro:
            raise SystemExit(f"JSON inválido na linha {numero}: {erro}") from erro
        if item.get("tipo_registro") == "ARQUIVO_RECEBIDO":
            registros.append(item)
    return registros


def main() -> int:
    parser = argparse.ArgumentParser(description="Copia uma prova para seu nome organizado.")
    parser.add_argument("pasta_do_caso")
    parser.add_argument("id", help="Identificador, por exemplo PROVA-0001.")
    parser.add_argument("categoria", choices=sorted(CATEGORIAS))
    parser.add_argument("tipo", help="Tipo objetivo, por exemplo AUDIO ou CONTRATO.")
    parser.add_argument("assunto", help="Descrição neutra e curta.")
    parser.add_argument("--data", default="DATA-NAO-CONFIRMADA")
    args = parser.parse_args()

    raiz = Path(args.pasta_do_caso).expanduser().resolve()
    registros = ler_registros(raiz / CONTROLE)
    correspondentes = [item for item in registros if item.get("id") == args.id]
    if len(correspondentes) != 1:
        raise SystemExit(f"Era esperado um registro único para {args.id}; encontrados: {len(correspondentes)}")
    registro = correspondentes[0]

    origem = (raiz / Path(registro["caminho_original"])).resolve()
    pasta_originais = (raiz / "00 - ORIGINAIS RECEBIDOS - NAO ALTERAR").resolve()
    try:
        origem.relative_to(pasta_originais)
    except ValueError as erro:
        raise SystemExit("O registro de origem aponta para fora da pasta autorizada.") from erro
    if not origem.is_file():
        raise SystemExit(f"Original não encontrado: {origem}")
    codigo_origem = sha256(origem)
    if codigo_origem != registro.get("sha256"):
        raise SystemExit("O original foi alterado depois do inventário. Cópia recusada.")

    if args.data != "DATA-NAO-CONFIRMADA" and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.data):
        raise SystemExit("A data deve usar AAAA-MM-DD ou DATA-NAO-CONFIRMADA.")
    if args.data != "DATA-NAO-CONFIRMADA":
        try:
            date.fromisoformat(args.data)
        except ValueError as erro:
            raise SystemExit("A data informada não existe no calendário.") from erro

    categoria = CATEGORIAS[args.categoria]
    raiz_organizadas = (raiz / "01 - PROVAS ORGANIZADAS").resolve()
    pasta_destino = (raiz_organizadas / categoria).resolve()
    pasta_destino.mkdir(parents=True, exist_ok=True)
    extensao = origem.suffix
    nome = f"{args.id}_{args.data}_{slug(args.tipo)}_{slug(args.assunto)}{extensao}"
    destino = pasta_destino / nome

    caminho_copias = raiz / COPIAS
    eventos_existentes = [
        item
        for item in ler_jsonl(caminho_copias)
        if item.get("tipo_registro") == "COPIA_ORGANIZADA" and item.get("id") == args.id
    ]
    arquivos_existentes = [
        arquivo
        for arquivo in raiz_organizadas.rglob(f"{args.id}_*")
        if arquivo.is_file()
    ]

    if arquivos_existentes or eventos_existentes:
        if len(arquivos_existentes) == 1 and len(eventos_existentes) == 1:
            existente = arquivos_existentes[0].resolve()
            evento = eventos_existentes[0]
            caminho_evento = (raiz / Path(str(evento.get("caminho_copia_organizada", "")))).resolve()
            if (
                existente == destino.resolve()
                and caminho_evento == existente
                and sha256(existente) == codigo_origem
                and evento.get("sha256_copia") == codigo_origem
            ):
                escrever_atomico(
                    raiz / "04 - INDICE E CRONOLOGIA" / "INVENTARIO-DE-PROVAS.md",
                    gerar_inventario_visivel(registros, ler_jsonl(caminho_copias)),
                )
                print(
                    json.dumps(
                        {"status": "COPIA_JA_EXISTIA_E_FOI_CONFERIDA", "destino": str(existente)},
                        ensure_ascii=False,
                        indent=2,
                    )
                )
                return 0
        encontrados = [str(item.relative_to(raiz)) for item in arquivos_existentes]
        raise SystemExit(
            f"{args.id} já possui cópia organizada ou registro incompatível. "
            f"Nenhuma segunda cópia foi criada. Arquivos encontrados: {encontrados}"
        )

    if destino.exists():
        raise SystemExit(f"Destino já existe com conteúdo diferente: {destino}")

    temporario = pasta_destino / f".{nome}.{uuid4().hex}.tmp"
    try:
        shutil.copy2(origem, temporario)
        codigo_copia = sha256(temporario)
        if codigo_copia != codigo_origem:
            raise RuntimeError("A cópia não corresponde ao original.")
        os.replace(temporario, destino)
    finally:
        if temporario.exists():
            temporario.unlink()

    evento = {
        "tipo_registro": "COPIA_ORGANIZADA",
        "id": args.id,
        "caminho_original": registro["caminho_original"],
        "caminho_copia_organizada": destino.relative_to(raiz).as_posix(),
        "sha256_original": codigo_origem,
        "sha256_copia": codigo_origem,
        "copia_identica_verificada": True,
        "registrado_em_utc": datetime.now(timezone.utc).isoformat(),
    }
    caminho_copias.parent.mkdir(parents=True, exist_ok=True)
    with caminho_copias.open("a", encoding="utf-8", newline="\n") as saida:
        saida.write(json.dumps(evento, ensure_ascii=False, sort_keys=True) + "\n")

    escrever_atomico(
        raiz / "04 - INDICE E CRONOLOGIA" / "INVENTARIO-DE-PROVAS.md",
        gerar_inventario_visivel(registros, ler_jsonl(caminho_copias)),
    )

    print(json.dumps({"status": "COPIA_CRIADA_E_CONFERIDA", **evento}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
