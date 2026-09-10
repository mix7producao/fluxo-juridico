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
WHITE = RGBColor(255, 255, 255)
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
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.65)
    p.paragraph_format.first_line_indent = Cm(-0.35)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.12
    marker = p.add_run("• ")
    set_run_font(marker, size=11, color=BLACK)
    run = p.add_run(text)
    set_run_font(run, size=11, color=BLACK)
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


def add_link(doc, url, label=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.keep_with_next = True
    relationship_id = p.part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), relationship_id)
    run = OxmlElement("w:r")
    run_properties = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    run_properties.append(color)
    run_properties.append(underline)
    run.append(run_properties)
    text = OxmlElement("w:t")
    text.text = label or url
    run.append(text)
    hyperlink.append(run)
    p._p.append(hyperlink)
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

    title_style = doc.styles["Title"]
    title_style.font.color.rgb = BLACK
    title_properties = title_style.element.get_or_add_pPr()
    title_border = title_properties.find(qn("w:pBdr"))
    if title_border is not None:
        title_properties.remove(title_border)

    add_paragraph(doc, "\u00a0", size=1, color=WHITE, space_after=46)
    add_paragraph(doc, "Guia de instalação no ChatGPT e Claude pessoais", style="Title", size=21, bold=True, space_after=4)
    add_paragraph(doc, "Primeiro instale. Depois veja para que serve e como usar.", size=12, color=GRAY, space_after=16)
    add_paragraph(
        doc,
        "Este guia é para contas pessoais do ChatGPT e do Claude. Não exige conta Business, programação ou conhecimento técnico.",
        size=11,
        space_after=12,
    )

    add_heading(doc, "Comece pelo GitHub")
    add_paragraph(doc, "Clique no link abaixo. Ele abre o pacote oficial que contém as instruções e os modelos do escritório.", size=11, space_after=2)
    add_link(doc, "https://github.com/mix7producao/fluxo-juridico", "ABRIR O PACOTE NO GITHUB")
    add_paragraph(doc, "Endereço completo: https://github.com/mix7producao/fluxo-juridico", size=9.5, color=GRAY, space_after=8)

    add_heading(doc, "Como baixar os arquivos")
    add_numbered(doc, 1, "Entre na sua conta do GitHub", "se a página pedir acesso.")
    add_numbered(doc, 2, "Na página do pacote", "clique no botão verde Code.")
    add_numbered(doc, 3, "Clique em Download ZIP", "e aguarde o download terminar.")
    add_numbered(doc, 4, "Abra a pasta Downloads", "clique com o botão direito no ZIP e escolha Extrair tudo.")
    add_numbered(doc, 5, "Abra a pasta extraída", "e localize os dois arquivos indicados abaixo.")
    add_bullet(doc, "PACOTE-UNICO-PARA-CHATGPT-E-CLAUDE.md, na primeira pasta.")
    add_bullet(doc, "PAPEL-TIMBRADO-OFICIAL-SA-ADVOCACIA.docx, dentro de plugins, sa-fluxo-juridico, assets e papeis-timbrados.")
    add_paragraph(doc, "Se aparecer Página não encontrada, o repositório ainda não foi liberado para a sua conta do GitHub. Peça acesso ao responsável pelo escritório.", size=10.5, bold=True, space_after=0)

    doc.add_section(WD_SECTION.NEW_PAGE)
    add_paragraph(doc, "\u00a0", size=1, color=WHITE, space_after=46)
    add_heading(doc, "Instalação no ChatGPT pessoal")
    add_numbered(doc, 1, "Entre no ChatGPT", "com sua conta pessoal.")
    add_numbered(doc, 2, "Proteja os dados dos clientes", "clique na sua foto, abra Configurações e Controles de dados e desative Melhorar o modelo para todos.")
    add_numbered(doc, 3, "Clique em Novo projeto", "na barra lateral.")
    add_numbered(doc, 4, "Dê um nome ao projeto", "por exemplo, CASO 2026-001.")
    add_numbered(doc, 5, "Adicione os dois arquivos baixados do GitHub", "use Adicionar arquivos ou Adicionar fonte e selecione o pacote e o papel timbrado.")
    add_numbered(doc, 6, "Abra as configurações do projeto", "e cole a instrução abaixo no campo Instruções do projeto.")
    add_prompt(doc, "Leia e siga integralmente o arquivo PACOTE-UNICO-PARA-CHATGPT-E-CLAUDE.md. Use o papel timbrado oficial nas peças em Word. Nunca invente informações.")
    add_numbered(doc, 7, "Inicie um novo chat dentro do projeto", "e use a frase de teste abaixo.")
    add_prompt(doc, "Confirme que leu as instruções da SA Advocacia e diga, em poucas linhas, quais tarefas pode realizar.")

    add_heading(doc, "Conexão direta com o GitHub no ChatGPT")
    add_paragraph(doc, "Se GitHub aparecer em Configurações e Apps, clique em Conectar, autorize sua conta e permita o acesso ao repositório fluxo-juridico. Essa opção varia conforme o plano e pode não aparecer no chat comum. O envio dos dois arquivos acima continua sendo o caminho mais simples e confiável.", size=10.5)

    add_heading(doc, "Como atualizar no ChatGPT")
    add_paragraph(doc, "Quando o escritório avisar que o pacote mudou, volte ao GitHub, baixe o ZIP atualizado, exclua do projeto o arquivo PACOTE-UNICO-PARA-CHATGPT-E-CLAUDE.md antigo e envie o novo.", size=10.5, space_after=0)

    doc.add_section(WD_SECTION.NEW_PAGE)
    add_paragraph(doc, "\u00a0", size=1, color=WHITE, space_after=46)
    add_heading(doc, "Instalação no Claude pessoal")
    add_numbered(doc, 1, "Entre no Claude", "com sua conta pessoal e abra Projetos.")
    add_numbered(doc, 2, "Proteja os dados dos clientes", "abra Configurações e Privacidade e deixe desativada qualquer opção que autorize o uso das conversas para melhorar o Claude.")
    add_numbered(doc, 3, "Clique em Novo projeto", "ou New Project.")
    add_numbered(doc, 4, "Dê um nome ao projeto", "por exemplo, CASO 2026-001.")
    add_numbered(doc, 5, "Conecte o GitHub", "na área Conhecimento do projeto, clique no sinal de mais e escolha GitHub.")
    add_numbered(doc, 6, "Cole o link do pacote", "use https://github.com/mix7producao/fluxo-juridico e autorize o acesso quando solicitado.")
    add_numbered(doc, 7, "Selecione as instruções", "escolha o arquivo PACOTE-UNICO-PARA-CHATGPT-E-CLAUDE.md e confirme.")
    add_numbered(doc, 8, "Envie o papel timbrado", "adicione o arquivo DOCX que foi baixado do GitHub.")
    add_numbered(doc, 9, "Defina as instruções do projeto", "clique em Set project instructions e cole a instrução abaixo.")
    add_prompt(doc, "Leia e siga integralmente o arquivo PACOTE-UNICO-PARA-CHATGPT-E-CLAUDE.md. Use o papel timbrado oficial nas peças em Word. Nunca invente informações.")
    add_numbered(doc, 10, "Inicie um novo chat dentro do projeto", "e use a frase de teste abaixo.")
    add_prompt(doc, "Confirme que leu as instruções da SA Advocacia e diga, em poucas linhas, quais tarefas pode realizar.")

    add_heading(doc, "Como atualizar no Claude")
    add_paragraph(doc, "Clique em Sync ou Sincronizar na conexão do GitHub antes de começar um trabalho novo. O Claude buscará a versão atual das instruções selecionadas. Troque o papel timbrado manualmente somente quando houver uma versão nova.", size=10.5)

    add_heading(doc, "Atenção ao separar os casos")
    add_paragraph(doc, "Crie um projeto diferente para cada cliente ou processo. Repita a configuração em cada projeto. Isso evita misturar informações de casos diferentes.", size=11, bold=True, space_after=0)

    doc.add_section(WD_SECTION.NEW_PAGE)
    add_paragraph(doc, "\u00a0", size=1, color=WHITE, space_after=46)
    add_heading(doc, "Para que serve")
    for text in (
        "Organizar os arquivos que você enviar, incluindo processos em PDF, conversas exportadas do WhatsApp, documentos, áudios, vídeos e imagens.",
        "Criar índice, resumo, linha do tempo, lista do que cada prova demonstra e perguntas sobre o que ainda estiver faltando.",
        "Identificar as provas de forma permanente, como PROVA-0001, sem alterar os arquivos originais.",
        "Preparar e revisar peças jurídicas em Word com a estrutura, a formatação e o papel timbrado oficial do escritório.",
        "Separar fatos comprovados de alegações e marcar claramente qualquer informação que ainda precise de confirmação.",
    ):
        add_bullet(doc, text)

    add_heading(doc, "Como usar em um caso novo")
    add_numbered(doc, 1, "Abra o projeto daquele caso", "nunca use o projeto de outro cliente.")
    add_numbered(doc, 2, "Envie tudo o que tiver", "inclusive o processo completo, documentos, conversas, ZIP do WhatsApp, áudios, vídeos e imagens.")
    add_numbered(doc, 3, "Peça a organização", "envie a frase abaixo depois de terminar todos os anexos.")
    add_prompt(doc, "Quero abrir e organizar um novo caso jurídico. Primeiro confira o que enviei e me lembre, de forma simples, o que pode estar faltando. Só comece quando eu escrever PODE ORGANIZAR.")
    add_numbered(doc, 4, "Responda às perguntas complementares", "elas serão feitas somente depois da leitura do material enviado.")
    add_numbered(doc, 5, "Peça a peça jurídica", "quando a organização estiver concluída, use a frase abaixo.")
    add_prompt(doc, "Analise o caso organizado e produza a peça jurídica adequada em Word, usando o papel timbrado oficial. Não invente informações e liste tudo que ainda depende de confirmação.")

    add_heading(doc, "Limite importante")
    add_paragraph(doc, "O ChatGPT e o Claude pessoais somente conseguem analisar os arquivos que você enviar ao projeto ou ao chat. Eles não abrem sozinhos uma pasta do seu computador. A advogada responsável deve revisar a peça antes de assinar ou protocolar.", size=10.5, bold=True)

    doc.core_properties.title = "Guia de instalação no ChatGPT e Claude pessoais"
    doc.core_properties.subject = "Instalação e uso do Fluxo Jurídico em contas pessoais"
    doc.core_properties.author = "Sousa Araújo Advocacia"
    doc.save(OUTPUT)
    preservar_timbrado_e_adicionar_descricao()
    print(OUTPUT)


if __name__ == "__main__":
    main()
