import logging, os, re, json
from urllib.parse import urljoin, urlparse

import azure.functions as func
import requests
from bs4 import BeautifulSoup
from azure.storage.blob import BlobServiceClient

ANP_URL = ("https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/"
           "precos/precos-revenda-e-de-distribuicao-combustiveis/serie-historica-do-levantamento-de-precos")

CONTAINER = "landingzone"           # nome do container
DEST_PREFIX = "raw/anp/"             # subpasta dentro do container

# ───────────────────────── helpers ──────────────────────────
def discover_links() -> list[str]:
    """Retorna todos os links ‘mensal-municipios*.xls*’."""
    soup = BeautifulSoup(requests.get(ANP_URL, timeout=30).text, "html.parser")
    pat = re.compile(r"(mensal-?municipios.*|semanal-municipio-202[2-5]).*\.(xlsb?|xlsx?)$", re.I)
    links = {urljoin(ANP_URL, a["href"]) for a in soup.find_all("a", href=True) if pat.search(a["href"])}
    if not links:
        raise RuntimeError("Nenhum link encontrado – verifique o HTML da página.")
    return sorted(links)

def upload_to_blob(svc: BlobServiceClient, url: str) -> None:
    """Baixa `url` e envia para o Blob (apenas se ainda não existir)."""
    filename = os.path.basename(urlparse(url).path)
    blob_path = f"{DEST_PREFIX}{filename}"
    blob = svc.get_blob_client(container=CONTAINER, blob=blob_path)

    data = requests.get(url, timeout=120).content

    logging.info("↓ Baixando %s", filename)
    resp = requests.get(url, timeout=120)
    resp.raise_for_status()

    logging.info("↑ Enviando para %s", blob_path)
    blob.upload_blob(resp.content, overwrite=True)

    return {"file": filename, "status": "uploaded", "size_bytes": len(data)}

# ───────────────────────── Function entry point ──────────────────────────
def _run_task() -> list[dict]:
    """Executa o fluxo de download e upload retornando o resumo."""
    svc = BlobServiceClient.from_connection_string(os.environ["BLOB_CONN_STR"])
    return [upload_to_blob(svc, link) for link in discover_links()]


def main(timer: func.TimerRequest) -> None:
    try:
        results = _run_task()
        logging.info("Timer execution completed. Files uploaded: %d", len(results))
    except Exception as exc:
        logging.exception("Falha na execução da função Timer")
        raise