# Usar no Claude

## Claude Code, opção recomendada

Cada advogado executa somente estes dois comandos, uma única vez:

```text
/plugin marketplace add ORGANIZACAO/REPOSITORIO
/plugin install sa-fluxo-juridico@sa-advocacia
```

O administrador substituirá `ORGANIZACAO/REPOSITORIO` pelo endereço curto do GitHub, por exemplo `nome-do-escritorio/fluxo-juridico`.

Depois da instalação, abra `/plugin`, entre em `Marketplaces`, selecione `sa-advocacia` e ative `Enable auto-update`. Assim, as novas versões publicadas no GitHub serão recebidas automaticamente.

Para usar, abra a pasta do caso e escreva:

```text
Quero abrir e organizar um novo caso jurídico.
```

## Claude pelo navegador

Se a conta usar Projects:

1. crie um Projeto chamado `SA Advocacia`;
2. conecte o repositório pelo GitHub ou adicione `PACOTE-UNICO-PARA-CHATGPT-E-CLAUDE.md` ao conhecimento do Projeto;
3. selecione os arquivos de instrução do repositório;
4. abra uma conversa nova para cada caso.

Use esta instrução no Projeto:

```text
Leia integralmente o arquivo PACOTE-UNICO-PARA-CHATGPT-E-CLAUDE.md antes de atuar. Siga essas regras em todas as conversas deste projeto. Em um caso novo, faça primeiro somente os lembretes de recebimento e aguarde a expressão PODE ORGANIZAR antes de processar os documentos. Nunca invente informações e nunca afirme que alterou ou organizou arquivos sem ter acesso real a eles.
```

A conexão do Projeto fornece contexto atualizado, mas não equivale à instalação central do plug-in em todas as contas.
