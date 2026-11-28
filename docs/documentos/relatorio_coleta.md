# Relatório da coleta de documentos

## Tempos desta execução

| Fonte | Itens processados | Segundos no total | Mediana por item (s) | Máximo (s) |
|---|---|---|---|---|
| IPE | 5818 | 11432 | 1.3 | 135.7 |
| FRE_PACOTE | 118 | 1902 | 12.3 | 205.0 |
| FRE | 6216 | 0 | 0.0 | 0.0 |
| PARECER | 1938 | 0 | 0.0 | 0.0 |

FRE_PACOTE é o download e a leitura de um formulário inteiro; FRE são as seções extraídas dele.

## Documentos por fonte e situação

| Fonte | Categoria | Situação | Documentos | Páginas | Caracteres (milhões) | Trechos |
|---|---|---|---|---|---|---|
| FRE | Formulário de Referência | ERRO | 3 | 0 | 0.00 | 0 |
| FRE | Formulário de Referência | OK | 6160 | 26838 | 66.05 | 73964 |
| FRE | Formulário de Referência | SEM_TEXTO | 53 | 77 | 0.00 | 0 |
| IPE | Comunicado ao Mercado | ERRO | 419 | 0 | 0.00 | 0 |
| IPE | Comunicado ao Mercado | OK | 3930 | 44669 | 41.52 | 48622 |
| IPE | Comunicado ao Mercado | SEM_TEXTO | 28 | 36 | 0.00 | 0 |
| IPE | Fato Relevante | ERRO | 152 | 0 | 0.00 | 0 |
| IPE | Fato Relevante | OK | 1283 | 4835 | 9.79 | 11548 |
| IPE | Fato Relevante | SEM_TEXTO | 6 | 10 | 0.00 | 0 |
| PARECER | Parecer ou declaração | OK | 1938 | 1938 | 5.79 | 6435 |

## Por companhia

| Companhia | Fatos e comunicados | Seções de FRE | Pareceres | Trechos | Sem texto | Com erro |
|---|---|---|---|---|---|---|
| AZZAS 2154 S.A. | 179 | 311 | 106 | 5731 | 2 | 15 |
| BANCO DO BRASIL S.A. | 390 | 311 | 132 | 6647 | 2 | 42 |
| CIA SANEAMENTO BÁSICO ESTADO SÃO PAULO | 317 | 313 | 88 | 6728 | 2 | 31 |
| COMPANHIA BRASILEIRA DE DISTRIBUIÇÃO | 261 | 312 | 75 | 5896 | 0 | 22 |
| COSAN S.A. | 211 | 314 | 94 | 6972 | 7 | 12 |
| EMBRAER S.A. | 408 | 305 | 109 | 6401 | 6 | 28 |
| GERDAU S.A. | 178 | 311 | 59 | 4942 | 0 | 15 |
| GRUPO CASAS BAHIA S.A. - EM RECUPERAÇÃO JUDICIAL | 221 | 310 | 88 | 6109 | 0 | 20 |
| IRB - BRASIL RESSEGUROS S.A. | 202 | 306 | 91 | 4705 | 5 | 22 |
| ITAÚ UNIBANCO HOLDING S.A. | 307 | 312 | 163 | 13208 | 7 | 32 |
| JBS SA | 152 | 309 | 115 | 5817 | 4 | 16 |
| LIGHT S.A. - EM RECUPERAÇÃO JUDICIAL | 269 | 314 | 97 | 6500 | 5 | 33 |
| NEOENERGIA S.A | 233 | 313 | 93 | 10728 | 0 | 19 |
| PETRÓLEO BRASILEIRO S.A. - PETROBRAS | 1358 | 314 | 89 | 14835 | 11 | 142 |
| REDE D'OR SÃO LUIZ S.A. | 151 | 307 | 123 | 6594 | 1 | 12 |
| SIMPAR S.A. | 256 | 310 | 98 | 7533 | 8 | 30 |
| TELEFÔNICA BRASIL S.A. | 207 | 310 | 89 | 3896 | 19 | 26 |
| TOTVS S.A | 235 | 311 | 88 | 5889 | 3 | 19 |
| VIBRA ENERGIA S/A | 230 | 311 | 86 | 6690 | 3 | 32 |
| VOTORANTIM CIMENTOS S.A. | 53 | 312 | 55 | 4748 | 2 | 6 |

## Trechos

| Trechos | Caracteres (milhões) | Tamanho mediano | Menor | Maior |
|---|---|---|---|---|
| 140569 | 140.81 | 1095.0 | 1 | 1949 |

## Erros mais frequentes

| Fonte | Erro | Documentos |
|---|---|---|
| IPE | O arquivo entregue não é um PDF. | 568 |
| FRE | Falha ao ler o PDF: DependencyError: cryptography>=3.1 is required for AES algorithm | 3 |
| IPE | Falha ao ler o PDF: DependencyError: cryptography>=3.1 is required for AES algorithm | 3 |

## Exemplo de busca textual

Consulta: `recuperação judicial` (os três trechos mais relevantes).

| Companhia | Fonte | Título | Página | Trecho |
|---|---|---|---|---|
| BANCO DO BRASIL S.A. | FRE | 4. Fatores de risco / Processos nao sigilosos | 4 | e de outras empresas do Grupo, conforme aprovado pela Assembleia Geral de Credores. Em outubro de 2021, o Juízo sentenciou o encerramento da recuperação judicia |
| BANCO DO BRASIL S.A. | FRE | 4. Fatores de risco / Processos nao sigilosos | 8 | transitou em julgado em razão de recurso manejado pela Planner. Formulário de Referência 2024 Banco do Brasil S.A. | Relações com Investidores 174 g. resumo das |
| BANCO DO BRASIL S.A. | FRE | 4. Fatores de risco / Processos nao sigilosos | 5 | de Falências e Recuperações Judiciais da Comarca de São Paulo/SP b. instância 1ª instância c. data de instauração 29.05.2019 d. partes no processo Autores/Recup |
