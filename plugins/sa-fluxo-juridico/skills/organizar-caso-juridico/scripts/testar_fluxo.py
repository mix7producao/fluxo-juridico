#!/usr/bin/env python3
"""Teste integrado e descartável dos scripts da habilidade."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from reportlab.pdfgen import canvas


SCRIPTS = Path(__file__).resolve().parent


def executar(nome: str, *argumentos: str, codigos: tuple[int, ...] = (0,)) -> subprocess.CompletedProcess[str]:
    resultado = subprocess.run(
        [sys.executable, "-B", "-X", "utf8", str(SCRIPTS / nome), *map(str, argumentos)],
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
    if resultado.returncode not in codigos:
        raise AssertionError(
            f"{nome} retornou {resultado.returncode}.\nSTDOUT:\n{resultado.stdout}\nSTDERR:\n{resultado.stderr}"
        )
    return resultado


def hash_arquivo(caminho: Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def ler_jsonl(caminho: Path) -> list[dict]:
    return [json.loads(linha) for linha in caminho.read_text(encoding="utf-8").splitlines() if linha.strip()]


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="teste_caso_juridico_") as temporario:
        base = Path(temporario)
        caso = base / "Caso de teste"
        executar("iniciar_estrutura_caso.py", caso, "--nome", "Caso de teste")
        executar("iniciar_estrutura_caso.py", caso, "--nome", "Caso de teste")

        originais = caso / "00 - ORIGINAIS RECEBIDOS - NAO ALTERAR"
        contrato = originais / "contrato com acentuação.txt"
        contrato.write_text("Contrato de teste com cláusula e obrigação.\n", encoding="utf-8")
        audio = originais / "áudio recebido.m4a"
        audio.write_bytes(b"audio-de-teste-nao-executavel")

        pdf = originais / "processo completo.pdf"
        documento = canvas.Canvas(str(pdf))
        documento.drawString(72, 780, "Página um do processo de teste.")
        documento.showPage()
        documento.drawString(72, 780, "Página dois do processo de teste.")
        documento.showPage()
        documento.showPage()
        documento.save()

        zip_seguro = originais / "WhatsApp seguro.zip"
        with zipfile.ZipFile(zip_seguro, "w", zipfile.ZIP_DEFLATED) as arquivo:
            arquivo.writestr("Conversa do WhatsApp.txt", "09/09/2026 10:00 - Pessoa: Mensagem\n")
            arquivo.writestr("IMG-0001.jpg", b"imagem-de-teste")

        primeira = executar("inventariar_originais.py", caso)
        assert json.loads(primeira.stdout)["novos_registros"] == 4
        segunda = executar("inventariar_originais.py", caso)
        assert json.loads(segunda.stdout)["novos_registros"] == 0

        inventario_visivel = caso / "04 - INDICE E CRONOLOGIA" / "INVENTARIO-DE-PROVAS.md"
        assert inventario_visivel.read_text(encoding="utf-8").count("| PROVA-") == 4

        novo = originais / "comprovante novo.txt"
        novo.write_text("Comprovante incluído depois do primeiro inventário.\n", encoding="utf-8")
        deteccao_novo = executar("validar_caso.py", caso, codigos=(2,))
        resultado_novo = json.loads(deteccao_novo.stdout)
        assert any("Original ainda não inventariado" in erro for erro in resultado_novo["erros"])
        terceira = executar("inventariar_originais.py", caso)
        assert json.loads(terceira.stdout)["novos_registros"] == 1

        controle = caso / "04 - INDICE E CRONOLOGIA" / "CONTROLE-TECNICO-DE-INTEGRIDADE.jsonl"
        registros = ler_jsonl(controle)
        por_nome = {item["nome_original"]: item for item in registros}
        antes = hash_arquivo(contrato)
        parametros = {
            contrato.name: ("documento", "CONTRATO", "LOCACAO-DE-TESTE"),
            audio.name: ("audio", "AUDIO", "CONVERSA-DE-TESTE"),
            pdf.name: ("documento", "PROCESSO", "PROCESSO-DE-TESTE"),
            zip_seguro.name: ("conversa", "WHATSAPP", "EXPORTACAO-DE-TESTE"),
            novo.name: ("documento", "COMPROVANTE", "PAGAMENTO-DE-TESTE"),
        }
        for registro in registros:
            categoria, tipo, assunto = parametros[registro["nome_original"]]
            executar("copiar_prova_organizada.py", caso, registro["id"], categoria, tipo, assunto)
        assert hash_arquivo(contrato) == antes

        id_contrato = por_nome[contrato.name]["id"]
        repetida = executar(
            "copiar_prova_organizada.py",
            caso,
            id_contrato,
            "documento",
            "CONTRATO",
            "LOCACAO-DE-TESTE",
        )
        assert json.loads(repetida.stdout)["status"] == "COPIA_JA_EXISTIA_E_FOI_CONFERIDA"
        executar(
            "copiar_prova_organizada.py",
            caso,
            id_contrato,
            "documento",
            "CONTRATO",
            "OUTRO-NOME-RECUSADO",
            codigos=(1,),
        )
        assert len([item for item in (caso / "01 - PROVAS ORGANIZADAS").rglob(f"{id_contrato}_*") if item.is_file()]) == 1

        copias = ler_jsonl(caso / "04 - INDICE E CRONOLOGIA" / "CONTROLE-DAS-COPIAS-ORGANIZADAS.jsonl")
        copia_por_id = {
            item["id"]: caso / Path(item["caminho_copia_organizada"])
            for item in copias
            if item.get("tipo_registro") == "COPIA_ORGANIZADA"
        }

        id_pdf = por_nome[pdf.name]["id"]
        saida_pdf = caso / "03 - PROCESSO JUDICIAL EM MARKDOWN" / f"{id_pdf}_PROCESSO-TESTE"
        executar(
            "extrair_pdf_para_md.py",
            copia_por_id[id_pdf],
            saida_pdf,
            "--id-prova",
            id_pdf,
        )
        relatorio_pdf = json.loads((saida_pdf / "RELATORIO-DA-EXTRACAO.json").read_text(encoding="utf-8"))
        assert relatorio_pdf["total_paginas_pdf"] == 3
        assert relatorio_pdf["total_marcadores_markdown"] == 3
        assert relatorio_pdf["paginas_pendentes_de_ocr_ou_revisao"] == [3]
        indice_principal = caso / "03 - PROCESSO JUDICIAL EM MARKDOWN" / "INDICE-DO-PROCESSO.md"
        assert f"{id_pdf}_PROCESSO-TESTE" in indice_principal.read_text(encoding="utf-8")

        id_zip = por_nome[zip_seguro.name]["id"]
        saida_zip = caso / "02 - TRANSCRICOES DE AUDIOS VIDEOS E CONVERSAS" / f"{id_zip}_WHATSAPP"
        executar(
            "extrair_zip_whatsapp.py",
            copia_por_id[id_zip],
            saida_zip,
            "--id-prova",
            id_zip,
        )
        manifesto = json.loads((saida_zip / "MANIFESTO-DA-EXTRACAO.json").read_text(encoding="utf-8"))
        assert manifesto["quantidade_de_arquivos"] == 2
        assert len(manifesto["conversas_markdown"]) == 1
        assert manifesto["pendencia_conversao"] is None
        assert (saida_zip / manifesto["conversas_markdown"][0]).is_file()

        zip_malicioso = base / "malicioso.zip"
        with zipfile.ZipFile(zip_malicioso, "w", zipfile.ZIP_DEFLATED) as arquivo:
            arquivo.writestr("../../fora.txt", "não pode sair")
        destino_malicioso = base / "saida maliciosa"
        executar("extrair_zip_whatsapp.py", zip_malicioso, destino_malicioso, codigos=(2,))
        assert not (base / "fora.txt").exists()

        validacao_pendente = executar("validar_caso.py", caso, codigos=(1,))
        resultado_pendente = json.loads(validacao_pendente.stdout)
        assert resultado_pendente["status"] == "INCOMPLETO_COM_PENDENCIAS"
        pendencias = caso / "05 - PERGUNTAS E PENDENCIAS" / "PENDENCIAS-ATUAIS.md"
        texto_pendencias = pendencias.read_text(encoding="utf-8")
        assert "Mídia sem transcrição" in texto_pendencias
        assert "PDF ainda sem revisão visual" in texto_pendencias
        assert texto_pendencias.count("<!-- INICIO: PENDENCIAS TECNICAS AUTOMATICAS -->") == 1

        executar(
            "registrar_revisao_pdf.py",
            saida_pdf,
            "--responsavel",
            "Teste automatizado",
            "--observacao",
            "Páginas textuais conferidas e página vazia confirmada.",
            "--resolver",
            "3=PAGINA_VAZIA_CONFIRMADA",
            "--confirmo-revisao-integral",
        )

        id_audio = por_nome[audio.name]["id"]
        transcricao_audio = (
            caso
            / "02 - TRANSCRICOES DE AUDIOS VIDEOS E CONVERSAS"
            / f"{id_audio}_TRANSCRICAO-INTEGRAL.md"
        )
        transcricao_audio.write_text(
            f"# {id_audio}: transcrição integral\n\n[00:00:00] LOCUTOR 1: conteúdo de teste.\n",
            encoding="utf-8",
        )
        (caso / "04 - INDICE E CRONOLOGIA" / "RESUMO-OBJETIVO-DO-CASO.md").write_text(
            "# Resumo objetivo do caso\n\nCaso descartável para validação dos scripts.\n",
            encoding="utf-8",
        )
        (caso / "04 - INDICE E CRONOLOGIA" / "LINHA-DO-TEMPO.md").write_text(
            "# Linha do tempo\n\nNenhum evento material foi criado no teste.\n",
            encoding="utf-8",
        )
        (caso / "04 - INDICE E CRONOLOGIA" / "MAPA-DE-FATOS-E-PROVAS.md").write_text(
            "# Mapa de fatos e provas\n\nConteúdo fictício restrito ao teste técnico.\n",
            encoding="utf-8",
        )
        pendencias.write_text(
            "# Perguntas e pendências atuais\n\nNenhuma pergunta factual no caso descartável de teste.\n",
            encoding="utf-8",
        )
        (caso / "LEIA-PRIMEIRO.md").write_text(
            "# Leia primeiro: Caso de teste\n\n- Organização: CONCLUÍDA\n- Próxima etapa: análise jurídica com Sol ou equivalente.\n",
            encoding="utf-8",
        )

        validacao_final = executar("validar_caso.py", caso)
        resultado_final = json.loads(validacao_final.stdout)
        assert resultado_final["status"] == "APROVADO"
        assert not resultado_final["erros"]
        assert not resultado_final["pendencias"]
        texto_final_pendencias = pendencias.read_text(encoding="utf-8")
        assert "Original ainda não inventariado" not in texto_final_pendencias
        assert texto_final_pendencias.count("<!-- INICIO: PENDENCIAS TECNICAS AUTOMATICAS -->") == 1

        inventario_correto = inventario_visivel.read_text(encoding="utf-8")
        inventario_visivel.write_text(
            inventario_correto.replace("CÓPIA ORGANIZADA", "NÃO EXAMINADA"),
            encoding="utf-8",
        )
        adulterado = executar("validar_caso.py", caso, codigos=(2,))
        assert any("situação correta" in erro for erro in json.loads(adulterado.stdout)["erros"])
        inventario_visivel.write_text(inventario_correto, encoding="utf-8")

        texto_audio = transcricao_audio
        conteudo_audio = texto_audio.read_text(encoding="utf-8")
        texto_audio.write_text("", encoding="utf-8")
        vazio_audio = executar("validar_caso.py", caso, codigos=(1,))
        assert any("vazio ou sem marcação de tempo" in item for item in json.loads(vazio_audio.stdout)["pendencias"])
        texto_audio.write_text(conteudo_audio, encoding="utf-8")

        registro_pdf = saida_pdf / "REGISTRO-DA-REVISAO.md"
        conteudo_registro_pdf = registro_pdf.read_text(encoding="utf-8")
        registro_pdf.unlink()
        sem_registro_pdf = executar("validar_caso.py", caso, codigos=(2,))
        assert any("Registro da revisão do PDF ausente" in erro for erro in json.loads(sem_registro_pdf.stdout)["erros"])
        registro_pdf.write_text(conteudo_registro_pdf, encoding="utf-8")

        conversa_md = saida_zip / manifesto["conversas_markdown"][0]
        conteudo_conversa = conversa_md.read_bytes()
        conversa_md.write_text("", encoding="utf-8")
        conversa_vazia = executar("validar_caso.py", caso, codigos=(2,))
        erros_conversa = json.loads(conversa_vazia.stdout)["erros"]
        assert any("Markdown da conversa foi alterado" in erro for erro in erros_conversa)
        conversa_md.write_bytes(conteudo_conversa)

        zip_alheio = base / "WhatsApp alheio.zip"
        with zipfile.ZipFile(zip_alheio, "w", zipfile.ZIP_DEFLATED) as arquivo:
            arquivo.writestr("Conversa do WhatsApp.txt", "10/09/2026 09:00 - Outra pessoa: Outro caso\n")
        saida_alheia = caso / "02 - TRANSCRICOES DE AUDIOS VIDEOS E CONVERSAS" / "EXTRACAO-ALHEIA"
        executar("extrair_zip_whatsapp.py", zip_alheio, saida_alheia, "--id-prova", id_zip)
        zip_incorreto = executar("validar_caso.py", caso, codigos=(2,))
        assert any("ZIP extraído não corresponde" in erro for erro in json.loads(zip_incorreto.stdout)["erros"])
        shutil.rmtree(saida_alheia)

        pendencias.write_text(
            "# Perguntas e pendências atuais\n\nNenhuma pergunta factual no caso descartável de teste.\n",
            encoding="utf-8",
        )
        confirmacao_final = executar("validar_caso.py", caso)
        assert json.loads(confirmacao_final.stdout)["status"] == "APROVADO"

        print(
            json.dumps(
                {
                    "status": "TESTE_INTEGRADO_APROVADO",
                    "original_novo_detectado": True,
                    "numeração_idempotente": True,
                    "original_preservado": True,
                    "uma_copia_por_id": True,
                    "inventario_visivel_sincronizado": True,
                    "pdf_com_todas_as_paginas": True,
                    "indice_principal_atualizado": True,
                    "revisao_pdf_registrada": True,
                    "whatsapp_convertido_para_markdown": True,
                    "path_traversal_bloqueado": True,
                    "pendencias_persistidas_e_resolvidas": True,
                    "falsos_aprovados_bloqueados": True,
                    "utf8_validado": True,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
