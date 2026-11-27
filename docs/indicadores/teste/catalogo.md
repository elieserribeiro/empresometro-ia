# Catálogo de indicadores

Fórmulas usadas no cálculo. Os valores vêm das demonstrações padronizadas da CVM, na versão vigente de cada documento,
com o balanço consolidado quando existe e o individual nos demais casos. Em ROE, ROA e ROIC o denominador é a média
entre o saldo do fim do período e o de um ano antes. Cada indicador é calculado para o exercício anual e para os
últimos 12 meses a cada trimestre. Quando não é possível calcular, o banco registra o motivo: não se aplica ao tipo
de companhia, dado ausente ou denominador zero ou negativo.

## Valores de base

| Indicador | Código | Unidade | Fórmula | Aplica-se a | Observação |
|---|---|---|---|---|---|
| Receita líquida | `RECEITA_LIQUIDA` | R$ | DRE 3.01 (receita de venda de bens e serviços; em bancos, receitas de intermediação financeira) | comum, banco, seguradora | - |
| Lucro bruto | `LUCRO_BRUTO` | R$ | DRE 3.03 (resultado bruto) | comum, seguradora | - |
| EBIT (resultado operacional) | `EBIT` | R$ | DRE: resultado antes do resultado financeiro e dos tributos | comum, seguradora | - |
| EBITDA | `EBITDA` | R$ | EBIT + depreciação, amortização e exaustão (DVA 7.04.01) | comum | Calculado pelas contas padronizadas; pode diferir do EBITDA ajustado divulgado pela companhia. |
| Lucro líquido | `LUCRO_LIQUIDO` | R$ | DRE: lucro ou prejuízo do período (consolidado, quando houver) | comum, banco, seguradora | - |
| Ativo total | `ATIVO_TOTAL` | R$ | Balanço: conta 1 | comum, banco, seguradora | - |
| Patrimônio líquido | `PATRIMONIO_LIQUIDO` | R$ | Balanço: patrimônio líquido (consolidado, quando houver) | comum, banco, seguradora | - |
| Caixa e aplicações financeiras | `CAIXA_E_APLICACOES` | R$ | Caixa e equivalentes (1.01.01) + aplicações financeiras de curto prazo (1.01.02) | comum | - |

## Rentabilidade

| Indicador | Código | Unidade | Fórmula | Aplica-se a | Observação |
|---|---|---|---|---|---|
| Margem bruta | `MARGEM_BRUTA` | % | Lucro bruto / receita líquida | comum, seguradora | - |
| Margem EBITDA | `MARGEM_EBITDA` | % | EBITDA / receita líquida | comum | - |
| Margem EBIT | `MARGEM_EBIT` | % | EBIT / receita líquida | comum, seguradora | - |
| Margem líquida | `MARGEM_LIQUIDA` | % | Lucro líquido / receita líquida | comum, banco, seguradora | - |
| ROE (retorno sobre o patrimônio) | `ROE` | % | Lucro líquido / patrimônio líquido médio do período | comum, banco, seguradora | Não calculado quando o patrimônio médio é zero ou negativo. |
| ROA (retorno sobre o ativo) | `ROA` | % | Lucro líquido / ativo total médio do período | comum, banco, seguradora | - |
| ROIC (retorno sobre o capital investido) | `ROIC` | % | EBIT x (1 - 34%) / capital investido médio; capital investido = patrimônio líquido + dívida bruta - caixa e aplicações | comum | Usa a alíquota nominal de 34% de imposto de renda e contribuição social. |

## Crescimento

| Indicador | Código | Unidade | Fórmula | Aplica-se a | Observação |
|---|---|---|---|---|---|
| Crescimento da receita | `CRESCIMENTO_RECEITA` | % | Receita líquida do período / receita líquida do período anterior - 1 | comum, banco, seguradora | No período de 12 meses, compara com os 12 meses encerrados um ano antes. |
| Crescimento do lucro líquido | `CRESCIMENTO_LUCRO` | % | Lucro líquido do período / lucro líquido do período anterior - 1 | comum, banco, seguradora | Não calculado quando o lucro do período anterior é zero ou negativo. |
| Crescimento do patrimônio líquido | `CRESCIMENTO_PATRIMONIO` | % | Patrimônio líquido final / patrimônio líquido um ano antes - 1 | comum, banco, seguradora | - |
| CAGR da receita na janela | `CAGR_RECEITA` | % | (Receita do último exercício / receita do primeiro exercício disponível) ^ (1 / anos) - 1 | comum, banco, seguradora | Somente no período anual, registrado no último exercício; exige ao menos dois exercícios com receita positiva. |

## Endividamento

| Indicador | Código | Unidade | Fórmula | Aplica-se a | Observação |
|---|---|---|---|---|---|
| Dívida bruta | `DIVIDA_BRUTA` | R$ | Empréstimos e financiamentos de curto prazo (2.01.04) + de longo prazo (2.02.01) | comum | Inclui debêntures e arrendamentos, que a CVM classifica nessas contas. |
| Dívida líquida | `DIVIDA_LIQUIDA` | R$ | Dívida bruta - caixa e aplicações financeiras | comum | - |
| Dívida líquida / EBITDA | `DIVIDA_LIQUIDA_EBITDA` | x | Dívida líquida / EBITDA | comum | Não calculado quando o EBITDA é zero ou negativo. |
| Dívida líquida / patrimônio líquido | `DIVIDA_LIQUIDA_PL` | x | Dívida líquida / patrimônio líquido | comum | - |
| Cobertura de juros | `COBERTURA_JUROS` | x | EBIT / despesas financeiras (DRE 3.06.02, em valor absoluto) | comum | Usa as despesas financeiras brutas, que incluem variação cambial e derivativos; tende a ficar abaixo da cobertura calculada só com juros. |
| Endividamento geral | `ENDIVIDAMENTO_GERAL` | % | (Passivo total - patrimônio líquido) / ativo total | comum, banco, seguradora | - |

## Liquidez e caixa

| Indicador | Código | Unidade | Fórmula | Aplica-se a | Observação |
|---|---|---|---|---|---|
| Liquidez corrente | `LIQUIDEZ_CORRENTE` | x | Ativo circulante / passivo circulante | comum, seguradora | - |
| Liquidez seca | `LIQUIDEZ_SECA` | x | (Ativo circulante - estoques) / passivo circulante | comum | - |
| Liquidez imediata | `LIQUIDEZ_IMEDIATA` | x | Caixa e aplicações / passivo circulante | comum | - |
| Capital de giro | `CAPITAL_DE_GIRO` | R$ | Ativo circulante - passivo circulante | comum, seguradora | - |
| Fluxo de caixa operacional | `FLUXO_CAIXA_OPERACIONAL` | R$ | DFC 6.01 (caixa líquido das atividades operacionais) | comum, seguradora | - |
| Fluxo de caixa livre simplificado | `FLUXO_CAIXA_LIVRE` | R$ | Caixa das atividades operacionais (6.01) + caixa das atividades de investimento (6.02) | comum | Aproximação: o investimento em imobilizado não tem conta padronizada na CVM, então usa-se todo o caixa de investimento. |
| Conversão de caixa | `CONVERSAO_DE_CAIXA` | % | Fluxo de caixa operacional / EBITDA | comum | Não calculado quando o EBITDA é zero ou negativo. |

## Bancos

| Indicador | Código | Unidade | Fórmula | Aplica-se a | Observação |
|---|---|---|---|---|---|
| Resultado bruto da intermediação financeira | `RESULTADO_INTERMEDIACAO` | R$ | DRE 3.03 | banco | - |
| Margem de intermediação | `MARGEM_INTERMEDIACAO` | % | Resultado bruto da intermediação / receitas de intermediação financeira | banco | - |
| Índice de eficiência | `INDICE_EFICIENCIA` | % | (Despesas de pessoal + outras despesas administrativas) / (resultado bruto da intermediação + receitas de prestação de serviços) | banco | Quanto menor, mais eficiente. Calculado pelas contas padronizadas; pode diferir do índice divulgado pelo banco. |
| Alavancagem | `ALAVANCAGEM` | x | Ativo total / patrimônio líquido | banco | - |

## Bancos: capital e crédito

| Indicador | Código | Unidade | Fórmula | Aplica-se a | Observação |
|---|---|---|---|---|---|
| Índice de Basileia | `INDICE_BASILEIA` | % | Patrimônio de referência / ativos ponderados pelo risco (IF.data, conta 79664) | banco | Fonte: IF.data do Banco Central, conglomerado prudencial. Valor na data-base do trimestre. |
| Índice de capital principal | `INDICE_CAPITAL_PRINCIPAL` | % | Capital principal / ativos ponderados pelo risco (IF.data, conta 79659) | banco | Fonte: IF.data do Banco Central, conglomerado prudencial. |
| Índice de capital nível I | `INDICE_CAPITAL_NIVEL_I` | % | Patrimônio de referência nível I / ativos ponderados pelo risco (IF.data, conta 79660) | banco | Fonte: IF.data do Banco Central, conglomerado prudencial. |
| Razão de alavancagem regulatória | `RAZAO_ALAVANCAGEM` | % | Patrimônio de referência nível I / exposição total (IF.data, conta 79661) | banco | Fonte: IF.data do Banco Central, conglomerado prudencial. |
| Inadimplência da carteira de crédito | `INADIMPLENCIA` | % | Operações inadimplentes / total da carteira de crédito (IF.data, contas 148834 e 24454) | banco | Fonte: IF.data do Banco Central. Disponível somente a partir de março de 2025, quando o relatório passou a ser publicado. |
| Ativos problemáticos | `ATIVOS_PROBLEMATICOS` | % | Ativos problemáticos / total da carteira de crédito (IF.data, contas 148833 e 24454) | banco | Fonte: IF.data do Banco Central. Disponível somente a partir de março de 2025. |
