"""
08_collect_daily.py
Collecte pour l'étude d'événement (E14, docs/plan_extensions.md).

1. Taux à 10 ans quotidiens France et Allemagne (BCE, jeu FM, obligations de référence).
2. Pages listant les dates de publication :
   - communiqués du ministère « Situation mensuelle budgétaire » (presse.economie.gouv.fr)
   - documents DGFiP « Situation mensuelle de l'État » (economie.gouv.fr)
   Les pages HTML brutes sont enregistrées telles quelles ; l'extraction des dates se fait ensuite.

À lancer sur ton ordinateur (accès internet), depuis la racine du dépôt :
    python src/08_collect_daily.py
puis :  git add data && git commit -m "Données quotidiennes étude d'événement" && git push
"""
from io import StringIO
from pathlib import Path
import time

import pandas as pd
import requests

RAW = Path("data/raw/daily")
HTML = Path("data/raw/events_html")
RAW.mkdir(parents=True, exist_ok=True)
HTML.mkdir(parents=True, exist_ok=True)
HEADERS = {"User-Agent": "Mozilla/5.0 (memoire ECE; recherche academique)"}

ECB_KEYS = {
    "oat_10y_daily": ["FM/D.FR.EUR.FR2.BB.FR10YT_RR.YLD"],
    "bund_10y_daily": ["FM/D.DE.EUR.DE2.BB.DE10YT_RR.YLD"],
}


def ecb(key):
    url = f"https://data-api.ecb.europa.eu/service/data/{key}?format=csvdata&startPeriod=2013-01-01"
    r = requests.get(url, timeout=60, headers=HEADERS)
    r.raise_for_status()
    df = pd.read_csv(StringIO(r.text))
    s = pd.to_numeric(df["OBS_VALUE"], errors="coerce")
    s.index = pd.to_datetime(df["TIME_PERIOD"])
    return s.dropna()


def save_pages(base_url, prefix, n_pages, param="page"):
    ok = 0
    for p in range(n_pages):
        url = base_url if p == 0 else f"{base_url}{'&' if '?' in base_url else '?'}{param}={p}"
        try:
            r = requests.get(url, timeout=30, headers=HEADERS)
            if r.status_code != 200:
                print(f"  {prefix} page {p} : HTTP {r.status_code}")
                continue
            (HTML / f"{prefix}_{p:02d}.html").write_text(r.text, encoding="utf-8")
            ok += 1
        except Exception as e:
            print(f"  {prefix} page {p} : {e}")
        time.sleep(1)
    print(f"  {prefix} : {ok}/{n_pages} pages enregistrées")


if __name__ == "__main__":
    print("1. Taux quotidiens (BCE)")
    for name, keys in ECB_KEYS.items():
        for key in keys:
            try:
                s = ecb(key)
                s.rename(name).to_csv(RAW / f"{name}.csv", index_label="date")
                print(f"  OK  {name} {s.index.min().date()} -> {s.index.max().date()} ({len(s)} obs.)")
                break
            except Exception as e:
                print(f"  ÉCHEC {name} ({key}) : {e}")

    print("2. Pages des dates de publication")
    save_pages("https://www.economie.gouv.fr/dgfip/la-situation-mensuelle-de-letat", "dgfip", 12)
    save_pages("https://presse.economie.gouv.fr/?s=situation+mensuelle+budg%C3%A9taire", "presse", 20, param="paged")
    print("\nTerminé. Pousse le dossier data/ sur GitHub.")
