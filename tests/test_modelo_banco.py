"""Testes do esquema do banco. Exigem um PostgreSQL com pgvector em DATABASE_URL."""

import datetime as dt
import os
from decimal import Decimal
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(
    not os.environ.get("DATABASE_URL"), reason="DATABASE_URL não definida"
)

RAIZ = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def engine():
    from alembic import command
    from alembic.config import Config

    from empresometro.db.config import criar_engine

    cfg = Config(str(RAIZ / "alembic.ini"))
    cfg.set_main_option("script_location", str(RAIZ / "migrations"))
    command.downgrade(cfg, "base")
    command.upgrade(cfg, "head")
    eng = criar_engine()
    yield eng
    eng.dispose()
    command.downgrade(cfg, "base")


@pytest.fixture()
def sessao(engine):
    from sqlalchemy.orm import Session

    with Session(engine) as s:
        yield s
        s.rollback()


def _companhia(sessao, cnpj="11111111000111"):
    from empresometro.db.models import Companhia, CompanhiaMercado, Setor

    setor = Setor(nome_cvm=f"Emp. Adm. Part. - Bancos {cnpj}", setor_base="Bancos", holding=True)
    cia = Companhia(
        cnpj=cnpj,
        cd_cvm=1023,
        denominacao="ALFA S.A.",
        setor=setor,
        situacao_registro="ATIVO",
        situacao_emissor="FASE OPERACIONAL",
        ativa=True,
        mercados=[CompanhiaMercado(tipo_mercado="BOLSA"), CompanhiaMercado(tipo_mercado="BALCÃO ORGANIZADO")],
    )
    sessao.add(cia)
    sessao.flush()
    return cia


def test_tabelas_extensao_e_particoes(engine):
    from sqlalchemy import inspect, text

    tabelas = set(inspect(engine).get_table_names())
    assert {
        "setor", "companhia", "companhia_mercado", "carga_arquivo", "documento",
        "demonstracao_linha", "composicao_capital", "parecer", "serie_macro", "serie_macro_valor",
    } <= tabelas
    with engine.connect() as c:
        assert c.execute(text("SELECT count(*) FROM pg_extension WHERE extname='vector'")).scalar() == 1
        particoes = c.execute(
            text("SELECT count(*) FROM pg_inherits WHERE inhparent = 'demonstracao_linha'::regclass")
        ).scalar()
    assert particoes == 10


def test_modelos_e_migracao_estao_alinhados(engine):
    from alembic.autogenerate import compare_metadata
    from alembic.migration import MigrationContext

    from empresometro.db.models import Base

    def somente_do_modelo(objeto, nome, tipo, refletido, comparado):
        # As partições existem só no banco; não são tabelas do modelo.
        return not (tipo == "table" and refletido and nome.startswith("demonstracao_linha_"))

    with engine.connect() as c:
        contexto = MigrationContext.configure(c, opts={"include_object": somente_do_modelo})
        assert compare_metadata(contexto, Base.metadata) == []


def test_companhia_com_dois_mercados(sessao):
    cia = _companhia(sessao)
    assert {m.tipo_mercado for m in cia.mercados} == {"BOLSA", "BALCÃO ORGANIZADO"}
    assert cia.setor.setor_base == "Bancos"


def test_cnpj_precisa_ter_14_digitos(sessao):
    from sqlalchemy.exc import IntegrityError

    from empresometro.db.models import Companhia

    sessao.add(Companhia(cnpj="11.111.111/00", denominacao="X"))
    with pytest.raises(IntegrityError):
        sessao.flush()


def test_versoes_e_apenas_uma_vigente(sessao):
    from sqlalchemy.exc import IntegrityError

    from empresometro.db.models import Documento

    cia = _companhia(sessao, "22222222000122")
    ref = dt.date(2025, 12, 31)
    sessao.add_all(
        [
            Documento(companhia_id=cia.id, tipo="DFP", dt_referencia=ref, versao=1, vigente=False),
            Documento(companhia_id=cia.id, tipo="DFP", dt_referencia=ref, versao=2, vigente=True),
        ]
    )
    sessao.flush()
    sessao.add(Documento(companhia_id=cia.id, tipo="DFP", dt_referencia=ref, versao=3, vigente=True))
    with pytest.raises(IntegrityError):
        sessao.flush()


def test_linha_vai_para_a_particao_do_ano(sessao):
    from sqlalchemy import text

    from empresometro.db.models import DemonstracaoLinha, Documento

    cia = _companhia(sessao, "33333333000133")
    doc = Documento(
        companhia_id=cia.id, tipo="ITR", dt_referencia=dt.date(2026, 9, 30), versao=1, vigente=True
    )
    sessao.add(doc)
    sessao.flush()
    linha = dict(
        ano_referencia=2026, documento_id=doc.id, demonstracao="DRE", escopo="CON",
        ordem_exercicio="ULTIMO", dt_inicio=dt.date(2026, 7, 1), dt_fim=dt.date(2026, 9, 30),
        cd_conta="3.01", ds_conta="Receita de Venda de Bens e/ou Serviços",
        valor_original=Decimal("1500.5"), escala="MIL", valor_reais=Decimal("1500500.00"),
        conta_fixa=True,
    )
    # A mesma combinação pode se repetir no arquivo da CVM; a sequência distingue as linhas.
    sessao.add_all([DemonstracaoLinha(**linha, sequencia=1), DemonstracaoLinha(**linha, sequencia=2)])
    sessao.flush()
    assert sessao.execute(text("SELECT count(*) FROM demonstracao_linha_2026")).scalar() == 2
    assert sessao.execute(text("SELECT sum(valor_reais) FROM demonstracao_linha")).scalar() == Decimal("3001000.00")


def test_dominios_sao_validados(sessao):
    from sqlalchemy.exc import IntegrityError

    from empresometro.db.models import Documento

    cia = _companhia(sessao, "44444444000144")
    sessao.add(Documento(companhia_id=cia.id, tipo="XYZ", dt_referencia=dt.date(2025, 12, 31), versao=1))
    with pytest.raises(IntegrityError):
        sessao.flush()
