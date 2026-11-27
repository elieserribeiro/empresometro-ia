"""Carga do IF.data (Banco Central): índices de capital e inadimplência dos bancos.

O IF.data publica, por trimestre, dados dos conglomerados prudenciais. A
correspondência com a CVM é feita pela raiz do CNPJ (8 primeiros dígitos):
a companhia é a própria instituição ou a líder do conglomerado.
"""

from __future__ import annotations

import calendar
import datetime as dt
import json
import time
import urllib.parse
import urllib.request
from decimal import Decimal, InvalidOperation

import psycopg

from .fontes import USER_AGENT
from .relatorio import _tabela

BASE = "https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata"
CONGLOMERADO_PRUDENCIAL = 1

# Contas de interesse: relatório -> {conta: nome}
CONTAS = {
    "5": {
        "79664": "Índice de Basileia",
        "79659": "Índice de Capital Principal",
        "79660": "Índice de Capital Nível I",
        "79661": "Razão de Alavancagem",
        "79649": "Patrimônio de Referência",
        "79665": "Ativos Ponderados pelo Risco (RWA)",
    },
    "16": {
        "148834": "Inadimplência",
        "148833": "Ativos problemáticos",
        "24454": "Carteira de crédito: total geral",
    },
}


def consultar(caminho: str, **parametros) -> list[dict]:
    consulta = urllib.parse.urlencode({"$format": "json", **parametros}, quote_via=urllib.parse.quote)
    ultimo_erro: Exception | None = None
    for tentativa in range(3):
        try:
            req = urllib.request.Request(
                f"{BASE}/{caminho}?{consulta}", headers={"User-Agent": USER_AGENT, "Accept": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=240) as resp:
                return json.loads(resp.read().decode("utf-8")).get("value", [])
        except Exception as erro:  # noqa: BLE001
            ultimo_erro = erro
            time.sleep(5 * (tentativa + 1))
    raise RuntimeError(f"IF.data indisponível: {type(ultimo_erro).__name__}: {ultimo_erro}")


def datas_base(ano_inicial: int, hoje: dt.date | None = None) -> list[int]:
    """Fins de trimestre, no formato AAAAMM, de dezembro do ano anterior ao inicial até hoje."""
    hoje = hoje or dt.date.today()
    datas = [(ano_inicial - 1) * 100 + 12]
    for ano in range(ano_inicial, hoje.year + 1):
        for mes in (3, 6, 9, 12):
            if dt.date(ano, mes, calendar.monthrange(ano, mes)[1]) <= hoje:
                datas.append(ano * 100 + mes)
    return datas


def fim_do_mes(ano_mes: int) -> dt.date:
    ano, mes = divmod(ano_mes, 100)
    return dt.date(ano, mes, calendar.monthrange(ano, mes)[1])


def corresponder(companhias: list[tuple[int, str]], cadastro: list[dict]) -> list[dict]:
    """Liga cada companhia da CVM (id, cnpj) ao código usado no IF.data para o conglomerado prudencial.

    Critérios, pela raiz do CNPJ: líder de conglomerado; instituição pertencente a
    um conglomerado; instituição independente (o próprio código é a raiz do CNPJ).
    """
    por_lider: dict[str, dict] = {}
    por_instituicao: dict[str, dict] = {}
    for linha in cadastro:
        if str(linha.get("Situacao") or "").strip() != "A":
            continue
        lider = str(linha.get("CnpjInstituicaoLider") or "").strip().zfill(8)
        codigo = str(linha.get("CodInst") or "").strip()
        if linha.get("CodConglomeradoPrudencial") and lider.strip("0"):
            por_lider.setdefault(lider, linha)
        if codigo.isdigit():
            por_instituicao.setdefault(codigo.zfill(8), linha)

    pares = []
    for companhia_id, cnpj in companhias:
        raiz = (cnpj or "")[:8]
        if raiz in por_lider:
            linha, criterio = por_lider[raiz], "LIDER_DO_CONGLOMERADO"
            codigo = linha["CodConglomeradoPrudencial"]
        elif raiz in por_instituicao:
            linha = por_instituicao[raiz]
            if linha.get("CodConglomeradoPrudencial"):
                codigo, criterio = linha["CodConglomeradoPrudencial"], "INSTITUICAO_DO_CONGLOMERADO"
            else:
                codigo, criterio = raiz, "INSTITUICAO_INDEPENDENTE"
        else:
            continue
        pares.append(
            {"companhia_id": companhia_id, "cod_inst": str(codigo).strip(),
             "nome": str(linha.get("NomeInstituicao") or "")[:200], "criterio": criterio}
        )
    return pares


def _decimal(valor) -> Decimal | None:
    try:
        return None if valor is None else Decimal(str(valor))
    except InvalidOperation:
        return None


def carregar_ifdata(conn: psycopg.Connection, ano_inicial: int = 2021, registrar=print) -> dict:
    """Atualiza a correspondência com a CVM e carrega os valores de todos os trimestres disponíveis."""
    datas = datas_base(ano_inicial)
    cadastro: list[dict] = []
    for data in reversed(datas):  # o cadastro mais recente que existir
        cadastro = consultar("IfDataCadastro(AnoMes=@AnoMes)", **{"@AnoMes": data, "$top": 20000})
        if cadastro:
            registrar(f"IF.data: cadastro de {data} com {len(cadastro)} instituições.")
            break
    if not cadastro:
        raise RuntimeError("IF.data: nenhum cadastro encontrado.")

    companhias = conn.execute("SELECT id, cnpj FROM companhia").fetchall()
    pares = corresponder(companhias, cadastro)
    codigos = {p["cod_inst"] for p in pares}
    with conn.transaction(), conn.cursor() as cur:
        cur.execute("TRUNCATE companhia_ifdata")
        cur.executemany(
            "INSERT INTO companhia_ifdata (companhia_id, cod_inst, nome_ifdata, criterio) VALUES (%s, %s, %s, %s)",
            [(p["companhia_id"], p["cod_inst"], p["nome"], p["criterio"]) for p in pares],
        )
    registrar(f"IF.data: {len(pares)} companhias da CVM correspondidas.")

    total = 0
    datas_com_dados = []
    for data in datas:
        linhas: dict[tuple, tuple] = {}
        for relatorio, contas in CONTAS.items():
            valores = consultar(
                "IfDataValores(AnoMes=@AnoMes,TipoInstituicao=@TipoInstituicao,Relatorio=@Relatorio)",
                **{"@AnoMes": data, "@TipoInstituicao": CONGLOMERADO_PRUDENCIAL, "@Relatorio": f"'{relatorio}'",
                   "$top": 500000},
            )
            for v in valores:
                codigo, conta = str(v.get("CodInst") or "").strip(), str(v.get("Conta") or "").strip()
                if codigo in codigos and conta in contas:
                    linhas[(codigo, conta)] = (codigo, fim_do_mes(data), conta, relatorio, contas[conta], _decimal(v.get("Saldo")))
        if not linhas:
            continue
        datas_com_dados.append(data)
        with conn.transaction(), conn.cursor() as cur:
            cur.execute("DELETE FROM ifdata_valor WHERE data_base = %s", (fim_do_mes(data),))
            cur.executemany(
                "INSERT INTO ifdata_valor (cod_inst, data_base, conta, relatorio, nome_coluna, saldo) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                list(linhas.values()),
            )
        total += len(linhas)
    resumo = {
        "companhias_correspondidas": len(pares), "datas_com_dados": len(datas_com_dados),
        "primeira_data": datas_com_dados[0] if datas_com_dados else None,
        "ultima_data": datas_com_dados[-1] if datas_com_dados else None, "valores": total,
    }
    registrar(f"IF.data: {resumo}")
    return resumo


def gerar_relatorio_ifdata(conn: psycopg.Connection) -> str:
    cur = conn.cursor()
    return "\n".join(
        [
            "# IF.data: índices de capital e inadimplência dos bancos",
            "",
            "Fonte: IF.data do Banco Central, conglomerados prudenciais. Índices em percentual.",
            "",
            "## Cobertura por data-base",
            "",
            _tabela(
                ["Data-base", "Instituições com Basileia", "Instituições com inadimplência"],
                cur.execute(
                    """
                    SELECT data_base, count(*) FILTER (WHERE conta = '79664' AND saldo IS NOT NULL),
                           count(*) FILTER (WHERE conta = '148834' AND saldo IS NOT NULL)
                    FROM ifdata_valor GROUP BY 1 ORDER BY 1
                    """
                ).fetchall(),
            ),
            "",
            "## Companhias correspondidas, na data-base mais recente",
            "",
            _tabela(
                ["Companhia (CVM)", "Nome no IF.data", "Código", "Critério", "Basileia %", "Capital principal %",
                 "Inadimplência %", "Ativos problemáticos %"],
                cur.execute(
                    """
                    WITH ultima AS (SELECT max(data_base) d FROM ifdata_valor WHERE conta = '79664')
                    SELECT c.denominacao, m.nome_ifdata, m.cod_inst, m.criterio,
                           round(max(v.saldo) FILTER (WHERE v.conta = '79664') * 100, 2),
                           round(max(v.saldo) FILTER (WHERE v.conta = '79659') * 100, 2),
                           round(max(v.saldo) FILTER (WHERE v.conta = '148834')
                                 / nullif(max(v.saldo) FILTER (WHERE v.conta = '24454'), 0) * 100, 2),
                           round(max(v.saldo) FILTER (WHERE v.conta = '148833')
                                 / nullif(max(v.saldo) FILTER (WHERE v.conta = '24454'), 0) * 100, 2)
                    FROM companhia_ifdata m JOIN companhia c ON c.id = m.companhia_id
                    LEFT JOIN ultima u ON true
                    LEFT JOIN ifdata_valor v ON v.cod_inst = m.cod_inst AND v.data_base = u.d
                    GROUP BY c.denominacao, m.nome_ifdata, m.cod_inst, m.criterio ORDER BY 1
                    """
                ).fetchall(),
            ),
            "",
        ]
    )
