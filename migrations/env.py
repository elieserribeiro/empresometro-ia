"""Ambiente do Alembic: usa DATABASE_URL e os modelos do projeto."""

from logging.config import fileConfig

from alembic import context

from empresometro.db.config import criar_engine, url_do_banco
from empresometro.db.models import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(url=url_do_banco(), target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = criar_engine()
    with engine.connect() as conexao:
        context.configure(connection=conexao, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
