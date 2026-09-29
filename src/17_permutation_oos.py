"""
17_permutation_oos.py
Importance des variables par permutation HORS ÉCHANTILLON (ajout post hoc, à déclarer comme tel).

Pourquoi : la part SHAP en échantillon ne distingue pas les dépenses du bruit (docs/revue_04_models.md, constat 4).
Ici, à chaque mois de test m, le modèle M1 est entraîné sur les mois < m (comme 04) et CONSERVÉ. On mélange ensuite
la colonne d'une variable entre les 79 mois de test (30 permutations) et on mesure la hausse du RMSE des prévisions
hors échantillon. Une variable utile fait monter le RMSE ; une variable inutile le laisse inchangé.

Contrôles intégrés :
  - négatif : 7 variables de pur bruit ajoutées à M1 (config « M1+bruit ») -> leur hausse de RMSE sert de référence ;
  - positif : une variable fictive corrélée à la cible (rho = 0,5), config « M1+signal » -> doit ressortir nettement.

Sortie : results/tables/models_permutation_oos.csv
Usage  : python src/17_permutation_oos.py     (~5 min)
"""
import importlib.util
from pathlib import Path
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
SRC = Path(__file__).parent
spec = importlib.util.spec_from_file_location("m04", SRC / "04_models.py")
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

N_PERM = 30
RHO = 0.5
OUT = M.TAB / "models_permutation_oos.csv"


def build(df, target, rng_noise, rng_signal):
    d = df.copy()
    noise = [f"bruit{i}" for i in range(7)]
    for c in noise:
        d[c] = rng_noise.standard_normal(len(d))
    z = (d[target] - d[target].mean()) / d[target].std()
    d["signal_rho05"] = RHO * z + np.sqrt(1 - RHO ** 2) * rng_signal.standard_normal(len(d))
    return d, noise


def permutation_table(d, target, model_name, cols, groups):
    """Entraîne un modèle par mois de test, puis mesure la hausse de RMSE par permutation de chaque variable."""
    test = list(d.index[d.index >= M.TEST_START])
    y = d.loc[test, target].values
    Xte = d.loc[test, cols].values
    models = []
    for m in test:
        tr = d[d.index < m]
        models.append(M.make_model(model_name).fit(tr[cols], tr[target]))

    n = len(test)
    base_pred = np.array([mod.predict(pd.DataFrame(Xte[[i]], columns=cols))[0] for i, mod in enumerate(models)])
    base = float(np.sqrt(np.mean((y - base_pred) ** 2)))
    rng = np.random.default_rng(123)
    perms = np.array([rng.permutation(n) for _ in range(N_PERM)])  # perms[k, i] : mois dont on emprunte la valeur
    rows = []
    items = [(c, [c]) for c in cols] + [(f"[groupe] {g}", members) for g, members in groups.items()]
    for name, members in items:
        idx = [cols.index(c) for c in members]
        sq = np.zeros(N_PERM)
        for i, mod in enumerate(models):
            Xi = np.tile(Xte[i], (N_PERM, 1))
            Xi[:, idx] = Xte[perms[:, i]][:, idx]
            sq += (y[i] - mod.predict(pd.DataFrame(Xi, columns=cols))) ** 2
        deltas = np.sqrt(sq / n) - base
        rows.append({"variable": name, "dRMSE_moyen": np.mean(deltas), "dRMSE_ecart_type": np.std(deltas, ddof=1),
                     "dRMSE_relatif_%": np.mean(deltas) / base * 100})
    return base, rows


def main():
    df = pd.read_csv(M.DATA, index_col="mois").dropna(subset=list(M.TARGETS))
    out = []
    for target in M.TARGETS:
        d, noise = build(df, target, np.random.default_rng(1), np.random.default_rng(2))
        for model_name in ("xgb", "ridge"):
            for config, extra in (("M1+bruit", noise), ("M1+signal", ["signal_rho05"])):
                cols = M.FEATURE_SETS["M1 + dépenses"] + extra
                groups = {"marchés": M.MARKETS, "dépenses": M.SPENDING}
                groups["bruit" if config == "M1+bruit" else "signal"] = extra
                base, rows = permutation_table(d, target, model_name, cols, groups)
                for r in rows:
                    v = r["variable"]
                    grp = ("dépenses" if v in M.SPENDING else "marchés" if v in M.MARKETS else
                           "bruit" if v in noise else "signal" if v in extra and config == "M1+signal" else "groupe")
                    out.append({"cible": target, "modele": model_name, "config": config, "RMSE_base": base,
                                "groupe": grp, **r})
                print(f"  {target} {model_name} {config} : base RMSE {base:.3f}", flush=True)
    res = pd.DataFrame(out).round(5)
    res.to_csv(OUT, index=False)
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
