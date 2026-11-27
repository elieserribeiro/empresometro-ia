"""Catálogo dos indicadores: nome, grupo, unidade, fórmula e a que tipo de companhia se aplica.

Planos de contas da CVM:
- COMUM: companhias comerciais, industriais e de serviços;
- BANCO: instituições financeiras;
- SEGURADORA: seguradoras e resseguradoras.
"""

from __future__ import annotations

from dataclasses import dataclass

TODOS = ("COMUM", "BANCO", "SEGURADORA")
COMUM = ("COMUM",)
COMUM_E_SEGURADORA = ("COMUM", "SEGURADORA")
BANCO = ("BANCO",)
ALIQUOTA_NOMINAL = "34%"


@dataclass(frozen=True)
class Definicao:
    codigo: str
    nome: str
    grupo: str
    unidade: str  # 'R$', '%' ou 'x'
    formula: str
    aplica_a: tuple[str, ...]
    observacao: str | None = None
    fonte: str = "CVM"  # "IFDATA" para os índices regulatórios do Banco Central


CATALOGO: list[Definicao] = [
    # Valores de base
    Definicao("RECEITA_LIQUIDA", "Receita líquida", "Valores de base", "R$",
              "DRE 3.01 (receita de venda de bens e serviços; em bancos, receitas de intermediação financeira)", TODOS),
    Definicao("LUCRO_BRUTO", "Lucro bruto", "Valores de base", "R$", "DRE 3.03 (resultado bruto)", COMUM_E_SEGURADORA),
    Definicao("EBIT", "EBIT (resultado operacional)", "Valores de base", "R$",
              "DRE: resultado antes do resultado financeiro e dos tributos", COMUM_E_SEGURADORA),
    Definicao("EBITDA", "EBITDA", "Valores de base", "R$",
              "EBIT + depreciação, amortização e exaustão (DVA 7.04.01)", COMUM,
              "Calculado pelas contas padronizadas; pode diferir do EBITDA ajustado divulgado pela companhia."),
    Definicao("LUCRO_LIQUIDO", "Lucro líquido", "Valores de base", "R$",
              "DRE: lucro ou prejuízo do período (consolidado, quando houver)", TODOS),
    Definicao("ATIVO_TOTAL", "Ativo total", "Valores de base", "R$", "Balanço: conta 1", TODOS),
    Definicao("PATRIMONIO_LIQUIDO", "Patrimônio líquido", "Valores de base", "R$",
              "Balanço: patrimônio líquido (consolidado, quando houver)", TODOS),
    Definicao("CAIXA_E_APLICACOES", "Caixa e aplicações financeiras", "Valores de base", "R$",
              "Caixa e equivalentes (1.01.01) + aplicações financeiras de curto prazo (1.01.02)", COMUM),
    # Rentabilidade
    Definicao("MARGEM_BRUTA", "Margem bruta", "Rentabilidade", "%", "Lucro bruto / receita líquida", COMUM_E_SEGURADORA),
    Definicao("MARGEM_EBITDA", "Margem EBITDA", "Rentabilidade", "%", "EBITDA / receita líquida", COMUM),
    Definicao("MARGEM_EBIT", "Margem EBIT", "Rentabilidade", "%", "EBIT / receita líquida", COMUM_E_SEGURADORA),
    Definicao("MARGEM_LIQUIDA", "Margem líquida", "Rentabilidade", "%", "Lucro líquido / receita líquida", TODOS),
    Definicao("ROE", "ROE (retorno sobre o patrimônio)", "Rentabilidade", "%",
              "Lucro líquido / patrimônio líquido médio do período", TODOS,
              "Não calculado quando o patrimônio médio é zero ou negativo."),
    Definicao("ROA", "ROA (retorno sobre o ativo)", "Rentabilidade", "%",
              "Lucro líquido / ativo total médio do período", TODOS),
    Definicao("ROIC", "ROIC (retorno sobre o capital investido)", "Rentabilidade", "%",
              f"EBIT x (1 - {ALIQUOTA_NOMINAL}) / capital investido médio; capital investido = patrimônio líquido + dívida bruta - caixa e aplicações",
              COMUM, f"Usa a alíquota nominal de {ALIQUOTA_NOMINAL} de imposto de renda e contribuição social."),
    # Crescimento
    Definicao("CRESCIMENTO_RECEITA", "Crescimento da receita", "Crescimento", "%",
              "Receita líquida do período / receita líquida do período anterior - 1", TODOS,
              "No período de 12 meses, compara com os 12 meses encerrados um ano antes."),
    Definicao("CRESCIMENTO_LUCRO", "Crescimento do lucro líquido", "Crescimento", "%",
              "Lucro líquido do período / lucro líquido do período anterior - 1", TODOS,
              "Não calculado quando o lucro do período anterior é zero ou negativo."),
    Definicao("CRESCIMENTO_PATRIMONIO", "Crescimento do patrimônio líquido", "Crescimento", "%",
              "Patrimônio líquido final / patrimônio líquido um ano antes - 1", TODOS),
    Definicao("CAGR_RECEITA", "CAGR da receita na janela", "Crescimento", "%",
              "(Receita do último exercício / receita do primeiro exercício disponível) ^ (1 / anos) - 1", TODOS,
              "Somente no período anual, registrado no último exercício; exige ao menos dois exercícios com receita positiva."),
    # Endividamento
    Definicao("DIVIDA_BRUTA", "Dívida bruta", "Endividamento", "R$",
              "Empréstimos e financiamentos de curto prazo (2.01.04) + de longo prazo (2.02.01)", COMUM,
              "Inclui debêntures e arrendamentos, que a CVM classifica nessas contas."),
    Definicao("DIVIDA_LIQUIDA", "Dívida líquida", "Endividamento", "R$", "Dívida bruta - caixa e aplicações financeiras", COMUM),
    Definicao("DIVIDA_LIQUIDA_EBITDA", "Dívida líquida / EBITDA", "Endividamento", "x", "Dívida líquida / EBITDA", COMUM,
              "Não calculado quando o EBITDA é zero ou negativo."),
    Definicao("DIVIDA_LIQUIDA_PL", "Dívida líquida / patrimônio líquido", "Endividamento", "x",
              "Dívida líquida / patrimônio líquido", COMUM),
    Definicao("COBERTURA_JUROS", "Cobertura de juros", "Endividamento", "x",
              "EBIT / despesas financeiras (DRE 3.06.02, em valor absoluto)", COMUM,
              "Usa as despesas financeiras brutas, que incluem variação cambial e derivativos; tende a ficar abaixo da cobertura calculada só com juros."),
    Definicao("ENDIVIDAMENTO_GERAL", "Endividamento geral", "Endividamento", "%",
              "(Passivo total - patrimônio líquido) / ativo total", TODOS),
    # Liquidez e caixa
    Definicao("LIQUIDEZ_CORRENTE", "Liquidez corrente", "Liquidez e caixa", "x", "Ativo circulante / passivo circulante", COMUM_E_SEGURADORA),
    Definicao("LIQUIDEZ_SECA", "Liquidez seca", "Liquidez e caixa", "x", "(Ativo circulante - estoques) / passivo circulante", COMUM),
    Definicao("LIQUIDEZ_IMEDIATA", "Liquidez imediata", "Liquidez e caixa", "x", "Caixa e aplicações / passivo circulante", COMUM),
    Definicao("CAPITAL_DE_GIRO", "Capital de giro", "Liquidez e caixa", "R$", "Ativo circulante - passivo circulante", COMUM_E_SEGURADORA),
    Definicao("FLUXO_CAIXA_OPERACIONAL", "Fluxo de caixa operacional", "Liquidez e caixa", "R$",
              "DFC 6.01 (caixa líquido das atividades operacionais)", COMUM_E_SEGURADORA),
    Definicao("FLUXO_CAIXA_LIVRE", "Fluxo de caixa livre simplificado", "Liquidez e caixa", "R$",
              "Caixa das atividades operacionais (6.01) + caixa das atividades de investimento (6.02)", COMUM,
              "Aproximação: o investimento em imobilizado não tem conta padronizada na CVM, então usa-se todo o caixa de investimento."),
    Definicao("CONVERSAO_DE_CAIXA", "Conversão de caixa", "Liquidez e caixa", "%",
              "Fluxo de caixa operacional / EBITDA", COMUM, "Não calculado quando o EBITDA é zero ou negativo."),
    # Bancos
    Definicao("RESULTADO_INTERMEDIACAO", "Resultado bruto da intermediação financeira", "Bancos", "R$", "DRE 3.03", BANCO),
    Definicao("MARGEM_INTERMEDIACAO", "Margem de intermediação", "Bancos", "%",
              "Resultado bruto da intermediação / receitas de intermediação financeira", BANCO),
    Definicao("INDICE_EFICIENCIA", "Índice de eficiência", "Bancos", "%",
              "(Despesas de pessoal + outras despesas administrativas) / (resultado bruto da intermediação + receitas de prestação de serviços)",
              BANCO, "Quanto menor, mais eficiente. Calculado pelas contas padronizadas; pode diferir do índice divulgado pelo banco."),
    Definicao("ALAVANCAGEM", "Alavancagem", "Bancos", "x", "Ativo total / patrimônio líquido", BANCO),
    # Bancos: capital regulatório e qualidade do crédito (IF.data do Banco Central, conglomerado prudencial)
    Definicao("INDICE_BASILEIA", "Índice de Basileia", "Bancos: capital e crédito", "%",
              "Patrimônio de referência / ativos ponderados pelo risco (IF.data, conta 79664)", BANCO,
              "Fonte: IF.data do Banco Central, conglomerado prudencial. Valor na data-base do trimestre.", "IFDATA"),
    Definicao("INDICE_CAPITAL_PRINCIPAL", "Índice de capital principal", "Bancos: capital e crédito", "%",
              "Capital principal / ativos ponderados pelo risco (IF.data, conta 79659)", BANCO,
              "Fonte: IF.data do Banco Central, conglomerado prudencial.", "IFDATA"),
    Definicao("INDICE_CAPITAL_NIVEL_I", "Índice de capital nível I", "Bancos: capital e crédito", "%",
              "Patrimônio de referência nível I / ativos ponderados pelo risco (IF.data, conta 79660)", BANCO,
              "Fonte: IF.data do Banco Central, conglomerado prudencial.", "IFDATA"),
    Definicao("RAZAO_ALAVANCAGEM", "Razão de alavancagem regulatória", "Bancos: capital e crédito", "%",
              "Patrimônio de referência nível I / exposição total (IF.data, conta 79661)", BANCO,
              "Fonte: IF.data do Banco Central, conglomerado prudencial.", "IFDATA"),
    Definicao("INADIMPLENCIA", "Inadimplência da carteira de crédito", "Bancos: capital e crédito", "%",
              "Operações inadimplentes / total da carteira de crédito (IF.data, contas 148834 e 24454)", BANCO,
              "Fonte: IF.data do Banco Central. Disponível somente a partir de março de 2025, quando o relatório passou a ser publicado.",
              "IFDATA"),
    Definicao("ATIVOS_PROBLEMATICOS", "Ativos problemáticos", "Bancos: capital e crédito", "%",
              "Ativos problemáticos / total da carteira de crédito (IF.data, contas 148833 e 24454)", BANCO,
              "Fonte: IF.data do Banco Central. Disponível somente a partir de março de 2025.", "IFDATA"),
]
CODIGOS_IFDATA = [d.codigo for d in CATALOGO if d.fonte == "IFDATA"]

POR_CODIGO = {d.codigo: d for d in CATALOGO}
