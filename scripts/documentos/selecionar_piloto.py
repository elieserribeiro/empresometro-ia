"""Seleciona as 20 companhias do piloto documental a partir dos indicadores.

Critério (representativas por setor):
- a maior receita anual de cada um dos 15 maiores setores-base (em número de companhias ativas);
- o segundo maior banco;
- a maior seguradora;
- as três maiores companhias em recuperação judicial ou extrajudicial.

Uso (com DATABASE_URL apontando para um banco com indicadores calculados):
    python scripts/documentos/selecionar_piloto.py --saida docs/documentos/piloto.md
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from empresometro.etl.fontes import conectar
from empresometro.etl.relatorio import _tabela

BASE = """
WITH ultimo AS (
    SELECT max(dt_referencia) d FROM indicador_valor
    WHERE periodo = 'ANUAL' AND extract(month FROM dt_referencia) = 12),
cia AS (
    SELECT c.id, c.cnpj, c.cd_cvm, c.denominacao, c.situacao_emissor, coalesce(s.setor_base, '(sem setor)') setor,
           max(v.plano) plano,
           max(v.valor) FILTER (WHERE v.codigo = 'RECEITA_LIQUIDA') receita,
           max(v.valor) FILTER (WHERE v.codigo = 'LUCRO_LIQUIDO') lucro
    FROM companhia c
    JOIN indicador_valor v ON v.companhia_id = c.id AND v.periodo = 'ANUAL'
    JOIN ultimo u ON u.d = v.dt_referencia
    LEFT JOIN setor s ON s.id = c.setor_id
    WHERE c.ativa
    GROUP BY c.id, c.cnpj, c.cd_cvm, c.denominacao, c.situacao_emissor, s.setor_base
    HAVING max(v.valor) FILTER (WHERE v.codigo = 'RECEITA_LIQUIDA') IS NOT NULL),
ordenada AS (
    SELECT cia.*, row_number() OVER (PARTITION BY setor, plano ORDER BY receita DESC) posicao FROM cia)
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--saida", type=Path, default=Path("docs/documentos/piloto.md"))
    args = parser.parse_args()
    conn = conectar()
    cur = conn.cursor()
    escolhidas: dict[str, tuple] = {}

    def incluir(linhas, motivo: str, limite: int) -> None:
        novas = 0
        for linha in linhas:
            if novas >= limite:
                break
            if linha[0] not in escolhidas:
                escolhidas[linha[0]] = (*linha, motivo)
                novas += 1

    campos = "cnpj, cd_cvm, denominacao, setor, plano, situacao_emissor, receita, lucro"
    setores = [
        s for (s,) in cur.execute(
            """
            SELECT s.setor_base FROM companhia c JOIN setor s ON s.id = c.setor_id
            WHERE c.ativa AND s.setor_base <> 'Sem Setor Principal'
            GROUP BY 1 ORDER BY count(*) DESC, 1 LIMIT 15
            """
        ).fetchall()
    ]
    for setor in setores:
        plano = "BANCO" if setor == "Bancos" else "COMUM"
        incluir(
            cur.execute(
                BASE + f"SELECT {campos} FROM ordenada WHERE setor = %s AND plano = %s "
                "AND situacao_emissor = 'FASE OPERACIONAL' ORDER BY receita DESC LIMIT 3",
                (setor, plano),
            ).fetchall(),
            "Maior receita do setor", 1,
        )
    incluir(
        cur.execute(BASE + f"SELECT {campos} FROM ordenada WHERE plano = 'BANCO' ORDER BY receita DESC LIMIT 5").fetchall(),
        "Segundo banco", 1,
    )
    incluir(
        cur.execute(BASE + f"SELECT {campos} FROM ordenada WHERE plano = 'SEGURADORA' ORDER BY receita DESC LIMIT 3").fetchall(),
        "Maior seguradora", 1,
    )
    incluir(
        cur.execute(
            BASE + f"SELECT {campos} FROM ordenada WHERE situacao_emissor ILIKE '%%RECUPERAÇÃO%%' ORDER BY receita DESC LIMIT 8"
        ).fetchall(),
        "Em recuperação judicial ou extrajudicial", 3,
    )
    # Completa até 20 com as maiores receitas ainda não escolhidas.
    incluir(
        cur.execute(BASE + f"SELECT {campos} FROM ordenada WHERE situacao_emissor = 'FASE OPERACIONAL' ORDER BY receita DESC LIMIT 60").fetchall(),
        "Maior receita entre as demais", max(0, 20 - len(escolhidas)),
    )

    linhas = list(escolhidas.values())
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    args.saida.write_text(
        "\n".join(
            [
                "# Companhias do piloto documental",
                "",
                "Seleção pelos indicadores do último exercício anual. Receita e lucro em R$ bilhões.",
                "",
                _tabela(
                    ["#", "Companhia", "Código CVM", "Setor-base", "Plano", "Situação", "Receita", "Lucro", "Critério"],
                    [
                        [i, l[2], l[1], l[3], l[4], l[5], round(l[6] / 10**9, 1), None if l[7] is None else round(l[7] / 10**9, 1), l[8]]
                        for i, l in enumerate(linhas, start=1)
                    ],
                ),
                "",
            ]
        ),
        encoding="utf-8",
    )
    with open(args.saida.with_suffix(".csv"), "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(["cnpj", "cd_cvm", "denominacao", "setor_base", "plano", "criterio"])
        for l in linhas:
            escritor.writerow([l[0], l[1], l[2], l[3], l[4], l[8]])
    print(f"{len(linhas)} companhias gravadas em {args.saida}")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
