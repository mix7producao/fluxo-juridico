# Escolha de modelo e economia de tokens

## Regra principal

Use o menor nível de capacidade que entregue o resultado com segurança. Tarefas determinísticas devem ser executadas por scripts ou ferramentas locais. Não use um modelo mais caro apenas porque o acervo tem muitos arquivos.

Nomes, preços, limites e disponibilidade de modelos mudam. Antes de orientar o usuário, confira o seletor da plataforma e, se a informação for relevante, a documentação oficial atual. Não prometa economia percentual, custo fixo ou quantidade de tokens.

## Matriz prática

| Etapa | Nível suficiente | Codex, referência atual | Claude ou outra plataforma | Esforço sugerido |
|---|---|---|---|---|
| Copiar, calcular hash, descompactar, validar caminhos e contar páginas | Ferramenta local | Scripts, sem modelo | Ferramentas locais | Não se aplica |
| Lembrete inicial e classificação simples | Rápido e econômico | Luna | Modelo rápido equivalente | Baixo |
| Inventário, nomes, extração, organização e Markdown | Operacional equilibrado | Terra | Sonnet disponível ou equivalente equilibrado | Baixo ou médio |
| Índice, cronologia e perguntas complementares | Operacional equilibrado | Terra | Sonnet disponível ou equivalente equilibrado | Médio |
| Matriz de fatos e provas, contradições e riscos | Raciocínio jurídico | Sol | Modelo de alta capacidade | Médio ou alto |
| Pesquisa jurídica, estratégia e primeira versão de peça | Raciocínio jurídico | Sol | Modelo de alta capacidade | Alto |
| Caso excepcionalmente complexo ou revisão crítica sensível | Revisão crítica | Astra | Modelo de máxima capacidade disponível | Alto ou extra-alto |

Na data de atualização deste arquivo, a documentação oficial da OpenAI descreve Luna para tarefas claras e repetitivas, Terra para trabalho cotidiano, Sol para tarefas complexas e abertas, e Astra para fluxos difíceis que exigem raciocínio sustentado. Fonte: https://developers.openai.com/codex/models

Para Claude, confira o modelo equilibrado e o modelo de máxima capacidade atualmente disponíveis. Não congele uma versão específica na habilidade. Fonte: https://docs.anthropic.com/en/docs/about-claude/models/choosing-a-model

## Gatilhos de escalonamento

Passe de Terra para Sol quando houver pelo menos uma destas situações:

- versões incompatíveis sobre fato juridicamente relevante;
- necessidade de distinguir fato comprovado de inferência delicada;
- dúvida sobre ônus da prova, competência, prescrição, decadência ou tutela urgente;
- documentos que sustentam teses jurídicas diferentes;
- necessidade de pesquisa legal ou jurisprudencial;
- elaboração de peça jurídica.

Passe de Sol para Astra quando houver:

- processo muito complexo com várias partes, incidentes ou recursos;
- risco grave ou irreversível;
- prova digital central com autenticidade ou integridade contestada;
- jurisprudência divergente ou questão jurídica incomum;
- conflito persistente após revisão com Sol;
- auditoria final de peça sensível ou de alto impacto.

OCR ruim, áudio inaudível e arquivo corrompido não se resolvem necessariamente com um modelo maior. Nesses casos, tente ferramenta especializada, outra cópia da fonte ou revisão humana.

## Economia de contexto

1. Processe o acervo uma vez e grave os resultados em Markdown.
2. Comece cada etapa futura por `LEIA-PRIMEIRO.md` e pelo índice geral.
3. Abra somente as provas citadas na tarefa atual.
4. Divida processos extensos por faixas de páginas, mantendo um índice único.
5. Não envie novamente o processo integral quando uma página ou uma prova específica bastar.
6. Use scripts para cópia, hash, ZIP, paginação e validação.
7. Use o modelo jurídico somente depois que a parte mecânica estiver pronta.
8. A revisão por modelo mais capaz não substitui a conferência do original nem a validação oficial da legislação e da jurisprudência.

## Texto curto para a primeira orientação

> Para organizar os arquivos, use Terra ou um modelo equilibrado equivalente. Sol será usado quando começar a análise jurídica. Astra fica reservado para casos complexos ou para uma revisão final sensível. Cópia, hash, ZIP e contagem de páginas serão feitos por ferramentas locais, sem gastar raciocínio de modelo.
