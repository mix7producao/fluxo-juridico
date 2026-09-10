# Estrutura de pastas, identificadores e nomes

## Estrutura padrão de cada caso

```text
NOME DO CASO/
|-- LEIA-PRIMEIRO.md
|-- 00 - ORIGINAIS RECEBIDOS - NAO ALTERAR/
|-- 01 - PROVAS ORGANIZADAS/
|   |-- DOCUMENTOS/
|   |-- CONVERSAS E EMAILS/
|   |-- AUDIOS/
|   |-- VIDEOS/
|   |-- FOTOS E CAPTURAS DE TELA/
|   `-- OUTROS/
|-- 02 - TRANSCRICOES DE AUDIOS VIDEOS E CONVERSAS/
|-- 03 - PROCESSO JUDICIAL EM MARKDOWN/
|-- 04 - INDICE E CRONOLOGIA/
|-- 05 - PERGUNTAS E PENDENCIAS/
|-- 06 - ANALISE JURIDICA/
|-- 07 - PECAS EM ELABORACAO/
`-- 08 - PECAS FINALIZADAS E PROTOCOLOS/
```

Os nomes das pastas usam caracteres simples para reduzir falhas em ZIPs, integrações e caminhos do Windows. Dentro de todo arquivo Markdown, use português do Brasil com acentuação completa.

## Função de cada pasta

| Local | Conteúdo |
|---|---|
| `LEIA-PRIMEIRO.md` | Entrada única para advogado e inteligência artificial, com resumo, situação da triagem e links. |
| `00 - ORIGINAIS RECEBIDOS - NAO ALTERAR` | Tudo o que foi recebido, exatamente como chegou. Nenhum arquivo desta pasta pode ser editado ou renomeado. |
| `01 - PROVAS ORGANIZADAS` | Cópias idênticas dos originais, classificadas e nomeadas com `PROVA-0000`. |
| `02 - TRANSCRICOES DE AUDIOS VIDEOS E CONVERSAS` | Arquivos Markdown derivados de mídias e conversas. |
| `03 - PROCESSO JUDICIAL EM MARKDOWN` | Transcrição integral e índice do PDF dos autos. |
| `04 - INDICE E CRONOLOGIA` | Inventário, resumo, linha do tempo, mapa de fatos e provas e controle técnico. |
| `05 - PERGUNTAS E PENDENCIAS` | Perguntas formuladas após a leitura, documentos faltantes e respostas recebidas. |
| `06 - ANALISE JURIDICA` | Teses, riscos e estratégia, separados das transcrições factuais. |
| `07 - PECAS EM ELABORACAO` | Rascunhos editáveis ainda não aprovados. |
| `08 - PECAS FINALIZADAS E PROTOCOLOS` | Versões aprovadas, recibos, decisões e intimações posteriores. |

O arquivo recebido pode ser colocado diretamente na pasta `00`. Quando o material estiver em outro local, copie-o para `00` e deixe a fonte externa intacta. Não crie uma terceira cópia de preservação sem necessidade.

## Identificador permanente

Use uma sequência única por caso:

```text
PROVA-0001
PROVA-0002
PROVA-0003
```

Regras:

- o número nunca é reutilizado, mesmo se a prova for posteriormente desconsiderada;
- uma nova execução sem arquivo novo não cria identificadores novos;
- o mesmo arquivo no mesmo caminho, com o mesmo conteúdo, mantém o identificador;
- dois arquivos recebidos separadamente podem receber identificadores diferentes, ainda que sejam duplicados exatos, com essa duplicidade registrada;
- arquivo extraído de ZIP deve indicar de qual prova original deriva;
- arquivo Markdown derivado mantém o identificador da prova e acrescenta a finalidade, por exemplo `PROVA-0007_TRANSCRICAO-INTEGRAL.md`;
- não coloque CPF, endereço residencial, diagnóstico ou outro dado sensível no nome do arquivo.

## Nome das cópias organizadas

Padrão:

```text
PROVA-0001_AAAA-MM-DD_TIPO_ASSUNTO.ext
```

Exemplos:

```text
PROVA-0001_2026-08-15_AUDIO_ACORDO-PAGAMENTO.m4a
PROVA-0002_2026-08-16_WHATSAPP_COBRANCA-INTEGRAL.txt
PROVA-0003_DATA-NAO-CONFIRMADA_CONTRATO_LOCACAO.pdf
PROVA-0004_DATA-NAO-CONFIRMADA_IMAGEM_CONTEUDO-A-IDENTIFICAR.png
```

Inclua a data apenas quando estiver confirmada no conteúdo ou em metadado confiável. Data de criação do arquivo no computador não prova a data do fato. Quando houver dúvida, use `DATA-NAO-CONFIRMADA` e abra pendência.

O assunto deve ser curto, objetivo e baseado na inspeção. Não nomeie um áudio como `CONFISSAO` apenas por interpretação. Prefira descrição neutra, como `FALA-SOBRE-PAGAMENTO`.

## Relação com a numeração processual

`PROVA-0007` é a identidade permanente dentro do caso. `Doc. 03` é a posição daquela prova em uma juntada determinada. Mantenha-os separados.

Exemplo:

```text
PROVA-0007 | Doc. 03 da petição inicial | protocolado em [A CONFIRMAR]
PROVA-0007 | Doc. 08 da réplica | protocolado em [A CONFIRMAR]
```

Essa separação evita renomear a prova quando a ordem dos anexos mudar.

## Duplicidades e versões

- Não apague duplicados automaticamente.
- Marque `DUPLICADO EXATO` somente quando os hashes coincidirem.
- Marque `VERSÃO APARENTE` quando os nomes forem parecidos, mas o conteúdo não for idêntico.
- Não escolha a versão correta por suposição.
- Para documento atualizado, preserve as duas versões e registre data, origem e diferença verificada.

## Controle técnico de integridade

Calcule SHA-256 automaticamente para o arquivo recebido e para a cópia organizada. Guarde o resultado em `04 - INDICE E CRONOLOGIA/CONTROLE-TECNICO-DE-INTEGRIDADE.jsonl`.

O advogado não precisa preencher nem ler esse controle no uso cotidiano. No inventário visível, basta registrar `cópia idêntica verificada` ou a falha correspondente.

O hash serve para comparar arquivos e detectar alteração. Ele não demonstra sozinho quem produziu o conteúdo, se a conversa é verdadeira ou se a gravação é lícita. Para prova digital sensível, avalie ata notarial, perícia ou outro método de autenticação adequado.
