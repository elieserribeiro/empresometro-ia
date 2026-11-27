# Relatório da coleta de documentos

## Tempos desta execução

| Fonte | Itens processados | Segundos no total | Mediana por item (s) | Máximo (s) |
|---|---|---|---|---|
| FRE_PACOTE | 2 | 199 | 99.3 | 169.9 |
| FRE | 157 | 0 | 0.0 | 0.0 |

FRE_PACOTE é o download e a leitura de um formulário inteiro; FRE são as seções extraídas dele.

## Documentos por fonte e situação

| Fonte | Categoria | Situação | Documentos | Páginas | Caracteres (milhões) | Trechos |
|---|---|---|---|---|---|---|
| FRE | Formulário de Referência | OK | 156 | 797 | 1.81 | 2118 |
| FRE | Formulário de Referência | SEM_TEXTO | 1 | 23 | 0.00 | 0 |
| IPE | Comunicado ao Mercado | ERRO | 1 | 0 | 0.00 | 0 |
| IPE | Comunicado ao Mercado | OK | 44 | 1282 | 0.78 | 971 |
| IPE | Fato Relevante | OK | 15 | 32 | 0.06 | 84 |
| PARECER | Parecer ou declaração | OK | 147 | 147 | 0.64 | 687 |

## Por companhia

| Companhia | Fatos e comunicados | Seções de FRE | Pareceres | Trechos | Sem texto | Com erro |
|---|---|---|---|---|---|---|
| AZZAS 2154 S.A. | 0 | 0 | 6 | 23 | 0 | 0 |
| BANCO DO BRASIL S.A. | 46 | 78 | 11 | 1126 | 1 | 0 |
| CIA SANEAMENTO BÁSICO ESTADO SÃO PAULO | 0 | 0 | 5 | 19 | 0 | 0 |
| COMPANHIA BRASILEIRA DE DISTRIBUIÇÃO | 0 | 0 | 7 | 33 | 0 | 0 |
| COSAN S.A. | 0 | 0 | 7 | 32 | 0 | 0 |
| EMBRAER S.A. | 0 | 0 | 7 | 28 | 0 | 0 |
| GERDAU S.A. | 0 | 0 | 6 | 21 | 0 | 0 |
| GRUPO CASAS BAHIA S.A. - EM RECUPERAÇÃO JUDICIAL | 0 | 0 | 8 | 40 | 0 | 0 |
| IRB - BRASIL RESSEGUROS S.A. | 0 | 0 | 6 | 25 | 0 | 0 |
| ITAÚ UNIBANCO HOLDING S.A. | 0 | 0 | 13 | 69 | 0 | 0 |
| JBS SA | 0 | 0 | 5 | 18 | 0 | 0 |
| LIGHT S.A. - EM RECUPERAÇÃO JUDICIAL | 0 | 0 | 8 | 37 | 0 | 0 |
| NEOENERGIA S.A | 14 | 79 | 8 | 2154 | 0 | 1 |
| PETRÓLEO BRASILEIRO S.A. - PETROBRAS | 0 | 0 | 7 | 32 | 0 | 0 |
| REDE D'OR SÃO LUIZ S.A. | 0 | 0 | 8 | 39 | 0 | 0 |
| SIMPAR S.A. | 0 | 0 | 8 | 33 | 0 | 0 |
| TELEFÔNICA BRASIL S.A. | 0 | 0 | 7 | 28 | 0 | 0 |
| TOTVS S.A | 0 | 0 | 6 | 34 | 0 | 0 |
| VIBRA ENERGIA S/A | 0 | 0 | 8 | 39 | 0 | 0 |
| VOTORANTIM CIMENTOS S.A. | 0 | 0 | 6 | 30 | 0 | 0 |

## Trechos

| Trechos | Caracteres (milhões) | Tamanho mediano | Menor | Maior |
|---|---|---|---|---|
| 3860 | 3.78 | 1042.0 | 18 | 1906 |

## Erros mais frequentes

| Fonte | Erro | Documentos |
|---|---|---|
| IPE | O arquivo entregue não é um PDF. | 1 |

## Exemplo de busca textual

Consulta: `recuperação judicial` (os três trechos mais relevantes).

| Companhia | Fonte | Título | Página | Trecho |
|---|---|---|---|---|
| BANCO DO BRASIL S.A. | FRE | 4. Fatores de risco / Processos nao sigilosos | 7 | Judicial aprovado e homologado, ou na falência, caso venha a ser confirmada a decisão de 1ª Instância pelo Tribunal de Justiça do Rio de Janeiro. Processos judi |
| BANCO DO BRASIL S.A. | FRE | 4. Fatores de risco / Processos nao sigilosos | 8 | haver impacto se não houver o recebimento do crédito previsto no Plano de Recuperação Judicial aprovado e homologado. Formulário de Referência 202 5 Banco do Br |
| BANCO DO BRASIL S.A. | FRE | 4. Fatores de risco / Processos nao sigilosos | 9 | em 14.05.2020 Valor habilitado na Recuperação Judicial em 28/07/2020: R$ 3.927.812.115,69. Valor Atualizado até 31.12.2024: R$ 3.565.970.077,66. f. principais f |
