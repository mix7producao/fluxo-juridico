import hashlib
from pathlib import Path
from zipfile import ZipFile

from docx import Document


ROOT = Path(__file__).resolve().parent.parent
REFERENCE = ROOT / "plugins" / "sa-fluxo-juridico" / "assets" / "papeis-timbrados" / "PAPEL-TIMBRADO-OFICIAL-SA-ADVOCACIA.docx"
FINAL = ROOT / "guias" / "MANUAL-DO-ADVOGADO-FLUXO-JURIDICO-SA-ADVOCACIA.docx"
REFERENCE_HASH = "0EE2641279BD55115BEBFB6B42277D21B5E38161D95B67BCD8D5B5B7E5591F97"
ALT_TEXT = ' descr="Marca Sousa Araújo Advocacia, Dra. Lidiane Sousa Araújo e contatos do escritório"'


def main():
    if hashlib.sha256(REFERENCE.read_bytes()).hexdigest().upper() != REFERENCE_HASH:
        raise RuntimeError("O papel timbrado oficial foi alterado.")

    with ZipFile(REFERENCE) as source, ZipFile(FINAL) as output:
        if source.read("word/media/image1.png") != output.read("word/media/image1.png"):
            raise RuntimeError("A imagem do papel timbrado não foi preservada.")
        if source.read("word/_rels/header1.xml.rels") != output.read("word/_rels/header1.xml.rels"):
            raise RuntimeError("A relação do cabeçalho foi alterada.")
        source_header = source.read("word/header1.xml").decode("utf-8")
        output_header = output.read("word/header1.xml").decode("utf-8")
        if output_header.replace(ALT_TEXT, "", 1) != source_header:
            raise RuntimeError("O cabeçalho sofreu alteração não prevista.")

    document = Document(FINAL)
    body = "\n".join(paragraph.text for paragraph in document.paragraphs)
    required = (
        "Guia de instalação no ChatGPT e Claude pessoais",
        "Comece pelo GitHub",
        "https://github.com/mix7producao/fluxo-juridico",
        "Como baixar os arquivos",
        "Instalação no ChatGPT pessoal",
        "Conexão direta com o GitHub no ChatGPT",
        "Instalação no Claude pessoal",
        "PACOTE-UNICO-PARA-CHATGPT-E-CLAUDE.md",
        "PAPEL-TIMBRADO-OFICIAL-SA-ADVOCACIA.docx",
        "Como atualizar no Claude",
        "Para que serve",
        "Como usar em um caso novo",
        "Limite importante",
        "Como atualizar no ChatGPT",
    )
    if not all(item in body for item in required):
        raise RuntimeError("O manual não contém todas as seções obrigatórias.")
    if "[A CONFIRMAR" in body or "TODO" in body:
        raise RuntimeError("O manual contém marcador de pendência indevido.")

    print("TIMBRADO_E_CONTEUDO_APROVADOS")
    print(f"SHA256_FINAL={hashlib.sha256(FINAL.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
