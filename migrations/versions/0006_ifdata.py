"""IF.data do Banco Central: correspondência de bancos e valores

Revisão: 0006
Anterior: 0005
"""
from alembic import op
import sqlalchemy as sa


revision = '0006'
down_revision = '0005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'companhia_ifdata',
        sa.Column('companhia_id', sa.Integer(), nullable=False),
        sa.Column('cod_inst', sa.String(length=20), nullable=False),
        sa.Column('nome_ifdata', sa.String(length=200), nullable=True),
        sa.Column('criterio', sa.String(length=40), nullable=False),
        sa.ForeignKeyConstraint(['companhia_id'], ['companhia.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('companhia_id'),
    )
    op.create_index(op.f('ix_companhia_ifdata_cod_inst'), 'companhia_ifdata', ['cod_inst'], unique=False)
    op.create_table(
        'ifdata_valor',
        sa.Column('cod_inst', sa.String(length=20), nullable=False),
        sa.Column('data_base', sa.Date(), nullable=False),
        sa.Column('conta', sa.String(length=12), nullable=False),
        sa.Column('relatorio', sa.String(length=4), nullable=False),
        sa.Column('nome_coluna', sa.String(length=200), nullable=True),
        sa.Column('saldo', sa.Numeric(precision=30, scale=10), nullable=True),
        sa.PrimaryKeyConstraint('cod_inst', 'data_base', 'conta'),
    )


def downgrade() -> None:
    op.drop_table('ifdata_valor')
    op.drop_index(op.f('ix_companhia_ifdata_cod_inst'), table_name='companhia_ifdata')
    op.drop_table('companhia_ifdata')
