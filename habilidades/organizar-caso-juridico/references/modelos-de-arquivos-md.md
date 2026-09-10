# Modelos dos arquivos Markdown do caso

Use estes campos como esquema. Remova somente se forem comprovadamente inaplicáveis. Mantenha `[A CONFIRMAR: descrição]` quando faltar informação.

## `LEIA-PRIMEIRO.md`

```markdown
# Leia primeiro: [nome interno do caso]

## Para começar

1. Use Terra ou outro modelo equilibrado para organizar esta pasta.
2. Coloque tudo o que recebeu em `00 - ORIGINAIS RECEBIDOS - NAO ALTERAR`.
3. Para WhatsApp, exporte a conversa inteira com mídias e coloque o ZIP sem modificá-lo.
4. Inclua o PDF integral do processo, além de áudios, vídeos, fotografias, contratos, comprovantes, planilhas, e-mails, decisões e intimações.
5. Informe imediatamente qualquer prazo, audiência ou risco urgente.
6. Quando terminar, diga `PODE ORGANIZAR`.

Sol ou modelo de alto raciocínio será usado na análise jurídica. Astra ou modelo de máxima capacidade fica reservado para caso complexo ou revisão final sensível.

## Situação atual

- Organização: [NÃO INICIADA | EM ANDAMENTO | INCOMPLETA COM PENDÊNCIAS | CONCLUÍDA]
- Área provável: [A CONFIRMAR]
- Prazo ou audiência: [A CONFIRMAR]
- Última atualização: [data e hora]
- Modelo sugerido para a próxima etapa: [nível e justificativa curta]

## Como consultar este caso

1. Leia o resumo objetivo.
2. Consulte o mapa de fatos e provas.
3. Abra somente as provas citadas na tarefa.
4. Confira no original qualquer trecho decisivo antes de usá-lo em peça.

## Atalhos

- [Resumo objetivo](04%20-%20INDICE%20E%20CRONOLOGIA/RESUMO-OBJETIVO-DO-CASO.md)
- [Inventário de provas](04%20-%20INDICE%20E%20CRONOLOGIA/INVENTARIO-DE-PROVAS.md)
- [Linha do tempo](04%20-%20INDICE%20E%20CRONOLOGIA/LINHA-DO-TEMPO.md)
- [Mapa de fatos e provas](04%20-%20INDICE%20E%20CRONOLOGIA/MAPA-DE-FATOS-E-PROVAS.md)
- [Índice do processo](03%20-%20PROCESSO%20JUDICIAL%20EM%20MARKDOWN/INDICE-DO-PROCESSO.md)
- [Perguntas e pendências](05%20-%20PERGUNTAS%20E%20PENDENCIAS/PENDENCIAS-ATUAIS.md)
```

## `INVENTARIO-DE-PROVAS.md`

```markdown
# Inventário de provas

Este arquivo é sincronizado automaticamente. A análise do conteúdo fica nas fichas das provas e no mapa de fatos e provas.

| ID | Nome recebido | Original preservado | Cópia organizada | Origem informada | Duplicidade | Situação |
|---|---|---|---|---|---|---|
| PROVA-0001 | contrato.pdf | [caminho] | [A ORGANIZAR] | [A CONFIRMAR] | Não | NÃO EXAMINADA |
```

Não escreva análise jurídica neste inventário automático. Use as fichas individuais e o mapa de fatos e provas.

## Ficha individual de prova

Nome sugerido: `PROVA-0001_FICHA.md`.

```markdown
# PROVA-0001: [descrição neutra]

## Arquivos relacionados

- Original: [caminho e nome recebido]
- Cópia organizada: [caminho]
- Derivados: [transcrição, OCR ou descrição]

## Origem e integridade

- Fornecido por: [A CONFIRMAR]
- Forma de obtenção: [A CONFIRMAR]
- Data de recebimento: [A CONFIRMAR]
- Cópia idêntica verificada: [SIM | NÃO | PENDENTE]
- Observações técnicas: [sem hash na ficha visível, salvo necessidade]

## Conteúdo objetivo

[descrição fiel, sem conclusão jurídica]

## Localizadores importantes

| Página ou tempo | Conteúdo | Status da conferência |
|---|---|---|
| [p. 1 ou 00:01:23] | [síntese] | [automática ou conferida] |

## O que pode ajudar a demonstrar

- [fato]

## O que pode contradizer

- [fato ou versão]

## Limitações

- [recorte, ausência de contexto, baixa qualidade, origem não confirmada]

## Pontos a confirmar

- [pergunta]
```

## `RESUMO-OBJETIVO-DO-CASO.md`

```markdown
# Resumo objetivo do caso

## Partes e papéis

| Pessoa ou entidade | Papel | Fonte | Status |
|---|---|---|---|

## Resultado pretendido informado

[texto curto ou A CONFIRMAR]

## Fatos principais

1. [fato] (PROVA-0001, p. 2) [COMPROVADO]
2. [afirmação] (relato de [pessoa]) [ALEGADO]

## Pontos controvertidos

- [ponto e fontes incompatíveis]

## Urgências

- [prazo, audiência, risco ou A CONFIRMAR]

## Limites deste resumo

Este arquivo facilita a consulta. Não substitui os originais nem a conferência das citações decisivas.
```

## `LINHA-DO-TEMPO.md`

```markdown
# Linha do tempo

| Data e hora | Evento | Pessoas envolvidas | Fonte e localizador | Situação |
|---|---|---|---|---|
| [data] | [evento objetivo] | [pessoas] | PROVA-0001, p. 3 | [COMPROVADO, ALEGADO, CONTRADITADO ou PENDENTE] |
```

Não ordene data incerta como se fosse exata. Use seção separada para `Eventos sem data confirmada`.

## `MAPA-DE-FATOS-E-PROVAS.md`

```markdown
# Mapa de fatos e provas

| Fato ou alegação | Quem afirma | Provas favoráveis | Provas contrárias | Limitações | Situação |
|---|---|---|---|---|---|
| [descrição] | [pessoa ou documento] | [PROVA e localizador] | [PROVA e localizador] | [limite] | [status] |
```

Situações permitidas:

- COMPROVADO
- PARCIALMENTE COMPROVADO
- ALEGADO SEM PROVA SUFICIENTE
- CONTRADITADO
- NÃO INFORMADO
- PENDENTE DE VALIDAÇÃO
- CONCLUSÃO JURÍDICA RESERVADA À ADVOGADA

## `INDICE-DO-PROCESSO.md`

```markdown
# Índice do processo judicial em Markdown

- PDF original: [PROVA-0000 e caminho]
- Total de páginas do PDF: [número]
- Total de páginas representadas em Markdown: [número]
- Páginas com OCR: [lista]
- Páginas pendentes: [lista]
- Status de completude: [status]

| Evento ou segmento | Tipo de ato | Data | Páginas do PDF | Arquivo Markdown | Observações |
|---|---|---|---|---|---|
| SEGMENTO-0001 | [tipo] | [data ou A CONFIRMAR] | 1 a 12 | [link] | [observação] |
```

## `PENDENCIAS-ATUAIS.md`

```markdown
# Perguntas e pendências atuais

## 1. Urgente

- [ ] [pergunta curta]. Motivo: [prazo, audiência, risco ou prova].

## 2. Informações indispensáveis

- [ ] [o que falta]. Já localizado: [fonte]. Precisamos confirmar: [ponto].

## 3. Documentos que faltam

- [ ] [documento]. Onde normalmente obter: [orientação simples, se segura].

## 4. Esclarecimentos úteis

- [ ] [pergunta].

## 5. Decisões da advogada responsável

- [ ] [decisão estratégica, sem decidir automaticamente].

## Respostas recebidas

| Data | Pergunta | Resposta | Quem respondeu | Prova enviada |
|---|---|---|---|---|
```

## Mapa entre prova e anexo processual

Crie um arquivo por peça, por exemplo `MAPA-DE-ANEXOS_PETICAO-INICIAL.md`:

```markdown
# Mapa de anexos da petição inicial

| Documento da peça | Prova permanente | Conteúdo | Conferido para protocolo |
|---|---|---|---|
| Doc. 01 | PROVA-0007 | [descrição] | [SIM ou NÃO] |
```

## Relatório final da organização

```markdown
# Relatório de conferência da organização

- Status: [APROVADO | INCOMPLETO_COM_PENDENCIAS | REPROVADO]
- Arquivos recebidos: [número]
- Provas registradas: [número]
- Duplicados exatos: [número]
- PDFs de processo: [número]
- Páginas de processo: [total e cobertura]
- Áudios e vídeos: [total e status]
- ZIPs: [total, itens e recusas]
- Falhas ou arquivos inacessíveis: [lista]
- Próxima etapa e modelo recomendado: [texto]
```
