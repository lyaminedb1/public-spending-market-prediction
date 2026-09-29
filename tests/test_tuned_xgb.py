"""
Non-fuite du réglage d'E10 (XGBoost réglé par validation croisée temporelle emboîtée, src/06_extensions.py).
Instrumente TunedXGB : à chaque prévision d'un mois m, ni le réglage (tune) ni l'ajustement (fit) ne doivent avoir vu
une ligne de mois >= m. Contrôle négatif : une version qui règle sur toutes les données est détectée.
  python tests/test_tuned_xgb.py
"""
import importlib.util
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("x06", ROOT / "src" / "06_extensions.py")
X = importlib.util.module_from_spec(spec)
spec.loader.exec_module(X)
RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append(bool(ok))
    print(f"  {'OK    ' if ok else 'ÉCHEC '} {label}" + (f"  ({detail})" if detail else ""))


def synthetic():
    idx = pd.period_range("2014-01", "2025-12", freq="M").astype(str)
    rng = np.random.default_rng(0)
    df = pd.DataFrame(rng.standard_normal((len(idx), len(X.MARKETS) + len(X.SPENDING))),
                      columns=X.MARKETS + X.SPENDING, index=idx)
    for t in X.TARGETS:
        df[t] = rng.standard_normal(len(idx))
    return df


def run(leaky=False):
    log = []
    orig_tune, orig_fit, orig_pred = X.TunedXGB.tune, X.TunedXGB.fit, X.TunedXGB.predict
    orig_grid, orig_targets = X.TunedXGB.GRID, X.TARGETS

    def tune(self, Xt, y):
        log.append(("tune", Xt.index.max()))
        return orig_tune(self, Xt, y)

    def fit(self, Xt, y):
        log.append(("fit", Xt.index.max()))
        return orig_fit(self, Xt, y)

    def pred(self, Xt):
        log.append(("pred", Xt.index.max()))
        return orig_pred(self, Xt)

    X.TunedXGB.tune, X.TunedXGB.fit, X.TunedXGB.predict = tune, fit, pred
    X.TunedXGB.GRID = orig_grid[:2]           # grille réduite : on teste la logique, pas la performance
    X.TARGETS = {"y_d_spread": "Δ spread"}
    try:
        df = synthetic()
        if leaky:                             # version cassée : le réglage voit toutes les données
            src_tune = X.TunedXGB.tune
            def tune_all(self, Xt, y):
                log.append(("tune", df.index.max()))
                return orig_tune(self, Xt, y)
            X.TunedXGB.tune = tune_all
        X.e_tuned(df)
    finally:
        X.TunedXGB.tune, X.TunedXGB.fit, X.TunedXGB.predict = orig_tune, orig_fit, orig_pred
        X.TunedXGB.GRID, X.TARGETS = orig_grid, orig_targets
    seen, viol, n_pred = "0000-00", 0, 0
    for kind, v in log:
        if kind in ("tune", "fit"):
            seen = max(seen, v)
        else:
            n_pred += 1
            viol += seen >= v                 # une ligne d'entraînement de mois >= mois prévu
    return viol, n_pred, sum(1 for k, _ in log if k == "tune")


viol, n_pred, n_tune = run()
check("aucun réglage ni ajustement n'a vu le mois prévu ou un mois postérieur", viol == 0, f"{n_pred} prévisions, {n_tune} réglages")
check("réglage refait tous les 12 mois (79 prévisions -> 7 réglages par jeu de variables)", n_tune == 14, f"{n_tune} réglages (2 jeux M0/M1)")
viol_bad, _, _ = run(leaky=True)
check("contrôle négatif : un réglage sur toutes les données est détecté", viol_bad > 0, f"{viol_bad} violations")
n_ok, n = sum(RESULTS), len(RESULTS)
print(f"\n{n_ok}/{n} contrôles réussis")
sys.exit(0 if n_ok == n else 1)
