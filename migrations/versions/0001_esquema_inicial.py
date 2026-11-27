"""esquema inicial

Revisão: 0001
Anterior: 
Criada em: 2026-11-27 01:19:35.652502
"""
from alembic import op
import sqlalchemy as sa


revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

ANO_PARTICAO_INICIAL = 2020
ANO_PARTICAO_FINAL = 2028


def upgrade() -> None:
    # pgvector fica habilitado desde já para a camada documental (Fase 4).
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table('carga_arquivo',
    sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('fonte', sa.String(length=40), nullable=False),
    sa.Column('url', sa.String(length=500), nullable=False),
    sa.Column('nome_arquivo', sa.String(length=200), nullable=False),
    sa.Column('sha256', sa.String(length=64), nullable=False),
    sa.Column('bytes', sa.BigInteger(), nullable=True),
    sa.Column('modificado_na_fonte', sa.DateTime(timezone=True), nullable=True),
    sa.Column('baixado_em', sa.DateTime(timezone=True), nullable=False),
    sa.Column('linhas', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url', 'sha256', name='uq_carga_arquivo_url_sha256')
    )
    op.create_table('serie_macro',
    sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('fonte', sa.String(length=20), nullable=False),
    sa.Column('codigo', sa.String(length=60), nullable=False),
    sa.Column('nome', sa.String(length=200), nullable=False),
    sa.Column('unidade', sa.String(length=60), nullable=True),
    sa.Column('periodicidade', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('fonte', 'codigo', name='uq_serie_macro_fonte_codigo')
    )
    op.create_table('setor',
    sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('nome_cvm', sa.String(length=120), nullable=False),
    sa.Column('setor_base', sa.String(length=120), nullable=False),
    sa.Column('holding', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nome_cvm')
    )
    op.create_index(op.f('ix_setor_setor_base'), 'setor', ['setor_base'], unique=False)
    op.create_table('companhia',
    sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('cnpj', sa.String(length=14), nullable=False),
    sa.Column('cd_cvm', sa.Integer(), nullable=True),
    sa.Column('denominacao', sa.String(length=200), nullable=False),
    sa.Column('nome_comercial', sa.String(length=200), nullable=True),
    sa.Column('setor_id', sa.Integer(), nullable=True),
    sa.Column('categoria_registro', sa.String(length=40), nullable=True),
    sa.Column('situacao_registro', sa.String(length=60), nullable=True),
    sa.Column('situacao_emissor', sa.String(length=80), nullable=True),
    sa.Column('controle_acionario', sa.String(length=60), nullable=True),
    sa.Column('uf', sa.String(length=2), nullable=True),
    sa.Column('municipio', sa.String(length=120), nullable=True),
    sa.Column('data_registro', sa.Date(), nullable=True),
    sa.Column('data_constituicao', sa.Date(), nullable=True),
    sa.Column('data_cancelamento', sa.Date(), nullable=True),
    sa.Column('ativa', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("cnpj ~ '^[0-9]{14}$'", name='ck_companhia_cnpj_digitos'),
    sa.ForeignKeyConstraint(['setor_id'], ['setor.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cnpj')
    )
    op.create_index(op.f('ix_companhia_ativa'), 'companhia', ['ativa'], unique=False)
    op.create_index(op.f('ix_companhia_cd_cvm'), 'companhia', ['cd_cvm'], unique=False)
    op.create_index(op.f('ix_companhia_setor_id'), 'companhia', ['setor_id'], unique=False)
    op.create_table('serie_macro_valor',
    sa.Column('serie_id', sa.Integer(), nullable=False),
    sa.Column('data', sa.Date(), nullable=False),
    sa.Column('valor', sa.Numeric(precision=24, scale=8), nullable=True),
    sa.ForeignKeyConstraint(['serie_id'], ['serie_macro.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('serie_id', 'data')
    )
    op.create_table('companhia_mercado',
    sa.Column('companhia_id', sa.Integer(), nullable=False),
    sa.Column('tipo_mercado', sa.String(length=40), nullable=False),
    sa.ForeignKeyConstraint(['companhia_id'], ['companhia.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('companhia_id', 'tipo_mercado')
    )
    op.create_table('documento',
    sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('companhia_id', sa.Integer(), nullable=False),
    sa.Column('tipo', sa.String(length=3), nullable=False),
    sa.Column('dt_referencia', sa.Date(), nullable=False),
    sa.Column('versao', sa.SmallInteger(), nullable=False),
    sa.Column('vigente', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('id_doc_cvm', sa.Integer(), nullable=True),
    sa.Column('dt_recebimento', sa.Date(), nullable=True),
    sa.Column('link', sa.String(length=300), nullable=True),
    sa.Column('carga_id', sa.Integer(), nullable=True),
    sa.CheckConstraint("tipo IN ('DFP', 'ITR')", name='ck_documento_tipo'),
    sa.ForeignKeyConstraint(['carga_id'], ['carga_arquivo.id'], ),
    sa.ForeignKeyConstraint(['companhia_id'], ['companhia.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('companhia_id', 'tipo', 'dt_referencia', 'versao', name='uq_documento_versao')
    )
    op.create_index(op.f('ix_documento_companhia_id'), 'documento', ['companhia_id'], unique=False)
    op.create_index('ix_documento_tipo_referencia', 'documento', ['tipo', 'dt_referencia'], unique=False)
    op.create_index('uq_documento_vigente', 'documento', ['companhia_id', 'tipo', 'dt_referencia'], unique=True, postgresql_where=sa.text('vigente'))
    op.create_table('composicao_capital',
    sa.Column('documento_id', sa.Integer(), nullable=False),
    sa.Column('acoes_ordinarias', sa.BigInteger(), nullable=True),
    sa.Column('acoes_preferenciais', sa.BigInteger(), nullable=True),
    sa.Column('acoes_total', sa.BigInteger(), nullable=True),
    sa.Column('tesouraria_ordinarias', sa.BigInteger(), nullable=True),
    sa.Column('tesouraria_preferenciais', sa.BigInteger(), nullable=True),
    sa.Column('tesouraria_total', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['documento_id'], ['documento.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('documento_id')
    )
    op.create_table('demonstracao_linha',
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
    sa.Column('ano_referencia', sa.SmallInteger(), nullable=False),
    sa.Column('documento_id', sa.Integer(), nullable=False),
    sa.Column('demonstracao', sa.String(length=8), nullable=False),
    sa.Column('escopo', sa.String(length=3), nullable=False),
    sa.Column('ordem_exercicio', sa.String(length=10), nullable=False),
    sa.Column('dt_inicio', sa.Date(), nullable=True),
    sa.Column('dt_fim', sa.Date(), nullable=False),
    sa.Column('coluna_df', sa.String(length=120), nullable=True),
    sa.Column('cd_conta', sa.String(length=20), nullable=False),
    sa.Column('ds_conta', sa.String(length=200), nullable=False),
    sa.Column('valor_original', sa.Numeric(precision=28, scale=6), nullable=True),
    sa.Column('escala', sa.String(length=7), nullable=False),
    sa.Column('moeda', sa.String(length=10), server_default=sa.text("'REAL'"), nullable=False),
    sa.Column('valor_reais', sa.Numeric(precision=30, scale=2), nullable=True),
    sa.Column('conta_fixa', sa.Boolean(), nullable=True),
    sa.Column('sequencia', sa.Integer(), nullable=False),
    sa.CheckConstraint("demonstracao IN ('BPA', 'BPP', 'DRE', 'DRA', 'DFC_MD', 'DFC_MI', 'DMPL', 'DVA')", name='ck_linha_demonstracao'),
    sa.CheckConstraint("escala IN ('UNIDADE', 'MIL')", name='ck_linha_escala'),
    sa.CheckConstraint("escopo IN ('CON', 'IND')", name='ck_linha_escopo'),
    sa.CheckConstraint("ordem_exercicio IN ('ULTIMO', 'PENULTIMO')", name='ck_linha_ordem'),
    sa.ForeignKeyConstraint(['documento_id'], ['documento.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'ano_referencia'),
    postgresql_partition_by='RANGE (ano_referencia)'
    )
    op.create_index('ix_linha_conta', 'demonstracao_linha', ['demonstracao', 'cd_conta', 'dt_fim'], unique=False)
    op.create_index('ix_linha_documento', 'demonstracao_linha', ['documento_id', 'demonstracao', 'escopo'], unique=False)
    # Partições anuais da tabela de linhas, com uma partição padrão de segurança.
    for ano in range(ANO_PARTICAO_INICIAL, ANO_PARTICAO_FINAL + 1):
        op.execute(
            f"CREATE TABLE demonstracao_linha_{ano} PARTITION OF demonstracao_linha "
            f"FOR VALUES FROM ({ano}) TO ({ano + 1})"
        )
    op.execute("CREATE TABLE demonstracao_linha_outros PARTITION OF demonstracao_linha DEFAULT")
    op.create_table('parecer',
    sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('documento_id', sa.Integer(), nullable=False),
    sa.Column('tipo_relatorio', sa.String(length=40), nullable=True),
    sa.Column('tipo_parecer', sa.String(length=200), nullable=True),
    sa.Column('item', sa.SmallInteger(), nullable=True),
    sa.Column('texto', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['documento_id'], ['documento.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_parecer_documento_id'), 'parecer', ['documento_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_parecer_documento_id'), table_name='parecer')
    op.drop_table('parecer')
    op.drop_index('ix_linha_documento', table_name='demonstracao_linha')
    op.drop_index('ix_linha_conta', table_name='demonstracao_linha')
    op.drop_table('demonstracao_linha')
    op.drop_table('composicao_capital')
    op.drop_index('uq_documento_vigente', table_name='documento', postgresql_where=sa.text('vigente'))
    op.drop_index('ix_documento_tipo_referencia', table_name='documento')
    op.drop_index(op.f('ix_documento_companhia_id'), table_name='documento')
    op.drop_table('documento')
    op.drop_table('companhia_mercado')
    op.drop_table('serie_macro_valor')
    op.drop_index(op.f('ix_companhia_setor_id'), table_name='companhia')
    op.drop_index(op.f('ix_companhia_cd_cvm'), table_name='companhia')
    op.drop_index(op.f('ix_companhia_ativa'), table_name='companhia')
    op.drop_table('companhia')
    op.drop_index(op.f('ix_setor_setor_base'), table_name='setor')
    op.drop_table('setor')
    op.drop_table('serie_macro')
    op.drop_table('carga_arquivo')
