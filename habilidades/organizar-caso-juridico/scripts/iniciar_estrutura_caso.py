#!/usr/bin/env python3
"""Cria, sem sobrescrever conteúdo, a estrutura padrão de um caso jurídico."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from uuid import uuid4


PASTAS = [
    "00 - ORIGINAIS RECEBIDOS - NAO ALTERAR",
    "01 - PROVAS ORGANIZADAS/DOCUMENTOS",
    "01 - PROVAS ORGANIZADAS/CONVERSAS E EMAILS",
    "01 - PROVAS ORGANIZADAS/AUDIOS",
    "01 - PROVAS ORGANIZADAS/VIDEOS",
    "01 - PROVAS ORGANIZADAS/FOTOS E CAPTURAS DE TELA",
    "01 - PROVAS ORGANIZADAS/OUTROS",
    "02 - TRANSCRICOES DE AUDIOS VIDEOS E CONVERSAS",
    "03 - PROCESSO JUDICIAL EM MARKDOWN",
    "04 - INDICE E CRONOLOGIA/FICHAS DAS PROVAS",
    "05 - PERGUNTAS E PENDENCIAS",
    "06 - ANALISE JURIDICA",
    "07 - PECAS EM ELABORACAO",
    "08 - PECAS FINALIZADAS E PROTOCOLOS",
]


def gravar_se_novo(caminho: Path, conteudo: str) -> bool:
    if caminho.exists():
        return False
    caminho.parent.mkdir(parents=True, exist_ok=True)
    temporario = caminho.with_name(f".{caminho.name}.{uuid4().hex}.tmp")
    temporario.write_text(conteudo, encoding="utf-8", newline="\n")
    os.replace(temporario, caminho)
    return True


def modelo_leia_primeiro(nome: str) -> str:
    return f"""# Leia primeiro: {nome}

## Para começar

1. Use Terra ou outro modelo equilibrado para organizar esta pasta.
2. Coloque tudo o que recebeu em `00 - ORIGINAIS RECEBIDOS - NAO ALTERAR`.
3. Para WhatsApp, exporte a conversa inteira com mídias e coloque o ZIP sem modificá-lo.
4. Inclua o PDF integral do processo, além de áudios, vídeos, fotografias, contratos, comprovantes, planilhas, e-mails, decisões e intimações.
5. Informe imediatamente qualquer prazo, audiência ou risco urgente.
6. Quando terminar, diga `PODE ORGANIZAR`.

Sol ou modelo de alto raciocínio será usado na análise jurídica. Astra ou modelo de máxima capacidade fica reservado para caso complexo ou revisão final sensível.

## Situação atual

- Organização: NÃO INICIADA
- Área provável: [A CONFIRMAR]
- Prazo ou audiência: [A CONFIRMAR]
- Última atualização: [A CONFIRMAR]
- Modelo sugerido para a próxima etapa: Terra ou equivalente equilibrado

## Como consultar este caso

1. Leia o resumo objetivo.
2. Consulte o mapa de fatos e provas.
3. Abra somente as provas indicadas para a tarefa atual.
4. Confira no original qualquer trecho decisivo antes de usá-lo em peça.

## Atalhos

- [Resumo objetivo](04%20-%20INDICE%20E%20CRONOLOGIA/RESUMO-OBJETIVO-DO-CASO.md)
- [Inventário de provas](04%20-%20INDICE%20E%20CRONOLOGIA/INVENTARIO-DE-PROVAS.md)
- [Linha do tempo](04%20-%20INDICE%20E%20CRONOLOGIA/LINHA-DO-TEMPO.md)
- [Mapa de fatos e provas](04%20-%20INDICE%20E%20CRONOLOGIA/MAPA-DE-FATOS-E-PROVAS.md)
- [Índice do processo](03%20-%20PROCESSO%20JUDICIAL%20EM%20MARKDOWN/INDICE-DO-PROCESSO.md)
- [Perguntas e pendências](05%20-%20PERGUNTAS%20E%20PENDENCIAS/PENDENCIAS-ATUAIS.md)
"""


MODELOS = {
    "04 - INDICE E CRONOLOGIA/RESUMO-OBJETIVO-DO-CASO.md": """# Resumo objetivo do caso

## Partes e papéis

| Pessoa ou entidade | Papel | Fonte | Status |
|---|---|---|---|

## Resultado pretendido informado

[A CONFIRMAR]

## Fatos principais

[A PREENCHER APÓS A LEITURA]

## Pontos controvertidos

[A PREENCHER APÓS A LEITURA]

## Urgências

[A CONFIRMAR]
""",
    "04 - INDICE E CRONOLOGIA/INVENTARIO-DE-PROVAS.md": """# Inventário de provas

Este arquivo é sincronizado automaticamente. A análise do conteúdo fica nas fichas das provas e no mapa de fatos e provas.

| ID | Nome recebido | Original preservado | Cópia organizada | Origem informada | Duplicidade | Situação |
|---|---|---|---|---|---|---|
""",
    "04 - INDICE E CRONOLOGIA/LINHA-DO-TEMPO.md": """# Linha do tempo

| Data e hora | Evento | Pessoas envolvidas | Fonte e localizador | Situação |
|---|---|---|---|---|

## Eventos sem data confirmada

[A PREENCHER APÓS A LEITURA]
""",
    "04 - INDICE E CRONOLOGIA/MAPA-DE-FATOS-E-PROVAS.md": """# Mapa de fatos e provas

| Fato ou alegação | Quem afirma | Provas favoráveis | Provas contrárias | Limitações | Situação |
|---|---|---|---|---|---|
""",
    "04 - INDICE E CRONOLOGIA/RELATORIO-DE-CONFERENCIA.md": """# Relatório de conferência da organização

- Status: ORGANIZAÇÃO NÃO INICIADA
- Arquivos recebidos: 0
- Provas registradas: 0
- Duplicados exatos: 0
- PDFs de processo: 0
- Páginas de processo: 0
- Áudios e vídeos: 0
- Falhas ou arquivos inacessíveis: [A CONFIRMAR]
- Próxima etapa e modelo recomendado: Terra ou equivalente equilibrado
""",
    "03 - PROCESSO JUDICIAL EM MARKDOWN/INDICE-DO-PROCESSO.md": """# Índice do processo judicial em Markdown

Nenhum processo foi extraído até o momento.
""",
    "05 - PERGUNTAS E PENDENCIAS/PENDENCIAS-ATUAIS.md": """# Perguntas e pendências atuais

As perguntas serão produzidas depois da leitura do acervo.

## 1. Urgente

- [ ] Existe prazo, audiência ou risco com data próxima? [A CONFIRMAR]

## 2. Informações indispensáveis

[A PREENCHER APÓS A LEITURA]

## 3. Documentos que faltam

[A PREENCHER APÓS A LEITURA]

## 4. Esclarecimentos úteis

[A PREENCHER APÓS A LEITURA]

## 5. Decisões da advogada responsável

[A PREENCHER APÓS A LEITURA]
""",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cria a estrutura não destrutiva de um novo caso jurídico."
    )
    parser.add_argument("pasta_do_caso", help="Pasta que receberá a estrutura.")
    parser.add_argument("--nome", help="Nome interno exibido no LEIA-PRIMEIRO.md.")
    args = parser.parse_args()

    raiz = Path(args.pasta_do_caso).expanduser().resolve()
    if raiz.exists() and not raiz.is_dir():
        raise SystemExit(f"O destino existe e não é uma pasta: {raiz}")
    raiz.mkdir(parents=True, exist_ok=True)

    criados: list[str] = []
    preservados: list[str] = []

    for pasta in PASTAS:
        destino = raiz / Path(pasta)
        if destino.exists():
            if not destino.is_dir():
                raise SystemExit(f"Era esperada uma pasta, mas existe um arquivo: {destino}")
            preservados.append(str(destino.relative_to(raiz)))
        else:
            destino.mkdir(parents=True)
            criados.append(str(destino.relative_to(raiz)))

    nome = args.nome or raiz.name
    arquivos = {"LEIA-PRIMEIRO.md": modelo_leia_primeiro(nome), **MODELOS}
    for relativo, conteudo in arquivos.items():
        caminho = raiz / Path(relativo)
        if gravar_se_novo(caminho, conteudo):
            criados.append(relativo)
        else:
            preservados.append(relativo)

    estado = raiz / "04 - INDICE E CRONOLOGIA" / "ESTADO-DA-NUMERACAO.json"
    if gravar_se_novo(
        estado,
        json.dumps(
            {"proximo_id": 1, "identificadores_ja_utilizados": []},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
    ):
        criados.append(str(estado.relative_to(raiz)))
    else:
        preservados.append(str(estado.relative_to(raiz)))

    controle = raiz / "04 - INDICE E CRONOLOGIA" / "CONTROLE-TECNICO-DE-INTEGRIDADE.jsonl"
    if gravar_se_novo(controle, ""):
        criados.append(str(controle.relative_to(raiz)))
    else:
        preservados.append(str(controle.relative_to(raiz)))

    print(
        json.dumps(
            {
                "pasta_do_caso": str(raiz),
                "itens_criados": criados,
                "itens_ja_existentes_e_preservados": preservados,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
