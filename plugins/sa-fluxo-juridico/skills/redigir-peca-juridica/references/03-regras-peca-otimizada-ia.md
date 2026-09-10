# 03. As 11 regras de estruturação da peça jurídica

Estas regras existem por um motivo técnico: magistrados e assessores usam modelos de linguagem para resumir e triar peças. Uma peça mal estruturada perde argumento no resumo. Cada regra corrige uma falha conhecida de processamento por IA. Não é enfeite.

Aplicar as 11 regras em toda petição, contestação, réplica, impugnação, recurso, notificação e contrato.

---

## Regra 1. Ementa no início

Logo após o endereçamento e antes dos fatos, inserir de 3 a 6 linhas resumindo o caso inteiro com o que ele tem de estritamente importante: quem pede, contra quem, o que pede, com base em qual fundamento e qual o resultado pretendido.

Funciona como resumo executivo e garante que a informação essencial seja lida mesmo quando o restante for truncado.

Verificação: a peça começa com ementa? Se não, falhou.

**Exemplo.** "Trata se de ação de despejo por falta de pagamento cumulada com cobrança, ajuizada por Valdir Machado de Araújo contra Kelvin Victor de Souza, com fundamento no art. 9º, inciso III, da Lei nº 8.245/1991. O contrato de locação venceu em 10/08/2026 e o réu permanece no imóvel sem pagar os aluguéis de julho e agosto de 2026 e o IPTU do período. Houve notificação extrajudicial em 01/09/2026, com prazo de 15 dias, não atendida. Requer se a desocupação do imóvel e a condenação ao pagamento do débito locatício atualizado."

## Regra 2. Imagem vira anexo (crítica)

Zero imagens no corpo da peça. Modelos de linguagem processam imagem muito pior que texto e podem simplesmente ignorar o dado visual ou gerar erro de leitura.

Sempre que houver print de conversa, foto, gráfico ou infográfico, transcrever o conteúdo relevante em texto e remeter a imagem aos anexos, com referência ao documento.

Verificação: existe "conforme imagem", "conforme print", "conforme infográfico"? Se sim, falhou.

**Antes.** "Conforme print de WhatsApp anexo, o réu admitiu o débito."

**Depois.** "Conforme conversa de WhatsApp transcrita a seguir (print anexo, Doc. 05):

Réu (15/03/2026, 14h35): 'Realmente estou devendo os dois aluguéis, vou acertar no fim do mês.'
Autor (15/03/2026, 14h37): 'São julho e agosto, mais o IPTU.'
Réu (15/03/2026, 14h40): 'Eu sei, me dá um prazo.'"

## Regra 3. Hierarquia numérica clara

Estruturar o documento com numeração hierárquica que separe de forma inequívoca fatos, fundamentos jurídicos e pedidos. Ver a estrutura padrão em `02-formatacao-documentos.md`.

Verificação: fatos, direito e pedidos estão em seções distintas e numeradas? Se não, falhou.

## Regra 4. Negrito estratégico

Destacar em negrito os termos-chave e as informações mais importantes, com moderação.

Verificação: ler apenas os negritos permite entender o caso? Se não, falhou.

Ressalva: quando a peça for longa e depender de destaque, incluir observação de que a formatação pode não ser preservada pelo sistema de extração de texto do juízo. Por isso, a informação essencial nunca pode depender apenas do negrito.

## Regra 5. Cronologia em tabela

Depois de narrar os fatos em texto corrido, apresentar tabela com três colunas: data, evento e documento do anexo que comprova o evento.

Verificação: a cronologia está apenas em parágrafo corrido? Se sim, falhou.

| Data | Evento | Documento |
|---|---|---|
| 10/02/2026 | Celebração do contrato de locação, prazo de 6 meses, aluguel de R$ 1.400,00 | Doc. 02 |
| 05/07/2026 | Vencimento do aluguel de julho, não pago | Doc. 03 |
| 01/09/2026 | Notificação extrajudicial com prazo de 15 dias | Doc. 06 |

Toda linha da tabela precisa ter documento correspondente. Evento sem documento deve ser assinalado como `[sem prova documental]` e a advogada deve ser avisada.

## Regra 6. Quadro de pedidos estruturado

Após formular os pedidos no texto, consolidar em tabela com colunas de pedido, fundamento legal (lei e artigo) e valor.

| Pedido | Fundamento legal | Valor |
|---|---|---|
| Rescisão do contrato e despejo do imóvel | Lei nº 8.245/1991, art. 9º, III | Não pecuniário |
| Aluguéis vencidos de julho e agosto de 2026 | Lei nº 8.245/1991, art. 62, I | R$ 2.800,00 |
| IPTU do período | Cláusula 5ª do contrato | R$ 420,00 |
| **Valor total da causa** | | **R$ 3.220,00** |

Verificação: os pedidos estão apenas em parágrafo extenso? Se sim, falhou.

## Regra 7. Síntese documental

Antes da assinatura, listar todos os documentos anexados em formato de índice, indicando o que cada um comprova. Facilita a referência cruzada pelo juízo.

```
DOCUMENTOS ANEXOS
Doc. 01: Procuração e documentos pessoais do autor.
Doc. 02: Contrato de locação de 10/02/2026, comprova o vínculo e o valor do aluguel.
Doc. 03: Recibos e extratos, comprovam a inadimplência de julho e agosto de 2026.
Doc. 06: Notificação extrajudicial e comprovante de recebimento, comprovam a mora e a ciência do réu.
```

## Regra 8. Jurisprudência estruturada

Ao citar precedente, incluir toda a indexação disponível: tribunal, órgão julgador, número do tema ou súmula quando houver, classe e número do recurso, data de julgamento, nome do relator e data de publicação.

Conferir sempre a existência real do julgado, em fonte oficial, antes de citar. Citação parcial é o principal vetor de alucinação de IA e o principal risco de credibilidade perante o juízo.

**Antes.** "Conforme o STJ no REsp 1234567, é devida a indenização."

**Depois.** "Conforme entendimento do Superior Tribunal de Justiça firmado no Tema 123 (REsp 1.234.567/SP, Terceira Turma, julgado em 10/03/2020, Relator Ministro Fulano de Tal, DJe de 15/03/2020)."

Se algum campo não puder ser verificado, não citar o julgado. Em nenhuma hipótese preencher com dado provável.

## Regra 9. Distinguishing literal

Ao usar jurisprudência, transcrever entre aspas o trecho relevante do precedente, incluindo a contextualização fática, e em seguida explicar de forma objetiva por que os fatos do caso concreto são similares, ponto a ponto.

Modelo:

> "[trecho literal do acórdão, com a moldura fática]"

"A hipótese dos autos é idêntica à do precedente pelos seguintes pontos: (a) em ambos os casos houve posse mansa e pacífica superior a cinco anos; (b) em ambos o imóvel é utilizado para moradia da família; (c) em ambos não há oposição do proprietário registral; (d) em ambos a área é inferior a 250 m². Aplica se, portanto, o mesmo entendimento."

Quando o precedente for invocado pela parte contrária e não se aplicar, fazer o distinguishing inverso, apontando as diferenças fáticas pela mesma técnica.

## Regra 10. Linguagem direta

Parágrafos curtos, no máximo 8 linhas. Frases objetivas, no máximo 3 linhas. Sem metáfora, sem latinismo desnecessário, sem ambiguidade, sem adjetivação emocional.

Verificação: há parágrafo com mais de 8 linhas ou frase com mais de 3 linhas? Se sim, reescrever.

## Regra 11. Justiça gratuita com título próprio

Em toda peça que contiver pedido de gratuidade de justiça, abrir título específico para fundamentar o pedido e mencionar as comprovações da hipossuficiência.

O título deve conter: (a) fundamento legal (arts. 98 a 100 do CPC e art. 5º, LXXIV, da Constituição Federal); (b) a situação econômica concreta da parte, com dados objetivos de renda e despesa; (c) a lista dos documentos que comprovam a hipossuficiência; (d) quando for o caso, a ressalva de que a presunção do art. 99, § 3º, do CPC milita em favor da pessoa natural.

Documentos usualmente citados: extratos bancários dos últimos três meses, declaração de imposto de renda ou comprovante de isenção, carteira de trabalho, comprovante de desemprego ou de benefício assistencial, declaração de moradia de favor ou contrato de aluguel, comprovantes de despesas fixas (energia, água, escola, medicamentos), declaração de hipossuficiência firmada pela parte.

Atenção prática: a gratuidade pode ser revogada em grau recursal quando a comprovação for frágil. Por isso, sempre anexar prova documental, e não apenas a declaração.

---

## Relatório de conformidade

Quando a tarefa for revisar ou otimizar uma peça existente, entregar em três blocos:

**Bloco 1. Relatório de conformidade.** Para cada uma das 11 regras: status (cumprida ou não cumprida), diagnóstico do que foi encontrado e problema específico. Ao final, resumo com o total de regras cumpridas e o nível de otimização (baixo, médio ou alto).

**Bloco 2. Peça otimizada completa,** com todas as correções aplicadas.

**Bloco 3. Relatório de mudanças,** no formato antes e depois, item por item.

Restrições na otimização: não inventar dados, não alterar o mérito dos argumentos, não remover conteúdo jurídico relevante. Quando faltar informação para completar uma citação, marcar `[A CONFIRMAR: pesquisa jurisprudencial]`.
