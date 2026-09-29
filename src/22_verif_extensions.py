"""
22_verif_extensions.py
Compare les résultats des extensions E1-E13 entre trois états :
  - « commité » : fichiers du dépôt avant la relance (calculés sur la machine d'origine, ancienne grille Ridge) ;
  - « ancienne grille, même environnement » : recalculés ici avec RidgeCV(10^-2 … 10^3) (référence isolant l'effet de
    l'environnement : versions de scikit-learn, numpy…) ;
  - « nouveau » : état courant (grille 10^-2 … 10^6).
Attendu : les comparaisons sans Ridge sont IDENTIQUES entre « ancienne grille » et « nouveau » ; seules celles qui font
intervenir Ridge changent.

Usage : python src/22_verif_extensions.py AVANT_SNAPSHOT DOSSIER_ANCIENNE_GRILLE
        (ex. tests/_snap/avant16/results/tables/extensions  /chemin/oldgrid/results/tables/extensions)
Sortie : results/tables/diag_04/verif_extensions.csv
"""
from pathlib import Path
import sys

import numpy as np
import pandas as pd

KEYS = ["extension", "cible", "comparaison"]
COLS = ["R2oos_sans_%", "R2oos_avec_%", "p_avec_meilleur"]
NEW = Path("results/tables/extensions")
FILES = ["E1", "E2", "E3", "E4", "E5", "E6", "E7E8", "E9", "E10", "E11", "E12", "E13"]


def load(folder):
    parts = []
    for k in FILES:
        f = Path(folder) / f"{k}.csv"
        if f.exists():
            parts.append(pd.read_csv(f))
    return pd.concat(parts, ignore_index=True)


committed, old, new = load(sys.argv[1]), load(sys.argv[2]), load(NEW)
m = new[KEYS + COLS].merge(old[KEYS + COLS], on=KEYS, suffixes=("_nouveau", "_ancienne_grille"), how="outer", indicator="_o")
m = m.merge(committed[KEYS + COLS].rename(columns={c: c + "_commite" for c in COLS}), on=KEYS, how="left")
assert (m["_o"] == "both").all(), "comparaisons différentes entre l'ancienne grille et le nouveau"
m["implique_ridge"] = m.comparaison.str.contains("ridge|Ridge|combinaison")  # E8 « combinaison » moyenne Ridge, RF et XGBoost
m["relance"] = ~m.extension.str.startswith("E10")  # E10 : relancé à l'étape 17
for c in ("R2oos_sans_%", "R2oos_avec_%", "p_avec_meilleur"):
    m[f"delta_grille_{c}"] = m[f"{c}_nouveau"] - m[f"{c}_ancienne_grille"]
    m[f"delta_env_{c}"] = m[f"{c}_ancienne_grille"] - m[f"{c}_commite"]
out = m.drop(columns="_o")
out.round(4).to_csv("results/tables/diag_04/verif_extensions.csv", index=False)

sans_ridge = out[~out.implique_ridge & out.relance]
avec_ridge = out[out.implique_ridge & out.relance]
print(f"{len(out)} comparaisons (E10 exclue des statistiques : relancée à l'étape 17) ; {len(avec_ridge)} avec Ridge, {len(sans_ridge)} sans")
print("sans Ridge : écart max nouveau - ancienne grille :", float(sans_ridge["delta_grille_R2oos_avec_%"].abs().max()),
      "(R² avec) /", float(sans_ridge["delta_grille_R2oos_sans_%"].abs().max()), "(R² sans)")
print("avec Ridge : écart max nouveau - ancienne grille (R², points) :",
      round(float(avec_ridge[["delta_grille_R2oos_avec_%", "delta_grille_R2oos_sans_%"]].abs().max().max()), 2),
      "| médiane :", round(float(avec_ridge[["delta_grille_R2oos_avec_%", "delta_grille_R2oos_sans_%"]].abs().stack().median()), 2))
print("écart environnement (ancienne grille ici - commité), tous modèles : max",
      round(float(out[["delta_env_R2oos_avec_%", "delta_env_R2oos_sans_%"]].abs().max().max()), 2),
      "| médiane", round(float(out[["delta_env_R2oos_avec_%", "delta_env_R2oos_sans_%"]].abs().stack().median()), 3))
