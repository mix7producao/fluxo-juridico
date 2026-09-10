# AGENTS.md

Instruções permanentes de trabalho para agentes de IA (Codex, Claude, ChatGPT e similares) que atuam nesta pasta.

Leia este arquivo por completo antes de produzir qualquer conteúdo. Ele é a fonte de verdade. Os arquivos da pasta `instrucoes/` detalham cada bloco e devem ser consultados conforme a tarefa.

## 1. Quem é a profissional

Dra. Lidiane Sousa Araújo, advogada, OAB/DF 34.876, fundadora da Sousa Araújo Advocacia (SA Advocacia), com sede em Planaltina, Brasília/DF.

Áreas de atuação: direito de família e sucessões (guarda compartilhada, alimentos, alienação parental, divórcio, inventário, cumprimento de sentença), direito imobiliário e regularização fundiária (usucapião, due diligence, contratos), registro de marcas no INPI, homologação de sentença estrangeira no STJ, consultoria jurídica para pequenas e médias empresas, direito do consumidor e locação.

Detalhes completos em `instrucoes/01-perfil-escritorio.md`.

## 2. Escopo: três modos de trabalho

O agente precisa identificar, antes de escrever, em qual modo está.

**Modo Peça Jurídica.** Vale quando o pedido envolve petição inicial, contestação, réplica, impugnação, recurso, notificação extrajudicial, contrato, parecer, memorando jurídico, acordo ou documento equivalente. Neste modo, aplicam se obrigatoriamente as 11 regras de estruturação (`instrucoes/03-regras-peca-otimizada-ia.md`), as regras de validação de provas e jurisprudência (`instrucoes/04-validacao-provas-e-jurisprudencia.md`) e o padrão de formatação (`instrucoes/02-formatacao-documentos.md`).

**Modo Conteúdo.** Vale para redes sociais, roteiros de Reels, legendas, e-mails, textos institucionais, propostas comerciais e material educativo. Neste modo, as 11 regras jurídicas NÃO se aplicam. Siga `instrucoes/09-escopo-conteudo-redes.md`.

**Modo Organização de Caso.** Vale quando o pedido envolve abertura, recebimento, preservação, identificação, transcrição, indexação ou triagem do acervo de um caso novo. Antes de qualquer redação, siga `instrucoes/10-abertura-e-organizacao-de-caso.md` e, no Codex, use a habilidade `habilidades/organizar-caso-juridico`. Neste modo, os arquivos originais são intocáveis, o processo em PDF deve ser integralmente convertido para Markdown e as perguntas complementares só são feitas depois da leitura do acervo.

Em ambos os modos valem sempre as regras de idioma do item 3.

## 3. Regras invioláveis (valem em qualquer entrega)

1. Português do Brasil em norma padrão, com acentuação gráfica completa em títulos, subtítulos, tabelas, notas de rodapé e corpo do texto. Sem exceção.
2. Codificação UTF-8 em qualquer arquivo gerado. Fontes com suporte a Latin Extended (Arial, Calibri, Times New Roman, Helvetica).
3. Proibido o uso de travessão. O travessão só é admitido em títulos, e apenas quando for realmente necessário. No corpo do texto, use vírgula, dois pontos ou parênteses.
4. Nunca inventar dados. Jurisprudência, número de processo, data, valor, artigo de lei e nome de parte só entram no documento se estiverem no material fornecido ou se forem verificados em fonte oficial. Quando faltar informação, escreva `[A CONFIRMAR: descrição do dado]` no documento e liste a pendência na resposta do chat.
5. Nunca alterar a estratégia jurídica definida pela advogada sem sinalizar de forma expressa. Sugestões de mérito vão fora da peça, na resposta do chat.
6. Não usar linguagem rebuscada, metáfora, latinismo desnecessário ou frase de efeito. Clareza vence erudição, sempre.
7. Não inserir imagem, print ou infográfico no corpo de peça jurídica. Transcrever o conteúdo e remeter a imagem aos anexos.
8. Dados de clientes são sigilosos. Não reproduzir nome, CPF, endereço ou número de processo em conteúdo de redes sociais, exemplo público ou material de divulgação.
9. Ao final de toda peça jurídica, rodar o checklist de `instrucoes/08-checklist-final.md` e informar o resultado.
10. Entregar peça jurídica em arquivo editável (.docx) sempre que possível, no padrão de formatação do escritório, e não apenas colada no chat.
11. Em caso novo, usar `PROVA-0001` como identificador interno permanente e reservar `Doc. 01` para a numeração dos anexos de cada peça ou protocolo.

## 4. Índice da pasta

| Arquivo | Quando usar |
|---|---|
| `instrucoes/01-perfil-escritorio.md` | Identidade, qualificação, assinatura, endereçamentos e foros habituais |
| `instrucoes/02-formatacao-documentos.md` | Fonte, margens, espaçamento, timbrado, numeração, nomeação de arquivos |
| `instrucoes/03-regras-peca-otimizada-ia.md` | As 11 regras de estruturação de peça para leitura por IA e por magistrado |
| `instrucoes/04-validacao-provas-e-jurisprudencia.md` | Como validar prova, cadeia de custódia, cálculo e precedente |
| `instrucoes/05-portugues-utf8.md` | Acentuação, erros frequentes, validação técnica de codificação |
| `instrucoes/06-fluxo-de-trabalho.md` | Passo a passo da produção de uma peça, da triagem à entrega |
| `instrucoes/07-modelos-estruturas.md` | Esqueletos prontos por tipo de peça |
| `instrucoes/08-checklist-final.md` | Auditoria obrigatória antes da entrega |
| `instrucoes/09-escopo-conteudo-redes.md` | Conteúdo de redes sociais e limites éticos da publicidade advocatícia |
| `instrucoes/10-abertura-e-organizacao-de-caso.md` | Abertura de caso, preservação, transcrição, índice e perguntas posteriores |

## 5. Fluxo padrão resumido

1. Em caso novo, preservar e organizar o acervo conforme `instrucoes/10-abertura-e-organizacao-de-caso.md`.
2. Ler o material fornecido por inteiro antes de escrever.
3. Listar os documentos disponíveis e o que cada um comprova.
4. Montar a linha do tempo do caso.
5. Definir a tese e o enquadramento legal.
6. Verificar cada precedente e cada dispositivo legal em fonte oficial.
7. Redigir aplicando as 11 regras.
8. Auditar com o checklist final e entregar, apontando as pendências.

Detalhamento em `instrucoes/06-fluxo-de-trabalho.md`.

## 6. Como responder

Resposta curta e direta no chat, com o essencial primeiro. A peça vai no arquivo, não no meio de explicações. Depois da entrega, informar apenas: o que foi produzido, as pendências de informação e, se houver, os riscos jurídicos identificados.
