"""Relatório de conferência dos indicadores."""

from __future__ import annotations

import psycopg

from ..etl.relatorio import _tabela

# Companhias conhecidas usadas para conferir a ordem de grandeza dos resultados.
AMOSTRA = ["PETROBRAS", "VALE S.A.", "ITAÚ UNIBANCO HOLDING", "WEG S.A.", "AMBEV S.A.", "MAGAZINE LUIZA", "BCO BRASIL"]


def gerar_relatorio_indicadores(conn: psycopg.Connection) -> str:
    cur = conn.cursor()

    def consulta(sql: str, parametros=None) -> list:
        return cur.execute(sql, parametros).fetchall()

    partes = ["# Relatório dos indicadores", ""]
    partes += [
        "## Cobertura",
        "",
        _tabela(
            ["Período", "Plano", "Companhias", "Datas", "Valores calculados", "Não se aplica", "Dado ausente", "Denominador inválido"],
            consulta(
                """
                SELECT periodo, plano, count(DISTINCT companhia_id), count(DISTINCT dt_referencia),
                       count(valor), count(*) FILTER (WHERE motivo = 'NAO_SE_APLICA'),
                       count(*) FILTER (WHERE motivo = 'DADO_AUSENTE'),
                       count(*) FILTER (WHERE motivo = 'DENOMINADOR_INVALIDO')
                FROM indicador_valor GROUP BY 1, 2 ORDER BY 1, 2
                """
            ),
        ),
        "",
        "## Base usada",
        "",
        _tabela(
            ["Período", "Escopo", "Companhias"],
            consulta(
                "SELECT periodo, escopo, count(DISTINCT companhia_id) FROM indicador_valor GROUP BY 1, 2 ORDER BY 1, 2"
            ),
        ),
        "",
        "## Indicadores por situação (último exercício anual)",
        "",
        _tabela(
            ["Grupo", "Indicador", "Unidade", "Calculados", "Não se aplica", "Dado ausente", "Denominador inválido", "Mediana"],
            consulta(
                """
                WITH ultimo AS (SELECT max(dt_referencia) d FROM indicador_valor
                                WHERE periodo = 'ANUAL' AND extract(month FROM dt_referencia) = 12)
                SELECT i.grupo, i.nome, i.unidade, count(v.valor),
                       count(*) FILTER (WHERE v.motivo = 'NAO_SE_APLICA'),
                       count(*) FILTER (WHERE v.motivo = 'DADO_AUSENTE'),
                       count(*) FILTER (WHERE v.motivo = 'DENOMINADOR_INVALIDO'),
                       round((percentile_cont(0.5) WITHIN GROUP (ORDER BY v.valor))::numeric, 2)
                FROM indicador i
                JOIN indicador_valor v ON v.codigo = i.codigo AND v.periodo = 'ANUAL'
                JOIN ultimo u ON v.dt_referencia = u.d
                GROUP BY i.ordem, i.grupo, i.nome, i.unidade ORDER BY i.ordem
                """
            ),
        ),
        "",
        "## Medianas por exercício (plano comum)",
        "",
        _tabela(
            ["Exercício", "Companhias", "Margem líquida (%)", "Margem EBITDA (%)", "ROE (%)", "Dívida líquida/EBITDA (x)", "Liquidez corrente (x)"],
            consulta(
                """
                SELECT extract(year FROM dt_referencia)::int, count(DISTINCT companhia_id),
                       round((percentile_cont(0.5) WITHIN GROUP (ORDER BY valor) FILTER (WHERE codigo = 'MARGEM_LIQUIDA'))::numeric, 2),
                       round((percentile_cont(0.5) WITHIN GROUP (ORDER BY valor) FILTER (WHERE codigo = 'MARGEM_EBITDA'))::numeric, 2),
                       round((percentile_cont(0.5) WITHIN GROUP (ORDER BY valor) FILTER (WHERE codigo = 'ROE'))::numeric, 2),
                       round((percentile_cont(0.5) WITHIN GROUP (ORDER BY valor) FILTER (WHERE codigo = 'DIVIDA_LIQUIDA_EBITDA'))::numeric, 2),
                       round((percentile_cont(0.5) WITHIN GROUP (ORDER BY valor) FILTER (WHERE codigo = 'LIQUIDEZ_CORRENTE'))::numeric, 2)
                FROM indicador_valor WHERE periodo = 'ANUAL' AND plano = 'COMUM' GROUP BY 1 ORDER BY 1
                """
            ),
        ),
        "",
        "## Conferência com companhias conhecidas",
        "",
        "Valores em R$ bilhões e percentuais, no último exercício anual e nos últimos 12 meses disponíveis.",
        "",
    ]
    for trecho in AMOSTRA:
        linhas = consulta(
            """
            WITH cia AS (
                SELECT c.id, c.denominacao FROM companhia c
                WHERE c.ativa AND c.denominacao ILIKE %s ORDER BY length(c.denominacao) LIMIT 1),
            datas AS (
                SELECT v.periodo, max(v.dt_referencia) d FROM indicador_valor v JOIN cia ON cia.id = v.companhia_id
                GROUP BY v.periodo)
            SELECT cia.denominacao, v.periodo, v.dt_referencia, max(v.plano), max(v.escopo),
                   round(max(v.valor) FILTER (WHERE v.codigo = 'RECEITA_LIQUIDA') / 1e9, 1),
                   round(max(v.valor) FILTER (WHERE v.codigo = 'EBITDA') / 1e9, 1),
                   round(max(v.valor) FILTER (WHERE v.codigo = 'LUCRO_LIQUIDO') / 1e9, 1),
                   round(max(v.valor) FILTER (WHERE v.codigo = 'PATRIMONIO_LIQUIDO') / 1e9, 1),
                   round(max(v.valor) FILTER (WHERE v.codigo = 'DIVIDA_LIQUIDA') / 1e9, 1),
                   round(max(v.valor) FILTER (WHERE v.codigo = 'ROE'), 1),
                   round(max(v.valor) FILTER (WHERE v.codigo = 'MARGEM_LIQUIDA'), 1),
                   round(max(v.valor) FILTER (WHERE v.codigo = 'CRESCIMENTO_RECEITA'), 1),
                   round(max(v.valor) FILTER (WHERE v.codigo = 'INDICE_EFICIENCIA'), 1)
            FROM indicador_valor v JOIN cia ON cia.id = v.companhia_id
            JOIN datas ON datas.periodo = v.periodo AND datas.d = v.dt_referencia
            GROUP BY cia.denominacao, v.periodo, v.dt_referencia ORDER BY v.periodo
            """,
            (f"%{trecho}%",),
        )
        if linhas:
            partes += [
                _tabela(
                    ["Companhia", "Período", "Data", "Plano", "Escopo", "Receita", "EBITDA", "Lucro", "Patrimônio",
                     "Dívida líquida", "ROE %", "Margem líq. %", "Cresc. receita %", "Eficiência %"],
                    linhas,
                ),
                "",
            ]
    return "\n".join(partes)


def gerar_catalogo_markdown() -> str:
    """Documentação das fórmulas, gerada a partir do catálogo usado no cálculo."""
    from .catalogo import CATALOGO

    partes = [
        "# Catálogo de indicadores",
        "",
        "Fórmulas usadas no cálculo. Os valores vêm das demonstrações padronizadas da CVM, na versão vigente de cada documento,",
        "com o balanço consolidado quando existe e o individual nos demais casos. Em ROE, ROA e ROIC o denominador é a média",
        "entre o saldo do fim do período e o de um ano antes. Cada indicador é calculado para o exercício anual e para os",
        "últimos 12 meses a cada trimestre. Quando não é possível calcular, o banco registra o motivo: não se aplica ao tipo",
        "de companhia, dado ausente ou denominador zero ou negativo.",
        "",
    ]
    grupo = None
    for d in CATALOGO:
        if d.grupo != grupo:
            grupo = d.grupo
            partes += [f"## {grupo}", "", "| Indicador | Código | Unidade | Fórmula | Aplica-se a | Observação |", "|---|---|---|---|---|---|"]
        partes.append(
            f"| {d.nome} | `{d.codigo}` | {d.unidade} | {d.formula} | {', '.join(d.aplica_a).lower()} | {d.observacao or '-'} |"
        )
        proximo = CATALOGO[CATALOGO.index(d) + 1].grupo if d is not CATALOGO[-1] else None
        if proximo != grupo:
            partes.append("")
    return "\n".join(partes)
