"""Extração de texto de PDFs e segmentação em trechos com página de origem."""

from __future__ import annotations

import io
import re

TAMANHO_ALVO = 1200      # caracteres por trecho
TAMANHO_MAXIMO = 1800
SOBREPOSICAO = 150       # caracteres repetidos entre trechos vizinhos
MAXIMO_DE_PAGINAS = 400


def limpar(texto: str) -> str:
    """Normaliza espaços e remove caracteres de controle, preservando parágrafos."""
    texto = texto.replace("\x00", "").replace("\r", "\n")
    texto = re.sub(r"[ \t ]+", " ", texto)
    texto = re.sub(r" ?\n ?", "\n", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()


def extrair_paginas(pdf: bytes, maximo: int = MAXIMO_DE_PAGINAS) -> list[str]:
    """Devolve o texto de cada página do PDF (vazio quando a página é só imagem)."""
    from pypdf import PdfReader

    leitor = PdfReader(io.BytesIO(pdf), strict=False)
    paginas = []
    for pagina in leitor.pages[:maximo]:
        try:
            paginas.append(limpar(pagina.extract_text() or ""))
        except Exception:  # noqa: BLE001 - página ilegível não invalida o documento
            paginas.append("")
    return paginas


def _partes(texto: str) -> list[str]:
    """Quebra o texto em unidades pequenas: parágrafos e, se preciso, frases ou blocos fixos."""
    unidades: list[str] = []
    for paragrafo in re.split(r"\n\s*\n", texto):
        paragrafo = paragrafo.strip()
        if not paragrafo:
            continue
        if len(paragrafo) <= TAMANHO_ALVO:
            unidades.append(paragrafo)
            continue
        atual = ""
        for frase in re.split(r"(?<=[.!?;:])\s+|\n", paragrafo):
            while len(frase) > TAMANHO_MAXIMO:  # frase gigante (tabelas sem pontuação)
                unidades.append(frase[:TAMANHO_ALVO])
                frase = frase[TAMANHO_ALVO:]
            if len(atual) + len(frase) + 1 > TAMANHO_ALVO and atual:
                unidades.append(atual)
                atual = frase
            else:
                atual = f"{atual} {frase}".strip()
        if atual:
            unidades.append(atual)
    return unidades


def segmentar(paginas: list[str]) -> list[dict]:
    """Agrupa o texto das páginas em trechos de tamanho próximo ao alvo.

    Cada trecho registra a primeira e a última página de onde veio, para a citação.
    Trechos vizinhos compartilham um pequeno final/início, para não cortar o contexto.
    """
    unidades: list[tuple[str, int]] = []
    for numero, texto in enumerate(paginas, start=1):
        unidades.extend((parte, numero) for parte in _partes(texto))

    trechos: list[dict] = []
    atual: list[tuple[str, int]] = []
    tamanho = 0
    novas = 0  # unidades acrescentadas desde o último fechamento (fora a sobreposição)

    def emitir() -> str:
        texto = "\n".join(parte for parte, _ in atual)
        trechos.append(
            {"texto": texto, "pagina_inicial": atual[0][1], "pagina_final": atual[-1][1], "caracteres": len(texto)}
        )
        return texto

    for parte, pagina in unidades:
        if novas and tamanho + len(parte) > TAMANHO_ALVO:
            texto = emitir()
            # Sobreposição: o fim deste trecho abre o próximo.
            cauda = texto[-SOBREPOSICAO:]
            corte = cauda.find(" ")
            cauda = cauda[corte + 1:] if corte >= 0 else cauda
            atual = [(cauda, atual[-1][1])] if len(texto) > SOBREPOSICAO * 2 else []
            tamanho = sum(len(p) for p, _ in atual)
            novas = 0
        atual.append((parte, pagina))
        tamanho += len(parte) + 1
        novas += 1
    if novas:
        emitir()
    return trechos
