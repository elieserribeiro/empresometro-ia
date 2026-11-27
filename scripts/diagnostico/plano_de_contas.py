"""Diagnóstico do plano de contas da CVM para definir as fórmulas dos indicadores.

Agrupa os documentos vigentes pelo tipo de plano de contas (identificado pela
descrição da conta 3.01 da DRE) e lista as contas fixas de cada plano, com a
descrição e o número de documentos em que aparecem.

Uso (com DATABASE_URL apontando para um banco carregado):
    python scripts/diagnostico/plano_de_contas.py --saida docs/indicadores/plano_de_contas.md
"""

from __future__ import annotations

import argparse
from pathlib import Path

from empresometro.etl.fontes import conectar
from empresometro.etl.relatorio import _tabela

FAMILIA = """
    SELECT d.id AS documento_id, d.companhia_id,
           coalesce((SELECT max(l.ds_conta) FROM demonstracao_linha l
                     WHERE l.documento_id = d.id AND l.demonstracao = 'DRE'
                       AND l.cd_conta = '3.01' AND l.ordem_exercicio = 'ULTIMO'), '(sem DRE)') AS familia
    FROM documento d WHERE d.vigente AND d.tipo = 'DFP'
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--saida", type=Path, default=Path("docs/indicadores/plano_de_contas.md"))
    parser.add_argument("--niveis", type=int, default=3)
    args = parser.parse_args()

    conn = conectar()
    cur = conn.cursor()
    cur.execute(f"CREATE TEMP TABLE familia AS {FAMILIA}")
    partes = ["# Plano de contas da CVM por tipo de companhia", ""]

    familias = cur.execute(
        "SELECT familia, count(*), count(DISTINCT companhia_id) FROM familia GROUP BY 1 ORDER BY 2 DESC"
    ).fetchall()
    partes += [
        "## Tipos de plano (pela descrição da conta 3.01 da DRE)",
        "",
        _tabela(["Descrição da conta 3.01", "Documentos", "Companhias"], familias),
        "",
        "## Setores em cada tipo de plano",
        "",
        _tabela(
            ["Descrição da conta 3.01", "Setor-base", "Companhias"],
            cur.execute(
                """
                SELECT f.familia, coalesce(s.setor_base, '(sem setor)'), count(DISTINCT f.companhia_id)
                FROM familia f JOIN companhia c ON c.id = f.companhia_id
                LEFT JOIN setor s ON s.id = c.setor_id
                GROUP BY 1, 2 ORDER BY 1, 3 DESC
                """
            ).fetchall(),
        ),
        "",
    ]

    for familia, documentos, _ in familias:
        if familia == "(sem DRE)":
            continue
        partes += [f"## Plano: {familia} ({documentos} documentos)", ""]
        linhas = cur.execute(
            """
            SELECT l.demonstracao, l.escopo, l.cd_conta,
                   mode() WITHIN GROUP (ORDER BY l.ds_conta), count(DISTINCT l.documento_id),
                   count(DISTINCT l.ds_conta)
            FROM demonstracao_linha l JOIN familia f ON f.documento_id = l.documento_id
            WHERE f.familia = %s AND l.ordem_exercicio = 'ULTIMO' AND l.conta_fixa
              AND l.demonstracao IN ('BPA', 'BPP', 'DRE', 'DFC_MI', 'DFC_MD', 'DVA')
              AND cardinality(string_to_array(l.cd_conta, '.')) <= %s
            GROUP BY 1, 2, 3
            ORDER BY 1, 2, string_to_array(l.cd_conta, '.')::int[]
            """,
            (familia, args.niveis),
        ).fetchall()
        partes += [
            _tabela(["Demonstração", "Escopo", "Conta", "Descrição mais comum", "Documentos", "Descrições distintas"], linhas),
            "",
        ]

    args.saida.parent.mkdir(parents=True, exist_ok=True)
    args.saida.write_text("\n".join(partes), encoding="utf-8")
    print(f"Diagnóstico gravado em {args.saida}")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
