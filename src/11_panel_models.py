"""
11_panel_models.py
Extensions E15 (panel trimestriel Eurostat) et E16 (réplication élargie de Bouillot et al., 2025).
Protocoles pré-enregistrés dans docs/plan_extensions.md.

Entrées :
  data/raw/large/base_elargie_mensuelle.csv   (src/10_collect_large.py)
  data/raw/large/dictionnaire_variables.csv
  data/raw/panel/eurostat_gov_10q_ggnfa.csv    (src/09_collect_panel.py)
Sorties : results/tables/extensions/E15.csv, E16.csv, E16_par_pays.csv, E16_features.csv

Usage : python src/11_panel_models.py [E15] [E16]
"""
from pathlib import Path
import sys
import time
import warnings

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import RidgeCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor

warnings.filterwarnings("ignore")
SEED = 42
PANEL = ["FR", "IT", "ES", "PT", "BE"]
BASE = Path("data/raw/large/base_elargie_mensuelle.csv")
DICO = Path("data/raw/large/dictionnaire_variables.csv")
EUROSTAT = Path("data/raw/panel/eurostat_gov_10q_ggnfa.csv")
TAB = Path("results/tables/extensions")
TAB.mkdir(parents=True, exist_ok=True)

GOV_ITEMS = ["TE", "D1PAY", "D41PAY", "P51G", "D62PAY", "P2", "TR"]
MACRO_LAG1 = ("chomage", "ipch", "production_ind", "production_manuf", "confiance_menages",
              "confiance_entreprises", "indicateur_avance", "us_production_ind", "us_inflation",
              "us_chomage", "zone_euro_chomage", "zone_euro_ipch")
YOY = ("ipch", "production_ind", "production_manuf", "us_production_ind", "us_inflation", "zone_euro_ipch")
LOGRET = ("actions", "petrole_brent", "eur_usd")


# ---------------------------------------------------------------------------
# Modèles (hyperparamètres de src/04_models.py ; imputation apprise sur l'entraînement)
# ---------------------------------------------------------------------------
def make_model(name):
    if name == "ridge":
        return make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                             RidgeCV(alphas=np.logspace(-2, 4, 30)))
    if name == "rf":
        return make_pipeline(SimpleImputer(strategy="median"),
                             RandomForestRegressor(n_estimators=300, max_depth=4, min_samples_leaf=5,
                                                   max_features=0.5, random_state=SEED, n_jobs=-1))
    if name == "xgb":
        return XGBRegressor(n_estimators=200, max_depth=2, learning_rate=0.05, subsample=0.8,
                            colsample_bytree=0.8, min_child_weight=5, reg_lambda=1.0,
                            random_state=SEED, n_jobs=2, verbosity=0)
    raise ValueError(name)


def dm_pvalue(loss_a, loss_b, h=1):
    """Diebold-Mariano (HLN) sur des pertes ; p unilatérale « b meilleur que a »."""
    d = np.asarray(loss_a) - np.asarray(loss_b)
    T = len(d)
    dc = d - d.mean()
    lrv = (dc ** 2).sum() / T
    for k in range(1, h):
        lrv += 2 * (1 - k / h) * (dc[k:] * dc[:-k]).sum() / T
    stat = d.mean() / np.sqrt(max(lrv, 1e-12) / T) * np.sqrt((T + 1 - 2 * h + h * (h - 1) / T) / T)
    return float(stat), float(1 - stats.t.cdf(stat, df=T - 1))


# ---------------------------------------------------------------------------
# Finances publiques Eurostat : croissance sur un an des sommes sur 4 trimestres
# ---------------------------------------------------------------------------
def gov_quarterly():
    g = pd.read_csv(EUROSTAT)
    g["q"] = pd.PeriodIndex(g["time"].str.replace("-", ""), freq="Q")
    w = g.pivot_table(index=["geo", "q"], columns="na_item", values="valeur").sort_index()
    out = []
    for geo, d in w.groupby(level=0):
        d = d.droplevel(0).sort_index()
        s4 = d.rolling(4).sum()
        f = pd.DataFrame(index=d.index)
        for it in GOV_ITEMS:
            if it in s4:
                f[f"gov_{it}_yoy"] = (s4[it] / s4[it].shift(4) - 1) * 100
        if {"B9", "TE"} <= set(d.columns):
            f["gov_solde_pct_depenses"] = s4["B9"] / s4["TE"] * 100
        if {"D41PAY", "TE"} <= set(d.columns):
            f["gov_part_interets"] = s4["D41PAY"] / s4["TE"] * 100
        f["geo"] = geo
        out.append(f)
    return pd.concat(out)


# ---------------------------------------------------------------------------
# Base mensuelle : transformations par bloc + décalages de publication
# ---------------------------------------------------------------------------
def transform(s, name):
    base = name.split("_", 1)[1] if name[:2] in ("FR", "DE", "IT", "ES", "PT", "BE") else name
    if base.endswith(YOY) or base in YOY:
        x = (s / s.shift(12) - 1) * 100
        out = {"yoy": x, "d": x.diff()}
    elif base in LOGRET:
        out = {"r1": np.log(s).diff() * 100, "r12": np.log(s).diff(12) * 100}
    else:
        out = {"lvl": s, "d": s.diff()}
    lag = 1 if base in MACRO_LAG1 else 0
    return {k: v.shift(lag) for k, v in out.items()}


def build_monthly():
    raw = pd.read_csv(BASE, index_col="mois")
    raw.index = pd.PeriodIndex(raw.index, freq="M")
    dico = pd.read_csv(DICO).set_index("variable")
    gov = gov_quarterly()

    common = {}  # Allemagne + mondial, identiques pour tous les pays
    for col in raw.columns:
        if col.startswith("DE_") or dico.loc[col, "pays"] == "MONDE":
            for k, v in transform(raw[col], col).items():
                common[f"{col}_{k}"] = v
                common[f"{col}_{k}_l1"] = v.shift(1)
    common = pd.DataFrame(common)

    rows = []
    for c in PANEL:
        if f"{c}_taux_long" not in raw or "DE_taux_long" not in raw:
            continue
        d = pd.DataFrame(index=raw.index)
        spread = (raw[f"{c}_taux_long"] - raw["DE_taux_long"]) * 100
        d["spread"] = spread
        d["d_spread"] = spread.diff()
        d["d_spread_l1"] = d["d_spread"].shift(1)
        d["y_level"] = spread.shift(-1)
        d["y_change"] = spread.shift(-1) - spread
        for col in [x for x in raw.columns if x.startswith(f"{c}_")]:
            for k, v in transform(raw[col], col).items():
                d[f"pays_{col[3:]}_{k}"] = v
                d[f"pays_{col[3:]}_{k}_l1"] = v.shift(1)
        # finances publiques du pays : trimestre q connu à partir du trimestre q+2
        gq = gov[gov.geo == c].drop(columns="geo")
        gq.index = gq.index + 2
        gm = gq.reindex(pd.period_range(gq.index.min().asfreq("M", "s"), raw.index.max(), freq="M").asfreq("Q"))
        gm.index = pd.period_range(gq.index.min().asfreq("M", "s"), raw.index.max(), freq="M")
        d = d.join(gm)
        # finances publiques allemandes (référence du spread)
        gde = gov[gov.geo == "DE"].drop(columns="geo")
        if len(gde):
            gde.index = gde.index + 2
            gdm = gde.reindex(pd.period_range(gde.index.min().asfreq("M", "s"), raw.index.max(), freq="M").asfreq("Q"))
            gdm.index = pd.period_range(gde.index.min().asfreq("M", "s"), raw.index.max(), freq="M")
            d = d.join(gdm.add_prefix("DE_"))
        d = d.join(common)
        for p in PANEL:
            d[f"pays_is_{p}"] = float(p == c)
        d["pays"] = c
        rows.append(d)
    df = pd.concat(rows)
    df.index.name = "mois"
    return df


# ---------------------------------------------------------------------------
# E16 : validation glissante mensuelle sur le panel
# ---------------------------------------------------------------------------
def e16(df, test_start="2012-01", refit_every=3):
    gov_cols = [c for c in df.columns if "gov_" in c]
    feats_all = [c for c in df.columns if c not in ("y_level", "y_change", "pays")]
    # retirer les variables trop incomplètes sur la période utile
    usable = df[df.index >= pd.Period("2002-01", "M")]
    feats_all = [c for c in feats_all if usable[c].notna().mean() >= 0.7]
    feats_nogov = [c for c in feats_all if c not in gov_cols]
    pd.Series({"variables_total": len(feats_all), "dont_finances_publiques": len(set(feats_all) & set(gov_cols))}).to_csv(TAB / "E16_features.csv")
    print(f"E16 : {len(feats_all)} variables ({len(set(feats_all) & set(gov_cols))} de finances publiques)", flush=True)

    d = df.dropna(subset=["y_level", "spread"]).copy()
    d = d[d.index >= pd.Period("2002-01", "M")]
    months = sorted(m for m in d.index.unique() if m >= pd.Period(test_start, "M"))
    preds = []
    for target in ("y_level", "y_change"):
        for model in ("xgb", "rf", "ridge"):
            for set_name, cols in (("sans_finances_publiques", feats_nogov), ("complet", feats_all)):
                fitted = None
                for i, m in enumerate(months):
                    if i % refit_every == 0:
                        train = d[d.index < m]
                        fitted = make_model(model).fit(train[cols], train[target])
                    test = d[d.index == m]
                    p = fitted.predict(test[cols])
                    hist = d[(d.index < m)]
                    for (_, r), pv in zip(test.iterrows(), p):
                        mean_c = hist.loc[hist.pays == r.pays, target].mean()
                        preds.append({"mois": str(m), "pays": r.pays, "cible": target, "modele": model,
                                      "variables": set_name, "y": r[target], "pred": pv,
                                      "spread_t": r.spread, "moyenne": mean_c})
                print(f"  {target} {model} {set_name} : terminé", flush=True)
    P = pd.DataFrame(preds)
    P.to_csv(TAB / "E16_predictions.csv", index=False)
    return P


def e16_summary(P):
    rows, by_country = [], []
    for (target, model), g in P.groupby(["cible", "modele"]):
        # prévision convertie en niveau pour comparer à la marche aléatoire
        def level(x):
            return x.pred if target == "y_level" else x.spread_t + x.pred
        def true_level(x):
            return x.y if target == "y_level" else x.spread_t + x.y
        res = {}
        for s, gs in g.groupby("variables"):
            gs = gs.sort_values(["mois", "pays"])
            e = true_level(gs) - level(gs)
            rw = true_level(gs) - gs.spread_t
            mean_err = gs.y - gs.moyenne
            res[s] = gs.assign(loss=e ** 2, loss_rw=rw ** 2, loss_mean=mean_err ** 2, err=gs.y - gs.pred)
        a, b = res["sans_finances_publiques"], res["complet"]
        la, lb = a.groupby("mois").loss.sum(), b.groupby("mois").loss.sum()
        lrw = b.groupby("mois").loss_rw.sum()
        stat, p = dm_pvalue(la.values, lb.values)
        _, p_rw = dm_pvalue(lrw.values, lb.values)
        r2_mean = lambda x: (1 - (x.err ** 2).sum() / x.loss_mean.sum()) * 100
        rows.append({
            "extension": "E16 réplication élargie", "cible": "spread " + ("niveau" if target == "y_level" else "variation"),
            "comparaison": f"{model} : complet vs sans finances publiques", "n_test": len(b),
            "R2_vs_moyenne_sans_%": r2_mean(a), "R2_vs_moyenne_avec_%": r2_mean(b),
            "gain_vs_marche_aleatoire_sans_%": (1 - a.loss.sum() / a.loss_rw.sum()) * 100,
            "gain_vs_marche_aleatoire_avec_%": (1 - b.loss.sum() / b.loss_rw.sum()) * 100,
            "RMSE_niveau_avec_pb": np.sqrt(b.loss.mean()), "RMSE_marche_aleatoire_pb": np.sqrt(b.loss_rw.mean()),
            "DM": stat, "p_avec_meilleur": p, "p_avec_bat_marche_aleatoire": p_rw,
        })
        for c in PANEL:
            ac, bc = a[a.pays == c], b[b.pays == c]
            if len(bc):
                by_country.append({"cible": target, "modele": model, "pays": c,
                                   "RMSE_sans_pb": np.sqrt(ac.loss.mean()), "RMSE_avec_pb": np.sqrt(bc.loss.mean()),
                                   "RMSE_marche_aleatoire_pb": np.sqrt(bc.loss_rw.mean())})
    out = pd.DataFrame(rows).round(3)
    out.to_csv(TAB / "E16.csv", index=False)
    pd.DataFrame(by_country).round(3).to_csv(TAB / "E16_par_pays.csv", index=False)
    return out


# ---------------------------------------------------------------------------
# E15 : panel trimestriel (moyennes trimestrielles), protocole réduit pré-enregistré
# ---------------------------------------------------------------------------
def e15(df, test_start="2010Q1"):
    q = df.copy()
    q["q"] = q.index.asfreq("Q")
    agg = q.groupby(["pays", "q"]).agg(spread=("spread", "mean"),
                                       vix=("vix_lvl", "mean") if "vix_lvl" in q else ("spread", "size"),
                                       bce=("bce_facilite_depot_lvl", "mean") if "bce_facilite_depot_lvl" in q else ("spread", "size"),
                                       bund=("DE_taux_long_lvl", "mean") if "DE_taux_long_lvl" in q else ("spread", "size"),
                                       **{c: (c, "last") for c in q.columns if c.startswith("gov_")})
    agg = agg.reset_index()
    out = []
    for c, g in agg.groupby("pays"):
        g = g.sort_values("q").copy()
        g["d_spread"] = g.spread.diff()
        g["y"] = g.spread.shift(-1) - g.spread
        g["d_bund"] = g.bund.diff()
        for p in PANEL:
            g[f"is_{p}"] = float(p == c)
        out.append(g)
    A = pd.concat(out).set_index("q")
    m0 = ["d_spread", "spread", "d_bund", "vix", "bce"] + [f"is_{p}" for p in PANEL]
    gov_cols = [c for c in A.columns if c.startswith("gov_")]
    m1 = m0 + gov_cols
    A = A.dropna(subset=["y"] + m0)
    quarters = sorted(x for x in A.index.unique() if x >= pd.Period(test_start, "Q"))
    rows = []
    for model in ("ridge", "rf", "xgb"):
        res = {}
        for name, cols in (("M0", m0), ("M1", m1)):
            recs = []
            for qq in quarters:
                train = A[A.index < qq].dropna(subset=["y"])
                fit = make_model(model).fit(train[cols], train.y)
                te = A[A.index == qq]
                for (_, r), pv in zip(te.iterrows(), fit.predict(te[cols])):
                    recs.append({"q": str(qq), "pays": r.pays, "y": r.y, "pred": pv,
                                 "moyenne": train.loc[train.pays == r.pays, "y"].mean()})
            res[name] = pd.DataFrame(recs)
        a, b = res["M0"], res["M1"]
        la = a.assign(l=(a.y - a.pred) ** 2).groupby("q").l.sum()
        lb = b.assign(l=(b.y - b.pred) ** 2).groupby("q").l.sum()
        lz = b.assign(l=b.y ** 2).groupby("q").l.sum()
        stat, p = dm_pvalue(la.values, lb.values)
        r2 = lambda x: (1 - ((x.y - x.pred) ** 2).sum() / ((x.y - x.moyenne) ** 2).sum()) * 100
        rows.append({"extension": "E15 panel trimestriel", "cible": "Δ spread trimestriel (5 pays)",
                     "comparaison": f"{model} : M1 vs M0", "n_test": len(b),
                     "R2oos_sans_%": r2(a), "R2oos_avec_%": r2(b),
                     "gain_vs_marche_aleatoire_avec_%": (1 - lb.sum() / lz.sum()) * 100,
                     "DM": stat, "p_avec_meilleur": p,
                     "note": f"test {quarters[0]} → {quarters[-1]}"})
        print(f"  E15 {model} : terminé", flush=True)
    out = pd.DataFrame(rows).round(3)
    out.to_csv(TAB / "E15.csv", index=False)
    return out


if __name__ == "__main__":
    todo = sys.argv[1:] or ["E15", "E16"]
    t0 = time.time()
    df = build_monthly()
    print(f"Panel mensuel : {df.shape[0]} lignes, {df.shape[1]} colonnes, pays {sorted(df.pays.unique())}", flush=True)
    pd.set_option("display.width", 250)
    if "E15" in todo:
        print(e15(df).to_string(index=False))
    if "E16" in todo:
        print(e16_summary(e16(df)).to_string(index=False))
    print(f"Durée : {time.time() - t0:.0f} s")
