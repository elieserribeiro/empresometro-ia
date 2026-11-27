"""Conta os documentos das companhias do piloto nos índices do IPE e do FRE, por ano."""

from __future__ import annotations

import csv
import datetime as dt
import io
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "discovery"))
from data_discovery import BASE_CVM, _tabela, baixar  # noqa: E402

csv.field_size_limit(10**9)
CATEGORIAS = ("Fato Relevante", "Comunicado ao Mercado")


def digitos(v):
    return re.sub(r"\D", "", v or "")


def main() -> int:
    piloto = {digitos(l["cnpj"]): l["denominacao"] for l in csv.DictReader(open("docs/documentos/piloto.csv", encoding="utf-8"), delimiter=";")}
    anos = list(range(2021, dt.date.today().year + 1))
    bruto = Path("data/raw/documentos")
    por_ano: dict = {a: Counter() for a in anos}
    por_cia: Counter = Counter()
    for ano in anos:
        destino = bruto / f"ipe_cia_aberta_{ano}.zip"
        baixar(f"{BASE_CVM}/DOC/IPE/DADOS/ipe_cia_aberta_{ano}.zip", destino)
        with zipfile.ZipFile(destino) as z:
            vistos = set()
            for l in csv.DictReader(io.TextIOWrapper(z.open(z.infolist()[0].filename), encoding="latin-1", newline=""), delimiter=";"):
                cnpj, cat = digitos(l.get("CNPJ_Companhia")), (l.get("Categoria") or "").strip()
                chave = (cnpj, (l.get("Protocolo_Entrega") or "").strip() or l.get("Link_Download"))
                if cnpj in piloto and cat in CATEGORIAS and chave not in vistos:
                    vistos.add(chave)
                    por_ano[ano][cat] += 1
                    por_cia[piloto[cnpj]] += 1
        destino = bruto / f"fre_cia_aberta_{ano}.zip"
        baixar(f"{BASE_CVM}/DOC/FRE/DADOS/fre_cia_aberta_{ano}.zip", destino)
        with zipfile.ZipFile(destino) as z:
            formularios = {
                (digitos(l.get("CNPJ_CIA")), l.get("DT_REFER"))
                for l in csv.DictReader(io.TextIOWrapper(z.open(f"fre_cia_aberta_{ano}.csv"), encoding="latin-1", newline=""), delimiter=";")
                if digitos(l.get("CNPJ_CIA")) in piloto
            }
            por_ano[ano]["FRE"] = len(formularios)
    saida = [
        "# Volume de documentos das companhias do piloto",
        "",
        _tabela(
            ["Ano", "Fatos relevantes", "Comunicados ao mercado", "Formulários de Referência"],
            [[a, por_ano[a]["Fato Relevante"], por_ano[a]["Comunicado ao Mercado"], por_ano[a]["FRE"]] for a in anos]
            + [["Total", sum(por_ano[a]["Fato Relevante"] for a in anos), sum(por_ano[a]["Comunicado ao Mercado"] for a in anos), sum(por_ano[a]["FRE"] for a in anos)]],
        ),
        "",
        _tabela(["Companhia", "Fatos e comunicados (2021 em diante)"], por_cia.most_common()),
        "",
    ]
    Path("docs/documentos/volume_piloto.md").write_text("\n".join(saida), encoding="utf-8")
    print("\n".join(saida))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
