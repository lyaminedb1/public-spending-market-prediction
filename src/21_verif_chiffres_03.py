"""
21_verif_chiffres_03.py
Recalcule, indépendamment de 03_exploration.py, les chiffres de l'exploration cités dans CLAUDE.md et
compare-les aux valeurs citées. Aucun résultat n'est modifié.

Sortie : results/tables/diag_04/verif_chiffres_03.csv  (chiffre, valeur citée min/max, recalculé, conforme)
Usage  : python src/21_verif_chiffres_03.py
"""
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf, adfuller

warnings.filterwarnings("ignore")
OUT = Path("results/tables/diag_04")
df = pd.read_csv("data/processed/dataset_monthly.csv", index_col="mois")
tg = ["y_d_spread", "y_d_oat", "y_cac_ret"]
d = df.dropna(subset=tg)
rows = []


def add(chiffre, lo, hi, val, tol=0.0, note=""):
    rows.append({"chiffre": chiffre, "cite_min": lo, "cite_max": hi, "recalcule": round(float(val), 3),
                 "conforme": bool(lo - tol <= val <= hi + tol), "note": note})


def spearman(a, b):
    m = a.notna() & b.notna()
    return a[m].rank().corr(b[m].rank())


def corr_partielle(data, x, y, controles):
    r = data[[x, y] + controles].rank()
    Z = np.column_stack([np.ones(len(r))] + [r[c] for c in controles])
    res_x = r[x] - Z @ np.linalg.lstsq(Z, r[x], rcond=None)[0]
    res_y = r[y] - Z @ np.linalg.lstsq(Z, r[y], rcond=None)[0]
    return np.corrcoef(res_x, res_y)[0, 1]


# autocorrélation d'ordre 1 des cibles
for t, cite in zip(tg, (0.14, 0.23, -0.09)):
    add(f"autocorrélation d'ordre 1 de {t}", cite, cite, acf(d[t], nlags=1, fft=False)[1], tol=0.006)
# seuil de significativité à 5 % des corrélations
add("seuil de significativité à 5 % (1,96 / racine de n)", 0.16, 0.16, 1.96 / np.sqrt(len(d)), tol=0.005,
    note=f"n = {len(d)}")
# corrélations de Spearman budget (t-2) / cibles (t+1)
sp = {"investissement": "b_dep_investissement_ytd_gap", "personnel": "b_dep_personnel_ytd_gap",
      "charge de la dette": "b_dep_charge_dette_ytd_gap", "fonctionnement": "b_dep_fonctionnement_ytd_gap"}
add("Spearman investissement / Δspread", -0.16, -0.16, spearman(d[sp["investissement"]], d["y_d_spread"]), tol=0.006)
for lab, cite in (("personnel", 0.23), ("charge de la dette", 0.21), ("fonctionnement", 0.17)):
    add(f"Spearman {lab} / ΔOAT", cite, cite, spearman(d[sp[lab]], d["y_d_oat"]), tol=0.006)
allsp = [c for c in d.columns if c.startswith("b_") and c.endswith("_ytd_gap")]
mx = max(abs(spearman(d[c], d["y_cac_ret"])) for c in allsp if "recettes" not in c and c in
         [v for v in sp.values()] + ["b_dep_totales_ytd_gap", "b_dep_intervention_ytd_gap", "b_psr_total_ytd_gap"])
add("CAC 40 : plus forte |corrélation de Spearman| avec les 7 dépenses (aucune significative)", 0, 0.16, mx,
    note="seuil ±0,16")
# corrélations partielles (inflation et ΔOAT passée contrôlées)
for lab in ("personnel", "fonctionnement", "charge de la dette"):
    add(f"corrélation partielle {lab} / ΔOAT (inflation, ΔOAT passée contrôlées)", 0.09, 0.15,
        abs(corr_partielle(d, sp[lab], "y_d_oat", ["inflation_yoy", "d_oat"])), tol=0.006)
# stationnarité (ADF)
for t in tg:
    add(f"ADF p-value {t}", 0, 0.01, adfuller(d[t].dropna(), autolag="AIC")[1])
l12 = [c for c in df.columns if c.startswith("b_") and c.endswith("_12m") and not c.startswith("b_part")]
for c in l12:
    add(f"ADF p-value {c}", 0.7, 1.0, adfuller(df[c].dropna(), autolag="AIC")[1],
        note="niveau (CLAUDE.md : p > 0,7)")
for c in [c for c in allsp if any(k in c for k in ("dep_", "psr_"))]:
    add(f"ADF p-value {c}", 0.01, 0.06, adfuller(df[c].dropna(), autolag="AIC")[1], tol=0.005,
        note="écart YTD (CLAUDE.md : 0,01 à 0,06)")
for c in ("spread_bp", "oat_10y"):
    add(f"ADF p-value {c} (niveau)", 0.7, 1.0, adfuller(df[c].dropna(), autolag="AIC")[1],
        note="le notebook 03_EDA écrit « niveaux non stationnaires (p > 0,7) » pour le spread et l'OAT")
# corrélations fallacieuses des niveaux _12m avec l'OAT
c1 = max(abs(spearman(df[c], df["oat_10y"])) for c in l12)
c2 = max(abs(spearman(d[c], d["y_d_oat"])) for c in l12)
add("corrélations fallacieuses : plus forte |Spearman| entre un niveau _12m et le niveau de l'OAT", 0.34, 0.34, c1,
    tol=0.02, note="CLAUDE.md : « jusqu'à 0,34 »")
add("idem avec la variation ΔOAT du mois suivant", 0.34, 0.34, c2, tol=0.02, note="autre lecture possible de « 0,34 »")

out = pd.DataFrame(rows)
out.to_csv(OUT / "verif_chiffres_03.csv", index=False)
pd.set_option("display.width", 230)
pd.set_option("display.max_colwidth", 95)
print(out[["chiffre", "cite_min", "cite_max", "recalcule", "conforme"]].to_string(index=False))
print(f"\n{int(out.conforme.sum())}/{len(out)} conformes")
