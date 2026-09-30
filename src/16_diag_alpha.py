"""
16_diag_alpha.py
Diagnostic du réglage de RidgeCV : à quelle fréquence l'alpha choisi est-il sur la borne haute de la grille ?
(constat 8 de docs/revue_04_models.md : quand l'optimum est au bord, le réglage ne fait pas son travail.)

Mesure la grille ACTUELLE de chaque script (04, 06, 11) sans modifier aucun résultat.
Usage : python src/16_diag_alpha.py NOM        -> results/tables/diag_04/alpha_bornes_NOM.csv (+ résumé affiché)
"""
import importlib.util
from pathlib import Path
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
SRC = Path(__file__).parent
OUT = Path("results/tables/diag_04")
OUT.mkdir(parents=True, exist_ok=True)


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, SRC / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def alpha_and_max(model):
    ridge = model[-1]
    return float(ridge.alpha_), float(np.max(ridge.alphas))


def rows_04():
    M = load("m04", "04_models.py")
    df = pd.read_csv(M.DATA, index_col="mois").dropna(subset=list(M.TARGETS))
    test = df.index[df.index >= M.TEST_START]
    rows = []
    for target in M.TARGETS:
        for jeu, cols in M.FEATURE_SETS.items():
            for m in test:
                tr = df[df.index < m]
                a, amax = alpha_and_max(M.make_model("ridge").fit(tr[cols], tr[target]))
                rows.append(("04", target, jeu.split()[0], m, a, amax))
    return rows


def rows_06():
    X = load("x06", "06_extensions.py")
    df = X.load()
    rows = []
    for target in X.TARGETS:
        for jeu, cols in (("M0", X.MARKETS), ("M1", X.MARKETS + X.SPENDING)):
            rec = []

            class Rec:
                def fit(self, Xt, y):
                    self.m = X.reg_model("ridge").fit(Xt, y)
                    rec.append(alpha_and_max(self.m))
                    return self

                def predict(self, Xt):
                    return self.m.predict(Xt)

            res = X.walk_forward(df, target, cols, Rec)
            for m, (a, amax) in zip(res.index, rec):
                rows.append(("06", target, jeu, m, a, amax))
    return rows


def rows_11():
    P = load("p11", "11_panel_models.py")
    df = P.build_monthly()
    gov_cols = [c for c in df.columns if "gov_" in c]
    feats = [c for c in df.columns if c not in ("y_level", "y_change", "pays")]
    usable = df[df.index >= pd.Period("2002-01", "M")]
    feats = [c for c in feats if usable[c].notna().mean() >= 0.7]
    d = df.dropna(subset=["y_level", "spread"])
    d = d[d.index >= pd.Period("2002-01", "M")]
    months = sorted(m for m in d.index.unique() if m >= pd.Period("2012-01", "M"))
    rows = []
    for jeu, cols in (("sans_fp", [c for c in feats if c not in gov_cols]), ("complet", feats)):
        for i, m in enumerate(months):
            if i % 3:
                continue  # réestimation tous les 3 mois, comme E16
            tr = d[d.index < m]
            a, amax = alpha_and_max(P.make_model("ridge").fit(tr[cols], tr["y_change"]))
            rows.append(("11", "E16 y_change", jeu, str(m), a, amax))
    return rows


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "courant"
    rows = rows_04() + rows_06() + rows_11()
    r = pd.DataFrame(rows, columns=["script", "cible", "jeu", "mois", "alpha", "alpha_max_grille"])
    r["borne_haute"] = r.alpha >= 0.99 * r.alpha_max_grille
    r.to_csv(OUT / f"alpha_bornes_{name}.csv", index=False)
    s = r.groupby(["script", "cible", "jeu"]).agg(n=("alpha", "size"), pct_borne_haute=("borne_haute", "mean"),
                                                   alpha_median=("alpha", "median"),
                                                   alpha_max_grille=("alpha_max_grille", "first"))
    s["pct_borne_haute"] = (s.pct_borne_haute * 100).round(1)
    print(s.to_string())
