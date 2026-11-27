"""Linha de comando do ETL.

Exemplos:
    python -m empresometro.etl carregar
    python -m empresometro.etl carregar --tipos dfp --anos 2025
    python -m empresometro.etl macro
    python -m empresometro.etl qualidade
    python -m empresometro.etl indicadores
    python -m empresometro.etl relatorio --saida docs/etl/relatorio_carga.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
import time
from pathlib import Path

from .cadastro import carregar_cadastro, ler_cadastro
from .documentos import carregar_documentos, ler_indice
from .fontes import (
    URL_CADASTRO, baixar, conectar, descrever_local, ja_carregado, registrar_carga, url_documentos,
)
from .ifdata import carregar_ifdata, gerar_relatorio_ifdata
from .macro import ANO_INICIAL_PADRAO as ANO_INICIAL_MACRO
from .macro import carregar_macro, gerar_relatorio_macro
from .qualidade import gerar_alertas, gerar_relatorio_qualidade
from .relatorio import gerar_relatorio
from ..indicadores.carga import calcular_tudo
from ..indicadores.relatorio import gerar_catalogo_markdown, gerar_relatorio_indicadores

ANO_INICIAL_PADRAO = 2021


def executar_carga(
    conn, pasta_bruta: Path, tipos: list[str], anos: list[int], usar_local: bool = False,
    forcar: bool = False, registrar=print,
) -> list[dict]:
    """Baixa (ou reaproveita) os arquivos, carrega o cadastro e depois os documentos."""
    eventos: list[dict] = []

    def obter(url: str, destino: Path) -> dict:
        if usar_local and destino.exists():
            return descrever_local(url, destino)
        registrar(f"Baixando {destino.name}...")
        return baixar(url, destino)

    cadastro_info = obter(URL_CADASTRO, pasta_bruta / "cad_cia_aberta.csv")
    if not cadastro_info["ok"]:
        raise RuntimeError(f"Não foi possível obter o cadastro: {cadastro_info.get('erro')}")

    arquivos = []
    for tipo in tipos:
        for ano in anos:
            destino = pasta_bruta / f"{tipo.lower()}_cia_aberta_{ano}.zip"
            info = obter(url_documentos(tipo, ano), destino)
            if info["ok"]:
                arquivos.append((tipo.upper(), ano, info))
            else:
                eventos.append({"arquivo": destino.name, "situacao": f"não obtido ({info.get('erro')})"})

    # As companhias com documentos na janela entram no banco mesmo que estejam inativas.
    cnpjs_com_documentos: set[str] = set()
    nomes: dict[str, str] = {}
    for tipo, ano, info in arquivos:
        for reg in ler_indice(info["caminho"], tipo, ano):
            cnpjs_com_documentos.add(reg["cnpj"])
            if reg["denominacao"]:
                nomes[reg["cnpj"]] = reg["denominacao"]

    inicio = time.monotonic()
    with conn.transaction():
        carga_id = registrar_carga(conn, "CVM Cadastro", cadastro_info)
        companhias = ler_cadastro(cadastro_info["caminho"])
        resumo = carregar_cadastro(conn, companhias, cnpjs_com_documentos, nomes)
        conn.execute("UPDATE carga_arquivo SET linhas = %s WHERE id = %s", (len(companhias), carga_id))
    registrar(f"Cadastro: {resumo}")
    eventos.append(
        {"arquivo": "cad_cia_aberta.csv", "situacao": "carregado",
         "documentos": resumo["companhias_gravadas"], "segundos": round(time.monotonic() - inicio, 1)}
    )

    for tipo, ano, info in arquivos:
        nome = Path(info["caminho"]).name
        if not forcar and ja_carregado(conn, info["url"], info["sha256"]):
            registrar(f"{nome}: sem mudança desde a última carga, pulando.")
            eventos.append({"arquivo": nome, "situacao": "sem mudança"})
            continue
        registrar(f"Carregando {nome}...")
        inicio = time.monotonic()
        resumo = carregar_documentos(conn, info["caminho"], tipo, ano, info)
        segundos = round(time.monotonic() - inicio, 1)
        registrar(f"{nome}: {resumo['documentos']} documentos, {resumo['linhas']} linhas em {segundos}s")
        eventos.append({"arquivo": nome, "situacao": "carregado", "segundos": segundos, **resumo})
    return eventos


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="empresometro.etl", description="ETL do Empresômetro IA")
    comandos = parser.add_subparsers(dest="comando", required=True)

    carregar = comandos.add_parser("carregar", help="baixa os arquivos da CVM e carrega o banco")
    carregar.add_argument("--bruto", type=Path, default=Path("data/raw/cvm"))
    carregar.add_argument("--tipos", nargs="+", default=["dfp", "itr"], choices=["dfp", "itr"])
    carregar.add_argument("--anos", nargs="+", type=int)
    carregar.add_argument("--ano-inicial", type=int, default=ANO_INICIAL_PADRAO)
    carregar.add_argument("--ano-final", type=int, default=dt.date.today().year)
    carregar.add_argument("--usar-local", action="store_true", help="reaproveita arquivos já baixados")
    carregar.add_argument("--forcar", action="store_true", help="recarrega mesmo sem mudança no arquivo")
    carregar.add_argument("--saida", type=Path, help="grava o relatório de carga neste arquivo")
    carregar.add_argument("--sem-macro", action="store_true", help="não carrega as séries macroeconômicas")
    carregar.add_argument("--sem-qualidade", action="store_true", help="não roda as validações de qualidade")
    carregar.add_argument("--sem-indicadores", action="store_true", help="não calcula os indicadores")
    carregar.add_argument("--sem-ifdata", action="store_true", help="não carrega o IF.data do Banco Central")

    ifdata = comandos.add_parser("ifdata", help="carrega os índices dos bancos do IF.data do Banco Central")
    ifdata.add_argument("--ano-inicial", type=int, default=ANO_INICIAL_PADRAO)
    ifdata.add_argument("--saida", type=Path, default=Path("docs/etl/relatorio_ifdata.md"))

    indicadores = comandos.add_parser("indicadores", help="calcula os indicadores financeiros")
    indicadores.add_argument("--saida", type=Path, default=Path("docs/indicadores/relatorio_indicadores.md"))

    macro = comandos.add_parser("macro", help="carrega as séries do Banco Central e do IBGE")
    macro.add_argument("--ano-inicial", type=int, default=ANO_INICIAL_MACRO)
    macro.add_argument("--saida", type=Path, default=Path("docs/etl/relatorio_macro.md"))

    qualidade = comandos.add_parser("qualidade", help="roda as validações e gera os alertas de qualidade")
    qualidade.add_argument("--saida", type=Path, default=Path("docs/etl/relatorio_qualidade.md"))

    relatorio = comandos.add_parser("relatorio", help="gera o relatório de conferência do banco")
    relatorio.add_argument("--saida", type=Path)

    args = parser.parse_args(argv)
    conn = conectar()
    conn.autocommit = True
    def gravar(caminho: Path, texto: str) -> None:
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text(texto, encoding="utf-8")
        print(f"Relatório gravado em {caminho}")

    def rodar_macro(caminho: Path, ano_inicial: int = ANO_INICIAL_MACRO) -> None:
        print("Carregando as séries macroeconômicas...")
        gravar(caminho, gerar_relatorio_macro(conn, carregar_macro(conn, ano_inicial)))

    def rodar_qualidade(caminho: Path) -> None:
        print("Rodando as validações de qualidade (pode levar alguns minutos)...")
        print(f"Alertas: {gerar_alertas(conn)}")
        gravar(caminho, gerar_relatorio_qualidade(conn))

    def rodar_ifdata(caminho: Path, ano_inicial: int = ANO_INICIAL_PADRAO) -> None:
        print("Carregando o IF.data do Banco Central (alguns minutos)...")
        try:
            carregar_ifdata(conn, ano_inicial)
        except RuntimeError as erro:  # a fonte fora do ar não deve interromper o restante
            print(f"IF.data não carregado: {erro}")
            return
        gravar(caminho, gerar_relatorio_ifdata(conn))

    def rodar_indicadores(caminho: Path) -> None:
        calcular_tudo(conn)
        gravar(caminho, gerar_relatorio_indicadores(conn))
        gravar(caminho.parent / "catalogo.md", gerar_catalogo_markdown())

    try:
        if args.comando == "indicadores":
            rodar_indicadores(args.saida)
        elif args.comando == "ifdata":
            rodar_ifdata(args.saida, args.ano_inicial)
        elif args.comando == "macro":
            rodar_macro(args.saida, args.ano_inicial)
        elif args.comando == "qualidade":
            rodar_qualidade(args.saida)
        elif args.comando == "relatorio":
            texto = gerar_relatorio(conn)
            gravar(args.saida, texto) if args.saida else print(texto)
        else:
            anos = args.anos or list(range(args.ano_inicial, args.ano_final + 1))
            eventos = executar_carga(conn, args.bruto, args.tipos, anos, args.usar_local, args.forcar)
            pasta = args.saida.parent if args.saida else Path("docs/etl")
            if args.saida:
                gravar(args.saida, gerar_relatorio(conn, eventos))
            if not args.sem_macro:
                rodar_macro(pasta / "relatorio_macro.md")
            if not args.sem_qualidade:
                rodar_qualidade(pasta / "relatorio_qualidade.md")
            if not args.sem_ifdata:
                rodar_ifdata(pasta / "relatorio_ifdata.md", args.ano_inicial)
            if not args.sem_indicadores:
                rodar_indicadores(pasta.parent / "indicadores" / "relatorio_indicadores.md")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
