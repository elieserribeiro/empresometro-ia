"""Modelo relacional do Empresômetro IA (camada Trusted).

Decisões refletidas aqui:
- todas as companhias ativas entram, com situação do registro e do emissor;
- uma companhia pode negociar em mais de um mercado;
- todas as versões dos documentos são guardadas, com marca da versão vigente;
- todas as contas das demonstrações são guardadas, em tabela única particionada por ano;
- o valor é guardado como publicado pela CVM e também convertido em reais;
- o setor é mantido como a CVM informa, com um setor-base para agrupamento.
"""

from __future__ import annotations

import datetime as dt
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Identity,
    Index,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

TIPOS_DOCUMENTO = ("DFP", "ITR")
DEMONSTRACOES = ("BPA", "BPP", "DRE", "DRA", "DFC_MD", "DFC_MI", "DMPL", "DVA")
ESCOPOS = ("CON", "IND")
ORDENS_EXERCICIO = ("ULTIMO", "PENULTIMO")
ESCALAS = ("UNIDADE", "MIL")


def _em(valores: tuple[str, ...]) -> str:
    return ", ".join(f"'{v}'" for v in valores)


class Base(DeclarativeBase):
    pass


class Setor(Base):
    __tablename__ = "setor"

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    nome_cvm: Mapped[str] = mapped_column(String(120), unique=True)
    setor_base: Mapped[str] = mapped_column(String(120), index=True)
    holding: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))

    companhias: Mapped[list[Companhia]] = relationship(back_populates="setor")


class Companhia(Base):
    __tablename__ = "companhia"

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    cnpj: Mapped[str] = mapped_column(String(14), unique=True)
    cd_cvm: Mapped[int | None] = mapped_column(Integer, index=True)
    denominacao: Mapped[str] = mapped_column(String(200))
    nome_comercial: Mapped[str | None] = mapped_column(String(200))
    setor_id: Mapped[int | None] = mapped_column(ForeignKey("setor.id"), index=True)
    categoria_registro: Mapped[str | None] = mapped_column(String(40))
    situacao_registro: Mapped[str | None] = mapped_column(String(60))
    situacao_emissor: Mapped[str | None] = mapped_column(String(80))
    controle_acionario: Mapped[str | None] = mapped_column(String(60))
    uf: Mapped[str | None] = mapped_column(String(2))
    municipio: Mapped[str | None] = mapped_column(String(120))
    data_registro: Mapped[dt.date | None] = mapped_column(Date)
    data_constituicao: Mapped[dt.date | None] = mapped_column(Date)
    data_cancelamento: Mapped[dt.date | None] = mapped_column(Date)
    ativa: Mapped[bool] = mapped_column(Boolean, server_default=text("false"), index=True)
    atualizado_em: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    setor: Mapped[Setor | None] = relationship(back_populates="companhias")
    mercados: Mapped[list[CompanhiaMercado]] = relationship(
        back_populates="companhia", cascade="all, delete-orphan"
    )
    documentos: Mapped[list[Documento]] = relationship(back_populates="companhia")

    __table_args__ = (
        CheckConstraint("cnpj ~ '^[0-9]{14}$'", name="ck_companhia_cnpj_digitos"),
    )


class CompanhiaMercado(Base):
    __tablename__ = "companhia_mercado"

    companhia_id: Mapped[int] = mapped_column(
        ForeignKey("companhia.id", ondelete="CASCADE"), primary_key=True
    )
    tipo_mercado: Mapped[str] = mapped_column(String(40), primary_key=True)

    companhia: Mapped[Companhia] = relationship(back_populates="mercados")


class CargaArquivo(Base):
    """Linhagem: cada arquivo baixado de uma fonte pública."""

    __tablename__ = "carga_arquivo"

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    fonte: Mapped[str] = mapped_column(String(40))
    url: Mapped[str] = mapped_column(String(500))
    nome_arquivo: Mapped[str] = mapped_column(String(200))
    sha256: Mapped[str] = mapped_column(String(64))
    bytes: Mapped[int | None] = mapped_column(BigInteger)
    modificado_na_fonte: Mapped[dt.datetime | None] = mapped_column(DateTime(timezone=True))
    baixado_em: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True))
    linhas: Mapped[int | None] = mapped_column(BigInteger)

    __table_args__ = (UniqueConstraint("url", "sha256", name="uq_carga_arquivo_url_sha256"),)


class Documento(Base):
    """Cada DFP ou ITR entregue, em cada versão."""

    __tablename__ = "documento"

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    companhia_id: Mapped[int] = mapped_column(ForeignKey("companhia.id"), index=True)
    tipo: Mapped[str] = mapped_column(String(3))
    dt_referencia: Mapped[dt.date] = mapped_column(Date)
    versao: Mapped[int] = mapped_column(SmallInteger)
    vigente: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    id_doc_cvm: Mapped[int | None] = mapped_column(Integer)
    dt_recebimento: Mapped[dt.date | None] = mapped_column(Date)
    link: Mapped[str | None] = mapped_column(String(300))
    carga_id: Mapped[int | None] = mapped_column(ForeignKey("carga_arquivo.id"))

    companhia: Mapped[Companhia] = relationship(back_populates="documentos")

    __table_args__ = (
        CheckConstraint(f"tipo IN ({_em(TIPOS_DOCUMENTO)})", name="ck_documento_tipo"),
        UniqueConstraint(
            "companhia_id", "tipo", "dt_referencia", "versao", name="uq_documento_versao"
        ),
        # No máximo uma versão vigente por companhia, tipo e data de referência.
        Index(
            "uq_documento_vigente",
            "companhia_id",
            "tipo",
            "dt_referencia",
            unique=True,
            postgresql_where=text("vigente"),
        ),
        Index("ix_documento_tipo_referencia", "tipo", "dt_referencia"),
    )


class DemonstracaoLinha(Base):
    """Cada conta de cada demonstração, particionada pelo ano de referência.

    Os arquivos da CVM têm algumas linhas repetidas mesmo na combinação mais
    completa de colunas; por isso a identificação usa `id` e `sequencia`
    (posição da linha no arquivo), sem restrição de unicidade natural.
    """

    __tablename__ = "demonstracao_linha"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    ano_referencia: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    documento_id: Mapped[int] = mapped_column(Integer)
    demonstracao: Mapped[str] = mapped_column(String(8))
    escopo: Mapped[str] = mapped_column(String(3))
    ordem_exercicio: Mapped[str] = mapped_column(String(10))
    dt_inicio: Mapped[dt.date | None] = mapped_column(Date)
    dt_fim: Mapped[dt.date] = mapped_column(Date)
    coluna_df: Mapped[str | None] = mapped_column(String(120))
    cd_conta: Mapped[str] = mapped_column(String(20))
    ds_conta: Mapped[str] = mapped_column(String(200))
    valor_original: Mapped[Decimal | None] = mapped_column(Numeric(28, 6))
    escala: Mapped[str] = mapped_column(String(7))
    moeda: Mapped[str] = mapped_column(String(10), server_default=text("'REAL'"))
    valor_reais: Mapped[Decimal | None] = mapped_column(Numeric(30, 2))
    conta_fixa: Mapped[bool | None] = mapped_column(Boolean)
    sequencia: Mapped[int] = mapped_column(Integer)

    __table_args__ = (
        ForeignKeyConstraint(["documento_id"], ["documento.id"], ondelete="CASCADE"),
        CheckConstraint(f"demonstracao IN ({_em(DEMONSTRACOES)})", name="ck_linha_demonstracao"),
        CheckConstraint(f"escopo IN ({_em(ESCOPOS)})", name="ck_linha_escopo"),
        CheckConstraint(f"ordem_exercicio IN ({_em(ORDENS_EXERCICIO)})", name="ck_linha_ordem"),
        CheckConstraint(f"escala IN ({_em(ESCALAS)})", name="ck_linha_escala"),
        Index("ix_linha_documento", "documento_id", "demonstracao", "escopo"),
        Index("ix_linha_conta", "demonstracao", "cd_conta", "dt_fim"),
        {"postgresql_partition_by": "RANGE (ano_referencia)"},
    )


class ComposicaoCapital(Base):
    __tablename__ = "composicao_capital"

    documento_id: Mapped[int] = mapped_column(
        ForeignKey("documento.id", ondelete="CASCADE"), primary_key=True
    )
    acoes_ordinarias: Mapped[int | None] = mapped_column(BigInteger)
    acoes_preferenciais: Mapped[int | None] = mapped_column(BigInteger)
    acoes_total: Mapped[int | None] = mapped_column(BigInteger)
    tesouraria_ordinarias: Mapped[int | None] = mapped_column(BigInteger)
    tesouraria_preferenciais: Mapped[int | None] = mapped_column(BigInteger)
    tesouraria_total: Mapped[int | None] = mapped_column(BigInteger)


class Parecer(Base):
    """Pareceres e declarações que acompanham o documento (também usados no RAG)."""

    __tablename__ = "parecer"

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    documento_id: Mapped[int] = mapped_column(
        ForeignKey("documento.id", ondelete="CASCADE"), index=True
    )
    tipo_relatorio: Mapped[str | None] = mapped_column(String(40))
    tipo_parecer: Mapped[str | None] = mapped_column(String(200))
    item: Mapped[int | None] = mapped_column(SmallInteger)
    texto: Mapped[str | None] = mapped_column(Text)


class SerieMacro(Base):
    __tablename__ = "serie_macro"

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    fonte: Mapped[str] = mapped_column(String(20))
    codigo: Mapped[str] = mapped_column(String(60))
    nome: Mapped[str] = mapped_column(String(200))
    unidade: Mapped[str | None] = mapped_column(String(60))
    periodicidade: Mapped[str | None] = mapped_column(String(20))

    __table_args__ = (UniqueConstraint("fonte", "codigo", name="uq_serie_macro_fonte_codigo"),)


class SerieMacroValor(Base):
    __tablename__ = "serie_macro_valor"

    serie_id: Mapped[int] = mapped_column(
        ForeignKey("serie_macro.id", ondelete="CASCADE"), primary_key=True
    )
    data: Mapped[dt.date] = mapped_column(Date, primary_key=True)
    valor: Mapped[Decimal | None] = mapped_column(Numeric(24, 8))
