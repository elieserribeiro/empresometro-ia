"""Aquisição dos arquivos públicos e conexão com o banco."""

from __future__ import annotations

import datetime as dt
import email.utils
import hashlib
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

import psycopg

BASE_CVM = "https://dados.cvm.gov.br/dados/CIA_ABERTA"
URL_CADASTRO = f"{BASE_CVM}/CAD/DADOS/cad_cia_aberta.csv"
CODIFICACAO_CVM = "latin-1"
USER_AGENT = "empresometro-ia-etl/1.0 (+https://github.com/elieserribeiro/empresometro-ia)"
URL_BANCO_PADRAO = "postgresql://empresometro:empresometro@localhost:5432/empresometro"


def url_documentos(tipo: str, ano: int) -> str:
    return f"{BASE_CVM}/DOC/{tipo.upper()}/DADOS/{tipo.lower()}_cia_aberta_{ano}.zip"


def conectar(url: str | None = None) -> psycopg.Connection:
    """Abre uma conexão psycopg a partir de DATABASE_URL (aceita o prefixo do SQLAlchemy)."""
    url = url or os.environ.get("DATABASE_URL", URL_BANCO_PADRAO)
    return psycopg.connect(url.replace("postgresql+psycopg://", "postgresql://"))


def sha256_do_arquivo(caminho: Path) -> str:
    sha = hashlib.sha256()
    with open(caminho, "rb") as arquivo:
        while bloco := arquivo.read(1 << 20):
            sha.update(bloco)
    return sha.hexdigest()


def baixar(url: str, destino: Path, tentativas: int = 3, timeout: int = 300) -> dict:
    """Baixa uma URL para `destino` e devolve os metadados da aquisição."""
    info: dict = {"url": url, "ok": False, "caminho": destino}
    for tentativa in range(1, tentativas + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                destino.parent.mkdir(parents=True, exist_ok=True)
                temporario = destino.with_suffix(destino.suffix + ".parcial")
                with open(temporario, "wb") as arquivo:
                    while bloco := resp.read(1 << 20):
                        arquivo.write(bloco)
                temporario.replace(destino)
                modificado = resp.headers.get("Last-Modified")
                info.update(
                    ok=True,
                    bytes=destino.stat().st_size,
                    sha256=sha256_do_arquivo(destino),
                    modificado_na_fonte=(
                        email.utils.parsedate_to_datetime(modificado) if modificado else None
                    ),
                    baixado_em=dt.datetime.now(dt.timezone.utc),
                )
                return info
        except urllib.error.HTTPError as erro:
            info["erro"] = f"HTTP {erro.code}"
            if erro.code == 404:
                return info
        except Exception as erro:  # noqa: BLE001 - a falha é registrada e reportada
            info["erro"] = f"{type(erro).__name__}: {erro}"
        if tentativa < tentativas:
            time.sleep(5 * tentativa)
    return info


def descrever_local(url: str, caminho: Path) -> dict:
    """Metadados de um arquivo já presente em disco (usado em testes e recargas)."""
    return {
        "url": url,
        "ok": True,
        "caminho": caminho,
        "bytes": caminho.stat().st_size,
        "sha256": sha256_do_arquivo(caminho),
        "modificado_na_fonte": None,
        "baixado_em": dt.datetime.now(dt.timezone.utc),
    }


def ja_carregado(conn: psycopg.Connection, url: str, sha256: str) -> bool:
    """Carga incremental: o mesmo arquivo (mesmo hash) já foi processado até o fim?"""
    linha = conn.execute(
        "SELECT 1 FROM carga_arquivo WHERE url = %s AND sha256 = %s AND linhas IS NOT NULL",
        (url, sha256),
    ).fetchone()
    return linha is not None


def registrar_carga(conn: psycopg.Connection, fonte: str, info: dict) -> int:
    """Cria (ou reaproveita) o registro de linhagem do arquivo e devolve o id."""
    return conn.execute(
        """
        INSERT INTO carga_arquivo (fonte, url, nome_arquivo, sha256, bytes, modificado_na_fonte, baixado_em)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT ON CONSTRAINT uq_carga_arquivo_url_sha256
        DO UPDATE SET baixado_em = EXCLUDED.baixado_em, linhas = NULL
        RETURNING id
        """,
        (
            fonte,
            info["url"],
            Path(info["caminho"]).name,
            info["sha256"],
            info["bytes"],
            info["modificado_na_fonte"],
            info["baixado_em"],
        ),
    ).fetchone()[0]
