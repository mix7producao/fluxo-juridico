# Fluxo Jurídico da SA Advocacia

Pacote de habilidades e instruções do escritório para uso no ChatGPT, Codex e Claude.

## O que o pacote faz

O plug-in `sa-fluxo-juridico` reúne três habilidades:

1. `organizar-caso-juridico`: recebe uma pasta com documentos mistos, preserva os originais, cria cópias identificadas, transcrições, índices, linha do tempo e checklist de pendências;
2. `redigir-peca-juridica`: analisa o caso organizado, relaciona fatos e provas, verifica fontes oficiais e produz a peça em Word conforme o padrão do escritório;
3. `criar-conteudo-juridico`: cria conteúdo institucional e educativo, observando o sigilo e os limites éticos da advocacia.

## Instalação para o time

Comece por [COMECE-AQUI.md](COMECE-AQUI.md). O administrador encontra o passo a passo em [INSTALACAO-DO-TIME.md](INSTALACAO-DO-TIME.md). O advogado usa somente [GUIA-DO-ADVOGADO.md](GUIA-DO-ADVOGADO.md).

O repositório contém os formatos de distribuição aceitos pelo ecossistema OpenAI e pelo Claude:

```text
.agents/plugins/marketplace.json
.claude-plugin/marketplace.json
plugins/sa-fluxo-juridico/
```

## Fluxo de um caso

1. Receber todos os documentos, inclusive ZIP integral do WhatsApp e PDF integral do processo.
2. Preservar os originais sem alteração.
3. Criar cópias de trabalho identificadas como `PROVA-0001` e números seguintes.
4. Transcrever PDFs, áudios e vídeos para Markdown, sem substituir o original.
5. Produzir índice, resumo, linha do tempo, mapa de provas e pendências.
6. Fazer perguntas somente depois de examinar o material disponível.
7. Produzir a peça em Word, relacionando cada afirmação à prova correspondente.
8. Renderizar e revisar todas as páginas antes da entrega.

## Modelos de inteligência artificial

Use um modelo equilibrado, como Terra ou equivalente, para organização mecânica, extração e classificação. Use Sol ou equivalente para análise jurídica e redação. Reserve Astra ou outro modelo de maior capacidade para casos excepcionalmente complexos e revisão final sensível. Os nomes e a disponibilidade devem ser conferidos na plataforma no momento do uso.

## Segurança

Este repositório deve conter somente regras, habilidades e modelos vazios. Casos reais e provas de clientes devem permanecer fora do GitHub.

## Manutenção

As regras principais estão em `AGENTS.md` e os detalhes em `instrucoes/`. Depois de uma alteração aprovada, publique uma nova versão no GitHub. O ChatGPT administrado pode sincronizar o repositório diariamente. No Claude Code, habilite a atualização automática do marketplace.
