"""Testes da camada documental: segmentação, leitura do FRE e coleta com downloads simulados."""

import base64
import os
import zipfile
from pathlib import Path

import pytest

from empresometro.documentos import coleta
from empresometro.documentos.texto import extrair_paginas, limpar, segmentar

RAIZ = Path(__file__).resolve().parents[1]


def criar_pdf(paginas: list[str]) -> bytes:
    """Monta um PDF mínimo, com uma linha de texto por página, para os testes."""
    objetos = ["<< /Type /Catalog /Pages 2 0 R >>", None, "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    filhos = []
    for texto in paginas:
        seguro = texto.replace("\\", "").replace("(", "").replace(")", "")
        fluxo = f"BT /F1 12 Tf 50 750 Td ({seguro}) Tj ET"
        objetos.append(f"<< /Length {len(fluxo)} >>\nstream\n{fluxo}\nendstream")
        conteudo = len(objetos)
        objetos.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents {conteudo} 0 R "
            "/Resources << /Font << /F1 3 0 R >> >> >>"
        )
        filhos.append(f"{len(objetos)} 0 R")
    objetos[1] = f"<< /Type /Pages /Kids [{' '.join(filhos)}] /Count {len(filhos)} >>"
    saida = b"%PDF-1.4\n"
    posicoes = []
    for numero, corpo in enumerate(objetos, start=1):
        posicoes.append(len(saida))
        saida += f"{numero} 0 obj\n{corpo}\nendobj\n".encode("latin-1")
    inicio_xref = len(saida)
    saida += f"xref\n0 {len(objetos) + 1}\n0000000000 65535 f \n".encode()
    for posicao in posicoes:
        saida += f"{posicao:010d} 00000 n \n".encode()
    saida += f"trailer\n<< /Size {len(objetos) + 1} /Root 1 0 R >>\nstartxref\n{inicio_xref}\n%%EOF\n".encode()
    return saida


def test_limpeza_e_segmentacao():
    assert limpar("a  b\r\n\r\n\r\n\r\nc\x00") == "a b\n\nc"
    assert segmentar([]) == [] and segmentar(["", " "]) == []
    unico = segmentar(["Texto curto."])
    assert unico == [{"texto": "Texto curto.", "pagina_inicial": 1, "pagina_final": 1, "caracteres": 12}]

    paginas = ["Primeira frase do risco. " * 60, "", "Segunda parte sobre liquidez. " * 60]
    trechos = segmentar(paginas)
    assert len(trechos) >= 3
    assert all(t["caracteres"] <= 1900 for t in trechos)
    assert trechos[0]["pagina_inicial"] == 1 and trechos[-1]["pagina_final"] == 3
    # Todo o conteúdo aparece em algum trecho, e vizinhos compartilham um pedaço.
    assert "Segunda parte sobre liquidez." in trechos[-1]["texto"]
    assert trechos[1]["texto"][:20] in trechos[0]["texto"]
    # Texto sem pontuação nem parágrafos também é dividido.
    assert len(segmentar(["x" * 5000])) >= 3


def test_extracao_de_pdf():
    paginas = extrair_paginas(criar_pdf(["Fato relevante sobre aquisicao", "Segunda pagina"]))
    assert paginas == ["Fato relevante sobre aquisicao", "Segunda pagina"]


def _xml_fre(pdf: bytes) -> bytes:
    conteudo = base64.b64encode(pdf).decode()
    return (
        '<?xml version="1.0" encoding="utf-8"?><XmlFormularioReferencia><Formulario>'
        f"<FatoresRisco><DescricaoFatoresRisco><NomeArquivoPdf>4.1.docx</NomeArquivoPdf>"
        f"<ImagemObjetoArquivoPdf>{conteudo}</ImagemObjetoArquivoPdf></DescricaoFatoresRisco>"
        "<ProcessosSigilosos><ImagemObjetoArquivoPdf></ImagemObjetoArquivoPdf></ProcessosSigilosos></FatoresRisco>"
        "<Documento><MotivoReapresentacao>Atualiza\xe7\xe3o</MotivoReapresentacao></Documento>"
        "</Formulario></XmlFormularioReferencia>"
    ).encode("cp1252")


def test_secoes_do_fre_com_codificacao_errada():
    secoes = coleta.extrair_secoes_fre(_xml_fre(criar_pdf(["Riscos de mercado e de credito"])))
    assert [(s["grupo"], s["item"]) for s in secoes] == [("FatoresRisco", "DescricaoFatoresRisco")]
    assert extrair_paginas(secoes[0]["pdf"]) == ["Riscos de mercado e de credito"]
    assert coleta.nome_da_secao("FatoresRisco", "DescricaoFatoresRisco") == "4. Fatores de risco / Descricao fatores risco"


def test_selecao_do_indice_do_ipe():
    linhas = [
        {"CNPJ_Companhia": "11.111.111/0001-11", "Categoria": "Fato Relevante", "Assunto": "A", "Versao": "1",
         "Protocolo_Entrega": "P1", "Link_Download": "http://x/1", "Data_Referencia": "2025-01-10", "Data_Entrega": "2025-01-10"},
        {"CNPJ_Companhia": "11.111.111/0001-11", "Categoria": "Fato Relevante", "Assunto": "A corrigido", "Versao": "2",
         "Protocolo_Entrega": "P1", "Link_Download": "http://x/2", "Data_Referencia": "2025-01-10", "Data_Entrega": "2025-01-11"},
        {"CNPJ_Companhia": "11.111.111/0001-11", "Categoria": "Assembleia", "Assunto": "Ata", "Versao": "1",
         "Protocolo_Entrega": "P2", "Link_Download": "http://x/3"},
        {"CNPJ_Companhia": "99.999.999/0001-99", "Categoria": "Fato Relevante", "Assunto": "Outra", "Versao": "1",
         "Protocolo_Entrega": "P3", "Link_Download": "http://x/4"},
    ]
    escolhidos = coleta.selecionar_ipe(linhas, {"11111111000111"})
    assert [(e["assunto"], e["versao"], e["link"]) for e in escolhidos] == [("A corrigido", 2, "http://x/2")]


@pytest.mark.skipif(not os.environ.get("DATABASE_URL"), reason="DATABASE_URL não definida")
def test_coleta_completa_com_downloads_simulados(tmp_path, monkeypatch):
    from alembic import command
    from alembic.config import Config

    from empresometro.documentos.relatorio import gerar_relatorio_coleta
    from empresometro.etl.fontes import conectar

    cfg = Config(str(RAIZ / "alembic.ini"))
    cfg.set_main_option("script_location", str(RAIZ / "migrations"))
    command.downgrade(cfg, "base")
    command.upgrade(cfg, "head")
    conn = conectar()
    conn.autocommit = True
    try:
        cia = conn.execute(
            "INSERT INTO companhia (cnpj, denominacao, ativa) VALUES ('11111111000111', 'ALFA S.A.', true) RETURNING id"
        ).fetchone()[0]
        doc = conn.execute(
            "INSERT INTO documento (companhia_id, tipo, dt_referencia, versao, vigente) "
            "VALUES (%s, 'DFP', '2025-12-31', 1, true) RETURNING id", (cia,)
        ).fetchone()[0]
        conn.execute(
            "INSERT INTO parecer (documento_id, tipo_relatorio, tipo_parecer, item, texto) VALUES (%s, %s, %s, 1, %s)",
            (doc, "Sem Ressalva", "Relatório do Auditor Independente", "Opinião sem ressalva sobre as demonstrações. " * 20),
        )
        piloto = [{"cnpj": "11111111000111", "denominacao": "ALFA S.A."}]

        # Índices sintéticos do IPE e do FRE.
        def zipar(nome_zip: str, membro: str, linhas: list[str]) -> Path:
            caminho = tmp_path / nome_zip
            with zipfile.ZipFile(caminho, "w") as z:
                z.writestr(membro, ("\r\n".join(linhas) + "\r\n").encode("latin-1"))
            return caminho

        indices = {
            "ipe": zipar("ipe_cia_aberta_2025.zip", "ipe_cia_aberta_2025.csv", [
                "CNPJ_Companhia;Nome_Companhia;Codigo_CVM;Data_Referencia;Categoria;Tipo;Especie;Assunto;Data_Entrega;Tipo_Apresentacao;Protocolo_Entrega;Versao;Link_Download",
                "11.111.111/0001-11;ALFA;1023;2025-03-01;Fato Relevante;;;Pedido de recuperação judicial;2025-03-01;AP;P1;1;http://cvm/ipe1",
                "11.111.111/0001-11;ALFA;1023;2025-04-01;Comunicado ao Mercado;Outros;;Arquivo que não é PDF;2025-04-01;AP;P2;1;http://cvm/ipe2",
                "11.111.111/0001-11;ALFA;1023;2025-05-01;Comunicado ao Mercado;Outros;;Servidor fora do ar;2025-05-01;AP;P3;1;http://cvm/ipe3",
            ]),
            "fre": zipar("fre_cia_aberta_2025.zip", "fre_cia_aberta_2025.csv", [
                "CNPJ_CIA;DT_REFER;VERSAO;DENOM_CIA;CD_CVM;CATEG_DOC;ID_DOC;DT_RECEB;LINK_DOC",
                "11.111.111/0001-11;2025-12-31;1;ALFA;001023;FRE;500;2025-05-30;http://cvm/fre-v1",
                "11.111.111/0001-11;2025-12-31;2;ALFA;001023;FRE;501;2025-08-30;http://cvm/fre-v2",
            ]),
        }
        monkeypatch.setattr(coleta, "_obter_indice", lambda tipo, ano, pasta: indices.get(tipo))

        pacote_fre = tmp_path / "fre.zip"
        with zipfile.ZipFile(pacote_fre, "w") as z:
            z.writestr("FormularioCadastral.xml", "<x/>")
            z.writestr("001023FRE.xml", _xml_fre(criar_pdf(["Riscos de mercado e de credito da companhia"])))
        respostas = {
            "http://cvm/ipe1": criar_pdf(["A companhia ajuizou pedido de recuperacao judicial", "Pagina dois"]),
            "http://cvm/ipe2": b"<html>" + b"x" * 600,
            "http://cvm/fre-v2": pacote_fre.read_bytes(),
        }
        chamadas = []

        def baixar_simulado(url, timeout=180):
            chamadas.append(url)
            if url not in respostas:
                raise RuntimeError("HTTPError: 503")
            return respostas[url]

        monkeypatch.setattr(coleta, "baixar_bytes", baixar_simulado)

        progresso = coleta.Progresso(registrar=lambda _: None)
        coleta.coletar_pareceres(conn, piloto, [2025], progresso)
        coleta.coletar_ipe(conn, piloto, [2025], tmp_path, progresso)
        coleta.coletar_fre(conn, piloto, [2025], tmp_path, progresso)

        situacoes = dict(conn.execute(
            "SELECT fonte || ':' || situacao, count(*) FROM documento_texto GROUP BY 1").fetchall())
        # IPE: um PDF bom, um arquivo que não é PDF e uma falha de rede. FRE: uma seção e o marcador do pacote.
        assert situacoes == {"PARECER:OK": 1, "IPE:OK": 1, "IPE:ERRO": 2, "FRE:OK": 1, "FRE:SEM_TEXTO": 1}
        assert "http://cvm/fre-v1" not in chamadas  # só a última versão do formulário é baixada

        pagina, titulo = conn.execute(
            "SELECT t.pagina_inicial, d.titulo FROM trecho t JOIN documento_texto d ON d.id = t.documento_texto_id, "
            "websearch_to_tsquery('portuguese', 'recuperacao judicial') q WHERE t.busca @@ q AND d.fonte = 'IPE'"
        ).fetchone()
        assert (pagina, titulo) == (1, "Pedido de recuperação judicial")
        secao = conn.execute("SELECT secao, tipo FROM documento_texto WHERE fonte = 'FRE' AND situacao = 'OK'").fetchone()
        assert secao == ("FatoresRisco/DescricaoFatoresRisco", "4. Fatores de risco")

        # Segunda execução: só os documentos com erro são tentados de novo.
        chamadas.clear()
        coleta.coletar_pareceres(conn, piloto, [2025], progresso)
        coleta.coletar_ipe(conn, piloto, [2025], tmp_path, progresso)
        coleta.coletar_fre(conn, piloto, [2025], tmp_path, progresso)
        assert sorted(chamadas) == ["http://cvm/ipe2", "http://cvm/ipe3"]
        assert conn.execute("SELECT count(*) FROM documento_texto").fetchone()[0] == 6

        texto = gerar_relatorio_coleta(conn, progresso.eventos)
        assert "| ALFA S.A. | 3 | 1 | 1 |" in texto
    finally:
        conn.close()
        command.downgrade(cfg, "base")
