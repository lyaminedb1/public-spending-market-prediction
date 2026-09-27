"""
15_diag_04.py
Diagnostics de la revue de 04_models (28/09/2026). Ne modifie AUCUN résultat de 04 : écrit seulement dans
results/tables/diag_04/. Rapport : docs/revue_04_models.md.

Usage (depuis la racine du dépôt) :
    python src/15_diag_04.py identite ar1 cw shap_bruit      (rapide)
    python src/15_diag_04.py positif                         (~10 min)
    python src/15_diag_04.py bruit_ridge bruit_rf bruit_xgb  (~30 min)
    python src/15_diag_04.py graines_rf graines_xgb          (~30 min)
    python src/15_diag_04.py cw_bruit_ridge cw_bruit_xgb     (~20 min)

Diagnostics :
  identite     : la validation glissante recodée ici redonne exactement les prévisions de 04 (Ridge M0, spread).
  ar1          : R² hors échantillon d'un AR(1) et de la prévision « variation nulle » face à la moyenne historique.
  cw           : test de Clark et West (2007) pour modèles emboîtés, sur les prévisions de 04.
  shap_bruit   : part de l'importance SHAP (XGBoost, en échantillon) obtenue par 7 variables de pur bruit.
  positif      : contrôle positif (puissance) : variable fictive de corrélation rho avec la cible ajoutée à M0 (Ridge).
  bruit_*      : contrôle négatif : 7 variables de bruit à la place des 7 dépenses ; compare le gain par rapport à M0.
  graines_*    : sensibilité de RF et XGBoost à la graine aléatoire (M0 et M1).
  cw_bruit_*   : taille du test de Clark-West : part des tirages de bruit jugés « significatifs ».
"""
import importlib.util
from pathlib import Path
import sys
import warnings

import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")
SRC = Path(__file__).parent
OUT = Path("results/tables/diag_04")
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(SRC))
spec = importlib.util.spec_from_file_location("m04", SRC / "04_models.py")
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

df = pd.read_csv(M.DATA, index_col="mois").dropna(subset=list(M.TARGETS))
TEST = df.index[df.index >= M.TEST_START]
M0, M1 = M.FEATURE_SETS["M0 marchés"], M.FEATURE_SETS["M1 + dépenses"]


def wf(d, target, cols, model="ridge", seed=None):
    """Même validation glissante que 04 : entraînement sur les mois < m, prévision du mois m."""
    out = []
    for m in TEST:
        tr = d[d.index < m]
        mod = M.make_model(model)
        if seed is not None and model in ("rf", "xgb"):
            mod.set_params(random_state=seed)
        mod.fit(tr[cols], tr[target])
        out.append(mod.predict(d.loc[[m], cols])[0])
    return np.array(out)


def mean_fc(target):
    return np.array([df.loc[df.index < m, target].mean() for m in TEST])


def r2(y, p, pm):
    return (1 - ((y - p) ** 2).sum() / ((y - pm) ** 2).sum()) * 100


def dm_p(e1, e2):
    """Diebold-Mariano, HLN, h = 1, bilatéral (même formule que 04)."""
    d = e1 ** 2 - e2 ** 2
    T = len(d)
    s = d.mean() / np.sqrt(d.var(ddof=0) / T) * np.sqrt((T - 1) / T)
    return 2 * (1 - stats.t.cdf(abs(s), T - 1))


def clark_west(y, p_small, p_big):
    """Clark et West (2007) : p unilatérale « le modèle emboîtant apporte quelque chose »."""
    f = (y - p_small) ** 2 - ((y - p_big) ** 2 - (p_small - p_big) ** 2)
    T = len(f)
    s = f.mean() / np.sqrt(f.var(ddof=1) / T)
    return s, 1 - stats.norm.cdf(s)


def noise(rng):
    return pd.DataFrame(rng.standard_normal((len(df), 7)), index=df.index, columns=[f"bruit{i}" for i in range(7)])


def identite():
    p = pd.read_csv("results/tables/models_predictions_y_d_spread.csv", index_col=0)
    ecart = np.abs(wf(df, "y_d_spread", M0) - p["ridge|M0 marchés"].values).max()
    print("écart max avec les prévisions de 04 (Ridge M0, spread) :", ecart)
    return pd.DataFrame([{"test": "identite ridge M0 spread", "ecart_max": ecart}])


def ar1():
    from sklearn.linear_model import LinearRegression
    rows = []
    for t, x in (("y_d_spread", "d_spread"), ("y_d_oat", "d_oat"), ("y_cac_ret", "cac_ret")):
        ym, y = mean_fc(t), df.loc[TEST, t].values
        p = np.array([LinearRegression().fit(df[df.index < m][[x]], df[df.index < m][t]).predict(df.loc[[m], [x]])[0]
                      for m in TEST])
        rows.append({"cible": t, "R2_AR1_%": r2(y, p, ym), "R2_variation_nulle_%": r2(y, np.zeros(len(y)), ym)})
    return pd.DataFrame(rows)


def cw():
    rows = []
    for t in M.TARGETS:
        p = pd.read_csv(f"results/tables/models_predictions_{t}.csv", index_col=0)
        y = p.y_true.values
        for mod in ("ridge", "rf", "xgb"):
            a, b = p[f"{mod}|M0 marchés"].values, p[f"{mod}|M1 + dépenses"].values
            s, pcw = clark_west(y, a, b)
            rows.append({"cible": t, "modele": mod, "CW_M1_vs_M0": s, "p_CW_M1_vs_M0": pcw,
                         "p_DM_bilat_M1_vs_M0": dm_p(y - a, y - b),
                         "p_CW_M1_vs_moyenne": clark_west(y, p.naif_moyenne.values, b)[1]})
    return pd.DataFrame(rows)


def shap_bruit():
    import shap
    rng, rows = np.random.default_rng(1), []
    for k in range(10):
        nz = noise(rng)
        d, cols = df.join(nz), M0 + list(nz.columns)
        for t in M.TARGETS:
            mod = M.make_model("xgb").fit(d[cols], d[t])
            sv = np.abs(shap.TreeExplainer(mod).shap_values(d[cols])).mean(0)
            rows.append({"tirage": k, "cible": t, "part_SHAP_bruit_%": sv[-7:].sum() / sv.sum() * 100})
    return pd.DataFrame(rows)


def positif():
    rng, rows = np.random.default_rng(0), []
    for t in M.TARGETS:
        y_all, ym, y = df[t], mean_fc(t), df.loc[TEST, t].values
        z = (y_all - y_all.mean()) / y_all.std()
        for rho in (0.1, 0.2, 0.3, 0.5, 1.0):
            for k in range(10 if rho < 1 else 1):
                sig = rho * z + np.sqrt(max(1 - rho ** 2, 0)) * rng.standard_normal(len(z))
                d = df.assign(signal=sig)
                p0, p1 = wf(d, t, M0), wf(d, t, M0 + ["signal"])
                rows.append({"cible": t, "rho": rho, "tirage": k, "R2_M0_%": r2(y, p0, ym),
                             "R2_avec_signal_%": r2(y, p1, ym), "p_DM": dm_p(y - p0, y - p1),
                             "p_CW": clark_west(y, p0, p1)[1]})
            print(f"  positif {t} rho={rho}", flush=True)
    return pd.DataFrame(rows)


def bruit(model, n):
    rng, rows = np.random.default_rng(0), []
    for t in M.TARGETS:
        ym, y = mean_fc(t), df.loc[TEST, t].values
        p0, p1 = wf(df, t, M0, model), wf(df, t, M1, model)
        rows.append({"cible": t, "jeu": "dépenses réelles", "R2_%": r2(y, p1, ym), "gain_vs_M0_pts": r2(y, p1, ym) - r2(y, p0, ym)})
        for k in range(n):
            nz = noise(rng)
            pb = wf(df.join(nz), t, M0 + list(nz.columns), model)
            rows.append({"cible": t, "jeu": f"bruit {k}", "R2_%": r2(y, pb, ym), "gain_vs_M0_pts": r2(y, pb, ym) - r2(y, p0, ym)})
        print(f"  bruit {model} {t}", flush=True)
    return pd.DataFrame(rows)


def graines(model, n):
    rows = []
    for t in M.TARGETS:
        ym, y = mean_fc(t), df.loc[TEST, t].values
        for s in range(n):
            p0, p1 = wf(df, t, M0, model, seed=s), wf(df, t, M1, model, seed=s)
            rows.append({"cible": t, "graine": s, "R2_M0_%": r2(y, p0, ym), "R2_M1_%": r2(y, p1, ym), "p_DM": dm_p(y - p0, y - p1)})
        print(f"  graines {model} {t}", flush=True)
    return pd.DataFrame(rows)


def cw_bruit(model, n=20):
    rng, rows = np.random.default_rng(7), []
    for t in M.TARGETS:
        y = df.loc[TEST, t].values
        p0 = wf(df, t, M0, model)
        for k in range(n):
            nz = noise(rng)
            pb = wf(df.join(nz), t, M0 + list(nz.columns), model)
            rows.append({"cible": t, "tirage": k, "p_CW": clark_west(y, p0, pb)[1], "p_DM": dm_p(y - p0, y - pb)})
        print(f"  cw_bruit {model} {t}", flush=True)
    return pd.DataFrame(rows)


JOBS = {
    "identite": identite, "ar1": ar1, "cw": cw, "shap_bruit": shap_bruit, "positif": positif,
    "bruit_ridge": lambda: bruit("ridge", 20), "bruit_rf": lambda: bruit("rf", 5), "bruit_xgb": lambda: bruit("xgb", 10),
    "graines_rf": lambda: graines("rf", 5), "graines_xgb": lambda: graines("xgb", 10),
    "cw_bruit_ridge": lambda: cw_bruit("ridge"), "cw_bruit_xgb": lambda: cw_bruit("xgb"),
}

if __name__ == "__main__":
    for job in sys.argv[1:] or ["identite", "ar1", "cw", "shap_bruit"]:
        res = JOBS[job]()
        res.to_csv(OUT / f"{job}.csv", index=False)
        print(f"{job} -> {OUT / (job + '.csv')}", flush=True)
