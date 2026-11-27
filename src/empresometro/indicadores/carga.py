"""Monta as bases padronizadas no banco e grava os indicadores por companhia e período."""

from __future__ import annotations

import datetime as dt
from collections import defaultdict
from decimal import Decimal

import psycopg

from .calculo import DADO_AUSENTE, cagr, calcular, somar_fluxos
from .catalogo import CATALOGO, CODIGOS_IFDATA

CONTAS_SALDO = ["1", "1.01", "1.01.01", "1.01.02", "1.01.04", "2", "2.01.04", "2.02.01"] + [
    f"2.{n:02d}" for n in range(1, 10)
]
CONTAS_FLUXO = (
    [f"3.{n:02d}" for n in range(1, 15)]
    + [f"3.04.{n:02d}" for n in range(1, 10)]
    + ["3.06.02", "6.01", "6.02", "7.04.01"]
)
CAMPOS_SALDO = (
    "ativo_total", "ativo_circulante", "caixa", "aplicacoes", "estoques", "passivo_total",
    "passivo_circulante", "passivo_nao_circulante", "emprestimos_cp", "emprestimos_lp",
    "patrimonio_liquido",
)
CAMPOS_FLUXO = (
    "receita", "resultado_bruto", "ebit", "despesas_financeiras", "lucro_liquido", "depreciacao",
    "fco", "fci", "banco_pessoal", "banco_administrativas", "banco_servicos",
)

SQL_BASE_SALDO = """
INSERT INTO base_saldo
SELECT l.documento_id, l.escopo, l.ordem_exercicio, l.dt_fim,
    max(l.valor_reais) FILTER (WHERE l.demonstracao = 'BPA' AND l.cd_conta = '1'),
    max(l.valor_reais) FILTER (WHERE l.demonstracao = 'BPA' AND l.cd_conta = '1.01' AND l.ds_conta = 'Ativo Circulante'),
    max(l.valor_reais) FILTER (WHERE l.demonstracao = 'BPA' AND l.cd_conta IN ('1.01', '1.01.01') AND l.ds_conta = 'Caixa e Equivalentes de Caixa'),
    max(l.valor_reais) FILTER (WHERE l.demonstracao = 'BPA' AND l.cd_conta = '1.01.02' AND l.ds_conta = 'Aplicações Financeiras'),
    max(l.valor_reais) FILTER (WHERE l.demonstracao = 'BPA' AND l.cd_conta = '1.01.04' AND l.ds_conta = 'Estoques'),
    max(l.valor_reais) FILTER (WHERE l.demonstracao = 'BPP' AND l.cd_conta = '2'),
    max(l.valor_reais) FILTER (WHERE l.demonstracao = 'BPP' AND l.cd_conta = '2.01' AND l.ds_conta = 'Passivo Circulante'),
    max(l.valor_reais) FILTER (WHERE l.demonstracao = 'BPP' AND l.cd_conta = '2.02' AND l.ds_conta = 'Passivo Não Circulante'),
    max(l.valor_reais) FILTER (WHERE l.demonstracao = 'BPP' AND l.cd_conta = '2.01.04' AND l.ds_conta = 'Empréstimos e Financiamentos'),
    max(l.valor_reais) FILTER (WHERE l.demonstracao = 'BPP' AND l.cd_conta = '2.02.01' AND l.ds_conta = 'Empréstimos e Financiamentos'),
    max(l.valor_reais) FILTER (WHERE l.demonstracao = 'BPP' AND l.cd_conta ~ '^2\\.\\d\\d$' AND l.ds_conta LIKE 'Patrimônio Líquido%%')
FROM demonstracao_linha_unica l
JOIN documento d ON d.id = l.documento_id AND d.vigente
WHERE l.demonstracao IN ('BPA', 'BPP') AND l.cd_conta = ANY(%s)
GROUP BY 1, 2, 3, 4
"""

SQL_BASE_FLUXO = """
INSERT INTO base_fluxo
SELECT l.documento_id, l.escopo, l.ordem_exercicio, l.dt_inicio, l.dt_fim,
    max(CASE WHEN l.demonstracao = 'DRE' AND l.cd_conta = '3.01' THEN
        CASE WHEN l.ds_conta ILIKE '%%Venda de Bens%%' THEN 'COMUM'
             WHEN l.ds_conta ILIKE '%%Intermediação Financeira%%' THEN 'BANCO'
             WHEN l.ds_conta ILIKE '%%Segurador%%' THEN 'SEGURADORA'
             ELSE 'OUTRO' END END),
    max(l.valor_reais) FILTER (WHERE l.demonstracao = 'DRE' AND l.cd_conta = '3.01'),
    max(l.valor_reais) FILTER (WHERE l.demonstracao = 'DRE' AND l.cd_conta = '3.03'),
    max(l.valor_reais) FILTER (WHERE l.demonstracao = 'DRE' AND l.cd_conta ~ '^3\\.\\d\\d$'
        AND l.ds_conta = 'Resultado Antes do Resultado Financeiro e dos Tributos'),
    max(l.valor_reais) FILTER (WHERE l.demonstracao = 'DRE' AND l.cd_conta = '3.06.02' AND l.ds_conta = 'Despesas Financeiras'),
    max(l.valor_reais) FILTER (WHERE l.demonstracao = 'DRE' AND l.cd_conta ~ '^3\\.\\d\\d$'
        AND l.ds_conta ~ '^Lucro(/| ou )Prejuízo.* do Período$'),
    max(l.valor_reais) FILTER (WHERE l.demonstracao = 'DVA' AND l.cd_conta = '7.04.01' AND l.ds_conta ILIKE 'Deprecia%%'),
    max(l.valor_reais) FILTER (WHERE l.demonstracao IN ('DFC_MI', 'DFC_MD') AND l.cd_conta = '6.01'),
    max(l.valor_reais) FILTER (WHERE l.demonstracao IN ('DFC_MI', 'DFC_MD') AND l.cd_conta = '6.02'),
    max(l.valor_reais) FILTER (WHERE l.demonstracao = 'DRE' AND l.cd_conta ~ '^3\\.04\\.\\d\\d$' AND l.ds_conta ~* '^Despesas? (com|de) Pessoal'),
    max(l.valor_reais) FILTER (WHERE l.demonstracao = 'DRE' AND l.cd_conta ~ '^3\\.04\\.\\d\\d$' AND l.ds_conta ~* '^Outras Despesas (de )?Administrativas'),
    max(l.valor_reais) FILTER (WHERE l.demonstracao = 'DRE' AND l.cd_conta ~ '^3\\.04\\.\\d\\d$' AND l.ds_conta ~* '^Receitas de Prestação de Serviços')
FROM demonstracao_linha_unica l
JOIN documento d ON d.id = l.documento_id AND d.vigente
WHERE l.demonstracao IN ('DRE', 'DVA', 'DFC_MI', 'DFC_MD') AND l.cd_conta = ANY(%s)
  AND l.dt_inicio IS NOT NULL
GROUP BY 1, 2, 3, 4, 5
"""


def montar_bases(conn: psycopg.Connection) -> dict:
    """Recria as tabelas base_saldo e base_fluxo a partir das demonstrações vigentes."""
    with conn.transaction(), conn.cursor() as cur:
        cur.execute("TRUNCATE base_saldo, base_fluxo")
        cur.execute(SQL_BASE_SALDO, (CONTAS_SALDO,))
        saldos = cur.rowcount
        cur.execute(SQL_BASE_FLUXO, (CONTAS_FLUXO,))
        fluxos = cur.rowcount
    return {"base_saldo": saldos, "base_fluxo": fluxos}


def um_ano_antes(data: dt.date) -> dt.date:
    try:
        return data.replace(year=data.year - 1)
    except ValueError:  # 29 de fevereiro
        return data.replace(year=data.year - 1, day=28)


def _escolher_escopo(disponiveis: dict[str, dict]) -> str | None:
    """Consolidado quando tem conteúdo; senão, individual."""
    for escopo in ("CON", "IND"):
        dados = disponiveis.get(escopo)
        if dados and any(v is not None for v in dados.values()):
            return escopo
    return None


def carregar_do_banco(conn: psycopg.Connection) -> dict[int, dict]:
    """Lê as bases e organiza por companhia.

    Devolve, por companhia: saldos por data, fluxos anuais por data de fim,
    acumulados do ano (atual e anterior) por data do ITR e o plano de contas.
    """
    cur = conn.cursor()
    companhias: dict[int, dict] = defaultdict(
        lambda: {"saldo": {}, "anual": {}, "acumulado": {}, "plano": {}, "documentos": {}}
    )

    # Saldos: o documento do próprio período tem prioridade sobre o comparativo de outro documento.
    brutos: dict = defaultdict(dict)
    for linha in cur.execute(
        f"""
        SELECT d.companhia_id, d.id, d.tipo, d.dt_referencia, s.escopo, s.ordem_exercicio, s.dt_fim,
               {', '.join('s.' + c for c in CAMPOS_SALDO)}
        FROM base_saldo s JOIN documento d ON d.id = s.documento_id
        """
    ):
        cia, doc, tipo, ref, escopo, ordem, fim = linha[:7]
        brutos[(cia, doc, tipo, ref, ordem, fim)][escopo] = dict(zip(CAMPOS_SALDO, linha[7:]))
    prioridade: dict = {}
    for (cia, doc, tipo, ref, ordem, fim), por_escopo in brutos.items():
        escopo = _escolher_escopo(por_escopo)
        if escopo is None:
            continue
        # 0 = saldo do próprio documento; 1 = comparativo trazido por outro documento.
        nivel = 0 if (ordem == "ULTIMO" and fim == ref) else 1
        chave = (cia, fim)
        if chave not in prioridade or nivel < prioridade[chave]:
            prioridade[chave] = nivel
            companhias[cia]["saldo"][fim] = {**por_escopo[escopo], "_escopo": escopo, "_documento": doc}

    fluxos: dict = defaultdict(dict)
    planos: dict = {}
    for linha in cur.execute(
        f"""
        SELECT d.companhia_id, d.id, d.tipo, d.dt_referencia, f.escopo, f.ordem_exercicio,
               f.dt_inicio, f.dt_fim, f.plano, {', '.join('f.' + c for c in CAMPOS_FLUXO)}
        FROM base_fluxo f JOIN documento d ON d.id = f.documento_id
        """
    ):
        cia, doc, tipo, ref, escopo, ordem, inicio, fim, plano = linha[:9]
        fluxos[(cia, doc, tipo, ref, ordem, inicio, fim)][escopo] = dict(zip(CAMPOS_FLUXO, linha[9:]))
        if plano:
            planos[(cia, doc, escopo)] = plano

    # Em cada documento e ordem, o período mais longo (início mais antigo) é o acumulado.
    mais_longo: dict = {}
    for (cia, doc, tipo, ref, ordem, inicio, fim), por_escopo in fluxos.items():
        chave = (cia, doc, tipo, ref, ordem, fim)
        if chave not in mais_longo or inicio < mais_longo[chave][0]:
            mais_longo[chave] = (inicio, por_escopo)

    for (cia, doc, tipo, ref, ordem, fim), (inicio, por_escopo) in mais_longo.items():
        escopo = _escolher_escopo(por_escopo)
        if escopo is None:
            continue
        dados = {**por_escopo[escopo], "_inicio": inicio, "_escopo": escopo, "_documento": doc}
        registro = companhias[cia]
        plano = planos.get((cia, doc, escopo))
        if tipo == "DFP":
            # Exercício completo; o comparativo (PENULTIMO) só entra se não houver o documento próprio.
            if ordem == "ULTIMO" and fim == ref:
                registro["anual"][fim] = dados
                if plano:
                    registro["plano"][fim] = plano
            elif fim not in registro["anual"] or registro["anual"][fim].get("_comparativo"):
                registro["anual"].setdefault(fim, {**dados, "_comparativo": True})
        elif tipo == "ITR":
            if ordem == "ULTIMO" and fim == ref:
                registro["acumulado"].setdefault(ref, {})["atual"] = dados
                if plano:
                    registro["plano"][ref] = plano
            elif ordem == "PENULTIMO":
                registro["acumulado"].setdefault(ref, {})["anterior"] = dados
    return companhias


def _plano_em(registro: dict, data: dt.date) -> str | None:
    if data in registro["plano"]:
        return registro["plano"][data]
    anteriores = [d for d in registro["plano"] if d <= data]
    if anteriores:
        return registro["plano"][max(anteriores)]
    return next(iter(registro["plano"].values()), None)


def calcular_companhia(registro: dict, ano_corrente: int) -> list[tuple]:
    """Devolve as linhas (codigo, periodo, data, valor, motivo, escopo, plano, documento)."""
    linhas: list[tuple] = []
    saldo, anual = registro["saldo"], registro["anual"]

    # Fluxos de 12 meses por data: fim de exercício (do DFP) e trimestres (do ITR).
    doze_meses: dict[dt.date, dict] = {}
    for fim, dados in anual.items():
        if not dados.get("_comparativo"):
            doze_meses[fim] = dados
    for ref, partes in registro["acumulado"].items():
        atual, anterior = partes.get("atual"), partes.get("anterior")
        if atual is None or ref in doze_meses:
            continue
        fim_exercicio_anterior = atual["_inicio"] - dt.timedelta(days=1)
        exercicio = anual.get(fim_exercicio_anterior)
        if anterior is None or exercicio is None:
            continue
        # O acumulado anterior precisa cobrir o mesmo intervalo, um ano antes.
        if anterior["_inicio"] != um_ano_antes(atual["_inicio"]):
            continue
        numeros = somar_fluxos(
            {c: atual.get(c) for c in CAMPOS_FLUXO},
            {c: exercicio.get(c) for c in CAMPOS_FLUXO},
            {c: anterior.get(c) for c in CAMPOS_FLUXO},
        )
        doze_meses[ref] = {**numeros, "_escopo": atual["_escopo"], "_documento": atual["_documento"]}

    def emitir(periodo: str, data: dt.date, fluxo: dict, fluxo_anterior: dict | None) -> None:
        plano = _plano_em(registro, data)
        if plano is None or plano == "OUTRO":
            return
        resultados = calcular(plano, fluxo, saldo.get(data), saldo.get(um_ano_antes(data)), fluxo_anterior)
        for codigo, (valor, motivo) in resultados.items():
            linhas.append(
                (codigo, periodo, data, valor, motivo, fluxo.get("_escopo", "IND"), plano, fluxo.get("_documento"))
            )

    exercicios = sorted(d for d, f in anual.items() if not f.get("_comparativo") and d.year < ano_corrente)
    for fim in exercicios:
        fluxo = anual[fim]
        anterior = anual.get(fluxo["_inicio"] - dt.timedelta(days=1))
        emitir("ANUAL", fim, fluxo, anterior)

    for data in sorted(doze_meses):
        antes = um_ano_antes(data)
        emitir("12M", data, doze_meses[data], doze_meses.get(antes) or anual.get(antes))

    # CAGR da receita entre o primeiro e o último exercício com receita informada.
    com_receita = [d for d in exercicios if anual[d].get("receita") is not None]
    if exercicios:
        ultimo = exercicios[-1]
        plano = _plano_em(registro, ultimo)
        if plano and plano != "OUTRO":
            if len(com_receita) >= 2 and com_receita[-1] == ultimo:
                primeiro = com_receita[0]
                valor, motivo = cagr(
                    anual[primeiro]["receita"], anual[ultimo]["receita"], ultimo.year - primeiro.year
                )
            else:
                valor, motivo = None, DADO_AUSENTE
            linhas.append(
                ("CAGR_RECEITA", "ANUAL", ultimo, valor, motivo, anual[ultimo]["_escopo"], plano, anual[ultimo]["_documento"])
            )
    return linhas


def gravar_catalogo(conn: psycopg.Connection) -> None:
    with conn.cursor() as cur:
        for ordem, d in enumerate(CATALOGO, start=1):
            cur.execute(
                """
                INSERT INTO indicador (codigo, nome, grupo, unidade, formula, aplica_a, observacao, ordem)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (codigo) DO UPDATE SET nome = EXCLUDED.nome, grupo = EXCLUDED.grupo,
                    unidade = EXCLUDED.unidade, formula = EXCLUDED.formula, aplica_a = EXCLUDED.aplica_a,
                    observacao = EXCLUDED.observacao, ordem = EXCLUDED.ordem
                """,
                (d.codigo, d.nome, d.grupo, d.unidade, d.formula, ", ".join(d.aplica_a), d.observacao, ordem),
            )


SQL_INDICADORES_IFDATA = """
INSERT INTO indicador_valor (companhia_id, codigo, periodo, dt_referencia, valor, motivo, escopo, plano, documento_id)
SELECT m.companhia_id, x.codigo, p.periodo, v.data_base, round(x.valor, 6), NULL, 'CON', 'BANCO', NULL
FROM companhia_ifdata m
JOIN (
    SELECT cod_inst, data_base,
           max(saldo) FILTER (WHERE conta = '79664') basileia,
           max(saldo) FILTER (WHERE conta = '79659') principal,
           max(saldo) FILTER (WHERE conta = '79660') nivel1,
           max(saldo) FILTER (WHERE conta = '79661') alavancagem,
           max(saldo) FILTER (WHERE conta = '148834') inadimplencia,
           max(saldo) FILTER (WHERE conta = '148833') problematicos,
           max(saldo) FILTER (WHERE conta = '24454') carteira
    FROM ifdata_valor GROUP BY 1, 2
) v ON v.cod_inst = m.cod_inst
CROSS JOIN LATERAL (VALUES
    ('INDICE_BASILEIA', v.basileia * 100),
    ('INDICE_CAPITAL_PRINCIPAL', v.principal * 100),
    ('INDICE_CAPITAL_NIVEL_I', v.nivel1 * 100),
    ('RAZAO_ALAVANCAGEM', v.alavancagem * 100),
    ('INADIMPLENCIA', v.inadimplencia / nullif(v.carteira, 0) * 100),
    ('ATIVOS_PROBLEMATICOS', v.problematicos / nullif(v.carteira, 0) * 100)
) x(codigo, valor)
CROSS JOIN LATERAL (VALUES ('12M'), ('ANUAL')) p(periodo)
WHERE x.valor IS NOT NULL
  AND (p.periodo = '12M' OR (extract(month FROM v.data_base) = 12 AND extract(year FROM v.data_base) < %(ano)s))
ON CONFLICT (companhia_id, codigo, periodo, dt_referencia)
DO UPDATE SET valor = EXCLUDED.valor, motivo = NULL
"""

# Bancos sem valor no IF.data ficam com o motivo registrado, nas mesmas datas dos demais indicadores.
SQL_IFDATA_AUSENTE = """
INSERT INTO indicador_valor (companhia_id, codigo, periodo, dt_referencia, valor, motivo, escopo, plano, documento_id)
SELECT v.companhia_id, i.codigo, v.periodo, v.dt_referencia, NULL, 'DADO_AUSENTE', v.escopo, v.plano, NULL
FROM indicador_valor v JOIN indicador i ON i.codigo = ANY(%(codigos)s)
WHERE v.codigo = 'LUCRO_LIQUIDO' AND v.plano = 'BANCO'
ON CONFLICT (companhia_id, codigo, periodo, dt_referencia) DO NOTHING
"""


def gravar_indicadores_ifdata(conn: psycopg.Connection, ano_corrente: int) -> int:
    """Grava os índices regulatórios dos bancos a partir das tabelas do IF.data."""
    with conn.cursor() as cur:
        cur.execute(SQL_INDICADORES_IFDATA, {"ano": ano_corrente})
        gravados = cur.rowcount
        cur.execute(SQL_IFDATA_AUSENTE, {"codigos": CODIGOS_IFDATA})
    return gravados


def calcular_tudo(conn: psycopg.Connection, ano_corrente: int | None = None, registrar=print) -> dict:
    """Recalcula todos os indicadores de todas as companhias."""
    ano_corrente = ano_corrente or dt.date.today().year
    registrar("Montando as bases padronizadas...")
    resumo = montar_bases(conn)
    registrar("Calculando os indicadores...")
    companhias = carregar_do_banco(conn)
    total = 0
    with conn.transaction(), conn.cursor() as cur:
        gravar_catalogo(conn)
        cur.execute("TRUNCATE indicador_valor")
        with cur.copy(
            "COPY indicador_valor (companhia_id, codigo, periodo, dt_referencia, valor, motivo, "
            "escopo, plano, documento_id) FROM STDIN"
        ) as copia:
            for companhia_id, registro in companhias.items():
                for codigo, periodo, data, valor, motivo, escopo, plano, documento in calcular_companhia(
                    registro, ano_corrente
                ):
                    if valor is not None:
                        valor = valor.quantize(Decimal("0.000001"))
                    copia.write_row((companhia_id, codigo, periodo, data, valor, motivo, escopo, plano, documento))
                    total += 1
        regulatorios = gravar_indicadores_ifdata(conn, ano_corrente)
    resumo.update(companhias=len(companhias), valores=total, valores_ifdata=regulatorios)
    registrar(f"Indicadores: {resumo}")
    return resumo
