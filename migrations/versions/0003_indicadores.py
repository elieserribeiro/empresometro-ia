"""indicadores

Revisão: 0003
Anterior: 0002
Criada em: 2026-11-27 13:27:21.989081
"""
from alembic import op
import sqlalchemy as sa


revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('indicador',
    sa.Column('codigo', sa.String(length=40), nullable=False),
    sa.Column('nome', sa.String(length=120), nullable=False),
    sa.Column('grupo', sa.String(length=40), nullable=False),
    sa.Column('unidade', sa.String(length=10), nullable=False),
    sa.Column('formula', sa.Text(), nullable=False),
    sa.Column('aplica_a', sa.String(length=60), nullable=False),
    sa.Column('observacao', sa.Text(), nullable=True),
    sa.Column('ordem', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('codigo')
    )
    op.create_table('base_fluxo',
    sa.Column('documento_id', sa.Integer(), nullable=False),
    sa.Column('escopo', sa.String(length=3), nullable=False),
    sa.Column('ordem_exercicio', sa.String(length=10), nullable=False),
    sa.Column('dt_inicio', sa.Date(), nullable=False),
    sa.Column('dt_fim', sa.Date(), nullable=False),
    sa.Column('plano', sa.String(length=12), nullable=True),
    sa.Column('receita', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.Column('resultado_bruto', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.Column('ebit', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.Column('despesas_financeiras', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.Column('lucro_liquido', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.Column('depreciacao', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.Column('fco', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.Column('fci', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.Column('banco_pessoal', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.Column('banco_administrativas', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.Column('banco_servicos', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['documento_id'], ['documento.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('documento_id', 'escopo', 'ordem_exercicio', 'dt_inicio', 'dt_fim')
    )
    op.create_table('base_saldo',
    sa.Column('documento_id', sa.Integer(), nullable=False),
    sa.Column('escopo', sa.String(length=3), nullable=False),
    sa.Column('ordem_exercicio', sa.String(length=10), nullable=False),
    sa.Column('dt_fim', sa.Date(), nullable=False),
    sa.Column('ativo_total', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.Column('ativo_circulante', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.Column('caixa', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.Column('aplicacoes', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.Column('estoques', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.Column('passivo_total', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.Column('passivo_circulante', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.Column('passivo_nao_circulante', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.Column('emprestimos_cp', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.Column('emprestimos_lp', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.Column('patrimonio_liquido', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['documento_id'], ['documento.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('documento_id', 'escopo', 'ordem_exercicio', 'dt_fim')
    )
    op.create_table('indicador_valor',
    sa.Column('companhia_id', sa.Integer(), nullable=False),
    sa.Column('codigo', sa.String(length=40), nullable=False),
    sa.Column('periodo', sa.String(length=5), nullable=False),
    sa.Column('dt_referencia', sa.Date(), nullable=False),
    sa.Column('valor', sa.Numeric(precision=30, scale=6), nullable=True),
    sa.Column('motivo', sa.String(length=24), nullable=True),
    sa.Column('escopo', sa.String(length=3), nullable=False),
    sa.Column('plano', sa.String(length=12), nullable=False),
    sa.Column('documento_id', sa.Integer(), nullable=True),
    sa.CheckConstraint("periodo IN ('ANUAL', '12M')", name='ck_indicador_valor_periodo'),
    sa.CheckConstraint('(valor IS NULL) <> (motivo IS NULL)', name='ck_indicador_valor_ou_motivo'),
    sa.ForeignKeyConstraint(['codigo'], ['indicador.codigo'], ),
    sa.ForeignKeyConstraint(['companhia_id'], ['companhia.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['documento_id'], ['documento.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('companhia_id', 'codigo', 'periodo', 'dt_referencia')
    )
    op.create_index('ix_indicador_valor_codigo_data', 'indicador_valor', ['codigo', 'periodo', 'dt_referencia'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_indicador_valor_codigo_data', table_name='indicador_valor')
    op.drop_table('indicador_valor')
    op.drop_table('indicador')
    op.drop_table('base_fluxo')
    op.drop_table('base_saldo')
