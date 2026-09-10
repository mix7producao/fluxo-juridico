# Processamento e integridade por tipo de material

Leia somente as seções relativas aos formatos encontrados no caso.

## Regras comuns

1. Preserve o arquivo recebido na pasta de originais.
2. Produza cópia organizada e derivados fora da pasta de originais.
3. Registre origem, pessoa que forneceu, data de recebimento e limitações.
4. Não execute programas, macros ou atalhos encontrados no acervo.
5. Não abra link externo automaticamente quando ele puder expor dados ou modificar estado.
6. Trate metadado como indício técnico, não como prova automática da data do fato.
7. Se usar serviço externo de inteligência artificial, confirme que o ambiente foi autorizado pelo escritório para dados sigilosos. Na dúvida, use processamento local.

## Processo judicial em PDF

O PDF completo é preservado como prova. O Markdown é uma cópia de consulta e não substitui o documento oficial, suas assinaturas ou seus certificados.

### Extração

No Codex Desktop, carregue primeiro o runtime do espaço de trabalho e use o Python retornado com `-X utf8`. Informe ao extrator o código permanente do PDF e grave a saída em uma subpasta de `03 - PROCESSO JUDICIAL EM MARKDOWN`.

1. Conte as páginas do PDF.
2. Extraia o texto nativo de todas as páginas.
3. Gere um marcador para cada página, inclusive página vazia.
4. Aplique OCR somente às páginas sem texto útil, com texto corrompido ou digitalizadas.
5. Não corrija silenciosamente o texto produzido por OCR.
6. Registre o método de extração de cada página.
7. Divida o processo em blocos de até 50 páginas para facilitar consulta e reduzir contexto.
8. Crie `INDICE-DO-PROCESSO.md` com as faixas, os atos identificados e os links.
9. Use o número real do evento processual quando constar do PDF. Se não constar, use `SEGMENTO-0001`.
10. Registre a numeração do visualizador e, quando relevante, a numeração impressa na folha.

Marcador mínimo:

```markdown
<a id="pdf-pagina-0001"></a>

## Página 0001

Método de extração: texto nativo

[texto integral]
```

Para página sem resultado:

```text
[PÁGINA SEM TEXTO DETECTÁVEL. O original foi preservado. Revisão visual ou novo OCR necessário.]
```

### Validação de completude

Compare:

- número de páginas informado pelo PDF;
- número de marcadores de página nos arquivos Markdown;
- primeira e última páginas de cada bloco;
- lista de páginas que receberam OCR;
- lista de páginas vazias, ilegíveis ou não processadas;
- existência de sobreposição ou lacuna entre blocos.

Não declare extração completa se uma página estiver ausente. Documento protegido por senha gera pendência e não autoriza contornar a proteção.

Uma extração bem-sucedida ainda fica com revisão visual pendente. Depois de conferir todas as páginas e resolver individualmente as páginas sem texto útil, use `scripts/registrar_revisao_pdf.py`. O validador mantém o caso como incompleto até esse registro.

## Conversa de WhatsApp

### Orientação simples para quem envia

1. Abra a conversa no WhatsApp.
2. Use a opção de exportar conversa.
3. Escolha incluir mídias.
4. Envie o arquivo ZIP gerado, sem abri-lo, editar nomes ou reorganizar o conteúdo.
5. Não apague a conversa nem as mídias do aparelho.
6. Se o WhatsApp limitar a quantidade de mídia exportada, envie também os arquivos originais que faltaram.

O caminho exato do menu varia entre Android, iPhone e versões do aplicativo. Se necessário, explique o procedimento conforme o aparelho informado, sem afirmar que a exportação contém mídias que o próprio aplicativo omitiu.

### Tratamento do ZIP

- Preserve o ZIP original.
- Extraia somente para pasta derivada e autorizada.
- Rejeite caminho absoluto, segmento `..`, link simbólico, item criptografado e destino que saia da pasta.
- Não extraia automaticamente outro arquivo compactado encontrado dentro do ZIP.
- Verifique CRC, quantidade de itens, tamanho total e colisões de nome.
- Registre todo item recusado e o motivo.
- Não use `extractall` sem validar individualmente cada entrada.
- Use a cópia organizada do ZIP, informe seu `PROVA-0000` ao script e grave a saída dentro de `02 - TRANSCRICOES DE AUDIOS VIDEOS E CONVERSAS`.
- Exija no resultado uma conversa integral em Markdown ou um arquivo de pendência de conversão. Apenas extrair o ZIP não conclui a etapa.

### Como resolver pendência de conversão

- Mais de um TXT convertido: confirme com a pessoa responsável qual é o TXT principal e use `scripts/registrar_revisao_whatsapp.py`. O registro mantém os demais arquivos e o histórico da dúvida.
- ZIP sem TXT, TXT vazio ou codificação não reconhecida: não limpe a pendência manualmente. Solicite nova exportação integral, registre o novo ZIP como nova prova e execute novamente em outra pasta.
- Markdown alterado depois da conversão: gere novamente a partir do ZIP preservado. Não ajuste o hash nem o manifesto manualmente.

### Conversa integral

- Preserve o TXT original da exportação.
- Mantenha mensagens de sistema, chamadas, mensagens apagadas registradas e linhas multilinha.
- Preserve remetente, data e horário exatamente como aparecem.
- Relacione mídia a mensagem somente quando o nome ou o contexto demonstrar essa relação.
- Liste mídia mencionada e ausente.
- Marque formato de data ambíguo como `[A CONFIRMAR]`.
- Gere uma transcrição integral em Markdown e, separadamente, uma seleção dos trechos juridicamente relevantes.

A exportação comum do WhatsApp não equivale a extração forense e pode ser incompleta. Para conteúdo decisivo, avalie preservação adicional, ata notarial ou perícia conforme o risco.

## Áudio

Produza um arquivo como `PROVA-0007_TRANSCRICAO-INTEGRAL.md`:

```markdown
# PROVA-0007: transcrição integral

- Arquivo original: [caminho]
- Duração: 00:12:43
- Método: transcrição automática
- Idioma: português do Brasil
- Status: AUTOMÁTICA NÃO REVISADA

[00:00:03] LOCUTOR 1: [fala]
[00:00:09] LOCUTOR 2: [fala]
[INAUDÍVEL: 00:03:17]
```

Não atribua nome a locutor sem confirmação. Mantenha negativas, hesitações e interrupções relevantes. Registre sobreposição de vozes. Divida gravações longas em blocos com cobertura contínua e sem intervalo omitido.

Pergunte, quando pertinente, quem gravou, quem participou, em qual aparelho o original está guardado e se houve edição. A licitude não pode ser deduzida apenas pelo arquivo.

## Vídeo

Produza:

1. transcrição integral do áudio;
2. descrição visual objetiva com marcações de tempo;
3. lista de trechos que exigem conferência humana.

Não afirme emoção, intenção, identidade ou local sem suporte. A análise por quadros reduz trabalho, mas não garante que todo detalhe visual foi capturado.

## Imagem e captura de tela

- Preserve dimensões, formato e arquivo original.
- Faça OCR do texto visível, sem completar palavras cortadas.
- Descreva elementos observáveis, posição e legibilidade.
- Registre se a imagem é parcial, recortada ou não mostra contexto anterior e posterior.
- Para conversa, procure a exportação integral ou sequência completa de capturas.
- Não trate data exibida na interface como automaticamente vinculada ao arquivo fora do contexto mostrado.

## PDF, DOCX, ODT e texto comum

- Extraia cabeçalhos, corpo, tabelas, notas, links e assinaturas indicadas.
- Preserve a ordem de leitura.
- Marque página ausente, ilegível ou aparentemente incompleta.
- Em contrato, confira todas as páginas, anexos, assinaturas e rubricas.
- Em certidão, registre data de emissão e validade aparente sem afirmar validade jurídica definitiva.
- Em PDF que não seja processo, mantenha página como localizador.

## E-mail

Prefira o arquivo original da mensagem, como EML ou MSG, acompanhado dos anexos. Preserve remetente, destinatários, cópia, assunto, data, fuso, identificadores técnicos e cadeia de respostas. PDF ou captura de tela é cópia de visualização e pode omitir cabeçalhos.

Não conclua que o remetente real é o endereço exibido sem examinar a origem e os cabeçalhos quando autenticidade for relevante.

## Planilha e cálculo

- Preserve o arquivo com fórmulas.
- Gere versão pesquisável das abas relevantes.
- Diferencie valor digitado, fórmula e resultado calculado.
- Registre filtros, linhas ocultas e células mescladas quando afetarem a leitura.
- Recalcule os totais antes de usar em peça.

## Arquivo repetido, corrompido ou desconhecido

- Duplicado exato: manter e registrar a coincidência de hash.
- Corrompido: não reparar o original. Trabalhar em cópia e pedir nova versão.
- Formato não reconhecido: registrar extensão, tamanho e origem; não inventar conteúdo.
- Arquivo sem extensão: identificar por assinatura técnica quando possível, sem alterar o original.

## Integridade e alcance do hash

O SHA-256 não é uma obrigação universal para todo documento de caso cível ou de família. Ele é um controle útil e barato para confirmar que uma cópia permaneceu idêntica ao arquivo recebido.

A Lei nº 11.419/2006 exige preservação dos originais digitalizados nas hipóteses do art. 11 e ressalva impugnação fundamentada de adulteração. Fonte oficial: https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2006/lei/l11419.htm

O art. 384 do Código de Processo Civil admite ata notarial para documentar fatos, inclusive dados representados por imagem ou som em arquivos eletrônicos. Fonte oficial: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105compilada.htm

Julgados recentes do STJ, em matéria penal e conforme as circunstâncias concretas examinadas, destacam a importância de mecanismos auditáveis, inclusive comparação de hashes, para prova digital. Não generalize automaticamente esses precedentes para todo caso cível. Fontes oficiais: https://scon.stj.jus.br/jurisprudencia/externo/informativo/?acao=pesquisar&aplicacao=informativo&livre=%40CNOT%3D%27022145%27 e https://processo.stj.jus.br/jurisprudencia/externo/informativo/?acao=pesquisar&ano=&b=INFJ&dtde=&dtdj=&l=25&livre=811&materia=&operador=e&orgao=&p=true&refinar=S.DISP.&relator=&thesaurus=JURIDICO

O hash não prova sozinho autoria, veracidade, origem, contexto ou licitude. Ele só tem utilidade probatória quando é possível saber de qual arquivo foi calculado, em que momento e com qual finalidade, e quando existe comparação posterior.
