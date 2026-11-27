"""Carga das séries macroeconômicas do Banco Central (SGS) e do IBGE (SIDRA)."""

from __future__ import annotations

import datetime as dt
import json
import time
import urllib.request
from decimal import Decimal, InvalidOperation

import psycopg

from .fontes import USER_AGENT
from .relatorio import _tabela

ANO_INICIAL_PADRAO = 2016

# (código SGS, nome, unidade, periodicidade)
SERIES_SGS = [
    (432, "Taxa Selic: meta definida pelo Copom", "% a.a.", "diária"),
    (4189, "Taxa Selic acumulada no mês, anualizada", "% a.a.", "mensal"),
    (4391, "CDI acumulado no mês", "% a.m.", "mensal"),
    (433, "IPCA: variação mensal", "% a.m.", "mensal"),
    (13522, "IPCA: acumulado em 12 meses", "% em 12 meses", "mensal"),
    (188, "INPC: variação mensal", "% a.m.", "mensal"),
    (189, "IGP-M: variação mensal", "% a.m.", "mensal"),
    (13521, "Meta para a inflação", "% a.a.", "anual"),
    (1, "Dólar comercial (venda), Ptax", "R$/US$", "diária"),
    (3698, "Dólar comercial (venda), média mensal", "R$/US$", "mensal"),
    (21619, "Euro (venda), Ptax", "R$/EUR", "diária"),
    (4380, "PIB mensal em valores correntes", "R$ milhões", "mensal"),
    (24363, "IBC-Br: índice de atividade econômica", "índice", "mensal"),
    (24364, "IBC-Br com ajuste sazonal", "índice", "mensal"),
    (21859, "Produção industrial geral", "índice", "mensal"),
    (1455, "Volume de vendas no varejo", "índice", "mensal"),
    (24369, "Taxa de desocupação (PNAD Contínua)", "%", "mensal"),
    (20539, "Saldo da carteira de crédito total", "R$ milhões", "mensal"),
    (20714, "Taxa média de juros das operações de crédito", "% a.a.", "mensal"),
    (21082, "Inadimplência da carteira de crédito total", "%", "mensal"),
    (21083, "Inadimplência da carteira de crédito: pessoas jurídicas", "%", "mensal"),
    (21084, "Inadimplência da carteira de crédito: pessoas físicas", "%", "mensal"),
]

# (código interno, nome, unidade, periodicidade, caminho da API SIDRA)
SERIES_SIDRA = [
    ("5932/6561/90707", "PIB: variação real contra o mesmo trimestre do ano anterior", "%",
     "trimestral", "t/5932/n1/all/v/6561/p/all/c11255/90707"),
    ("6381/4099", "Taxa de desocupação: trimestre móvel (IBGE)", "%", "mensal",
     "t/6381/n1/all/v/4099/p/all"),
]


def _obter_json(url: str, tentativas: int = 3, timeout: int = 90):
    ultimo_erro: Exception | None = None
    for tentativa in range(1, tentativas + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as erro:  # noqa: BLE001
            ultimo_erro = erro
            if tentativa < tentativas:
                time.sleep(3 * tentativa)
    raise RuntimeError(f"{type(ultimo_erro).__name__}: {ultimo_erro}")


def _decimal(texto) -> Decimal | None:
    try:
        return Decimal(str(texto).strip().replace(",", "."))
    except (InvalidOperation, AttributeError):
        return None


def interpretar_sgs(registros: list[dict]) -> list[tuple[dt.date, Decimal]]:
    """Converte a resposta do SGS ({"data": "dd/mm/aaaa", "valor": "x"}) em pares (data, valor)."""
    pontos = []
    for registro in registros:
        valor = _decimal(registro.get("valor"))
        try:
            data = dt.datetime.strptime(registro.get("data", ""), "%d/%m/%Y").date()
        except ValueError:
            continue
        if valor is not None:
            pontos.append((data, valor))
    return pontos


def buscar_sgs(codigo: int, inicio: dt.date, fim: dt.date) -> list[tuple[dt.date, Decimal]]:
    """Consulta o SGS em janelas de cinco anos (a API limita o período por requisição)."""
    pontos: dict[dt.date, Decimal] = {}
    ano = inicio.year
    while ano <= fim.year:
        de = max(inicio, dt.date(ano, 1, 1))
        ate = min(fim, dt.date(ano + 4, 12, 31))
        url = (
            f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json"
            f"&dataInicial={de:%d/%m/%Y}&dataFinal={ate:%d/%m/%Y}"
        )
        pontos.update(interpretar_sgs(_obter_json(url)))
        ano += 5
    return sorted(pontos.items())


def interpretar_sidra(registros: list[dict], periodicidade: str) -> list[tuple[dt.date, Decimal]]:
    """Converte a resposta do SIDRA em pares (data, valor).

    A primeira linha traz os nomes das colunas; o período vem como AAAAMM
    (mês ou trimestre móvel) ou AAAATT (trimestre).
    """
    if len(registros) < 2:
        return []
    cabecalho = registros[0]
    chave_periodo = next(
        (
            k for k, nome in cabecalho.items()
            if nome.endswith("(Código)") and any(p in nome for p in ("Mês", "Trimestre", "Ano"))
        ),
        None,
    )
    if chave_periodo is None:
        return []
    pontos = []
    for registro in registros[1:]:
        codigo = str(registro.get(chave_periodo, ""))
        valor = _decimal(registro.get("V"))
        if valor is None or len(codigo) != 6 or not codigo.isdigit():
            continue
        ano, parte = int(codigo[:4]), int(codigo[4:])
        mes = parte * 3 if periodicidade == "trimestral" else parte
        if 1 <= mes <= 12:
            pontos.append((dt.date(ano, mes, 1), valor))
    return sorted(pontos)


def gravar_serie(
    conn: psycopg.Connection, fonte: str, codigo: str, nome: str, unidade: str,
    periodicidade: str, pontos: list[tuple[dt.date, Decimal]],
) -> None:
    with conn.transaction(), conn.cursor() as cur:
        serie_id = cur.execute(
            """
            INSERT INTO serie_macro (fonte, codigo, nome, unidade, periodicidade)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT ON CONSTRAINT uq_serie_macro_fonte_codigo
            DO UPDATE SET nome = EXCLUDED.nome, unidade = EXCLUDED.unidade,
                          periodicidade = EXCLUDED.periodicidade
            RETURNING id
            """,
            (fonte, codigo, nome, unidade, periodicidade),
        ).fetchone()[0]
        cur.execute("DELETE FROM serie_macro_valor WHERE serie_id = %s", (serie_id,))
        with cur.copy("COPY serie_macro_valor (serie_id, data, valor) FROM STDIN") as copia:
            for data, valor in pontos:
                copia.write_row((serie_id, data, valor))


def carregar_macro(
    conn: psycopg.Connection, ano_inicial: int = ANO_INICIAL_PADRAO, registrar=print
) -> list[dict]:
    """Carrega todas as séries; uma falha em uma série não interrompe as demais."""
    inicio, fim = dt.date(ano_inicial, 1, 1), dt.date.today()
    eventos = []

    def processar(fonte, codigo, nome, unidade, periodicidade, buscar):
        try:
            pontos = [p for p in buscar() if p[0] >= inicio]
            if not pontos:
                raise RuntimeError("nenhum valor retornado")
            gravar_serie(conn, fonte, codigo, nome, unidade, periodicidade, pontos)
            eventos.append({"fonte": fonte, "codigo": codigo, "nome": nome, "ok": True, "pontos": len(pontos)})
        except Exception as erro:  # noqa: BLE001
            registrar(f"Série {fonte} {codigo} ({nome}) não carregada: {erro}")
            eventos.append({"fonte": fonte, "codigo": codigo, "nome": nome, "ok": False, "erro": str(erro)[:200]})

    for codigo, nome, unidade, periodicidade in SERIES_SGS:
        processar("BCB SGS", str(codigo), nome, unidade, periodicidade,
                  lambda c=codigo: buscar_sgs(c, inicio, fim))
    for codigo, nome, unidade, periodicidade, caminho in SERIES_SIDRA:
        processar("IBGE SIDRA", codigo, nome, unidade, periodicidade,
                  lambda c=caminho, p=periodicidade: interpretar_sidra(
                      _obter_json(f"https://apisidra.ibge.gov.br/values/{c}"), p))
    carregadas = sum(1 for e in eventos if e["ok"])
    registrar(f"Séries macroeconômicas: {carregadas} de {len(eventos)} carregadas")
    return eventos


def gerar_relatorio_macro(conn: psycopg.Connection, eventos: list[dict] | None = None) -> str:
    cur = conn.cursor()
    partes = [
        "# Séries macroeconômicas",
        "",
        _tabela(
            ["Fonte", "Código", "Série", "Unidade", "Periodicidade", "Valores", "Primeira data", "Última data", "Último valor"],
            cur.execute(
                """
                SELECT s.fonte, s.codigo, s.nome, s.unidade, s.periodicidade,
                       count(v.*), min(v.data), max(v.data),
                       (SELECT trim_scale(u.valor) FROM serie_macro_valor u
                        WHERE u.serie_id = s.id ORDER BY u.data DESC LIMIT 1)
                FROM serie_macro s LEFT JOIN serie_macro_valor v ON v.serie_id = s.id
                GROUP BY s.id ORDER BY s.fonte, s.id
                """
            ).fetchall(),
        ),
        "",
    ]
    # Conferência cruzada: a média mensal publicada deve bater com a média da série diária.
    conferencia = cur.execute(
        """
        SELECT to_char(m.data, 'YYYY-MM'), trim_scale(m.valor),
               (SELECT round(avg(d.valor), 4) FROM serie_macro_valor d
                WHERE d.serie_id = sd.id AND date_trunc('month', d.data) = m.data)
        FROM serie_macro sm
        JOIN serie_macro_valor m ON m.serie_id = sm.id
        JOIN serie_macro sd ON sd.fonte = 'BCB SGS' AND sd.codigo = '1'
        WHERE sm.fonte = 'BCB SGS' AND sm.codigo = '3698'
        ORDER BY m.data DESC LIMIT 3
        """
    ).fetchall()
    if conferencia:
        partes += [
            "## Conferência do dólar",
            "",
            _tabela(["Mês", "Média mensal publicada (série 3698)", "Média calculada da série diária (série 1)"], conferencia),
            "",
        ]
    falhas = [e for e in (eventos or []) if not e["ok"]]
    if falhas:
        partes += [
            "## Séries não carregadas nesta execução",
            "",
            _tabela(["Fonte", "Código", "Série", "Erro"], [[e["fonte"], e["codigo"], e["nome"], e["erro"]] for e in falhas]),
            "",
        ]
    return "\n".join(partes)
