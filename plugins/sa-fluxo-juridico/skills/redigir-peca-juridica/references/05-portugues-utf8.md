# 05. Português do Brasil, acentuação e codificação

## Regra absoluta

Nunca omitir acento gráfico, til, cedilha ou crase, em nenhum tipo de arquivo: DOCX, PDF, ODT, PPTX, XLSX, Markdown, HTML, JSON, CSV, texto puro e strings de script em qualquer linguagem. Vale para títulos, subtítulos, cabeçalhos de tabela, rodapés e corpo do texto.

## Proibição do travessão

O travessão não é usado no corpo do texto. Só é admitido em título, e apenas quando realmente necessário. Substituir por vírgula, dois pontos, ponto e vírgula ou parênteses.

Errado: "O contrato venceu em agosto [travessão] e o réu permaneceu no imóvel."
Certo: "O contrato venceu em agosto e o réu permaneceu no imóvel."

## Erros de acentuação mais frequentes

| Errado | Correto | | Errado | Correto |
|---|---|---|---|---|
| nao | não | | voce | você |
| sao | são | | ja | já |
| ate | até | | tres | três |
| mes | mês | | esta (verbo) | está |
| so (somente) | só | | publico | público |
| unico | único | | ultimo | último |
| proximo | próximo | | necessario | necessário |
| historico | histórico | | basico | básico |
| pratico | prático | | tecnico | técnico |
| analise | análise | | grafico | gráfico |
| video | vídeo | | audio | áudio |
| facil | fácil | | rapido | rápido |
| dificil | difícil | | possivel | possível |
| disponivel | disponível | | conteudo | conteúdo |
| usuario | usuário | | numero | número |
| titulo | título | | codigo | código |
| juridico | jurídico | | judicial (sem acento) | judicial |
| sentenca | sentença | | audiencia | audiência |
| alimentos (sem acento) | alimentos | | inventario | inventário |
| peticao | petição | | contestacao | contestação |
| execucao | execução | | prescricao | prescrição |
| citacao | citação | | intimacao | intimação |

Palavras terminadas em ção, são e tão sempre levam til ou cedilha: ação, atenção, informação, organização, situação, relação, função, solução, construção, direção, produção, comunicação, posição, condição, opção, gestão, decisão, razão, pretensão, extensão.

A mesma regra vale para a maiúscula no início da frase: Não, Ação, Você, São, Já, Até.

## Categorias

- Til: ã, õ (não, então, mão, põe, limões, irmãs)
- Agudo: á, é, í, ó, ú (está, é, país, só, saúde, café)
- Circunflexo: â, ê, ô (câmera, você, pôde, convênio)
- Cedilha: ç (ação, criança, peço, sentença)
- Crase: à (vou à audiência, das 9h às 18h, quanto à alegação)

Atenção à crase em expressões jurídicas frequentes: "quanto à prescrição", "em relação à parte ré", "dá se provimento à apelação", "à luz do art. 5º".

## Fontes e codificação

Fontes admitidas por terem suporte completo a Latin Extended: Arial, Calibri, Times New Roman, Helvetica. Nunca usar Symbol, Wingdings, Webdings ou Courier antigo.

Ao gerar arquivos por código, escrever sempre com UTF-8 explícito:

```python
with open('arquivo.md', 'w', encoding='utf-8') as f:
    f.write(conteudo)
```

Para executar Node.js com conteúdo em português, garantir o locale:

```bash
export LANG=pt_BR.UTF-8
export LC_ALL=C.UTF-8
```

## Validação obrigatória antes de entregar

Executar após gerar qualquer arquivo com conteúdo em português:

```python
import os, sys, glob, zipfile

mojibake = ['\u00c3\u00a9', '\u00c3\u00a7', '\u00c3\u00a3', '\u00c3\u00a1',
            '\u00c3\u00b3', '\u00c3\u00ad', '\u00c3\u00aa', '\u00c3\u00ba',
            '\u00c3\u00a2', '\u00c3\u00b4']

falhas = []
out_dir = '.'  # ajustar para a pasta de saída

for ext in ['md', 'txt', 'js', 'py', 'html', 'json', 'csv']:
    for f in glob.glob(f'{out_dir}/*.{ext}'):
        with open(f, 'r', encoding='utf-8', errors='replace') as fh:
            conteudo = fh.read()
        if any(m in conteudo for m in mojibake):
            falhas.append(os.path.basename(f))

for ext, xml_path in [('docx', 'word/document.xml'),
                      ('pptx', 'ppt/slides/slide1.xml'),
                      ('xlsx', 'xl/sharedStrings.xml')]:
    for f in glob.glob(f'{out_dir}/*.{ext}'):
        try:
            with zipfile.ZipFile(f) as z:
                xml = z.read(xml_path).decode('utf-8')
            if any(m in xml for m in mojibake):
                falhas.append(os.path.basename(f))
        except KeyError:
            pass

print('ERRO DE CODIFICACAO em:', falhas) if falhas else print('Codificacao UTF-8 correta')
```

Se a validação acusar erro, corrigir e reescrever o arquivo antes de apresentar o resultado.

## Checklist de idioma

1. Todos os acentos gráficos estão presentes, inclusive em títulos e tabelas?
2. As cedilhas e os tis estão corretos?
3. As crases foram usadas onde devido?
4. Não há travessão fora de título?
5. Datas, valores e percentuais estão no padrão brasileiro?
6. A validação UTF-8 foi executada e passou?
