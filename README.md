# Empresômetro IA

> **Mais de 600 empresas. Cinco anos de informações. Uma única pergunta. Muitas respostas.**

Plataforma de inteligência empresarial com IA generativa, agentes e RAG sobre dados públicos da CVM, do Banco Central e do IBGE.

## Situação do projeto

Em construção. Etapa atual: **Fase 1 — Data Discovery**.

| Fase | Entrega | Situação |
|---|---|---|
| 1 | Data Discovery: inventário de fontes, cobertura e chaves de integração | Em andamento |
| 2 | Fundação de dados: cadastro, ETL e PostgreSQL | A fazer |
| 3 | Indicadores financeiros | A fazer |
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

## Direitos

© 2026 Eliéser Ribeiro. Todos os direitos reservados.

Este repositório é público apenas para consulta. Não é concedida licença para usar, copiar, modificar, executar ou distribuir o código, no todo ou em parte, sem autorização prévia e por escrito do autor.
