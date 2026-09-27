"""
14_more_extensions.py
Extensions E17 à E20 (pré-enregistrées le 27/09/2026 à 13h03, commit 79c7a4c) et E14 (étude d'événement).
Protocoles : docs/plan_extensions.md. Tous les résultats sont écrits, favorables ou non.

Usage : python src/14_more_extensions.py [E17] [E18] [E19] [E20] [E14]
puis   : python src/06_extensions.py resume   (correction Benjamini-Hochberg sur toutes les extensions)
"""
import importlib.util
from pathlib import Path
import sys
import time
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
SRC = Path(__file__).parent


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, SRC / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


X = _load("ext06", "06_extensions.py")     # France mensuel : walk_forward, compare, reg_model, load
P = _load("pan11", "11_panel_models.py")    # panel : build_monthly, gov_quarterly, make_model, dm_pvalue
TAB = Path("results/tables/extensions")
MORE = Path("data/raw/more")
PANEL = P.PANEL
MODELS = ("ridge", "rf", "xgb")


def panel_compare(ext, cible, label, a, b, period_col, note=""):
    """a, b : prévisions (y, pred, moyenne) sans / avec finances publiques ; DM sur la perte sommée sur les pays."""
    la = a.assign(l=(a.y - a.pred) ** 2).groupby(period_col).l.sum()
    lb = b.assign(l=(b.y - b.pred) ** 2).groupby(period_col).l.sum()
    lz = b.assign(l=b.y ** 2).groupby(period_col).l.sum()
    stat, p = P.dm_pvalue(la.values, lb.values)
    _, p_rw = P.dm_pvalue(lz.values, lb.values)
    r2 = lambda x: (1 - ((x.y - x.pred) ** 2).sum() / ((x.y - x.moyenne) ** 2).sum()) * 100
    rw = lambda x: (1 - ((x.y - x.pred) ** 2).sum() / (x.y ** 2).sum()) * 100
    return {"extension": ext, "cible": cible, "comparaison": label, "n_test": len(b),
            "R2oos_sans_%": r2(a), "R2oos_avec_%": r2(b),
            "gain_vs_marche_aleatoire_sans_%": rw(a), "gain_vs_marche_aleatoire_avec_%": rw(b),
            "DM": stat, "p_avec_meilleur": p, "p_avec_bat_marche_aleatoire": p_rw, "note": note}


def panel_walk(A, period_col, periods, cols, model, target="y"):
    recs = []
    for per in periods:
        tr = A[A[period_col] < per].dropna(subset=[target])
        fit = P.make_model(model).fit(tr[cols], tr[target])
        te = A[A[period_col] == per]
        for (_, r), pv in zip(te.iterrows(), fit.predict(te[cols])):
            recs.append({period_col: per, "pays": r.pays, "y": r[target], "pred": pv,
                         "moyenne": tr.loc[tr.pays == r.pays, target].mean()})
    return pd.DataFrame(recs)


# ---------------------------------------------------------------------------
# E17 : panel annuel (valeurs de décembre)
# ---------------------------------------------------------------------------
def e17(df):
    gov = P.gov_quarterly()
    rows_ = []
    for c in PANEL:
        d = df[df.pays == c]
        dec = d[d.index.month == 12]
        a = pd.DataFrame({"annee": dec.index.year, "spread": dec.spread.values,
                          "bund": dec["DE_taux_long_lvl"].values, "vix": dec["vix_lvl"].values,
                          "bce": dec["bce_facilite_depot_lvl"].values})
        a["pays"] = c
        a["d_spread"] = a.spread.diff()
        a["d_bund"] = a.bund.diff()
        a["y"] = a.spread.shift(-1) - a.spread
        g = gov[gov.geo == c].drop(columns="geo")
        q2 = g[g.index.quarter == 2].copy()                  # T2 de l'année t : connu fin décembre t
        q2["gov_d_solde_pct"] = q2["gov_solde_pct_depenses"].diff()
        q2.index = q2.index.year
        a = a.merge(q2, left_on="annee", right_index=True, how="left")
        for p in PANEL:
            a[f"is_{p}"] = float(p == c)
        rows_.append(a)
    A = pd.concat(rows_, ignore_index=True)
    m0 = ["spread", "d_spread", "d_bund", "vix", "bce"] + [f"is_{p}" for p in PANEL]
    govc = [c for c in A.columns if c.startswith("gov_")]
    A = A.dropna(subset=m0 + ["y"] + govc)
    origins = list(range(2010, 2025))
    out = []
    for m in MODELS:
        a = panel_walk(A, "annee", origins, m0, m)
        b = panel_walk(A, "annee", origins, m0 + govc, m)
        out.append(panel_compare("E17 panel annuel", "Δ spread annuel (5 pays)", f"{m} : M1 vs M0", a, b, "annee",
                                 note=f"origines 2010-2024 ; entraînement dès {A.annee.min()}"))
        print(f"  E17 {m} : terminé", flush=True)
    return out


# ---------------------------------------------------------------------------
# E18 : régime de crise (trimestriel, fin de trimestre) — exploratoire
# ---------------------------------------------------------------------------
def e18(df):
    q = df.copy()
    q["q"] = q.index.asfreq("Q")
    agg = q.groupby(["pays", "q"]).agg(spread=("spread", "last"), bund=("DE_taux_long_lvl", "last"),
                                       vix=("vix_lvl", "mean"), bce=("bce_facilite_depot_lvl", "mean"),
                                       **{c: (c, "last") for c in q.columns if c.startswith("gov_")}).reset_index()
    parts = []
    for c, g in agg.groupby("pays"):
        g = g.sort_values("q").copy()
        g["d_spread"] = g.spread.diff()
        g["d_bund"] = g.bund.diff()
        g["y"] = g.spread.shift(-1) - g.spread
        for p in PANEL:
            g[f"is_{p}"] = float(p == c)
        parts.append(g)
    A = pd.concat(parts, ignore_index=True)
    A["tension"] = (A.spread > 200).astype(float)
    govc = [c for c in A.columns if c.startswith("gov_")]
    for c in govc:
        A[f"{c}_x_tension"] = A[c] * A.tension
    m0 = ["d_spread", "spread", "d_bund", "vix", "bce", "tension"] + [f"is_{p}" for p in PANEL]
    m1 = m0 + govc + [f"{c}_x_tension" for c in govc]
    A = A.dropna(subset=m0 + ["y"])
    quarters = sorted(x for x in A.q.unique() if x >= pd.Period("2010Q1", "Q"))
    out = []
    for m in MODELS:
        a = panel_walk(A, "q", quarters, m0, m)
        b = panel_walk(A, "q", quarters, m1, m)
        out.append(panel_compare("E18 régime de crise (exploratoire)", "Δ spread trimestriel fin de trimestre (5 pays)",
                                 f"{m} : M1 vs M0", a, b, "q", note="test 2010T1+ (tension : spread > 200 pb)"))
        cut = pd.Period("2015Q1", "Q")
        for lab, fa, fb in (("2010-2014", a[a.q < cut], b[b.q < cut]), ("2015+", a[a.q >= cut], b[b.q >= cut])):
            r = panel_compare("E18 ventilation (hors correction)", "Δ spread trimestriel fin de trimestre (5 pays)",
                              f"{m} : M1 vs M0, {lab}", fa, fb, "q", note="sous-période, hors correction BH")
            out.append(r)
        print(f"  E18 {m} : terminé", flush=True)
    return out


# ---------------------------------------------------------------------------
# E19 : actions sectorielles (France)
# ---------------------------------------------------------------------------
def e19(df):
    px = pd.read_csv(MORE / "actions_mensuel.csv", index_col="mois")
    ret = px.pct_change() * 100
    baskets = {"btp_concessions": ["vinci", "eiffage", "bouygues"], "defense": ["thales", "dassault_aviation"]}
    d = df.copy()
    out = []
    for bname, members in baskets.items():
        exc = ret[members].mean(axis=1) - ret["cac40"]
        d[f"{bname}_exc"] = exc
        d[f"{bname}_exc_l1"] = exc.shift(1)
        d[f"y_{bname}_h1"] = exc.shift(-1)
        d[f"y_{bname}_h3"] = exc[::-1].rolling(3).sum()[::-1].shift(-1)
        own = [f"{bname}_exc", f"{bname}_exc_l1"]
        for h in (1, 3):
            for m in MODELS:
                a = X.walk_forward(d, f"y_{bname}_h{h}", X.MARKETS + own, lambda: X.reg_model(m), h=h)
                b = X.walk_forward(d, f"y_{bname}_h{h}", X.MARKETS + own + X.SPENDING, lambda: X.reg_model(m), h=h)
                out.append(X.compare("E19 actions sectorielles", f"{bname} (excès CAC 40)", f"{m} h={h} : M1 vs M0",
                                     a, b, h=h))
            print(f"  E19 {bname} h={h} : terminé", flush=True)
    return out


# ---------------------------------------------------------------------------
# E20 : incertitude de politique économique (Baker, Bloom et Davis)
# ---------------------------------------------------------------------------
def e20(df):
    f = MORE / "epu_FRAEPUINDXM.csv"
    if not f.exists():  # écart déclaré dans docs/plan_extensions.md : indice européen
        f = MORE / "epu_EUEPUINDXM.csv"
    e = pd.read_csv(f, index_col="date", parse_dates=True).iloc[:, 0]
    e.index = e.index.to_period("M").astype(str)
    d = df.copy()
    d["epu_log"] = np.log(e).shift(1).reindex(d.index)       # publié début du mois suivant
    out = []
    for t in X.TARGETS:
        for m in MODELS:
            m0 = X.walk_forward(d, t, X.MARKETS, lambda: X.reg_model(m))
            m0e = X.walk_forward(d, t, X.MARKETS + ["epu_log"], lambda: X.reg_model(m))
            m1e = X.walk_forward(d, t, X.MARKETS + ["epu_log"] + X.SPENDING, lambda: X.reg_model(m))
            out.append(X.compare("E20a incertitude politique", t, f"{m} : M0+EPU vs M0", m0, m0e))
            out.append(X.compare("E20b dépenses + incertitude", t, f"{m} : M1+EPU vs M0+EPU", m0e, m1e))
        print(f"  E20 {t} : terminé", flush=True)
    return out


RUN = {"E17": ("panel", e17), "E18": ("panel", e18), "E19": ("france", e19), "E20": ("france", e20)}

if __name__ == "__main__":
    todo = sys.argv[1:] or list(RUN)
    t0 = time.time()
    data = {}
    pd.set_option("display.width", 250)
    for key in todo:
        kind, fn = RUN[key]
        if kind not in data:
            data[kind] = P.build_monthly() if kind == "panel" else X.load()
        rows = fn(data[kind])
        res = pd.DataFrame(rows).round(3)
        res.to_csv(TAB / f"{key}.csv", index=False)
        cols = [c for c in ["comparaison", "n_test", "R2oos_sans_%", "R2oos_avec_%", "gain_vs_marche_aleatoire_avec_%",
                            "p_avec_meilleur", "p_avec_bat_moyenne", "p_avec_bat_marche_aleatoire"] if c in res]
        print(res[["extension", "cible"] + cols].to_string(index=False), flush=True)
    print(f"Durée : {time.time() - t0:.0f} s")
