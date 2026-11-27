"""documentos e trechos

Revisão: 0004
Anterior: 0003
Criada em: 2026-11-27 14:54:23.596464
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('documento_texto',
    sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('companhia_id', sa.Integer(), nullable=False),
    sa.Column('fonte', sa.String(length=10), nullable=False),
    sa.Column('chave_origem', sa.String(length=200), nullable=False),
    sa.Column('categoria', sa.String(length=120), nullable=True),
    sa.Column('tipo', sa.String(length=200), nullable=True),
    sa.Column('secao', sa.String(length=200), nullable=True),
    sa.Column('titulo', sa.Text(), nullable=False),
    sa.Column('dt_referencia', sa.Date(), nullable=True),
    sa.Column('dt_entrega', sa.Date(), nullable=True),
    sa.Column('versao', sa.SmallInteger(), nullable=True),
    sa.Column('link', sa.Text(), nullable=True),
    sa.Column('arquivo_sha256', sa.String(length=64), nullable=True),
    sa.Column('paginas', sa.Integer(), nullable=True),
    sa.Column('caracteres', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('situacao', sa.String(length=12), nullable=False),
    sa.Column('erro', sa.Text(), nullable=True),
    sa.Column('coletado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("fonte IN ('IPE', 'FRE', 'PARECER')", name='ck_documento_texto_fonte'),
    sa.CheckConstraint("situacao IN ('OK', 'SEM_TEXTO', 'ERRO')", name='ck_documento_texto_situacao'),
    sa.ForeignKeyConstraint(['companhia_id'], ['companhia.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('fonte', 'chave_origem', name='uq_documento_texto_origem')
    )
    op.create_index(op.f('ix_documento_texto_companhia_id'), 'documento_texto', ['companhia_id'], unique=False)
    op.create_index('ix_documento_texto_fonte_data', 'documento_texto', ['fonte', 'dt_referencia'], unique=False)
    op.create_table('trecho',
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
    sa.Column('documento_texto_id', sa.Integer(), nullable=False),
    sa.Column('ordem', sa.Integer(), nullable=False),
    sa.Column('pagina_inicial', sa.Integer(), nullable=True),
    sa.Column('pagina_final', sa.Integer(), nullable=True),
    sa.Column('texto', sa.Text(), nullable=False),
    sa.Column('caracteres', sa.Integer(), nullable=False),
    sa.Column('busca', postgresql.TSVECTOR(), sa.Computed("to_tsvector('portuguese', texto)", persisted=True), nullable=False),
    sa.ForeignKeyConstraint(['documento_texto_id'], ['documento_texto.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('documento_texto_id', 'ordem', name='uq_trecho_ordem')
    )
    op.create_index('ix_trecho_busca', 'trecho', ['busca'], unique=False, postgresql_using='gin')
    op.create_index(op.f('ix_trecho_documento_texto_id'), 'trecho', ['documento_texto_id'], unique=False)


def downgrade() -> None:
    op.drop_table('trecho')
    op.drop_table('documento_texto')
