# Relatório de carga do banco

## Execução

| Arquivo | Situação | Documentos | Linhas | Linhas órfãs | Segundos |
|---|---|---|---|---|---|
| cad_cia_aberta.csv | carregado | 895 | - | - | 0.2 |
| dfp_cia_aberta_2021.zip | sem mudança | - | - | - | - |
| dfp_cia_aberta_2022.zip | sem mudança | - | - | - | - |
| dfp_cia_aberta_2023.zip | sem mudança | - | - | - | - |
| dfp_cia_aberta_2024.zip | sem mudança | - | - | - | - |
| dfp_cia_aberta_2025.zip | sem mudança | - | - | - | - |
| dfp_cia_aberta_2026.zip | sem mudança | - | - | - | - |
| itr_cia_aberta_2021.zip | sem mudança | - | - | - | - |
| itr_cia_aberta_2022.zip | sem mudança | - | - | - | - |
| itr_cia_aberta_2023.zip | sem mudança | - | - | - | - |
| itr_cia_aberta_2024.zip | sem mudança | - | - | - | - |
| itr_cia_aberta_2025.zip | sem mudança | - | - | - | - |
| itr_cia_aberta_2026.zip | sem mudança | - | - | - | - |

Linha órfã: linha de demonstração cuja companhia, data e versão não constam do índice do arquivo.

## Tabelas

Tamanho total do banco: **5803 MB**

| Tabela | Linhas | Tamanho |
|---|---|---|
| setor | 56 | 96 kB |
| companhia | 895 | 680 kB |
| companhia_mercado | 638 | 152 kB |
| documento | 18510 | 5928 kB |
| demonstracao_linha | 28107659 | 5538 MB |
| composicao_capital | 16382 | 1768 kB |
| parecer | 63580 | 110 MB |
| carga_arquivo | 13 | 48 kB |

## Companhias

| Ativa | Companhias | Com algum documento |
|---|---|---|
| sim | 656 | 644 |
| não | 239 | 239 |

| Situação do emissor (ativas) | Companhias |
|---|---|
| FASE OPERACIONAL | 606 |
| EM RECUPERAÇÃO JUDICIAL OU EQUIVALENTE | 24 |
| FASE PRÉ-OPERACIONAL | 9 |
| LIQUIDAÇÃO EXTRAJUDICIAL | 6 |
| EM RECUPERAÇÃO EXTRAJUDICIAL | 6 |
| PARALISADA | 2 |
| FALIDA | 2 |
| EM LIQUIDAÇÃO JUDICIAL | 1 |

| Companhias ativas por quantidade de mercados | Companhias |
|---|---|
| 0 | 213 |
| 1 | 354 |
| 2 | 85 |
| 3 | 4 |

| Setor-base | Setores da CVM reunidos | Companhias ativas |
|---|---|---|
| Energia Elétrica | 2 | 105 |
| Serviços Transporte e Logística | 2 | 104 |
| Construção Civil, Mat. Constr. e Decoração | 2 | 58 |
| Comércio (Atacado e Varejo) | 2 | 51 |
| Saneamento, Serv. Água e Gás | 2 | 36 |
| Máquinas, Equipamentos, Veículos e Peças | 2 | 27 |
| Sem Setor Principal | 1 | 25 |
| Telecomunicações | 2 | 25 |
| Bancos | 2 | 22 |
| Alimentos | 2 | 20 |
| Metalurgia e Siderurgia | 2 | 20 |
| Serviços Médicos | 2 | 18 |
| Têxtil e Vestuário | 2 | 18 |
| Comunicação e Informática | 2 | 16 |
| Petróleo e Gás | 2 | 14 |
| Agricultura (Açúcar, Álcool e Cana) | 2 | 13 |
| Educação | 2 | 13 |
| Farmacêutico e Higiene | 1 | 10 |
| Extração Mineral | 2 | 8 |
| Securitização de Recebíveis | 2 | 8 |
| Intermediação Financeira | 2 | 7 |
| Petroquímicos e Borracha | 1 | 7 |
| Hospedagem e Turismo | 2 | 6 |
| Seguradoras e Corretoras | 2 | 6 |
| Brinquedos e Lazer | 2 | 5 |
| Papel e Celulose | 2 | 5 |
| Arrendamento Mercantil | 1 | 2 |
| Bebidas e Fumo | 1 | 2 |
| Crédito Imobiliário | 2 | 2 |
| Bolsas de Valores/Mercadorias e Futuros | 1 | 1 |
| Embalagens | 1 | 1 |
| Reflorestamento | 1 | 1 |

## Documentos

| Tipo | Ano | Documentos | Vigentes | Versões anteriores | Companhias |
|---|---|---|---|---|---|
| DFP | 2021 | 945 | 770 | 175 | 765 |
| DFP | 2022 | 935 | 731 | 204 | 729 |
| DFP | 2023 | 892 | 733 | 159 | 732 |
| DFP | 2024 | 872 | 709 | 163 | 709 |
| DFP | 2025 | 762 | 672 | 90 | 672 |
| DFP | 2026 | 9 | 9 | 0 | 9 |
| ITR | 2021 | 2478 | 2228 | 250 | 752 |
| ITR | 2022 | 2496 | 2222 | 274 | 763 |
| ITR | 2023 | 2411 | 2158 | 253 | 727 |
| ITR | 2024 | 2448 | 2161 | 287 | 728 |
| ITR | 2025 | 2266 | 2084 | 182 | 709 |
| ITR | 2026 | 1996 | 1907 | 89 | 651 |

### Os arquivos trazem os valores das versões anteriores?

| Versão | Documentos | Com linhas de demonstração | Sem linhas |
|---|---|---|---|
| vigente | 16384 | 16381 | 3 |
| anterior | 2126 | 1 | 2125 |

## Linhas das demonstrações

| Ano | Demonstração | Linhas | Em milhares | Em unidades | Sem valor |
|---|---|---|---|---|---|
| 2021 | BPA | 618002 | 582741 | 35261 | 0 |
| 2021 | BPP | 1052988 | 991458 | 61530 | 0 |
| 2021 | DFC_MD | 5189 | 4792 | 397 | 0 |
| 2021 | DFC_MI | 402031 | 388521 | 13510 | 0 |
| 2021 | DMPL | 1840293 | 1743221 | 97072 | 0 |
| 2021 | DRA | 74531 | 71438 | 3093 | 0 |
| 2021 | DRE | 473219 | 446551 | 26668 | 0 |
| 2021 | DVA | 396861 | 373475 | 23386 | 0 |
| 2022 | BPA | 632543 | 605980 | 26563 | 0 |
| 2022 | BPP | 1075084 | 1028782 | 46302 | 0 |
| 2022 | DFC_MD | 6934 | 6266 | 668 | 0 |
| 2022 | DFC_MI | 426855 | 417332 | 9523 | 0 |
| 2022 | DMPL | 1874677 | 1801065 | 73612 | 0 |
| 2022 | DRA | 78469 | 76082 | 2387 | 0 |
| 2022 | DRE | 482172 | 461828 | 20344 | 0 |
| 2022 | DVA | 406265 | 388670 | 17595 | 0 |
| 2023 | BPA | 636175 | 614893 | 21282 | 0 |
| 2023 | BPP | 1079470 | 1042182 | 37288 | 0 |
| 2023 | DFC_MD | 6946 | 6330 | 616 | 0 |
| 2023 | DFC_MI | 444644 | 436544 | 8100 | 0 |
| 2023 | DMPL | 1879705 | 1819809 | 59896 | 0 |
| 2023 | DRA | 80061 | 78115 | 1946 | 0 |
| 2023 | DRE | 483186 | 467182 | 16004 | 0 |
| 2023 | DVA | 406320 | 392202 | 14118 | 0 |
| 2024 | BPA | 635761 | 614337 | 21424 | 0 |
| 2024 | BPP | 1079168 | 1041572 | 37596 | 0 |
| 2024 | DFC_MD | 7036 | 6244 | 792 | 0 |
| 2024 | DFC_MI | 452821 | 445065 | 7756 | 0 |
| 2024 | DMPL | 1881278 | 1820752 | 60526 | 0 |
| 2024 | DRA | 80437 | 78427 | 2010 | 0 |
| 2024 | DRE | 480874 | 464330 | 16544 | 0 |
| 2024 | DVA | 404812 | 390664 | 14148 | 0 |
| 2025 | BPA | 609618 | 591920 | 17698 | 0 |
| 2025 | BPP | 1033912 | 1002734 | 31178 | 0 |
| 2025 | DFC_MD | 4691 | 4113 | 578 | 0 |
| 2025 | DFC_MI | 445029 | 438363 | 6666 | 0 |
| 2025 | DMPL | 1808291 | 1757537 | 50754 | 0 |
| 2025 | DRA | 78798 | 77134 | 1664 | 0 |
| 2025 | DRE | 459758 | 445928 | 13830 | 0 |
| 2025 | DVA | 387567 | 375983 | 11584 | 0 |
| 2026 | BPA | 427238 | 416588 | 10650 | 0 |
| 2026 | BPP | 726094 | 707358 | 18736 | 0 |
| 2026 | DFC_MD | 2768 | 2386 | 382 | 0 |
| 2026 | DFC_MI | 314454 | 310206 | 4248 | 0 |
| 2026 | DMPL | 1237000 | 1206494 | 30506 | 0 |
| 2026 | DRA | 61248 | 60186 | 1062 | 0 |
| 2026 | DRE | 356070 | 347288 | 8782 | 0 |
| 2026 | DVA | 270316 | 263460 | 6856 | 0 |

### Linhas repetidas na chave completa

Grupos de linhas com o mesmo documento, demonstração, escopo, exercício, período, coluna e código de conta.

| Demonstração | Grupos repetidos | Com descrições diferentes | Com valores diferentes | Idênticos |
|---|---|---|---|---|
| BPA | 17651 | 8 | 65 | 17582 |
| BPP | 30446 | 22 | 172 | 30269 |
| DFC_MD | 1807 | 0 | 7 | 1800 |
| DFC_MI | 7621 | 18 | 31 | 7573 |
| DMPL | 53880 | 78 | 459 | 53356 |
| DRA | 1523 | 2 | 4 | 1517 |
| DRE | 10523 | 0 | 72 | 10451 |
| DVA | 11797 | 4 | 90 | 11703 |

### Conferência: ativo total igual a passivo total

Documentos vigentes, consolidado, último exercício: conta 1 do balanço ativo comparada à conta 2 do passivo.

| Documentos comparados | Iguais | Diferentes |
|---|---|---|
| 10444 | 10432 | 12 |
