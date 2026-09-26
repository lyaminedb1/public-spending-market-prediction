"""
05_extra_features.py
Variables supplémentaires pour les extensions pré-enregistrées (docs/plan_extensions.md).

E4  Surprise budgétaire : taux d'exécution du budget voté (LFI) à fin de mois,
    comparé au même mois de l'année précédente (points de %). Disponible pour 2013-2025
    (LFI 2026 absente des fichiers open data). Décalé de 2 mois comme le reste du budget.
E13 Notations souveraines : nombre moyen de crans sous AAA (Fitch, Moody's, S&P) et nombre
    de dégradations sur 12 mois, connus en fin de mois t (information publique immédiate).

Sortie : data/processed/extra_features.csv (index = mois du jeu de données)
"""
from pathlib import Path
import numpy as np
import pandas as pd

RAW = Path("data/raw")
BUDGET_LAG = 2
LINES = {"Total dépenses nettes du budget général": "dep", "Solde budgétaire": "solde"}


def read_smb(fname):
    d = pd.read_csv(RAW / "budget" / fname, sep=";", encoding="utf-16", decimal=",")
    d = d.dropna(subset=["Ligne d'information"])
    d["ligne"] = d["Ligne d'information"].str.strip()
    dates = [c for c in d.columns if isinstance(c, str) and c.count("/") == 2]
    d = d[d["ligne"].isin(LINES)].set_index("ligne")[dates].T
    d.index = pd.to_datetime(d.index, format="%d/%m/%Y").to_period("M")
    return d.rename(columns=LINES).astype(float)


def read_lfi(fname):
    d = pd.read_csv(RAW / "budget" / fname, sep=";", encoding="utf-16", decimal=",")
    d = d.dropna(axis=1, how="all").dropna(subset=["Ligne d'information"])
    d["ligne"] = d["Ligne d'information"].str.strip()
    years = [c for c in d.columns if str(c).strip().isdigit()]
    d = d[(d["Texte législatif"] == "LFI") & d["ligne"].isin(LINES)].set_index("ligne")[years].T
    d.index = d.index.astype(int)
    return d.rename(columns=LINES).astype(float)


def surprise():
    cumul = pd.concat([read_smb("Séries longues SMB_DGFiP_2013-2023.csv"),
                       read_smb("Serie longue SMB_DGFiP_2024-xx.csv")]).sort_index()
    cumul = cumul[~cumul.index.duplicated(keep="last")]
    lfi = pd.concat([read_lfi("textes législatifs open data_2013-2023.csv"),
                     read_lfi("textes législatifs_2024-xx.csv")])
    lfi_m = lfi.reindex(cumul.index.year).set_axis(cumul.index)
    ratio = cumul / lfi_m * 100                      # % du budget voté exécuté à fin de mois
    out = (ratio - ratio.shift(12)).add_prefix("surprise_exec_")
    out.index = out.index + BUDGET_LAG               # décalage de publication
    return out


def ratings(index):
    ev = pd.read_csv(RAW / "ratings_france.csv", parse_dates=["date"])
    ev["mois"] = ev["date"].dt.to_period("M")
    start = {"Fitch": 0, "S&P": 1, "Moody's": 1}     # crans sous AAA en janvier 2013
    months = pd.period_range("2013-01", index.max(), freq="M")
    notches = pd.DataFrame({a: float(n) for a, n in start.items()}, index=months)
    for _, r in ev.iterrows():
        notches.loc[notches.index >= r["mois"], r["agence"]] += 1
    down = ev.groupby("mois").size().reindex(months, fill_value=0)
    out = pd.DataFrame({"rating_crans_moyen": notches.mean(axis=1),
                        "degradations_12m": down.rolling(12, min_periods=1).sum()})
    return out.reindex(index)


def main():
    base = pd.read_csv("data/processed/dataset_monthly.csv", index_col="mois")
    idx = pd.PeriodIndex(base.index, freq="M")
    out = surprise().reindex(idx).join(ratings(idx))
    out.index = out.index.astype(str)
    out.index.name = "mois"
    out.to_csv("data/processed/extra_features.csv")
    print(out.describe().round(2).T[["count", "mean", "std", "min", "max"]])
    print("Surprise disponible jusqu'au mois :", out["surprise_exec_dep"].dropna().index.max())


if __name__ == "__main__":
    main()
