#!/usr/bin/env python3
"""Extrai ZIP de WhatsApp sem path traversal, sobrescrita ou extração aninhada."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import tempfile
import unicodedata
import zipfile
from pathlib import Path, PurePosixPath


RESERVADOS_WINDOWS = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}
CARACTERES_PROIBIDOS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
PADRAO_ID = re.compile(r"^PROVA-\d+$")
ID_NO_NOME = re.compile(r"^(PROVA-\d+)_")


def sha256(caminho: Path) -> str:
    digest = hashlib.sha256()
    with caminho.open("rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(1024 * 1024), b""):
            digest.update(bloco)
    return digest.hexdigest()


def componente_seguro(nome: str) -> str:
    nome = unicodedata.normalize("NFC", nome)
    nome = CARACTERES_PROIBIDOS.sub("_", nome).rstrip(" .")
    if not nome:
        nome = "ITEM-SEM-NOME"
    raiz = nome.split(".", 1)[0].upper()
    if raiz in RESERVADOS_WINDOWS:
        nome = f"_{nome}"
    return nome


def caminho_seguro(nome: str) -> tuple[Path | None, str | None]:
    if "\x00" in nome:
        return None, "nome contém byte nulo"
    normalizado = nome.replace("\\", "/")
    if normalizado.startswith("/") or re.match(r"^[A-Za-z]:", normalizado):
        return None, "caminho absoluto ou com unidade"
    partes = PurePosixPath(normalizado).parts
    if not partes:
        return None, "nome vazio"
    if any(parte in {"..", "."} for parte in partes):
        return None, "segmento de caminho inseguro"
    return Path(*(componente_seguro(parte) for parte in partes)), None


def eh_link(info: zipfile.ZipInfo) -> bool:
    modo = (info.external_attr >> 16) & 0xFFFF
    return stat.S_ISLNK(modo)


def decodificar_txt(caminho: Path) -> tuple[str | None, str | None]:
    dados = caminho.read_bytes()
    for codificacao in ("utf-8-sig", "utf-16"):
        try:
            texto = dados.decode(codificacao)
        except UnicodeDecodeError:
            continue
        if texto.count("\x00") > max(2, len(texto) // 100):
            continue
        return texto, codificacao
    return None, None


def cerca_markdown(texto: str) -> str:
    maior = max((len(item) for item in re.findall(r"`+", texto)), default=0)
    return "`" * max(4, maior + 1)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extrai com segurança um ZIP exportado pelo WhatsApp.")
    parser.add_argument("zip")
    parser.add_argument("pasta_de_saida")
    parser.add_argument("--maximo-arquivos", type=int, default=50_000)
    parser.add_argument("--maximo-total-bytes", type=int, default=25 * 1024**3)
    parser.add_argument("--maximo-arquivo-bytes", type=int, default=4 * 1024**3)
    parser.add_argument("--maxima-taxa-compressao", type=float, default=200.0)
    parser.add_argument("--id-prova", help="ID permanente do ZIP, por exemplo PROVA-0004.")
    args = parser.parse_args()

    if args.id_prova and not PADRAO_ID.fullmatch(args.id_prova):
        raise SystemExit("O ID da prova deve usar o formato PROVA-0001.")

    origem = Path(args.zip).expanduser().resolve()
    if not origem.is_file():
        raise SystemExit(f"ZIP não encontrado: {origem}")

    destino = Path(args.pasta_de_saida).expanduser().resolve()
    if destino.exists() and not destino.is_dir():
        raise SystemExit(f"A saída existe e não é uma pasta: {destino}")
    if destino.exists() and any(destino.iterdir()):
        raise SystemExit(f"A pasta de saída precisa estar vazia: {destino}")
    destino.parent.mkdir(parents=True, exist_ok=True)

    erros: list[dict] = []
    plano: list[tuple[zipfile.ZipInfo, Path]] = []
    nomes_destino: dict[str, str] = {}

    try:
        arquivo_zip = zipfile.ZipFile(origem)
    except (zipfile.BadZipFile, OSError) as erro:
        raise SystemExit(f"ZIP inválido ou inacessível: {erro}") from erro

    with arquivo_zip:
        itens = arquivo_zip.infolist()
        arquivos = [item for item in itens if not item.is_dir()]
        if len(arquivos) > args.maximo_arquivos:
            erros.append({"motivo": "quantidade máxima excedida", "quantidade": len(arquivos)})

        tamanho_total = sum(item.file_size for item in arquivos)
        if tamanho_total > args.maximo_total_bytes:
            erros.append({"motivo": "tamanho total máximo excedido", "tamanho": tamanho_total})

        for info in itens:
            relativo, erro_caminho = caminho_seguro(info.filename)
            if erro_caminho:
                erros.append({"item": info.filename, "motivo": erro_caminho})
                continue
            assert relativo is not None
            if info.flag_bits & 0x1:
                erros.append({"item": info.filename, "motivo": "item criptografado"})
            if eh_link(info):
                erros.append({"item": info.filename, "motivo": "link simbólico não permitido"})
            if not info.is_dir() and info.file_size > args.maximo_arquivo_bytes:
                erros.append({"item": info.filename, "motivo": "arquivo individual excede o limite"})
            if not info.is_dir() and info.file_size:
                taxa = info.file_size / max(info.compress_size, 1)
                if taxa > args.maxima_taxa_compressao:
                    erros.append(
                        {"item": info.filename, "motivo": "taxa de compressão suspeita", "taxa": taxa}
                    )
            chave = relativo.as_posix().casefold()
            anterior = nomes_destino.get(chave)
            if anterior is not None:
                erros.append(
                    {
                        "item": info.filename,
                        "motivo": "colisão de nome após normalização",
                        "colide_com": anterior,
                    }
                )
            else:
                nomes_destino[chave] = info.filename
            plano.append((info, relativo))

        if erros:
            print(json.dumps({"status": "EXTRACAO_RECUSADA", "erros": erros}, ensure_ascii=False, indent=2))
            return 2

        falha_crc = arquivo_zip.testzip()
        if falha_crc:
            print(
                json.dumps(
                    {"status": "EXTRACAO_RECUSADA", "erros": [{"item": falha_crc, "motivo": "falha de CRC"}]},
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 2

        temporario = Path(tempfile.mkdtemp(prefix="whatsapp_", dir=destino.parent))
        manifesto: list[dict] = []
        conversas_markdown: list[str] = []
        conversoes: list[dict] = []
        pendencia_conversao: str | None = None
        try:
            raiz_resolvida = temporario.resolve()
            for info, relativo in plano:
                alvo = (temporario / relativo).resolve()
                try:
                    alvo.relative_to(raiz_resolvida)
                except ValueError as erro:
                    raise RuntimeError(f"Destino fora da pasta autorizada: {info.filename}") from erro

                if info.is_dir():
                    alvo.mkdir(parents=True, exist_ok=True)
                    continue

                alvo.parent.mkdir(parents=True, exist_ok=True)
                if alvo.exists():
                    raise RuntimeError(f"Sobrescrita recusada: {alvo}")
                bytes_gravados = 0
                with arquivo_zip.open(info, "r") as entrada, alvo.open("xb") as saida:
                    while True:
                        bloco = entrada.read(1024 * 1024)
                        if not bloco:
                            break
                        saida.write(bloco)
                        bytes_gravados += len(bloco)
                if bytes_gravados != info.file_size:
                    raise RuntimeError(f"Tamanho divergente após extração: {info.filename}")
                manifesto.append(
                    {
                        "nome_no_zip": info.filename,
                        "caminho_extraido": relativo.as_posix(),
                        "tamanho_bytes": info.file_size,
                        "crc32": f"{info.CRC:08x}",
                        "arquivo_compactado_aninhado": relativo.suffix.casefold() in {".zip", ".7z", ".rar"},
                    }
                )

            id_detectado = args.id_prova
            if not id_detectado:
                encontrado = ID_NO_NOME.match(origem.name)
                id_detectado = encontrado.group(1) if encontrado else "PROVA-A-CONFIRMAR"

            txts = sorted(
                [
                    temporario / Path(item["caminho_extraido"])
                    for item in manifesto
                    if Path(item["caminho_extraido"]).suffix.casefold() == ".txt"
                ],
                key=lambda item: item.as_posix().casefold(),
            )
            derivados = temporario / "MARKDOWN-GERADO"
            motivos_pendencia: list[str] = []
            if not txts:
                motivos_pendencia.append("Nenhum arquivo TXT de conversa foi localizado no ZIP.")
            if len(txts) > 1:
                motivos_pendencia.append(
                    "Mais de um arquivo TXT foi localizado. Todos foram convertidos literalmente, mas é preciso confirmar quais pertencem à conversa principal."
                )

            for numero, txt in enumerate(txts, 1):
                conteudo, codificacao = decodificar_txt(txt)
                if conteudo is None or codificacao is None:
                    motivos_pendencia.append(
                        f"Não foi possível decodificar com segurança o TXT: {txt.relative_to(temporario).as_posix()}."
                    )
                    continue
                if not conteudo.strip():
                    motivos_pendencia.append(
                        f"O TXT está vazio e não pode ser aceito como conversa integral: {txt.relative_to(temporario).as_posix()}."
                    )
                    continue
                derivados.mkdir(parents=True, exist_ok=True)
                sufixo = "" if len(txts) == 1 else f"-{numero:02d}"
                nome_md = f"{id_detectado}_CONVERSA-INTEGRAL{sufixo}.md"
                cerca = cerca_markdown(conteudo)
                texto_md = "\n".join(
                    [
                        f"# {id_detectado}: conversa integral{sufixo}",
                        "",
                        f"- TXT preservado: `{txt.relative_to(temporario).as_posix()}`",
                        f"- Codificação utilizada: `{codificacao}`",
                        "- Status: CONVERSÃO LITERAL AUTOMÁTICA VERIFICADA",
                        "",
                        "O bloco abaixo reproduz integralmente o TXT decodificado. Nenhuma mensagem foi corrigida ou reordenada.",
                        "",
                        cerca,
                        conteudo,
                        cerca,
                        "",
                    ]
                )
                caminho_md = derivados / nome_md
                caminho_md.write_text(texto_md, encoding="utf-8", newline="\n")
                relativo_md = caminho_md.relative_to(temporario).as_posix()
                relativo_txt = txt.relative_to(temporario).as_posix()
                conversas_markdown.append(relativo_md)
                conversoes.append(
                    {
                        "txt_extraido": relativo_txt,
                        "sha256_txt_extraido": sha256(txt),
                        "markdown_gerado": relativo_md,
                        "sha256_markdown_gerado": sha256(caminho_md),
                        "codificacao": codificacao,
                    }
                )

            if motivos_pendencia:
                derivados.mkdir(parents=True, exist_ok=True)
                nome_pendencia = f"{id_detectado}_PENDENCIA-CONVERSAO-WHATSAPP.md"
                caminho_pendencia = derivados / nome_pendencia
                caminho_pendencia.write_text(
                    "\n".join(
                        [
                            f"# {id_detectado}: pendência da conversão do WhatsApp",
                            "",
                            *(f"- [ ] {motivo}" for motivo in motivos_pendencia),
                            "",
                        ]
                    ),
                    encoding="utf-8",
                    newline="\n",
                )
                pendencia_conversao = caminho_pendencia.relative_to(temporario).as_posix()

            (temporario / "MANIFESTO-DA-EXTRACAO.json").write_text(
                json.dumps(
                    {
                        "zip_original": str(origem),
                        "sha256_zip_original": sha256(origem),
                        "quantidade_de_arquivos": len(manifesto),
                        "tamanho_total_bytes": tamanho_total,
                        "itens": manifesto,
                        "id_prova_zip": id_detectado,
                        "conversas_markdown": conversas_markdown,
                        "conversoes": conversoes,
                        "pendencia_conversao": pendencia_conversao,
                        "revisao_humana_concluida": False,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
                newline="\n",
            )
            if destino.exists():
                destino.rmdir()
            temporario.rename(destino)
        except Exception:
            shutil.rmtree(temporario, ignore_errors=True)
            raise

    print(
        json.dumps(
            {
                "status": "EXTRACAO_CONCLUIDA",
                "zip_original": str(origem),
                "pasta_de_saida": str(destino),
                "quantidade_de_arquivos": len(manifesto),
                "tamanho_total_bytes": tamanho_total,
                "conversas_markdown": conversas_markdown,
                "pendencia_conversao": pendencia_conversao,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
