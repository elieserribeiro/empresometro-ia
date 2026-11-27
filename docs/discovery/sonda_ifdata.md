# Sonda do IF.data (data-base 202506)

## Relatórios disponíveis

`https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/ListaDeRelatorio()?%24format=json`

- {"NomeRelatorio": "Resumo", "NumeroRelatorio": "1"}
- {"NomeRelatorio": "Ativo", "NumeroRelatorio": "2"}
- {"NomeRelatorio": "Passivo", "NumeroRelatorio": "3"}
- {"NomeRelatorio": "Demonstração de Resultado", "NumeroRelatorio": "4"}
- {"NomeRelatorio": "Informações de Capital", "NumeroRelatorio": "5"}
- {"NomeRelatorio": "Segmentação", "NumeroRelatorio": "6"}
- {"NomeRelatorio": "Carteira de Crédito Ativa - Por indexador", "NumeroRelatorio": "7"}
- {"NomeRelatorio": "Carteira de crédito ativa - por nível de risco da operação", "NumeroRelatorio": "8"}
- {"NomeRelatorio": "Carteira de crédito ativa - por região geográfica", "NumeroRelatorio": "9"}
- {"NomeRelatorio": "Carteira de crédito ativa - quantidade de clientes e de operações", "NumeroRelatorio": "10"}
- {"NomeRelatorio": "Carteira de crédito ativa Pessoa Física - modalidade e prazo de vencimento", "NumeroRelatorio": "11"}
- {"NomeRelatorio": "Carteira de crédito ativa Pessoa Jurídica -  por atividade econômica (CNAE)", "NumeroRelatorio": "12"}
- {"NomeRelatorio": "Carteira de crédito ativa Pessoa Jurídica - modalidade e prazo de vencimento", "NumeroRelatorio": "13"}
- {"NomeRelatorio": "Carteira de crédito ativa Pessoa Jurídica - por porte do tomador", "NumeroRelatorio": "14"}
- {"NomeRelatorio": "Movimentação de Câmbio no Trimestre", "NumeroRelatorio": "15"}
- {"NomeRelatorio": "Carteira de crédito ativa - por carteiras de instrumentos financeiros", "NumeroRelatorio": "16"}

## Cadastro

`https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata/IfDataCadastro(AnoMes=@AnoMes)?%24format=json&%40AnoMes=202506&%24top=5000`

4995 linhas.

Campos: `CodInst`, `Data`, `NomeInstituicao`, `DataInicioAtividade`, `Tcb`, `Td`, `Tc`, `SegmentoTb`, `Atividade`, `Uf`, `Municipio`, `Sr`, `CodConglomeradoFinanceiro`, `CodConglomeradoPrudencial`, `CnpjInstituicaoLider`, `Situacao`
- `Data`: 202506 = 4995
- `Tcb`: B3S = 2273; N2 = 1184; N1 = 651; N4 = 381; B1 = 239; B2 = 174; B3C = 50; N3 = 31; B4 = 12
- `Td`: I = 4995
- `Tc`: 2 = 4584; 3 = 336; 1 = 75
- `Sr`: None = 3443; S5 = 853; S4 = 470; S3 = 121; S1 = 71; S2 = 37
- `Situacao`: I = 3290; A = 1662; F = 22; LO = 18; LE = 3
- Exemplo ITAU: {"CodInst": "60394079", "Data": "202506", "NomeInstituicao": "BANCO ITAUBANK S.A.", "DataInicioAtividade": 196508, "Tcb": "B1", "Td": "I", "Tc": 2, "SegmentoTb": "Banco Múltiplo", "Atividade": null, "Uf": "SP", "Municipio": "São Paulo", "Sr": "S1", "CodConglomeradoFinanceiro": "C0010069", "CodConglomeradoPrudencial": "C0080099", "CnpjInstituicaoLider": "60872504", "Situacao": "A"}
- Exemplo ITAU: {"CodInst": "61200044", "Data": "202506", "NomeInstituicao": "BANCO ITAU DE INVESTIMENTO S/A", "DataInicioAtividade": 196907, "Tcb": "B2", "Td": "I", "Tc": 2, "SegmentoTb": "Banco de Investimento", "Atividade": null, "Uf": "SP", "Municipio": "São Paulo", "Sr": null, "CodConglomeradoFinanceiro": null, "CodConglomeradoPrudencial": null, "CnpjInstituicaoLider": null, "Situacao": "I"}
- Exemplo ITAU: {"CodInst": "17192451", "Data": "202506", "NomeInstituicao": "BANCO ITAUCARD S.A.", "DataInicioAtividade": 196805, "Tcb": "B2", "Td": "I", "Tc": 2, "SegmentoTb": "Banco Múltiplo", "Atividade": null, "Uf": "SP", "Municipio": "São Paulo", "Sr": "S1", "CodConglomeradoFinanceiro": "C0010069", "CodConglomeradoPrudencial": "C0080099", "CnpjInstituicaoLider": "60872504", "Situacao": "A"}
- Exemplo ITAU: {"CodInst": "59461152", "Data": "202506", "NomeInstituicao": "BANCO ITAUCRED FINANCIAMENTOS S.A.", "DataInicioAtividade": 198809, "Tcb": "B2", "Td": "I", "Tc": 2, "SegmentoTb": "Banco Múltiplo", "Atividade": null, "Uf": "SP", "Municipio": "São Paulo", "Sr": null, "CodConglomeradoFinanceiro": null, "CodConglomeradoPrudencial": null, "CnpjInstituicaoLider": null, "Situacao": "I"}
- Exemplo BRASIL: {"CodInst": "28195667", "Data": "202506", "NomeInstituicao": "BANCO ABC BRASIL S.A.", "DataInicioAtividade": 198312, "Tcb": "B1", "Td": "I", "Tc": 3, "SegmentoTb": "Banco Múltiplo", "Atividade": null, "Uf": "SP", "Municipio": "São Paulo", "Sr": "S3", "CodConglomeradoFinanceiro": "C0041856", "CodConglomeradoPrudencial": "C0080312", "CnpjInstituicaoLider": "28195667", "Situacao": "A"}
- Exemplo BRASIL: {"CodInst": "48795256", "Data": "202506", "NomeInstituicao": "BANCO ANDBANK (BRASIL) S.A.", "DataInicioAtividade": 197708, "Tcb": "B1", "Td": "I", "Tc": 3, "SegmentoTb": "Banco Múltiplo", "Atividade": null, "Uf": "SP", "Municipio": "São Paulo", "Sr": "S4", "CodConglomeradoFinanceiro": "C0051949", "CodConglomeradoPrudencial": "C0081256", "CnpjInstituicaoLider": "48795256", "Situacao": "A"}
- Exemplo BRASIL: {"CodInst": "01522368", "Data": "202506", "NomeInstituicao": "BANCO BNP PARIBAS BRASIL S.A.", "DataInicioAtividade": 199612, "Tcb": "B1", "Td": "I", "Tc": 3, "SegmentoTb": "Banco Múltiplo", "Atividade": null, "Uf": "SP", "Municipio": "São Paulo", "Sr": "S3", "CodConglomeradoFinanceiro": null, "CodConglomeradoPrudencial": "C0080673", "CnpjInstituicaoLider": "01522368", "Situacao": "A"}
- Exemplo BRASIL: {"CodInst": "13004577", "Data": "202506", "NomeInstituicao": "BANCO BRASILEIRO COMERCIAL S.A.", "DataInicioAtividade": 193409, "Tcb": "B1", "Td": "I", "Tc": 2, "SegmentoTb": "Banco Múltiplo", "Atividade": null, "Uf": "GO", "Municipio": "Goiânia", "Sr": null, "CodConglomeradoFinanceiro": null, "CodConglomeradoPrudencial": null, "CnpjInstituicaoLider": null, "Situacao": "I"}
- Exemplo BRADESCO: {"CodInst": "06271464", "Data": "202506", "NomeInstituicao": "BANCO BRADESCO BBI S.A.", "DataInicioAtividade": 193906, "Tcb": "B1", "Td": "I", "Tc": 2, "SegmentoTb": "Banco Múltiplo", "Atividade": null, "Uf": "SP", "Municipio": "Osasco", "Sr": "S1", "CodConglomeradoFinanceiro": "C0010045", "CodConglomeradoPrudencial": "C0080075", "CnpjInstituicaoLider": "60746948", "Situacao": "A"}
- Exemplo BRADESCO: {"CodInst": "33147315", "Data": "202506", "NomeInstituicao": "BANCO BRADESCO BERJ S.A.", "DataInicioAtividade": 194503, "Tcb": "B1", "Td": "I", "Tc": 2, "SegmentoTb": "Banco Múltiplo", "Atividade": null, "Uf": "SP", "Municipio": "Osasco", "Sr": "S1", "CodConglomeradoFinanceiro": "C0010045", "CodConglomeradoPrudencial": "C0080075", "CnpjInstituicaoLider": "60746948", "Situacao": "A"}
- Exemplo BRADESCO: {"CodInst": "59438325", "Data": "202506", "NomeInstituicao": "BANCO BRADESCO CARTÕES S.A.", "DataInicioAtividade": 198902, "Tcb": "B1", "Td": "I", "Tc": 3, "SegmentoTb": "Banco Múltiplo", "Atividade": null, "Uf": "SP", "Municipio": "Osasco", "Sr": null, "CodConglomeradoFinanceiro": null, "CodConglomeradoPrudencial": null, "CnpjInstituicaoLider": null, "Situacao": "I"}
- Exemplo BRADESCO: {"CodInst": "07207996", "Data": "202506", "NomeInstituicao": "BANCO BRADESCO FINANCIAMENTOS S.A.", "DataInicioAtividade": 193907, "Tcb": "B1", "Td": "I", "Tc": 2, "SegmentoTb": "Banco Múltiplo", "Atividade": null, "Uf": "SP", "Municipio": "Osasco", "Sr": "S1", "CodConglomeradoFinanceiro": "C0010045", "CodConglomeradoPrudencial": "C0080075", "CnpjInstituicaoLider": "60746948", "Situacao": "A"}
- Exemplo BTG: {"CodInst": "30306294", "Data": "202506", "NomeInstituicao": "BANCO BTG PACTUAL S.A.", "DataInicioAtividade": 198612, "Tcb": "B1", "Td": "I", "Tc": 2, "SegmentoTb": "Banco Múltiplo", "Atividade": null, "Uf": "RJ", "Municipio": "Rio de Janeiro", "Sr": "S1", "CodConglomeradoFinanceiro": "C0049944", "CodConglomeradoPrudencial": "C0080336", "CnpjInstituicaoLider": "30306294", "Situacao": "A"}
- Exemplo BTG: {"CodInst": "59149941", "Data": "202506", "NomeInstituicao": "JV BTG SENIOR SOCIEDADE DE CRÉDITO DIRETO S.A.", "DataInicioAtividade": 180001, "Tcb": "N1", "Td": "I", "Tc": 2, "SegmentoTb": "Sociedade de Crédito Direto", "Atividade": null, "Uf": "RJ", "Municipio": "Rio de Janeiro", "Sr": "S1", "CodConglomeradoFinanceiro": null, "CodConglomeradoPrudencial": "C0080336", "CnpjInstituicaoLider": "30306294", "Situacao": "I"}
- Exemplo BTG: {"CodInst": "00997804", "Data": "202506", "NomeInstituicao": "BTG PACTUAL ADVISORS DISTRIBUIDORA DE TÍTULOS E VALORES MOBILIÁRIOS S.A.", "DataInicioAtividade": 199602, "Tcb": "N2", "Td": "I", "Tc": 2, "SegmentoTb": "Sociedade Distribuidora de TVM", "Atividade": null, "Uf": "SP", "Municipio": "São Paulo", "Sr": null, "CodConglomeradoFinanceiro": null, "CodConglomeradoPrudencial": null, "CnpjInstituicaoLider": null, "Situacao": "I"}
- Exemplo BTG: {"CodInst": "29650082", "Data": "202506", "NomeInstituicao": "BTG PACTUAL ASSET MANAGEMENT S.A. DISTRIBUIDORA DE TÍTULOS E VALORES MOBILIÁRIOS", "DataInicioAtividade": 198612, "Tcb": "N2", "Td": "I", "Tc": 2, "SegmentoTb": "Sociedade Distribuidora de TVM", "Atividade": null, "Uf": "RJ", "Municipio": "Rio de Janeiro", "Sr": "S1", "CodConglomeradoFinanceiro": "C0049944", "CodConglomeradoPrudencial": "C0080336", "CnpjInstituicaoLider": "30306294", "Situacao": "A"}

## Tipo de instituição 1, relatório 1

13670 valores, 1367 instituições, 10 colunas.
Campos: `TipoInstituicao`, `CodInst`, `AnoMes`, `NomeRelatorio`, `NumeroRelatorio`, `Grupo`, `Conta`, `NomeColuna`, `DescricaoColuna`, `Saldo`
Exemplo: {"TipoInstituicao": 1, "CodInst": "00068987", "AnoMes": "202506", "NomeRelatorio": "Resumo", "NumeroRelatorio": "1", "Grupo": null, "Conta": "140200", "NomeColuna": "Títulos e Valores Mobiliários", "DescricaoColuna": "[1300000008]-[1330000009]", "Saldo": 21752485.33}

Colunas (nome | grupo | conta | linhas):
- Títulos e Valores Mobiliários | None | 140200 | 1367
- Ativo Total | None | 140220 | 1367
- Captações | None | 140239 | 1367
- Passivo Exigível | None | 140244 | 1367
- Patrimônio Líquido | None | 140246 | 1367
- Lucro Líquido | None | 141870 | 1367
- Carteira de Crédito | None | 141873 | 1367
- Patrimônio de Referência para Comparação com o RWA 
(e) | None | 79649 | 1367
- Índice de Imobilização | None | 79662 | 1367
- Índice de Basileia | None | 79664 | 1367

## Tipo de instituição 1, relatório 2

32808 valores, 1367 instituições, 24 colunas.
Campos: `TipoInstituicao`, `CodInst`, `AnoMes`, `NomeRelatorio`, `NumeroRelatorio`, `Grupo`, `Conta`, `NomeColuna`, `DescricaoColuna`, `Saldo`
Exemplo: {"TipoInstituicao": 1, "CodInst": "00068987", "AnoMes": "202506", "NomeRelatorio": "Ativo", "NumeroRelatorio": "2", "Grupo": null, "Conta": "140198", "NomeColuna": "Disponibilidades \n(a)", "DescricaoColuna": "[1100000002]", "Saldo": 5174236.99}

Colunas (nome | grupo | conta | linhas):
- Disponibilidades 
(a) | None | 140198 | 1367
- Aplicações Interfinanceiras de Liquidez 
(b) | None | 140199 | 1367
- Títulos e Valores Mobiliários 
(c) | None | 140200 | 1367
- Outros Ativos Realizáveis 
(i) | None | 140218 | 1367
- Ativo Permanente 
(j) | None | 140219 | 1367
- Ativo Total 
(k) = (a) + (b) + (c) + (d) + (e) + (f) + (g) + (h) + (i) + (j) | None | 140220 | 1367
- Instrumentos Derivativos (d) | None | 141612 | 1367
- Valor Contábil Bruto 
(f1) | Operações de Arrendamento Financeiro | 140207 | 1367
- Perda Esperada 
(f2) | Operações de Arrendamento Financeiro | 140208 | 1367
- Hedge de Valor Justo 
(f3) | Operações de Arrendamento Financeiro | 140209 | 1367
- Operações de Arrendamento Financeiro 
(f) | Operações de Arrendamento Financeiro | 140210 | 1367
- Valor Contábil Bruto 
(e1) | Operações de Crédito | 140201 | 1367
- Perda Esperada 
(e2) | Operações de Crédito | 140202 | 1367
- Hedge de Valor Justo 
(e3) | Operações de Crédito | 140203 | 1367
- Ajuste a Valor Justo 
(e4) | Operações de Crédito | 140204 | 1367
- Operações de Crédito 
(e) | Operações de Crédito | 140205 | 1367
- Valor Contábil Bruto 
(g1) | Outras Operações com Características de Concessão de Crédito | 140212 | 1367
- Perda Esperada 
(g2) | Outras Operações com Características de Concessão de Crédito | 140213 | 1367
- Hedge de Valor Justo 
(g3) | Outras Operações com Características de Concessão de Crédito | 140214 | 1367
- Ajuste a Valor Justo 
(g4) | Outras Operações com Características de Concessão de Crédito | 140215 | 1367
- Outras Operações com Características de Concessão de Crédito 
(g) | Outras Operações com Características de Concessão de Crédito | 140216 | 1367
- Valor Contábil Bruto 
(h1) | Valores a Receber de Transações de Pagamentos - Usuários Finais (Pós-pago) | 145831 | 1367
- Perda Esperada 
(h2) | Valores a Receber de Transações de Pagamentos - Usuários Finais (Pós-pago) | 145832 | 1367
- Valores a Receber de Transações de Pagamentos - Usuários Finais (Pós-pago) 
(h) | Valores a Receber de Transações de Pagamentos - Usuários Finais (Pós-pago) | 145833 | 1367

## Tipo de instituição 1, relatório 3

30074 valores, 1367 instituições, 22 colunas.
Campos: `TipoInstituicao`, `CodInst`, `AnoMes`, `NomeRelatorio`, `NumeroRelatorio`, `Grupo`, `Conta`, `NomeColuna`, `DescricaoColuna`, `Saldo`
Exemplo: {"TipoInstituicao": 1, "CodInst": "00068987", "AnoMes": "202506", "NomeRelatorio": "Passivo", "NumeroRelatorio": "3", "Grupo": null, "Conta": "140241", "NomeColuna": "Instrumentos Derivativos \n(f)", "DescricaoColuna": "[4700000007]", "Saldo": 0.0}

Colunas (nome | grupo | conta | linhas):
- Instrumentos Derivativos 
(f) | None | 140241 | 1367
- Outras Obrigações 
(g) | None | 140242 | 1367
- Instrumentos de Dívida Elegíveis a Capital 
(h) | None | 140243 | 1367
- Passivo Exigível 
(i) = (e) + (f) + (g) + (h) | None | 140244 | 1367
- Patrimônio Líquido 
(j) | None | 140246 | 1367
- Passivo Total 
(k) = (i) + (j) | None | 140247 | 1367
- Obrigações por Operações Compromissadas 
(b) | Captações | 140230 | 1367
- Obrigações por Empréstimos e Repasses 
(d) | Captações | 140238 | 1367
- Captações 
(e) = (a) + (b) + (c) + (d) | Captações | 140239 | 1367
- Depósitos à Vista 
(a1) | Captações - Depósitos | 140222 | 1367
- Depósitos de Poupança 
(a2) | Captações - Depósitos | 140223 | 1367
- Depósitos Interfinanceiros 
(a3) | Captações - Depósitos | 140224 | 1367
- Depósitos a Prazo 
(a4) | Captações - Depósitos | 140225 | 1367
- Conta de Pagamento Pré-Paga 
(a5) | Captações - Depósitos | 140226 | 1367
- Depósitos Outros 
(a6) | Captações - Depósitos | 140227 | 1367
- Depósitos 
(a) | Captações - Depósitos | 140228 | 1367
- Letras de Crédito Imobiliário 
(c1) | Captações - Outros Instrumentos de Dívida | 140231 | 1367
- Letras de Crédito do Agronegócio 
(c2) | Captações - Outros Instrumentos de Dívida | 140232 | 1367
- Letras Financeiras 
(c3) | Captações - Outros Instrumentos de Dívida | 140233 | 1367
- Obrigações por Títulos e Valores Mobiliários no Exterior 
(c4) | Captações - Outros Instrumentos de Dívida | 140234 | 1367
- Demais instrumentos de dívida 
(c5) | Captações - Outros Instrumentos de Dívida | 140235 | 1367
- Outros Instrumentos de Dívida 
(c) | Captações - Outros Instrumentos de Dívida | 140236 | 1367

## Tipo de instituição 1, relatório 4

71084 valores, 1367 instituições, 52 colunas.
Campos: `TipoInstituicao`, `CodInst`, `AnoMes`, `NomeRelatorio`, `NumeroRelatorio`, `Grupo`, `Conta`, `NomeColuna`, `DescricaoColuna`, `Saldo`
Exemplo: {"TipoInstituicao": 1, "CodInst": "00068987", "AnoMes": "202506", "NomeRelatorio": "Demonstração de Resultado", "NumeroRelatorio": "4", "Grupo": null, "Conta": "140220", "NomeColuna": "Ativo Total", "DescricaoColuna": "[1000000009] + [2000000008]", "Saldo": 665476916.87}

Colunas (nome | grupo | conta | linhas):
- Ativo Total | None | 140220 | 1367
- Juros Sobre Capital Próprio de Cooperativas 
(aa) | None | 141861 | 1367
- Resultado antes da Tributação e Participações 
(w) = (k) + (l) + (v) | None | 141867 | 1367
- Imposto de Renda e Contribuição Social 
(x) | None | 141868 | 1367
- Participações no Lucro 
(y) | None | 141869 | 1367
- Lucro Líquido 
(z) = (w) + (x) + (y) | None | 141870 | 1367
- Rendas de Tarifas Bancárias 
(m) | Outras Receitas / Despesas | 141856 | 1367
- Outras Rendas de Prestação de Serviços 
(n) | Outras Receitas / Despesas | 141857 | 1367
- Despesas de Pessoal 
(o) | Outras Receitas / Despesas | 141858 | 1367
- Despesas Administrativas 
(p) | Outras Receitas / Despesas | 141859 | 1367
- Resultado com Perdas Esperadas de Outras Operações 
(q) | Outras Receitas / Despesas | 141860 | 1367
- Despesas Tributárias 
(r) | Outras Receitas / Despesas | 141862 | 1367
- Resultado de Participações 
(s) | Outras Receitas / Despesas | 141863 | 1367
- Outras Receitas 
(t) | Outras Receitas / Despesas | 141864 | 1367
- Outras Despesas 
(u) | Outras Receitas / Despesas | 141865 | 1367
- Outras Receitas / Despesas 
(v)= (m) + (n) + (o) +  (p) + (q) + (r) + (s) + (t) + (u) | Outras Receitas / Despesas | 141866 | 1367
- Resultado com Serviços por Transações de Pagamento 
(l1) | Resultado com Transações de Pagamento | 141852 | 1367
- Resultados de Perda Esperada com Transações de Pagamento 
(l2) | Resultado com Transações de Pagamento | 141853 | 1367
- Outros Resultados com Transações de Pagamento 
(l3) | Resultado com Transações de Pagamento | 141854 | 1367
- Resultado com Transações de Pagamento 
(l) | Resultado com Transações de Pagamento | 141855 | 1367
- Rendas de Arrendamento Financeiro 
(d) | Resultado de Intermediação Financeira | 141836 | 1367
- Rendas de Outras Operações com Características de Concessão de Crédito 
(e) | Resultado de Intermediação Financeira | 141837 | 1367
- Despesas de Instrumentos de Dívida Elegíveis a Capital 
(h) | Resultado de Intermediação Financeira | 141848 | 1367
- Resultado com Derivativos 
(i) | Resultado de Intermediação Financeira | 141849 | 1367
- Outros Resultados de Intermediação Financeira 
(j) | Resultado de Intermediação Financeira | 141850 | 1367
- Resultado de Intermediação Financeira 
(k) = (a) + (b) + (c) + (d) + (e) + (f) + (g) + (h) + (i) + (j) | Resultado de Intermediação Financeira | 141851 | 1367
- Despesa de Juros com Captações 
(g1) | Resultado de Intermediação Financeira - Despesas de Captações | 141843 | 1367
- Ajuste de Variação Cambial de Captações 
(g2) | Resultado de Intermediação Financeira - Despesas de Captações | 141844 | 1367
- Ajuste de Hedge de Valor Justo de Captações 
(g3) | Resultado de Intermediação Financeira - Despesas de Captações | 141845 | 1367
- Outros Resultados de Captações 
(g4) | Resultado de Intermediação Financeira - Despesas de Captações | 141846 | 1367
- Despesas de Captações 
(g) | Resultado de Intermediação Financeira - Despesas de Captações | 141847 | 1367
- Receita de Juros com Aplicações Interfinanceiras de Liquidez 
(a1) | Resultado de Intermediação Financeira - Rendas de Aplicações Interfinanceiras de Liquidez | 141821 | 1367
- Ajuste de Variação Cambial de Aplicações Interfinanceiras de Liquidez 
(a2) | Resultado de Intermediação Financeira - Rendas de Aplicações Interfinanceiras de Liquidez | 141822 | 1367
- Ajuste a Valor Justo e Ajuste de Hedge de Valor Justo de Aplicações Interfinanceiras de Liquidez 
(a3) | Resultado de Intermediação Financeira - Rendas de Aplicações Interfinanceiras de Liquidez | 141823 | 1367
- Rendas de Aplicações Interfinanceiras de Liquidez 
(a) | Resultado de Intermediação Financeira - Rendas de Aplicações Interfinanceiras de Liquidez | 141825 | 1367
- Receita de Juros com Operações de Crédito 
(c1) | Resultado de Intermediação Financeira - Rendas de Operações de Crédito | 141831 | 1367
- Ajuste de Variação Cambial de Operações de Crédito 
(c2) | Resultado de Intermediação Financeira - Rendas de Operações de Crédito | 141832 | 1367
- Ajuste a Valor Justo e Ajuste de Hedge de Valor Justo de Operações de Crédito 
(c3) | Resultado de Intermediação Financeira - Rendas de Operações de Crédito | 141833 | 1367
- Outros Resultados de Operações de Crédito 
(c4) | Resultado de Intermediação Financeira - Rendas de Operações de Crédito | 141834 | 1367
- Rendas de Operações de Crédito 
(c) | Resultado de Intermediação Financeira - Rendas de Operações de Crédito | 141835 | 1367
- Receita de Juros com TVM 
(b1) | Resultado de Intermediação Financeira - Rendas de Títulos e Valores Mobiliários | 141826 | 1367
- Ajuste de Variação Cambial de TVM 
(b2) | Resultado de Intermediação Financeira - Rendas de Títulos e Valores Mobiliários | 141827 | 1367
- Ajuste a Valor Justo e Ajuste de Hedge de Valor Justo de TVM 
(b3) | Resultado de Intermediação Financeira - Rendas de Títulos e Valores Mobiliários | 141828 | 1367
- Outros Resultados de TVM 
(b4) | Resultado de Intermediação Financeira - Rendas de Títulos e Valores Mobiliários | 141829 | 1367
- Rendas de Títulos e Valores Mobiliários 
(b) | Resultado de Intermediação Financeira - Rendas de Títulos e Valores Mobiliários | 141830 | 1367
- Resultado com Perda Esperada de Aplicações Interfinanceiras de Liquidez 
(f1) | Resultado de Intermediação Financeira - Resultado com Perda Esperada | 141838 | 1367
- Resultado com Perda Esperada de TVM 
(f2) | Resultado de Intermediação Financeira - Resultado com Perda Esperada | 141839 | 1367
- Resultado com Perda Esperada de Operações de Crédito 
(f3) | Resultado de Intermediação Financeira - Resultado com Perda Esperada | 141840 | 1367
- Resultado com Perda Esperada de Outros Ativos Geradores de Renda 
(f6) | Resultado de Intermediação Financeira - Resultado com Perda Esperada | 141841 | 1367
- Resultado com Perda Esperada 
(f) | Resultado de Intermediação Financeira - Resultado com Perda Esperada | 141842 | 1367
- Resultado com Perda Esperada de Arrendamento 
(f4) | Resultado de Intermediação Financeira - Resultado com Perda Esperada | 142851 | 1367
- Resultado com Perda Esperada de Outras Operações com Características de Concessão de Crédito
(f5) | Resultado de Intermediação Financeira - Resultado com Perda Esperada | 142852 | 1367

## Tipo de instituição 1, relatório 5

32808 valores, 1367 instituições, 24 colunas.
Campos: `TipoInstituicao`, `CodInst`, `AnoMes`, `NomeRelatorio`, `NumeroRelatorio`, `Grupo`, `Conta`, `NomeColuna`, `DescricaoColuna`, `Saldo`
Exemplo: {"TipoInstituicao": 1, "CodInst": "00068987", "AnoMes": "202506", "NomeRelatorio": "Informações de Capital", "NumeroRelatorio": "5", "Grupo": null, "Conta": "79658", "NomeColuna": "Exposição Total \n(k)", "DescricaoColuna": "Exposição Total, sem ponderação de risco, conforme definido na Circular n° 3.748 de 27 de fevereiro de 2015", "Saldo": null}

Colunas (nome | grupo | conta | linhas):
- Exposição Total 
(k) | None | 79658 | 1367
- Índice de Capital Principal 
(l) = (a) / (j) | None | 79659 | 1367
- Índice de Capital Nível I 
(m) = (c) / (j) | None | 79660 | 1367
- Razão de Alavancagem 
(o) = (c) / (k) | None | 79661 | 1367
- Índice de Imobilização 
(p) | None | 79662 | 1367
- Índice de Basileia 
(n) = (e) / (j) | None | 79664 | 1367
- Adicional de Capital Principal | None | 92999 | 1367
- IRRBB | None | 98576 | 1367
- RWAsp 
(i) | Ativos Ponderados pelo Risco (RWA) | 134461 | 1367
- RWA para Risco de Crédito 
(f) | Ativos Ponderados pelo Risco (RWA) | 138232 | 1367
- RWA para Risco Operacional 
(h) | Ativos Ponderados pelo Risco (RWA) | 79656 | 1367
- Ativos Ponderados pelo Risco (RWA) 
(j) = (f) + (g) + (h) + (i) | Ativos Ponderados pelo Risco (RWA) | 79665 | 1367
- RWAcva 
(g5) | Ativos Ponderados pelo Risco (RWA) - RWA para Risco de Mercado | 134460 | 1367
- RWAdrc 
(g6) | Ativos Ponderados pelo Risco (RWA) - RWA para Risco de Mercado | 142840 | 1367
- RWA para Risco de Mercado 
(g) = (g1) + (g2) + (g3) + (g4) + (g5) + (g6) | Ativos Ponderados pelo Risco (RWA) - RWA para Risco de Mercado | 79651 | 1367
- RWAcam 
(g1) | Ativos Ponderados pelo Risco (RWA) - RWA para Risco de Mercado | 79652 | 1367
- RWAcom 
(g2) | Ativos Ponderados pelo Risco (RWA) - RWA para Risco de Mercado | 79653 | 1367
- RWAjur 
(g3) | Ativos Ponderados pelo Risco (RWA) - RWA para Risco de Mercado | 79654 | 1367
- RWAacs 
(g4) | Ativos Ponderados pelo Risco (RWA) - RWA para Risco de Mercado | 79655 | 1367
- Capital Nível II 
(d) | Patrimônio de Referência para Comparação com o RWA | 79648 | 1367
- Patrimônio de Referência para Comparação com o RWA 
(e) | Patrimônio de Referência para Comparação com o RWA | 79649 | 1367
- Capital Principal para Comparação com RWA 
(a) | Patrimônio de Referência para Comparação com o RWA - Patrimônio de Referência Nível I para Comparação com RWA | 79645 | 1367
- Capital Complementar 
(b) | Patrimônio de Referência para Comparação com o RWA - Patrimônio de Referência Nível I para Comparação com RWA | 79646 | 1367
- Patrimônio de Referência Nível I para Comparação com RWA 
(c) = (a) + (b) | Patrimônio de Referência para Comparação com o RWA - Patrimônio de Referência Nível I para Comparação com RWA | 79647 | 1367

## Tipo de instituição 1, relatório 6

5468 valores, 1367 instituições, 4 colunas.
Campos: `TipoInstituicao`, `CodInst`, `AnoMes`, `NomeRelatorio`, `NumeroRelatorio`, `Grupo`, `Conta`, `NomeColuna`, `DescricaoColuna`, `Saldo`
Exemplo: {"TipoInstituicao": 1, "CodInst": "00068987", "AnoMes": "202506", "NomeRelatorio": "Segmentação", "NumeroRelatorio": "6", "Grupo": null, "Conta": "148471", "NomeColuna": "Instituição Sujeita à \nApuração da Exposição Total", "DescricaoColuna": "Para cálculo do porte da instituição é considerada a exposição total, calculada conforme metodologia definida pelo Banco Central do Brasil. Se a instituição não for sujeita a apuração da exposição total, deve substituir pelo valor do ativo total (art 3º, Res 4553/2017)", "Saldo": 0.0}

Colunas (nome | grupo | conta | linhas):
- Instituição Sujeita à 
Apuração da Exposição Total | None | 148471 | 1367
- Exposição Total ou Ativo Total 
(R$ mil) | None | 148474 | 1367
- Total de Ativos Consolidados no Exterior 
(US$ mil) | None | 148475 | 1367
- Instituição Utiliza 
Metodologia Simplificada | None | 149619 | 1367

## Tipo de instituição 1, relatório 7

28707 valores, 1367 instituições, 21 colunas.
Campos: `TipoInstituicao`, `CodInst`, `AnoMes`, `NomeRelatorio`, `NumeroRelatorio`, `Grupo`, `Conta`, `NomeColuna`, `DescricaoColuna`, `Saldo`
Exemplo: {"TipoInstituicao": 1, "CodInst": "00068987", "AnoMes": "202506", "NomeRelatorio": "Carteira de crédito ativa - por indexador", "NumeroRelatorio": "7", "Grupo": null, "Conta": "107030", "NomeColuna": "TCR pré", "DescricaoColuna": "Volume das operações de crédito com indexador TCR pré", "Saldo": null}

Colunas (nome | grupo | conta | linhas):
- TCR pré | None | 107030 | 1367
- TCR pós | None | 112607 | 1367
- TRFC pré | None | 112608 | 1367
- TRFC pós | None | 112609 | 1367
- Prefixado | None | 23367 | 1367
- TR / TBF | None | 23368 | 1367
- TJLP | None | 23369 | 1367
- Libor | None | 23370 | 1367
- Outras Taxas Pós-Fixadas | None | 23371 | 1367
- Carteira ativa com indexador CDI | None | 23372 | 1367
- SELIC | None | 23373 | 1367
- Outras Taxas Flutuantes | None | 23374 | 1367
- IGPM | None | 23375 | 1367
- IPCA | None | 23376 | 1367
- IPCC | None | 23377 | 1367
- Outros Índices de Preço | None | 23378 | 1367
- Outros Indexadores | None | 23379 | 1367
- Total Exterior | None | 23383 | 1367
- Total Geral | None | 24454 | 1367
- Total não Individualizado | None | 24457 | 1367
- TLP | None | 94951 | 1367

## Tipo 1, relatório 8: sem dados (vazio)

## Tipo de instituição 1, relatório 9

10936 valores, 1367 instituições, 8 colunas.
Campos: `TipoInstituicao`, `CodInst`, `AnoMes`, `NomeRelatorio`, `NumeroRelatorio`, `Grupo`, `Conta`, `NomeColuna`, `DescricaoColuna`, `Saldo`
Exemplo: {"TipoInstituicao": 1, "CodInst": "00068987", "AnoMes": "202506", "NomeRelatorio": "Carteira de crédito ativa - por região geográfica", "NumeroRelatorio": "9", "Grupo": null, "Conta": "23358", "NomeColuna": "Sudeste", "DescricaoColuna": "Volume das operações de crédito realizadas na região Sudeste", "Saldo": 249261316.82}

Colunas (nome | grupo | conta | linhas):
- Sudeste | None | 23358 | 1367
- Centro-oeste | None | 23359 | 1367
- Nordeste | None | 23360 | 1367
- Norte | None | 23361 | 1367
- Sul | None | 23362 | 1367
- Total Exterior | None | 23383 | 1367
- Região não Informada | None | 24449 | 1367
- Total Geral | None | 24454 | 1367

## Tipo de instituição 1, relatório 10

2734 valores, 1367 instituições, 2 colunas.
Campos: `TipoInstituicao`, `CodInst`, `AnoMes`, `NomeRelatorio`, `NumeroRelatorio`, `Grupo`, `Conta`, `NomeColuna`, `DescricaoColuna`, `Saldo`
Exemplo: {"TipoInstituicao": 1, "CodInst": "00068987", "AnoMes": "202506", "NomeRelatorio": "Carteira de crédito ativa - quantidade de clientes e de operações", "NumeroRelatorio": "10", "Grupo": null, "Conta": "113786", "NomeColuna": "Quantidade de clientes com operações ativas", "DescricaoColuna": "O total de clientes é calculado para os clientes, que possuam carteira ativa, identificados, ou seja, aqueles possuidores de dívidas acima do limite de individualização do SCR. A porção agregada das informações constantes do documento 3040 não está refletida nesse número.", "Saldo": 5753.0}

Colunas (nome | grupo | conta | linhas):
- Quantidade de clientes com operações ativas | None | 113786 | 1367
- Quantidade de operações ativas | None | 113787 | 1367

## Tipo de instituição 1, relatório 11

79286 valores, 1367 instituições, 58 colunas.
Campos: `TipoInstituicao`, `CodInst`, `AnoMes`, `NomeRelatorio`, `NumeroRelatorio`, `Grupo`, `Conta`, `NomeColuna`, `DescricaoColuna`, `Saldo`
Exemplo: {"TipoInstituicao": 1, "CodInst": "00068987", "AnoMes": "202506", "NomeRelatorio": "Carteira de crédito ativa Pessoa Física - modalidade e prazo de vencimento", "NumeroRelatorio": "11", "Grupo": null, "Conta": "23385", "NomeColuna": "Total Exterior Pessoa Física", "DescricaoColuna": "Volume das operações de crédito realizadas por IFs brasileiras no exterior para pessoas físicas.", "Saldo": null}

Colunas (nome | grupo | conta | linhas):
- Total Exterior Pessoa Física | None | 23385 | 1367
- Total da Carteira de Pessoa Física | None | 24452 | 1367
- A Vencer Entre 1081 a 1800 Dias | Cartão de Crédito | 23236 | 1367
- Vencido a Partir de 15 Dias | Cartão de Crédito | 23237 | 1367
- A Vencer Entre 1801 a 5400 Dias | Cartão de Crédito | 23238 | 1367
- A Vencer Entre 361 a 1080 Dias | Cartão de Crédito | 23239 | 1367
- A Vencer em até 90 Dias | Cartão de Crédito | 23240 | 1367
- A Vencer Entre 91 a 360 Dias | Cartão de Crédito | 23241 | 1367
- A vencer Acima de 5400 Dias | Cartão de Crédito | 23242 | 1367
- Total | Cartão de Crédito | 23243 | 1367
- A Vencer Entre 1081 a 1800 Dias | Empréstimo com Consignação em Folha | 23220 | 1367
- Vencido a Partir de 15 Dias | Empréstimo com Consignação em Folha | 23221 | 1367
- A Vencer Entre 1801 a 5400 Dias | Empréstimo com Consignação em Folha | 23222 | 1367
- A Vencer Entre 361 a 1080 Dias | Empréstimo com Consignação em Folha | 23223 | 1367
- A Vencer em até 90 Dias | Empréstimo com Consignação em Folha | 23224 | 1367
- A Vencer Entre 91 a 360 Dias | Empréstimo com Consignação em Folha | 23225 | 1367
- A vencer Acima de 5400 Dias | Empréstimo com Consignação em Folha | 23226 | 1367
- Total | Empréstimo com Consignação em Folha | 23227 | 1367
- A Vencer Entre 1081 a 1800 Dias | Empréstimo sem Consignação em Folha | 23228 | 1367
- Vencido a Partir de 15 Dias | Empréstimo sem Consignação em Folha | 23229 | 1367
- A Vencer Entre 1801 a 5400 Dias | Empréstimo sem Consignação em Folha | 23230 | 1367
- A Vencer Entre 361 a 1080 Dias | Empréstimo sem Consignação em Folha | 23231 | 1367
- A Vencer em até 90 Dias | Empréstimo sem Consignação em Folha | 23232 | 1367
- A Vencer Entre 91 a 360 Dias | Empréstimo sem Consignação em Folha | 23233 | 1367
- A vencer Acima de 5400 Dias | Empréstimo sem Consignação em Folha | 23234 | 1367
- Total | Empréstimo sem Consignação em Folha | 23235 | 1367
- A Vencer Entre 1081 a 1800 Dias | Habitação | 23252 | 1367
- Vencido a Partir de 15 Dias | Habitação | 23253 | 1367
- A Vencer Entre 1801 a 5400 Dias | Habitação | 23254 | 1367
- A Vencer Entre 361 a 1080 Dias | Habitação | 23255 | 1367
- A Vencer em até 90 Dias | Habitação | 23256 | 1367
- A Vencer Entre 91 a 360 Dias | Habitação | 23257 | 1367
- A vencer Acima de 5400 Dias | Habitação | 23258 | 1367
- Total | Habitação | 23259 | 1367
- A Vencer Entre 1081 a 1800 Dias | Outros Créditos | 23268 | 1367
- Vencido a Partir de 15 Dias | Outros Créditos | 23269 | 1367
- A Vencer Entre 1801 a 5400 Dias | Outros Créditos | 23270 | 1367
- A Vencer Entre 361 a 1080 Dias | Outros Créditos | 23271 | 1367
- A Vencer em até 90 Dias | Outros Créditos | 23272 | 1367
- A Vencer Entre 91 a 360 Dias | Outros Créditos | 23273 | 1367
- A vencer Acima de 5400 Dias | Outros Créditos | 23274 | 1367
- Total | Outros Créditos | 23275 | 1367
- A Vencer Entre 1081 a 1800 dias | Rural e Agroindustrial | 23260 | 1367
- Vencido a Partir de 15 Dias | Rural e Agroindustrial | 23261 | 1367
- A Vencer Entre 1801 a 5400 Dias | Rural e Agroindustrial | 23262 | 1367
- A Vencer Entre 361 a 1080 Dias | Rural e Agroindustrial | 23263 | 1367
- A Vencer em até 90 Dias | Rural e Agroindustrial | 23264 | 1367
- A Vencer Entre 91 a 360 Dias | Rural e Agroindustrial | 23265 | 1367
- A Vencer Acima de 5400 Dias | Rural e Agroindustrial | 23266 | 1367
- Total | Rural e Agroindustrial | 23267 | 1367
- A Vencer Entre 1081 a 1800 Dias | Veículos | 23244 | 1367
- Vencido a Partir de 15 Dias | Veículos | 23245 | 1367
- A Vencer Entre 1801 a 5400 Dias | Veículos | 23246 | 1367
- A Vencer Entre 361 a 1080 Dias | Veículos | 23247 | 1367
- A Vencer em até 90 Dias | Veículos | 23248 | 1367
- A Vencer Entre 91 a 360 Dias | Veículos | 23249 | 1367
- A vencer Acima de 5400 Dias | Veículos | 23250 | 1367
- Total | Veículos | 23251 | 1367

## Tipo de instituição 1, relatório 12

100000 valores, 1316 instituições, 76 colunas.
Campos: `TipoInstituicao`, `CodInst`, `AnoMes`, `NomeRelatorio`, `NumeroRelatorio`, `Grupo`, `Conta`, `NomeColuna`, `DescricaoColuna`, `Saldo`
Exemplo: {"TipoInstituicao": 1, "CodInst": "00068987", "AnoMes": "202506", "NomeRelatorio": "Carteira de crédito ativa Pessoa Jurídica -  por atividade econômica (CNAE)", "NumeroRelatorio": "12", "Grupo": null, "Conta": "23386", "NomeColuna": "Total Exterior Pessoa Jurídica", "DescricaoColuna": "Volume das operações de crédito realizadas IFs brasileiras no exterior para pessoas jurídicas.", "Saldo": null}

Colunas (nome | grupo | conta | linhas):
- Total Exterior Pessoa Jurídica | None | 23386 | 1316
- Atividade não Informada ou não se Aplica | None | 24447 | 1316
- Total da Carteira de Pessoa Jurídica | None | 24453 | 1316
- Total não Individualizado Pessoa Jurídica | None | 24459 | 1316
- A Vencer Entre 1081 a 1800 Dias | Administração Pública, Defesa e Seguridade Social | 23156 | 1316
- Vencido a Partir de 15 Dias | Administração Pública, Defesa e Seguridade Social | 23157 | 1316
- A Vencer Entre 1801 a 5400 Dias | Administração Pública, Defesa e Seguridade Social | 23158 | 1316
- A Vencer Entre 361 a 1080 Dias | Administração Pública, Defesa e Seguridade Social | 23159 | 1316
- A Vencer em 90 Dias | Administração Pública, Defesa e Seguridade Social | 23160 | 1316
- A Vencer Entre 91 a 360 Dias | Administração Pública, Defesa e Seguridade Social | 23161 | 1316
- A vencer Acima de 5400 Dias | Administração Pública, Defesa e Seguridade Social | 23162 | 1316
- Total | Administração Pública, Defesa e Seguridade Social | 23163 | 1316
- A Vencer Entre 1081 a 1800 Dias | Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura | 23044 | 1316
- Vencido a Partir de 15 Dias | Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura | 23045 | 1316
- A Vencer Entre 1801 a 5400 Dias | Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura | 23046 | 1316
- A Vencer Entre 361 a 1080 Dias | Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura | 23047 | 1316
- A Vencer em 90 Dias | Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura | 23048 | 1316
- A Vencer Entre 91 a 360 Dias | Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura | 23049 | 1316
- A vencer Acima de 5400 Dias | Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura | 23050 | 1316
- Total | Agricultura, Pecuária, Produção Florestal, Pesca e Aquicultura | 23051 | 1316
- A Vencer Entre 1081 a 1800 Dias | Comércio, Reparação de Veículos Automotores e Motocicletas | 23092 | 1316
- Vencido a Partir de 15 Dias | Comércio, Reparação de Veículos Automotores e Motocicletas | 23093 | 1316
- A Vencer Entre 1801 a 5400 Dias | Comércio, Reparação de Veículos Automotores e Motocicletas | 23094 | 1316
- A Vencer Entre 361 a 1080 Dias | Comércio, Reparação de Veículos Automotores e Motocicletas | 23095 | 1316
- A Vencer em 90 Dias | Comércio, Reparação de Veículos Automotores e Motocicletas | 23096 | 1316
- A Vencer Entre 91 a 360 Dias | Comércio, Reparação de Veículos Automotores e Motocicletas | 23097 | 1316
- A vencer Acima de 5400 Dias | Comércio, Reparação de Veículos Automotores e Motocicletas | 23098 | 1316
- Total | Comércio, Reparação de Veículos Automotores e Motocicletas | 23099 | 1316
- A Vencer Entre 1081 a 1800 Dias | Construção | 23084 | 1316
- Vencido a Partir de 15 Dias | Construção | 23085 | 1316
- A Vencer Entre 1801 a 5400 Dias | Construção | 23086 | 1316
- A Vencer Entre 361 a 1080 Dias | Construção | 23087 | 1316
- A Vencer em 90 Dias | Construção | 23088 | 1316
- A Vencer Entre 91 a 360 Dias | Construção | 23089 | 1316
- A vencer Acima de 5400 Dias | Construção | 23090 | 1316
- Total | Construção | 23091 | 1316
- A Vencer Entre 1081 a 1800 Dias | Indústrias de Transformação | 23060 | 1316
- Vencido a Partir de 15 Dias | Indústrias de Transformação | 23061 | 1316
- A Vencer Entre 1801 a 5400 Dias | Indústrias de Transformação | 23062 | 1316
- A Vencer Entre 361 a 1080 Dias | Indústrias de Transformação | 23063 | 1316
- A Vencer em 90 Dias | Indústrias de Transformação | 23064 | 1316
- A Vencer Entre 91 a 360 Dias | Indústrias de Transformação | 23065 | 1316
- A vencer Acima de 5400 Dias | Indústrias de Transformação | 23066 | 1316
- Total | Indústrias de Transformação | 23067 | 1316
- A Vencer Entre 1081 a 1800 Dias | Industrias Extrativas | 23052 | 1316
- Vencido a Partir de 15 Dias | Industrias Extrativas | 23053 | 1316
- A Vencer Entre 1801 a 5400 Dias | Industrias Extrativas | 23054 | 1316
- A Vencer Entre 361 a 1080 Dias | Industrias Extrativas | 23055 | 1316
- A Vencer em 90 Dias | Industrias Extrativas | 23056 | 1316
- A Vencer Entre 91 a 360 Dias | Industrias Extrativas | 23057 | 1316
- A vencer Acima de 5400 Dias | Industrias Extrativas | 23058 | 1316
- Total | Industrias Extrativas | 23059 | 1316
- Vencido a Partir de 15 Dias | Outros | 42785 | 1316
- A Vencer em 90 Dias | Outros | 42786 | 1316
- A Vencer Entre 91 a 360 Dias | Outros | 42787 | 1316
- A Vencer Entre 361 a 1080 Dias | Outros | 42788 | 1316
- a Vencer entre 1081 e 1800 Dias | Outros | 42789 | 1316
- A Vencer Entre 1801 a 5400 Dias | Outros | 42790 | 1316
- A vencer Acima de 5400 Dias | Outros | 42791 | 1316
- Total | Outros | 42792 | 1316
- Vencido a Partir de 15 Dias | Serviços Industriais de Utilidade Pública | 42777 | 1315
- A Vencer em 90 Dias | Serviços Industriais de Utilidade Pública | 42778 | 1315
- A Vencer Entre 91 a 360 Dias | Serviços Industriais de Utilidade Pública | 42779 | 1315
- A Vencer Entre 361 a 1080 Dias | Serviços Industriais de Utilidade Pública | 42780 | 1315
- a Vencer entre 1081 e 1800 Dias | Serviços Industriais de Utilidade Pública | 42781 | 1315
- A Vencer Entre 1801 a 5400 Dias | Serviços Industriais de Utilidade Pública | 42782 | 1315
- A vencer Acima de 5400 Dias | Serviços Industriais de Utilidade Pública | 42783 | 1315
- Total | Serviços Industriais de Utilidade Pública | 42784 | 1315
- A Vencer Entre 1081 a 1800 Dias | Transporte, Armazenagem e Correio | 23100 | 1315
- Vencido a Partir de 15 Dias | Transporte, Armazenagem e Correio | 23101 | 1315
- A Vencer Entre 1801 a 5400 Dias | Transporte, Armazenagem e Correio | 23102 | 1315
- A Vencer Entre 361 a 1080 Dias | Transporte, Armazenagem e Correio | 23103 | 1315
- A Vencer em 90 Dias | Transporte, Armazenagem e Correio | 23104 | 1315
- A Vencer Entre 91 a 360 Dias | Transporte, Armazenagem e Correio | 23105 | 1315
- A vencer Acima de 5400 Dias | Transporte, Armazenagem e Correio | 23106 | 1315
- Total | Transporte, Armazenagem e Correio | 23107 | 1315

## Tipo de instituição 1, relatório 13

100000 valores, 1352 instituições, 74 colunas.
Campos: `TipoInstituicao`, `CodInst`, `AnoMes`, `NomeRelatorio`, `NumeroRelatorio`, `Grupo`, `Conta`, `NomeColuna`, `DescricaoColuna`, `Saldo`
Exemplo: {"TipoInstituicao": 1, "CodInst": "00068987", "AnoMes": "202506", "NomeRelatorio": "Carteira de crédito ativa Pessoa Jurídica - modalidade e prazo de vencimento", "NumeroRelatorio": "13", "Grupo": null, "Conta": "23386", "NomeColuna": "Total Exterior Pessoa Jurídica", "DescricaoColuna": "Volume das operações de crédito realizadas IFs brasileiras no exterior para pessoas jurídicas.", "Saldo": null}

Colunas (nome | grupo | conta | linhas):
- Total Exterior Pessoa Jurídica | None | 23386 | 1352
- Total da Carteira de Pessoa Jurídica | None | 24453 | 1352
- A Vencer Entre 1081 a 1800 Dias | Capital de Giro | 23276 | 1352
- Vencido a Partir de 15 Dias | Capital de Giro | 23277 | 1352
- A Vencer Entre 1801 a 5400 Dias | Capital de Giro | 23278 | 1352
- A Vencer Entre 361 a 1080 Dias | Capital de Giro | 23279 | 1352
- A Vencer em até 90 Dias | Capital de Giro | 23280 | 1352
- A Vencer Entre 91 a 360 Dias | Capital de Giro | 23281 | 1352
- A vencer Acima de 5400 Dias | Capital de Giro | 23282 | 1352
- Total | Capital de Giro | 23283 | 1352
- A Vencer Entre 1081 a 1800 Dias | Cheque Especial e Conta Garantida | 23284 | 1352
- Vencido a Partir de 15 Dias | Cheque Especial e Conta Garantida | 23285 | 1352
- A Vencer Entre 1801 a 5400 Dias | Cheque Especial e Conta Garantida | 23286 | 1352
- A Vencer Entre 361 a 1080 Dias | Cheque Especial e Conta Garantida | 23287 | 1352
- A Vencer em até 90 Dias | Cheque Especial e Conta Garantida | 23288 | 1352
- A Vencer Entre 91 a 360 Dias | Cheque Especial e Conta Garantida | 23289 | 1352
- A vencer Acima de 5400 Dias | Cheque Especial e Conta Garantida | 23290 | 1352
- Total | Cheque Especial e Conta Garantida | 23291 | 1352
- A Vencer Entre 1081 a 1800 Dias | Comércio Exterior | 23332 | 1352
- Vencido a Partir de 15 Dias | Comércio Exterior | 23333 | 1352
- A Vencer Entre 1801 a 5400 Dias | Comércio Exterior | 23334 | 1352
- A Vencer Entre 361 a 1080 Dias | Comércio Exterior | 23335 | 1352
- A Vencer em até 90 Dias | Comércio Exterior | 23336 | 1352
- A Vencer Entre 91 a 360 Dias | Comércio Exterior | 23337 | 1352
- A vencer Acima de 5400 Dias | Comércio Exterior | 23338 | 1352
- Total | Comércio Exterior | 23339 | 1352
- A Vencer Entre 1081 a 1800 Dias | Financiamento de Infraestrutura/Desenvolvimento/Projeto e Outros Créditos | 23308 | 1351
- Vencido a Partir de 15 Dias | Financiamento de Infraestrutura/Desenvolvimento/Projeto e Outros Créditos | 23309 | 1351
- A Vencer Entre 1801 a 5400 Dias | Financiamento de Infraestrutura/Desenvolvimento/Projeto e Outros Créditos | 23310 | 1351
- A Vencer Entre 361 a 1080 Dias | Financiamento de Infraestrutura/Desenvolvimento/Projeto e Outros Créditos | 23311 | 1351
- A Vencer em até 90 Dias | Financiamento de Infraestrutura/Desenvolvimento/Projeto e Outros Créditos | 23312 | 1351
- A Vencer Entre 91 a 360 Dias | Financiamento de Infraestrutura/Desenvolvimento/Projeto e Outros Créditos | 23313 | 1351
- A vencer Acima de 5400 Dias | Financiamento de Infraestrutura/Desenvolvimento/Projeto e Outros Créditos | 23314 | 1351
- Total | Financiamento de Infraestrutura/Desenvolvimento/Projeto e Outros Créditos | 23315 | 1351
- A Vencer Entre 1081 a 1800 Dias | Habitacional | 23316 | 1351
- Vencido a Partir de 15 Dias | Habitacional | 23317 | 1351
- A Vencer Entre 1801 a 5400 Dias | Habitacional | 23318 | 1351
- A Vencer Entre 361 a 1080 Dias | Habitacional | 23319 | 1351
- A Vencer em até 90 Dias | Habitacional | 23320 | 1351
- A Vencer Entre 91 a 360 Dias | Habitacional | 23321 | 1351
- A vencer Acima de 5400 Dias | Habitacional | 23322 | 1351
- Total | Habitacional | 23323 | 1351
- A Vencer Entre 1081 a 1800 Dias | Investimento | 23292 | 1351
- Vencido a Partir de 15 Dias | Investimento | 23293 | 1351
- A Vencer Entre 1801 a 5400 Dias | Investimento | 23294 | 1351
- A Vencer Entre 361 a 1080 Dias | Investimento | 23295 | 1351
- A Vencer em até 90 Dias | Investimento | 23296 | 1351
- A Vencer Entre 91 a 360 Dias | Investimento | 23297 | 1351
- A vencer Acima de 5400 Dias | Investimento | 23298 | 1351
- Total | Investimento | 23299 | 1351
- A Vencer Entre 1081 a 1800 Dias | Operações com Recebíveis | 23300 | 1351
- Vencido a Partir de 15 Dias | Operações com Recebíveis | 23301 | 1351
- A Vencer Entre 1801 a 5400 Dias | Operações com Recebíveis | 23302 | 1351
- A Vencer Entre 361 a 1080 Dias | Operações com Recebíveis | 23303 | 1351
- A Vencer em até 90 Dias | Operações com Recebíveis | 23304 | 1351
- A Vencer Entre 91 a 360 Dias | Operações com Recebíveis | 23305 | 1351
- A vencer Acima de 5400 Dias | Operações com Recebíveis | 23306 | 1351
- Total | Operações com Recebíveis | 23307 | 1351
- A Vencer Entre 1081 a 1800 Dias | Outros Créditos | 23340 | 1351
- Vencido a Partir de 15 Dias | Outros Créditos | 23341 | 1351
- A Vencer Entre 1801 a 5400 Dias | Outros Créditos | 23342 | 1351
- A Vencer Entre 361 a 1080 Dias | Outros Créditos | 23343 | 1351
- A Vencer em até 90 Dias | Outros Créditos | 23344 | 1351
- A Vencer Entre 91 a 360 Dias | Outros Créditos | 23345 | 1351
- A vencer Acima de 5400 Dias | Outros Créditos | 23346 | 1351
- Total | Outros Créditos | 23347 | 1351
- A Vencer Entre 1081 a 1800 Dias | Rural e Agroindustrial | 23324 | 1351
- Vencido a Partir de 15 Dias | Rural e Agroindustrial | 23325 | 1351
- A Vencer Entre 1801 a 5400 Dias | Rural e Agroindustrial | 23326 | 1351
- A Vencer Entre 361 a 1080 Dias | Rural e Agroindustrial | 23327 | 1351
- A Vencer em até 90 Dias | Rural e Agroindustrial | 23328 | 1351
- A Vencer Entre 91 a 360 Dias | Rural e Agroindustrial | 23329 | 1351
- A vencer Acima de 5400 Dias | Rural e Agroindustrial | 23330 | 1351
- Total | Rural e Agroindustrial | 23331 | 1351

## Tipo de instituição 1, relatório 14

10936 valores, 1367 instituições, 8 colunas.
Campos: `TipoInstituicao`, `CodInst`, `AnoMes`, `NomeRelatorio`, `NumeroRelatorio`, `Grupo`, `Conta`, `NomeColuna`, `DescricaoColuna`, `Saldo`
Exemplo: {"TipoInstituicao": 1, "CodInst": "00068987", "AnoMes": "202506", "NomeRelatorio": "Carteira de crédito ativa Pessoa Jurídica - por porte do tomador", "NumeroRelatorio": "14", "Grupo": null, "Conta": "101484", "NomeColuna": "Indisponível", "DescricaoColuna": "Créditos com Classificação de Porte Indisponível", "Saldo": 1192009.93}

Colunas (nome | grupo | conta | linhas):
- Indisponível | None | 101484 | 1367
- Micro | None | 23363 | 1367
- Pequena | None | 23364 | 1367
- Média | None | 23365 | 1367
- Grande | None | 23366 | 1367
- Total Exterior Pessoa Jurídica | None | 23386 | 1367
- Total da Carteira de Pessoa Jurídica | None | 24453 | 1367
- Total não Individualizado Pessoa Jurídica | None | 24459 | 1367

## Tipo 1, relatório 15: sem dados (vazio)

## Tipo de instituição 1, relatório 16

15037 valores, 1367 instituições, 11 colunas.
Campos: `TipoInstituicao`, `CodInst`, `AnoMes`, `NomeRelatorio`, `NumeroRelatorio`, `Grupo`, `Conta`, `NomeColuna`, `DescricaoColuna`, `Saldo`
Exemplo: {"TipoInstituicao": 1, "CodInst": "00068987", "AnoMes": "202506", "NomeRelatorio": "Carteira de crédito ativa - por carteiras de instrumentos financeiros", "NumeroRelatorio": "16", "Grupo": null, "Conta": "148833", "NomeColuna": "Ativos problemáticos", "DescricaoColuna": "Carteira de ativos problemáticos", "Saldo": 41474964.07}

Colunas (nome | grupo | conta | linhas):
- Ativos problemáticos | None | 148833 | 1367
- Inadimplência | None | 148834 | 1367
- Carteira não Informada ou não se Aplica | None | 149385 | 1367
- Total Exterior | None | 23383 | 1367
- Total Geral | None | 24454 | 1367
- Total não Individualizado | None | 24457 | 1367
- C1 | Carteiras | 148835 | 1367
- C2 | Carteiras | 148836 | 1367
- C3 | Carteiras | 148837 | 1367
- C4 | Carteiras | 148838 | 1367
- C5 | Carteiras | 148839 | 1367

## Tipo de instituição 2, relatório 1

9982 valores, 1426 instituições, 7 colunas.
Campos: `TipoInstituicao`, `CodInst`, `AnoMes`, `NomeRelatorio`, `NumeroRelatorio`, `Grupo`, `Conta`, `NomeColuna`, `DescricaoColuna`, `Saldo`
Exemplo: {"TipoInstituicao": 2, "CodInst": "00068987", "AnoMes": "202506", "NomeRelatorio": "Resumo", "NumeroRelatorio": "1", "Grupo": null, "Conta": "140200", "NomeColuna": "Títulos e Valores Mobiliários", "DescricaoColuna": "[1300000008]-[1330000009]", "Saldo": 21752485.33}

Colunas (nome | grupo | conta | linhas):
- Títulos e Valores Mobiliários | None | 140200 | 1426
- Ativo Total | None | 140220 | 1426
- Captações | None | 140239 | 1426
- Passivo Exigível | None | 140244 | 1426
- Patrimônio Líquido | None | 140246 | 1426
- Lucro Líquido | None | 141870 | 1426
- Carteira de Crédito | None | 141873 | 1426

## Tipo de instituição 2, relatório 2

34224 valores, 1426 instituições, 24 colunas.
Campos: `TipoInstituicao`, `CodInst`, `AnoMes`, `NomeRelatorio`, `NumeroRelatorio`, `Grupo`, `Conta`, `NomeColuna`, `DescricaoColuna`, `Saldo`
Exemplo: {"TipoInstituicao": 2, "CodInst": "00068987", "AnoMes": "202506", "NomeRelatorio": "Ativo", "NumeroRelatorio": "2", "Grupo": null, "Conta": "140198", "NomeColuna": "Disponibilidades \n(a)", "DescricaoColuna": "[1100000002]", "Saldo": 5174236.99}

Colunas (nome | grupo | conta | linhas):
- Disponibilidades 
(a) | None | 140198 | 1426
- Aplicações Interfinanceiras de Liquidez 
(b) | None | 140199 | 1426
- Títulos e Valores Mobiliários 
(c) | None | 140200 | 1426
- Outros Ativos Realizáveis 
(i) | None | 140218 | 1426
- Ativo Permanente 
(j) | None | 140219 | 1426
- Ativo Total 
(k) = (a) + (b) + (c) + (d) + (e) + (f) + (g) + (h) + (i) + (j) | None | 140220 | 1426
- Instrumentos Derivativos (d) | None | 141612 | 1426
- Valor Contábil Bruto 
(f1) | Operações de Arrendamento Financeiro | 140207 | 1426
- Perda Esperada 
(f2) | Operações de Arrendamento Financeiro | 140208 | 1426
- Hedge de Valor Justo 
(f3) | Operações de Arrendamento Financeiro | 140209 | 1426
- Operações de Arrendamento Financeiro 
(f) | Operações de Arrendamento Financeiro | 140210 | 1426
- Valor Contábil Bruto 
(e1) | Operações de Crédito | 140201 | 1426
- Perda Esperada 
(e2) | Operações de Crédito | 140202 | 1426
- Hedge de Valor Justo 
(e3) | Operações de Crédito | 140203 | 1426
- Ajuste a Valor Justo 
(e4) | Operações de Crédito | 140204 | 1426
- Operações de Crédito 
(e) | Operações de Crédito | 140205 | 1426
- Valor Contábil Bruto 
(g1) | Outras Operações com Características de Concessão de Crédito | 140212 | 1426
- Perda Esperada 
(g2) | Outras Operações com Características de Concessão de Crédito | 140213 | 1426
- Hedge de Valor Justo 
(g3) | Outras Operações com Características de Concessão de Crédito | 140214 | 1426
- Ajuste a Valor Justo 
(g4) | Outras Operações com Características de Concessão de Crédito | 140215 | 1426
- Outras Operações com Características de Concessão de Crédito 
(g) | Outras Operações com Características de Concessão de Crédito | 140216 | 1426
- Valor Contábil Bruto 
(h1) | Valores a Receber de Transações de Pagamentos - Usuários Finais (Pós-pago) | 145831 | 1426
- Perda Esperada 
(h2) | Valores a Receber de Transações de Pagamentos - Usuários Finais (Pós-pago) | 145832 | 1426
- Valores a Receber de Transações de Pagamentos - Usuários Finais (Pós-pago) 
(h) | Valores a Receber de Transações de Pagamentos - Usuários Finais (Pós-pago) | 145833 | 1426

## Tipo de instituição 2, relatório 3

31372 valores, 1426 instituições, 22 colunas.
Campos: `TipoInstituicao`, `CodInst`, `AnoMes`, `NomeRelatorio`, `NumeroRelatorio`, `Grupo`, `Conta`, `NomeColuna`, `DescricaoColuna`, `Saldo`
Exemplo: {"TipoInstituicao": 2, "CodInst": "00068987", "AnoMes": "202506", "NomeRelatorio": "Passivo", "NumeroRelatorio": "3", "Grupo": null, "Conta": "140241", "NomeColuna": "Instrumentos Derivativos \n(f)", "DescricaoColuna": "[4700000007]", "Saldo": 0.0}

Colunas (nome | grupo | conta | linhas):
- Instrumentos Derivativos 
(f) | None | 140241 | 1426
- Outras Obrigações 
(g) | None | 140242 | 1426
- Instrumentos de Dívida Elegíveis a Capital 
(h) | None | 140243 | 1426
- Passivo Exigível 
(i) = (e) + (f) + (g) + (h) | None | 140244 | 1426
- Patrimônio Líquido 
(j) | None | 140246 | 1426
- Passivo Total 
(k) = (i) + (j) | None | 140247 | 1426
- Obrigações por Operações Compromissadas 
(b) | Captações | 140230 | 1426
- Obrigações por Empréstimos e Repasses 
(d) | Captações | 140238 | 1426
- Captações 
(e) = (a) + (b) + (c) + (d) | Captações | 140239 | 1426
- Depósitos à Vista 
(a1) | Captações - Depósitos | 140222 | 1426
- Depósitos de Poupança 
(a2) | Captações - Depósitos | 140223 | 1426
- Depósitos Interfinanceiros 
(a3) | Captações - Depósitos | 140224 | 1426
- Depósitos a Prazo 
(a4) | Captações - Depósitos | 140225 | 1426
- Conta de Pagamento Pré-Paga 
(a5) | Captações - Depósitos | 140226 | 1426
- Depósitos Outros 
(a6) | Captações - Depósitos | 140227 | 1426
- Depósitos 
(a) | Captações - Depósitos | 140228 | 1426
- Letras de Crédito Imobiliário 
(c1) | Captações - Outros Instrumentos de Dívida | 140231 | 1426
- Letras de Crédito do Agronegócio 
(c2) | Captações - Outros Instrumentos de Dívida | 140232 | 1426
- Letras Financeiras 
(c3) | Captações - Outros Instrumentos de Dívida | 140233 | 1426
- Obrigações por Títulos e Valores Mobiliários no Exterior 
(c4) | Captações - Outros Instrumentos de Dívida | 140234 | 1426
- Demais instrumentos de dívida 
(c5) | Captações - Outros Instrumentos de Dívida | 140235 | 1426
- Outros Instrumentos de Dívida 
(c) | Captações - Outros Instrumentos de Dívida | 140236 | 1426

## Tipo de instituição 2, relatório 4

74152 valores, 1426 instituições, 52 colunas.
Campos: `TipoInstituicao`, `CodInst`, `AnoMes`, `NomeRelatorio`, `NumeroRelatorio`, `Grupo`, `Conta`, `NomeColuna`, `DescricaoColuna`, `Saldo`
Exemplo: {"TipoInstituicao": 2, "CodInst": "00068987", "AnoMes": "202506", "NomeRelatorio": "Demonstração de Resultado", "NumeroRelatorio": "4", "Grupo": null, "Conta": "140220", "NomeColuna": "Ativo Total", "DescricaoColuna": "[1000000009] + [2000000008]", "Saldo": 665476916.87}

Colunas (nome | grupo | conta | linhas):
- Ativo Total | None | 140220 | 1426
- Juros Sobre Capital Próprio de Cooperativas 
(aa) | None | 141861 | 1426
- Resultado antes da Tributação e Participações 
(w) = (k) + (l) + (v) | None | 141867 | 1426
- Imposto de Renda e Contribuição Social 
(x) | None | 141868 | 1426
- Participações no Lucro 
(y) | None | 141869 | 1426
- Lucro Líquido 
(z) = (w) + (x) + (y) | None | 141870 | 1426
- Rendas de Tarifas Bancárias 
(m) | Outras Receitas / Despesas | 141856 | 1426
- Outras Rendas de Prestação de Serviços 
(n) | Outras Receitas / Despesas | 141857 | 1426
- Despesas de Pessoal 
(o) | Outras Receitas / Despesas | 141858 | 1426
- Despesas Administrativas 
(p) | Outras Receitas / Despesas | 141859 | 1426
- Resultado com Perdas Esperadas de Outras Operações 
(q) | Outras Receitas / Despesas | 141860 | 1426
- Despesas Tributárias 
(r) | Outras Receitas / Despesas | 141862 | 1426
- Resultado de Participações 
(s) | Outras Receitas / Despesas | 141863 | 1426
- Outras Receitas 
(t) | Outras Receitas / Despesas | 141864 | 1426
- Outras Despesas 
(u) | Outras Receitas / Despesas | 141865 | 1426
- Outras Receitas / Despesas 
(v)= (m) + (n) + (o) +  (p) + (q) + (r) + (s) + (t) + (u) | Outras Receitas / Despesas | 141866 | 1426
- Resultado com Serviços por Transações de Pagamento 
(l1) | Resultado com Transações de Pagamento | 141852 | 1426
- Resultados de Perda Esperada com Transações de Pagamento 
(l2) | Resultado com Transações de Pagamento | 141853 | 1426
- Outros Resultados com Transações de Pagamento 
(l3) | Resultado com Transações de Pagamento | 141854 | 1426
- Resultado com Transações de Pagamento 
(l) | Resultado com Transações de Pagamento | 141855 | 1426
- Rendas de Arrendamento Financeiro 
(d) | Resultado de Intermediação Financeira | 141836 | 1426
- Rendas de Outras Operações com Características de Concessão de Crédito 
(e) | Resultado de Intermediação Financeira | 141837 | 1426
- Despesas de Instrumentos de Dívida Elegíveis a Capital 
(h) | Resultado de Intermediação Financeira | 141848 | 1426
- Resultado com Derivativos 
(i) | Resultado de Intermediação Financeira | 141849 | 1426
- Outros Resultados de Intermediação Financeira 
(j) | Resultado de Intermediação Financeira | 141850 | 1426
- Resultado de Intermediação Financeira 
(k) = (a) + (b) + (c) + (d) + (e) + (f) + (g) + (h) + (i) + (j) | Resultado de Intermediação Financeira | 141851 | 1426
- Despesa de Juros com Captações 
(g1) | Resultado de Intermediação Financeira - Despesas de Captações | 141843 | 1426
- Ajuste de Variação Cambial de Captações 
(g2) | Resultado de Intermediação Financeira - Despesas de Captações | 141844 | 1426
- Ajuste de Hedge de Valor Justo de Captações 
(g3) | Resultado de Intermediação Financeira - Despesas de Captações | 141845 | 1426
- Outros Resultados de Captações 
(g4) | Resultado de Intermediação Financeira - Despesas de Captações | 141846 | 1426
- Despesas de Captações 
(g) | Resultado de Intermediação Financeira - Despesas de Captações | 141847 | 1426
- Receita de Juros com Aplicações Interfinanceiras de Liquidez 
(a1) | Resultado de Intermediação Financeira - Rendas de Aplicações Interfinanceiras de Liquidez | 141821 | 1426
- Ajuste de Variação Cambial de Aplicações Interfinanceiras de Liquidez 
(a2) | Resultado de Intermediação Financeira - Rendas de Aplicações Interfinanceiras de Liquidez | 141822 | 1426
- Ajuste a Valor Justo e Ajuste de Hedge de Valor Justo de Aplicações Interfinanceiras de Liquidez 
(a3) | Resultado de Intermediação Financeira - Rendas de Aplicações Interfinanceiras de Liquidez | 141823 | 1426
- Rendas de Aplicações Interfinanceiras de Liquidez 
(a) | Resultado de Intermediação Financeira - Rendas de Aplicações Interfinanceiras de Liquidez | 141825 | 1426
- Receita de Juros com Operações de Crédito 
(c1) | Resultado de Intermediação Financeira - Rendas de Operações de Crédito | 141831 | 1426
- Ajuste de Variação Cambial de Operações de Crédito 
(c2) | Resultado de Intermediação Financeira - Rendas de Operações de Crédito | 141832 | 1426
- Ajuste a Valor Justo e Ajuste de Hedge de Valor Justo de Operações de Crédito 
(c3) | Resultado de Intermediação Financeira - Rendas de Operações de Crédito | 141833 | 1426
- Outros Resultados de Operações de Crédito 
(c4) | Resultado de Intermediação Financeira - Rendas de Operações de Crédito | 141834 | 1426
- Rendas de Operações de Crédito 
(c) | Resultado de Intermediação Financeira - Rendas de Operações de Crédito | 141835 | 1426
- Receita de Juros com TVM 
(b1) | Resultado de Intermediação Financeira - Rendas de Títulos e Valores Mobiliários | 141826 | 1426
- Ajuste de Variação Cambial de TVM 
(b2) | Resultado de Intermediação Financeira - Rendas de Títulos e Valores Mobiliários | 141827 | 1426
- Ajuste a Valor Justo e Ajuste de Hedge de Valor Justo de TVM 
(b3) | Resultado de Intermediação Financeira - Rendas de Títulos e Valores Mobiliários | 141828 | 1426
- Outros Resultados de TVM 
(b4) | Resultado de Intermediação Financeira - Rendas de Títulos e Valores Mobiliários | 141829 | 1426
- Rendas de Títulos e Valores Mobiliários 
(b) | Resultado de Intermediação Financeira - Rendas de Títulos e Valores Mobiliários | 141830 | 1426
- Resultado com Perda Esperada de Aplicações Interfinanceiras de Liquidez 
(f1) | Resultado de Intermediação Financeira - Resultado com Perda Esperada | 141838 | 1426
- Resultado com Perda Esperada de TVM 
(f2) | Resultado de Intermediação Financeira - Resultado com Perda Esperada | 141839 | 1426
- Resultado com Perda Esperada de Operações de Crédito 
(f3) | Resultado de Intermediação Financeira - Resultado com Perda Esperada | 141840 | 1426
- Resultado com Perda Esperada de Outros Ativos Geradores de Renda 
(f6) | Resultado de Intermediação Financeira - Resultado com Perda Esperada | 141841 | 1426
- Resultado com Perda Esperada 
(f) | Resultado de Intermediação Financeira - Resultado com Perda Esperada | 141842 | 1426
- Resultado com Perda Esperada de Arrendamento 
(f4) | Resultado de Intermediação Financeira - Resultado com Perda Esperada | 142851 | 1426
- Resultado com Perda Esperada de Outras Operações com Características de Concessão de Crédito
(f5) | Resultado de Intermediação Financeira - Resultado com Perda Esperada | 142852 | 1426

## Tipo 2, relatório 5: sem dados (vazio)

## Tipo 2, relatório 6: sem dados (vazio)

## Tipo 2, relatório 7: sem dados (vazio)

## Tipo 2, relatório 8: sem dados (vazio)

## Tipo 2, relatório 9: sem dados (vazio)

## Tipo 2, relatório 10: sem dados (vazio)

## Tipo 2, relatório 11: sem dados (vazio)

## Tipo 2, relatório 12: sem dados (vazio)

## Tipo 2, relatório 13: sem dados (vazio)

## Tipo 2, relatório 14: sem dados (vazio)

## Tipo 2, relatório 15: sem dados (vazio)

## Tipo 2, relatório 16: sem dados (vazio)

## Tipo de instituição 3, relatório 1

11165 valores, 1595 instituições, 7 colunas.
Campos: `TipoInstituicao`, `CodInst`, `AnoMes`, `NomeRelatorio`, `NumeroRelatorio`, `Grupo`, `Conta`, `NomeColuna`, `DescricaoColuna`, `Saldo`
Exemplo: {"TipoInstituicao": 3, "CodInst": "00000000", "AnoMes": "202506", "NomeRelatorio": "Resumo", "NumeroRelatorio": "1", "Grupo": null, "Conta": "140200", "NomeColuna": "Títulos e Valores Mobiliários", "DescricaoColuna": "[1300000008]-[1330000009]", "Saldo": 557184810452.83}

Colunas (nome | grupo | conta | linhas):
- Títulos e Valores Mobiliários | None | 140200 | 1595
- Ativo Total | None | 140220 | 1595
- Captações | None | 140239 | 1595
- Passivo Exigível | None | 140244 | 1595
- Patrimônio Líquido | None | 140246 | 1595
- Lucro Líquido | None | 141870 | 1595
- Carteira de Crédito | None | 141873 | 1595

## Tipo de instituição 3, relatório 2

38280 valores, 1595 instituições, 24 colunas.
Campos: `TipoInstituicao`, `CodInst`, `AnoMes`, `NomeRelatorio`, `NumeroRelatorio`, `Grupo`, `Conta`, `NomeColuna`, `DescricaoColuna`, `Saldo`
Exemplo: {"TipoInstituicao": 3, "CodInst": "00000000", "AnoMes": "202506", "NomeRelatorio": "Ativo", "NumeroRelatorio": "2", "Grupo": null, "Conta": "140198", "NomeColuna": "Disponibilidades \n(a)", "DescricaoColuna": "[1100000002]", "Saldo": 21444840645.46}

Colunas (nome | grupo | conta | linhas):
- Disponibilidades 
(a) | None | 140198 | 1595
- Aplicações Interfinanceiras de Liquidez 
(b) | None | 140199 | 1595
- Títulos e Valores Mobiliários 
(c) | None | 140200 | 1595
- Outros Ativos Realizáveis 
(i) | None | 140218 | 1595
- Ativo Permanente 
(j) | None | 140219 | 1595
- Ativo Total 
(k) = (a) + (b) + (c) + (d) + (e) + (f) + (g) + (h) + (i) + (j) | None | 140220 | 1595
- Instrumentos Derivativos (d) | None | 141612 | 1595
- Valor Contábil Bruto 
(f1) | Operações de Arrendamento Financeiro | 140207 | 1595
- Perda Esperada 
(f2) | Operações de Arrendamento Financeiro | 140208 | 1595
- Hedge de Valor Justo 
(f3) | Operações de Arrendamento Financeiro | 140209 | 1595
- Operações de Arrendamento Financeiro 
(f) | Operações de Arrendamento Financeiro | 140210 | 1595
- Valor Contábil Bruto 
(e1) | Operações de Crédito | 140201 | 1595
- Perda Esperada 
(e2) | Operações de Crédito | 140202 | 1595
- Hedge de Valor Justo 
(e3) | Operações de Crédito | 140203 | 1595
- Ajuste a Valor Justo 
(e4) | Operações de Crédito | 140204 | 1595
- Operações de Crédito 
(e) | Operações de Crédito | 140205 | 1595
- Valor Contábil Bruto 
(g1) | Outras Operações com Características de Concessão de Crédito | 140212 | 1595
- Perda Esperada 
(g2) | Outras Operações com Características de Concessão de Crédito | 140213 | 1595
- Hedge de Valor Justo 
(g3) | Outras Operações com Características de Concessão de Crédito | 140214 | 1595
- Ajuste a Valor Justo 
(g4) | Outras Operações com Características de Concessão de Crédito | 140215 | 1595
- Outras Operações com Características de Concessão de Crédito 
(g) | Outras Operações com Características de Concessão de Crédito | 140216 | 1595
- Valor Contábil Bruto 
(h1) | Valores a Receber de Transações de Pagamentos - Usuários Finais (Pós-pago) | 145831 | 1595
- Perda Esperada 
(h2) | Valores a Receber de Transações de Pagamentos - Usuários Finais (Pós-pago) | 145832 | 1595
- Valores a Receber de Transações de Pagamentos - Usuários Finais (Pós-pago) 
(h) | Valores a Receber de Transações de Pagamentos - Usuários Finais (Pós-pago) | 145833 | 1595

## Tipo de instituição 3, relatório 3

35090 valores, 1595 instituições, 22 colunas.
Campos: `TipoInstituicao`, `CodInst`, `AnoMes`, `NomeRelatorio`, `NumeroRelatorio`, `Grupo`, `Conta`, `NomeColuna`, `DescricaoColuna`, `Saldo`
Exemplo: {"TipoInstituicao": 3, "CodInst": "00000000", "AnoMes": "202506", "NomeRelatorio": "Passivo", "NumeroRelatorio": "3", "Grupo": null, "Conta": "140241", "NomeColuna": "Instrumentos Derivativos \n(f)", "DescricaoColuna": "[4700000007]", "Saldo": 4244818155.13}

Colunas (nome | grupo | conta | linhas):
- Instrumentos Derivativos 
(f) | None | 140241 | 1595
- Outras Obrigações 
(g) | None | 140242 | 1595
- Instrumentos de Dívida Elegíveis a Capital 
(h) | None | 140243 | 1595
- Passivo Exigível 
(i) = (e) + (f) + (g) + (h) | None | 140244 | 1595
- Patrimônio Líquido 
(j) | None | 140246 | 1595
- Passivo Total 
(k) = (i) + (j) | None | 140247 | 1595
- Obrigações por Operações Compromissadas 
(b) | Captações | 140230 | 1595
- Obrigações por Empréstimos e Repasses 
(d) | Captações | 140238 | 1595
- Captações 
(e) = (a) + (b) + (c) + (d) | Captações | 140239 | 1595
- Depósitos à Vista 
(a1) | Captações - Depósitos | 140222 | 1595
- Depósitos de Poupança 
(a2) | Captações - Depósitos | 140223 | 1595
- Depósitos Interfinanceiros 
(a3) | Captações - Depósitos | 140224 | 1595
- Depósitos a Prazo 
(a4) | Captações - Depósitos | 140225 | 1595
- Conta de Pagamento Pré-Paga 
(a5) | Captações - Depósitos | 140226 | 1595
- Depósitos Outros 
(a6) | Captações - Depósitos | 140227 | 1595
- Depósitos 
(a) | Captações - Depósitos | 140228 | 1595
- Letras de Crédito Imobiliário 
(c1) | Captações - Outros Instrumentos de Dívida | 140231 | 1595
- Letras de Crédito do Agronegócio 
(c2) | Captações - Outros Instrumentos de Dívida | 140232 | 1595
- Letras Financeiras 
(c3) | Captações - Outros Instrumentos de Dívida | 140233 | 1595
- Obrigações por Títulos e Valores Mobiliários no Exterior 
(c4) | Captações - Outros Instrumentos de Dívida | 140234 | 1595
- Demais instrumentos de dívida 
(c5) | Captações - Outros Instrumentos de Dívida | 140235 | 1595
- Outros Instrumentos de Dívida 
(c) | Captações - Outros Instrumentos de Dívida | 140236 | 1595

## Tipo de instituição 3, relatório 4

82940 valores, 1595 instituições, 52 colunas.
Campos: `TipoInstituicao`, `CodInst`, `AnoMes`, `NomeRelatorio`, `NumeroRelatorio`, `Grupo`, `Conta`, `NomeColuna`, `DescricaoColuna`, `Saldo`
Exemplo: {"TipoInstituicao": 3, "CodInst": "00000000", "AnoMes": "202506", "NomeRelatorio": "Demonstração de Resultado", "NumeroRelatorio": "4", "Grupo": null, "Conta": "140220", "NomeColuna": "Ativo Total", "DescricaoColuna": "[1000000009] + [2000000008]", "Saldo": 2340882371329.85}

Colunas (nome | grupo | conta | linhas):
- Ativo Total | None | 140220 | 1595
- Juros Sobre Capital Próprio de Cooperativas 
(aa) | None | 141861 | 1595
- Resultado antes da Tributação e Participações 
(w) = (k) + (l) + (v) | None | 141867 | 1595
- Imposto de Renda e Contribuição Social 
(x) | None | 141868 | 1595
- Participações no Lucro 
(y) | None | 141869 | 1595
- Lucro Líquido 
(z) = (w) + (x) + (y) | None | 141870 | 1595
- Rendas de Tarifas Bancárias 
(m) | Outras Receitas / Despesas | 141856 | 1595
- Outras Rendas de Prestação de Serviços 
(n) | Outras Receitas / Despesas | 141857 | 1595
- Despesas de Pessoal 
(o) | Outras Receitas / Despesas | 141858 | 1595
- Despesas Administrativas 
(p) | Outras Receitas / Despesas | 141859 | 1595
- Resultado com Perdas Esperadas de Outras Operações 
(q) | Outras Receitas / Despesas | 141860 | 1595
- Despesas Tributárias 
(r) | Outras Receitas / Despesas | 141862 | 1595
- Resultado de Participações 
(s) | Outras Receitas / Despesas | 141863 | 1595
- Outras Receitas 
(t) | Outras Receitas / Despesas | 141864 | 1595
- Outras Despesas 
(u) | Outras Receitas / Despesas | 141865 | 1595
- Outras Receitas / Despesas 
(v)= (m) + (n) + (o) +  (p) + (q) + (r) + (s) + (t) + (u) | Outras Receitas / Despesas | 141866 | 1595
- Resultado com Serviços por Transações de Pagamento 
(l1) | Resultado com Transações de Pagamento | 141852 | 1595
- Resultados de Perda Esperada com Transações de Pagamento 
(l2) | Resultado com Transações de Pagamento | 141853 | 1595
- Outros Resultados com Transações de Pagamento 
(l3) | Resultado com Transações de Pagamento | 141854 | 1595
- Resultado com Transações de Pagamento 
(l) | Resultado com Transações de Pagamento | 141855 | 1595
- Rendas de Arrendamento Financeiro 
(d) | Resultado de Intermediação Financeira | 141836 | 1595
- Rendas de Outras Operações com Características de Concessão de Crédito 
(e) | Resultado de Intermediação Financeira | 141837 | 1595
- Despesas de Instrumentos de Dívida Elegíveis a Capital 
(h) | Resultado de Intermediação Financeira | 141848 | 1595
- Resultado com Derivativos 
(i) | Resultado de Intermediação Financeira | 141849 | 1595
- Outros Resultados de Intermediação Financeira 
(j) | Resultado de Intermediação Financeira | 141850 | 1595
- Resultado de Intermediação Financeira 
(k) = (a) + (b) + (c) + (d) + (e) + (f) + (g) + (h) + (i) + (j) | Resultado de Intermediação Financeira | 141851 | 1595
- Despesa de Juros com Captações 
(g1) | Resultado de Intermediação Financeira - Despesas de Captações | 141843 | 1595
- Ajuste de Variação Cambial de Captações 
(g2) | Resultado de Intermediação Financeira - Despesas de Captações | 141844 | 1595
- Ajuste de Hedge de Valor Justo de Captações 
(g3) | Resultado de Intermediação Financeira - Despesas de Captações | 141845 | 1595
- Outros Resultados de Captações 
(g4) | Resultado de Intermediação Financeira - Despesas de Captações | 141846 | 1595
- Despesas de Captações 
(g) | Resultado de Intermediação Financeira - Despesas de Captações | 141847 | 1595
- Receita de Juros com Aplicações Interfinanceiras de Liquidez 
(a1) | Resultado de Intermediação Financeira - Rendas de Aplicações Interfinanceiras de Liquidez | 141821 | 1595
- Ajuste de Variação Cambial de Aplicações Interfinanceiras de Liquidez 
(a2) | Resultado de Intermediação Financeira - Rendas de Aplicações Interfinanceiras de Liquidez | 141822 | 1595
- Ajuste a Valor Justo e Ajuste de Hedge de Valor Justo de Aplicações Interfinanceiras de Liquidez 
(a3) | Resultado de Intermediação Financeira - Rendas de Aplicações Interfinanceiras de Liquidez | 141823 | 1595
- Rendas de Aplicações Interfinanceiras de Liquidez 
(a) | Resultado de Intermediação Financeira - Rendas de Aplicações Interfinanceiras de Liquidez | 141825 | 1595
- Receita de Juros com Operações de Crédito 
(c1) | Resultado de Intermediação Financeira - Rendas de Operações de Crédito | 141831 | 1595
- Ajuste de Variação Cambial de Operações de Crédito 
(c2) | Resultado de Intermediação Financeira - Rendas de Operações de Crédito | 141832 | 1595
- Ajuste a Valor Justo e Ajuste de Hedge de Valor Justo de Operações de Crédito 
(c3) | Resultado de Intermediação Financeira - Rendas de Operações de Crédito | 141833 | 1595
- Outros Resultados de Operações de Crédito 
(c4) | Resultado de Intermediação Financeira - Rendas de Operações de Crédito | 141834 | 1595
- Rendas de Operações de Crédito 
(c) | Resultado de Intermediação Financeira - Rendas de Operações de Crédito | 141835 | 1595
- Receita de Juros com TVM 
(b1) | Resultado de Intermediação Financeira - Rendas de Títulos e Valores Mobiliários | 141826 | 1595
- Ajuste de Variação Cambial de TVM 
(b2) | Resultado de Intermediação Financeira - Rendas de Títulos e Valores Mobiliários | 141827 | 1595
- Ajuste a Valor Justo e Ajuste de Hedge de Valor Justo de TVM 
(b3) | Resultado de Intermediação Financeira - Rendas de Títulos e Valores Mobiliários | 141828 | 1595
- Outros Resultados de TVM 
(b4) | Resultado de Intermediação Financeira - Rendas de Títulos e Valores Mobiliários | 141829 | 1595
- Rendas de Títulos e Valores Mobiliários 
(b) | Resultado de Intermediação Financeira - Rendas de Títulos e Valores Mobiliários | 141830 | 1595
- Resultado com Perda Esperada de Aplicações Interfinanceiras de Liquidez 
(f1) | Resultado de Intermediação Financeira - Resultado com Perda Esperada | 141838 | 1595
- Resultado com Perda Esperada de TVM 
(f2) | Resultado de Intermediação Financeira - Resultado com Perda Esperada | 141839 | 1595
- Resultado com Perda Esperada de Operações de Crédito 
(f3) | Resultado de Intermediação Financeira - Resultado com Perda Esperada | 141840 | 1595
- Resultado com Perda Esperada de Outros Ativos Geradores de Renda 
(f6) | Resultado de Intermediação Financeira - Resultado com Perda Esperada | 141841 | 1595
- Resultado com Perda Esperada 
(f) | Resultado de Intermediação Financeira - Resultado com Perda Esperada | 141842 | 1595
- Resultado com Perda Esperada de Arrendamento 
(f4) | Resultado de Intermediação Financeira - Resultado com Perda Esperada | 142851 | 1595
- Resultado com Perda Esperada de Outras Operações com Características de Concessão de Crédito
(f5) | Resultado de Intermediação Financeira - Resultado com Perda Esperada | 142852 | 1595

## Tipo 3, relatório 5: sem dados (vazio)

## Tipo 3, relatório 6: sem dados (vazio)

## Tipo 3, relatório 7: sem dados (vazio)

## Tipo 3, relatório 8: sem dados (vazio)

## Tipo 3, relatório 9: sem dados (vazio)

## Tipo 3, relatório 10: sem dados (vazio)

## Tipo 3, relatório 11: sem dados (vazio)

## Tipo 3, relatório 12: sem dados (vazio)

## Tipo 3, relatório 13: sem dados (vazio)

## Tipo 3, relatório 14: sem dados (vazio)

## Tipo 3, relatório 15: sem dados (vazio)

## Tipo 3, relatório 16: sem dados (vazio)