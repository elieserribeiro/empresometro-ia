"""Coleta dos documentos das companhias do piloto: IPE, FRE e pareceres de auditoria."""

from __future__ import annotations

import base64
import csv
import io
import re
import time
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import psycopg

from ..etl.fontes import BASE_CVM, baixar
from .armazenamento import gravar_documento, ja_coletado
from .rede import baixar_bytes
from .texto import limpar

csv.field_size_limit(10**9)
CATEGORIAS_IPE = ("Fato Relevante", "Comunicado ao Mercado")

# Nomes legíveis para os grupos de seções do Formulário de Referência.
GRUPOS_FRE = {
    "AtividadesEmissor": "1. Atividades do emissor",
    "ComentariosDiretores": "2. Comentários dos diretores",
    "Projecoes": "3. Projeções",
    "FatoresRisco": "4. Fatores de risco",
    "PoliticaGerenciamentoRiscosEControleInterno": "5. Gerenciamento de riscos e controles internos",
    "ControleGrupoEconomico": "6. Controle e grupo econômico",
    "AssembleiaGeralEAdm": "7. Assembleia geral e administração",
    "RemuneracaoAdministradores": "8. Remuneração dos administradores",
    "Auditores": "9. Auditores",
    "RecursosHumanos": "10. Recursos humanos",
    "TransacoesPartesRelacionadas": "11. Transações com partes relacionadas",
    "CapitalSocialValoresMobiliarios": "12. Capital social e valores mobiliários",
}


def so_digitos(valor: str | None) -> str:
    return re.sub(r"\D", "", valor or "")


def ler_piloto(caminho: Path) -> list[dict]:
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        return [
            {"cnpj": so_digitos(l["cnpj"]), "denominacao": l.get("denominacao", "")}
            for l in csv.DictReader(arquivo, delimiter=";")
        ]


def _ids_das_companhias(conn: psycopg.Connection, piloto: list[dict]) -> dict[str, int]:
    cnpjs = [p["cnpj"] for p in piloto]
    return dict(conn.execute("SELECT cnpj, id FROM companhia WHERE cnpj = ANY(%s)", (cnpjs,)).fetchall())


def _ler_csv_do_zip(caminho: Path, membro: str | None = None) -> list[dict]:
    with zipfile.ZipFile(caminho) as pacote:
        nome = membro or next(m.filename for m in pacote.infolist() if not m.is_dir())
        texto = io.TextIOWrapper(pacote.open(nome), encoding="latin-1", newline="")
        return list(csv.DictReader(texto, delimiter=";"))


def _obter_indice(tipo: str, ano: int, pasta: Path) -> Path | None:
    destino = pasta / f"{tipo}_cia_aberta_{ano}.zip"
    info = baixar(f"{BASE_CVM}/DOC/{tipo.upper()}/DADOS/{tipo}_cia_aberta_{ano}.zip", destino)
    return destino if info["ok"] else None


class Progresso:
    """Acompanha a coleta e registra tempos, para estimar o esforço do piloto completo."""

    def __init__(self, registrar=print):
        self.registrar = registrar
        self.eventos: list[dict] = []

    def anotar(self, fonte: str, resumo: dict, segundos: float, titulo: str) -> None:
        self.eventos.append({"fonte": fonte, "segundos": segundos, **resumo})
        if len(self.eventos) % 25 == 0:
            self.registrar(f"  {len(self.eventos)} documentos processados (último: {titulo[:60]})")


# --------------------------------------------------------------------------
# IPE: fatos relevantes e comunicados ao mercado
# --------------------------------------------------------------------------

def selecionar_ipe(linhas: list[dict], cnpjs: set[str]) -> list[dict]:
    """Filtra o índice do IPE pelas companhias e categorias, mantendo a última versão de cada protocolo."""
    escolhidos: dict[tuple, dict] = {}
    for linha in linhas:
        cnpj = so_digitos(linha.get("CNPJ_Companhia"))
        categoria = (linha.get("Categoria") or "").strip()
        link = (linha.get("Link_Download") or "").strip()
        if cnpj not in cnpjs or categoria not in CATEGORIAS_IPE or not link:
            continue
        protocolo = (linha.get("Protocolo_Entrega") or "").strip() or link
        try:
            versao = int((linha.get("Versao") or "1").strip() or 1)
        except ValueError:
            versao = 1
        registro = {
            "cnpj": cnpj, "categoria": categoria, "tipo": (linha.get("Tipo") or "").strip(),
            "assunto": (linha.get("Assunto") or "").strip(), "link": link, "versao": versao,
            "protocolo": protocolo, "dt_referencia": (linha.get("Data_Referencia") or "").strip() or None,
            "dt_entrega": (linha.get("Data_Entrega") or "").strip()[:10] or None,
        }
        chave = (cnpj, protocolo)
        if chave not in escolhidos or versao > escolhidos[chave]["versao"]:
            escolhidos[chave] = registro
    return list(escolhidos.values())


def coletar_ipe(conn, piloto, anos, pasta: Path, progresso: Progresso, limite: int | None = None) -> None:
    ids = _ids_das_companhias(conn, piloto)
    for ano in anos:
        indice = _obter_indice("ipe", ano, pasta)
        if indice is None:
            progresso.registrar(f"IPE {ano}: índice não obtido.")
            continue
        selecionados = selecionar_ipe(_ler_csv_do_zip(indice), set(ids))
        if limite:
            selecionados = selecionados[:limite]
        progresso.registrar(f"IPE {ano}: {len(selecionados)} documentos a verificar.")
        for doc in selecionados:
            chave = f"{doc['protocolo']}:{doc['versao']}"
            if ja_coletado(conn, "IPE", chave):
                continue
            inicio = time.monotonic()
            pdf, erro = None, None
            try:
                pdf = baixar_bytes(doc["link"])
                if not pdf.startswith(b"%PDF"):
                    pdf, erro = None, "O arquivo entregue não é um PDF."
            except RuntimeError as falha:
                erro = str(falha)
            titulo = doc["assunto"] or doc["tipo"] or doc["categoria"]
            resumo = gravar_documento(
                conn, companhia_id=ids[doc["cnpj"]], fonte="IPE", chave=chave, titulo=titulo, pdf=pdf, erro=erro,
                categoria=doc["categoria"], tipo=doc["tipo"], dt_referencia=doc["dt_referencia"],
                dt_entrega=doc["dt_entrega"], versao=doc["versao"], link=doc["link"],
            )
            progresso.anotar("IPE", resumo, round(time.monotonic() - inicio, 1), titulo)


# --------------------------------------------------------------------------
# FRE: seções narrativas do Formulário de Referência
# --------------------------------------------------------------------------

def nome_da_secao(grupo: str, item: str) -> str:
    legivel = re.sub(r"(?<=[a-zà-ú])(?=[A-Z])", " ", item).strip().capitalize()
    return f"{GRUPOS_FRE.get(grupo, grupo)} / {legivel}"


def extrair_secoes_fre(xml: bytes) -> list[dict]:
    """Extrai as seções do XML do FRE cujo conteúdo é um PDF embutido em base64."""
    try:
        xml.decode("utf-8")
    except UnicodeDecodeError:  # o arquivo declara UTF-8, mas vem em Windows-1252
        xml = xml.decode("cp1252", errors="replace").encode("utf-8")
    secoes: list[dict] = []
    pilha: list[str] = []
    for evento, elem in ET.iterparse(io.BytesIO(xml), events=("start", "end")):
        if evento == "start":
            pilha.append(elem.tag)
            continue
        if elem.tag == "ImagemObjetoArquivoPdf" and elem.text and len(pilha) >= 3:
            conteudo = elem.text.strip()
            if conteudo.startswith("JVBERi0"):
                grupo, item = pilha[-3], pilha[-2]
                try:
                    secoes.append({"grupo": grupo, "item": item, "pdf": base64.b64decode(conteudo)})
                except ValueError:
                    pass
            elem.text = None
        pilha.pop()
    return secoes


def selecionar_fre(linhas: list[dict], cnpjs: set[str]) -> list[dict]:
    """Do índice do FRE, a última versão de cada companhia e data de referência."""
    escolhidos: dict[tuple, dict] = {}
    for linha in linhas:
        cnpj = so_digitos(linha.get("CNPJ_CIA"))
        link = (linha.get("LINK_DOC") or "").strip()
        if cnpj not in cnpjs or not link:
            continue
        try:
            versao = int((linha.get("VERSAO") or "1").strip() or 1)
        except ValueError:
            versao = 1
        chave = (cnpj, (linha.get("DT_REFER") or "").strip())
        if chave not in escolhidos or versao > escolhidos[chave]["versao"]:
            escolhidos[chave] = {
                "cnpj": cnpj, "dt_referencia": chave[1] or None, "versao": versao, "link": link,
                "id_doc": (linha.get("ID_DOC") or "").strip(), "dt_entrega": (linha.get("DT_RECEB") or "").strip()[:10] or None,
            }
    return list(escolhidos.values())


def coletar_fre(conn, piloto, anos, pasta: Path, progresso: Progresso, limite: int | None = None) -> None:
    ids = _ids_das_companhias(conn, piloto)
    for ano in anos:
        indice = _obter_indice("fre", ano, pasta)
        if indice is None:
            progresso.registrar(f"FRE {ano}: índice não obtido.")
            continue
        formularios = selecionar_fre(_ler_csv_do_zip(indice, f"fre_cia_aberta_{ano}.csv"), set(ids))
        if limite:
            formularios = formularios[:limite]
        progresso.registrar(f"FRE {ano}: {len(formularios)} formulários a verificar.")
        for fre in formularios:
            marca = f"{fre['id_doc']}:v{fre['versao']}"
            if ja_coletado(conn, "FRE", f"{marca}:_pacote"):
                continue
            inicio = time.monotonic()
            comuns = dict(
                companhia_id=ids[fre["cnpj"]], fonte="FRE", categoria="Formulário de Referência",
                dt_referencia=fre["dt_referencia"], dt_entrega=fre["dt_entrega"], versao=fre["versao"], link=fre["link"],
            )
            try:
                pacote = baixar_bytes(fre["link"], timeout=300)
                with zipfile.ZipFile(io.BytesIO(pacote)) as z:
                    maior = max((m for m in z.infolist() if m.filename.lower().endswith(".xml")), key=lambda m: m.file_size)
                    secoes = extrair_secoes_fre(z.read(maior))
            except Exception as falha:  # noqa: BLE001
                resumo = gravar_documento(
                    conn, chave=f"{marca}:_pacote", titulo=f"Formulário de Referência {ano}",
                    erro=f"{type(falha).__name__}: {falha}", **comuns,
                )
                progresso.anotar("FRE", resumo, round(time.monotonic() - inicio, 1), "pacote com erro")
                continue
            for secao in secoes:
                titulo = nome_da_secao(secao["grupo"], secao["item"])
                resumo = gravar_documento(
                    conn, chave=f"{marca}:{secao['grupo']}/{secao['item']}", titulo=titulo, pdf=secao["pdf"],
                    secao=f"{secao['grupo']}/{secao['item']}"[:200], tipo=GRUPOS_FRE.get(secao["grupo"], secao["grupo"]),
                    **comuns,
                )
                progresso.anotar("FRE", resumo, 0.0, titulo)
            # Marca o pacote como concluído, para a coleta poder ser retomada.
            gravar_documento(
                conn, chave=f"{marca}:_pacote", titulo=f"Formulário de Referência {ano}: {len(secoes)} seções",
                paginas=[], **comuns,
            )
            progresso.eventos.append(
                {"fonte": "FRE_PACOTE", "segundos": round(time.monotonic() - inicio, 1), "trechos": 0, "paginas": 0,
                 "caracteres": 0, "situacao": "OK"}
            )


# --------------------------------------------------------------------------
# Pareceres de auditoria (já carregados no banco pelo ETL)
# --------------------------------------------------------------------------

def coletar_pareceres(conn, piloto, anos, progresso: Progresso, limite: int | None = None) -> None:
    ids = _ids_das_companhias(conn, piloto)
    linhas = conn.execute(
        """
        SELECT p.id, d.companhia_id, d.tipo, d.dt_referencia, d.dt_recebimento, d.versao, d.link,
               p.tipo_relatorio, p.tipo_parecer, p.texto
        FROM parecer p JOIN documento d ON d.id = p.documento_id AND d.vigente
        WHERE d.companhia_id = ANY(%s) AND extract(year FROM d.dt_referencia) = ANY(%s)
          AND p.texto IS NOT NULL AND length(p.texto) > 200
        ORDER BY p.id
        """,
        (list(ids.values()), list(anos)),
    ).fetchall()
    if limite:
        linhas = linhas[:limite]
    progresso.registrar(f"Pareceres: {len(linhas)} textos a verificar.")
    for parecer_id, companhia_id, tipo_doc, referencia, recebimento, versao, link, relatorio, tipo, texto in linhas:
        chave = f"parecer:{parecer_id}"
        if ja_coletado(conn, "PARECER", chave):
            continue
        titulo = f"{tipo or 'Parecer'} ({tipo_doc} de {referencia})"
        resumo = gravar_documento(
            conn, companhia_id=companhia_id, fonte="PARECER", chave=chave, titulo=titulo, paginas=[limpar(texto)],
            categoria="Parecer ou declaração", tipo=(relatorio or tipo), dt_referencia=referencia,
            dt_entrega=recebimento, versao=versao, link=link,
        )
        progresso.anotar("PARECER", resumo, 0.0, titulo)
