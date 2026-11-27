"""Data Discovery do Empresômetro IA (Fase 1).

Inventaria as fontes públicas do projeto e mede a cobertura real:

- CVM: cadastro de companhias abertas, DFP (anual) e ITR (trimestral);
- CVM: disponibilidade dos arquivos de FRE e IPE;
- Banco Central (SGS) e IBGE (SIDRA): teste de acesso às APIs.

Janela: de 2021 até o último trimestre fechado do ano corrente.

Usa somente a biblioteca padrão do Python. Os arquivos brutos ficam em uma
pasta temporária (não versionada); o relatório é gravado em docs/discovery/.

Uso:
    python scripts/discovery/data_discovery.py
    python scripts/discovery/data_discovery.py --ano-inicial 2021 --saida docs/discovery
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import re
import sys
import time
import urllib.error
import urllib.request
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

BASE_CVM = "https://dados.cvm.gov.br/dados/CIA_ABERTA"
URL_CADASTRO = f"{BASE_CVM}/CAD/DADOS/cad_cia_aberta.csv"
ANO_INICIAL_PADRAO = 2021
CODIFICACAO_CVM = "latin-1"
USER_AGENT = "empresometro-ia-data-discovery/1.0 (+https://github.com/elieserribeiro/empresometro-ia)"

# Séries usadas apenas para testar o acesso às APIs macroeconômicas.
SERIES_SGS = {432: "Meta Selic", 433: "IPCA mensal", 1: "Dólar comercial (venda)"}
URL_SIDRA_TESTE = "https://apisidra.ibge.gov.br/values/t/1737/n1/all/v/2266/p/last%201"

csv.field_size_limit(10**9)


# --------------------------------------------------------------------------
# Normalização de chaves
# --------------------------------------------------------------------------

def normalizar_cnpj(valor: str | None) -> str:
    """Mantém somente os dígitos do CNPJ."""
    return re.sub(r"\D", "", valor or "")


def normalizar_cd_cvm(valor: str | None) -> str:
    """Remove zeros à esquerda e caracteres não numéricos do código CVM."""
    digitos = re.sub(r"\D", "", valor or "")
    return digitos.lstrip("0") or ("0" if digitos else "")


# --------------------------------------------------------------------------
# Rede
# --------------------------------------------------------------------------

def baixar(url: str, destino: Path, tentativas: int = 3, timeout: int = 180) -> dict:
    """Baixa uma URL para um arquivo e devolve os metadados da aquisição."""
    info: dict = {"url": url, "ok": False}
    for tentativa in range(1, tentativas + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                sha = hashlib.sha256()
                tamanho = 0
                destino.parent.mkdir(parents=True, exist_ok=True)
                with open(destino, "wb") as arquivo:
                    while bloco := resp.read(1 << 20):
                        arquivo.write(bloco)
                        sha.update(bloco)
                        tamanho += len(bloco)
                info.update(
                    ok=True,
                    status=resp.status,
                    bytes=tamanho,
                    sha256=sha.hexdigest(),
                    last_modified=resp.headers.get("Last-Modified"),
                    baixado_em=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                )
                return info
        except urllib.error.HTTPError as erro:
            info.update(status=erro.code, erro=f"HTTP {erro.code}")
            if erro.code == 404:
                return info
        except Exception as erro:  # noqa: BLE001 - o relatório registra qualquer falha
            info.update(erro=f"{type(erro).__name__}: {erro}")
        if tentativa < tentativas:
            time.sleep(5 * tentativa)
    return info


def consultar_json(url: str, timeout: int = 60) -> dict:
    """Consulta uma API JSON e devolve um resumo (sem levantar exceção)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            dados = json.loads(resp.read().decode("utf-8"))
        amostra = dados[-1] if isinstance(dados, list) and dados else dados
        return {"url": url, "ok": True, "amostra": amostra}
    except Exception as erro:  # noqa: BLE001
        return {"url": url, "ok": False, "erro": f"{type(erro).__name__}: {erro}"}


# --------------------------------------------------------------------------
# Análise do cadastro
# --------------------------------------------------------------------------

def ler_csv_cvm(fluxo_binario) -> csv.DictReader:
    texto = io.TextIOWrapper(fluxo_binario, encoding=CODIFICACAO_CVM, newline="")
    return csv.DictReader(texto, delimiter=";")


def esta_ativa(situacao: str | None) -> bool:
    return (situacao or "").strip().upper().startswith("ATIVO")


def analisar_cadastro(caminho: Path) -> dict:
    """Resume o cadastro de companhias abertas e lista as companhias ativas."""
    with open(caminho, "rb") as arquivo:
        leitor = ler_csv_cvm(arquivo)
        colunas = leitor.fieldnames or []
        linhas = list(leitor)

    situacoes = Counter((l.get("SIT") or "").strip() or "(vazio)" for l in linhas)
    ativas_por_cnpj: dict[str, dict] = {}
    cnpjs_repetidos = 0
    for linha in linhas:
        if not esta_ativa(linha.get("SIT")):
            continue
        cnpj = normalizar_cnpj(linha.get("CNPJ_CIA"))
        if not cnpj:
            continue
        if cnpj in ativas_por_cnpj:
            cnpjs_repetidos += 1
            continue
        ativas_por_cnpj[cnpj] = {
            "cnpj": cnpj,
            "cd_cvm": normalizar_cd_cvm(linha.get("CD_CVM")),
            "denominacao": (linha.get("DENOM_SOCIAL") or "").strip(),
            "nome_comercial": (linha.get("DENOM_COMERC") or "").strip(),
            "setor": (linha.get("SETOR_ATIV") or "").strip(),
            "tipo_mercado": (linha.get("TP_MERC") or "").strip(),
            "categoria_registro": (linha.get("CATEG_REG") or "").strip(),
            "situacao_emissor": (linha.get("SIT_EMISSOR") or "").strip(),
            "data_registro": (linha.get("DT_REG") or "").strip(),
        }

    ativas = list(ativas_por_cnpj.values())

    def distribuicao(campo: str) -> dict:
        return dict(Counter(a[campo] or "(vazio)" for a in ativas).most_common())

    return {
        "colunas": colunas,
        "linhas": len(linhas),
        "situacoes": dict(situacoes.most_common()),
        "ativas": ativas,
        "total_ativas": len(ativas),
        "cnpjs_ativos_repetidos": cnpjs_repetidos,
        "por_setor": distribuicao("setor"),
        "por_tipo_mercado": distribuicao("tipo_mercado"),
        "por_categoria_registro": distribuicao("categoria_registro"),
        "por_situacao_emissor": distribuicao("situacao_emissor"),
    }


# --------------------------------------------------------------------------
# Análise dos arquivos DFP / ITR
# --------------------------------------------------------------------------

def analisar_zip_documentos(caminho: Path, tipo: str, ano: int) -> dict:
    """Resume um ZIP anual de DFP ou ITR.

    Devolve os arquivos internos (linhas e colunas) e, a partir do arquivo
    índice, as entregas por companhia: {cnpj: {data_referencia: maior_versao}}.
    """
    nome_indice = f"{tipo}_cia_aberta_{ano}.csv"
    membros = []
    entregas: dict[str, dict[str, int]] = defaultdict(dict)
    cd_cvm_por_cnpj: dict[str, str] = {}
    colunas_indice: list[str] = []
    indice_encontrado = False

    with zipfile.ZipFile(caminho) as pacote:
        for membro in pacote.infolist():
            if membro.is_dir():
                continue
            with pacote.open(membro) as fluxo:
                leitor = ler_csv_cvm(fluxo)
                colunas = leitor.fieldnames or []
                total = 0
                eh_indice = membro.filename.lower() == nome_indice
                if eh_indice:
                    indice_encontrado = True
                    colunas_indice = colunas
                for linha in leitor:
                    total += 1
                    if not eh_indice:
                        continue
                    cnpj = normalizar_cnpj(linha.get("CNPJ_CIA"))
                    data = (linha.get("DT_REFER") or "").strip()
                    if not cnpj or not data:
                        continue
                    try:
                        versao = int((linha.get("VERSAO") or "1").strip() or 1)
                    except ValueError:
                        versao = 1
                    entregas[cnpj][data] = max(versao, entregas[cnpj].get(data, 0))
                    cd_cvm_por_cnpj[cnpj] = normalizar_cd_cvm(linha.get("CD_CVM"))
            membros.append(
                {
                    "arquivo": membro.filename,
                    "linhas": total,
                    "bytes": membro.file_size,
                    "colunas": colunas,
                }
            )

    datas = Counter(data for por_data in entregas.values() for data in por_data)
    reapresentacoes = sum(1 for por_data in entregas.values() for v in por_data.values() if v > 1)
    return {
        "tipo": tipo,
        "ano": ano,
        "indice_encontrado": indice_encontrado,
        "colunas_indice": colunas_indice,
        "membros": membros,
        "linhas_totais": sum(m["linhas"] for m in membros),
        "companhias": len(entregas),
        "datas_referencia": dict(sorted(datas.items())),
        "documentos_reapresentados": reapresentacoes,
        "entregas": {cnpj: dict(sorted(d.items())) for cnpj, d in entregas.items()},
        "cd_cvm_por_cnpj": cd_cvm_por_cnpj,
    }


# --------------------------------------------------------------------------
# Cobertura
# --------------------------------------------------------------------------

def calcular_cobertura(ativas: list[dict], dfp: dict[int, dict], itr: dict[int, dict]) -> dict:
    """Cruza as companhias ativas com as entregas de DFP e ITR."""
    anos_dfp = sorted(dfp)
    anos_itr = sorted(itr)
    cnpjs_ativos = {a["cnpj"] for a in ativas}
    cd_cvm_ativos = {a["cd_cvm"] for a in ativas if a["cd_cvm"]}

    linhas = []
    for cia in ativas:
        cnpj = cia["cnpj"]
        anos_com_dfp = [ano for ano in anos_dfp if cnpj in dfp[ano]["entregas"]]
        trimestres = sorted(
            data for ano in anos_itr for data in itr[ano]["entregas"].get(cnpj, {})
        )
        linhas.append(
            {
                **cia,
                "anos_com_dfp": anos_com_dfp,
                "qtd_anos_dfp": len(anos_com_dfp),
                "qtd_itr": len(trimestres),
                "ultimo_itr": trimestres[-1] if trimestres else "",
            }
        )

    por_qtd_anos = Counter(l["qtd_anos_dfp"] for l in linhas)
    ativas_por_ano_dfp = {
        ano: sum(1 for l in linhas if ano in l["anos_com_dfp"]) for ano in anos_dfp
    }

    # Qualidade das chaves de integração entre documentos e cadastro.
    cnpjs_doc: set[str] = set()
    cds_doc: set[str] = set()
    for resumo in list(dfp.values()) + list(itr.values()):
        cnpjs_doc.update(resumo["entregas"])
        cds_doc.update(c for c in resumo["cd_cvm_por_cnpj"].values() if c)

    ultimo_ano_itr = max(anos_itr) if anos_itr else None
    datas_ultimo_ano = itr[ultimo_ano_itr]["datas_referencia"] if ultimo_ano_itr else {}
    ultimo_trimestre = max(datas_ultimo_ano) if datas_ultimo_ano else None
    ativas_no_ultimo_trimestre = (
        sum(
            1
            for cnpj in cnpjs_ativos
            if ultimo_trimestre in itr[ultimo_ano_itr]["entregas"].get(cnpj, {})
        )
        if ultimo_trimestre
        else 0
    )

    return {
        "anos_dfp": anos_dfp,
        "anos_itr": anos_itr,
        "linhas": linhas,
        "ativas_por_qtd_anos_dfp": {str(k): por_qtd_anos[k] for k in sorted(por_qtd_anos)},
        "ativas_por_ano_dfp": ativas_por_ano_dfp,
        "ativas_com_todos_os_anos_dfp": por_qtd_anos.get(len(anos_dfp), 0) if anos_dfp else 0,
        "ativas_sem_nenhuma_dfp": por_qtd_anos.get(0, 0),
        "ativas_sem_nenhum_itr": sum(1 for l in linhas if l["qtd_itr"] == 0),
        "chaves": {
            "cnpjs_em_documentos": len(cnpjs_doc),
            "cnpjs_em_documentos_ativos_no_cadastro": len(cnpjs_doc & cnpjs_ativos),
            "cd_cvm_em_documentos": len(cds_doc),
            "cd_cvm_em_documentos_ativos_no_cadastro": len(cds_doc & cd_cvm_ativos),
        },
        "ultimo_ano_itr": ultimo_ano_itr,
        "ultimo_trimestre_fechado": ultimo_trimestre,
        "datas_itr_ultimo_ano": datas_ultimo_ano,
        "ativas_no_ultimo_trimestre": ativas_no_ultimo_trimestre,
    }


# --------------------------------------------------------------------------
# Relatório
# --------------------------------------------------------------------------

def _mb(qtd_bytes: int | None) -> str:
    return f"{(qtd_bytes or 0) / 1e6:.1f} MB"


def _tabela(cabecalho: list[str], linhas: list[list]) -> str:
    saida = ["| " + " | ".join(cabecalho) + " |", "|" + "---|" * len(cabecalho)]
    saida += ["| " + " | ".join(str(c) for c in linha) + " |" for linha in linhas]
    return "\n".join(saida)


def gerar_relatorio(resultado: dict) -> str:
    cad = resultado["cadastro"]
    cob = resultado["cobertura"]
    partes = [
        "# Data Discovery — Relatório de cobertura",
        "",
        f"Gerado em {resultado['gerado_em']} (UTC). "
        f"Janela: {resultado['ano_inicial']} até o último trimestre fechado de {resultado['ano_final']}.",
        "",
        "Todos os números abaixo são contagens reais dos arquivos baixados nesta execução.",
        "",
        "## 1. Aquisição dos arquivos",
        "",
        _tabela(
            ["Fonte", "Arquivo", "Situação", "Tamanho", "Última modificação"],
            [
                [
                    a["fonte"],
                    a["url"].rsplit("/", 1)[-1],
                    "OK" if a["ok"] else f"FALHOU ({a.get('erro', 'sem detalhe')})",
                    _mb(a.get("bytes")),
                    a.get("last_modified") or "-",
                ]
                for a in resultado["aquisicoes"]
            ],
        ),
        "",
    ]

    if cad:
        partes += [
            "## 2. Cadastro de companhias abertas",
            "",
            f"- Linhas no cadastro: **{cad['linhas']}**",
            f"- Companhias ativas (CNPJ distinto): **{cad['total_ativas']}**",
            f"- Linhas ativas com CNPJ repetido (ignoradas): {cad['cnpjs_ativos_repetidos']}",
            "",
            "### Situação do registro",
            "",
            _tabela(["Situação", "Linhas"], [[k, v] for k, v in cad["situacoes"].items()]),
            "",
            "### Companhias ativas por tipo de mercado",
            "",
            _tabela(["Tipo de mercado", "Companhias"], [[k, v] for k, v in cad["por_tipo_mercado"].items()]),
            "",
            "### Companhias ativas por categoria de registro",
            "",
            _tabela(["Categoria", "Companhias"], [[k, v] for k, v in cad["por_categoria_registro"].items()]),
            "",
            "### Companhias ativas por setor de atividade",
            "",
            _tabela(["Setor", "Companhias"], [[k, v] for k, v in cad["por_setor"].items()]),
            "",
            "Colunas do cadastro: " + ", ".join(f"`{c}`" for c in cad["colunas"]),
            "",
        ]

    for titulo, chave in (("3. DFP — demonstrações anuais", "dfp"), ("4. ITR — informações trimestrais", "itr")):
        resumos = resultado[chave]
        partes += [f"## {titulo}", ""]
        if not resumos:
            partes += ["Nenhum arquivo analisado.", ""]
            continue
        partes += [
            _tabela(
                ["Ano", "Companhias", "Arquivos no ZIP", "Linhas totais", "Reapresentações", "Datas de referência"],
                [
                    [
                        ano,
                        r["companhias"],
                        len(r["membros"]),
                        r["linhas_totais"],
                        r["documentos_reapresentados"],
                        ", ".join(f"{d} ({n})" for d, n in r["datas_referencia"].items()) or "-",
                    ]
                    for ano, r in sorted(resumos.items())
                ],
            ),
            "",
        ]
        ultimo = resumos[max(resumos)]
        partes += [
            f"### Arquivos internos do ZIP de {ultimo['ano']}",
            "",
            _tabela(
                ["Arquivo", "Linhas", "Tamanho"],
                [[m["arquivo"], m["linhas"], _mb(m["bytes"])] for m in ultimo["membros"]],
            ),
            "",
            "Colunas do arquivo índice: " + ", ".join(f"`{c}`" for c in ultimo["colunas_indice"]),
            "",
        ]
        demonstracao = next((m for m in ultimo["membros"] if "_BPA_con_" in m["arquivo"]), None)
        if demonstracao:
            partes += [
                "Colunas das demonstrações (exemplo BPA consolidado): "
                + ", ".join(f"`{c}`" for c in demonstracao["colunas"]),
                "",
            ]

    if cob:
        total = len(cob["linhas"])
        partes += [
            "## 5. Cobertura das companhias ativas",
            "",
            f"- Companhias ativas avaliadas: **{total}**",
            f"- Com DFP em todos os {len(cob['anos_dfp'])} exercícios ({cob['anos_dfp'][0]}–{cob['anos_dfp'][-1]}): "
            f"**{cob['ativas_com_todos_os_anos_dfp']}**"
            if cob["anos_dfp"]
            else "- Sem exercícios de DFP analisados",
            f"- Sem nenhuma DFP na janela: {cob['ativas_sem_nenhuma_dfp']}",
            f"- Sem nenhum ITR na janela: {cob['ativas_sem_nenhum_itr']}",
            f"- Último trimestre fechado encontrado: **{cob['ultimo_trimestre_fechado'] or '-'}** "
            f"({cob['ativas_no_ultimo_trimestre']} companhias ativas já entregaram)",
            "",
            "### Companhias ativas por quantidade de exercícios com DFP",
            "",
            _tabela(["Exercícios com DFP", "Companhias"], [[k, v] for k, v in cob["ativas_por_qtd_anos_dfp"].items()]),
            "",
            "### Companhias ativas com DFP por exercício",
            "",
            _tabela(["Exercício", "Companhias ativas com DFP"], [[k, v] for k, v in cob["ativas_por_ano_dfp"].items()]),
            "",
            f"### Entregas de ITR em {cob['ultimo_ano_itr']}",
            "",
            _tabela(["Data de referência", "Companhias"], [[k, v] for k, v in cob["datas_itr_ultimo_ano"].items()]),
            "",
            "### Chaves de integração",
            "",
            _tabela(
                ["Chave", "Distintos nos documentos", "Encontrados entre as ativas do cadastro"],
                [
                    ["CNPJ", cob["chaves"]["cnpjs_em_documentos"], cob["chaves"]["cnpjs_em_documentos_ativos_no_cadastro"]],
                    ["Código CVM", cob["chaves"]["cd_cvm_em_documentos"], cob["chaves"]["cd_cvm_em_documentos_ativos_no_cadastro"]],
                ],
            ),
            "",
            "Os documentos também incluem companhias que hoje não estão ativas; por isso o total "
            "nos documentos pode superar o total de ativas.",
            "",
        ]

    partes += [
        "## 6. Outras fontes",
        "",
        _tabela(
            ["Fonte", "Recurso", "Situação", "Detalhe"],
            [
                [
                    o["fonte"],
                    o["recurso"],
                    "OK" if o["ok"] else "FALHOU",
                    o.get("detalhe", "-"),
                ]
                for o in resultado["outras_fontes"]
            ],
        ),
        "",
        "## 7. Arquivos gerados",
        "",
        "- `relatorio_cobertura.md`: este relatório.",
        "- `cobertura.json`: os mesmos números em formato estruturado.",
        "- `companhias_ativas.csv`: uma linha por companhia ativa, com a cobertura de DFP e ITR.",
        "",
    ]
    return "\n".join(partes)


def gravar_csv_companhias(caminho: Path, linhas: list[dict]) -> None:
    campos = [
        "cnpj", "cd_cvm", "denominacao", "nome_comercial", "setor", "tipo_mercado",
        "categoria_registro", "situacao_emissor", "data_registro",
        "qtd_anos_dfp", "anos_com_dfp", "qtd_itr", "ultimo_itr",
    ]
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos, delimiter=";")
        escritor.writeheader()
        for linha in sorted(linhas, key=lambda l: l["denominacao"]):
            registro = {c: linha.get(c, "") for c in campos}
            registro["anos_com_dfp"] = " ".join(str(a) for a in linha["anos_com_dfp"])
            escritor.writerow(registro)


# --------------------------------------------------------------------------
# Execução
# --------------------------------------------------------------------------

def executar(ano_inicial: int, ano_final: int, pasta_bruta: Path, pasta_saida: Path) -> dict:
    aquisicoes: list[dict] = []
    outras: list[dict] = []

    print("Baixando cadastro de companhias abertas...")
    caminho_cad = pasta_bruta / "cad_cia_aberta.csv"
    info = baixar(URL_CADASTRO, caminho_cad)
    aquisicoes.append({"fonte": "CVM Cadastro", **info})
    cadastro = analisar_cadastro(caminho_cad) if info["ok"] else None

    documentos: dict[str, dict[int, dict]] = {"dfp": {}, "itr": {}}
    for tipo in ("dfp", "itr"):
        for ano in range(ano_inicial, ano_final + 1):
            url = f"{BASE_CVM}/DOC/{tipo.upper()}/DADOS/{tipo}_cia_aberta_{ano}.zip"
            destino = pasta_bruta / f"{tipo}_cia_aberta_{ano}.zip"
            print(f"Baixando {tipo.upper()} {ano}...")
            info = baixar(url, destino)
            aquisicoes.append({"fonte": f"CVM {tipo.upper()} {ano}", **info})
            if not info["ok"]:
                continue
            try:
                documentos[tipo][ano] = analisar_zip_documentos(destino, tipo, ano)
            except Exception as erro:  # noqa: BLE001
                aquisicoes[-1].update(ok=False, erro=f"Falha na leitura: {type(erro).__name__}: {erro}")

    # FRE e IPE: nesta fase só medimos disponibilidade e volume dos arquivos.
    for tipo in ("fre", "ipe"):
        for ano in range(ano_inicial, ano_final + 1):
            url = f"{BASE_CVM}/DOC/{tipo.upper()}/DADOS/{tipo}_cia_aberta_{ano}.zip"
            destino = pasta_bruta / f"{tipo}_cia_aberta_{ano}.zip"
            print(f"Baixando {tipo.upper()} {ano}...")
            info = baixar(url, destino)
            detalhe = "-"
            if info["ok"]:
                try:
                    with zipfile.ZipFile(destino) as pacote:
                        qtd = len([m for m in pacote.infolist() if not m.is_dir()])
                    detalhe = f"{_mb(info['bytes'])}, {qtd} arquivos internos"
                except zipfile.BadZipFile:
                    info["ok"] = False
                    detalhe = "arquivo ZIP inválido"
            else:
                detalhe = info.get("erro", "-")
            outras.append({"fonte": f"CVM {tipo.upper()}", "recurso": f"{ano}", "ok": info["ok"], "detalhe": detalhe})
            destino.unlink(missing_ok=True)

    for codigo, nome in SERIES_SGS.items():
        resposta = consultar_json(
            f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados/ultimos/1?formato=json"
        )
        detalhe = json.dumps(resposta.get("amostra"), ensure_ascii=False) if resposta["ok"] else resposta["erro"]
        outras.append({"fonte": "BCB SGS", "recurso": f"{codigo} — {nome}", "ok": resposta["ok"], "detalhe": detalhe})

    resposta = consultar_json(URL_SIDRA_TESTE)
    if resposta["ok"] and isinstance(resposta["amostra"], dict):
        amostra = resposta["amostra"]
        detalhe = f"{amostra.get('D3N', '')}: {amostra.get('V', '')}".strip(": ") or "resposta recebida"
    else:
        detalhe = resposta.get("erro", "resposta recebida")
    outras.append({"fonte": "IBGE SIDRA", "recurso": "Tabela 1737 (IPCA)", "ok": resposta["ok"], "detalhe": detalhe})

    cobertura = None
    if cadastro and (documentos["dfp"] or documentos["itr"]):
        dfp_completos = {ano: r for ano, r in documentos["dfp"].items() if ano < ano_final}
        cobertura = calcular_cobertura(cadastro["ativas"], dfp_completos, documentos["itr"])

    resultado = {
        "gerado_em": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "ano_inicial": ano_inicial,
        "ano_final": ano_final,
        "aquisicoes": aquisicoes,
        "cadastro": cadastro,
        "dfp": documentos["dfp"],
        "itr": documentos["itr"],
        "cobertura": cobertura,
        "outras_fontes": outras,
    }

    pasta_saida.mkdir(parents=True, exist_ok=True)
    (pasta_saida / "relatorio_cobertura.md").write_text(gerar_relatorio(resultado), encoding="utf-8")

    # O JSON guarda os resumos; os detalhes por companhia ficam no CSV.
    enxuto = json.loads(json.dumps(resultado, default=str))
    if enxuto["cadastro"]:
        enxuto["cadastro"].pop("ativas", None)
    for tipo in ("dfp", "itr"):
        for resumo in enxuto[tipo].values():
            resumo.pop("entregas", None)
            resumo.pop("cd_cvm_por_cnpj", None)
    if enxuto["cobertura"]:
        enxuto["cobertura"].pop("linhas", None)
    (pasta_saida / "cobertura.json").write_text(
        json.dumps(enxuto, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    if cobertura:
        gravar_csv_companhias(pasta_saida / "companhias_ativas.csv", cobertura["linhas"])
    return resultado


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Data Discovery do Empresômetro IA")
    parser.add_argument("--ano-inicial", type=int, default=ANO_INICIAL_PADRAO)
    parser.add_argument("--ano-final", type=int, default=dt.date.today().year)
    parser.add_argument("--bruto", type=Path, default=Path("data/raw/discovery"))
    parser.add_argument("--saida", type=Path, default=Path("docs/discovery"))
    args = parser.parse_args(argv)

    resultado = executar(args.ano_inicial, args.ano_final, args.bruto, args.saida)
    falhas = [a for a in resultado["aquisicoes"] if not a["ok"]]
    print(f"Relatório gravado em {args.saida}/relatorio_cobertura.md")
    if resultado["cadastro"]:
        print(f"Companhias ativas: {resultado['cadastro']['total_ativas']}")
    if falhas:
        print(f"Atenção: {len(falhas)} arquivo(s) não foram obtidos; veja o relatório.")
    # Falha a execução somente se o cadastro (base de tudo) não foi obtido.
    return 0 if resultado["cadastro"] else 1


if __name__ == "__main__":
    sys.exit(main())
