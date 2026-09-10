# Execução local e dependências

## No Codex Desktop

Antes do primeiro script, carregue os caminhos das dependências do espaço de trabalho. Use o executável Python retornado pelo ambiente e acrescente `-B -X utf8`.

Não presuma que o comando `python` do sistema possui as bibliotecas necessárias. O processamento de PDF requer `pypdf`. O teste integrado também usa `reportlab`, apenas para criar um PDF descartável de teste.

Execute `scripts/verificar_ambiente.py` com os requisitos da etapa:

```text
python -B -X utf8 scripts/verificar_ambiente.py --exigir pdf
python -B -X utf8 scripts/verificar_ambiente.py --exigir midia
python -B -X utf8 scripts/verificar_ambiente.py --exigir teste
```

Se uma dependência estiver ausente, use primeiro o runtime fornecido pelo ambiente. Não envie arquivo sigiloso a serviço externo e não instale ferramenta em ambiente compartilhado sem verificar a política do escritório.

## Códigos de saída

- `0`: operação concluída ou caso integralmente aprovado.
- `1`: operação executada, mas o caso ainda possui pendências registradas.
- `2`: falha técnica, inconsistência ou violação de integridade.

A extração inicial de um PDF pode retornar `0` e manter o status interno como revisão pendente. O caso completo continuará retornando `1` no validador até que a revisão seja registrada.

## Caminhos no Windows

Coloque entre aspas qualquer caminho com espaço ou acento. Use sempre a pasta exata do caso, nunca uma pasta ampla ou a raiz do OneDrive.
