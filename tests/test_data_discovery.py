"""Testes do Data Discovery com dados sintéticos (sem acesso à rede)."""

import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "discovery"))

import data_discovery as dd  # noqa: E402


def _csv(linhas: list[str]) -> bytes:
    return ("\r\n".join(linhas) + "\r\n").encode("latin-1")


def _criar_cadastro(pasta: Path) -> Path:
    caminho = pasta / "cad_cia_aberta.csv"
    caminho.write_bytes(
        _csv(
            [
                "CNPJ_CIA;DENOM_SOCIAL;DENOM_COMERC;DT_REG;SIT;CD_CVM;SETOR_ATIV;TP_MERC;CATEG_REG;SIT_EMISSOR",
                "11.111.111/0001-11;ALFA S.A.;ALFA;2000-01-01;ATIVO;001023;Bancos;BOLSA;Categoria A;FASE OPERACIONAL",
                "22.222.222/0001-22;BETA S.A.;BETA;2022-06-01;ATIVO;2000;Energia Elétrica;BALCÃO;Categoria B;FASE OPERACIONAL",
                "33.333.333/0001-33;GAMA S.A.;GAMA;1990-01-01;CANCELADA;3000;Comércio;BOLSA;Categoria A;",
                "11.111.111/0001-11;ALFA S.A.;ALFA;2000-01-01;ATIVO;001023;Bancos;BOLSA;Categoria A;FASE OPERACIONAL",
            ]
        )
    )
    return caminho


def _criar_zip(pasta: Path, tipo: str, ano: int, indice: list[str]) -> Path:
    caminho = pasta / f"{tipo}_cia_aberta_{ano}.zip"
    with zipfile.ZipFile(caminho, "w") as pacote:
        pacote.writestr(
            f"{tipo}_cia_aberta_{ano}.csv",
            _csv(["CNPJ_CIA;DT_REFER;VERSAO;DENOM_CIA;CD_CVM;CATEG_DOC;ID_DOC;DT_RECEB;LINK_DOC"] + indice),
        )
        pacote.writestr(
            f"{tipo}_cia_aberta_BPA_con_{ano}.csv",
            _csv(
                [
                    "CNPJ_CIA;DT_REFER;VERSAO;DENOM_CIA;CD_CVM;CD_CONTA;DS_CONTA;VL_CONTA",
                    f"11.111.111/0001-11;{ano}-12-31;1;ALFA S.A.;001023;1;Ativo Total;100.0",
                ]
            ),
        )
    return caminho


def test_normalizacao_de_chaves():
    assert dd.normalizar_cnpj("11.111.111/0001-11") == "11111111000111"
    assert dd.normalizar_cnpj(None) == ""
    assert dd.normalizar_cd_cvm("001023") == "1023"
    assert dd.normalizar_cd_cvm("1023") == "1023"
    assert dd.normalizar_cd_cvm("") == ""


def test_cadastro_conta_apenas_ativas_distintas(tmp_path):
    cad = dd.analisar_cadastro(_criar_cadastro(tmp_path))
    assert cad["linhas"] == 4
    assert cad["total_ativas"] == 2
    assert cad["cnpjs_ativos_repetidos"] == 1
    assert cad["situacoes"] == {"ATIVO": 3, "CANCELADA": 1}
    assert cad["por_setor"] == {"Bancos": 1, "Energia Elétrica": 1}
    assert {a["cd_cvm"] for a in cad["ativas"]} == {"1023", "2000"}


def test_zip_resume_entregas_e_reapresentacoes(tmp_path):
    caminho = _criar_zip(
        tmp_path,
        "dfp",
        2023,
        [
            "11.111.111/0001-11;2023-12-31;1;ALFA S.A.;001023;DFP;1;2024-03-01;x",
            "11.111.111/0001-11;2023-12-31;2;ALFA S.A.;001023;DFP;2;2024-05-01;x",
            "33.333.333/0001-33;2023-12-31;1;GAMA S.A.;3000;DFP;3;2024-03-01;x",
        ],
    )
    resumo = dd.analisar_zip_documentos(caminho, "dfp", 2023)
    assert resumo["indice_encontrado"]
    assert resumo["companhias"] == 2
    assert resumo["documentos_reapresentados"] == 1
    assert resumo["entregas"]["11111111000111"] == {"2023-12-31": 2}
    assert resumo["datas_referencia"] == {"2023-12-31": 2}
    assert len(resumo["membros"]) == 2


def test_cobertura_e_relatorio(tmp_path):
    cad = dd.analisar_cadastro(_criar_cadastro(tmp_path))
    dfp = {
        2022: dd.analisar_zip_documentos(
            _criar_zip(tmp_path, "dfp", 2022, ["11.111.111/0001-11;2022-12-31;1;ALFA;001023;DFP;1;x;x"]),
            "dfp",
            2022,
        ),
        2023: dd.analisar_zip_documentos(
            _criar_zip(
                tmp_path,
                "dfp",
                2023,
                [
                    "11.111.111/0001-11;2023-12-31;1;ALFA;001023;DFP;1;x;x",
                    "22.222.222/0001-22;2023-12-31;1;BETA;2000;DFP;2;x;x",
                ],
            ),
            "dfp",
            2023,
        ),
    }
    itr = {
        2024: dd.analisar_zip_documentos(
            _criar_zip(
                tmp_path,
                "itr",
                2024,
                [
                    "11.111.111/0001-11;2024-03-31;1;ALFA;001023;ITR;1;x;x",
                    "11.111.111/0001-11;2024-06-30;1;ALFA;001023;ITR;2;x;x",
                    "22.222.222/0001-22;2024-03-31;1;BETA;2000;ITR;3;x;x",
                ],
            ),
            "itr",
            2024,
        )
    }
    cob = dd.calcular_cobertura(cad["ativas"], dfp, itr)
    assert cob["ativas_com_todos_os_anos_dfp"] == 1
    assert cob["ativas_por_qtd_anos_dfp"] == {"1": 1, "2": 1}
    assert cob["ativas_por_ano_dfp"] == {2022: 1, 2023: 2}
    assert cob["ultimo_trimestre_fechado"] == "2024-06-30"
    assert cob["ativas_no_ultimo_trimestre"] == 1
    assert cob["chaves"]["cnpjs_em_documentos_ativos_no_cadastro"] == 2
    assert cob["chaves"]["cd_cvm_em_documentos_ativos_no_cadastro"] == 2

    resultado = {
        "gerado_em": "2026-01-01T00:00:00+00:00",
        "ano_inicial": 2022,
        "ano_final": 2024,
        "aquisicoes": [{"fonte": "CVM Cadastro", "url": "http://x/cad.csv", "ok": True, "bytes": 10}],
        "cadastro": cad,
        "dfp": dfp,
        "itr": itr,
        "cobertura": cob,
        "outras_fontes": [{"fonte": "BCB SGS", "recurso": "432", "ok": False, "detalhe": "erro"}],
    }
    texto = dd.gerar_relatorio(resultado)
    assert "Companhias ativas (CNPJ distinto): **2**" in texto
    assert "2024-06-30" in texto

    dd.gravar_csv_companhias(tmp_path / "saida.csv", cob["linhas"])
    linhas = (tmp_path / "saida.csv").read_text(encoding="utf-8").splitlines()
    assert len(linhas) == 3
    assert linhas[1].startswith("11111111000111;1023;ALFA S.A.")
