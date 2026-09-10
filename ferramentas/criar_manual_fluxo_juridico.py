from copy import deepcopy
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "plugins" / "sa-fluxo-juridico" / "assets" / "papeis-timbrados" / "PAPEL-TIMBRADO-OFICIAL-SA-ADVOCACIA.docx"
OUTPUT = ROOT / "guias" / "MANUAL-DO-ADVOGADO-FLUXO-JURIDICO-SA-ADVOCACIA.docx"

BLACK = RGBColor(0, 0, 0)
GRAY = RGBColor(89, 89, 89)
BEIGE = "D9C9BA"
LIGHT_BEIGE = "F7F3F0"
LIGHT_GRAY = "D9D9D9"


def set_run_font(run, name="Arial", size=None, bold=None, color=None, italic=None):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:ascii"), name)
    run._element.rPr.rFonts.set(qn("w:hAnsi"), name)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if color is not None:
        run.font.color.rgb = color
    if italic is not None:
        run.italic = italic


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_border(cell, color=LIGHT_GRAY, size="6"):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right"):
        tag = qn(f"w:{edge}")
        element = borders.find(tag)
        if element is None:
            element = OxmlElement(f"w:{edge}")
            borders.append(element)
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), size)
        element.set(qn("w:color"), color)


def set_cell_margins(cell, top=120, start=140, bottom=120, end=140):
    tc_pr = cell._tc.get_or_add_tcPr()
    margins = tc_pr.first_child_found_in("w:tcMar")
    if margins is None:
        margins = OxmlElement("w:tcMar")
        tc_pr.append(margins)
    for side, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = margins.find(qn(f"w:{side}"))
        if node is None:
            node = OxmlElement(f"w:{side}")
            margins.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def format_table(table, widths, header=True):
    table.autofit = False
    for row_index, row in enumerate(table.rows):
        for col_index, cell in enumerate(row.cells):
            cell.width = widths[col_index]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell)
            set_cell_border(cell)
            if header and row_index == 0:
                set_cell_shading(cell, BEIGE)
            elif row_index % 2 == 0:
                set_cell_shading(cell, LIGHT_BEIGE)
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.space_after = Pt(0)
                paragraph.paragraph_format.space_before = Pt(0)
                for run in paragraph.runs:
                    set_run_font(run, size=10.5, bold=(header and row_index == 0), color=BLACK)
    if header:
        tr_pr = table.rows[0]._tr.get_or_add_trPr()
        tbl_header = OxmlElement("w:tblHeader")
        tbl_header.set(qn("w:val"), "true")
        tr_pr.append(tbl_header)


def clear_body(doc):
    body = doc._element.body
    for child in list(body):
        if child.tag != qn("w:sectPr"):
            body.remove(child)


def add_paragraph(doc, text="", style=None, size=11, bold=False, color=BLACK, space_before=0, space_after=8, alignment=None, italic=False):
    p = doc.add_paragraph(style=style)
    if alignment is not None:
        p.alignment = alignment
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold, color=color, italic=italic)
    return p


def add_heading(doc, text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14 if level == 1 else 10)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    set_run_font(run, size=14 if level == 1 else 12, bold=True, color=BLACK)
    return p


def add_bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.12
    for run in p.runs:
        set_run_font(run, size=11, color=BLACK)
    if not p.runs:
        run = p.add_run(text)
        set_run_font(run, size=11, color=BLACK)
    else:
        p.runs[-1].text = text
    return p


def add_numbered(doc, number, title, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.15
    r1 = p.add_run(f"{number}. ")
    set_run_font(r1, size=11, bold=True)
    r2 = p.add_run(title)
    set_run_font(r2, size=11, bold=True)
    r3 = p.add_run(f": {text}")
    set_run_font(r3, size=11)
    return p


def add_prompt(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.55)
    p.paragraph_format.right_indent = Cm(0.55)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(7)
    p.paragraph_format.line_spacing = 1.1
    run = p.add_run(text)
    set_run_font(run, name="Courier New", size=10.5, color=BLACK)
    return p


def preservar_timbrado_e_adicionar_descricao():
    """Restaura a arte do timbrado e adiciona texto alternativo sem mudança visual."""
    partes = ("word/header1.xml", "word/_rels/header1.xml.rels", "word/media/image1.png")
    with ZipFile(TEMPLATE, "r") as fonte, ZipFile(OUTPUT, "r") as destino:
        conteudos = {item.filename: destino.read(item.filename) for item in destino.infolist()}
        for parte in partes:
            conteudos[parte] = fonte.read(parte)

    cabecalho = conteudos["word/header1.xml"].decode("utf-8")
    cabecalho = cabecalho.replace(
        'name="Picture 1"',
        'name="Picture 1" descr="Marca Sousa Araújo Advocacia, Dra. Lidiane Sousa Araújo e contatos do escritório"',
        1,
    )
    conteudos["word/header1.xml"] = cabecalho.encode("utf-8")

    pacote = BytesIO()
    with ZipFile(OUTPUT, "r") as destino, ZipFile(pacote, "w", ZIP_DEFLATED) as novo:
        for item in destino.infolist():
            novo.writestr(item, conteudos[item.filename])
    OUTPUT.write_bytes(pacote.getvalue())


def main():
    if not TEMPLATE.is_file():
        raise FileNotFoundError(f"Modelo não encontrado: {TEMPLATE}")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = Document(TEMPLATE)
    clear_body(doc)

    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    normal.font.size = Pt(11)

    add_paragraph(doc, "Manual do Fluxo Jurídico", size=22, bold=True, space_after=4)
    add_paragraph(doc, "Como organizar um caso e pedir uma peça jurídica com segurança", size=12, color=GRAY, space_after=16)
    add_paragraph(
        doc,
        "Este manual mostra, em linguagem simples, como usar as ferramentas do escritório. Você não precisa entender programação. Basta enviar os documentos, seguir o roteiro e revisar o resultado antes de utilizar a peça.",
        size=11,
        space_after=12,
    )

    add_heading(doc, "O que você passa a ter")
    for text in (
        "Uma pasta de caso organizada, com os originais preservados.",
        "Provas numeradas de forma permanente, como PROVA-0001 e PROVA-0002.",
        "Processos, conversas, áudios e vídeos organizados para consulta posterior.",
        "Resumo do caso, linha do tempo, índice de provas e lista de pendências.",
        "Peças jurídicas em Word, seguindo o padrão do escritório e o papel timbrado oficial.",
    ):
        add_bullet(doc, text)

    add_heading(doc, "Antes de começar")
    add_paragraph(doc, "Você precisa de uma pasta no computador para cada caso e acesso ao ChatGPT ou ao Claude configurado pelo escritório. Nunca envie documentos de clientes para o GitHub.", size=11, space_after=7)
    add_paragraph(doc, "Ao receber documentos, coloque tudo na pasta do caso: processo completo, conversas, áudios, vídeos, fotos, contratos, comprovantes, decisões e intimações.", size=11, space_after=10)

    add_heading(doc, "Passo a passo para organizar um caso")
    table = doc.add_table(rows=1, cols=3)
    table.rows[0].cells[0].text = "Nº"
    table.rows[0].cells[1].text = "O que você faz"
    table.rows[0].cells[2].text = "O que a ferramenta entrega"
    rows = (
        ("1", "Crie uma pasta com o nome interno do caso.", "Uma estrutura segura para receber tudo."),
        ("2", "Coloque todos os arquivos recebidos nessa pasta.", "Nada é descartado ou alterado nos originais."),
        ("3", "No WhatsApp, exporte a conversa com mídias e guarde o arquivo ZIP intacto.", "A conversa pode ser organizada e transcrita sem perder o arquivo original."),
        ("4", "Abra uma conversa nova e peça a abertura do caso.", "A ferramenta mostra um lembrete do que conferir antes de organizar."),
        ("5", "Quando terminar de enviar tudo, escreva PODE ORGANIZAR.", "Índice, cronologia, provas identificadas, transcrições e pendências."),
        ("6", "Leia o resumo e responda às perguntas que ficaram pendentes.", "Contexto completo para análise e redação."),
    )
    for row in rows:
        cells = table.add_row().cells
        for index, value in enumerate(row):
            cells[index].text = value
    format_table(table, (Cm(1.3), Cm(7.0), Cm(7.0)))
    for row in table.rows[1:]:
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_heading(doc, "Frase para abrir um caso")
    add_prompt(doc, "Quero abrir e organizar um novo caso jurídico.")

    add_heading(doc, "Como exportar o WhatsApp")
    add_numbered(doc, 1, "Abra a conversa", "no WhatsApp.")
    add_numbered(doc, 2, "Abra o menu", "e escolha Mais ou Exportar conversa, conforme o aparelho.")
    add_numbered(doc, 3, "Escolha incluir mídias", "para preservar imagens, áudios e vídeos junto com a conversa.")
    add_numbered(doc, 4, "Guarde o arquivo ZIP", "sem renomear ou retirar arquivos de dentro dele.")

    add_heading(doc, "Passo a passo para pedir uma peça jurídica")
    add_numbered(doc, 1, "Aguarde a organização terminar", "e leia o resumo, a cronologia e as pendências.")
    add_numbered(doc, 2, "Informe o objetivo", "por exemplo, petição inicial, contestação, réplica, acordo ou recurso.")
    add_numbered(doc, 3, "Informe prazo, audiência ou urgência", "se houver.")
    add_numbered(doc, 4, "Peça a produção em Word", "usando o caso já organizado.")

    add_heading(doc, "Frase para pedir uma peça")
    add_prompt(doc, "Analise o caso organizado e produza a peça jurídica adequada em Word. Não invente informações. Antes de concluir, liste as pendências que dependem de confirmação da advogada.")

    doc.add_page_break()
    add_heading(doc, "O que a IA faz e o que a advogada confere")
    roles = doc.add_table(rows=1, cols=2)
    roles.rows[0].cells[0].text = "A IA prepara"
    roles.rows[0].cells[1].text = "A advogada confere"
    role_rows = (
        ("Organização, índices, transcrições e cronologia.", "Se todos os documentos importantes foram recebidos."),
        ("Rascunho da peça, estrutura, formatação e relação entre fatos e provas.", "Estratégia, fatos, pedidos, valores, prazos e documentos anexados."),
        ("Uso de uma cópia do papel timbrado oficial e revisão visual do Word.", "Versão final antes de assinar ou protocolar."),
    )
    for left, right in role_rows:
        cells = roles.add_row().cells
        cells[0].text = left
        cells[1].text = right
    format_table(roles, (Cm(7.65), Cm(7.65)))

    add_heading(doc, "Regra de sigilo")
    add_paragraph(doc, "O GitHub guarda somente o manual, as instruções e os modelos vazios. Processos, conversas, provas, documentos pessoais e dados de clientes ficam exclusivamente na pasta de cada caso.", size=11, bold=True, space_after=0)

    doc.core_properties.title = "Manual do Fluxo Jurídico"
    doc.core_properties.subject = "Uso do fluxo de organização de casos e criação de peças jurídicas"
    doc.core_properties.author = "Sousa Araújo Advocacia"
    doc.save(OUTPUT)
    preservar_timbrado_e_adicionar_descricao()
    print(OUTPUT)


if __name__ == "__main__":
    main()
