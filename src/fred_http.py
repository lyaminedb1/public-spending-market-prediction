"""
fred_http.py
Téléchargement d'une série FRED (CSV public, sans clé).

Depuis le 27/09, FRED coupe les connexions venant de la bibliothèque Python `requests`
(RemoteDisconnected / délai dépassé) alors que `curl` répond en 0,2 s.
On passe donc par `curl` en priorité, puis par `requests` avec un en-tête de navigateur standard.
"""
from io import StringIO
import subprocess
import time

import pandas as pd
import requests

URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"
BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


class SerieIntrouvable(Exception):
    pass


def _via_curl(series_id, timeout=25):
    res = subprocess.run(
        ["curl", "-s", "-L", "--max-time", str(timeout), "-w", "\n%{http_code}", URL.format(series_id)],
        capture_output=True, text=True, timeout=timeout + 5,
    )
    body, _, code = res.stdout.rpartition("\n")
    if code.strip() == "404":
        raise SerieIntrouvable(series_id)
    if res.returncode != 0 or code.strip() != "200":
        raise RuntimeError(f"curl code={code.strip()} retour={res.returncode}")
    return body


def _via_requests(series_id, timeout=25):
    r = requests.get(URL.format(series_id), timeout=timeout,
                     headers={"User-Agent": BROWSER_UA, "Accept": "text/csv,*/*"})
    if r.status_code == 404:
        raise SerieIntrouvable(series_id)
    r.raise_for_status()
    return r.text


def fred_csv(series_id, tries=2):
    """Renvoie la série FRED (pd.Series, index date) ; lève une exception si introuvable."""
    last = None
    for attempt in range(tries):
        for method in (_via_curl, _via_requests):
            try:
                text = method(series_id)
                df = pd.read_csv(StringIO(text))
                if series_id not in df.columns:
                    raise SerieIntrouvable(series_id)  # page HTML au lieu du CSV
                s = pd.to_numeric(df[series_id], errors="coerce")
                s.index = pd.to_datetime(df[df.columns[0]])
                return s.dropna()
            except SerieIntrouvable:
                raise
            except Exception as e:
                last = e
        time.sleep(3)
    raise last
