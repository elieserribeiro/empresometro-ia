# Relatório de qualidade dos dados

## Alertas por tipo

| Tipo | O que significa | Alertas |
|---|---|---|
| BALANCO_NAO_FECHA | Ativo total diferente do passivo total no documento vigente | 0 |
| CONTA_REPETIDA_COM_VALORES_DIFERENTES | Mesma conta repetida no documento com valores diferentes | 4 |
| HISTORICO_INCOMPLETO | Companhia ativa sem demonstração anual em parte dos exercícios | 0 |
| SEM_DFP_NA_JANELA | Companhia ativa sem nenhuma demonstração anual na janela | 17 |
| VIGENTE_SEM_LINHAS | Documento vigente sem linhas de demonstração | 2 |
| FORA_DO_CADASTRO | Companhia presente nos documentos e ausente do cadastro da CVM | 5 |

## Balanços em que ativo e passivo não coincidem

Nenhum caso.

## Companhias ativas com histórico anual incompleto

| Exercícios faltantes | Companhias |
|---|---|
| 1 | 17 |

## Documentos com mais contas repetidas com valores diferentes

| Companhia | Documento | Referência | Contas |
|---|---|---|---|
| BRASIL TERRENOS HOLDING S.A. | DFP | 2025-12-31 | 112 |
| BRASIL TERRENOS HOLDING S.A. | ITR | 2026-03-31 | 108 |
| BRASIL TERRENOS HOLDING S.A. | ITR | 2026-06-30 | 16 |
| BANCO VOTORANTIM S.A. | DFP | 2025-12-31 | 5 |
