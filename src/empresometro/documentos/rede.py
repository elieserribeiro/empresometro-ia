"""Download educado de documentos do site da CVM: pausa entre requisições e novas tentativas."""

from __future__ import annotations

import time
import urllib.request

from ..etl.fontes import USER_AGENT

PAUSA_ENTRE_REQUISICOES = 1.0   # segundos
ESPERAS_APOS_FALHA = (10, 30, 60)
TAMANHO_MINIMO = 500            # respostas menores são mensagens de erro do servidor
TAMANHO_MAXIMO = 60 * 1024 * 1024

_ultimo = 0.0


def baixar_bytes(url: str, timeout: int = 180) -> bytes:
    """Baixa uma URL respeitando a pausa mínima; levanta RuntimeError após esgotar as tentativas."""
    global _ultimo
    ultimo_erro = "sem resposta"
    for espera in (0, *ESPERAS_APOS_FALHA):
        if espera:
            time.sleep(espera)
        aguardar = PAUSA_ENTRE_REQUISICOES - (time.monotonic() - _ultimo)
        if aguardar > 0:
            time.sleep(aguardar)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                corpo = resp.read(TAMANHO_MAXIMO + 1)
            _ultimo = time.monotonic()
            if len(corpo) > TAMANHO_MAXIMO:
                raise RuntimeError("arquivo acima de 60 MB")
            if len(corpo) >= TAMANHO_MINIMO:
                return corpo
            ultimo_erro = f"resposta curta do servidor: {corpo[:120]!r}"
        except RuntimeError:
            raise
        except Exception as erro:  # noqa: BLE001
            _ultimo = time.monotonic()
            ultimo_erro = f"{type(erro).__name__}: {erro}"
    raise RuntimeError(ultimo_erro)
