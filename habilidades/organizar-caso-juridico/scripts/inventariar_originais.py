#!/usr/bin/env python3
"""Atribui IDs estáveis e calcula hashes dos arquivos originais de um caso."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


ORIGINAIS = "00 - ORIGINAIS RECEBIDOS - NAO ALTERAR"
CONTROLE = Path("04 - INDICE E CRONOLOGIA/CONTROLE-TECNICO-DE-INTEGRIDADE.jsonl")
COPIAS = Path("04 - INDICE E CRONOLOGIA/CONTROLE-DAS-COPIAS-ORGANIZADAS.jsonl")
ESTADO = Path("04 - INDICE E CRONOLOGIA/ESTADO-DA-NUMERACAO.json")
INVENTARIO = Path("04 - INDICE E CRONOLOGIA/INVENTARIO-TECNICO-DE-ORIGINAIS.md")
INVENTARIO_VISIVEL = Path("04 - INDICE E CRONOLOGIA/INVENTARIO-DE-PROVAS.md")
PADRAO_ID = re.compile(r"^PROVA-(\d+)$")


def sha256(caminho: Path) -> str:
    digest = hashlib.sha256()
    with caminho.open("rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(1024 * 1024), b""):
            digest.update(bloco)
    return digest.hexdigest()


def ordenar(caminho: Path) -> str:
    return unicodedata.normalize("NFC", caminho.as_posix()).casefold()


def ler_jsonl(caminho: Path) -> list[dict]:
    if not caminho.exists():
        return []
    registros: list[dict] = []
    for numero, linha in enumerate(caminho.read_text(encoding="utf-8").splitlines(), 1):
        if not linha.strip():
            continue
        try:
            item = json.loads(linha)
        except json.JSONDecodeError as erro:
            raise SystemExit(f"JSON inválido em {caminho}, linha {numero}: {erro}") from erro
        if not isinstance(item, dict):
            raise SystemExit(f"Registro inválido em {caminho}, linha {numero}: era esperado um objeto JSON.")
        registros.append(item)
    return registros


def escrever_atomico(caminho: Path, conteudo: str) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    temporario = caminho.with_name(f".{caminho.name}.{uuid4().hex}.tmp")
    temporario.write_text(conteudo, encoding="utf-8", newline="\n")
    os.replace(temporario, caminho)


def maior_numero(registros: list[dict]) -> int:
    maior = 0
    for registro in registros:
        encontrado = PADRAO_ID.match(str(registro.get("id", "")))
        if encontrado:
            maior = max(maior, int(encontrado.group(1)))
    return maior


def gerar_inventario(registros: list[dict]) -> str:
    linhas = [
        "# Inventário técnico de originais",
        "",
        "Este arquivo é gerado automaticamente. Datas do sistema não provam a data do fato.",
        "",
        "| ID | Caminho original | Tamanho | SHA-256 | Duplicado exato | Registrado em |",
        "|---|---|---:|---|---|---|",
    ]
    for registro in sorted(registros, key=lambda item: item.get("id", "")):
        caminho = str(registro.get("caminho_original", "")).replace("|", "\\|")
        duplicado = registro.get("duplicado_exato_de") or "Não"
        linhas.append(
            f"| {registro.get('id')} | `{caminho}` | {registro.get('tamanho_bytes')} | "
            f"`{registro.get('sha256')}` | {duplicado} | {registro.get('registrado_em_utc')} |"
        )
    linhas.extend(
        [
            "",
            "O hash confirma igualdade de bytes quando comparado. Ele não prova sozinho autoria, veracidade ou licitude.",
            "",
        ]
    )
    return "\n".join(linhas)


def campo_tabela(valor: object) -> str:
    return str(valor).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def gerar_inventario_visivel(registros: list[dict], copias: list[dict]) -> str:
    copias_por_id: dict[str, list[dict]] = {}
    for copia in copias:
        if copia.get("tipo_registro") != "COPIA_ORGANIZADA":
            continue
        copias_por_id.setdefault(str(copia.get("id", "")), []).append(copia)

    linhas = [
        "# Inventário de provas",
        "",
        "Este arquivo é sincronizado automaticamente. A análise do conteúdo fica nas fichas das provas e no mapa de fatos e provas.",
        "",
        "| ID | Nome recebido | Original preservado | Cópia organizada | Origem informada | Duplicidade | Situação |",
        "|---|---|---|---|---|---|---|",
    ]
    for registro in sorted(registros, key=lambda item: item.get("id", "")):
        identificador = str(registro.get("id", ""))
        eventos = copias_por_id.get(identificador, [])
        if len(eventos) == 1:
            caminho_copia = f"`{campo_tabela(eventos[0].get('caminho_copia_organizada', ''))}`"
            situacao = "CÓPIA ORGANIZADA"
        elif len(eventos) > 1:
            caminho_copia = "[CONFLITO: MAIS DE UMA CÓPIA REGISTRADA]"
            situacao = "ERRO DE DUPLICIDADE"
        else:
            caminho_copia = "[A ORGANIZAR]"
            situacao = "NÃO EXAMINADA"
        duplicado = registro.get("duplicado_exato_de") or "Não"
        linhas.append(
            f"| {identificador} | {campo_tabela(registro.get('nome_original', ''))} | "
            f"`{campo_tabela(registro.get('caminho_original', ''))}` | {caminho_copia} | "
            f"{campo_tabela(registro.get('origem', '[A CONFIRMAR]'))} | {campo_tabela(duplicado)} | {situacao} |"
        )
    linhas.extend(
        [
            "",
            "`PROVA-0000` é o identificador permanente. A numeração `Doc. 00` pertence a cada peça ou protocolo.",
            "",
        ]
    )
    return "\n".join(linhas)


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventaria os originais sem alterá-los.")
    parser.add_argument("pasta_do_caso")
    args = parser.parse_args()

    raiz = Path(args.pasta_do_caso).expanduser().resolve()
    pasta_originais = raiz / ORIGINAIS
    if not pasta_originais.is_dir():
        raise SystemExit(f"Pasta de originais não encontrada: {pasta_originais}")

    caminho_controle = raiz / CONTROLE
    registros = ler_jsonl(caminho_controle)
    por_caminho = {registro["caminho_original"]: registro for registro in registros}
    por_hash: dict[str, dict] = {}
    for registro in registros:
        por_hash.setdefault(registro["sha256"], registro)

    proximo = maior_numero(registros) + 1
    caminho_estado = raiz / ESTADO
    if caminho_estado.exists():
        estado_anterior = json.loads(caminho_estado.read_text(encoding="utf-8"))
        proximo = max(proximo, int(estado_anterior.get("proximo_id", 1)))

    arquivos = sorted((p for p in pasta_originais.rglob("*") if p.is_file()), key=ordenar)
    novos: list[dict] = []
    alterados: list[dict] = []

    for arquivo in arquivos:
        relativo = arquivo.relative_to(raiz).as_posix()
        tamanho = arquivo.stat().st_size
        codigo = sha256(arquivo)
        anterior = por_caminho.get(relativo)
        if anterior:
            if anterior.get("sha256") != codigo or anterior.get("tamanho_bytes") != tamanho:
                alterados.append(
                    {
                        "id": anterior.get("id"),
                        "caminho": relativo,
                        "sha256_anterior": anterior.get("sha256"),
                        "sha256_atual": codigo,
                    }
                )
            continue

        identificador = f"PROVA-{proximo:04d}"
        proximo += 1
        duplicado = por_hash.get(codigo)
        registro = {
            "id": identificador,
            "tipo_registro": "ARQUIVO_RECEBIDO",
            "nome_original": arquivo.name,
            "caminho_original": relativo,
            "tamanho_bytes": tamanho,
            "sha256": codigo,
            "modificado_em_utc": datetime.fromtimestamp(
                arquivo.stat().st_mtime, tz=timezone.utc
            ).isoformat(),
            "registrado_em_utc": datetime.now(timezone.utc).isoformat(),
            "fornecido_por": "[A CONFIRMAR]",
            "origem": "[A CONFIRMAR]",
            "duplicado_exato_de": duplicado.get("id") if duplicado else None,
            "observacao": "A data técnica do arquivo não comprova a data do fato.",
        }
        novos.append(registro)
        registros.append(registro)
        por_caminho[relativo] = registro
        por_hash.setdefault(codigo, registro)

    if alterados:
        print(json.dumps({"erro": "ORIGINAL_ALTERADO_APOS_REGISTRO", "itens": alterados}, ensure_ascii=False, indent=2))
        return 2

    if novos:
        caminho_controle.parent.mkdir(parents=True, exist_ok=True)
        with caminho_controle.open("a", encoding="utf-8", newline="\n") as saida:
            for registro in novos:
                saida.write(json.dumps(registro, ensure_ascii=False, sort_keys=True) + "\n")

    ids = [registro.get("id") for registro in registros]
    estado = {
        "proximo_id": proximo,
        "identificadores_ja_utilizados": ids,
    }
    escrever_atomico(caminho_estado, json.dumps(estado, ensure_ascii=False, indent=2) + "\n")
    escrever_atomico(raiz / INVENTARIO, gerar_inventario(registros))
    copias = ler_jsonl(raiz / COPIAS)
    escrever_atomico(raiz / INVENTARIO_VISIVEL, gerar_inventario_visivel(registros, copias))

    print(
        json.dumps(
            {
                "arquivos_encontrados": len(arquivos),
                "novos_registros": len(novos),
                "total_registrado": len(registros),
                "proximo_id": f"PROVA-{proximo:04d}",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
