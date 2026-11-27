"""vetores dos trechos

Revisão: 0005
Anterior: 0004
"""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


revision = '0005'
down_revision = '0004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'trecho_embedding',
        sa.Column('trecho_id', sa.BigInteger(), nullable=False),
        sa.Column('modelo', sa.String(length=60), nullable=False),
        sa.Column('embedding', Vector(1024), nullable=False),
        sa.ForeignKeyConstraint(['trecho_id'], ['trecho.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('trecho_id'),
    )
    # O índice de vizinhança (HNSW) é criado depois da carga dos vetores,
    # pelo comando de importação, porque fica mais rápido e de melhor qualidade.


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_trecho_embedding_hnsw")
    op.drop_table('trecho_embedding')
