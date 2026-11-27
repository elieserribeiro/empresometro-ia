"""Relatório de conferência da carga."""

from __future__ import annotations

import psycopg


def _tabela(cabecalho: list[str], linhas: list) -> str:
    saida = ["| " + " | ".join(cabecalho) + " |", "|" + "---|" * len(cabecalho)]
    saida += ["| " + " | ".join("-" if c is None else str(c) for c in linha) + " |" for linha in linhas]
    return "\n".join(saida)


def gerar_relatorio(conn: psycopg.Connection, eventos: list[dict] | None = None) -> str:
    """Monta um relatório em Markdown com as contagens e verificações do banco."""
    cur = conn.cursor()

    def consulta(sql: str) -> list:
        return cur.execute(sql).fetchall()

    partes = ["# Relatório de carga do banco", ""]

    if eventos:
        partes += [
            "## Execução",
            "",
            _tabela(
                ["Arquivo", "Situação", "Documentos", "Linhas", "Linhas órfãs", "Segundos"],
                [
                    [e["arquivo"], e["situacao"], e.get("documentos"), e.get("linhas"),
                     e.get("linhas_orfas"), e.get("segundos")]
                    for e in eventos
                ],
            ),
            "",
            "Linha órfã: linha de demonstração cuja companhia, data e versão não constam do índice do arquivo.",
            "",
        ]

    tamanho = consulta("SELECT pg_size_pretty(pg_database_size(current_database()))")[0][0]
    partes += [
        "## Tabelas",
        "",
        f"Tamanho total do banco: **{tamanho}**",
        "",
        _tabela(
            ["Tabela", "Linhas", "Tamanho"],
            consulta(
                """
                SELECT t, n, pg_size_pretty(s) FROM (
                    SELECT 'setor' t, (SELECT count(*) FROM setor) n, pg_total_relation_size('setor') s
                    UNION ALL SELECT 'companhia', (SELECT count(*) FROM companhia), pg_total_relation_size('companhia')
                    UNION ALL SELECT 'companhia_mercado', (SELECT count(*) FROM companhia_mercado), pg_total_relation_size('companhia_mercado')
                    UNION ALL SELECT 'documento', (SELECT count(*) FROM documento), pg_total_relation_size('documento')
                    UNION ALL SELECT 'demonstracao_linha', (SELECT count(*) FROM demonstracao_linha),
                        (SELECT coalesce(sum(pg_total_relation_size(inhrelid)), 0)::bigint FROM pg_inherits
                         WHERE inhparent = 'demonstracao_linha'::regclass)
                    UNION ALL SELECT 'composicao_capital', (SELECT count(*) FROM composicao_capital), pg_total_relation_size('composicao_capital')
                    UNION ALL SELECT 'parecer', (SELECT count(*) FROM parecer), pg_total_relation_size('parecer')
                    UNION ALL SELECT 'carga_arquivo', (SELECT count(*) FROM carga_arquivo), pg_total_relation_size('carga_arquivo')
                ) x
                """
            ),
        ),
        "",
        "## Companhias",
        "",
        _tabela(
            ["Ativa", "Companhias", "Com algum documento"],
            consulta(
                """
                SELECT CASE WHEN c.ativa THEN 'sim' ELSE 'não' END, count(*),
                       count(*) FILTER (WHERE EXISTS (SELECT 1 FROM documento d WHERE d.companhia_id = c.id))
                FROM companhia c GROUP BY c.ativa ORDER BY c.ativa DESC
                """
            ),
        ),
        "",
        _tabela(
            ["Situação do emissor (ativas)", "Companhias"],
            consulta(
                "SELECT coalesce(situacao_emissor, '(vazio)'), count(*) FROM companhia WHERE ativa "
                "GROUP BY 1 ORDER BY 2 DESC"
            ),
        ),
        "",
        _tabela(
            ["Companhias ativas por quantidade de mercados", "Companhias"],
            consulta(
                """
                SELECT n, count(*) FROM (
                    SELECT c.id, (SELECT count(*) FROM companhia_mercado m WHERE m.companhia_id = c.id) n
                    FROM companhia c WHERE c.ativa) x GROUP BY n ORDER BY n
                """
            ),
        ),
        "",
        _tabela(
            ["Setor-base", "Setores da CVM reunidos", "Companhias ativas"],
            consulta(
                """
                SELECT s.setor_base, count(DISTINCT s.id), count(c.id) FILTER (WHERE c.ativa)
                FROM setor s LEFT JOIN companhia c ON c.setor_id = s.id
                GROUP BY s.setor_base ORDER BY 3 DESC, 1
                """
            ),
        ),
        "",
        "## Documentos",
        "",
        _tabela(
            ["Tipo", "Ano", "Documentos", "Vigentes", "Versões anteriores", "Companhias"],
            consulta(
                """
                SELECT tipo, extract(year FROM dt_referencia)::int, count(*),
                       count(*) FILTER (WHERE vigente), count(*) FILTER (WHERE NOT vigente),
                       count(DISTINCT companhia_id)
                FROM documento GROUP BY 1, 2 ORDER BY 1, 2
                """
            ),
        ),
        "",
        "### Os arquivos trazem os valores das versões anteriores?",
        "",
        _tabela(
            ["Versão", "Documentos", "Com linhas de demonstração", "Sem linhas"],
            consulta(
                """
                SELECT CASE WHEN d.vigente THEN 'vigente' ELSE 'anterior' END, count(*),
                       count(*) FILTER (WHERE t.documento_id IS NOT NULL),
                       count(*) FILTER (WHERE t.documento_id IS NULL)
                FROM documento d
                LEFT JOIN (SELECT DISTINCT documento_id FROM demonstracao_linha) t ON t.documento_id = d.id
                GROUP BY d.vigente ORDER BY d.vigente DESC
                """
            ),
        ),
        "",
        "## Linhas das demonstrações",
        "",
        _tabela(
            ["Ano", "Demonstração", "Linhas", "Em milhares", "Em unidades", "Sem valor"],
            consulta(
                """
                SELECT ano_referencia, demonstracao, count(*), count(*) FILTER (WHERE escala = 'MIL'),
                       count(*) FILTER (WHERE escala = 'UNIDADE'), count(*) FILTER (WHERE valor_original IS NULL)
                FROM demonstracao_linha GROUP BY 1, 2 ORDER BY 1, 2
                """
            ),
        ),
        "",
        "### Linhas repetidas na chave completa",
        "",
        "Grupos de linhas com o mesmo documento, demonstração, escopo, exercício, período, coluna e código de conta.",
        "",
        _tabela(
            ["Demonstração", "Grupos repetidos", "Com descrições diferentes", "Com valores diferentes", "Idênticos"],
            consulta(
                """
                SELECT demonstracao, count(*),
                       count(*) FILTER (WHERE descricoes > 1),
                       count(*) FILTER (WHERE valores > 1),
                       count(*) FILTER (WHERE descricoes = 1 AND valores <= 1)
                FROM (
                    SELECT demonstracao, count(DISTINCT ds_conta) descricoes, count(DISTINCT valor_original) valores
                    FROM demonstracao_linha
                    GROUP BY documento_id, demonstracao, escopo, ordem_exercicio, dt_inicio, dt_fim, coluna_df, cd_conta
                    HAVING count(*) > 1
                ) g GROUP BY demonstracao ORDER BY demonstracao
                """
            ),
        ),
        "",
        "### Conferência: ativo total igual a passivo total",
        "",
        "Documentos vigentes, consolidado, último exercício: conta 1 do balanço ativo comparada à conta 2 do passivo.",
        "",
        _tabela(
            ["Documentos comparados", "Iguais", "Diferentes"],
            consulta(
                """
                SELECT count(*), count(*) FILTER (WHERE a.v = p.v), count(*) FILTER (WHERE a.v IS DISTINCT FROM p.v)
                FROM (SELECT l.documento_id, max(l.valor_reais) v FROM demonstracao_linha l
                      JOIN documento d ON d.id = l.documento_id AND d.vigente
                      WHERE l.demonstracao = 'BPA' AND l.escopo = 'CON' AND l.ordem_exercicio = 'ULTIMO' AND l.cd_conta = '1'
                      GROUP BY l.documento_id) a
                JOIN (SELECT l.documento_id, max(l.valor_reais) v FROM demonstracao_linha l
                      WHERE l.demonstracao = 'BPP' AND l.escopo = 'CON' AND l.ordem_exercicio = 'ULTIMO' AND l.cd_conta = '2'
                      GROUP BY l.documento_id) p USING (documento_id)
                """
            ),
        ),
        "",
    ]
    return "\n".join(partes)
