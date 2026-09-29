"""
19_robustesse_lag.py
Robustesse au décalage de publication du budget : compare 04 avec un décalage de 2 mois (principal) à ceux de
1 et 3 mois (results/tables/robustesse/*_lagN.csv, produits par
    python src/02_build_dataset.py --lag N
    python src/04_models.py --data data/processed/dataset_monthly_lagN.csv --suffix lagN ).

Sortie : results/tables/robustesse_lag.csv  (une ligne par lag, cible, modèle ; puis lignes de synthèse par lag)
"""
from pathlib import Path
import re

import pandas as pd

TAB = Path("results/tables")
ROB = TAB / "robustesse"
MODELS = ("ridge", "rf", "xgb")


def tables(lag):
    """(métriques, tests DM, nombre de mois de test) pour un décalage donné."""
    if lag == 2:
        met, dm = pd.read_csv(TAB / "models_metrics.csv"), pd.read_csv(TAB / "models_dm_tests.csv")
        n = len(pd.read_csv(TAB / "models_predictions_y_d_spread.csv"))
    else:
        met = pd.read_csv(ROB / f"models_metrics_lag{lag}.csv")
        dm = pd.read_csv(ROB / f"models_dm_tests_lag{lag}.csv")
        n = len(pd.read_csv(ROB / f"models_predictions_y_d_spread_lag{lag}.csv"))
    return met, dm, n


lags = sorted({2} | {int(re.search(r"lag(\d+)", f.stem).group(1)) for f in ROB.glob("models_metrics_lag*.csv")
                     if "lag0" not in f.stem})
rows, summary = [], []
label = {"ridge": "Ridge", "rf": "Forêt aléatoire", "xgb": "XGBoost"}
for lag in lags:
    met, dm, n = tables(lag)
    for t in met.cible.unique():
        for mod in MODELS:
            m = met[(met.cible == t) & (met.modele == mod)].set_index("variables")
            d = dm[(dm.cible == t) & (dm.test == f"{label[mod]} : M1 + dépenses vs M0")].iloc[0]
            rows.append({"lag_mois": lag, "cible": t, "modele": mod, "n_test": n,
                         "R2_M0_%": m.loc["M0 marchés", "R2_oos_%"], "R2_M1_%": m.loc["M1 + dépenses", "R2_oos_%"],
                         "delta_R2_M1_moins_M0_pts": m.loc["M1 + dépenses", "R2_oos_%"] - m.loc["M0 marchés", "R2_oos_%"],
                         "p_DM_bilaterale_M1_vs_M0": d.p_bilaterale, "p_BH_H1": d.p_BH_H1})
    r = pd.DataFrame([x for x in rows if x["lag_mois"] == lag])
    best = met[met.modele.isin(MODELS)]["R2_oos_%"].max()
    summary.append({"lag_mois": lag, "cible": "TOUTES", "modele": "synthèse", "n_test": n,
                    "meilleur_R2_%_tous_modeles": best, "R2_positif_quelque_part": bool(best > 0),
                    "p_DM_bilaterale_M1_vs_M0": r.p_DM_bilaterale_M1_vs_M0.min(),
                    "p_BH_H1": dm.p_BH_H1.min()})
out = pd.concat([pd.DataFrame(rows), pd.DataFrame(summary)], ignore_index=True).round(3)
out.to_csv(TAB / "robustesse_lag.csv", index=False)
print(out[out.cible == "TOUTES"].to_string(index=False))
print(f"-> {TAB / 'robustesse_lag.csv'}")
