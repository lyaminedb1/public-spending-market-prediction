"""
01_collect_data.py
Collecte automatique des données de marché et de contrôle pour le mémoire
« Prédiction d'indicateurs des marchés financiers à partir des données de dépenses publiques ouvertes ».

À lancer depuis la racine du dépôt :
    pip install pandas requests yfinance
    python src/01_collect_data.py

Les fichiers bruts sont enregistrés dans data/raw/.
Les données budgétaires (data.economie.gouv.fr) sont téléchargées à la main
et déposées dans data/raw/budget/ (voir README).
"""

from io import StringIO
from pathlib import Path

import pandas as pd
import requests

RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

START = "2010-01-01"  # un peu avant 2013 pour pouvoir calculer retards et variations sur un an

# ---------------------------------------------------------------------------
# 1. FRED (Federal Reserve Bank of St. Louis) : taux souverains et contrôles
# ---------------------------------------------------------------------------
FRED_SERIES = {
    "IRLTLT01FRM156N": "oat_10y",        # Taux long France 10 ans (OCDE, mensuel, %)
    "IRLTLT01DEM156N": "bund_10y",       # Taux long Allemagne 10 ans (OCDE, mensuel, %)
    "VIXCLS": "vix",                     # Volatilité implicite S&P 500 (aversion au risque, quotidien)
    "CP0000FRM086NEST": "hicp_fr",       # Indice des prix harmonisé France (Eurostat, mensuel)
}


def get_fred(series_id: str) -> pd.Series:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    df = pd.read_csv(StringIO(r.text))
    date_col = df.columns[0]  # "observation_date" (ou "DATE" selon la version)
    df[date_col] = pd.to_datetime(df[date_col])
    s = pd.to_numeric(df[series_id], errors="coerce")  # "." = valeur manquante
    s.index = df[date_col]
    return s


# ---------------------------------------------------------------------------
# 2. BCE : taux directeurs
# ---------------------------------------------------------------------------
ECB_SERIES = {
    "FM/B.U2.EUR.4F.KR.MRR_FR.LEV": "ecb_mro",  # Taux des opérations principales de refinancement
    "FM/B.U2.EUR.4F.KR.DFR.LEV": "ecb_dfr",     # Taux de la facilité de dépôt
}


def get_ecb(key: str) -> pd.Series:
    url = f"https://data-api.ecb.europa.eu/service/data/{key}?format=csvdata"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    df = pd.read_csv(StringIO(r.text))
    s = pd.to_numeric(df["OBS_VALUE"], errors="coerce")
    s.index = pd.to_datetime(df["TIME_PERIOD"])
    return s


# ---------------------------------------------------------------------------
# 3. CAC 40 (Yahoo Finance)
# ---------------------------------------------------------------------------
def get_cac40() -> pd.Series:
    import yfinance as yf

    df = yf.download("^FCHI", start=START, interval="1d", auto_adjust=True, progress=False)
    close = df["Close"]
    if isinstance(close, pd.DataFrame):  # selon la version de yfinance
        close = close.iloc[:, 0]
    return close


# ---------------------------------------------------------------------------
# Exécution
# ---------------------------------------------------------------------------
def save(s: pd.Series, name: str) -> None:
    s = s[s.index >= START].rename(name)
    s.to_csv(RAW / f"{name}.csv", index_label="date")
    print(f"  OK  {name:<10} {s.index.min().date()} -> {s.index.max().date()}  ({s.notna().sum()} obs.)")


if __name__ == "__main__":
    print("Téléchargement des données brutes dans", RAW.resolve())
    errors = []

    for sid, name in FRED_SERIES.items():
        try:
            save(get_fred(sid), name)
        except Exception as e:
            errors.append((name, e))

    for key, name in ECB_SERIES.items():
        try:
            save(get_ecb(key), name)
        except Exception as e:
            errors.append((name, e))

    try:
        save(get_cac40(), "cac40")
    except Exception as e:
        errors.append(("cac40", e))

    if errors:
        print("\nÉchecs :")
        for name, e in errors:
            print(f"  ERREUR {name}: {e}")
    else:
        print("\nToutes les séries ont été téléchargées.")

    budget_dir = RAW / "budget"
    if not budget_dir.exists() or not any(budget_dir.iterdir()):
        print(
            "\nRappel : télécharger les séries longues budgétaires sur\n"
            "https://data.economie.gouv.fr/explore/assets/situations-mensuelles-budgetaires-series-longues/\n"
            "et les placer dans data/raw/budget/"
        )
