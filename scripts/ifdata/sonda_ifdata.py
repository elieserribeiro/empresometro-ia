"""Sonda do IF.data (Banco Central): descobre relatórios, campos e nomes das contas.

Consulta a API OData do IF.data e registra a estrutura do que volta, para
definir como obter o índice de Basileia e a inadimplência dos bancos.
"""

from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

BASE = "https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata"
ANO_MES = int(sys.argv[1]) if len(sys.argv) > 1 else 202506


def obter(caminho: str, **parametros) -> tuple[list, str]:
    consulta = urllib.parse.urlencode({"$format": "json", **parametros}, quote_via=urllib.parse.quote)
    url = f"{BASE}/{caminho}?{consulta}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "empresometro-ia/1.0", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=180) as resp:
            return json.loads(resp.read().decode("utf-8")).get("value", []), url
    except Exception as erro:  # noqa: BLE001
        corpo = ""
        if hasattr(erro, "read"):
            corpo = erro.read()[:300].decode("utf-8", "replace")
        return [{"ERRO": f"{type(erro).__name__}: {erro} {corpo}"}], url


def main() -> int:
    saida = [f"# Sonda do IF.data (data-base {ANO_MES})", ""]

    relatorios, url = obter("ListaDeRelatorio()")
    saida += ["## Relatórios disponíveis", "", f"`{url}`", ""]
    saida += [f"- {json.dumps(r, ensure_ascii=False)}" for r in relatorios[:60]]

    cadastro, url = obter(f"IfDataCadastro(AnoMes=@AnoMes)", **{"@AnoMes": ANO_MES, "$top": 5000})
    saida += ["", "## Cadastro", "", f"`{url}`", "", f"{len(cadastro)} linhas."]
    if cadastro and "ERRO" not in cadastro[0]:
        saida += ["", "Campos: " + ", ".join(f"`{c}`" for c in cadastro[0])]
        for campo in cadastro[0]:
            valores = Counter(str(l.get(campo)) for l in cadastro)
            if len(valores) <= 12:
                saida += [f"- `{campo}`: " + "; ".join(f"{v} = {n}" for v, n in valores.most_common())]
        for nome in ("ITAU", "BRASIL", "BRADESCO", "BTG"):
            achados = [l for l in cadastro if nome in str(l.get("NomeInstituicao", "")).upper()][:4]
            saida += [f"- Exemplo {nome}: {json.dumps(a, ensure_ascii=False)}" for a in achados]
    else:
        saida += [f"- {cadastro[:1]}"]

    codigos = [str(r.get("NumeroRelatorio") or r.get("Relatorio") or r.get("Codigo")) for r in relatorios if "ERRO" not in r]
    for tipo in (1, 2, 3):
        for relatorio in (codigos or ["1", "5"])[:20]:
            valores, url = obter(
                "IfDataValores(AnoMes=@AnoMes,TipoInstituicao=@TipoInstituicao,Relatorio=@Relatorio)",
                **{"@AnoMes": ANO_MES, "@TipoInstituicao": tipo, "@Relatorio": f"'{relatorio}'", "$top": 100000},
            )
            if not valores or "ERRO" in valores[0]:
                saida += ["", f"## Tipo {tipo}, relatório {relatorio}: sem dados ({(valores or [{}])[0].get('ERRO', 'vazio')[:160]})"]
                continue
            contas = Counter((str(v.get("NomeColuna")), str(v.get("Grupo")), str(v.get("Conta"))) for v in valores)
            instituicoes = {v.get("CodInst") for v in valores}
            saida += [
                "", f"## Tipo de instituição {tipo}, relatório {relatorio}", "",
                f"{len(valores)} valores, {len(instituicoes)} instituições, {len(contas)} colunas.",
                "Campos: " + ", ".join(f"`{c}`" for c in valores[0]),
                f"Exemplo: {json.dumps(valores[0], ensure_ascii=False)}", "", "Colunas (nome | grupo | conta | linhas):",
            ]
            saida += [f"- {nome} | {grupo} | {conta} | {n}" for (nome, grupo, conta), n in contas.most_common(80)]

    destino = Path("docs/discovery/sonda_ifdata.md")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(saida), encoding="utf-8")
    print("\n".join(saida)[:6000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
