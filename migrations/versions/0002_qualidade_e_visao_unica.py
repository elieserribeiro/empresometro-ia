"""alertas de qualidade e visão sem linhas repetidas

Revisão: 0002
Anterior: 0001
"""
from alembic import op
import sqlalchemy as sa


revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None

# Colunas que identificam uma conta dentro de um documento.
CHAVE = (
    "ano_referencia, documento_id, demonstracao, escopo, ordem_exercicio, "
    "dt_inicio, dt_fim, coluna_df, cd_conta"
)


def upgrade() -> None:
    op.create_table(
        'alerta_qualidade',
        sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column('tipo', sa.String(length=50), nullable=False),
        sa.Column('companhia_id', sa.Integer(), nullable=True),
        sa.Column('documento_id', sa.Integer(), nullable=True),
        sa.Column('detalhe', sa.Text(), nullable=False),
        sa.Column('valor', sa.Numeric(precision=30, scale=2), nullable=True),
        sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['companhia_id'], ['companhia.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['documento_id'], ['documento.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_alerta_qualidade_tipo'), 'alerta_qualidade', ['tipo'], unique=False)
    op.create_index(op.f('ix_alerta_qualidade_companhia_id'), 'alerta_qualidade', ['companhia_id'], unique=False)
    op.create_index(op.f('ix_alerta_qualidade_documento_id'), 'alerta_qualidade', ['documento_id'], unique=False)

    # Os dados brutos ficam como a CVM publicou; os cálculos usam esta visão,
    # que mostra cada conta uma única vez (a primeira ocorrência no arquivo).
    op.execute(
        f"""
        CREATE VIEW demonstracao_linha_unica AS
        SELECT DISTINCT ON ({CHAVE}) *
        FROM demonstracao_linha
        ORDER BY {CHAVE}, sequencia
        """
    )


def downgrade() -> None:
    op.execute("DROP VIEW IF EXISTS demonstracao_linha_unica")
    op.drop_index(op.f('ix_alerta_qualidade_documento_id'), table_name='alerta_qualidade')
    op.drop_index(op.f('ix_alerta_qualidade_companhia_id'), table_name='alerta_qualidade')
    op.drop_index(op.f('ix_alerta_qualidade_tipo'), table_name='alerta_qualidade')
    op.drop_table('alerta_qualidade')
