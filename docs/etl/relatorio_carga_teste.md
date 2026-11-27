# Relatório de carga do banco

## Execução

| Arquivo | Situação | Documentos | Linhas | Linhas órfãs | Segundos |
|---|---|---|---|---|---|
| cad_cia_aberta.csv | carregado | 676 | - | - | 0.1 |
| itr_cia_aberta_2026.zip | carregado | 1996 | 3375356 | 0 | 46.2 |

Linha órfã: linha de demonstração cuja companhia, data e versão não constam do índice do arquivo.

## Tabelas

Tamanho total do banco: **932 MB**

| Tabela | Linhas | Tamanho |
|---|---|---|
| setor | 53 | 88 kB |
| companhia | 688 | 560 kB |
| companhia_mercado | 549 | 136 kB |
| documento | 2758 | 1152 kB |
| demonstracao_linha | 4562673 | 902 MB |
| composicao_capital | 2577 | 328 kB |
| parecer | 10219 | 19 MB |
| carga_arquivo | 3 | 48 kB |

## Companhias

| Ativa | Companhias | Com algum documento |
|---|---|---|
| sim | 655 | 640 |
| não | 33 | 33 |

| Situação do emissor (ativas) | Companhias |
|---|---|
| FASE OPERACIONAL | 605 |
| EM RECUPERAÇÃO JUDICIAL OU EQUIVALENTE | 24 |
| FASE PRÉ-OPERACIONAL | 9 |
| LIQUIDAÇÃO EXTRAJUDICIAL | 6 |
| EM RECUPERAÇÃO EXTRAJUDICIAL | 6 |
| PARALISADA | 2 |
| FALIDA | 2 |
| EM LIQUIDAÇÃO JUDICIAL | 1 |

| Companhias ativas por quantidade de mercados | Companhias |
|---|---|
| 0 | 212 |
| 1 | 354 |
| 2 | 85 |
| 3 | 4 |

| Setor-base | Setores da CVM reunidos | Companhias ativas |
|---|---|---|
| Energia Elétrica | 2 | 105 |
| Serviços Transporte e Logística | 2 | 104 |
| Construção Civil, Mat. Constr. e Decoração | 2 | 57 |
| Comércio (Atacado e Varejo) | 2 | 51 |
| Saneamento, Serv. Água e Gás | 2 | 36 |
| Máquinas, Equipamentos, Veículos e Peças | 2 | 27 |
| Sem Setor Principal | 1 | 25 |
| Telecomunicações | 2 | 25 |
| Bancos | 2 | 22 |
| Alimentos | 2 | 20 |
| Metalurgia e Siderurgia | 2 | 20 |
| Serviços Médicos | 2 | 18 |
| Têxtil e Vestuário | 1 | 18 |
| Comunicação e Informática | 2 | 16 |
| Petróleo e Gás | 2 | 14 |
| Agricultura (Açúcar, Álcool e Cana) | 2 | 13 |
| Educação | 2 | 13 |
| Farmacêutico e Higiene | 1 | 10 |
| Extração Mineral | 2 | 8 |
| Securitização de Recebíveis | 1 | 8 |
| Intermediação Financeira | 2 | 7 |
| Petroquímicos e Borracha | 1 | 7 |
| Hospedagem e Turismo | 2 | 6 |
| Seguradoras e Corretoras | 2 | 6 |
| Brinquedos e Lazer | 2 | 5 |
| Papel e Celulose | 2 | 5 |
| Arrendamento Mercantil | 1 | 2 |
| Bebidas e Fumo | 1 | 2 |
| Crédito Imobiliário | 1 | 2 |
| Bolsas de Valores/Mercadorias e Futuros | 1 | 1 |
| Embalagens | 1 | 1 |
| Reflorestamento | 1 | 1 |

## Documentos

| Tipo | Ano | Documentos | Vigentes | Versões anteriores | Companhias |
|---|---|---|---|---|---|
| DFP | 2025 | 762 | 672 | 90 | 672 |
| ITR | 2026 | 1996 | 1907 | 89 | 651 |

### Os arquivos trazem os valores das versões anteriores?

| Versão | Documentos | Com linhas de demonstração | Sem linhas |
|---|---|---|---|
| vigente | 2579 | 2577 | 2 |
| anterior | 179 | 0 | 179 |

## Linhas das demonstrações

| Ano | Demonstração | Linhas | Em milhares | Em unidades | Sem valor |
|---|---|---|---|---|---|
| 2025 | BPA | 150397 | 146459 | 3938 | 0 |
| 2025 | BPP | 255198 | 248196 | 7002 | 0 |
| 2025 | DFC_MD | 1358 | 1232 | 126 | 0 |
| 2025 | DFC_MI | 115239 | 113513 | 1726 | 0 |
| 2025 | DMPL | 479872 | 468034 | 11838 | 0 |
| 2025 | DRA | 13520 | 13264 | 256 | 0 |
| 2025 | DRE | 75415 | 73407 | 2008 | 0 |
| 2025 | DVA | 96318 | 93704 | 2614 | 0 |
| 2026 | BPA | 424710 | 414320 | 10390 | 0 |
| 2026 | BPP | 722006 | 703704 | 18302 | 0 |
| 2026 | DFC_MD | 2768 | 2386 | 382 | 0 |
| 2026 | DFC_MI | 312368 | 308378 | 3990 | 0 |
| 2026 | DMPL | 1228946 | 1199422 | 29524 | 0 |
| 2026 | DRA | 61004 | 59962 | 1042 | 0 |
| 2026 | DRE | 354916 | 346258 | 8658 | 0 |
| 2026 | DVA | 268638 | 261954 | 6684 | 0 |

### Linhas repetidas na chave completa

Grupos de linhas com o mesmo documento, demonstração, escopo, exercício, período, coluna e código de conta.

| Demonstração | Grupos repetidos | Com descrições diferentes | Com valores diferentes | Idênticos |
|---|---|---|---|---|
| BPA | 1770 | 0 | 16 | 1754 |
| BPP | 2918 | 0 | 63 | 2855 |
| DFC_MD | 182 | 0 | 7 | 175 |
| DFC_MI | 602 | 2 | 0 | 600 |
| DMPL | 5631 | 0 | 78 | 5553 |
| DRA | 188 | 0 | 0 | 188 |
| DRE | 1022 | 0 | 23 | 999 |
| DVA | 1166 | 0 | 54 | 1112 |

### Conferência: ativo total igual a passivo total

Documentos vigentes, consolidado, último exercício: conta 1 do balanço ativo comparada à conta 2 do passivo.

| Documentos comparados | Iguais | Diferentes |
|---|---|---|
| 1692 | 1692 | 0 |
