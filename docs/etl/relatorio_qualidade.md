# Relatório de qualidade dos dados

## Alertas por tipo

| Tipo | O que significa | Alertas |
|---|---|---|
| BALANCO_NAO_FECHA | Ativo total diferente do passivo total no documento vigente | 26 |
| CONTA_REPETIDA_COM_VALORES_DIFERENTES | Mesma conta repetida no documento com valores diferentes | 29 |
| HISTORICO_INCOMPLETO | Companhia ativa sem demonstração anual em parte dos exercícios | 83 |
| SEM_DFP_NA_JANELA | Companhia ativa sem nenhuma demonstração anual na janela | 14 |
| VIGENTE_SEM_LINHAS | Documento vigente sem linhas de demonstração | 3 |
| FORA_DO_CADASTRO | Companhia presente nos documentos e ausente do cadastro da CVM | 10 |

## Balanços em que ativo e passivo não coincidem

| Companhia | Documento | Referência | Diferença (R$) | Detalhe |
|---|---|---|---|---|
| CESP - COMPANHIA ENERGÉTICA DE SÃO PAULO | ITR | 2022-06-30 | 14440481000.00 | Consolidado: ativo total R$ 14,440,481,000.00, passivo total R$ 0.00. Diferença relevante, sem causa identificada automaticamente. |
| ORIZON MEIO AMBIENTE S.A. | ITR | 2022-06-30 | -2305890000.00 | Individual: ativo total R$ 0.00, passivo total R$ 2,305,890,000.00. Diferença relevante, sem causa identificada automaticamente. |
| ORIZON MEIO AMBIENTE S.A. | ITR | 2022-06-30 | -2295293000.00 | Consolidado: ativo total R$ 0.00, passivo total R$ 2,295,293,000.00. Diferença relevante, sem causa identificada automaticamente. |
| BRBI BR PARTNERS S.A | ITR | 2021-06-30 | 1424966000.00 | Consolidado: ativo total R$ 1,424,966,000.00, passivo total R$ 0.00. Diferença relevante, sem causa identificada automaticamente. |
| HOLDING VERZANI & SANDRINI S.A. | ITR | 2021-03-31 | 970637000.00 | Consolidado: ativo total R$ 970,637,000.00, passivo total R$ 0.00. Diferença relevante, sem causa identificada automaticamente. |
| HOLDING VERZANI & SANDRINI S.A. | ITR | 2021-06-30 | 956729000.00 | Consolidado: ativo total R$ 956,729,000.00, passivo total R$ 0.00. Diferença relevante, sem causa identificada automaticamente. |
| ORIZON MEIO AMBIENTE S.A. | ITR | 2022-03-31 | -853761000.00 | Individual: ativo total R$ 844,394,000.00, passivo total R$ 1,698,155,000.00. Diferença relevante, sem causa identificada automaticamente. |
| ITAPEBI GERAÇÃO DE ENERGIA S/A | DFP | 2021-12-31 | 369675000.00 | Individual: ativo total R$ 699,798,000.00, passivo total R$ 330,123,000.00. Diferença relevante, sem causa identificada automaticamente. |
| BRAZILIAN FINANCE & REAL ESTATE S.A. | ITR | 2022-06-30 | -191577000.00 | Individual: ativo total R$ 17,921,000.00, passivo total R$ 209,498,000.00. Diferença relevante, sem causa identificada automaticamente. |
| BRAZILIAN FINANCE & REAL ESTATE S.A. | ITR | 2022-03-31 | -150529000.00 | Consolidado: ativo total R$ 60,280,000.00, passivo total R$ 210,809,000.00. Diferença relevante, sem causa identificada automaticamente. |
| BRAZILIAN FINANCE & REAL ESTATE S.A. | ITR | 2022-03-31 | -148763000.00 | Individual: ativo total R$ 57,216,000.00, passivo total R$ 205,979,000.00. Diferença relevante, sem causa identificada automaticamente. |
| BOMBRIL S.A. - EM RECUPERAÇÃO JUDICIAL | ITR | 2022-06-30 | -120849000.00 | Individual: ativo total R$ 857,363,000.00, passivo total R$ 978,212,000.00. Diferença relevante, sem causa identificada automaticamente. |
| DATORA PARTICIPAÇÕES E SERVIÇOS S/A | DFP | 2021-12-31 | -28000.00 | Individual: ativo total R$ 127,906,000.00, passivo total R$ 127,934,000.00. Diferença relevante, sem causa identificada automaticamente. |
| RGE SUL DISTRIBUIDORA DE ENERGIA S.A. | DFP | 2021-12-31 | 1000.00 | Individual: ativo total R$ 15,479,988,000.00, passivo total R$ 15,479,987,000.00. Causa provável: arredondamento (diferença de até mil reais). |
| SYN PROP & TECH S.A. | DFP | 2022-12-31 | -1000.00 | Consolidado: ativo total R$ 4,075,077,000.00, passivo total R$ 4,075,078,000.00. Causa provável: arredondamento (diferença de até mil reais). |
| COMPANHIA  MELHORAMENTOS DE SÃO PAULO | ITR | 2021-06-30 | -1000.00 | Consolidado: ativo total R$ 1,385,365,000.00, passivo total R$ 1,385,366,000.00. Causa provável: arredondamento (diferença de até mil reais). |
| GAFISA SA | ITR | 2022-06-30 | -1000.00 | Individual: ativo total R$ 3,437,375,000.00, passivo total R$ 3,437,376,000.00. Causa provável: arredondamento (diferença de até mil reais). |
| COMPANHIA  MELHORAMENTOS DE SÃO PAULO | ITR | 2022-06-30 | 1000.00 | Individual: ativo total R$ 1,361,582,000.00, passivo total R$ 1,361,581,000.00. Causa provável: arredondamento (diferença de até mil reais). |
| COMPANHIA  MELHORAMENTOS DE SÃO PAULO | ITR | 2022-09-30 | 500.00 | Consolidado: ativo total R$ 1,415,441,000.00, passivo total R$ 1,415,440,500.00. Causa provável: arredondamento (diferença de até mil reais). |
| BANCO MODAL S.A. | DFP | 2022-12-31 | 330.00 | Consolidado: ativo total R$ 7,673,331,330.00, passivo total R$ 7,673,331,000.00. Causa provável: arredondamento (diferença de até mil reais). |
| PET CENTER COMÉRCIO E PARTICIPAÇÕES S.A. | ITR | 2025-09-30 | 133.61 | Consolidado: ativo total R$ 3,944,594,133.61, passivo total R$ 3,944,594,000.00. Causa provável: arredondamento (diferença de até mil reais). |
| TERMOPERNAMBUCO SA | ITR | 2022-06-30 | 81.22 | Individual: ativo total R$ 2,420,867,000.00, passivo total R$ 2,420,866,918.78. Causa provável: arredondamento (diferença de até mil reais). |
| CERRADINHO BIOENERGIA S.A. | ITR | 2025-12-31 | -80.00 | Individual: ativo total R$ 5,739,899,000.00, passivo total R$ 5,739,899,080.00. Causa provável: arredondamento (diferença de até mil reais). |
| TERMOPERNAMBUCO SA | ITR | 2022-09-30 | -59.00 | Individual: ativo total R$ 2,411,410,000.00, passivo total R$ 2,411,410,059.00. Causa provável: arredondamento (diferença de até mil reais). |
| ALLIED TECNOLOGIA S.A. | ITR | 2022-03-31 | -45.29 | Individual: ativo total R$ 3,874,769,000.00, passivo total R$ 3,874,769,045.29. Causa provável: arredondamento (diferença de até mil reais). |
| VIVARA PARTICIPAÇÕES S.A. | ITR | 2022-09-30 | 2.00 | Consolidado: ativo total R$ 2,679,775,949.00, passivo total R$ 2,679,775,947.00. Causa provável: arredondamento (diferença de até mil reais). |

## Companhias ativas com histórico anual incompleto

| Exercícios faltantes | Companhias |
|---|---|
| 1 | 22 |
| 2 | 32 |
| 3 | 17 |
| 4 | 12 |
| 5 | 14 |

## Documentos com mais contas repetidas com valores diferentes

| Companhia | Documento | Referência | Contas |
|---|---|---|---|
| BRASIL TECNOLOGIA E PARTICIPAÇÕES S.A. | DFP | 2023-12-31 | 137 |
| BRASIL TERRENOS HOLDING S.A. | DFP | 2025-12-31 | 112 |
| BRASIL TERRENOS HOLDING S.A. | ITR | 2026-03-31 | 108 |
| ENGELHART CTP (BRASIL) S.A. | DFP | 2023-12-31 | 94 |
| BRASIL BIOFUELS S.A. - EM RECUPERAÇÃO JUDICIAL | ITR | 2023-03-31 | 63 |
| PRODUTORES ENERGET.DE MANSO S.A.- PROMAN | ITR | 2021-06-30 | 55 |
| ATOM EDUCAÇÃO E EDITORA S.A. | ITR | 2024-03-31 | 48 |
| BRASIL BIOFUELS S.A. - EM RECUPERAÇÃO JUDICIAL | ITR | 2023-06-30 | 48 |
| BRASIL BIOFUELS S.A. - EM RECUPERAÇÃO JUDICIAL | ITR | 2023-09-30 | 36 |
| ATOM EDUCAÇÃO E EDITORA S.A. | ITR | 2024-06-30 | 30 |
| ENERGISA MINAS RIO - DISTRIBUIDORA DE ENERGIA S/A | ITR | 2021-06-30 | 18 |
| BRASIL TERRENOS HOLDING S.A. | ITR | 2026-06-30 | 16 |
| CONCESSIONARIA ROTA DE SANTA MARIA S.A | DFP | 2022-12-31 | 16 |
| REVEE MCO S.A. | DFP | 2023-12-31 | 13 |
| AUTOMOB PARTICIPAÇÕES S.A. | DFP | 2023-12-31 | 12 |
| BRADSAÚDE S.A. | DFP | 2023-12-31 | 12 |
| CIA. SECURITIZADORA DE CRED. FIN. VERT-UME | ITR | 2021-06-30 | 11 |
| RIO ALTO ENERGIAS RENOVÁVEIS S.A. - EM RECUPERAÇÃO JUDICIAL | DFP | 2022-12-31 | 11 |
| METALFRIO SOLUTIONS S/A | ITR | 2021-06-30 | 10 |
| RIO ALTO ENERGIAS RENOVÁVEIS S.A. - EM RECUPERAÇÃO JUDICIAL | ITR | 2022-09-30 | 8 |
