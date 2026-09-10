# 10. Abertura e organização de novo caso

## Finalidade

Este protocolo vale antes da redação jurídica. Ele transforma os materiais recebidos em um acervo preservado, pesquisável e fácil de consultar por advogado ou inteligência artificial.

A organização não substitui a análise jurídica. Sua função é permitir que a análise posterior parta de fontes localizáveis, com distinção entre documento original, transcrição, resumo, alegação e conclusão.

## Primeira interação

Antes de processar os arquivos, responder de forma curta:

1. indicar o nível de modelo recomendado para a etapa;
2. pedir que a pessoa coloque na pasta tudo o que já possui;
3. lembrar do PDF integral do processo, se houver;
4. orientar a exportação integral do WhatsApp com mídias, em ZIP;
5. pedir áudios, vídeos, fotografias, e-mails com anexos, contratos, comprovantes, planilhas, decisões e intimações;
6. perguntar apenas se existe prazo, audiência ou urgência conhecida;
7. pedir que a pessoa informe quando o material estiver pronto.

Não aplicar um questionário genérico antes de examinar os documentos. Depois da organização, perguntar somente o que ainda não estiver respondido.

## Estrutura padrão

```text
NOME DO CASO/
|-- LEIA-PRIMEIRO.md
|-- 00 - ORIGINAIS RECEBIDOS - NAO ALTERAR/
|-- 01 - PROVAS ORGANIZADAS/
|-- 02 - TRANSCRICOES DE AUDIOS VIDEOS E CONVERSAS/
|-- 03 - PROCESSO JUDICIAL EM MARKDOWN/
|-- 04 - INDICE E CRONOLOGIA/
|-- 05 - PERGUNTAS E PENDENCIAS/
|-- 06 - ANALISE JURIDICA/
|-- 07 - PECAS EM ELABORACAO/
`-- 08 - PECAS FINALIZADAS E PROTOCOLOS/
```

Os nomes de pasta usam caracteres simples para melhorar a compatibilidade entre Windows, OneDrive, arquivos ZIP e ferramentas de inteligência artificial. O conteúdo dos arquivos Markdown deve manter acentuação completa e codificação UTF-8.

## Originais e derivados

- Tudo o que foi recebido permanece em `00 - ORIGINAIS RECEBIDOS - NAO ALTERAR`.
- Nenhum original é editado, convertido, renomeado ou substituído.
- Uma cópia idêntica recebe nome organizado em `01 - PROVAS ORGANIZADAS`.
- Transcrição, OCR, descrição e resumo são arquivos derivados e sempre apontam para o original.
- Não criar cópias redundantes sem finalidade definida.

## Identificador de prova

Cada prova recebe código permanente e não reutilizável:

```text
PROVA-0001_2026-08-15_AUDIO_FALA-SOBRE-PAGAMENTO.m4a
PROVA-0002_DATA-NAO-CONFIRMADA_CONTRATO_LOCACAO.pdf
```

O nome deve ser neutro e descrever o conteúdo. Não usar conclusão jurídica no nome.

O identificador `PROVA-0001` é interno e permanente. A numeração `Doc. 01` é criada separadamente para cada petição ou juntada. Um mapa deve registrar a correspondência entre os dois.

## Processo integral em Markdown

Quando houver processo em PDF:

1. preservar o PDF integral;
2. extrair todas as páginas;
3. aplicar OCR nas páginas digitalizadas;
4. criar um marcador para cada página, inclusive vazia ou ilegível;
5. dividir a transcrição em blocos de até 50 páginas;
6. criar índice por evento ou segmento processual;
7. conferir que o total de páginas do PDF coincide com a cobertura em Markdown;
8. marcar falhas sem completar conteúdo por suposição.

O Markdown serve para pesquisa e economia de contexto. Citação decisiva deve ser conferida no PDF original.

## Conversas, áudios e vídeos

- WhatsApp: preservar o ZIP e o TXT, manter a ordem integral e relacionar mídias somente quando houver base para isso.
- WhatsApp sem TXT útil: manter a pendência e pedir nova exportação, que receberá novo código de prova. Não limpar a pendência por suposição.
- Áudio: transcrever integralmente com locutores e tempo; usar `[INAUDÍVEL: 00:00:00]`.
- Vídeo: transcrever o áudio e produzir descrição visual objetiva com tempo.
- Captura de tela: transcrever o texto e registrar limites do recorte.
- Não identificar locutor, remetente, data ou contexto por adivinhação.

## Arquivos principais do caso

- `LEIA-PRIMEIRO.md`;
- `RESUMO-OBJETIVO-DO-CASO.md`;
- `INVENTARIO-DE-PROVAS.md`;
- `LINHA-DO-TEMPO.md`;
- `MAPA-DE-FATOS-E-PROVAS.md`;
- `INDICE-DO-PROCESSO.md`, quando houver processo;
- `PENDENCIAS-ATUAIS.md`;
- `RELATORIO-DE-CONFERENCIA.md`.

Cada fato resumido deve apontar para prova, página, mensagem ou marca de tempo.

## Situação dos fatos

Usar uma destas classificações:

- `COMPROVADO`;
- `PARCIALMENTE COMPROVADO`;
- `ALEGADO SEM PROVA SUFICIENTE`;
- `CONTRADITADO`;
- `NÃO INFORMADO`;
- `PENDENTE DE VALIDAÇÃO`;
- `CONCLUSÃO JURÍDICA RESERVADA À ADVOGADA`.

## Hash sem complicação para o advogado

Calcular SHA-256 automaticamente para verificar se as cópias permanecem idênticas. Guardar o resultado apenas no controle técnico.

O hash não é obrigação universal em todo processo civil ou de família e não prova sozinho autoria ou veracidade. Ele é uma medida de integridade e comparação. Para prova digital sensível, avaliar providências adicionais conforme o caso.

## Modelos e economia

- Ferramentas locais: cópia, hash, ZIP, paginação e validação.
- Luna ou equivalente rápido: tarefas simples e repetitivas.
- Terra ou equivalente equilibrado: organização, extração, classificação, Markdown, índice e perguntas.
- Sol ou equivalente de alto raciocínio: análise jurídica, contradições, pesquisa e redação.
- Astra ou equivalente de máxima capacidade: caso excepcionalmente complexo ou revisão final sensível.

Volume, por si só, não justifica modelo mais forte. Primeiro dividir, indexar e consultar apenas a fonte necessária.

## Sigilo

Cada caso é estanque. Não reutilizar dados em outro caso. Não enviar acervo sigiloso a serviço externo sem ambiente autorizado pelo escritório. Nomes e dados pessoais não devem aparecer em exemplos, testes ou prompts públicos.

## Conclusão

Somente declarar conclusão quando todos os arquivos estiverem inventariados, os originais preservados, as páginas do processo cobertas, as mídias transcritas ou marcadas como pendentes, os índices funcionais e as lacunas explicitadas.

O validador usa três estados. `APROVADO` permite concluir. `INCOMPLETO_COM_PENDENCIAS` significa que a triagem mecânica foi executada, mas ainda há trabalho aberto. `REPROVADO` indica falha de integridade ou estrutura que precisa ser corrigida.

Use a habilidade `habilidades/organizar-caso-juridico` para executar este protocolo no Codex. Para outra inteligência artificial, use `prompts/PROMPT-PORTATIL-ABERTURA-E-ORGANIZACAO-DE-CASO.md`.
