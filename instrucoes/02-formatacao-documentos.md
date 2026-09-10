# 02. Padrão de formatação de documentos

## Configuração de página

- Formato: A4 (210 mm x 297 mm)
- Margens ABNT NBR 14724: superior 3 cm, inferior 2 cm, esquerda 3 cm, direita 2 cm
- Quando usar papel timbrado da SA Advocacia, ajustar a margem superior para não invadir o cabeçalho do timbrado

Em DOCX gerado por código, os valores em DXA são: largura 11906, altura 16838, margem superior 1701, inferior 1134, esquerda 1701, direita 1134.

## Tipografia

- Fonte do corpo: Times New Roman, 12 pt (padrão do escritório para peças processuais)
- Alternativa aceita quando o documento for institucional ou contratual: Arial 12 pt
- Espaçamento entre linhas: 1,5
- Alinhamento do corpo: justificado
- Recuo de primeira linha do parágrafo: 1,25 cm
- Espaçamento entre parágrafos: 0 pt antes, 6 pt depois
- Títulos de seção: caixa alta, negrito, centralizados ou alinhados à esquerda, com espaçamento de 12 pt antes
- Citação direta longa: recuo de 4 cm, fonte 10 pt, espaçamento simples, sem aspas
- Nunca usar fonte sem suporte a Latin Extended (Symbol, Wingdings, Webdings, Courier antigo)

## Numeração e hierarquia

Estrutura obrigatória em peças processuais, em algarismos romanos para as seções principais e decimal para os subitens:

```
I. DA SÍNTESE (EMENTA)
II. DOS FATOS
   2.1. ...
   2.2. ...
III. DO DIREITO
   3.1. ...
IV. DOS PEDIDOS
V. DAS PROVAS
VI. DO VALOR DA CAUSA
```

Cada parágrafo relevante pode receber numeração sequencial contínua quando a peça for longa, facilitando a referência cruzada pelo juízo e pela parte contrária.

## Negrito estratégico

Destacar em negrito apenas: nomes das partes na primeira menção, datas decisivas, valores, teses centrais, o pedido principal e os dispositivos legais mais importantes. O teste de qualidade é simples: ler apenas os trechos em negrito deve permitir compreender o caso. Excesso de negrito anula o efeito.

## Tabelas

Usar tabela para cronologia, quadro de pedidos, planilha de débito, comparativo de propostas e índice de documentos. Cabeçalho em negrito. Em documentos .docx, aplicar bordas simples e evitar mesclagem de células, que atrapalha a extração automática de texto.

## Elementos proibidos no corpo da peça

- Imagem, print, gráfico ou infográfico. Transcrever o conteúdo e remeter aos anexos.
- Travessão.
- Nota de rodapé com informação essencial. O que é essencial vai no corpo.
- Marca d'água ou fundo colorido.

## Formatação de dados

- Datas: 10/02/2026 no corpo técnico, ou 10 de fevereiro de 2026 quando por extenso no fecho.
- Valores: R$ 1.400,00 (ponto de milhar, vírgula decimal). Em pedidos, repetir por extenso: R$ 1.400,00 (mil e quatrocentos reais).
- Processos: número CNJ completo, sem abreviação.
- Percentuais: 40% (sem espaço antes do símbolo).
- Legislação: Lei nº 8.245/1991, art. 62, inciso II, alínea "a". Código: art. 1.694 do Código Civil.

## Arquivos de saída

- Peça processual: .docx com timbrado do escritório e, quando solicitado, .pdf gerado a partir dele.
- Nome do arquivo, padrão sugerido: `AAAA-MM-DD_TipoDaPeca_NomeDoCliente.docx`. Exemplo: `2026-09-09_Contestacao_FranciscoCorreia.docx`.
- Contrato e notificação: .docx editável, com campos variáveis entre colchetes quando faltar dado.
- Sempre validar a codificação UTF-8 antes de entregar, conforme `05-portugues-utf8.md`.
