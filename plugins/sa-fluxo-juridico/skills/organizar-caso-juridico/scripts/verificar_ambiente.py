#!/usr/bin/env python3
"""Informa se o ambiente local possui as dependências da etapa solicitada."""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import sys


REQUISITOS = {
    "pdf": [("modulo", "pypdf")],
    "midia": [("executavel", "ffmpeg"), ("executavel", "ffprobe")],
    "teste": [("modulo", "pypdf"), ("modulo", "reportlab")],
}


def localizar(tipo: str, nome: str) -> str | None:
    if tipo == "modulo":
        especificacao = importlib.util.find_spec(nome)
        return especificacao.origin if especificacao else None
    return shutil.which(nome)


def main() -> int:
    parser = argparse.ArgumentParser(description="Confere dependências locais da organização do caso.")
    parser.add_argument("--exigir", action="append", choices=sorted(REQUISITOS), default=[])
    args = parser.parse_args()

    exigencias = args.exigir or ["pdf"]
    itens: list[dict] = []
    ausentes: list[str] = []
    vistos: set[tuple[str, str]] = set()
    for etapa in exigencias:
        for tipo, nome in REQUISITOS[etapa]:
            chave = (tipo, nome)
            if chave in vistos:
                continue
            vistos.add(chave)
            caminho = localizar(tipo, nome)
            itens.append({"tipo": tipo, "nome": nome, "disponivel": bool(caminho), "caminho": caminho})
            if not caminho:
                ausentes.append(nome)

    resultado = {
        "python": sys.executable,
        "versao_python": sys.version.split()[0],
        "etapas_exigidas": exigencias,
        "dependencias": itens,
        "status": "APROVADO" if not ausentes else "DEPENDENCIAS_AUSENTES",
        "ausentes": ausentes,
    }
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0 if not ausentes else 2


if __name__ == "__main__":
    raise SystemExit(main())
