"""
06_extensions.py
Extensions pré-enregistrées (docs/plan_extensions.md, commit b136e8f du 26/09/2026 21:26).

Chaque extension compare une version « avec dépenses » à une version « sans dépenses »,
en validation glissante (test 2020-01 → dernier mois disponible), et contre la moyenne historique.
Les p-values « avec dépenses meilleure » de toutes les extensions sont corrigées par
Benjamini-Hochberg (taux de fausses découvertes 10 %) dans results/tables/ext_summary.csv.

Usage :  python src/06_extensions.py            (toutes les extensions, ~30-40 min)
         python src/06_extensions.py E1 E4      (seulement certaines)
"""
from pathlib import Path
import sys
import time
import warnings

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import ElasticNetCV, LogisticRegression, RidgeCV
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier, XGBRegressor

warnings.filterwarnings("ignore")

TAB = Path("results/tables/extensions")
TAB.mkdir(parents=True, exist_ok=True)
SEED = 42
TEST_START = "2020-01"

TARGETS = {"y_d_spread": "Δ spread", "y_d_oat": "Δ OAT", "y_cac_ret": "CAC 40"}
MARKETS = ["d_spread", "d_spread_l1", "spread_bp", "d_oat", "d_oat_l1", "cac_ret", "cac_ret_l1",
           "vix", "d_vix", "inflation_yoy", "ecb_dfr"]
SPENDING = ["b_dep_totales_ytd_gap", "b_dep_personnel_ytd_gap", "b_dep_fonctionnement_ytd_gap",
            "b_dep_charge_dette_ytd_gap", "b_dep_investissement_ytd_gap", "b_dep_intervention_ytd_gap",
            "b_psr_total_ytd_gap"]
REDUCED = ["d_spread", "d_oat", "cac_ret", "vix", "inflation_yoy", "ecb_dfr"]
SURPRISE = ["surprise_exec_dep", "surprise_exec_solde"]
RATINGS = ["rating_crans_moyen", "degradations_12m"]


# ---------------------------------------------------------------------------
# Modèles (mêmes hyperparamètres que src/04_models.py)
# ---------------------------------------------------------------------------
def reg_model(name):
    if name == "ridge":
        return make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-2, 3, 30)))
    if name == "rf":
        return RandomForestRegressor(n_estimators=300, max_depth=4, min_samples_leaf=5,
                                     max_features=0.5, random_state=SEED, n_jobs=-1)
    if name == "xgb":
        return XGBRegressor(n_estimators=200, max_depth=2, learning_rate=0.05, subsample=0.8,
                            colsample_bytree=0.8, min_child_weight=5, reg_lambda=1.0,
                            random_state=SEED, n_jobs=2, verbosity=0)
    if name == "enet":
        return make_pipeline(StandardScaler(), ElasticNetCV(
            l1_ratio=[0.1, 0.5, 0.9, 1.0], cv=TimeSeriesSplit(5), max_iter=20000, random_state=SEED))
    raise ValueError(name)


def clf_model(name):
    if name == "logit":
        return make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=5000))
    if name == "rf":
        return RandomForestClassifier(n_estimators=300, max_depth=4, min_samples_leaf=5,
                                      max_features=0.5, random_state=SEED, n_jobs=-1)
    if name == "xgb":
        return XGBClassifier(n_estimators=200, max_depth=2, learning_rate=0.05, subsample=0.8,
                             colsample_bytree=0.8, min_child_weight=5, reg_lambda=1.0,
                             random_state=SEED, n_jobs=2, verbosity=0)
    raise ValueError(name)


class PCAFeatures:
    """Modèle qui remplace les dépenses par leurs 2 premières composantes principales,
    l'ACP étant estimée sur l'échantillon d'entraînement uniquement."""

    def __init__(self, base, keep, spend, k=2):
        self.base, self.keep, self.spend, self.k = base, keep, spend, k

    def _t(self, X):
        pcs = self.pca.transform(self.scaler.transform(X[self.spend]))
        return np.column_stack([X[self.keep].values, pcs])

    def fit(self, X, y):
        self.scaler = StandardScaler().fit(X[self.spend])
        self.pca = PCA(self.k, random_state=SEED).fit(self.scaler.transform(X[self.spend]))
        self.model = reg_model(self.base).fit(self._t(X), y)
        return self

    def predict(self, X):
        return self.model.predict(self._t(X))


class TunedXGB:
    """XGBoost réglé par validation croisée temporelle emboîtée (entraînement uniquement)."""
    GRID = [dict(max_depth=d, n_estimators=n, learning_rate=lr)
            for d in (1, 2, 3) for n in (50, 150, 300) for lr in (0.03, 0.1)]

    def __init__(self, params=None):
        self.params = params

    def tune(self, X, y):
        best, best_err = None, np.inf
        for p in self.GRID:
            errs = []
            for tr, va in TimeSeriesSplit(4).split(X):
                m = XGBRegressor(subsample=0.8, colsample_bytree=0.8, min_child_weight=5,
                                 random_state=SEED, n_jobs=2, verbosity=0, **p)
                m.fit(X.iloc[tr], y.iloc[tr])
                errs.append(((y.iloc[va] - m.predict(X.iloc[va])) ** 2).mean())
            if np.mean(errs) < best_err:
                best, best_err = p, np.mean(errs)
        self.params = best
        return best

    def fit(self, X, y):
        self.model = XGBRegressor(subsample=0.8, colsample_bytree=0.8, min_child_weight=5,
                                  random_state=SEED, n_jobs=2, verbosity=0, **self.params).fit(X, y)
        return self

    def predict(self, X):
        return self.model.predict(X)


# ---------------------------------------------------------------------------
# Moteur de validation glissante
# ---------------------------------------------------------------------------
def walk_forward(df, target, cols, factory, h=1, window=None, test_end=None, proba=False):
    """Prévision de chaque mois de test avec un modèle entraîné sur les seules cibles déjà observées :
    pour un horizon h, la cible de la ligne s couvre s → s+h, donc on n'entraîne que sur s <= t-h."""
    d = df.dropna(subset=[target] + cols)
    pos = {m: i for i, m in enumerate(d.index)}
    test = [m for m in d.index if m >= TEST_START and (test_end is None or m <= test_end)]
    preds, means = [], []
    for m in test:
        i = pos[m]
        train = d.iloc[: max(0, i - h + 1)]
        if window:
            train = train.iloc[-window:]
        model = factory()
        model.fit(train[cols], train[target])
        x = d.loc[[m], cols]
        preds.append(model.predict_proba(x)[0, 1] if proba else model.predict(x)[0])
        means.append(train[target].mean())
    return pd.DataFrame({"y": d.loc[test, target], "pred": preds, "moyenne": means}, index=test)


def dm_test(e_a, e_b, h=1):
    """Diebold-Mariano (HLN), perte = e (déjà une perte si `loss` fourni).
    Renvoie la p-value unilatérale « b meilleur que a »."""
    d = e_a - e_b
    T = len(d)
    dc = d - d.mean()
    lrv = (dc ** 2).sum() / T
    for k in range(1, h):
        lrv += 2 * (1 - k / h) * (dc[k:] * dc[:-k]).sum() / T
    lrv = max(lrv, 1e-12)
    dm = d.mean() / np.sqrt(lrv / T)
    dm *= np.sqrt((T + 1 - 2 * h + h * (h - 1) / T) / T)
    return float(dm), float(1 - stats.t.cdf(dm, df=T - 1))


def r2_oos(res):
    return (1 - ((res.y - res.pred) ** 2).sum() / ((res.y - res.moyenne) ** 2).sum()) * 100


def compare(ext, target, label, res_a, res_b, h=1, note=""):
    """Ligne de synthèse : version A (sans dépenses) contre version B (avec dépenses)."""
    idx = res_a.index.intersection(res_b.index)
    a, b = res_a.loc[idx], res_b.loc[idx]
    stat, p = dm_test(((a.y - a.pred) ** 2).values, ((b.y - b.pred) ** 2).values, h)
    _, p_b_mean = dm_test(((b.y - b.moyenne) ** 2).values, ((b.y - b.pred) ** 2).values, h)
    return {"extension": ext, "cible": target, "comparaison": label, "n_test": len(idx),
            "R2oos_sans_%": r2_oos(a), "R2oos_avec_%": r2_oos(b), "DM": stat,
            "p_avec_meilleur": p, "p_avec_bat_moyenne": p_b_mean, "note": note}


# ---------------------------------------------------------------------------
# Données
# ---------------------------------------------------------------------------
def load():
    df = pd.read_csv("data/processed/dataset_monthly.csv", index_col="mois")
    extra = pd.read_csv("data/processed/extra_features.csv", index_col="mois")
    df = df.join(extra)
    # cibles à horizon h (variation cumulée entre t et t+h)
    for h in (3, 6, 12):
        df[f"y_d_spread_h{h}"] = df["y_d_spread"][::-1].rolling(h, min_periods=h).sum()[::-1]
        df[f"y_d_oat_h{h}"] = df["y_d_oat"][::-1].rolling(h, min_periods=h).sum()[::-1]
        g = np.log1p(df["y_cac_ret"] / 100)[::-1].rolling(h, min_periods=h).sum()[::-1]
        df[f"y_cac_ret_h{h}"] = np.expm1(g) * 100
    for t in TARGETS:
        df[f"{t}_abs"] = df[t].abs()
        df[f"{t}_up"] = (df[t] > 0).astype(float).where(df[t].notna())
    for c in ["d_spread", "d_oat", "cac_ret"]:
        df[f"{c}_abs"] = df[c].abs()
    df["regime_taux_pos"] = (df["ecb_dfr"] > 0).astype(float)
    for c in SPENDING:
        df[f"{c}_x_regime"] = df[c] * df["regime_taux_pos"]
    return df


# ---------------------------------------------------------------------------
# Extensions
# ---------------------------------------------------------------------------
def e_horizons(df):
    rows = []
    for h in (3, 6, 12):
        for t in TARGETS:
            tgt = f"{t}_h{h}"
            for m in ("ridge", "rf", "xgb"):
                a = walk_forward(df, tgt, MARKETS, lambda: reg_model(m), h=h)
                b = walk_forward(df, tgt, MARKETS + SPENDING, lambda: reg_model(m), h=h)
                rows.append(compare("E1 horizon", t, f"{m} h={h} : M1 vs M0", a, b, h=h))
    return rows


def e_classification(df):
    rows = []
    for t in TARGETS:
        tgt = f"{t}_up"
        for m in ("logit", "rf", "xgb"):
            a = walk_forward(df, tgt, MARKETS, lambda: clf_model(m), proba=True)
            b = walk_forward(df, tgt, MARKETS + SPENDING, lambda: clf_model(m), proba=True)
            r = compare("E2 classification", t, f"{m} : M1 vs M0 (perte de Brier)", a, b)
            for name, res in (("sans", a), ("avec", b)):
                r[f"precision_{name}_%"] = ((res.pred > 0.5) == (res.y == 1)).mean() * 100
                r[f"AUC_{name}"] = roc_auc_score(res.y, res.pred) if res.y.nunique() > 1 else np.nan
            r["precision_classe_majoritaire_%"] = ((a.moyenne > 0.5) == (a.y == 1)).mean() * 100
            r["note"] = "R2oos = score de Brier relatif à la fréquence historique"
            rows.append(r)
    return rows


def e_volatility(df):
    rows = []
    abs_lags = ["d_spread_abs", "d_oat_abs", "cac_ret_abs"]
    for t in TARGETS:
        for m in ("ridge", "rf", "xgb"):
            a = walk_forward(df, f"{t}_abs", MARKETS + abs_lags, lambda: reg_model(m))
            b = walk_forward(df, f"{t}_abs", MARKETS + abs_lags + SPENDING, lambda: reg_model(m))
            rows.append(compare("E3 volatilité", t, f"{m} : M1 vs M0", a, b))
    return rows


def e_surprise(df):
    rows = []
    end = df["surprise_exec_dep"].dropna().index.max()
    for t in TARGETS:
        for m in ("ridge", "rf", "xgb"):
            a = walk_forward(df, t, MARKETS, lambda: reg_model(m), test_end=end)
            b = walk_forward(df, t, MARKETS + SURPRISE, lambda: reg_model(m), test_end=end)
            c = walk_forward(df, t, MARKETS + SPENDING + SURPRISE, lambda: reg_model(m), test_end=end)
            rows.append(compare("E4 surprise", t, f"{m} : M0 + surprise vs M0", a, b,
                                note=f"test jusqu'à {end} (LFI 2026 indisponible)"))
            rows.append(compare("E4 surprise", t, f"{m} : M1 + surprise vs M0", a, c,
                                note=f"test jusqu'à {end}"))
    return rows


def e_regime(df):
    rows = []
    inter = [f"{c}_x_regime" for c in SPENDING]
    for t in TARGETS:
        a = walk_forward(df, t, MARKETS + ["regime_taux_pos"], lambda: reg_model("ridge"))
        b = walk_forward(df, t, MARKETS + ["regime_taux_pos"] + SPENDING + inter, lambda: reg_model("ridge"))
        rows.append(compare("E5 régime", t, "ridge : M1 + interactions régime vs M0 + régime", a, b))
    return rows


def e_reduced(df):
    rows = []
    small_spend = ["b_dep_totales_ytd_gap", "b_dep_charge_dette_ytd_gap"]
    for t in TARGETS:
        for m in ("ridge", "rf", "xgb"):
            a = walk_forward(df, t, REDUCED, lambda: reg_model(m))
            b = walk_forward(df, t, REDUCED + small_spend, lambda: reg_model(m))
            c = walk_forward(df, t, REDUCED + SPENDING, lambda: PCAFeatures(m, REDUCED, SPENDING))
            rows.append(compare("E6 réduit", t, f"{m} : réduit + 2 dépenses vs réduit", a, b))
            rows.append(compare("E6 réduit", t, f"{m} : réduit + 2 CP des dépenses vs réduit", a, c))
    return rows


def e_shrink_combo(df):
    """E7 et E8 à partir des prévisions déjà calculées par src/04_models.py."""
    rows = []
    for t in TARGETS:
        p = pd.read_csv(f"results/tables/models_predictions_{t}.csv", index_col=0)
        base = lambda col: pd.DataFrame({"y": p.y_true, "pred": p[col], "moyenne": p.naif_moyenne})
        for m in ("ridge", "rf", "xgb"):
            a, b = base(f"{m}|M0 marchés"), base(f"{m}|M1 + dépenses")
            a.pred = 0.5 * a.pred + 0.5 * a.moyenne
            b.pred = 0.5 * b.pred + 0.5 * b.moyenne
            rows.append(compare("E7 tempérée", t, f"{m} 50/50 avec la moyenne : M1 vs M0", a, b))
        combo = {s: base(f"ridge|{s}").assign(pred=p[[f"{m}|{s}" for m in ("ridge", "rf", "xgb")]].mean(axis=1))
                 for s in ("M0 marchés", "M1 + dépenses")}
        rows.append(compare("E8 combinaison", t, "moyenne Ridge/RF/XGB : M1 vs M0",
                            combo["M0 marchés"], combo["M1 + dépenses"]))
        for s in combo:
            combo[s] = combo[s].assign(pred=0.5 * combo[s].pred + 0.5 * combo[s].moyenne)
        rows.append(compare("E8 combinaison", t, "combinaison tempérée 50/50 : M1 vs M0",
                            combo["M0 marchés"], combo["M1 + dépenses"]))
    return rows


def e_enet(df):
    rows = []
    for t in TARGETS:
        a = walk_forward(df, t, MARKETS, lambda: reg_model("enet"))
        b = walk_forward(df, t, MARKETS + SPENDING, lambda: reg_model("enet"))
        rows.append(compare("E9 Elastic Net", t, "enet : M1 vs M0", a, b))
    return rows


def e_tuned(df):
    rows = []
    for t in TARGETS:
        out = {}
        for name, cols in (("M0", MARKETS), ("M1", MARKETS + SPENDING)):
            d = df.dropna(subset=[t] + cols)
            test = [m for m in d.index if m >= TEST_START]
            preds, means, params = [], [], None
            for k, m in enumerate(test):
                train = d[d.index < m]
                if k % 12 == 0:  # réglage refait tous les 12 mois, sur l'entraînement seulement
                    params = TunedXGB().tune(train[cols], train[t])
                model = TunedXGB(params).fit(train[cols], train[t])
                preds.append(model.predict(d.loc[[m], cols])[0])
                means.append(train[t].mean())
            out[name] = pd.DataFrame({"y": d.loc[test, t], "pred": preds, "moyenne": means}, index=test)
        rows.append(compare("E10 XGB réglé", t, "xgb réglé : M1 vs M0", out["M0"], out["M1"]))
    return rows


def e_rolling(df):
    rows = []
    for t in TARGETS:
        for m in ("ridge", "rf", "xgb"):
            a = walk_forward(df, t, MARKETS, lambda: reg_model(m), window=60)
            b = walk_forward(df, t, MARKETS + SPENDING, lambda: reg_model(m), window=60)
            rows.append(compare("E11 fenêtre 60 mois", t, f"{m} : M1 vs M0", a, b))
    return rows


def e_periods(df):
    rows = []
    for t in TARGETS:
        p = pd.read_csv(f"results/tables/models_predictions_{t}.csv", index_col=0)
        vix = df.loc[p.index, "vix"]
        subsets = {"2020-2021": p.index < "2022-01", "2022-2026": p.index >= "2022-01",
                   "VIX ≤ 20": (vix <= 20).values, "VIX > 20": (vix > 20).values}
        for m in ("ridge", "rf", "xgb"):
            for sname, mask in subsets.items():
                q = p[mask]
                a = pd.DataFrame({"y": q.y_true, "pred": q[f"{m}|M0 marchés"], "moyenne": q.naif_moyenne})
                b = pd.DataFrame({"y": q.y_true, "pred": q[f"{m}|M1 + dépenses"], "moyenne": q.naif_moyenne})
                rows.append(compare("E12 par période", t, f"{m} [{sname}] : M1 vs M0", a, b))
    return rows


def e_ratings(df):
    rows = []
    for t in TARGETS:
        for m in ("ridge", "rf", "xgb"):
            a0 = walk_forward(df, t, MARKETS, lambda: reg_model(m))
            a = walk_forward(df, t, MARKETS + RATINGS, lambda: reg_model(m))
            b = walk_forward(df, t, MARKETS + RATINGS + SPENDING, lambda: reg_model(m))
            r = compare("E13 notations", t, f"{m} : M1 + notations vs M0 + notations", a, b)
            r["R2oos_M0_sans_notations_%"] = r2_oos(a0.loc[a.index])
            rows.append(r)
    return rows


EXTENSIONS = {"E1": e_horizons, "E2": e_classification, "E3": e_volatility, "E4": e_surprise,
              "E5": e_regime, "E6": e_reduced, "E7E8": e_shrink_combo, "E9": e_enet,
              "E10": e_tuned, "E11": e_rolling, "E12": e_periods, "E13": e_ratings}


def benjamini_hochberg(p, q=0.10):
    p = np.asarray(p)
    n = len(p)
    order = np.argsort(p)
    adj = np.empty(n)
    adj[order] = np.minimum.accumulate((p[order] * n / np.arange(1, n + 1))[::-1])[::-1]
    return np.minimum(adj, 1), np.minimum(adj, 1) <= q


def summarize():
    files = sorted(TAB.glob("E*.csv"))
    s = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    # E12 (sous-périodes) est une ventilation d'E0, pas un test indépendant : exclue de la correction
    mask = ~s.extension.str.startswith("E12")
    s["p_BH"], s["significatif_BH_10%"] = np.nan, False
    adj, sig = benjamini_hochberg(s.loc[mask, "p_avec_meilleur"])
    s.loc[mask, "p_BH"], s.loc[mask, "significatif_BH_10%"] = adj, sig
    s.round(3).to_csv("results/tables/ext_summary.csv", index=False)
    return s


if __name__ == "__main__":
    df = load()
    todo = sys.argv[1:] or list(EXTENSIONS)
    for key in todo:
        t0 = time.time()
        rows = EXTENSIONS[key](df)
        pd.DataFrame(rows).round(4).to_csv(TAB / f"{key}.csv", index=False)
        print(f"{key} terminé en {time.time() - t0:.0f} s ({len(rows)} comparaisons)", flush=True)
    s = summarize()
    print(f"\nComparaisons au total : {len(s)} ; significatives après correction BH : "
          f"{int(s['significatif_BH_10%'].sum())}")
