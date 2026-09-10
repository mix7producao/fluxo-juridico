# Instruções de IA da SA Advocacia

Esta pasta concentra o padrão de trabalho da Dra. Lidiane Sousa Araújo para produção de peças jurídicas e de conteúdo, em formato legível por agentes de inteligência artificial.

## Instalação simples

Comece pelo arquivo [`COMECE-AQUI.md`](COMECE-AQUI.md). No Windows, `INSTALAR-HABILIDADE.cmd` instala a habilidade no Codex e no Claude Code. Para ChatGPT ou Claude pelo navegador, envie apenas `PACOTE-UNICO-PARA-CHATGPT-E-CLAUDE.md` ao projeto da plataforma.

## Como usar

**No Codex (OpenAI).** O Codex lê automaticamente o arquivo `AGENTS.md` da pasta em que está trabalhando. Basta apontar o Codex para esta pasta, ou copiar esta pasta para dentro do projeto em que ele vai atuar. Para abrir e organizar um caso novo, use `$organizar-caso-juridico`. A versão principal da habilidade está em `habilidades/organizar-caso-juridico`.

**No Claude Code ou Claude Cowork.** Um arquivo `CLAUDE.md` com o mesmo conteúdo do `AGENTS.md` funciona da mesma forma. Também é possível conectar esta pasta como contexto da sessão.

**No ChatGPT, Gemini ou similar sem acesso a pasta.** Cole o conteúdo de `AGENTS.md` no campo de instruções personalizadas ou no início da conversa, e anexe os arquivos da pasta `instrucoes/` conforme a tarefa. Para caso novo, use também `prompts/PROMPT-PORTATIL-ABERTURA-E-ORGANIZACAO-DE-CASO.md`. A plataforma só pode afirmar que organizou arquivos quando possuir acesso real a eles.

## Fluxo rápido para um caso novo

1. Duplique `modelos/MODELO-DE-PASTA-PARA-NOVO-CASO` e dê à cópia o nome interno do caso, ou peça à habilidade que crie a estrutura.
2. Inicie `$organizar-caso-juridico`.
3. Coloque tudo o que foi recebido em `00 - ORIGINAIS RECEBIDOS - NAO ALTERAR`.
4. Para WhatsApp, exporte a conversa com mídias e envie o ZIP intacto.
5. Inclua o PDF integral do processo, quando houver.
6. Informe prazo, audiência ou urgência.
7. Diga `PODE ORGANIZAR`.

A organização usa Terra ou modelo equilibrado equivalente. Sol fica para análise jurídica e redação. Astra fica reservado para complexidade excepcional ou revisão final sensível. Os nomes e a disponibilidade dos modelos devem ser conferidos na plataforma no momento do uso.

## Estrutura

```
000 - Instruções IA/
├── AGENTS.md                 arquivo de entrada, regras principais
├── README.md                 este arquivo
└── instrucoes/
    ├── 01-perfil-escritorio.md
    ├── 02-formatacao-documentos.md
    ├── 03-regras-peca-otimizada-ia.md
    ├── 04-validacao-provas-e-jurisprudencia.md
    ├── 05-portugues-utf8.md
    ├── 06-fluxo-de-trabalho.md
    ├── 07-modelos-estruturas.md
    ├── 08-checklist-final.md
    ├── 09-escopo-conteudo-redes.md
    └── 10-abertura-e-organizacao-de-caso.md
├── habilidades/
│   └── organizar-caso-juridico/
│       ├── SKILL.md
│       ├── agents/
│       ├── references/
│       └── scripts/
├── modelos/
│   └── MODELO-DE-PASTA-PARA-NOVO-CASO/
└── prompts/
    └── PROMPT-PORTATIL-ABERTURA-E-ORGANIZACAO-DE-CASO.md
```

## Manutenção

Sempre que um padrão novo for adotado, atualize o arquivo correspondente em `instrucoes/` e, se for regra estruturante, registre também no `AGENTS.md`. Arquivos de modelo em .docx (timbrado, procuração, contrato de honorários) podem ser guardados em uma subpasta `modelos/` desta mesma pasta, e o agente será orientado a usá-los.
