"""
09_collect_panel.py
Collecte pour l'extension E15 (panel européen trimestriel, docs/plan_extensions.md).

1. Taux à 10 ans mensuels (OCDE via FRED) : France, Allemagne, Italie, Espagne, Portugal, Belgique.
2. Comptes trimestriels non financiers des administrations publiques (Eurostat gov_10q_ggnfa).

À lancer sur ton ordinateur, depuis la racine du dépôt :
    python src/09_collect_panel.py
puis :  git add data && git commit -m "Données panel européen" && git push
"""
from itertools import product
import json
from pathlib import Path

import pandas as pd
import requests

from fred_http import fred_csv

OUT = Path("data/raw/panel")
OUT.mkdir(parents=True, exist_ok=True)
HEADERS = {"User-Agent": "Mozilla/5.0 (memoire ECE; recherche academique)"}

COUNTRIES = {"FR": "France", "DE": "Allemagne", "IT": "Italie", "ES": "Espagne", "PT": "Portugal", "BE": "Belgique"}
NA_ITEMS = ["TE", "D1PAY", "D41PAY", "P51G", "D62PAY", "P2", "TR", "B9"]


def fred(series_id):
    return fred_csv(series_id)


def eurostat_jsonstat():
    params = [("format", "JSON"), ("lang", "EN"), ("unit", "MIO_EUR"), ("s_adj", "NSA"), ("sector", "S13")]
    params += [("na_item", x) for x in NA_ITEMS] + [("geo", g) for g in COUNTRIES]
    url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/gov_10q_ggnfa"
    r = requests.get(url, params=params, timeout=120, headers=HEADERS)
    r.raise_for_status()
    js = r.json()
    (OUT / "eurostat_gov_10q_ggnfa_raw.json").write_text(json.dumps(js), encoding="utf-8")
    ids, sizes = js["id"], js["size"]
    cats = []
    for d in ids:
        idx = js["dimension"][d]["category"]["index"]
        cats.append(sorted(idx, key=idx.get))
    values = js["value"]
    rows = []
    for flat, combo in enumerate(product(*cats)):
        v = values.get(str(flat)) if isinstance(values, dict) else values[flat]
        if v is not None:
            rows.append(dict(zip(ids, combo), valeur=v))
    df = pd.DataFrame(rows)
    return df[["geo", "na_item", "time", "valeur"]]


if __name__ == "__main__":
    print("1. Taux à 10 ans (FRED / OCDE)")
    rates = {}
    for code in COUNTRIES:
        sid = f"IRLTLT01{code}M156N"
        try:
            rates[code] = fred(sid)
            print(f"  OK  {code} {rates[code].index.min().date()} -> {rates[code].index.max().date()}")
        except Exception as e:
            print(f"  ÉCHEC {code} ({sid}) : {e}")
    pd.DataFrame(rates).to_csv(OUT / "taux_10y_mensuels.csv", index_label="date")

    print("2. Eurostat gov_10q_ggnfa")
    if (OUT / "eurostat_gov_10q_ggnfa.csv").exists():
        print("  déjà téléchargé, on garde le fichier existant")
        raise SystemExit("\nTerminé. Pousse le dossier data/ sur GitHub.")
    try:
        df = eurostat_jsonstat()
        df.to_csv(OUT / "eurostat_gov_10q_ggnfa.csv", index=False)
        print(f"  OK  {len(df)} valeurs ; périodes {df.time.min()} -> {df.time.max()}")
        print(df.groupby(["geo", "na_item"]).size().unstack().to_string())
    except Exception as e:
        print(f"  ÉCHEC Eurostat : {e}")
    print("\nTerminé. Pousse le dossier data/ sur GitHub.")
