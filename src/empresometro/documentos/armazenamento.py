"""Gravação de documentos e trechos no banco."""

from __future__ import annotations

import hashlib

import psycopg

from .texto import extrair_paginas, segmentar


def ja_coletado(conn: psycopg.Connection, fonte: str, chave: str) -> bool:
    linha = conn.execute(
        "SELECT 1 FROM documento_texto WHERE fonte = %s AND chave_origem = %s AND situacao <> 'ERRO'",
        (fonte, chave),
    ).fetchone()
    return linha is not None


def gravar_documento(
    conn: psycopg.Connection, *, companhia_id: int, fonte: str, chave: str, titulo: str,
    paginas: list[str] | None = None, pdf: bytes | None = None, erro: str | None = None, **campos,
) -> dict:
    """Grava um documento e seus trechos; devolve um resumo (situação, páginas, trechos).

    Recebe o PDF (o texto é extraído aqui) ou as páginas já em texto.
    """
    sha = hashlib.sha256(pdf).hexdigest() if pdf else None
    if erro is None and pdf is not None:
        try:
            paginas = extrair_paginas(pdf)
        except Exception as falha:  # noqa: BLE001
            erro = f"Falha ao ler o PDF: {type(falha).__name__}: {falha}"
    trechos = segmentar(paginas) if (erro is None and paginas) else []
    caracteres = sum(len(p) for p in (paginas or []))
    situacao = "ERRO" if erro else ("OK" if trechos else "SEM_TEXTO")

    with conn.transaction(), conn.cursor() as cur:
        cur.execute("DELETE FROM documento_texto WHERE fonte = %s AND chave_origem = %s", (fonte, chave))
        documento_id = cur.execute(
            """
            INSERT INTO documento_texto (companhia_id, fonte, chave_origem, categoria, tipo, secao, titulo,
                dt_referencia, dt_entrega, versao, link, arquivo_sha256, paginas, caracteres, situacao, erro)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            """,
            (
                companhia_id, fonte, chave[:200], campos.get("categoria"), (campos.get("tipo") or None),
                campos.get("secao"), (titulo or "(sem título)")[:2000], campos.get("dt_referencia"),
                campos.get("dt_entrega"), campos.get("versao"), campos.get("link"), sha,
                len(paginas) if paginas else None, caracteres, situacao, (erro or None) and erro[:1000],
            ),
        ).fetchone()[0]
        if trechos:
            with cur.copy(
                "COPY trecho (documento_texto_id, ordem, pagina_inicial, pagina_final, texto, caracteres) FROM STDIN"
            ) as copia:
                for ordem, t in enumerate(trechos, start=1):
                    copia.write_row(
                        (documento_id, ordem, t["pagina_inicial"], t["pagina_final"], t["texto"], t["caracteres"])
                    )
    return {"situacao": situacao, "paginas": len(paginas or []), "trechos": len(trechos), "caracteres": caracteres}
