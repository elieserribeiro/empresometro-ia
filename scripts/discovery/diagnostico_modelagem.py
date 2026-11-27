"""Diagnóstico para a modelagem do banco (Fase 2).

Lê os arquivos já baixados pelo data_discovery.py e responde a três perguntas:

1. Por que há CNPJs repetidos entre as linhas ativas do cadastro?
2. Qual é a estrutura real das demonstrações (colunas, domínios, tamanhos)?
3. Qual combinação de colunas identifica uma linha sem repetição (chave)?

Uso:
    python scripts/discovery/diagnostico_modelagem.py --ano-dfp 2025 --ano-itr 2026
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from data_discovery import _tabela, esta_ativa, ler_csv_cvm, normalizar_cnpj  # noqa: E402

# Colunas de baixo número de valores distintos cujo domínio interessa à modelagem.
COLUNAS_DOMINIO = ["GRUPO_DFP", "MOEDA", "ESCALA_MOEDA", "ORDEM_EXERC", "ST_CONTA_FIXA", "CATEG_DOC"]
# Candidatas a chave, da mais simples para a mais completa.
CHAVES_CANDIDATAS = [
    ["CNPJ_CIA", "DT_REFER", "VERSAO", "ORDEM_EXERC", "CD_CONTA"],
    ["CNPJ_CIA", "DT_REFER", "VERSAO", "ORDEM_EXERC", "DT_INI_EXERC", "CD_CONTA"],
    ["CNPJ_CIA", "DT_REFER", "VERSAO", "ORDEM_EXERC", "DT_INI_EXERC", "COLUNA_DF", "CD_CONTA"],
]
COLUNAS_IGNORADAS_NO_CADASTRO = set()


def diagnosticar_cadastro(caminho: Path, max_exemplos: int = 8) -> dict:
    """Agrupa as linhas ativas por CNPJ e mostra em que colunas as repetidas diferem."""
    with open(caminho, "rb") as arquivo:
        linhas = list(ler_csv_cvm(arquivo))

    grupos: dict[str, list[dict]] = defaultdict(list)
    for linha in linhas:
        if esta_ativa(linha.get("SIT")):
            grupos[normalizar_cnpj(linha.get("CNPJ_CIA"))].append(linha)
    repetidos = {cnpj: g for cnpj, g in grupos.items() if len(g) > 1}

    colunas_divergentes: Counter = Counter()
    identicas = 0
    exemplos = []
    for cnpj, grupo in sorted(repetidos.items()):
        diferentes = [
            coluna
            for coluna in grupo[0]
            if coluna not in COLUNAS_IGNORADAS_NO_CADASTRO
            and len({(l.get(coluna) or "").strip() for l in grupo}) > 1
        ]
        if not diferentes:
            identicas += 1
        colunas_divergentes.update(diferentes)
        if len(exemplos) < max_exemplos:
            exemplos.append(
                {
                    "cnpj": cnpj,
                    "denominacao": (grupo[0].get("DENOM_SOCIAL") or "").strip(),
                    "linhas": len(grupo),
                    "diferencas": {
                        c: sorted({(l.get(c) or "").strip() for l in grupo}) for c in diferentes[:6]
                    },
                }
            )

    # Um mesmo código CVM aparece em mais de um CNPJ ativo?
    cnpjs_por_cd: dict[str, set] = defaultdict(set)
    for cnpj, grupo in grupos.items():
        for linha in grupo:
            cnpjs_por_cd[(linha.get("CD_CVM") or "").strip()].add(cnpj)

    return {
        "linhas_ativas": sum(len(g) for g in grupos.values()),
        "cnpjs_ativos": len(grupos),
        "cnpjs_repetidos": len(repetidos),
        "linhas_excedentes": sum(len(g) - 1 for g in repetidos.values()),
        "tamanho_dos_grupos": dict(sorted(Counter(len(g) for g in repetidos.values()).items())),
        "grupos_totalmente_identicos": identicas,
        "colunas_divergentes": dict(colunas_divergentes.most_common()),
        "cd_cvm_em_mais_de_um_cnpj": sum(1 for c in cnpjs_por_cd.values() if len(c) > 1),
        "exemplos": exemplos,
    }


def diagnosticar_zip(caminho: Path, limite_dominio: int = 15) -> list[dict]:
    """Perfila cada arquivo interno de um ZIP de DFP ou ITR."""
    perfis = []
    with zipfile.ZipFile(caminho) as pacote:
        for membro in pacote.infolist():
            if membro.is_dir():
                continue
            with pacote.open(membro) as fluxo:
                leitor = ler_csv_cvm(fluxo)
                colunas = leitor.fieldnames or []
                dominios = {c: Counter() for c in COLUNAS_DOMINIO if c in colunas}
                chaves = [k for k in CHAVES_CANDIDATAS if all(c in colunas for c in k)]
                vistos = [set() for _ in chaves]
                repetidas = [0] * len(chaves)
                tamanho_max: Counter = Counter()
                contas: set = set()
                profundidade: Counter = Counter()
                vazios: Counter = Counter()
                total = 0
                for linha in leitor:
                    total += 1
                    for coluna, contador in dominios.items():
                        contador[(linha.get(coluna) or "").strip()] += 1
                    for coluna in colunas:
                        valor = linha.get(coluna) or ""
                        if len(valor) > tamanho_max[coluna]:
                            tamanho_max[coluna] = len(valor)
                        if not valor.strip():
                            vazios[coluna] += 1
                    conta = (linha.get("CD_CONTA") or "").strip()
                    if conta:
                        contas.add(conta)
                        profundidade[conta.count(".") + 1] += 1
                    for i, chave in enumerate(chaves):
                        marca = hash(tuple(linha.get(c) for c in chave))
                        if marca in vistos[i]:
                            repetidas[i] += 1
                        else:
                            vistos[i].add(marca)
            perfis.append(
                {
                    "arquivo": membro.filename,
                    "linhas": total,
                    "colunas": colunas,
                    "dominios": {
                        c: dict(v.most_common(limite_dominio)) for c, v in dominios.items()
                    },
                    "tamanho_max": dict(tamanho_max),
                    "vazios": {c: n for c, n in vazios.items() if n},
                    "contas_distintas": len(contas),
                    "profundidade_contas": dict(sorted(profundidade.items())),
                    "chaves": [
                        {"colunas": chave, "linhas_repetidas": repetidas[i]}
                        for i, chave in enumerate(chaves)
                    ],
                }
            )
    return perfis


def _secao_zip(titulo: str, perfis: list[dict]) -> list[str]:
    partes = [f"## {titulo}", ""]
    partes += [
        _tabela(
            ["Arquivo", "Linhas", "Contas distintas", "Níveis de conta", "Colunas"],
            [
                [
                    p["arquivo"],
                    p["linhas"],
                    p["contas_distintas"] or "-",
                    ", ".join(f"{n}: {q}" for n, q in p["profundidade_contas"].items()) or "-",
                    len(p["colunas"]),
                ]
                for p in perfis
            ],
        ),
        "",
        "### Chaves candidatas (linhas repetidas por combinação)",
        "",
    ]
    linhas_chave = [
        [p["arquivo"], " + ".join(k["colunas"]), k["linhas_repetidas"]]
        for p in perfis
        for k in p["chaves"]
    ]
    partes += [_tabela(["Arquivo", "Combinação", "Linhas repetidas"], linhas_chave), ""]

    partes += ["### Domínios e tamanhos por arquivo", ""]
    for p in perfis:
        partes += [f"**{p['arquivo']}**", ""]
        partes += ["- Colunas: " + ", ".join(f"`{c}` (máx. {p['tamanho_max'].get(c, 0)})" for c in p["colunas"])]
        for coluna, valores in p["dominios"].items():
            partes += [f"- `{coluna}`: " + "; ".join(f"{v or '(vazio)'} = {n}" for v, n in valores.items())]
        if p["vazios"]:
            partes += ["- Vazios: " + ", ".join(f"`{c}` = {n}" for c, n in p["vazios"].items())]
        partes += [""]
    return partes


def gerar_relatorio(cadastro: dict | None, zips: dict[str, list[dict]]) -> str:
    partes = ["# Diagnóstico para a modelagem do banco", ""]
    if cadastro:
        partes += [
            "## 1. CNPJs repetidos entre as linhas ativas do cadastro",
            "",
            f"- Linhas ativas: **{cadastro['linhas_ativas']}**",
            f"- CNPJs ativos distintos: **{cadastro['cnpjs_ativos']}**",
            f"- CNPJs com mais de uma linha ativa: **{cadastro['cnpjs_repetidos']}** "
            f"({cadastro['linhas_excedentes']} linhas excedentes)",
            f"- Grupos em que todas as colunas são idênticas: {cadastro['grupos_totalmente_identicos']}",
            f"- Códigos CVM associados a mais de um CNPJ ativo: {cadastro['cd_cvm_em_mais_de_um_cnpj']}",
            "",
            "### Linhas por CNPJ repetido",
            "",
            _tabela(["Linhas no grupo", "CNPJs"], [[k, v] for k, v in cadastro["tamanho_dos_grupos"].items()]),
            "",
            "### Colunas em que as linhas repetidas diferem",
            "",
            _tabela(["Coluna", "Grupos em que difere"], [[k, v] for k, v in cadastro["colunas_divergentes"].items()]),
            "",
            "### Exemplos",
            "",
        ]
        for exemplo in cadastro["exemplos"]:
            partes += [f"- **{exemplo['denominacao']}** ({exemplo['linhas']} linhas)"]
            for coluna, valores in exemplo["diferencas"].items():
                partes += [f"  - `{coluna}`: " + " | ".join(v or "(vazio)" for v in valores)]
        partes += [""]
    for titulo, perfis in zips.items():
        partes += _secao_zip(titulo, perfis)
    return "\n".join(partes)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Diagnóstico para a modelagem do banco")
    parser.add_argument("--bruto", type=Path, default=Path("data/raw/discovery"))
    parser.add_argument("--saida", type=Path, default=Path("docs/discovery"))
    parser.add_argument("--ano-dfp", type=int, default=2025)
    parser.add_argument("--ano-itr", type=int, default=2026)
    args = parser.parse_args(argv)

    caminho_cad = args.bruto / "cad_cia_aberta.csv"
    cadastro = diagnosticar_cadastro(caminho_cad) if caminho_cad.exists() else None

    zips: dict[str, list[dict]] = {}
    for numero, (tipo, ano) in enumerate((("dfp", args.ano_dfp), ("itr", args.ano_itr)), start=2):
        caminho = args.bruto / f"{tipo}_cia_aberta_{ano}.zip"
        if caminho.exists():
            print(f"Perfilando {caminho.name}...")
            zips[f"{numero}. Estrutura do {tipo.upper()} de {ano}"] = diagnosticar_zip(caminho)

    args.saida.mkdir(parents=True, exist_ok=True)
    destino = args.saida / "diagnostico_modelagem.md"
    destino.write_text(gerar_relatorio(cadastro, zips), encoding="utf-8")
    print(f"Diagnóstico gravado em {destino}")
    return 0 if cadastro else 1


if __name__ == "__main__":
    sys.exit(main())
