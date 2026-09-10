# Instalação do pacote para o time

## Melhor configuração para o ChatGPT e o Codex

Use um workspace ChatGPT Business, Enterprise ou equivalente administrado pelo escritório. O administrador faz a configuração uma vez:

1. Publique este repositório como privado no GitHub.
2. No ChatGPT, abra `Administração`, depois `Plug-ins`.
3. Escolha `Adicionar` e `Importar marketplace`.
4. Cole a URL do repositório privado.
5. Deixe a referência de versão vazia para acompanhar a branch principal.
6. Importe o marketplace.
7. Abra o plug-in `Fluxo Jurídico SA Advocacia`.
8. Defina a política como instalado para os advogados autorizados.

Depois disso, cada advogado abre uma conversa nova e escreve apenas:

```text
Quero abrir e organizar um novo caso jurídico.
```

Ou:

```text
Analise este caso e produza a peça jurídica adequada.
```

O marketplace importado do GitHub é sincronizado automaticamente pelo workspace. O administrador também pode usar `Sincronizar agora` quando houver atualização urgente.

## Melhor configuração para Claude Code

Cada advogado executa uma única vez, substituindo `USUARIO/REPOSITORIO` pelo endereço informado pelo escritório:

```text
/plugin marketplace add USUARIO/REPOSITORIO
/plugin install sa-fluxo-juridico@sa-advocacia
```

Depois, abra `/plugin`, entre em `Marketplaces`, selecione `sa-advocacia` e ative a atualização automática. As habilidades aparecerão com estes nomes:

```text
/sa-fluxo-juridico:organizar-caso-juridico
/sa-fluxo-juridico:redigir-peca-juridica
/sa-fluxo-juridico:criar-conteudo-juridico
```

## ChatGPT ou Claude em conta individual

Uma conta individual fora do workspace não recebe automaticamente um pacote privado administrado pelo escritório. Nesse caso, use um Projeto da plataforma e adicione `PACOTE-UNICO-PARA-CHATGPT-E-CLAUDE.md` como conhecimento permanente. Para instalação realmente centralizada no ChatGPT, o caminho recomendado é o workspace administrado ou a publicação do plug-in no diretório público.

## Segurança

O GitHub contém somente instruções, habilidades e modelos vazios. Processos, provas, conversas e dados de clientes ficam na pasta de cada caso e nunca são publicados no repositório.
