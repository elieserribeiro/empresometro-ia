"""Cálculo determinístico dos indicadores a partir das bases padronizadas.

Todas as funções são puras: recebem dicionários de valores (Decimal ou None)
e devolvem, para cada indicador, o valor ou o motivo de não ter sido calculado.
"""

from __future__ import annotations

from decimal import Decimal

from .catalogo import CATALOGO

NAO_SE_APLICA = "NAO_SE_APLICA"
DADO_AUSENTE = "DADO_AUSENTE"
DENOMINADOR_INVALIDO = "DENOMINADOR_INVALIDO"

CEM = Decimal(100)
UM_MENOS_ALIQUOTA = Decimal("0.66")

Resultado = tuple[Decimal | None, str | None]


def _soma(*valores: Decimal | None) -> Decimal | None:
    """Soma que exige todos os termos presentes."""
    if any(v is None for v in valores):
        return None
    return sum(valores, Decimal(0))


def _media(atual: Decimal | None, anterior: Decimal | None) -> Decimal | None:
    if atual is None or anterior is None:
        return None
    return (atual + anterior) / 2


def _razao(numerador, denominador, fator: Decimal = Decimal(1), exige_positivo: bool = True) -> Resultado:
    if numerador is None or denominador is None:
        return None, DADO_AUSENTE
    if denominador == 0 or (exige_positivo and denominador < 0):
        return None, DENOMINADOR_INVALIDO
    return numerador / denominador * fator, None


def _valor(v: Decimal | None) -> Resultado:
    return (v, None) if v is not None else (None, DADO_AUSENTE)


def _crescimento(atual, anterior) -> Resultado:
    if atual is None or anterior is None:
        return None, DADO_AUSENTE
    if anterior <= 0:
        return None, DENOMINADOR_INVALIDO
    return (atual / anterior - 1) * CEM, None


def somar_fluxos(a: dict | None, b: dict | None, c: dict | None) -> dict | None:
    """Últimos 12 meses: acumulado do ano + exercício anterior completo - acumulado do ano anterior."""
    if a is None or b is None or c is None:
        return None
    campos = set(a) | set(b) | set(c)
    saida = {}
    for campo in campos:
        x, y, z = a.get(campo), b.get(campo), c.get(campo)
        saida[campo] = None if (x is None or y is None or z is None) else x + y - z
    return saida


def calcular(
    plano: str,
    fluxo: dict | None,
    saldo: dict | None,
    saldo_anterior: dict | None,
    fluxo_anterior: dict | None,
) -> dict[str, Resultado]:
    """Calcula todos os indicadores de um período para uma companhia.

    `fluxo` e `fluxo_anterior`: resultados e fluxos de caixa do período e do período um ano antes.
    `saldo` e `saldo_anterior`: balanço no fim do período e um ano antes.
    """
    f = fluxo or {}
    s = saldo or {}
    sa = saldo_anterior or {}
    fa = fluxo_anterior or {}
    g = f.get
    comum = plano == "COMUM"

    receita, lucro, ebit = g("receita"), g("lucro_liquido"), g("ebit")
    depreciacao = g("depreciacao")
    ebitda = None if ebit is None or depreciacao is None else ebit + abs(depreciacao)
    pl, ativo = s.get("patrimonio_liquido"), s.get("ativo_total")

    def caixa_e_aplicacoes(b: dict) -> Decimal | None:
        if b.get("caixa") is None:
            return None
        return b["caixa"] + (b.get("aplicacoes") or Decimal(0))

    def divida_bruta(b: dict) -> Decimal | None:
        return _soma(b.get("emprestimos_cp"), b.get("emprestimos_lp"))

    def capital_investido(b: dict) -> Decimal | None:
        divida, caixa = divida_bruta(b), caixa_e_aplicacoes(b)
        if b.get("patrimonio_liquido") is None or divida is None or caixa is None:
            return None
        return b["patrimonio_liquido"] + divida - caixa

    caixa = caixa_e_aplicacoes(s)
    bruta = divida_bruta(s)
    liquida = None if bruta is None or caixa is None else bruta - caixa
    ac, pc = s.get("ativo_circulante"), s.get("passivo_circulante")
    fco, fci = g("fco"), g("fci")
    despesas_fin = g("despesas_financeiras")

    r: dict[str, Resultado] = {
        "RECEITA_LIQUIDA": _valor(receita),
        "LUCRO_BRUTO": _valor(g("resultado_bruto")),
        "EBIT": _valor(ebit),
        "EBITDA": _valor(ebitda),
        "LUCRO_LIQUIDO": _valor(lucro),
        "ATIVO_TOTAL": _valor(ativo),
        "PATRIMONIO_LIQUIDO": _valor(pl),
        "CAIXA_E_APLICACOES": _valor(caixa),
        "MARGEM_BRUTA": _razao(g("resultado_bruto"), receita, CEM),
        "MARGEM_EBITDA": _razao(ebitda, receita, CEM),
        "MARGEM_EBIT": _razao(ebit, receita, CEM),
        "MARGEM_LIQUIDA": _razao(lucro, receita, CEM),
        "ROE": _razao(lucro, _media(pl, sa.get("patrimonio_liquido")), CEM),
        "ROA": _razao(lucro, _media(ativo, sa.get("ativo_total")), CEM),
        "ROIC": _razao(
            None if ebit is None else ebit * UM_MENOS_ALIQUOTA,
            _media(capital_investido(s), capital_investido(sa)), CEM,
        ),
        "CRESCIMENTO_RECEITA": _crescimento(receita, fa.get("receita")),
        "CRESCIMENTO_LUCRO": _crescimento(lucro, fa.get("lucro_liquido")),
        "CRESCIMENTO_PATRIMONIO": _crescimento(pl, sa.get("patrimonio_liquido")),
        "DIVIDA_BRUTA": _valor(bruta),
        "DIVIDA_LIQUIDA": _valor(liquida),
        "DIVIDA_LIQUIDA_EBITDA": _razao(liquida, ebitda),
        "DIVIDA_LIQUIDA_PL": _razao(liquida, pl),
        "COBERTURA_JUROS": _razao(ebit, None if despesas_fin is None else abs(despesas_fin)),
        "ENDIVIDAMENTO_GERAL": _razao(
            None if s.get("passivo_total") is None or pl is None else s["passivo_total"] - pl, ativo, CEM
        ),
        "LIQUIDEZ_CORRENTE": _razao(ac, pc),
        "LIQUIDEZ_SECA": _razao(
            None if ac is None else ac - (s.get("estoques") or Decimal(0)), pc
        ),
        "LIQUIDEZ_IMEDIATA": _razao(caixa, pc),
        "CAPITAL_DE_GIRO": _valor(None if ac is None or pc is None else ac - pc),
        "FLUXO_CAIXA_OPERACIONAL": _valor(fco),
        "FLUXO_CAIXA_LIVRE": _valor(_soma(fco, fci)),
        "CONVERSAO_DE_CAIXA": _razao(fco, ebitda, CEM),
        "RESULTADO_INTERMEDIACAO": _valor(g("resultado_bruto")),
        "MARGEM_INTERMEDIACAO": _razao(g("resultado_bruto"), receita, CEM),
        "INDICE_EFICIENCIA": _razao(
            None
            if g("banco_pessoal") is None or g("banco_administrativas") is None
            else abs(g("banco_pessoal")) + abs(g("banco_administrativas")),
            None
            if g("resultado_bruto") is None
            else g("resultado_bruto") + (g("banco_servicos") or Decimal(0)),
            CEM,
        ),
        "ALAVANCAGEM": _razao(ativo, pl),
    }

    saida: dict[str, Resultado] = {}
    for definicao in CATALOGO:
        if definicao.codigo == "CAGR_RECEITA":
            continue  # calculado à parte, com todos os exercícios da companhia
        if plano not in definicao.aplica_a:
            saida[definicao.codigo] = (None, NAO_SE_APLICA)
        elif definicao.fonte == "CVM":
            saida[definicao.codigo] = r[definicao.codigo]
        # Indicadores de outras fontes (IF.data) são gravados depois, direto no banco.
    return saida


def cagr(primeiro: Decimal | None, ultimo: Decimal | None, anos: int) -> Resultado:
    """Taxa composta de crescimento anual entre dois exercícios."""
    if primeiro is None or ultimo is None or anos < 1:
        return None, DADO_AUSENTE
    if primeiro <= 0 or ultimo <= 0:
        return None, DENOMINADOR_INVALIDO
    taxa = (float(ultimo) / float(primeiro)) ** (1 / anos) - 1
    return Decimal(str(round(taxa * 100, 6))), None
