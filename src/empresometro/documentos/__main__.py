"""Linha de comando da camada documental.

Exemplos:
    python -m empresometro.documentos coletar
    python -m empresometro.documentos coletar --fontes ipe --anos 2025 --limite 20
    python -m empresometro.documentos exportar-trechos
    python -m empresometro.documentos importar-embeddings --arquivo data/embeddings/embeddings.npz
    python -m empresometro.documentos relatorio
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

from ..etl.fontes import conectar
from .coleta import Progresso, coletar_fre, coletar_ipe, coletar_pareceres, ler_piloto
from .embeddings import MODELO_PADRAO, criar_indice, exportar_trechos, importar_embeddings, situacao
from .relatorio import gerar_relatorio_coleta


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="empresometro.documentos", description="Coleta de documentos")
    comandos = parser.add_subparsers(dest="comando", required=True)
    coletar = comandos.add_parser("coletar", help="baixa, extrai e segmenta os documentos do piloto")
    coletar.add_argument("--companhias", type=Path, default=Path("docs/documentos/piloto.csv"))
    coletar.add_argument("--fontes", nargs="+", default=["parecer", "ipe", "fre"], choices=["parecer", "ipe", "fre"])
    coletar.add_argument("--anos", nargs="+", type=int)
    coletar.add_argument("--ano-inicial", type=int, default=2021)
    coletar.add_argument("--ano-final", type=int, default=dt.date.today().year)
    coletar.add_argument("--limite", type=int, help="máximo de itens por fonte e ano (para testes)")
    coletar.add_argument("--bruto", type=Path, default=Path("data/raw/documentos"))
    coletar.add_argument("--saida", type=Path, default=Path("docs/documentos/relatorio_coleta.md"))
    exportar = comandos.add_parser("exportar-trechos", help="grava os trechos sem vetor para o Colab")
    exportar.add_argument("--saida", type=Path, default=Path("data/embeddings/trechos.csv.gz"))
    exportar.add_argument("--todos", action="store_true", help="exporta também os trechos que já têm vetor")
    importar = comandos.add_parser("importar-embeddings", help="carrega os vetores gerados no Colab")
    importar.add_argument("--arquivo", type=Path, default=Path("data/embeddings/embeddings.npz"))
    importar.add_argument("--modelo", default=MODELO_PADRAO)
    importar.add_argument("--sem-indice", action="store_true", help="não cria o índice de vizinhança")
    relatorio = comandos.add_parser("relatorio", help="gera o relatório da coleta")
    relatorio.add_argument("--saida", type=Path, default=Path("docs/documentos/relatorio_coleta.md"))
    args = parser.parse_args(argv)

    conn = conectar()
    conn.autocommit = True
    try:
        eventos = None
        if args.comando == "exportar-trechos":
            total = exportar_trechos(conn, args.saida, somente_pendentes=not args.todos)
            megabytes = args.saida.stat().st_size / 1e6
            print(f"{total} trechos exportados para {args.saida} ({megabytes:.1f} MB)")
            return 0
        if args.comando == "importar-embeddings":
            print(f"Importando vetores de {args.arquivo}...")
            print(f"Resultado: {importar_embeddings(conn, args.arquivo, args.modelo)}")
            if not args.sem_indice:
                print("Criando o índice de vizinhança (pode levar alguns minutos)...")
                criar_indice(conn)
            print(f"Situação: {situacao(conn)}")
            return 0
        if args.comando == "coletar":
            piloto = ler_piloto(args.companhias)
            anos = args.anos or list(range(args.ano_inicial, args.ano_final + 1))
            progresso = Progresso()
            print(f"Coletando documentos de {len(piloto)} companhias, anos {anos[0]} a {anos[-1]}.")
            if "parecer" in args.fontes:
                coletar_pareceres(conn, piloto, anos, progresso, args.limite)
            if "ipe" in args.fontes:
                coletar_ipe(conn, piloto, anos, args.bruto, progresso, args.limite)
            if "fre" in args.fontes:
                coletar_fre(conn, piloto, anos, args.bruto, progresso, args.limite)
            eventos = progresso.eventos
            print(f"Coleta concluída: {len(eventos)} itens processados nesta execução.")
        args.saida.parent.mkdir(parents=True, exist_ok=True)
        args.saida.write_text(gerar_relatorio_coleta(conn, eventos), encoding="utf-8")
        print(f"Relatório gravado em {args.saida}")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
