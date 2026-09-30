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
  ecarts_revue : compare resume.csv aux chiffres écrits dans docs/revue_04_models.md -> ecarts_revue.csv
  resume       : agrège tous les CSV ci-dessus en un tableau long (bloc, cible, modele, cle, valeur) -> resume.csv
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


def resume():
    """Agrège les diagnostics déjà calculés (lecture seule des CSV) ; échoue si un fichier manque."""
    rows = []

    def add(bloc, cible, modele, cle, valeur):
        rows.append({"bloc": bloc, "cible": cible, "modele": modele, "cle": cle, "valeur": float(valeur)})

    def read(name):
        f = OUT / f"{name}.csv"
        if not f.exists():
            raise FileNotFoundError(f"{f} manquant : lancer d'abord le job « {name} »")
        return pd.read_csv(f)

    # puissance : variable fictive de corrélation rho ajoutée à M0 (Ridge)
    for (t, rho), g in read("positif").groupby(["cible", "rho"]):
        better = g["R2_avec_signal_%"] > g["R2_M0_%"]
        add("puissance", t, "ridge", f"rho={rho} : % tirages où le modèle bat la moyenne", (g["R2_avec_signal_%"] > 0).mean() * 100)
        add("puissance", t, "ridge", f"rho={rho} : % tirages où DM détecte l'apport (p<0,05 et gain>0)", ((g.p_DM < 0.05) & better).mean() * 100)
        add("puissance", t, "ridge", f"rho={rho} : % tirages où Clark-West détecte l'apport (p<0,05)", (g.p_CW < 0.05).mean() * 100)
    # contrôle négatif : rang des vraies dépenses parmi les tirages de bruit (part des tirages de bruit battus)
    for mod in ("ridge", "rf", "xgb"):
        for t, g in read(f"bruit_{mod}").groupby("cible"):
            reel = g.loc[g.jeu == "dépenses réelles", "gain_vs_M0_pts"].iloc[0]
            bruit_ = g.loc[g.jeu != "dépenses réelles", "gain_vs_M0_pts"]
            add("bruit", t, mod, "% tirages de bruit battus par les vraies dépenses", (reel > bruit_).mean() * 100)
            add("bruit", t, mod, "gain des vraies dépenses vs M0 (pts de R²)", reel)
            add("bruit", t, mod, "gain médian du bruit vs M0 (pts de R²)", bruit_.median())
    # Clark-West sur les prévisions de 04, et taille du test sur du bruit
    for _, r in read("cw").iterrows():
        add("clark_west", r.cible, r.modele, "p CW M1 vs M0", r.p_CW_M1_vs_M0)
        add("clark_west", r.cible, r.modele, "p DM bilatérale M1 vs M0", r.p_DM_bilat_M1_vs_M0)
    for mod in ("ridge", "xgb"):
        for t, g in read(f"cw_bruit_{mod}").groupby("cible"):
            add("taille_test", t, mod, "% tirages de bruit « significatifs » (Clark-West, p<0,05)", (g.p_CW < 0.05).mean() * 100)
            add("taille_test", t, mod, "% tirages de bruit « significatifs » (DM bilatéral, p<0,05)", (g.p_DM < 0.05).mean() * 100)
    # SHAP : part de 7 variables de bruit (en échantillon)
    for t, g in read("shap_bruit").groupby("cible"):
        add("shap_bruit", t, "xgb", "part SHAP du bruit : min (%)", g["part_SHAP_bruit_%"].min())
        add("shap_bruit", t, "xgb", "part SHAP du bruit : moyenne (%)", g["part_SHAP_bruit_%"].mean())
        add("shap_bruit", t, "xgb", "part SHAP du bruit : max (%)", g["part_SHAP_bruit_%"].max())
    # sensibilité à la graine
    for mod in ("rf", "xgb"):
        for t, g in read(f"graines_{mod}").groupby("cible"):
            add("graines", t, mod, "R² M0 min (%)", g["R2_M0_%"].min())
            add("graines", t, mod, "R² M0 max (%)", g["R2_M0_%"].max())
            add("graines", t, mod, "R² M1 min (%)", g["R2_M1_%"].min())
            add("graines", t, mod, "R² M1 max (%)", g["R2_M1_%"].max())
            add("graines", t, mod, "p DM M1 vs M0 minimale", g.p_DM.min())
    for _, r in read("ar1").iterrows():
        add("references", r.cible, "AR(1)", "R² hors échantillon (%)", r["R2_AR1_%"])
        add("references", r.cible, "variation nulle", "R² hors échantillon (%)", r["R2_variation_nulle_%"])
    return pd.DataFrame(rows)


def ecarts_revue():
    """Compare resume.csv aux chiffres de docs/revue_04_models.md (fourchettes [min, max] écrites dans la revue)."""
    r = pd.read_csv(OUT / "resume.csv")
    # (constat, bloc, texte de la clé, modele, cible, min, max, tolérance)
    attendu = [
        (1, "puissance", "rho=0.3 : % tirages où le modèle bat", None, None, 10, 30, 0),
        (1, "puissance", "rho=0.3 : % tirages où DM", None, None, 0, 50, 0),
        (1, "puissance", "rho=0.5 : % tirages où le modèle bat", None, None, 80, 100, 0),
        (1, "puissance", "rho=0.5 : % tirages où DM", None, None, 30, 80, 0),
        (1, "puissance", "rho=1.0 : % tirages où le modèle bat", None, None, 100, 100, 0),
        (2, "bruit", "% tirages de bruit battus", "ridge", None, 0, 10, 0),
        (2, "bruit", "% tirages de bruit battus", "rf", None, 0, 20, 0),
        (2, "bruit", "% tirages de bruit battus", "xgb", None, 40, 50, 0),
        (3, "clark_west", "p CW M1 vs M0", "xgb", "y_d_spread", 0.018, 0.018, 0.005),
        (3, "clark_west", "p CW M1 vs M0", "xgb", "y_cac_ret", 0.030, 0.030, 0.005),
        (3, "clark_west", "p CW M1 vs M0", "xgb", "y_d_oat", 0.083, 0.083, 0.005),
        (3, "taille_test", "Clark-West", "xgb", None, 45, 75, 0),
        (3, "taille_test", "Clark-West", "ridge", ["y_d_spread", "y_d_oat"], 40, 50, 0),
        (3, "taille_test", "DM bilatéral", None, None, 0, 5, 0),
        (4, "shap_bruit", "moyenne", None, None, 34, 38, 0.2),
        (5, "graines", "R² M0 min", "xgb", "y_d_spread", -39.8, -39.8, 0.1),
        (5, "graines", "R² M0 max", "xgb", "y_d_spread", -30.8, -30.8, 0.1),
        (5, "graines", "R² M0 min", "rf", "y_d_spread", -6.3, -6.3, 0.1),
        (5, "graines", "R² M0 max", "rf", "y_d_spread", -3.3, -3.3, 0.1),
        (5, "graines", "p DM M1 vs M0 minimale", "xgb", "y_d_spread", 0.14, 0.14, 0.01),
        (5, "graines", "p DM M1 vs M0 minimale", "rf", "y_d_spread", 0.13, 0.13, 0.01),
        (6, "references", "R²", "AR(1)", None, -2.7, -1.9, 0.06),
        (6, "references", "R²", "variation nulle", "y_d_spread", 1.7, 1.7, 0.06),
        (6, "references", "R²", "variation nulle", "y_d_oat", 2.4, 2.4, 0.06),
        (6, "references", "R²", "variation nulle", "y_cac_ret", -0.2, -0.2, 0.06),
    ]
    rows = []
    for constat, bloc, cle, modele, cible, lo, hi, tol in attendu:
        sel = r[(r.bloc == bloc) & r.cle.str.contains(cle, regex=False)]
        if modele:
            sel = sel[sel.modele == modele]
        if cible:
            sel = sel[sel.cible.isin([cible] if isinstance(cible, str) else cible)]
        for _, x in sel.iterrows():
            ok = lo - tol <= x.valeur <= hi + tol
            rows.append({"constat_revue": constat, "bloc": bloc, "cle": x.cle, "modele": x.modele, "cible": x.cible,
                         "revue_min": lo, "revue_max": hi, "recalcule": round(x.valeur, 3), "conforme": ok})
    return pd.DataFrame(rows)


JOBS = {
    "identite": identite, "ar1": ar1, "cw": cw, "shap_bruit": shap_bruit, "positif": positif,
    "bruit_ridge": lambda: bruit("ridge", 20), "bruit_rf": lambda: bruit("rf", 5), "bruit_xgb": lambda: bruit("xgb", 10),
    "graines_rf": lambda: graines("rf", 5), "graines_xgb": lambda: graines("xgb", 10),
    "cw_bruit_ridge": lambda: cw_bruit("ridge"), "cw_bruit_xgb": lambda: cw_bruit("xgb"), "resume": resume, "ecarts_revue": ecarts_revue,
}

if __name__ == "__main__":
    for job in sys.argv[1:] or ["identite", "ar1", "cw", "shap_bruit"]:
        res = JOBS[job]()
        res.to_csv(OUT / f"{job}.csv", index=False)
        print(f"{job} -> {OUT / (job + '.csv')}", flush=True)
