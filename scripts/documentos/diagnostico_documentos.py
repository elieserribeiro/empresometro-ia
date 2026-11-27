"""Diagnóstico das fontes documentais da CVM (FRE e IPE) para dimensionar o RAG.

Mede o que existe nos arquivos consolidados: quais arquivos e colunas trazem
texto longo no FRE e quantos documentos o IPE lista por categoria e por ano.

Uso:
    python scripts/documentos/diagnostico_documentos.py --saida docs/discovery/diagnostico_documentos.md
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import statistics
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "discovery"))

from data_discovery import BASE_CVM, _tabela, baixar  # noqa: E402

csv.field_size_limit(10**9)
TEXTO_LONGO = 500


def _ler(pacote: zipfile.ZipFile, membro: str) -> csv.DictReader:
    return csv.DictReader(io.TextIOWrapper(pacote.open(membro), encoding="latin-1", newline=""), delimiter=";")


def perfilar_fre(caminho: Path) -> list[dict]:
    perfis = []
    with zipfile.ZipFile(caminho) as pacote:
        for membro in pacote.infolist():
            if membro.is_dir():
                continue
            leitor = _ler(pacote, membro.filename)
            colunas = leitor.fieldnames or []
            maximo: Counter = Counter()
            soma: Counter = Counter()
            companhias = set()
            linhas = 0
            for linha in leitor:
                linhas += 1
                companhias.add(linha.get("CNPJ_Companhia") or linha.get("CNPJ_CIA") or "")
                for coluna in colunas:
                    tamanho = len(linha.get(coluna) or "")
                    soma[coluna] += tamanho
                    if tamanho > maximo[coluna]:
                        maximo[coluna] = tamanho
            textos = {c: (maximo[c], soma[c]) for c in colunas if maximo[c] >= TEXTO_LONGO}
            perfis.append(
                {
                    "arquivo": membro.filename, "linhas": linhas, "colunas": colunas,
                    "companhias": len(companhias - {""}), "bytes": membro.file_size,
                    "caracteres": sum(soma.values()), "textos": textos,
                }
            )
    return perfis


def perfilar_ipe(caminho: Path) -> dict:
    with zipfile.ZipFile(caminho) as pacote:
        membro = next(m.filename for m in pacote.infolist() if not m.is_dir())
        leitor = _ler(pacote, membro)
        colunas = leitor.fieldnames or []

        def achar(*trechos: str) -> str | None:
            return next((c for c in colunas if all(t in c.lower() for t in trechos)), None)

        c_cnpj, c_cat, c_tipo, c_esp = achar("cnpj"), achar("categoria"), achar("tipo"), achar("especie")
        c_link = achar("link")
        por_categoria: Counter = Counter()
        por_par: Counter = Counter()
        por_companhia: Counter = Counter()
        exemplo_link = ""
        total = 0
        for linha in leitor:
            total += 1
            categoria = (linha.get(c_cat) or "").strip() if c_cat else ""
            por_categoria[categoria] += 1
            por_par[(categoria, (linha.get(c_tipo) or "").strip() if c_tipo else "",
                     (linha.get(c_esp) or "").strip() if c_esp else "")] += 1
            if c_cnpj:
                por_companhia[linha.get(c_cnpj) or ""] += 1
            if c_link and not exemplo_link:
                exemplo_link = (linha.get(c_link) or "")[:120]
    return {
        "arquivo": membro, "colunas": colunas, "total": total, "por_categoria": por_categoria,
        "por_par": por_par, "por_companhia": por_companhia, "exemplo_link": exemplo_link,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ano-inicial", type=int, default=2021)
    parser.add_argument("--ano-final", type=int, default=dt.date.today().year)
    parser.add_argument("--bruto", type=Path, default=Path("data/raw/documentos"))
    parser.add_argument("--saida", type=Path, default=Path("docs/discovery/diagnostico_documentos.md"))
    args = parser.parse_args()
    anos = range(args.ano_inicial, args.ano_final + 1)
    partes = ["# Diagnóstico das fontes documentais (FRE e IPE)", ""]

    # ---------------- FRE ----------------
    fre: dict[int, list[dict]] = {}
    for ano in anos:
        destino = args.bruto / f"fre_cia_aberta_{ano}.zip"
        info = baixar(f"{BASE_CVM}/DOC/FRE/DADOS/fre_cia_aberta_{ano}.zip", destino)
        if info["ok"]:
            fre[ano] = perfilar_fre(destino)
    partes += [
        "## Formulário de Referência (FRE)",
        "",
        _tabela(
            ["Ano", "Arquivos", "Linhas", "Caracteres (milhões)", "Arquivos com texto longo"],
            [
                [ano, len(p), sum(x["linhas"] for x in p), round(sum(x["caracteres"] for x in p) / 1e6, 1),
                 sum(1 for x in p if x["textos"])]
                for ano, p in fre.items()
            ],
        ),
        "",
    ]
    if fre:
        ultimo = max(a for a in fre if a < args.ano_final) if len(fre) > 1 else max(fre)
        partes += [
            f"### Arquivos do FRE de {ultimo}",
            "",
            _tabela(
                ["Arquivo", "Linhas", "Companhias", "Caracteres (mil)", "Colunas com texto longo (maior tamanho)"],
                [
                    [x["arquivo"], x["linhas"], x["companhias"], round(x["caracteres"] / 1e3),
                     ", ".join(f"{c} ({m})" for c, (m, _) in x["textos"].items()) or "-"]
                    for x in sorted(fre[ultimo], key=lambda x: -x["caracteres"])
                ],
            ),
            "",
            "Colunas do arquivo índice: "
            + ", ".join(
                f"`{c}`"
                for x in fre[ultimo] if x["arquivo"].lower() == f"fre_cia_aberta_{ultimo}.csv"
                for c in x["colunas"]
            ),
            "",
        ]

    # ---------------- IPE ----------------
    ipe: dict[int, dict] = {}
    for ano in anos:
        destino = args.bruto / f"ipe_cia_aberta_{ano}.zip"
        info = baixar(f"{BASE_CVM}/DOC/IPE/DADOS/ipe_cia_aberta_{ano}.zip", destino)
        if info["ok"]:
            ipe[ano] = perfilar_ipe(destino)
    partes += ["## Informações Periódicas e Eventuais (IPE)", ""]
    if ipe:
        linhas = []
        for ano, p in ipe.items():
            contagens = [n for cnpj, n in p["por_companhia"].items() if cnpj]
            linhas.append(
                [ano, p["total"], len(contagens), round(statistics.median(contagens)) if contagens else 0,
                 max(contagens) if contagens else 0]
            )
        partes += [
            _tabela(["Ano", "Documentos listados", "Companhias", "Mediana por companhia", "Máximo em uma companhia"], linhas),
            "",
        ]
        categorias = Counter()
        for p in ipe.values():
            categorias.update(p["por_categoria"])
        anos_ipe = list(ipe)
        partes += [
            "### Documentos por categoria e ano",
            "",
            _tabela(
                ["Categoria"] + [str(a) for a in anos_ipe] + ["Total"],
                [
                    [cat or "(vazio)"] + [ipe[a]["por_categoria"].get(cat, 0) for a in anos_ipe] + [total]
                    for cat, total in categorias.most_common()
                ],
            ),
            "",
        ]
        pares = Counter()
        for p in ipe.values():
            pares.update(p["por_par"])
        partes += [
            "### Combinações mais frequentes de categoria, tipo e espécie",
            "",
            _tabela(
                ["Categoria", "Tipo", "Espécie", "Documentos"],
                [[c or "-", t or "-", e or "-", n] for (c, t, e), n in pares.most_common(40)],
            ),
            "",
            "Colunas do índice: " + ", ".join(f"`{c}`" for c in ipe[anos_ipe[-1]]["colunas"]),
            "",
            f"Exemplo de link: `{ipe[anos_ipe[-1]]['exemplo_link']}`",
            "",
        ]

    args.saida.parent.mkdir(parents=True, exist_ok=True)
    args.saida.write_text("\n".join(partes), encoding="utf-8")
    print(f"Diagnóstico gravado em {args.saida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
