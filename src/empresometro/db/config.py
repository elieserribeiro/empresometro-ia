"""Configuração de acesso ao banco."""

from __future__ import annotations

import os

from sqlalchemy import Engine, create_engine

URL_PADRAO = "postgresql+psycopg://empresometro:empresometro@localhost:5432/empresometro"


def url_do_banco() -> str:
    """Lê a URL do banco da variável de ambiente DATABASE_URL."""
    return os.environ.get("DATABASE_URL", URL_PADRAO)


def criar_engine(url: str | None = None) -> Engine:
    return create_engine(url or url_do_banco(), pool_pre_ping=True)
