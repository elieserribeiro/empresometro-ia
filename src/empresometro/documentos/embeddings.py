"""Exportação dos trechos para o Colab e importação dos vetores gerados."""

from __future__ import annotations

import csv
import gzip
from pathlib import Path

import psycopg

MODELO_PADRAO = "BAAI/bge-m3"
DIMENSOES = 1024
NOME_DO_INDICE = "ix_trecho_embedding_hnsw"

csv.field_size_limit(10**9)


def exportar_trechos(conn: psycopg.Connection, destino: Path, somente_pendentes: bool = True) -> int:
    """Grava um CSV compactado (id;texto) com os trechos que ainda não têm vetor."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    filtro = (
        "WHERE NOT EXISTS (SELECT 1 FROM trecho_embedding e WHERE e.trecho_id = t.id)" if somente_pendentes else ""
    )
    total = 0
    with (
        gzip.open(destino, "wt", encoding="utf-8", newline="") as arquivo,
        conn.transaction(),
        conn.cursor(name="exportacao") as cur,
    ):
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(["id", "texto"])
        cur.itersize = 5000
        cur.execute(f"SELECT t.id, t.texto FROM trecho t {filtro} ORDER BY t.id")
        for trecho_id, texto in cur:
            escritor.writerow([trecho_id, texto])
            total += 1
    return total


def importar_embeddings(conn: psycopg.Connection, arquivo: Path, modelo: str = MODELO_PADRAO, registrar=print) -> dict:
    """Carrega um arquivo .npz (ids, embeddings) na tabela trecho_embedding.

    Vetores de trechos que não existem mais no banco são ignorados; os já
    carregados são substituídos.
    """
    import numpy as np

    dados = np.load(arquivo)
    ids, vetores = dados["ids"], dados["embeddings"]
    if vetores.ndim != 2 or vetores.shape[1] != DIMENSOES or len(ids) != len(vetores):
        raise ValueError(
            f"Formato inesperado: ids {ids.shape}, embeddings {vetores.shape}; esperado N x {DIMENSOES}."
        )
    existentes = {linha[0] for linha in conn.execute("SELECT id FROM trecho").fetchall()}
    carregados = ignorados = 0
    with conn.transaction(), conn.cursor() as cur:
        cur.execute("CREATE TEMP TABLE novos (trecho_id bigint, embedding text) ON COMMIT DROP")
        with cur.copy("COPY novos (trecho_id, embedding) FROM STDIN") as copia:
            for trecho_id, vetor in zip(ids.tolist(), vetores):
                if trecho_id not in existentes:
                    ignorados += 1
                    continue
                texto = "[" + ",".join(f"{v:.5f}" for v in vetor.astype("float32").tolist()) + "]"
                copia.write_row((trecho_id, texto))
                carregados += 1
                if carregados % 20000 == 0:
                    registrar(f"  {carregados} vetores enviados...")
        cur.execute("DELETE FROM trecho_embedding e USING novos n WHERE e.trecho_id = n.trecho_id")
        cur.execute(
            "INSERT INTO trecho_embedding (trecho_id, modelo, embedding) "
            f"SELECT trecho_id, %s, embedding::vector({DIMENSOES}) FROM novos",
            (modelo,),
        )
    return {"carregados": carregados, "ignorados": ignorados}


def criar_indice(conn: psycopg.Connection) -> None:
    """Cria o índice HNSW para busca por similaridade de cosseno."""
    conn.execute(
        f"CREATE INDEX IF NOT EXISTS {NOME_DO_INDICE} ON trecho_embedding USING hnsw (embedding vector_cosine_ops)"
    )
    conn.execute("ANALYZE trecho_embedding")


def situacao(conn: psycopg.Connection) -> dict:
    trechos, com_vetor = conn.execute(
        "SELECT (SELECT count(*) FROM trecho), (SELECT count(*) FROM trecho_embedding)"
    ).fetchone()
    return {"trechos": trechos, "com_vetor": com_vetor, "pendentes": trechos - com_vetor}
