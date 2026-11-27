"""Carga das demonstrações DFP e ITR: documentos, linhas, composição do capital e pareceres."""

from __future__ import annotations

import csv
import io
import re
import zipfile
from decimal import Decimal, InvalidOperation
from pathlib import Path

import psycopg

from .cadastro import normalizar_cnpj
from .fontes import CODIFICACAO_CVM, registrar_carga

csv.field_size_limit(10**9)

DEMONSTRACOES = ("BPA", "BPP", "DRE", "DRA", "DFC_MD", "DFC_MI", "DMPL", "DVA")
PADRAO_DEMONSTRACAO = re.compile(
    r"^(dfp|itr)_cia_aberta_(" + "|".join(DEMONSTRACOES) + r")_(con|ind)_(\d{4})\.csv$", re.I
)
ORDEM_EXERCICIO = {"ÚLTIMO": "ULTIMO", "ULTIMO": "ULTIMO", "PENÚLTIMO": "PENULTIMO", "PENULTIMO": "PENULTIMO"}
FATOR_ESCALA = {"UNIDADE": Decimal(1), "MIL": Decimal(1000)}
MIL = Decimal(1000)

COLUNAS_LINHA = (
    "ano_referencia", "documento_id", "demonstracao", "escopo", "ordem_exercicio", "dt_inicio",
    "dt_fim", "coluna_df", "cd_conta", "ds_conta", "valor_original", "escala", "moeda",
    "valor_reais", "conta_fixa", "sequencia",
)


def _ler(pacote: zipfile.ZipFile, membro: str) -> csv.DictReader:
    texto = io.TextIOWrapper(pacote.open(membro), encoding=CODIFICACAO_CVM, newline="")
    return csv.DictReader(texto, delimiter=";")


def _texto(valor: str | None) -> str | None:
    valor = (valor or "").strip()
    return valor or None


def _inteiro(valor: str | None) -> int | None:
    valor = (valor or "").strip()
    try:
        return int(Decimal(valor)) if valor else None
    except (InvalidOperation, ValueError):
        return None


def _decimal(valor: str | None) -> Decimal | None:
    valor = (valor or "").strip()
    if not valor:
        return None
    try:
        return Decimal(valor)
    except InvalidOperation:
        return None


def nome_do_indice(tipo: str, ano: int) -> str:
    return f"{tipo.lower()}_cia_aberta_{ano}.csv"


def ler_indice(caminho_zip: Path, tipo: str, ano: int) -> list[dict]:
    """Lê o arquivo índice do ZIP: um registro por (CNPJ, data de referência, versão)."""
    registros: dict[tuple, dict] = {}
    with zipfile.ZipFile(caminho_zip) as pacote:
        for linha in _ler(pacote, nome_do_indice(tipo, ano)):
            cnpj = normalizar_cnpj(linha.get("CNPJ_CIA"))
            data = _texto(linha.get("DT_REFER"))
            versao = _inteiro(linha.get("VERSAO")) or 1
            if len(cnpj) != 14 or not data:
                continue
            registros[(cnpj, data, versao)] = {
                "cnpj": cnpj,
                "dt_referencia": data,
                "versao": versao,
                "denominacao": _texto(linha.get("DENOM_CIA")),
                "id_doc_cvm": _inteiro(linha.get("ID_DOC")),
                "dt_recebimento": _texto(linha.get("DT_RECEB")),
                "link": _texto(linha.get("LINK_DOC")),
            }
    return list(registros.values())


def carregar_documentos(
    conn: psycopg.Connection, caminho_zip: Path, tipo: str, ano: int, info_arquivo: dict
) -> dict:
    """Carrega um ZIP anual de DFP ou ITR, substituindo a carga anterior do mesmo tipo e ano.

    Tudo acontece em uma única transação: se algo falhar, o banco fica como estava.
    """
    tipo = tipo.upper()
    resumo = {
        "tipo": tipo, "ano": ano, "documentos": 0, "linhas": 0, "linhas_orfas": 0,
        "linhas_escala_desconhecida": 0, "composicao": 0, "pareceres": 0, "por_demonstracao": {},
    }
    indice = ler_indice(caminho_zip, tipo, ano)

    with conn.transaction(), conn.cursor() as cur:
        carga_id = registrar_carga(conn, f"CVM {tipo}", info_arquivo)

        # Remove a carga anterior deste tipo e ano (as linhas primeiro, pela partição).
        cur.execute(
            """
            DELETE FROM demonstracao_linha
            WHERE ano_referencia = %s
              AND documento_id IN (
                  SELECT id FROM documento
                  WHERE tipo = %s AND dt_referencia >= make_date(%s, 1, 1)
                    AND dt_referencia < make_date(%s, 1, 1))
            """,
            (ano, tipo, ano, ano + 1),
        )
        cur.execute(
            "DELETE FROM documento WHERE tipo = %s AND dt_referencia >= make_date(%s, 1, 1) "
            "AND dt_referencia < make_date(%s, 1, 1)",
            (tipo, ano, ano + 1),
        )

        cur.execute("SELECT cnpj, id FROM companhia")
        id_companhia = dict(cur.fetchall())

        # A versão vigente é a de maior número para cada companhia e data de referência.
        maior_versao: dict[tuple, int] = {}
        for reg in indice:
            chave = (reg["cnpj"], reg["dt_referencia"])
            maior_versao[chave] = max(reg["versao"], maior_versao.get(chave, 0))

        with cur.copy(
            "COPY documento (companhia_id, tipo, dt_referencia, versao, vigente, id_doc_cvm, "
            "dt_recebimento, link, carga_id) FROM STDIN"
        ) as copia:
            for reg in indice:
                companhia_id = id_companhia.get(reg["cnpj"])
                if companhia_id is None:
                    continue
                copia.write_row(
                    (
                        companhia_id, tipo, reg["dt_referencia"], reg["versao"],
                        reg["versao"] == maior_versao[(reg["cnpj"], reg["dt_referencia"])],
                        reg["id_doc_cvm"], reg["dt_recebimento"], reg["link"], carga_id,
                    )
                )
                resumo["documentos"] += 1

        cur.execute(
            """
            SELECT c.cnpj, d.dt_referencia::text, d.versao, d.id
            FROM documento d JOIN companhia c ON c.id = d.companhia_id
            WHERE d.carga_id = %s
            """,
            (carga_id,),
        )
        id_documento = {(cnpj, data, versao): doc for cnpj, data, versao, doc in cur.fetchall()}

        with zipfile.ZipFile(caminho_zip) as pacote:
            membros = [m.filename for m in pacote.infolist() if not m.is_dir()]

            for membro in membros:
                casamento = PADRAO_DEMONSTRACAO.match(Path(membro).name)
                if not casamento:
                    continue
                demonstracao = casamento.group(2).upper()
                escopo = casamento.group(3).upper()
                gravadas = 0
                with cur.copy(
                    f"COPY demonstracao_linha ({', '.join(COLUNAS_LINHA)}) FROM STDIN"
                ) as copia:
                    for sequencia, linha in enumerate(_ler(pacote, membro), start=1):
                        data = (linha.get("DT_REFER") or "").strip()
                        chave = (
                            normalizar_cnpj(linha.get("CNPJ_CIA")), data,
                            _inteiro(linha.get("VERSAO")) or 1,
                        )
                        documento_id = id_documento.get(chave)
                        if documento_id is None:
                            resumo["linhas_orfas"] += 1
                            continue
                        escala = (linha.get("ESCALA_MOEDA") or "").strip().upper()
                        valor = _decimal(linha.get("VL_CONTA"))
                        fator = FATOR_ESCALA.get(escala)
                        if fator is None:
                            resumo["linhas_escala_desconhecida"] += 1
                            escala, fator = "UNIDADE", Decimal(1)
                        fixa = (linha.get("ST_CONTA_FIXA") or "").strip().upper()
                        copia.write_row(
                            (
                                int(data[:4]), documento_id, demonstracao, escopo,
                                ORDEM_EXERCICIO.get((linha.get("ORDEM_EXERC") or "").strip().upper(), "ULTIMO"),
                                _texto(linha.get("DT_INI_EXERC")),
                                _texto(linha.get("DT_FIM_EXERC")) or data,
                                _texto(linha.get("COLUNA_DF")),
                                (linha.get("CD_CONTA") or "").strip()[:20],
                                (linha.get("DS_CONTA") or "").strip()[:200],
                                valor, escala, (linha.get("MOEDA") or "REAL").strip()[:10] or "REAL",
                                None if valor is None else (valor * fator).quantize(Decimal("0.01")),
                                {"S": True, "N": False}.get(fixa), sequencia,
                            )
                        )
                        gravadas += 1
                resumo["por_demonstracao"][f"{demonstracao}_{escopo}"] = gravadas
                resumo["linhas"] += gravadas

            # Composição do capital: uma linha por documento.
            nome_capital = f"{tipo.lower()}_cia_aberta_composicao_capital_{ano}.csv"
            if nome_capital in membros:
                capital: dict[int, tuple] = {}
                for linha in _ler(pacote, nome_capital):
                    chave = (
                        normalizar_cnpj(linha.get("CNPJ_CIA")), (linha.get("DT_REFER") or "").strip(),
                        _inteiro(linha.get("VERSAO")) or 1,
                    )
                    documento_id = id_documento.get(chave)
                    if documento_id is None:
                        continue
                    capital[documento_id] = (
                        documento_id,
                        _inteiro(linha.get("QT_ACAO_ORDIN_CAP_INTEGR")),
                        _inteiro(linha.get("QT_ACAO_PREF_CAP_INTEGR")),
                        _inteiro(linha.get("QT_ACAO_TOTAL_CAP_INTEGR")),
                        _inteiro(linha.get("QT_ACAO_ORDIN_TESOURO")),
                        _inteiro(linha.get("QT_ACAO_PREF_TESOURO")),
                        _inteiro(linha.get("QT_ACAO_TOTAL_TESOURO")),
                    )
                with cur.copy(
                    "COPY composicao_capital (documento_id, acoes_ordinarias, acoes_preferenciais, "
                    "acoes_total, tesouraria_ordinarias, tesouraria_preferenciais, tesouraria_total) "
                    "FROM STDIN"
                ) as copia:
                    for registro in capital.values():
                        copia.write_row(registro)
                resumo["composicao"] = len(capital)

            # Pareceres e declarações.
            nome_parecer = f"{tipo.lower()}_cia_aberta_parecer_{ano}.csv"
            if nome_parecer in membros:
                with cur.copy(
                    "COPY parecer (documento_id, tipo_relatorio, tipo_parecer, item, texto) FROM STDIN"
                ) as copia:
                    for linha in _ler(pacote, nome_parecer):
                        chave = (
                            normalizar_cnpj(linha.get("CNPJ_CIA")),
                            (linha.get("DT_REFER") or "").strip(),
                            _inteiro(linha.get("VERSAO")) or 1,
                        )
                        documento_id = id_documento.get(chave)
                        if documento_id is None:
                            continue
                        copia.write_row(
                            (
                                documento_id,
                                (_texto(linha.get("TP_RELAT_AUD")) or "")[:40] or None,
                                (_texto(linha.get("TP_PARECER_DECL")) or "")[:200] or None,
                                _inteiro(linha.get("NUM_ITEM_PARECER_DECL")),
                                (_texto(linha.get("TXT_PARECER_DECL")) or "").replace("\x00", "") or None,
                            )
                        )
                        resumo["pareceres"] += 1

        cur.execute(
            "UPDATE carga_arquivo SET linhas = %s WHERE id = %s", (resumo["linhas"], carga_id)
        )
    return resumo
