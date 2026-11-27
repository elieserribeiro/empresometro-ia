"""Carga do cadastro de companhias abertas: setores, companhias e mercados."""

from __future__ import annotations

import csv
import io
import re
from collections import defaultdict
from pathlib import Path

import psycopg

from .fontes import CODIFICACAO_CVM

PREFIXO_HOLDING = "Emp. Adm. Part. - "
# Nomes abreviados que a CVM usa nas holdings -> nome do setor operacional equivalente.
EQUIVALENCIAS_SETOR = {
    "const. civil, mat. const. e decoração": "Construção Civil, Mat. Constr. e Decoração",
    "máqs., equip., veíc. e peças": "Máquinas, Equipamentos, Veículos e Peças",
    "serviços médicos": "Serviços Médicos",
}


def normalizar_cnpj(valor: str | None) -> str:
    return re.sub(r"\D", "", valor or "")


def _limpo(valor: str | None) -> str | None:
    valor = (valor or "").strip()
    return valor or None


def _inteiro(valor: str | None) -> int | None:
    digitos = re.sub(r"\D", "", valor or "")
    return int(digitos) if digitos else None


def esta_ativa(situacao: str | None) -> bool:
    return (situacao or "").strip().upper().startswith("ATIVO")


def classificar_setor(nome_cvm: str) -> tuple[str, bool]:
    """Devolve (setor_base, holding) a partir do nome do setor informado pela CVM."""
    if not nome_cvm.startswith(PREFIXO_HOLDING):
        return nome_cvm, False
    base = nome_cvm[len(PREFIXO_HOLDING):].strip()
    return EQUIVALENCIAS_SETOR.get(base.lower(), base), True


def ler_cadastro(caminho: Path) -> dict[str, dict]:
    """Lê o CSV do cadastro e devolve uma entrada consolidada por CNPJ.

    Um CNPJ pode ter várias linhas (um registro por tipo de mercado, ou registros
    antigos cancelados). A linha representativa é a ativa mais recente; se não
    houver ativa, a mais recente. Os mercados são reunidos em uma lista.
    """
    grupos: dict[str, list[dict]] = defaultdict(list)
    with open(caminho, "rb") as arquivo:
        texto = io.TextIOWrapper(arquivo, encoding=CODIFICACAO_CVM, newline="")
        for linha in csv.DictReader(texto, delimiter=";"):
            cnpj = normalizar_cnpj(linha.get("CNPJ_CIA"))
            if len(cnpj) == 14:
                grupos[cnpj].append(linha)

    companhias: dict[str, dict] = {}
    for cnpj, linhas in grupos.items():
        ativas = [l for l in linhas if esta_ativa(l.get("SIT"))]
        candidatas = ativas or linhas
        principal = max(candidatas, key=lambda l: (l.get("DT_REG") or "", l.get("DT_INI_SIT") or ""))
        mercados = sorted({m for l in candidatas if (m := _limpo(l.get("TP_MERC")))})
        companhias[cnpj] = {
            "cnpj": cnpj,
            "cd_cvm": _inteiro(principal.get("CD_CVM")),
            "denominacao": _limpo(principal.get("DENOM_SOCIAL")) or cnpj,
            "nome_comercial": _limpo(principal.get("DENOM_COMERC")),
            "setor": _limpo(principal.get("SETOR_ATIV")),
            "categoria_registro": _limpo(principal.get("CATEG_REG")),
            "situacao_registro": _limpo(principal.get("SIT")),
            "situacao_emissor": _limpo(principal.get("SIT_EMISSOR")),
            "controle_acionario": _limpo(principal.get("CONTROLE_ACIONARIO")),
            "uf": (_limpo(principal.get("UF")) or "")[:2] or None,
            "municipio": _limpo(principal.get("MUN")),
            "data_registro": _limpo(principal.get("DT_REG")),
            "data_constituicao": _limpo(principal.get("DT_CONST")),
            "data_cancelamento": None if ativas else _limpo(principal.get("DT_CANCEL")),
            "ativa": bool(ativas),
            "mercados": mercados,
        }
    return companhias


def carregar_cadastro(
    conn: psycopg.Connection,
    companhias: dict[str, dict],
    cnpjs_com_documentos: set[str],
    nomes_nos_documentos: dict[str, str] | None = None,
) -> dict:
    """Grava as companhias ativas e as que têm documentos na janela.

    Companhias presentes nos documentos mas ausentes do cadastro entram com os
    dados mínimos (CNPJ e denominação) e ficam marcadas como inativas.
    """
    nomes_nos_documentos = nomes_nos_documentos or {}
    selecionadas = {
        cnpj: c for cnpj, c in companhias.items() if c["ativa"] or cnpj in cnpjs_com_documentos
    }
    fora_do_cadastro = cnpjs_com_documentos - set(companhias)
    for cnpj in fora_do_cadastro:
        selecionadas[cnpj] = {
            "cnpj": cnpj, "cd_cvm": None, "denominacao": nomes_nos_documentos.get(cnpj, cnpj),
            "nome_comercial": None, "setor": None, "categoria_registro": None,
            "situacao_registro": "FORA DO CADASTRO", "situacao_emissor": None,
            "controle_acionario": None, "uf": None, "municipio": None, "data_registro": None,
            "data_constituicao": None, "data_cancelamento": None, "ativa": False, "mercados": [],
        }

    with conn.cursor() as cur:
        setores = sorted({c["setor"] for c in selecionadas.values() if c["setor"]})
        for nome in setores:
            base, holding = classificar_setor(nome)
            cur.execute(
                """
                INSERT INTO setor (nome_cvm, setor_base, holding) VALUES (%s, %s, %s)
                ON CONFLICT (nome_cvm) DO UPDATE
                SET setor_base = EXCLUDED.setor_base, holding = EXCLUDED.holding
                """,
                (nome, base, holding),
            )
        cur.execute("SELECT nome_cvm, id FROM setor")
        id_setor = dict(cur.fetchall())

        cur.executemany(
            """
            INSERT INTO companhia (
                cnpj, cd_cvm, denominacao, nome_comercial, setor_id, categoria_registro,
                situacao_registro, situacao_emissor, controle_acionario, uf, municipio,
                data_registro, data_constituicao, data_cancelamento, ativa, atualizado_em
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())
            ON CONFLICT (cnpj) DO UPDATE SET
                cd_cvm = EXCLUDED.cd_cvm, denominacao = EXCLUDED.denominacao,
                nome_comercial = EXCLUDED.nome_comercial, setor_id = EXCLUDED.setor_id,
                categoria_registro = EXCLUDED.categoria_registro,
                situacao_registro = EXCLUDED.situacao_registro,
                situacao_emissor = EXCLUDED.situacao_emissor,
                controle_acionario = EXCLUDED.controle_acionario, uf = EXCLUDED.uf,
                municipio = EXCLUDED.municipio, data_registro = EXCLUDED.data_registro,
                data_constituicao = EXCLUDED.data_constituicao,
                data_cancelamento = EXCLUDED.data_cancelamento, ativa = EXCLUDED.ativa,
                atualizado_em = now()
            """,
            [
                (
                    c["cnpj"], c["cd_cvm"], c["denominacao"][:200], (c["nome_comercial"] or None),
                    id_setor.get(c["setor"]), c["categoria_registro"], c["situacao_registro"],
                    c["situacao_emissor"], c["controle_acionario"], c["uf"], c["municipio"],
                    c["data_registro"], c["data_constituicao"], c["data_cancelamento"], c["ativa"],
                )
                for c in selecionadas.values()
            ],
        )
        cur.execute("SELECT cnpj, id FROM companhia")
        id_companhia = dict(cur.fetchall())

        ids = [id_companhia[cnpj] for cnpj in selecionadas]
        cur.execute("DELETE FROM companhia_mercado WHERE companhia_id = ANY(%s)", (ids,))
        cur.executemany(
            "INSERT INTO companhia_mercado (companhia_id, tipo_mercado) VALUES (%s, %s)",
            [(id_companhia[c["cnpj"]], m) for c in selecionadas.values() for m in c["mercados"]],
        )

    return {
        "companhias_gravadas": len(selecionadas),
        "ativas": sum(1 for c in selecionadas.values() if c["ativa"]),
        "inativas_com_documentos": sum(1 for c in selecionadas.values() if not c["ativa"]),
        "fora_do_cadastro": len(fora_do_cadastro),
        "setores": len(setores),
    }
