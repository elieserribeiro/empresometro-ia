"""Sonda: verifica como o site da CVM entrega os documentos do IPE e do FRE.

Baixa alguns links de cada tipo para uma companhia e registra o que volta
(tipo de conteúdo, tamanho, início do arquivo e, em PDFs, se há texto extraível).
"""

from __future__ import annotations

import csv
import io
import re
import sys
import time
import urllib.request
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "discovery"))
from data_discovery import BASE_CVM, USER_AGENT, baixar  # noqa: E402

CD_CVM = "9512"  # Petrobras
ANO = 2025
csv.field_size_limit(10**9)


def obter(url: str) -> dict:
    inicio = time.monotonic()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=120) as resp:
            corpo = resp.read()
            return {
                "status": resp.status, "tipo": resp.headers.get("Content-Type"),
                "disposicao": resp.headers.get("Content-Disposition"), "bytes": len(corpo),
                "inicio": corpo[:8], "corpo": corpo, "segundos": round(time.monotonic() - inicio, 1),
                "url_final": resp.geturl(),
            }
    except Exception as erro:  # noqa: BLE001
        return {"erro": f"{type(erro).__name__}: {erro}", "segundos": round(time.monotonic() - inicio, 1)}


def texto_do_pdf(corpo: bytes) -> str:
    try:
        from pypdf import PdfReader

        leitor = PdfReader(io.BytesIO(corpo))
        texto = "\n".join((p.extract_text() or "") for p in leitor.pages[:3])
        return f"{len(leitor.pages)} páginas; primeiras 3 com {len(texto)} caracteres; amostra: {texto[:160]!r}"
    except Exception as erro:  # noqa: BLE001
        return f"falha ao ler PDF: {type(erro).__name__}: {erro}"


def main() -> int:
    bruto = Path("data/raw/documentos")
    saida = ["# Sonda dos downloads de documentos da CVM", ""]

    ipe = bruto / f"ipe_cia_aberta_{ANO}.zip"
    baixar(f"{BASE_CVM}/DOC/IPE/DADOS/ipe_cia_aberta_{ANO}.zip", ipe)
    with zipfile.ZipFile(ipe) as pacote:
        membro = pacote.infolist()[0].filename
        linhas = list(csv.DictReader(io.TextIOWrapper(pacote.open(membro), encoding="latin-1", newline=""), delimiter=";"))
    da_cia = [l for l in linhas if (l.get("Codigo_CVM") or "").lstrip("0") == CD_CVM]
    saida += [f"IPE {ANO}: {len(da_cia)} documentos da companhia {CD_CVM}.", ""]
    for categoria in ("Fato Relevante", "Comunicado ao Mercado"):
        escolhidos = [l for l in da_cia if (l.get("Categoria") or "").strip() == categoria][:1]
        saida += [f"## {categoria}", ""]
        for l in escolhidos:
            r = obter(l.get("Link_Download") or "")
            saida += [
                f"- Assunto: {(l.get('Assunto') or '')[:100]}",
                f"  - Linha do índice: " + "; ".join(f"{k}={str(v)[:60]}" for k, v in l.items() if k != "Link_Download"),
                f"  - Link: `{(l.get('Link_Download') or '')[:160]}`",
            ]
            if "erro" in r:
                saida += [f"  - ERRO: {r['erro']} ({r['segundos']}s)"]
                continue
            saida += [
                f"  - Resposta: status {r['status']}, tipo {r['tipo']}, {r['bytes']} bytes, {r['segundos']}s, "
                f"início {r['inicio']!r}, disposição {r['disposicao']}",
            ]
            if r["inicio"].startswith(b"%PDF"):
                saida += [f"  - PDF: {texto_do_pdf(r['corpo'])}"]
            time.sleep(1)
        saida += [""]

    fre = bruto / f"fre_cia_aberta_{ANO}.zip"
    baixar(f"{BASE_CVM}/DOC/FRE/DADOS/fre_cia_aberta_{ANO}.zip", fre)
    with zipfile.ZipFile(fre) as pacote:
        indice = list(
            csv.DictReader(
                io.TextIOWrapper(pacote.open(f"fre_cia_aberta_{ANO}.csv"), encoding="latin-1", newline=""), delimiter=";"
            )
        )
    da_cia = [l for l in indice if (l.get("CD_CVM") or "").lstrip("0") == CD_CVM]
    saida += ["## Formulário de Referência", "", f"{len(da_cia)} versões no índice de {ANO}.", ""]
    for l in da_cia[-1:]:
        link = l.get("LINK_DOC") or ""
        r = obter(link)
        saida += [f"- Versão {l.get('VERSAO')}, recebida em {l.get('DT_RECEB')}", f"  - Link: `{link}`"]
        if "erro" in r:
            saida += [f"  - ERRO: {r['erro']}"]
            continue
        saida += [
            f"  - Resposta: status {r['status']}, tipo {r['tipo']}, {r['bytes']} bytes, {r['segundos']}s, início {r['inicio']!r}",
            f"  - URL final: `{r['url_final'][:200]}`",
        ]
        if r["inicio"].startswith(b"PK"):
            def listar(dados: bytes, nivel: int = 0) -> None:
                with zipfile.ZipFile(io.BytesIO(dados)) as z:
                    for m in z.infolist()[:60]:
                        saida.append(f"  {'  ' * nivel}- `{m.filename}` ({m.file_size} bytes)")
                        conteudo = z.read(m) if m.file_size < 80_000_000 else b""
                        if conteudo[:2] == b"PK" and nivel < 2:
                            listar(conteudo, nivel + 1)
                        elif conteudo[:4] == b"%PDF":
                            saida.append(f"  {'  ' * (nivel + 1)}- PDF: {texto_do_pdf(conteudo)}")
                        elif m.filename.lower().endswith((".xml", ".txt", ".htm", ".html")) and conteudo:
                            trecho = conteudo[:700].decode("utf-8", errors="replace").replace("\n", " ")
                            saida.append(f"  {'  ' * (nivel + 1)}- início: {trecho!r}")
            saida.append("  - Conteúdo do pacote:")
            try:
                listar(r["corpo"])
            except Exception as erro:  # noqa: BLE001
                saida.append(f"  - falha ao abrir o pacote: {type(erro).__name__}: {erro}")
            continue
        html = r["corpo"].decode("utf-8", errors="replace")
        titulos = re.findall(r"<title>(.*?)</title>", html, flags=re.S)[:1]
        saida += [f"  - Título da página: {titulos}"]
        achados = sorted(set(re.findall(r"(frm[A-Za-z]+\.aspx[^\"'<> ]{0,120})", html)))[:25]
        saida += ["  - Referências a páginas internas:"] + [f"    - `{a}`" for a in achados]
        opcoes = re.findall(r"<option[^>]*value=\"([^\"]*)\"[^>]*>([^<]{0,80})", html)[:40]
        saida += ["  - Opções de menu encontradas:"] + [f"    - {v[:80]} => {t.strip()}" for v, t in opcoes]

    destino = Path("docs/discovery/sonda_downloads.md")
    destino.write_text("\n".join(saida), encoding="utf-8")
    print("\n".join(saida)[:3000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
