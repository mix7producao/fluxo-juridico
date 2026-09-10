---
name: organizar-caso-juridico
description: Organiza a abertura e a triagem de novos casos jurídicos civis, de família e inventário a partir de uma pasta com arquivos mistos. Use quando for necessário receber, preservar, copiar, identificar, transcrever, catalogar e relacionar processos em PDF, exportações do WhatsApp, áudios, vídeos, imagens, documentos e demais provas antes da análise ou da redação jurídica. Não use para uma simples revisão de peça quando o acervo do caso já estiver organizado.
---

# Organizar caso jurídico

## Resultado obrigatório

Transformar uma pasta de materiais recebidos em um acervo jurídico pesquisável, sem alterar os originais, com:

1. cópia organizada das provas com identificadores permanentes;
2. transcrição integral das fontes que não sejam facilmente pesquisáveis;
3. processo judicial completo em Markdown, quando houver PDF dos autos;
4. índice geral, inventário, cronologia e mapa entre fatos e provas;
5. separação explícita entre fato comprovado, alegação, contradição e pendência;
6. perguntas complementares formuladas somente após a leitura do acervo;
7. indicação do nível de modelo adequado a cada etapa.

Leia primeiro o `AGENTS.md` aplicável ao diretório do caso. As regras locais de sigilo, idioma, prova, estratégia e formatação prevalecem.

## Primeira resposta em um caso novo

Antes de organizar arquivos, indique o modelo recomendado para a etapa e apresente apenas um lembrete curto:

1. coloque na pasta tudo o que já possui, mesmo que pareça repetido ou desorganizado;
2. inclua o PDF integral do processo, se já existir;
3. exporte as conversas do WhatsApp com mídia e envie o arquivo ZIP sem modificá-lo;
4. inclua áudios, vídeos, fotografias, contratos, comprovantes, planilhas, e-mails e documentos pessoais ou processuais pertinentes;
5. não recorte, edite, renomeie nem converta os arquivos antes do recebimento;
6. informe prazo, audiência ou urgência conhecida;
7. avise que poderá acrescentar outros arquivos depois.

Se o usuário ainda não tiver declarado que o material está pronto para organização, encerre essa primeira resposta pedindo que diga `PODE ORGANIZAR` quando terminar. Se já tiver dado essa autorização expressamente, prossiga sem repetir a pergunta.

Leia [modelos e economia](references/modelos-e-economia.md) antes de recomendar modelo ou esforço de raciocínio.

Antes de executar scripts, leia [execução local e dependências](references/execucao-local-e-dependencias.md). No Codex Desktop, carregue o runtime do espaço de trabalho e use o Python retornado com `-B -X utf8`; não presuma que o Python padrão possui `pypdf` ou as dependências de teste.

## Regras invioláveis

- Nunca invente conteúdo, data, remetente, locutor, página, descrição, vínculo ou conclusão.
- Nunca altere o arquivo original. Conversões, OCR, renomeações e transcrições ocorrem apenas em cópias ou arquivos derivados.
- Não exclua, substitua nem mova arquivo recebido sem autorização específica.
- Não misture dados entre casos. Cada pasta é estanque.
- Preserve a conversa e o processo em sua ordem integral, mesmo quando apenas parte parecer relevante.
- Resumo não substitui transcrição. A transcrição não substitui o original.
- Antes de citar trecho decisivo em peça, confira-o novamente no original e indique página ou tempo exato.
- Trate OCR, identificação automática de voz e descrição de imagem como resultados sujeitos a conferência.
- Marque dúvida factual como `[A CONFIRMAR: descrição]`.
- Não declare que a triagem terminou enquanto houver arquivo sem registro, página não processada ou falha de leitura não sinalizada.

## Fluxo

### 1. Delimitar e preservar

Resolva o caminho exato da pasta do caso e faça um inventário antes de qualquer alteração. Identifique arquivos soltos, subpastas, ZIPs, duplicidades aparentes, PDFs, mídias e formatos não reconhecidos.

Crie a estrutura com `scripts/iniciar_estrutura_caso.py`. Coloque ou copie o material recebido em `00 - ORIGINAIS RECEBIDOS - NAO ALTERAR`, preservando nomes, subpastas, bytes e datas sempre que possível. Não use a pasta de saída como entrada de sua própria varredura.

Leia [estrutura, nomes e identificadores](references/estrutura-pastas-e-nomes.md) antes de criar ou renomear cópias.

### 2. Registrar integridade e atribuir identificadores

Execute `scripts/inventariar_originais.py` para registrar caminho, tamanho, data técnica e SHA-256. O hash é um controle automático, não um campo a ser preenchido pelo advogado e não prova autenticidade sozinho.

Atribua a cada prova um identificador permanente e não reutilizável no formato `PROVA-0001`. Depois de inspecionar o conteúdo, use `scripts/copiar_prova_organizada.py` para duplicar o original na categoria adequada de `01 - PROVAS ORGANIZADAS`, com nome neutro e cópia conferida.

Não use `Doc. 01` como identificador permanente. `Doc. 01`, `Doc. 02` e equivalentes pertencem a uma juntada específica. Registre a correspondência entre `PROVA-0001` e o número do documento apenas quando a peça ou o protocolo for montado.

### 3. Converter e transcrever

Leia [processamento por tipo de arquivo](references/processamento-e-integridade.md) somente nas seções correspondentes aos formatos encontrados.

- PDF de processo: transcreva todas as páginas para Markdown, com marcadores de página e índice. Use `scripts/extrair_pdf_para_md.py` como primeira extração, informe o `--id-prova` correspondente e mantenha a saída dentro de `03 - PROCESSO JUDICIAL EM MARKDOWN`. Aplique OCR e revisão visual nas páginas indicadas como vazias, escaneadas ou ilegíveis. Registre a conclusão com `scripts/registrar_revisao_pdf.py`.
- WhatsApp: preserve o ZIP e use a cópia organizada como entrada de `scripts/extrair_zip_whatsapp.py`, com `--id-prova`. Mantenha a saída dentro de `02 - TRANSCRICOES DE AUDIOS VIDEOS E CONVERSAS`. O script cria uma cópia literal verificada do TXT em Markdown ou uma pendência persistente. Quando houver mais de um TXT, registre a escolha humana com `scripts/registrar_revisao_whatsapp.py`. Se não houver TXT útil, solicite nova exportação e registre o novo ZIP como nova prova. Depois, organize cronologicamente sem alterar a transcrição literal, mantendo participantes, datas, horários e vínculos comprovados com as mídias.
- Áudio e vídeo: produza transcrição integral com locutores e marcações de tempo. Use `[INAUDÍVEL: 00:00:00]` quando necessário.
- Imagem e captura de tela: faça OCR quando houver texto e descreva somente elementos observáveis. Não deduza intenção, identidade ou contexto ausente.
- DOCX, e-mail, planilha e demais documentos: extraia o conteúdo integral relevante para arquivo Markdown, preservando tabelas, cabeçalhos, links e referência ao original.

### 4. Produzir os arquivos de navegação

Use os esquemas em [modelos de arquivos Markdown](references/modelos-de-arquivos-md.md). Produza, no mínimo:

- `LEIA-PRIMEIRO.md`;
- `04 - INDICE E CRONOLOGIA/INVENTARIO-DE-PROVAS.md`;
- `04 - INDICE E CRONOLOGIA/LINHA-DO-TEMPO.md`;
- `04 - INDICE E CRONOLOGIA/MAPA-DE-FATOS-E-PROVAS.md`;
- `04 - INDICE E CRONOLOGIA/RESUMO-OBJETIVO-DO-CASO.md`;
- `05 - PERGUNTAS E PENDENCIAS/PENDENCIAS-ATUAIS.md`.

O índice deve permitir que outra inteligência artificial localize a fonte sem reabrir todo o acervo. Cada afirmação resumida deve apontar para `PROVA-0000`, página, item, mensagem ou marca de tempo.

### 5. Formular perguntas depois da leitura

Somente depois de processar o que foi entregue, leia [checklists por área](references/checklists-por-area.md) na seção aplicável. Não envie questionário genérico já respondido pelos documentos.

Organize as perguntas em:

1. urgentes, ligadas a prazo, audiência, risco ou preservação de prova;
2. indispensáveis para compreender fatos, partes, pedidos ou competência;
3. documentos que faltam;
4. esclarecimentos úteis, mas não impeditivos;
5. decisões estratégicas reservadas ao advogado responsável.

Faça perguntas curtas, em linguagem acessível, explique onde obter o documento quando isso ajudar e aceite a resposta `não sei` sem preencher por dedução.

### 6. Analisar somente com base no acervo

Depois da triagem, produza a matriz jurídica e a estratégia apenas quando solicitadas. Diferencie:

- `COMPROVADO`: há fonte identificada e conferida;
- `ALEGADO`: alguém afirmou, mas não há suporte independente suficiente;
- `CONTRADITADO`: existem fontes incompatíveis;
- `NÃO INFORMADO`: não consta do material;
- `PENDENTE DE VALIDAÇÃO`: extração, OCR, autenticidade ou contexto exige revisão.

Pesquisa de legislação e jurisprudência deve seguir as fontes oficiais exigidas pelo `AGENTS.md` aplicável.

## Critérios de conclusão

Execute `scripts/validar_caso.py` antes de informar que a organização terminou. A validação automática não substitui a revisão jurídica ou visual.

Interprete o resultado assim: `APROVADO` permite concluir a organização; `INCOMPLETO_COM_PENDENCIAS` exige continuidade e já registra as pendências no caso; `REPROVADO` exige correção de integridade. O validador retorna, respectivamente, os códigos `0`, `1` e `2`.

Só informe que a organização terminou quando:

1. todos os arquivos recebidos constarem do inventário;
2. todos os identificadores forem únicos e estáveis;
3. as cópias organizadas puderem ser relacionadas aos originais;
4. todas as páginas do processo estiverem presentes no Markdown ou marcadas para revisão;
5. todas as mídias tiverem transcrição ou pendência explícita;
6. os links internos dos índices funcionarem;
7. fatos, alegações, contradições e lacunas estiverem separados;
8. as perguntas complementares tiverem sido geradas a partir do acervo real;
9. o relatório de validação não contiver erro silencioso.

Na entrega, informe apenas: o que foi organizado, o que permanece pendente, riscos imediatos e qual modelo usar na próxima etapa.
