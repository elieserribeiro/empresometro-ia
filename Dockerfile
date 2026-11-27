# Imagem do ETL do Empresômetro IA.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

COPY pyproject.toml alembic.ini ./
COPY src ./src
COPY migrations ./migrations
RUN pip install .

# Aplica as migrações pendentes e depois executa o comando do ETL.
ENTRYPOINT ["sh", "-c", "alembic upgrade head && exec python -m empresometro.etl \"$@\"", "--"]
CMD ["carregar", "--saida", "docs/etl/relatorio_carga.md"]
