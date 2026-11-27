"""Sonda do IF.data: disponibilidade dos relatórios de capital e de crédito ao longo do tempo."""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sonda_ifdata import obter  # noqa: E402

DATAS = [202103, 202112, 202212, 202312, 202412, 202503, 202506, 202509]
ITAU = "C0080099"


def main() -> int:
    saida = ["# IF.data: disponibilidade por data-base (conglomerados prudenciais)", ""]
    for data in DATAS:
        saida += [f"## {data}", ""]
        for relatorio in ("5", "8", "16"):
            valores, _ = obter(
                "IfDataValores(AnoMes=@AnoMes,TipoInstituicao=@TipoInstituicao,Relatorio=@Relatorio)",
                **{"@AnoMes": data, "@TipoInstituicao": 1, "@Relatorio": f"'{relatorio}'", "$top": 100000},
            )
            if not valores or "ERRO" in valores[0]:
                saida += [f"- Relatório {relatorio}: sem dados {(valores or [{}])[0].get('ERRO', '')[:100]}"]
                continue
            colunas = Counter((str(v.get("Conta")), " ".join(str(v.get("NomeColuna")).split())) for v in valores)
            saida += [
                f"- Relatório {relatorio}: {len(valores)} valores, {len({v.get('CodInst') for v in valores})} instituições; "
                + "; ".join(f"{conta}={nome}" for (conta, nome), _ in sorted(colunas.items())[:40])
            ]
            do_itau = {str(v.get("Conta")): v.get("Saldo") for v in valores if v.get("CodInst") == ITAU}
            interesse = {c: do_itau.get(c) for c in ("79664", "79659", "79660", "79661", "148834", "148833", "24454") if c in do_itau}
            if interesse:
                saida += [f"  - Itaú ({ITAU}): {interesse}"]
            elif relatorio == "8":
                saida += [f"  - Itaú ({ITAU}): {dict(list(do_itau.items())[:14])}"]
    Path("docs/discovery/sonda_ifdata_datas.md").write_text("\n".join(saida), encoding="utf-8")
    print("\n".join(saida))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
