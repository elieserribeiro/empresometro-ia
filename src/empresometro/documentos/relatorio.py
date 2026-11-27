"""Relatório da coleta documental."""

from __future__ import annotations

import statistics

import psycopg

from ..etl.relatorio import _tabela


def gerar_relatorio_coleta(conn: psycopg.Connection, eventos: list[dict] | None = None) -> str:
    cur = conn.cursor()

    def consulta(sql: str) -> list:
        return cur.execute(sql).fetchall()

    partes = ["# Relatório da coleta de documentos", ""]
    if eventos:
        partes += ["## Tempos desta execução", ""]
        linhas = []
        for fonte in ("IPE", "FRE_PACOTE", "FRE", "PARECER"):
            tempos = [e["segundos"] for e in eventos if e["fonte"] == fonte]
            if tempos:
                linhas.append(
                    [fonte, len(tempos), round(sum(tempos)), round(statistics.median(tempos), 1), round(max(tempos), 1)]
                )
        partes += [
            _tabela(["Fonte", "Itens processados", "Segundos no total", "Mediana por item (s)", "Máximo (s)"], linhas),
            "",
            "FRE_PACOTE é o download e a leitura de um formulário inteiro; FRE são as seções extraídas dele.",
            "",
        ]
    partes += [
        "## Documentos por fonte e situação",
        "",
        _tabela(
            ["Fonte", "Categoria", "Situação", "Documentos", "Páginas", "Caracteres (milhões)", "Trechos"],
            consulta(
                """
                SELECT d.fonte, coalesce(d.categoria, '-'), d.situacao, count(*), coalesce(sum(d.paginas), 0),
                       round(sum(d.caracteres) / 1e6, 2), coalesce(sum(n.trechos), 0)
                FROM documento_texto d
                LEFT JOIN (SELECT documento_texto_id, count(*) trechos FROM trecho GROUP BY 1) n
                       ON n.documento_texto_id = d.id
                WHERE d.chave_origem NOT LIKE '%:_pacote'
                GROUP BY d.fonte, coalesce(d.categoria, '-'), d.situacao ORDER BY 1, 2, 3
                """
            ),
        ),
        "",
        "## Por companhia",
        "",
        _tabela(
            ["Companhia", "Fatos e comunicados", "Seções de FRE", "Pareceres", "Trechos", "Sem texto", "Com erro"],
            consulta(
                """
                SELECT c.denominacao,
                       count(*) FILTER (WHERE d.fonte = 'IPE'),
                       count(*) FILTER (WHERE d.fonte = 'FRE' AND d.chave_origem NOT LIKE '%:_pacote'),
                       count(*) FILTER (WHERE d.fonte = 'PARECER'),
                       (SELECT count(*) FROM trecho t JOIN documento_texto x ON x.id = t.documento_texto_id
                        WHERE x.companhia_id = c.id),
                       count(*) FILTER (WHERE d.situacao = 'SEM_TEXTO' AND d.chave_origem NOT LIKE '%:_pacote'),
                       count(*) FILTER (WHERE d.situacao = 'ERRO')
                FROM documento_texto d JOIN companhia c ON c.id = d.companhia_id
                GROUP BY c.id, c.denominacao ORDER BY 1
                """
            ),
        ),
        "",
        "## Trechos",
        "",
        _tabela(
            ["Trechos", "Caracteres (milhões)", "Tamanho mediano", "Menor", "Maior"],
            consulta(
                """
                SELECT count(*), round(coalesce(sum(caracteres), 0) / 1e6, 2),
                       percentile_cont(0.5) WITHIN GROUP (ORDER BY caracteres), min(caracteres), max(caracteres)
                FROM trecho
                """
            ),
        ),
        "",
        "## Erros mais frequentes",
        "",
        _tabela(
            ["Fonte", "Erro", "Documentos"],
            consulta(
                "SELECT fonte, left(erro, 120), count(*) FROM documento_texto WHERE situacao = 'ERRO' "
                "GROUP BY 1, 2 ORDER BY 3 DESC LIMIT 10"
            ),
        ),
        "",
        "## Exemplo de busca textual",
        "",
        "Consulta: `recuperação judicial` (os três trechos mais relevantes).",
        "",
        _tabela(
            ["Companhia", "Fonte", "Título", "Página", "Trecho"],
            consulta(
                """
                SELECT c.denominacao, d.fonte, left(d.titulo, 60), t.pagina_inicial,
                       replace(left(t.texto, 160), E'\\n', ' ')
                FROM trecho t JOIN documento_texto d ON d.id = t.documento_texto_id
                JOIN companhia c ON c.id = d.companhia_id,
                     websearch_to_tsquery('portuguese', 'recuperação judicial') q
                WHERE t.busca @@ q ORDER BY ts_rank(t.busca, q) DESC LIMIT 3
                """
            ),
        ),
        "",
    ]
    return "\n".join(partes)
