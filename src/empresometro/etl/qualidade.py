"""Validações de qualidade: gera alertas no banco e um relatório em Markdown."""

from __future__ import annotations

import datetime as dt

import psycopg

from .relatorio import _tabela

DESCRICAO = {
    "BALANCO_NAO_FECHA": "Ativo total diferente do passivo total no documento vigente",
    "CONTA_REPETIDA_COM_VALORES_DIFERENTES": "Mesma conta repetida no documento com valores diferentes",
    "HISTORICO_INCOMPLETO": "Companhia ativa sem demonstração anual em parte dos exercícios",
    "SEM_DFP_NA_JANELA": "Companhia ativa sem nenhuma demonstração anual na janela",
    "VIGENTE_SEM_LINHAS": "Documento vigente sem linhas de demonstração",
    "FORA_DO_CADASTRO": "Companhia presente nos documentos e ausente do cadastro da CVM",
}


def gerar_alertas(conn: psycopg.Connection, ano_corrente: int | None = None) -> dict[str, int]:
    """Recria todos os alertas de qualidade e devolve a contagem por tipo."""
    ano_corrente = ano_corrente or dt.date.today().year
    with conn.transaction(), conn.cursor() as cur:
        cur.execute("TRUNCATE alerta_qualidade RESTART IDENTITY")

        # 1. Balanços vigentes em que ativo total e passivo total não coincidem.
        cur.execute(
            """
            WITH ativo AS (
                SELECT documento_id, escopo, max(valor_reais) v, count(DISTINCT valor_reais) n
                FROM demonstracao_linha
                WHERE demonstracao = 'BPA' AND cd_conta = '1' AND ordem_exercicio = 'ULTIMO'
                GROUP BY 1, 2),
            passivo AS (
                SELECT documento_id, escopo, max(valor_reais) v, count(DISTINCT valor_reais) n
                FROM demonstracao_linha
                WHERE demonstracao = 'BPP' AND cd_conta = '2' AND ordem_exercicio = 'ULTIMO'
                GROUP BY 1, 2)
            INSERT INTO alerta_qualidade (tipo, companhia_id, documento_id, detalhe, valor)
            SELECT 'BALANCO_NAO_FECHA', d.companhia_id, d.id,
                   format('%s: ativo total R$ %s, passivo total R$ %s. %s',
                          CASE a.escopo WHEN 'CON' THEN 'Consolidado' ELSE 'Individual' END,
                          to_char(a.v, 'FM999G999G999G999G999G990D00'),
                          to_char(p.v, 'FM999G999G999G999G999G990D00'),
                          CASE WHEN a.n > 1 OR p.n > 1 THEN 'Causa provável: a conta de total aparece repetida com valores diferentes no arquivo da CVM.'
                               WHEN abs(a.v - p.v) <= 1000 THEN 'Causa provável: arredondamento (diferença de até mil reais).'
                               ELSE 'Diferença relevante, sem causa identificada automaticamente.' END),
                   a.v - p.v
            FROM ativo a
            JOIN passivo p USING (documento_id, escopo)
            JOIN documento d ON d.id = a.documento_id AND d.vigente
            WHERE a.v IS DISTINCT FROM p.v
            """
        )

        # 2. Contas repetidas com valores diferentes, por documento.
        cur.execute(
            """
            INSERT INTO alerta_qualidade (tipo, companhia_id, documento_id, detalhe, valor)
            SELECT 'CONTA_REPETIDA_COM_VALORES_DIFERENTES', d.companhia_id, d.id,
                   format('%s conta(s) repetida(s) com valores diferentes', count(*)), count(*)
            FROM (
                SELECT documento_id FROM demonstracao_linha
                GROUP BY ano_referencia, documento_id, demonstracao, escopo, ordem_exercicio,
                         dt_inicio, dt_fim, coluna_df, cd_conta
                HAVING count(DISTINCT valor_original) > 1
            ) g JOIN documento d ON d.id = g.documento_id
            GROUP BY d.companhia_id, d.id
            """
        )

        # 3. Histórico de demonstrações anuais das companhias ativas.
        anos = [
            linha[0]
            for linha in cur.execute(
                "SELECT DISTINCT extract(year FROM dt_referencia)::int FROM documento "
                "WHERE tipo = 'DFP' AND extract(year FROM dt_referencia) < %s ORDER BY 1",
                (ano_corrente,),
            ).fetchall()
        ]
        if anos:
            cur.execute(
                """
                INSERT INTO alerta_qualidade (tipo, companhia_id, detalhe, valor)
                SELECT CASE WHEN cardinality(f.faltam) = cardinality(%(anos)s::int[])
                            THEN 'SEM_DFP_NA_JANELA' ELSE 'HISTORICO_INCOMPLETO' END,
                       f.id,
                       'Sem demonstração anual em: ' || array_to_string(f.faltam, ', '),
                       cardinality(f.faltam)
                FROM (
                    SELECT c.id, ARRAY(
                        SELECT a FROM unnest(%(anos)s::int[]) a
                        WHERE NOT EXISTS (
                            SELECT 1 FROM documento d
                            WHERE d.companhia_id = c.id AND d.tipo = 'DFP'
                              AND extract(year FROM d.dt_referencia) = a)
                        ORDER BY a) AS faltam
                    FROM companhia c WHERE c.ativa
                ) f
                WHERE cardinality(f.faltam) > 0
                """,
                {"anos": anos},
            )

        # 4. Documentos vigentes sem nenhuma linha.
        cur.execute(
            """
            INSERT INTO alerta_qualidade (tipo, companhia_id, documento_id, detalhe)
            SELECT 'VIGENTE_SEM_LINHAS', d.companhia_id, d.id,
                   format('%s de %s, versão %s, sem linhas no arquivo da CVM', d.tipo, d.dt_referencia, d.versao)
            FROM documento d
            WHERE d.vigente AND NOT EXISTS (
                SELECT 1 FROM demonstracao_linha l
                WHERE l.documento_id = d.id
                  AND l.ano_referencia = extract(year FROM d.dt_referencia)::int)
            """
        )

        # 5. Companhias que só existem nos documentos.
        cur.execute(
            """
            INSERT INTO alerta_qualidade (tipo, companhia_id, detalhe)
            SELECT 'FORA_DO_CADASTRO', id, 'Presente nos documentos, ausente do cadastro atual da CVM'
            FROM companhia WHERE situacao_registro = 'FORA DO CADASTRO'
            """
        )

        return dict(cur.execute("SELECT tipo, count(*) FROM alerta_qualidade GROUP BY 1").fetchall())


def gerar_relatorio_qualidade(conn: psycopg.Connection) -> str:
    cur = conn.cursor()
    contagem = dict(cur.execute("SELECT tipo, count(*) FROM alerta_qualidade GROUP BY 1").fetchall())
    partes = [
        "# Relatório de qualidade dos dados",
        "",
        "## Alertas por tipo",
        "",
        _tabela(
            ["Tipo", "O que significa", "Alertas"],
            [[tipo, descricao, contagem.get(tipo, 0)] for tipo, descricao in DESCRICAO.items()],
        ),
        "",
        "## Balanços em que ativo e passivo não coincidem",
        "",
    ]
    casos = cur.execute(
        """
        SELECT c.denominacao, d.tipo, d.dt_referencia, a.valor, a.detalhe
        FROM alerta_qualidade a
        JOIN documento d ON d.id = a.documento_id
        JOIN companhia c ON c.id = a.companhia_id
        WHERE a.tipo = 'BALANCO_NAO_FECHA'
        ORDER BY abs(a.valor) DESC
        """
    ).fetchall()
    partes += [
        _tabela(["Companhia", "Documento", "Referência", "Diferença (R$)", "Detalhe"], casos)
        if casos else "Nenhum caso.",
        "",
        "## Companhias ativas com histórico anual incompleto",
        "",
        _tabela(
            ["Exercícios faltantes", "Companhias"],
            cur.execute(
                "SELECT valor::int, count(*) FROM alerta_qualidade "
                "WHERE tipo IN ('HISTORICO_INCOMPLETO', 'SEM_DFP_NA_JANELA') GROUP BY 1 ORDER BY 1"
            ).fetchall(),
        ),
        "",
        "## Documentos com mais contas repetidas com valores diferentes",
        "",
        _tabela(
            ["Companhia", "Documento", "Referência", "Contas"],
            cur.execute(
                """
                SELECT c.denominacao, d.tipo, d.dt_referencia, a.valor::int
                FROM alerta_qualidade a
                JOIN documento d ON d.id = a.documento_id
                JOIN companhia c ON c.id = a.companhia_id
                WHERE a.tipo = 'CONTA_REPETIDA_COM_VALORES_DIFERENTES'
                ORDER BY a.valor DESC, c.denominacao LIMIT 20
                """
            ).fetchall(),
        ),
        "",
    ]
    return "\n".join(partes)
