#!/usr/bin/env python3
"""Registra conferência humana de uma conversão de WhatsApp sem apagar o histórico."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


MANIFESTO = "MANIFESTO-DA-EXTRACAO.json"
REGISTRO = "REGISTRO-DA-CONFERENCIA-WHATSAPP.md"


def sha256(caminho: Path) -> str:
    digest = hashlib.sha256()
    with caminho.open("rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(1024 * 1024), b""):
            digest.update(bloco)
    return digest.hexdigest()


def gravar_atomico(caminho: Path, conteudo: str) -> None:
    temporario = caminho.with_name(f".{caminho.name}.{uuid4().hex}.tmp")
    temporario.write_text(conteudo, encoding="utf-8", newline="\n")
    os.replace(temporario, caminho)


def campo(valor: str, nome: str) -> str:
    texto = " ".join(valor.replace("\r", " ").replace("\n", " ").split())
    if not texto:
        raise SystemExit(f"Informe {nome}.")
    return texto


def caminho_interno(pasta: Path, relativo: object) -> Path:
    bruto = Path(str(relativo))
    if bruto.is_absolute() or ".." in bruto.parts:
        raise SystemExit(f"Caminho inválido no manifesto: {bruto}")
    destino = (pasta / bruto).resolve()
    try:
        destino.relative_to(pasta)
    except ValueError as erro:
        raise SystemExit(f"Caminho fora da extração: {bruto}") from erro
    return destino


def main() -> int:
    parser = argparse.ArgumentParser(description="Registra a conferência da conversa exportada do WhatsApp.")
    parser.add_argument("pasta_da_extracao")
    parser.add_argument("--responsavel", required=True)
    parser.add_argument("--observacao", required=True)
    parser.add_argument(
        "--txt-principal",
        help="Caminho do TXT principal quando o ZIP possuir mais de um candidato.",
    )
    parser.add_argument("--confirmo-conferencia-integral", action="store_true")
    args = parser.parse_args()

    if not args.confirmo_conferencia_integral:
        raise SystemExit(
            "Nada foi alterado. Use --confirmo-conferencia-integral somente depois de comparar o Markdown com o TXT extraído."
        )

    pasta = Path(args.pasta_da_extracao).expanduser().resolve()
    if not pasta.is_dir():
        raise SystemExit(f"Pasta da extração não encontrada: {pasta}")
    caminho_manifesto = pasta / MANIFESTO
    if not caminho_manifesto.is_file():
        raise SystemExit(f"Manifesto não encontrado: {caminho_manifesto}")
    try:
        manifesto = json.loads(caminho_manifesto.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as erro:
        raise SystemExit(f"Manifesto inválido: {erro}") from erro
    if not isinstance(manifesto, dict):
        raise SystemExit("O manifesto deve conter um objeto JSON.")
    if manifesto.get("revisao_humana_concluida"):
        raise SystemExit("A conferência humana já foi registrada. Nada foi alterado.")

    conversoes = manifesto.get("conversoes", [])
    if not isinstance(conversoes, list) or not conversoes:
        raise SystemExit(
            "Não existe TXT convertido para conferir. Solicite nova exportação integral do WhatsApp, registre-a como nova prova e faça nova extração."
        )
    for conversao in conversoes:
        if not isinstance(conversao, dict):
            raise SystemExit("Há conversão inválida no manifesto.")
        txt = caminho_interno(pasta, conversao.get("txt_extraido", ""))
        markdown = caminho_interno(pasta, conversao.get("markdown_gerado", ""))
        if not txt.is_file() or not markdown.is_file():
            raise SystemExit("TXT ou Markdown declarado no manifesto não foi localizado.")
        if sha256(txt) != conversao.get("sha256_txt_extraido"):
            raise SystemExit(f"O TXT extraído foi alterado: {txt}")
        if sha256(markdown) != conversao.get("sha256_markdown_gerado"):
            raise SystemExit(f"O Markdown da conversa foi alterado após a conversão: {markdown}")
        if not markdown.read_text(encoding="utf-8").strip():
            raise SystemExit(f"O Markdown da conversa está vazio: {markdown}")

    pendencia_original = manifesto.get("pendencia_conversao")
    principal: dict | None = None
    if len(conversoes) > 1:
        if not args.txt_principal:
            raise SystemExit("Há mais de um TXT. Informe --txt-principal com o caminho confirmado pela pessoa responsável.")
        candidatos = [
            item
            for item in conversoes
            if str(item.get("txt_extraido")) == args.txt_principal
            or Path(str(item.get("txt_extraido"))).name == args.txt_principal
        ]
        if len(candidatos) != 1:
            raise SystemExit("O TXT principal informado não corresponde de forma única ao manifesto.")
        principal = candidatos[0]
    elif args.txt_principal:
        unico = conversoes[0]
        if args.txt_principal not in {str(unico.get("txt_extraido")), Path(str(unico.get("txt_extraido"))).name}:
            raise SystemExit("O TXT principal informado não corresponde ao único TXT convertido.")
        principal = unico
    else:
        principal = conversoes[0]

    if pendencia_original:
        pendencia_path = caminho_interno(pasta, pendencia_original)
        texto_pendencia = pendencia_path.read_text(encoding="utf-8") if pendencia_path.is_file() else ""
        if "Nenhum arquivo TXT" in texto_pendencia or "Não foi possível decodificar" in texto_pendencia or "está vazio" in texto_pendencia:
            raise SystemExit(
                "A pendência não pode ser resolvida por confirmação. Solicite nova exportação, registre-a como nova prova e faça nova extração."
            )

    caminho_registro = pasta / REGISTRO
    if caminho_registro.exists():
        raise SystemExit(f"Já existe um registro de conferência, que foi preservado: {caminho_registro}")
    responsavel = campo(args.responsavel, "o responsável")
    observacao = campo(args.observacao, "uma observação")
    data = datetime.now(timezone.utc).isoformat(timespec="seconds")
    registro = "\n".join(
        [
            "# Registro da conferência do WhatsApp",
            "",
            f"- Prova: {manifesto.get('id_prova_zip', '[A CONFIRMAR]')}",
            f"- Responsável: {responsavel}",
            f"- Data UTC: {data}",
            f"- TXT principal: `{principal.get('txt_extraido')}`",
            f"- Markdown conferido: `{principal.get('markdown_gerado')}`",
            f"- Observação: {observacao}",
            "",
            "O ZIP e o TXT originais permanecem preservados.",
            "",
        ]
    )

    manifesto["pendencia_conversao_original"] = pendencia_original
    manifesto["pendencia_conversao"] = None
    manifesto["revisao_humana_concluida"] = True
    manifesto["responsavel_revisao"] = responsavel
    manifesto["data_revisao_utc"] = data
    manifesto["observacao_revisao"] = observacao
    manifesto["txt_principal_confirmado"] = principal.get("txt_extraido")
    manifesto["registro_revisao"] = REGISTRO
    gravar_atomico(caminho_registro, registro)
    gravar_atomico(caminho_manifesto, json.dumps(manifesto, ensure_ascii=False, indent=2) + "\n")

    print(
        json.dumps(
            {
                "status": "CONFERENCIA_WHATSAPP_REGISTRADA",
                "prova": manifesto.get("id_prova_zip"),
                "txt_principal": principal.get("txt_extraido"),
                "registro": str(caminho_registro),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
