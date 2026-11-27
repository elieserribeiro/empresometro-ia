# Empresômetro IA

> **Mais de 600 empresas. Cinco anos de informações. Uma única pergunta. Muitas respostas.**

Plataforma de inteligência empresarial com IA generativa, agentes e RAG sobre dados públicos da CVM, do Banco Central e do IBGE.

## Situação do projeto

Em construção. Etapa atual: **Fase 3 — Indicadores**.

| Fase | Entrega | Situação |
|---|---|---|
| 1 | Data Discovery: inventário de fontes, cobertura e chaves de integração | Concluída |
| 2 | Fundação de dados: cadastro, ETL e PostgreSQL | Concluída |
| 3 | Indicadores financeiros | Em andamento |
| 4 | RAG piloto | A fazer |
| 5 | Agentes e API | A fazer |
| 6 | Generative BI | A fazer |
| 7 | Governança e testes | A fazer |
| 8 | Expansão documental | A fazer |
| 9 | Publicação | A fazer |

## Data Discovery

O script `scripts/discovery/data_discovery.py` baixa o cadastro de companhias abertas, as DFP e os ITR da CVM (de 2021 até o último trimestre fechado), verifica a disponibilidade de FRE, IPE, Banco Central (SGS) e IBGE (SIDRA) e mede a cobertura real das companhias ativas.

Ele é executado pelo GitHub Actions (aba **Actions > Data Discovery > Run workflow**) e grava o resultado em `docs/discovery/`:

- `relatorio_cobertura.md`: relatório de cobertura;
- `cobertura.json`: os mesmos números em formato estruturado;
- `companhias_ativas.csv`: uma linha por companhia ativa.

## Banco de dados

PostgreSQL 16 com a extensão pgvector, em Docker Compose. O esquema é versionado com Alembic e descrito em `src/empresometro/db/models.py`.

| Tabela | Conteúdo |
|---|---|
| `companhia` | Uma linha por CNPJ, com situação do registro e do emissor |
| `companhia_mercado` | Mercados em que a companhia negocia (pode haver mais de um) |
| `setor` | Setor informado pela CVM e setor-base para agrupamento |
| `documento` | Cada DFP ou ITR entregue, em todas as versões, com marca da vigente |
| `demonstracao_linha` | Todas as contas das demonstrações, particionada por ano, com valor original e em reais |
| `composicao_capital` | Quantidade de ações por documento |
| `parecer` | Pareceres e declarações |
| `carga_arquivo` | Linhagem dos arquivos baixados |
| `serie_macro`, `serie_macro_valor` | Séries do Banco Central e do IBGE |
| `alerta_qualidade` | Sinalizações das validações de qualidade |

### Rodar tudo pelo Docker

Com o Docker Desktop instalado, na pasta do projeto:

```bash
copy .env.example .env        # no Windows; depois troque a senha no arquivo .env
docker compose run --rm etl
```

O comando sobe o banco, cria as tabelas e carrega o cadastro, as DFP e os ITR de 2021 até o ano corrente. Os arquivos baixados ficam em `data/` e o relatório em `docs/etl/relatorio_carga.md`. Para carregar só uma parte:

```bash
docker compose run --rm etl carregar --tipos dfp --anos 2025
```

## Carga dos dados

O ETL em `src/empresometro/etl/` baixa os arquivos da CVM e carrega o banco: cadastro (companhias ativas e inativas com documentos na janela), DFP e ITR com todas as contas, o registro de todas as versões, composição do capital e pareceres.

Fora do Docker, com Python 3.12:

```bash
pip install -e ".[dev]"
alembic upgrade head
python -m empresometro.etl carregar
python -m empresometro.etl relatorio --saida docs/etl/relatorio_carga.md
```

Ao final, o comando `carregar` também traz cerca de 20 séries macroeconômicas do Banco Central e do IBGE (desde 2016) e roda as validações de qualidade, que gravam alertas na tabela `alerta_qualidade`. Os cálculos devem usar a visão `demonstracao_linha_unica`, que mostra cada conta uma única vez; a tabela `demonstracao_linha` preserva os arquivos como a CVM publicou. Relatórios gerados em `docs/etl/`: `relatorio_carga.md`, `relatorio_macro.md` e `relatorio_qualidade.md`.

A carga é incremental: um arquivo que não mudou desde a última execução (mesmo hash) é pulado. Use `--forcar` para recarregar. O workflow **Carga de teste** valida o ETL com dados reais em um banco temporário e grava o resultado em `docs/etl/relatorio_carga_teste.md`.

## Indicadores

O módulo `src/empresometro/indicadores/` calcula 36 indicadores financeiros de forma determinística, em Python e SQL, sem uso de modelo de linguagem: valores de base, rentabilidade, crescimento, endividamento, liquidez e caixa, além de indicadores próprios de bancos. As fórmulas estão em `docs/indicadores/catalogo.md`.

- **Períodos:** exercício anual e últimos 12 meses a cada trimestre.
- **Base:** balanço consolidado quando existe; individual nos demais casos.
- **Planos de contas:** o tipo de companhia (comum, banco ou seguradora) é identificado pelas contas de cada documento.
- **Sem valor inventado:** quando o indicador não pode ser calculado, a tabela `indicador_valor` registra o motivo.

```bash
docker compose run --rm etl indicadores
```

## Documentos

O módulo `src/empresometro/documentos/` monta a base de textos para a busca (RAG), no piloto com 20 companhias listadas em `docs/documentos/piloto.md`:

- **Fatos relevantes e comunicados ao mercado:** um PDF por documento, baixado do site da CVM.
- **Formulário de Referência:** as seções narrativas (fatores de risco, atividades, comentários dos diretores), que vêm como PDFs embutidos no arquivo do formulário.
- **Pareceres de auditoria:** textos já carregados pelo ETL.

Cada documento é dividido em trechos com a página de origem, guardados na tabela `trecho` com busca textual em português. A coleta faz uma pausa entre as requisições e pode ser interrompida e retomada.

```bash
docker compose run --rm --build documentos
docker compose run --rm documentos coletar --fontes ipe --anos 2025
```

## Direitos

© 2026 Eliéser Ribeiro. Todos os direitos reservados.

Este repositório é público apenas para consulta. Não é concedida licença para usar, copiar, modificar, executar ou distribuir o código, no todo ou em parte, sem autorização prévia e por escrito do autor.
