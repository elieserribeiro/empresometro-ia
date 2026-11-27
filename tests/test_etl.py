"""Testes do ETL com arquivos sintéticos. Exigem PostgreSQL em DATABASE_URL."""

import os
import zipfile
from decimal import Decimal
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(
    not os.environ.get("DATABASE_URL"), reason="DATABASE_URL não definida"
)

RAIZ = Path(__file__).resolve().parents[1]

CADASTRO = [
    "CNPJ_CIA;DENOM_SOCIAL;DENOM_COMERC;DT_REG;DT_CONST;DT_CANCEL;SIT;DT_INI_SIT;CD_CVM;SETOR_ATIV;TP_MERC;CATEG_REG;SIT_EMISSOR;CONTROLE_ACIONARIO;MUN;UF",
    "11.111.111/0001-11;ALFA S.A.;ALFA;2000-01-01;1990-01-01;;ATIVO;2000-01-01;001023;Bancos;BOLSA;Categoria A;FASE OPERACIONAL;PRIVADO;SÃO PAULO;SP",
    "11.111.111/0001-11;ALFA S.A.;ALFA;2000-01-01;1990-01-01;;ATIVO;2000-01-01;001023;Bancos;BALCÃO ORGANIZADO;Categoria A;FASE OPERACIONAL;PRIVADO;SÃO PAULO;SP",
    "22.222.222/0001-22;BETA PARTICIPAÇÕES S.A.;BETA;2010-01-01;2009-01-01;;ATIVO;2010-01-01;2000;Emp. Adm. Part. - Máqs., Equip., Veíc. e Peças;;Categoria B;EM RECUPERAÇÃO JUDICIAL OU EQUIVALENTE;PRIVADO;RIO;RJ",
    "33.333.333/0001-33;GAMA S.A.;GAMA;1990-01-01;1980-01-01;2024-06-01;CANCELADA;2024-06-01;3000;Comércio (Atacado e Varejo);BOLSA;Categoria A;;PRIVADO;BH;MG",
    "44.444.444/0001-44;DELTA S.A.;DELTA;1990-01-01;1980-01-01;2015-06-01;CANCELADA;2015-06-01;4000;Alimentos;BOLSA;Categoria A;;PRIVADO;BH;MG",
]

INDICE = [
    "CNPJ_CIA;DT_REFER;VERSAO;DENOM_CIA;CD_CVM;CATEG_DOC;ID_DOC;DT_RECEB;LINK_DOC",
    "11.111.111/0001-11;2023-12-31;1;ALFA S.A.;001023;DFP;101;2024-03-01;http://x/101",
    "11.111.111/0001-11;2023-12-31;2;ALFA S.A.;001023;DFP;102;2024-05-01;http://x/102",
    "33.333.333/0001-33;2023-12-31;1;GAMA S.A.;003000;DFP;103;2024-03-10;http://x/103",
    "55.555.555/0001-55;2023-12-31;1;ÉPSILON S.A.;005000;DFP;104;2024-03-11;http://x/104",
]
CAB_BP = "CNPJ_CIA;DT_REFER;VERSAO;DENOM_CIA;CD_CVM;GRUPO_DFP;MOEDA;ESCALA_MOEDA;ORDEM_EXERC;DT_FIM_EXERC;CD_CONTA;DS_CONTA;VL_CONTA;ST_CONTA_FIXA"
BPA = [
    CAB_BP,
    "11.111.111/0001-11;2023-12-31;2;ALFA S.A.;001023;BPA;REAL;MIL;ÚLTIMO;2023-12-31;1;Ativo Total;1500.5000000000;S",
    "11.111.111/0001-11;2023-12-31;2;ALFA S.A.;001023;BPA;REAL;MIL;PENÚLTIMO;2022-12-31;1;Ativo Total;1200.0000000000;S",
    "11.111.111/0001-11;2023-12-31;2;ALFA S.A.;001023;BPA;REAL;MIL;ÚLTIMO;2023-12-31;1.01;Ativo Circulante;;S",
    "33.333.333/0001-33;2023-12-31;1;GAMA S.A.;003000;BPA;REAL;UNIDADE;ÚLTIMO;2023-12-31;1;Ativo Total;777.0000000000;S",
    "99.999.999/0001-99;2023-12-31;1;SEM INDICE;009999;BPA;REAL;MIL;ÚLTIMO;2023-12-31;1;Ativo Total;1.0;S",
]
BPP = [
    CAB_BP,
    "11.111.111/0001-11;2023-12-31;2;ALFA S.A.;001023;BPP;REAL;MIL;ÚLTIMO;2023-12-31;2;Passivo Total;1500.5000000000;S",
]
DRE = [
    "CNPJ_CIA;DT_REFER;VERSAO;DENOM_CIA;CD_CVM;GRUPO_DFP;MOEDA;ESCALA_MOEDA;ORDEM_EXERC;DT_INI_EXERC;DT_FIM_EXERC;CD_CONTA;DS_CONTA;VL_CONTA;ST_CONTA_FIXA",
    "11.111.111/0001-11;2023-12-31;2;ALFA S.A.;001023;DRE;REAL;MIL;ÚLTIMO;2023-01-01;2023-12-31;3.01;Receita;-10.0000000000;S",
    "11.111.111/0001-11;2023-12-31;2;ALFA S.A.;001023;DRE;REAL;MIL;ÚLTIMO;2023-01-01;2023-12-31;3.01;Receita;-10.0000000000;S",
]
CAPITAL = [
    "CNPJ_CIA;DT_REFER;VERSAO;DENOM_CIA;QT_ACAO_ORDIN_CAP_INTEGR;QT_ACAO_PREF_CAP_INTEGR;QT_ACAO_TOTAL_CAP_INTEGR;QT_ACAO_ORDIN_TESOURO;QT_ACAO_PREF_TESOURO;QT_ACAO_TOTAL_TESOURO",
    "11.111.111/0001-11;2023-12-31;2;ALFA S.A.;100;50;150;1;0;1",
]
PARECER = [
    "CNPJ_CIA;DT_REFER;VERSAO;DENOM_CIA;TP_RELAT_AUD;TP_PARECER_DECL;NUM_ITEM_PARECER_DECL;TXT_PARECER_DECL",
    "11.111.111/0001-11;2023-12-31;2;ALFA S.A.;Sem Ressalva;Relatório do Auditor Independente;1;Texto do parecer.",
]


def _csv(linhas):
    return ("\r\n".join(linhas) + "\r\n").encode("latin-1")


@pytest.fixture(scope="module")
def conn():
    from alembic import command
    from alembic.config import Config

    from empresometro.etl.fontes import conectar

    cfg = Config(str(RAIZ / "alembic.ini"))
    cfg.set_main_option("script_location", str(RAIZ / "migrations"))
    command.downgrade(cfg, "base")
    command.upgrade(cfg, "head")
    conexao = conectar()
    conexao.autocommit = True
    yield conexao
    conexao.close()
    command.downgrade(cfg, "base")


@pytest.fixture(scope="module")
def pasta(tmp_path_factory):
    pasta = tmp_path_factory.mktemp("bruto")
    (pasta / "cad_cia_aberta.csv").write_bytes(_csv(CADASTRO))
    with zipfile.ZipFile(pasta / "dfp_cia_aberta_2023.zip", "w") as z:
        z.writestr("dfp_cia_aberta_2023.csv", _csv(INDICE))
        z.writestr("dfp_cia_aberta_BPA_con_2023.csv", _csv(BPA))
        z.writestr("dfp_cia_aberta_BPP_con_2023.csv", _csv(BPP))
        z.writestr("dfp_cia_aberta_DRE_ind_2023.csv", _csv(DRE))
        z.writestr("dfp_cia_aberta_composicao_capital_2023.csv", _csv(CAPITAL))
        z.writestr("dfp_cia_aberta_parecer_2023.csv", _csv(PARECER))
    return pasta


@pytest.fixture(scope="module")
def carga(conn, pasta):
    from empresometro.etl.__main__ import executar_carga

    return executar_carga(conn, pasta, ["dfp"], [2023], usar_local=True, registrar=lambda _: None)


def _um(conn, sql, *params):
    return conn.execute(sql, params).fetchone()


def test_setor_base_e_holding():
    from empresometro.etl.cadastro import classificar_setor

    assert classificar_setor("Bancos") == ("Bancos", False)
    assert classificar_setor("Emp. Adm. Part. - Bancos") == ("Bancos", True)
    assert classificar_setor("Emp. Adm. Part. - Máqs., Equip., Veíc. e Peças") == (
        "Máquinas, Equipamentos, Veículos e Peças", True,
    )


def test_companhias_ativas_inativas_e_fora_do_cadastro(conn, carga):
    # Ativas: ALFA e BETA. Inativas com documento: GAMA e ÉPSILON (fora do cadastro).
    # DELTA, cancelada e sem documento na janela, não entra.
    assert _um(conn, "SELECT count(*) FROM companhia")[0] == 4
    assert _um(conn, "SELECT count(*) FROM companhia WHERE ativa")[0] == 2
    assert _um(conn, "SELECT ativa, data_cancelamento::text FROM companhia WHERE cnpj = '33333333000133'") == (False, "2024-06-01")
    assert _um(conn, "SELECT denominacao, situacao_registro FROM companhia WHERE cnpj = '55555555000155'") == ("ÉPSILON S.A.", "FORA DO CADASTRO")
    assert _um(conn, "SELECT count(*) FROM companhia WHERE cnpj = '44444444000144'")[0] == 0


def test_mercados_e_situacao_do_emissor(conn, carga):
    mercados = conn.execute(
        "SELECT m.tipo_mercado FROM companhia_mercado m JOIN companhia c ON c.id = m.companhia_id "
        "WHERE c.cnpj = '11111111000111' ORDER BY 1"
    ).fetchall()
    assert [m[0] for m in mercados] == ["BALCÃO ORGANIZADO", "BOLSA"]
    assert _um(conn, "SELECT cd_cvm FROM companhia WHERE cnpj = '11111111000111'")[0] == 1023
    assert _um(
        conn,
        "SELECT c.situacao_emissor, s.setor_base, s.holding FROM companhia c JOIN setor s ON s.id = c.setor_id "
        "WHERE c.cnpj = '22222222000122'",
    ) == ("EM RECUPERAÇÃO JUDICIAL OU EQUIVALENTE", "Máquinas, Equipamentos, Veículos e Peças", True)


def test_versoes_e_vigente(conn, carga):
    versoes = conn.execute(
        "SELECT d.versao, d.vigente FROM documento d JOIN companhia c ON c.id = d.companhia_id "
        "WHERE c.cnpj = '11111111000111' ORDER BY 1"
    ).fetchall()
    assert versoes == [(1, False), (2, True)]
    assert _um(conn, "SELECT count(*) FROM documento")[0] == 4


def test_linhas_valores_e_orfas(conn, carga):
    evento = next(e for e in carga if e["arquivo"] == "dfp_cia_aberta_2023.zip")
    assert evento["linhas"] == 7
    assert evento["linhas_orfas"] == 1
    assert evento["por_demonstracao"] == {"BPA_CON": 4, "BPP_CON": 1, "DRE_IND": 2}
    # Milhares são convertidos em reais; unidades ficam como estão.
    assert _um(
        conn,
        "SELECT valor_original, valor_reais, ordem_exercicio, dt_fim::text FROM demonstracao_linha "
        "WHERE demonstracao = 'BPA' AND cd_conta = '1' AND ordem_exercicio = 'ULTIMO' AND escala = 'MIL'",
    ) == (Decimal("1500.500000"), Decimal("1500500.00"), "ULTIMO", "2023-12-31")
    assert _um(conn, "SELECT valor_reais FROM demonstracao_linha WHERE escala = 'UNIDADE'")[0] == Decimal("777.00")
    assert _um(conn, "SELECT count(*) FROM demonstracao_linha WHERE ordem_exercicio = 'PENULTIMO'")[0] == 1
    assert _um(conn, "SELECT count(*) FROM demonstracao_linha WHERE valor_original IS NULL")[0] == 1
    # Linhas repetidas no arquivo são preservadas e distinguidas pela sequência.
    assert conn.execute(
        "SELECT sequencia, dt_inicio::text FROM demonstracao_linha WHERE demonstracao = 'DRE' ORDER BY 1"
    ).fetchall() == [(1, "2023-01-01"), (2, "2023-01-01")]
    assert _um(conn, "SELECT count(*) FROM demonstracao_linha_2023")[0] == 7


def test_composicao_e_parecer(conn, carga):
    assert _um(conn, "SELECT acoes_ordinarias, acoes_total, tesouraria_total FROM composicao_capital") == (100, 150, 1)
    assert _um(conn, "SELECT tipo_relatorio, item, texto FROM parecer") == ("Sem Ressalva", 1, "Texto do parecer.")


def test_recarga_incremental_e_forcada(conn, pasta, carga):
    from empresometro.etl.__main__ import executar_carga

    de_novo = executar_carga(conn, pasta, ["dfp"], [2023], usar_local=True, registrar=lambda _: None)
    assert next(e for e in de_novo if e["arquivo"].endswith(".zip"))["situacao"] == "sem mudança"
    assert _um(conn, "SELECT count(*) FROM demonstracao_linha")[0] == 7

    forcada = executar_carga(conn, pasta, ["dfp"], [2023], usar_local=True, forcar=True, registrar=lambda _: None)
    assert next(e for e in forcada if e["arquivo"].endswith(".zip"))["situacao"] == "carregado"
    assert _um(conn, "SELECT count(*) FROM demonstracao_linha")[0] == 7
    assert _um(conn, "SELECT count(*) FROM documento")[0] == 4
    assert _um(conn, "SELECT count(*) FROM companhia")[0] == 4


def test_relatorio(conn, carga):
    from empresometro.etl.relatorio import gerar_relatorio

    texto = gerar_relatorio(conn, carga)
    assert "| demonstracao_linha | 7 |" in texto
    assert "| DRE | 1 | 0 | 0 | 1 |" in texto
    assert "| 1 | 1 | 0 |" in texto


def test_visao_sem_repeticoes(conn, carga):
    assert _um(conn, "SELECT count(*) FROM demonstracao_linha")[0] == 7
    assert _um(conn, "SELECT count(*) FROM demonstracao_linha_unica")[0] == 6
    assert _um(conn, "SELECT count(*), min(sequencia) FROM demonstracao_linha_unica WHERE demonstracao = 'DRE'") == (1, 1)


def test_alertas_de_qualidade(conn, carga):
    from empresometro.etl.qualidade import gerar_alertas, gerar_relatorio_qualidade

    contagem = gerar_alertas(conn, ano_corrente=2026)
    # BETA é ativa e não tem DFP; ÉPSILON está fora do cadastro e seu documento não tem linhas.
    assert contagem == {"SEM_DFP_NA_JANELA": 1, "VIGENTE_SEM_LINHAS": 1, "FORA_DO_CADASTRO": 1}

    # Um passivo total diferente do ativo total passa a gerar alerta.
    conn.execute(
        """
        INSERT INTO demonstracao_linha (ano_referencia, documento_id, demonstracao, escopo, ordem_exercicio,
            dt_fim, cd_conta, ds_conta, valor_original, escala, valor_reais, sequencia)
        SELECT 2023, d.id, 'BPP', 'CON', 'ULTIMO', '2023-12-31', '2', 'Passivo Total', 778, 'UNIDADE', 778, 99
        FROM documento d JOIN companhia c ON c.id = d.companhia_id WHERE c.cnpj = '33333333000133'
        """
    )
    contagem = gerar_alertas(conn, ano_corrente=2026)
    assert contagem["BALANCO_NAO_FECHA"] == 1
    valor, detalhe = _um(conn, "SELECT valor, detalhe FROM alerta_qualidade WHERE tipo = 'BALANCO_NAO_FECHA'")
    assert valor == Decimal("-1.00")
    assert "arredondamento" in detalhe
    texto = gerar_relatorio_qualidade(conn)
    assert "GAMA S.A." in texto and "| BALANCO_NAO_FECHA |" in texto


def test_interpretacao_das_series():
    import datetime as dt

    from empresometro.etl.macro import interpretar_sgs, interpretar_sidra

    assert interpretar_sgs(
        [{"data": "02/01/2024", "valor": "11.75"}, {"data": "x", "valor": "1"}, {"data": "03/01/2024", "valor": ""}]
    ) == [(dt.date(2024, 1, 2), Decimal("11.75"))]

    cabecalho = {"NC": "Nível Territorial (Código)", "V": "Valor", "D2C": "Trimestre (Código)", "D2N": "Trimestre"}
    trimestral = [cabecalho, {"V": "3.5", "D2C": "202402"}, {"V": "...", "D2C": "202403"}]
    assert interpretar_sidra(trimestral, "trimestral") == [(dt.date(2024, 6, 1), Decimal("3.5"))]
    mensal = [{"V": "Valor", "D3C": "Trimestre Móvel (Código)"}, {"V": "7,9", "D3C": "202401"}]
    assert interpretar_sidra(mensal, "mensal") == [(dt.date(2024, 1, 1), Decimal("7.9"))]


def test_gravacao_de_serie_e_relatorio(conn, carga):
    import datetime as dt

    from empresometro.etl.macro import gerar_relatorio_macro, gravar_serie

    pontos = [(dt.date(2024, 1, 1), Decimal("11.75")), (dt.date(2024, 2, 1), Decimal("11.25"))]
    gravar_serie(conn, "BCB SGS", "432", "Taxa Selic", "% a.a.", "diária", pontos)
    gravar_serie(conn, "BCB SGS", "432", "Taxa Selic: meta", "% a.a.", "diária", pontos[1:])
    assert _um(conn, "SELECT count(*) FROM serie_macro")[0] == 1
    assert _um(conn, "SELECT count(*), max(valor) FROM serie_macro_valor") == (1, Decimal("11.25000000"))
    assert "| BCB SGS | 432 | Taxa Selic: meta | % a.a. | diária | 1 | 2024-02-01 | 2024-02-01 | 11.25 |" in gerar_relatorio_macro(conn)
