# Diagnóstico para a modelagem do banco

## 1. CNPJs repetidos entre as linhas ativas do cadastro

- Linhas ativas: **748**
- CNPJs ativos distintos: **655**
- CNPJs com mais de uma linha ativa: **89** (93 linhas excedentes)
- Grupos em que todas as colunas são idênticas: 0
- Códigos CVM associados a mais de um CNPJ ativo: 0

### Linhas por CNPJ repetido

| Linhas no grupo | CNPJs |
|---|---|
| 2 | 85 |
| 3 | 4 |

### Colunas em que as linhas repetidas diferem

| Coluna | Grupos em que difere |
|---|---|
| TP_MERC | 89 |

### Exemplos

- **ARMAC LOCAÇÃO, LOGÍSTICA E SERVIÇOS S.A.** (2 linhas)
  - `TP_MERC`: BALCÃO ORGANIZADO | BOLSA
- **AMERICANAS S.A. - EM RECUPERAÇÃO JUDICIAL** (2 linhas)
  - `TP_MERC`: BALCÃO ORGANIZADO | BOLSA
- **CONCESSIONARIA RIO-TERESOPOLIS SA** (2 linhas)
  - `TP_MERC`: BALCÃO ORGANIZADO | BOLSA
- **BBM LOGÍSTICA S.A.** (2 linhas)
  - `TP_MERC`: BALCÃO ORGANIZADO | BOLSA
- **CIA DE PARTICIPAÇÕES ALIANÇA DA BAHIA** (2 linhas)
  - `TP_MERC`: BALCÃO ORGANIZADO | BOLSA
- **RUMO S.A.** (2 linhas)
  - `TP_MERC`: BALCÃO ORGANIZADO | BOLSA
- **CPFL ENERGIA SA** (2 linhas)
  - `TP_MERC`: BALCÃO ORGANIZADO | BOLSA
- **CONCESSIONÁRIA DO SISTEMA ANHANGUERA-BANDEIRANTES S.A.** (2 linhas)
  - `TP_MERC`: BALCÃO ORGANIZADO | BOLSA

## 2. Estrutura do DFP de 2025

| Arquivo | Linhas | Contas distintas | Níveis de conta | Colunas |
|---|---|---|---|---|
| dfp_cia_aberta_2025.csv | 763 | - | - | 9 |
| dfp_cia_aberta_BPA_con_2025.csv | 60334 | 282 | 1: 898, 2: 1946, 3: 11058, 4: 23576, 5: 22856 | 14 |
| dfp_cia_aberta_BPA_ind_2025.csv | 90063 | 334 | 1: 1346, 2: 2902, 3: 16696, 4: 34286, 5: 34833 | 14 |
| dfp_cia_aberta_BPP_con_2025.csv | 103164 | 353 | 1: 898, 2: 2822, 3: 19516, 4: 40498, 5: 39430 | 14 |
| dfp_cia_aberta_BPP_ind_2025.csv | 152034 | 393 | 1: 1346, 2: 4208, 3: 28322, 4: 60552, 5: 57606 | 14 |
| dfp_cia_aberta_composicao_capital_2025.csv | 673 | - | - | 10 |
| dfp_cia_aberta_DFC_MD_con_2025.csv | 558 | 47 | 2: 160, 3: 398 | 15 |
| dfp_cia_aberta_DFC_MD_ind_2025.csv | 800 | 57 | 2: 240, 3: 560 | 15 |
| dfp_cia_aberta_DFC_MI_con_2025.csv | 49110 | 108 | 2: 4330, 3: 19098, 4: 25682 | 15 |
| dfp_cia_aberta_DFC_MI_ind_2025.csv | 66129 | 111 | 2: 6490, 3: 25307, 4: 34332 | 15 |
| dfp_cia_aberta_DMPL_con_2025.csv | 229887 | 90 | 2: 50442, 3: 125792, 4: 53653 | 16 |
| dfp_cia_aberta_DMPL_ind_2025.csv | 249985 | 133 | 2: 57302, 3: 134321, 4: 58362 | 16 |
| dfp_cia_aberta_DRA_con_2025.csv | 6684 | 40 | 2: 2716, 3: 3848, 4: 120 | 15 |
| dfp_cia_aberta_DRA_ind_2025.csv | 6836 | 40 | 2: 4078, 3: 2610, 4: 148 | 15 |
| dfp_cia_aberta_DRE_con_2025.csv | 31404 | 202 | 2: 10768, 3: 15440, 4: 5196 | 15 |
| dfp_cia_aberta_DRE_ind_2025.csv | 44011 | 208 | 2: 16170, 3: 20499, 4: 7342 | 15 |
| dfp_cia_aberta_DVA_con_2025.csv | 39386 | 194 | 2: 7226, 3: 16172, 4: 15188, 5: 800 | 15 |
| dfp_cia_aberta_DVA_ind_2025.csv | 56932 | 182 | 2: 10830, 3: 24250, 4: 20794, 5: 1058 | 15 |
| dfp_cia_aberta_parecer_2025.csv | 3761 | - | - | 8 |

### Chaves candidatas (linhas repetidas por combinação)

| Arquivo | Combinação | Linhas repetidas |
|---|---|---|
| dfp_cia_aberta_BPA_con_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 770 |
| dfp_cia_aberta_BPA_ind_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 758 |
| dfp_cia_aberta_BPP_con_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 1252 |
| dfp_cia_aberta_BPP_ind_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 1240 |
| dfp_cia_aberta_DFC_MD_con_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 36 |
| dfp_cia_aberta_DFC_MD_con_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 36 |
| dfp_cia_aberta_DFC_MD_ind_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 28 |
| dfp_cia_aberta_DFC_MD_ind_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 28 |
| dfp_cia_aberta_DFC_MI_con_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 416 |
| dfp_cia_aberta_DFC_MI_con_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 416 |
| dfp_cia_aberta_DFC_MI_ind_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 428 |
| dfp_cia_aberta_DFC_MI_ind_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 428 |
| dfp_cia_aberta_DMPL_con_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 201576 |
| dfp_cia_aberta_DMPL_con_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 201576 |
| dfp_cia_aberta_DMPL_con_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + COLUNA_DF + CD_CONTA | 2804 |
| dfp_cia_aberta_DMPL_ind_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 208903 |
| dfp_cia_aberta_DMPL_ind_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 208903 |
| dfp_cia_aberta_DMPL_ind_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + COLUNA_DF + CD_CONTA | 2141 |
| dfp_cia_aberta_DRA_con_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 90 |
| dfp_cia_aberta_DRA_con_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 90 |
| dfp_cia_aberta_DRA_ind_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 66 |
| dfp_cia_aberta_DRA_ind_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 66 |
| dfp_cia_aberta_DRE_con_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 414 |
| dfp_cia_aberta_DRE_con_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 414 |
| dfp_cia_aberta_DRE_ind_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 392 |
| dfp_cia_aberta_DRE_ind_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 392 |
| dfp_cia_aberta_DVA_con_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 526 |
| dfp_cia_aberta_DVA_con_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 526 |
| dfp_cia_aberta_DVA_ind_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 490 |
| dfp_cia_aberta_DVA_ind_2025.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 490 |

### Domínios e tamanhos por arquivo

**dfp_cia_aberta_2025.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `CATEG_DOC` (máx. 3), `ID_DOC` (máx. 6), `DT_RECEB` (máx. 10), `LINK_DOC` (máx. 117)
- `CATEG_DOC`: DFP = 763

**dfp_cia_aberta_BPA_con_2025.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 42), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 13), `DS_CONTA` (máx. 98), `VL_CONTA` (máx. 21), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Consolidado - Balanço Patrimonial Ativo = 60334
- `MOEDA`: REAL = 60334
- `ESCALA_MOEDA`: MIL = 59076; UNIDADE = 1258
- `ORDEM_EXERC`: PENÚLTIMO = 30167; ÚLTIMO = 30167
- `ST_CONTA_FIXA`: S = 45324; N = 15010

**dfp_cia_aberta_BPA_ind_2025.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 41), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 13), `DS_CONTA` (máx. 98), `VL_CONTA` (máx. 21), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Individual - Balanço Patrimonial Ativo = 90063
- `MOEDA`: REAL = 90063
- `ESCALA_MOEDA`: MIL = 87383; UNIDADE = 2680
- `ORDEM_EXERC`: ÚLTIMO = 45151; PENÚLTIMO = 44912
- `ST_CONTA_FIXA`: S = 69350; N = 20713

**dfp_cia_aberta_BPP_con_2025.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 44), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 13), `DS_CONTA` (máx. 97), `VL_CONTA` (máx. 21), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Consolidado - Balanço Patrimonial Passivo = 103164
- `MOEDA`: REAL = 103164
- `ESCALA_MOEDA`: MIL = 100906; UNIDADE = 2258
- `ORDEM_EXERC`: PENÚLTIMO = 51582; ÚLTIMO = 51582
- `ST_CONTA_FIXA`: S = 87656; N = 15508

**dfp_cia_aberta_BPP_ind_2025.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 43), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 13), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 21), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Individual - Balanço Patrimonial Passivo = 152034
- `MOEDA`: REAL = 152034
- `ESCALA_MOEDA`: MIL = 147290; UNIDADE = 4744
- `ORDEM_EXERC`: ÚLTIMO = 76225; PENÚLTIMO = 75809
- `ST_CONTA_FIXA`: S = 132490; N = 19544

**dfp_cia_aberta_composicao_capital_2025.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `QT_ACAO_ORDIN_CAP_INTEGR` (máx. 13), `QT_ACAO_PREF_CAP_INTEGR` (máx. 13), `QT_ACAO_TOTAL_CAP_INTEGR` (máx. 13), `QT_ACAO_ORDIN_TESOURO` (máx. 10), `QT_ACAO_PREF_TESOURO` (máx. 8), `QT_ACAO_TOTAL_TESOURO` (máx. 10)

**dfp_cia_aberta_DFC_MD_con_2025.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 58), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 63), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 7), `DS_CONTA` (máx. 96), `VL_CONTA` (máx. 20), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Consolidado - Demonstração do Fluxo de Caixa (Método Direto) = 558
- `MOEDA`: REAL = 558
- `ESCALA_MOEDA`: MIL = 516; UNIDADE = 42
- `ORDEM_EXERC`: PENÚLTIMO = 279; ÚLTIMO = 279
- `ST_CONTA_FIXA`: N = 334; S = 224

**dfp_cia_aberta_DFC_MD_ind_2025.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 58), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 62), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 7), `DS_CONTA` (máx. 99), `VL_CONTA` (máx. 20), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Individual - Demonstração do Fluxo de Caixa (Método Direto) = 800
- `MOEDA`: REAL = 800
- `ESCALA_MOEDA`: MIL = 716; UNIDADE = 84
- `ORDEM_EXERC`: PENÚLTIMO = 400; ÚLTIMO = 400
- `ST_CONTA_FIXA`: N = 464; S = 336

**dfp_cia_aberta_DFC_MI_con_2025.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 65), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 10), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 21), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Consolidado - Demonstração do Fluxo de Caixa (Método Indireto) = 49110
- `MOEDA`: REAL = 49110
- `ESCALA_MOEDA`: MIL = 48460; UNIDADE = 650
- `ORDEM_EXERC`: PENÚLTIMO = 24555; ÚLTIMO = 24555
- `ST_CONTA_FIXA`: N = 40406; S = 8704

**dfp_cia_aberta_DFC_MI_ind_2025.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 64), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 10), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 21), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Individual - Demonstração do Fluxo de Caixa (Método Indireto) = 66129
- `MOEDA`: REAL = 66129
- `ESCALA_MOEDA`: MIL = 65053; UNIDADE = 1076
- `ORDEM_EXERC`: ÚLTIMO = 33145; PENÚLTIMO = 32984
- `ST_CONTA_FIXA`: N = 53061; S = 13068

**dfp_cia_aberta_DMPL_con_2025.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 64), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `COLUNA_DF` (máx. 60), `CD_CONTA` (máx. 10), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 21), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Consolidado - Demonstração das Mutações do Patrimônio Líquido = 229887
- `MOEDA`: REAL = 229887
- `ESCALA_MOEDA`: MIL = 225327; UNIDADE = 4560
- `ORDEM_EXERC`: ÚLTIMO = 115570; PENÚLTIMO = 114317
- `ST_CONTA_FIXA`: S = 187356; N = 42531
- Vazios: `COLUNA_DF` = 647

**dfp_cia_aberta_DMPL_ind_2025.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 63), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `COLUNA_DF` (máx. 60), `CD_CONTA` (máx. 10), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 21), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Individual - Demonstração das Mutações do Patrimônio Líquido = 249985
- `MOEDA`: REAL = 249985
- `ESCALA_MOEDA`: MIL = 242707; UNIDADE = 7278
- `ORDEM_EXERC`: ÚLTIMO = 125620; PENÚLTIMO = 124365
- `ST_CONTA_FIXA`: S = 210786; N = 39199

**dfp_cia_aberta_DRA_con_2025.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 53), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 10), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 20), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Consolidado - Demonstração de Resultado Abrangente = 6684
- `MOEDA`: REAL = 6684
- `ESCALA_MOEDA`: MIL = 6572; UNIDADE = 112
- `ORDEM_EXERC`: PENÚLTIMO = 3342; ÚLTIMO = 3342
- `ST_CONTA_FIXA`: S = 4608; N = 2076

**dfp_cia_aberta_DRA_ind_2025.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 52), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 10), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 20), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Individual - Demonstração de Resultado Abrangente = 6836
- `MOEDA`: REAL = 6836
- `ESCALA_MOEDA`: MIL = 6692; UNIDADE = 144
- `ORDEM_EXERC`: ÚLTIMO = 3424; PENÚLTIMO = 3412
- `ST_CONTA_FIXA`: S = 4246; N = 2590

**dfp_cia_aberta_DRE_con_2025.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 42), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 10), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 22), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Consolidado - Demonstração do Resultado = 31404
- `MOEDA`: REAL = 31404
- `ESCALA_MOEDA`: MIL = 30734; UNIDADE = 670
- `ORDEM_EXERC`: PENÚLTIMO = 15702; ÚLTIMO = 15702
- `ST_CONTA_FIXA`: S = 22438; N = 8966

**dfp_cia_aberta_DRE_ind_2025.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 41), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 10), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 21), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Individual - Demonstração do Resultado = 44011
- `MOEDA`: REAL = 44011
- `ESCALA_MOEDA`: MIL = 42673; UNIDADE = 1338
- `ORDEM_EXERC`: ÚLTIMO = 22072; PENÚLTIMO = 21939
- `ST_CONTA_FIXA`: S = 30934; N = 13077

**dfp_cia_aberta_DVA_con_2025.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 49), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 13), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 22), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Consolidado - Demonstração de Valor Adicionado = 39386
- `MOEDA`: REAL = 39386
- `ESCALA_MOEDA`: MIL = 38542; UNIDADE = 844
- `ORDEM_EXERC`: PENÚLTIMO = 19693; ÚLTIMO = 19693
- `ST_CONTA_FIXA`: S = 35918; N = 3468

**dfp_cia_aberta_DVA_ind_2025.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 48), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 13), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 21), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Individual - Demonstração de Valor Adicionado = 56932
- `MOEDA`: REAL = 56932
- `ESCALA_MOEDA`: MIL = 55162; UNIDADE = 1770
- `ORDEM_EXERC`: ÚLTIMO = 28549; PENÚLTIMO = 28383
- `ST_CONTA_FIXA`: S = 52472; N = 4460

**dfp_cia_aberta_parecer_2025.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `TP_RELAT_AUD` (máx. 19), `TP_PARECER_DECL` (máx. 101), `NUM_ITEM_PARECER_DECL` (máx. 2), `TXT_PARECER_DECL` (máx. 7996)
- Vazios: `TP_RELAT_AUD` = 2072

## 3. Estrutura do ITR de 2026

| Arquivo | Linhas | Contas distintas | Níveis de conta | Colunas |
|---|---|---|---|---|
| itr_cia_aberta_2026.csv | 1996 | - | - | 9 |
| itr_cia_aberta_BPA_con_2026.csv | 169158 | 275 | 1: 2510, 2: 5390, 3: 30808, 4: 66000, 5: 64450 | 14 |
| itr_cia_aberta_BPA_ind_2026.csv | 255552 | 323 | 1: 3804, 2: 8146, 3: 47062, 4: 96716, 5: 99824 | 14 |
| itr_cia_aberta_BPP_con_2026.csv | 289816 | 357 | 1: 2510, 2: 7854, 3: 54682, 4: 113780, 5: 110990 | 14 |
| itr_cia_aberta_BPP_ind_2026.csv | 432190 | 398 | 1: 3804, 2: 11848, 3: 80018, 4: 171570, 5: 164950 | 14 |
| itr_cia_aberta_composicao_capital_2026.csv | 1905 | - | - | 10 |
| itr_cia_aberta_DFC_MD_con_2026.csv | 1250 | 51 | 2: 390, 3: 860 | 15 |
| itr_cia_aberta_DFC_MD_ind_2026.csv | 1518 | 49 | 2: 540, 3: 978 | 15 |
| itr_cia_aberta_DFC_MI_con_2026.csv | 132010 | 110 | 2: 12160, 3: 49892, 4: 69958 | 15 |
| itr_cia_aberta_DFC_MI_ind_2026.csv | 180358 | 114 | 2: 18480, 3: 67152, 4: 94726 | 15 |
| itr_cia_aberta_DMPL_con_2026.csv | 581749 | 89 | 2: 140882, 3: 302937, 4: 137930 | 16 |
| itr_cia_aberta_DMPL_ind_2026.csv | 647197 | 117 | 2: 161854, 3: 332739, 4: 152604 | 16 |
| itr_cia_aberta_DRA_con_2026.csv | 29980 | 41 | 2: 12550, 3: 16994, 4: 436 | 15 |
| itr_cia_aberta_DRA_ind_2026.csv | 31024 | 42 | 2: 19094, 3: 11260, 4: 670 | 15 |
| itr_cia_aberta_DRE_con_2026.csv | 145214 | 220 | 2: 49844, 3: 71636, 4: 23734 | 15 |
| itr_cia_aberta_DRE_ind_2026.csv | 209702 | 226 | 2: 75782, 3: 97270, 4: 36650 | 15 |
| itr_cia_aberta_DVA_con_2026.csv | 108556 | 195 | 2: 20190, 3: 45208, 4: 41248, 5: 1910 | 15 |
| itr_cia_aberta_DVA_ind_2026.csv | 160082 | 191 | 2: 30598, 3: 68532, 4: 58178, 5: 2774 | 15 |
| itr_cia_aberta_parecer_2026.csv | 6458 | - | - | 8 |

### Chaves candidatas (linhas repetidas por combinação)

| Arquivo | Combinação | Linhas repetidas |
|---|---|---|
| itr_cia_aberta_BPA_con_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 752 |
| itr_cia_aberta_BPA_ind_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 746 |
| itr_cia_aberta_BPP_con_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 1308 |
| itr_cia_aberta_BPP_ind_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 1304 |
| itr_cia_aberta_DFC_MD_con_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 112 |
| itr_cia_aberta_DFC_MD_con_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 112 |
| itr_cia_aberta_DFC_MD_ind_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 122 |
| itr_cia_aberta_DFC_MD_ind_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 122 |
| itr_cia_aberta_DFC_MI_con_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 0 |
| itr_cia_aberta_DFC_MI_con_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 0 |
| itr_cia_aberta_DFC_MI_ind_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 0 |
| itr_cia_aberta_DFC_MI_ind_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 0 |
| itr_cia_aberta_DMPL_con_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 509515 |
| itr_cia_aberta_DMPL_con_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 509515 |
| itr_cia_aberta_DMPL_con_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + COLUNA_DF + CD_CONTA | 2560 |
| itr_cia_aberta_DMPL_ind_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 540221 |
| itr_cia_aberta_DMPL_ind_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 540221 |
| itr_cia_aberta_DMPL_ind_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + COLUNA_DF + CD_CONTA | 1896 |
| itr_cia_aberta_DRA_con_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 11990 |
| itr_cia_aberta_DRA_con_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 80 |
| itr_cia_aberta_DRA_ind_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 12420 |
| itr_cia_aberta_DRA_ind_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 48 |
| itr_cia_aberta_DRE_con_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 58002 |
| itr_cia_aberta_DRE_con_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 468 |
| itr_cia_aberta_DRE_ind_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 83746 |
| itr_cia_aberta_DRE_ind_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 436 |
| itr_cia_aberta_DVA_con_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 482 |
| itr_cia_aberta_DVA_con_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 482 |
| itr_cia_aberta_DVA_ind_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + CD_CONTA | 470 |
| itr_cia_aberta_DVA_ind_2026.csv | CNPJ_CIA + DT_REFER + VERSAO + ORDEM_EXERC + DT_INI_EXERC + CD_CONTA | 470 |

### Domínios e tamanhos por arquivo

**itr_cia_aberta_2026.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `CATEG_DOC` (máx. 3), `ID_DOC` (máx. 6), `DT_RECEB` (máx. 10), `LINK_DOC` (máx. 117)
- `CATEG_DOC`: ITR = 1996

**itr_cia_aberta_BPA_con_2026.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 42), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 13), `DS_CONTA` (máx. 98), `VL_CONTA` (máx. 21), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Consolidado - Balanço Patrimonial Ativo = 169158
- `MOEDA`: REAL = 169158
- `ESCALA_MOEDA`: MIL = 165840; UNIDADE = 3318
- `ORDEM_EXERC`: PENÚLTIMO = 84579; ÚLTIMO = 84579
- `ST_CONTA_FIXA`: S = 126678; N = 42480

**itr_cia_aberta_BPA_ind_2026.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 41), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 13), `DS_CONTA` (máx. 98), `VL_CONTA` (máx. 21), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Individual - Balanço Patrimonial Ativo = 255552
- `MOEDA`: REAL = 255552
- `ESCALA_MOEDA`: MIL = 248480; UNIDADE = 7072
- `ORDEM_EXERC`: PENÚLTIMO = 127776; ÚLTIMO = 127776
- `ST_CONTA_FIXA`: S = 196104; N = 59448

**itr_cia_aberta_BPP_con_2026.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 44), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 13), `DS_CONTA` (máx. 97), `VL_CONTA` (máx. 21), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Consolidado - Balanço Patrimonial Passivo = 289816
- `MOEDA`: REAL = 289816
- `ESCALA_MOEDA`: MIL = 283894; UNIDADE = 5922
- `ORDEM_EXERC`: PENÚLTIMO = 144908; ÚLTIMO = 144908
- `ST_CONTA_FIXA`: S = 245544; N = 44272

**itr_cia_aberta_BPP_ind_2026.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 43), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 13), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 21), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Individual - Balanço Patrimonial Passivo = 432190
- `MOEDA`: REAL = 432190
- `ESCALA_MOEDA`: MIL = 419810; UNIDADE = 12380
- `ORDEM_EXERC`: PENÚLTIMO = 216095; ÚLTIMO = 216095
- `ST_CONTA_FIXA`: S = 375126; N = 57064

**itr_cia_aberta_composicao_capital_2026.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `QT_ACAO_ORDIN_CAP_INTEGR` (máx. 16), `QT_ACAO_PREF_CAP_INTEGR` (máx. 13), `QT_ACAO_TOTAL_CAP_INTEGR` (máx. 16), `QT_ACAO_ORDIN_TESOURO` (máx. 9), `QT_ACAO_PREF_TESOURO` (máx. 8), `QT_ACAO_TOTAL_TESOURO` (máx. 9)

**itr_cia_aberta_DFC_MD_con_2026.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 63), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 7), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 21), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Consolidado - Demonstração do Fluxo de Caixa (Método Direto) = 1250
- `MOEDA`: REAL = 1250
- `ESCALA_MOEDA`: MIL = 1138; UNIDADE = 112
- `ORDEM_EXERC`: PENÚLTIMO = 625; ÚLTIMO = 625
- `ST_CONTA_FIXA`: N = 704; S = 546

**itr_cia_aberta_DFC_MD_ind_2026.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 58), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 62), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 7), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 20), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Individual - Demonstração do Fluxo de Caixa (Método Direto) = 1518
- `MOEDA`: REAL = 1518
- `ESCALA_MOEDA`: MIL = 1248; UNIDADE = 270
- `ORDEM_EXERC`: PENÚLTIMO = 759; ÚLTIMO = 759
- `ST_CONTA_FIXA`: N = 762; S = 756

**itr_cia_aberta_DFC_MI_con_2026.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 65), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 10), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 21), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Consolidado - Demonstração do Fluxo de Caixa (Método Indireto) = 132010
- `MOEDA`: REAL = 132010
- `ESCALA_MOEDA`: MIL = 130524; UNIDADE = 1486
- `ORDEM_EXERC`: PENÚLTIMO = 66005; ÚLTIMO = 66005
- `ST_CONTA_FIXA`: N = 107594; S = 24416

**itr_cia_aberta_DFC_MI_ind_2026.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 64), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 10), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 21), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Individual - Demonstração do Fluxo de Caixa (Método Indireto) = 180358
- `MOEDA`: REAL = 180358
- `ESCALA_MOEDA`: MIL = 177854; UNIDADE = 2504
- `ORDEM_EXERC`: PENÚLTIMO = 90179; ÚLTIMO = 90179
- `ST_CONTA_FIXA`: N = 143178; S = 37180

**itr_cia_aberta_DMPL_con_2026.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 64), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `COLUNA_DF` (máx. 60), `CD_CONTA` (máx. 10), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 21), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Consolidado - Demonstração das Mutações do Patrimônio Líquido = 581749
- `MOEDA`: REAL = 581749
- `ESCALA_MOEDA`: MIL = 570453; UNIDADE = 11296
- `ORDEM_EXERC`: PENÚLTIMO = 291621; ÚLTIMO = 290128
- `ST_CONTA_FIXA`: S = 523276; N = 58473
- Vazios: `COLUNA_DF` = 1317

**itr_cia_aberta_DMPL_ind_2026.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 63), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `COLUNA_DF` (máx. 60), `CD_CONTA` (máx. 10), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 21), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Individual - Demonstração das Mutações do Patrimônio Líquido = 647197
- `MOEDA`: REAL = 647197
- `ESCALA_MOEDA`: MIL = 628969; UNIDADE = 18228
- `ORDEM_EXERC`: PENÚLTIMO = 325418; ÚLTIMO = 321779
- `ST_CONTA_FIXA`: S = 595432; N = 51765

**itr_cia_aberta_DRA_con_2026.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 53), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 10), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 20), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Consolidado - Demonstração de Resultado Abrangente = 29980
- `MOEDA`: REAL = 29980
- `ESCALA_MOEDA`: MIL = 29528; UNIDADE = 452
- `ORDEM_EXERC`: PENÚLTIMO = 14990; ÚLTIMO = 14990
- `ST_CONTA_FIXA`: S = 21210; N = 8770

**itr_cia_aberta_DRA_ind_2026.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 52), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 10), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 20), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Individual - Demonstração de Resultado Abrangente = 31024
- `MOEDA`: REAL = 31024
- `ESCALA_MOEDA`: MIL = 30434; UNIDADE = 590
- `ORDEM_EXERC`: PENÚLTIMO = 15512; ÚLTIMO = 15512
- `ST_CONTA_FIXA`: S = 19814; N = 11210

**itr_cia_aberta_DRE_con_2026.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 42), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 10), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 22), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Consolidado - Demonstração do Resultado = 145214
- `MOEDA`: REAL = 145214
- `ESCALA_MOEDA`: MIL = 142244; UNIDADE = 2970
- `ORDEM_EXERC`: PENÚLTIMO = 72607; ÚLTIMO = 72607
- `ST_CONTA_FIXA`: S = 103940; N = 41274

**itr_cia_aberta_DRE_ind_2026.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 41), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 10), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 21), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Individual - Demonstração do Resultado = 209702
- `MOEDA`: REAL = 209702
- `ESCALA_MOEDA`: MIL = 204014; UNIDADE = 5688
- `ORDEM_EXERC`: PENÚLTIMO = 104851; ÚLTIMO = 104851
- `ST_CONTA_FIXA`: S = 145024; N = 64678

**itr_cia_aberta_DVA_con_2026.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 49), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 13), `DS_CONTA` (máx. 100), `VL_CONTA` (máx. 22), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Consolidado - Demonstração de Valor Adicionado = 108556
- `MOEDA`: REAL = 108556
- `ESCALA_MOEDA`: MIL = 106404; UNIDADE = 2152
- `ORDEM_EXERC`: PENÚLTIMO = 54278; ÚLTIMO = 54278
- `ST_CONTA_FIXA`: S = 100410; N = 8146

**itr_cia_aberta_DVA_ind_2026.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `CD_CVM` (máx. 6), `GRUPO_DFP` (máx. 48), `MOEDA` (máx. 4), `ESCALA_MOEDA` (máx. 7), `ORDEM_EXERC` (máx. 9), `DT_INI_EXERC` (máx. 10), `DT_FIM_EXERC` (máx. 10), `CD_CONTA` (máx. 13), `DS_CONTA` (máx. 96), `VL_CONTA` (máx. 21), `ST_CONTA_FIXA` (máx. 1)
- `GRUPO_DFP`: DF Individual - Demonstração de Valor Adicionado = 160082
- `MOEDA`: REAL = 160082
- `ESCALA_MOEDA`: MIL = 155550; UNIDADE = 4532
- `ORDEM_EXERC`: PENÚLTIMO = 80041; ÚLTIMO = 80041
- `ST_CONTA_FIXA`: S = 148310; N = 11772

**itr_cia_aberta_parecer_2026.csv**

- Colunas: `CNPJ_CIA` (máx. 18), `DT_REFER` (máx. 10), `VERSAO` (máx. 1), `DENOM_CIA` (máx. 60), `TP_RELAT_ESP` (máx. 19), `TP_PARECER_DECL` (máx. 101), `NUM_ITEM_PARECER_DECL` (máx. 2), `TXT_PARECER_DECL` (máx. 7989)
- Vazios: `TP_RELAT_ESP` = 4448
