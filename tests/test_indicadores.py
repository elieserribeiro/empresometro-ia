"""Testes dos indicadores: funções puras e cálculo completo sobre o banco."""

import datetime as dt
import os
from decimal import Decimal as D
from pathlib import Path

import pytest

from empresometro.indicadores.calculo import (
    DADO_AUSENTE, DENOMINADOR_INVALIDO, NAO_SE_APLICA, cagr, calcular, somar_fluxos,
)
from empresometro.indicadores.carga import calcular_companhia, um_ano_antes
from empresometro.indicadores.catalogo import CATALOGO

RAIZ = Path(__file__).resolve().parents[1]

FLUXO = dict(receita=D(1000), resultado_bruto=D(400), ebit=D(200), despesas_financeiras=D(-40),
             lucro_liquido=D(100), depreciacao=D(-50), fco=D(180), fci=D(-100))
SALDO = dict(ativo_total=D(2000), ativo_circulante=D(800), caixa=D(100), aplicacoes=D(50), estoques=D(200),
             passivo_total=D(2000), passivo_circulante=D(400), passivo_nao_circulante=D(600),
             emprestimos_cp=D(100), emprestimos_lp=D(300), patrimonio_liquido=D(1000))
SALDO_ANTERIOR = dict(ativo_total=D(1800), caixa=D(80), aplicacoes=D(20), emprestimos_cp=D(80),
                      emprestimos_lp=D(220), patrimonio_liquido=D(800))
FLUXO_ANTERIOR = dict(receita=D(800), lucro_liquido=D(50))


def _v(resultado, codigo):
    valor, motivo = resultado[codigo]
    assert motivo is None, f"{codigo}: {motivo}"
    return round(valor, 4)


def test_catalogo_sem_codigos_repetidos():
    codigos = [d.codigo for d in CATALOGO]
    assert len(codigos) == len(set(codigos)) == 42
    assert sum(1 for d in CATALOGO if "COMUM" in d.aplica_a) == 32


def test_indicadores_do_plano_comum():
    r = calcular("COMUM", FLUXO, SALDO, SALDO_ANTERIOR, FLUXO_ANTERIOR)
    esperado = {
        "EBITDA": 250, "CAIXA_E_APLICACOES": 150, "MARGEM_BRUTA": 40, "MARGEM_EBITDA": 25,
        "MARGEM_EBIT": 20, "MARGEM_LIQUIDA": 10, "ROE": D("11.1111"), "ROA": D("5.2632"),
        "ROIC": D("11.7333"), "CRESCIMENTO_RECEITA": 25, "CRESCIMENTO_LUCRO": 100,
        "CRESCIMENTO_PATRIMONIO": 25, "DIVIDA_BRUTA": 400, "DIVIDA_LIQUIDA": 250,
        "DIVIDA_LIQUIDA_EBITDA": 1, "DIVIDA_LIQUIDA_PL": D("0.25"), "COBERTURA_JUROS": 5,
        "ENDIVIDAMENTO_GERAL": 50, "LIQUIDEZ_CORRENTE": 2, "LIQUIDEZ_SECA": D("1.5"),
        "LIQUIDEZ_IMEDIATA": D("0.375"), "CAPITAL_DE_GIRO": 400, "FLUXO_CAIXA_OPERACIONAL": 180,
        "FLUXO_CAIXA_LIVRE": 80, "CONVERSAO_DE_CAIXA": 72,
    }
    for codigo, valor in esperado.items():
        assert _v(r, codigo) == valor, codigo
    assert r["INDICE_EFICIENCIA"] == (None, NAO_SE_APLICA)
    assert "CAGR_RECEITA" not in r


def test_motivos_quando_nao_calcula():
    negativo = {**SALDO, "patrimonio_liquido": D(-500)}
    r = calcular("COMUM", {**FLUXO, "depreciacao": None}, negativo, {"patrimonio_liquido": D(-300)}, {"lucro_liquido": D(-5)})
    assert r["ROE"] == (None, DENOMINADOR_INVALIDO)
    assert r["DIVIDA_LIQUIDA_PL"] == (None, DENOMINADOR_INVALIDO)
    assert r["CRESCIMENTO_LUCRO"] == (None, DENOMINADOR_INVALIDO)
    assert r["EBITDA"] == (None, DADO_AUSENTE)
    assert r["MARGEM_EBITDA"] == (None, DADO_AUSENTE)
    assert r["CRESCIMENTO_RECEITA"] == (None, DADO_AUSENTE)
    prejuizo = calcular("COMUM", {**FLUXO, "ebit": D(-100)}, SALDO, SALDO_ANTERIOR, FLUXO_ANTERIOR)
    assert _v(prejuizo, "EBITDA") == -50
    assert prejuizo["DIVIDA_LIQUIDA_EBITDA"] == (None, DENOMINADOR_INVALIDO)


def test_indicadores_de_banco():
    fluxo = dict(receita=D(5000), resultado_bruto=D(2000), lucro_liquido=D(600),
                 banco_pessoal=D(-500), banco_administrativas=D(-400), banco_servicos=D(1000))
    saldo = dict(ativo_total=D(50000), passivo_total=D(50000), patrimonio_liquido=D(5000))
    r = calcular("BANCO", fluxo, saldo, dict(ativo_total=D(46000), patrimonio_liquido=D(4600)), None)
    assert _v(r, "MARGEM_INTERMEDIACAO") == 40
    assert _v(r, "INDICE_EFICIENCIA") == 30
    assert _v(r, "ALAVANCAGEM") == 10
    assert _v(r, "ROE") == D("12.5")
    assert _v(r, "ENDIVIDAMENTO_GERAL") == 90
    for codigo in ("EBITDA", "DIVIDA_LIQUIDA", "LIQUIDEZ_CORRENTE", "LUCRO_BRUTO"):
        assert r[codigo] == (None, NAO_SE_APLICA)


def test_auxiliares():
    assert somar_fluxos({"receita": D(30)}, {"receita": D(100)}, {"receita": D(20)}) == {"receita": D(110)}
    assert somar_fluxos({"fco": D(1)}, {"fco": None}, {"fco": D(1)}) == {"fco": None}
    assert somar_fluxos({"receita": D(1)}, None, {"receita": D(1)}) is None
    assert cagr(D(100), D(121), 2) == (D("10.0"), None)
    assert cagr(D(-1), D(121), 2) == (None, DENOMINADOR_INVALIDO)
    assert um_ano_antes(dt.date(2024, 2, 29)) == dt.date(2023, 2, 28)


def test_doze_meses_a_partir_do_trimestre():
    d = dt.date
    def fluxo(inicio, receita, lucro, **extra):
        return {"receita": D(receita), "lucro_liquido": D(lucro), "resultado_bruto": None, "ebit": None,
                "despesas_financeiras": None, "depreciacao": None, "fco": None, "fci": None,
                "banco_pessoal": None, "banco_administrativas": None, "banco_servicos": None,
                "_inicio": inicio, "_escopo": "CON", "_documento": 1, **extra}
    registro = {
        "plano": {d(2024, 12, 31): "COMUM", d(2025, 12, 31): "COMUM", d(2026, 3, 31): "COMUM"},
        "saldo": {
            d(2024, 12, 31): {"patrimonio_liquido": D(900), "ativo_total": D(1900)},
            d(2025, 3, 31): {"patrimonio_liquido": D(920), "ativo_total": D(1900)},
            d(2025, 12, 31): {"patrimonio_liquido": D(1000), "ativo_total": D(2000)},
            d(2026, 3, 31): {"patrimonio_liquido": D(1080), "ativo_total": D(2100)},
        },
        "anual": {
            d(2023, 12, 31): fluxo(d(2023, 1, 1), 700, 60, _comparativo=True),
            d(2024, 12, 31): fluxo(d(2024, 1, 1), 800, 80),
            d(2025, 12, 31): fluxo(d(2025, 1, 1), 1000, 100),
        },
        "acumulado": {
            d(2026, 3, 31): {"atual": fluxo(d(2026, 1, 1), 300, 40), "anterior": fluxo(d(2025, 1, 1), 200, 20)},
        },
    }
    linhas = calcular_companhia(registro, ano_corrente=2026)
    valor = {(c, p, data): (v, m) for c, p, data, v, m, *_ in linhas}
    # 12 meses até março de 2026 = 300 + 1000 - 200
    assert valor[("RECEITA_LIQUIDA", "12M", d(2026, 3, 31))] == (D(1100), None)
    assert valor[("LUCRO_LIQUIDO", "12M", d(2026, 3, 31))] == (D(120), None)
    # ROE de 12 meses usa o patrimônio de um ano antes: 120 / ((1080 + 920) / 2)
    assert valor[("ROE", "12M", d(2026, 3, 31))][0] == D(12)
    assert valor[("RECEITA_LIQUIDA", "ANUAL", d(2025, 12, 31))] == (D(1000), None)
    assert valor[("CRESCIMENTO_RECEITA", "ANUAL", d(2025, 12, 31))][0] == D(25)
    assert valor[("CRESCIMENTO_RECEITA", "ANUAL", d(2024, 12, 31))][0].quantize(D("0.0001")) == D("14.2857")
    assert ("RECEITA_LIQUIDA", "ANUAL", d(2023, 12, 31)) not in valor  # só comparativo
    # CAGR entre o primeiro e o último exercício próprios: 800 -> 1000 em um ano
    assert valor[("CAGR_RECEITA", "ANUAL", d(2025, 12, 31))][0] == D(25)
    assert valor[("RECEITA_LIQUIDA", "12M", d(2025, 12, 31))] == (D(1000), None)


@pytest.mark.skipif(not os.environ.get("DATABASE_URL"), reason="DATABASE_URL não definida")
def test_calculo_completo_no_banco():
    from alembic import command
    from alembic.config import Config

    from empresometro.etl.fontes import conectar
    from empresometro.indicadores.carga import calcular_tudo
    from empresometro.indicadores.relatorio import gerar_relatorio_indicadores

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
        linhas = [
            # (demonstração, ordem, início, fim, conta, descrição, valor em milhares)
            ("BPA", "ULTIMO", None, "2025-12-31", "1", "Ativo Total", 2000),
            ("BPA", "ULTIMO", None, "2025-12-31", "1.01", "Ativo Circulante", 800),
            ("BPA", "ULTIMO", None, "2025-12-31", "1.01.01", "Caixa e Equivalentes de Caixa", 100),
            ("BPA", "ULTIMO", None, "2025-12-31", "1.01.02", "Aplicações Financeiras", 50),
            ("BPA", "ULTIMO", None, "2025-12-31", "1.01.04", "Estoques", 200),
            ("BPA", "PENULTIMO", None, "2024-12-31", "1", "Ativo Total", 1800),
            ("BPP", "ULTIMO", None, "2025-12-31", "2", "Passivo Total", 2000),
            ("BPP", "ULTIMO", None, "2025-12-31", "2.01", "Passivo Circulante", 400),
            ("BPP", "ULTIMO", None, "2025-12-31", "2.01.04", "Empréstimos e Financiamentos", 100),
            ("BPP", "ULTIMO", None, "2025-12-31", "2.02", "Passivo Não Circulante", 600),
            ("BPP", "ULTIMO", None, "2025-12-31", "2.02.01", "Empréstimos e Financiamentos", 300),
            ("BPP", "ULTIMO", None, "2025-12-31", "2.03", "Patrimônio Líquido Consolidado", 1000),
            ("BPP", "PENULTIMO", None, "2024-12-31", "2.03", "Patrimônio Líquido Consolidado", 800),
            ("DRE", "ULTIMO", "2025-01-01", "2025-12-31", "3.01", "Receita de Venda de Bens e/ou Serviços", 1000),
            ("DRE", "ULTIMO", "2025-01-01", "2025-12-31", "3.01", "Receita de Venda de Bens e/ou Serviços", 1000),
            ("DRE", "ULTIMO", "2025-01-01", "2025-12-31", "3.03", "Resultado Bruto", 400),
            ("DRE", "ULTIMO", "2025-01-01", "2025-12-31", "3.05", "Resultado Antes do Resultado Financeiro e dos Tributos", 200),
            ("DRE", "ULTIMO", "2025-01-01", "2025-12-31", "3.06.02", "Despesas Financeiras", -40),
            ("DRE", "ULTIMO", "2025-01-01", "2025-12-31", "3.09", "Resultado Líquido das Operações Continuadas", 999),
            ("DRE", "ULTIMO", "2025-01-01", "2025-12-31", "3.11", "Lucro/Prejuízo Consolidado do Período", 100),
            ("DRE", "PENULTIMO", "2024-01-01", "2024-12-31", "3.01", "Receita de Venda de Bens e/ou Serviços", 800),
            ("DRE", "PENULTIMO", "2024-01-01", "2024-12-31", "3.11", "Lucro/Prejuízo Consolidado do Período", 50),
            ("DVA", "ULTIMO", "2025-01-01", "2025-12-31", "7.04.01", "Depreciação, Amortização e Exaustão", -50),
            ("DFC_MI", "ULTIMO", "2025-01-01", "2025-12-31", "6.01", "Caixa Líquido Atividades Operacionais", 180),
            ("DFC_MI", "ULTIMO", "2025-01-01", "2025-12-31", "6.02", "Caixa Líquido Atividades de Investimento", -100),
        ]
        for seq, (dem, ordem, inicio, fim, conta, descricao, valor) in enumerate(linhas, start=1):
            conn.execute(
                "INSERT INTO demonstracao_linha (ano_referencia, documento_id, demonstracao, escopo, ordem_exercicio, "
                "dt_inicio, dt_fim, cd_conta, ds_conta, valor_original, escala, valor_reais, sequencia) "
                "VALUES (2025, %s, %s, 'CON', %s, %s, %s, %s, %s, %s, 'MIL', %s, %s)",
                (doc, dem, ordem, inicio, fim, conta, descricao, valor, valor * 1000, seq),
            )
        resumo = calcular_tudo(conn, ano_corrente=2026, registrar=lambda _: None)
        assert resumo["companhias"] == 1

        def valor(codigo, periodo="ANUAL"):
            return conn.execute(
                "SELECT valor, motivo, escopo, plano FROM indicador_valor WHERE codigo = %s AND periodo = %s",
                (codigo, periodo),
            ).fetchone()

        assert valor("RECEITA_LIQUIDA") == (D("1000000.000000"), None, "CON", "COMUM")
        assert valor("LUCRO_LIQUIDO")[0] == D(100000)
        assert valor("EBITDA")[0] == D(250000)
        assert valor("ROE")[0] == D("11.111111")
        assert valor("DIVIDA_LIQUIDA_EBITDA")[0] == D(1)
        assert valor("CRESCIMENTO_RECEITA")[0] == D(25)
        assert valor("FLUXO_CAIXA_LIVRE")[0] == D(80000)
        assert valor("INDICE_EFICIENCIA")[:2] == (None, "NAO_SE_APLICA")
        assert valor("ROIC")[:2] == (None, "DADO_AUSENTE")  # falta o capital investido do ano anterior
        assert valor("CAGR_RECEITA")[:2] == (None, "DADO_AUSENTE")  # só um exercício próprio
        assert valor("RECEITA_LIQUIDA", "12M")[0] == D(1000000)
        assert conn.execute("SELECT count(*) FROM indicador").fetchone()[0] == 42
        assert "| ANUAL | COMUM | 1 |" in gerar_relatorio_indicadores(conn)
    finally:
        conn.close()
        command.downgrade(cfg, "base")


def test_ifdata_datas_e_correspondencia():
    from empresometro.etl.ifdata import corresponder, datas_base, fim_do_mes

    assert datas_base(2025, dt.date(2025, 10, 15)) == [202412, 202503, 202506, 202509]
    assert fim_do_mes(202402) == dt.date(2024, 2, 29)
    cadastro = [
        {"CodInst": "60872504", "NomeInstituicao": "ITAU UNIBANCO HOLDING", "CodConglomeradoPrudencial": "C0080099",
         "CnpjInstituicaoLider": "60872504", "Situacao": "A"},
        {"CodInst": "17192451", "NomeInstituicao": "BANCO ITAUCARD", "CodConglomeradoPrudencial": "C0080099",
         "CnpjInstituicaoLider": "60872504", "Situacao": "A"},
        {"CodInst": "11111111", "NomeInstituicao": "BANCO SOZINHO", "CodConglomeradoPrudencial": None,
         "CnpjInstituicaoLider": None, "Situacao": "A"},
        {"CodInst": "22222222", "NomeInstituicao": "BANCO INATIVO", "CodConglomeradoPrudencial": None,
         "CnpjInstituicaoLider": None, "Situacao": "I"},
    ]
    companhias = [(1, "60872504000123"), (2, "17192451000170"), (3, "11111111000111"), (4, "22222222000122"), (5, "99999999000199")]
    pares = {p["companhia_id"]: (p["cod_inst"], p["criterio"]) for p in corresponder(companhias, cadastro)}
    assert pares == {
        1: ("C0080099", "LIDER_DO_CONGLOMERADO"),
        2: ("C0080099", "INSTITUICAO_DO_CONGLOMERADO"),
        3: ("11111111", "INSTITUICAO_INDEPENDENTE"),
    }


def test_indicadores_do_ifdata_nao_saem_do_calculo_da_cvm():
    banco = calcular("BANCO", {"lucro_liquido": D(1)}, {}, {}, None)
    assert "INDICE_BASILEIA" not in banco
    assert calcular("COMUM", FLUXO, SALDO, SALDO_ANTERIOR, FLUXO_ANTERIOR)["INDICE_BASILEIA"] == (None, NAO_SE_APLICA)


@pytest.mark.skipif(not os.environ.get("DATABASE_URL"), reason="DATABASE_URL não definida")
def test_indicadores_regulatorios_no_banco():
    from alembic import command
    from alembic.config import Config

    from empresometro.etl.fontes import conectar
    from empresometro.etl.ifdata import gerar_relatorio_ifdata
    from empresometro.indicadores.carga import gravar_catalogo, gravar_indicadores_ifdata

    cfg = Config(str(RAIZ / "alembic.ini"))
    cfg.set_main_option("script_location", str(RAIZ / "migrations"))
    command.downgrade(cfg, "base")
    command.upgrade(cfg, "head")
    conn = conectar()
    conn.autocommit = True
    try:
        gravar_catalogo(conn)
        ids = [
            conn.execute(
                "INSERT INTO companhia (cnpj, denominacao, ativa) VALUES (%s, %s, true) RETURNING id", (cnpj, nome)
            ).fetchone()[0]
            for cnpj, nome in (("60872504000123", "BANCO COM DADOS"), ("11111111000111", "BANCO SEM DADOS"))
        ]
        conn.execute(
            "INSERT INTO companhia_ifdata (companhia_id, cod_inst, nome_ifdata, criterio) "
            "VALUES (%s, 'C0080099', 'ITAU', 'LIDER_DO_CONGLOMERADO')", (ids[0],)
        )
        valores = [
            ("2024-12-31", "5", "79664", "0.165"), ("2025-06-30", "5", "79664", "0.1653"),
            ("2025-06-30", "5", "79659", "0.1312"), ("2025-06-30", "16", "148834", "24.5"),
            ("2025-06-30", "16", "148833", "40"), ("2025-06-30", "16", "24454", "1000"),
        ]
        for data, relatorio, conta, saldo in valores:
            conn.execute(
                "INSERT INTO ifdata_valor (cod_inst, data_base, conta, relatorio, saldo) VALUES ('C0080099', %s, %s, %s, %s)",
                (data, conta, relatorio, saldo),
            )
        # O banco sem correspondência tem os demais indicadores e deve receber "dado ausente".
        conn.execute(
            "INSERT INTO indicador_valor (companhia_id, codigo, periodo, dt_referencia, valor, escopo, plano) "
            "VALUES (%s, 'LUCRO_LIQUIDO', '12M', '2025-06-30', 10, 'CON', 'BANCO')", (ids[1],)
        )
        gravar_indicadores_ifdata(conn, ano_corrente=2026)

        def valor(companhia, codigo, periodo, data):
            return conn.execute(
                "SELECT valor, motivo FROM indicador_valor WHERE companhia_id = %s AND codigo = %s AND periodo = %s "
                "AND dt_referencia = %s", (companhia, codigo, periodo, data),
            ).fetchone()

        assert valor(ids[0], "INDICE_BASILEIA", "12M", "2025-06-30") == (D("16.530000"), None)
        assert valor(ids[0], "INDICE_BASILEIA", "ANUAL", "2024-12-31") == (D("16.500000"), None)
        assert valor(ids[0], "INDICE_BASILEIA", "ANUAL", "2025-06-30") is None  # anual só em dezembro
        assert valor(ids[0], "INADIMPLENCIA", "12M", "2025-06-30") == (D("2.450000"), None)
        assert valor(ids[0], "ATIVOS_PROBLEMATICOS", "12M", "2025-06-30") == (D("4.000000"), None)
        assert valor(ids[0], "INADIMPLENCIA", "12M", "2024-12-31") is None  # relatório ainda não existia
        assert valor(ids[1], "INDICE_BASILEIA", "12M", "2025-06-30") == (None, "DADO_AUSENTE")
        assert "| BANCO COM DADOS | ITAU | C0080099 | LIDER_DO_CONGLOMERADO | 16.53 | 13.12 | 2.45 | 4.00 |" in gerar_relatorio_ifdata(conn)
    finally:
        conn.close()
        command.downgrade(cfg, "base")
