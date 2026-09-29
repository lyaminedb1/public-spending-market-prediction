"""
20_limites_chiffres.py
Reproduit par script les chiffres cités comme limites dans CLAUDE.md / la Discussion :
  1. variance des écarts `_ytd_gap` selon le mois de l'année (revendiqué : x6 de janvier à décembre) ;
  2. effectifs d'entraînement et de test ;
  3. E16 : séries de la base élargie arrêtées avant la fin de la période, part de valeurs imputées en fin de test ;
  4. autocorrélation d'ordre 1 des cibles (moyennes mensuelles pour les taux) ;
  5. puissance du test (extrait de diag_04/resume.csv).

Sortie : results/tables/limites_chiffres.csv  (limite, cible, valeur, unite, texte, source)
Usage  : python src/20_limites_chiffres.py     (~1 min)
"""
import importlib.util
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf

warnings.filterwarnings("ignore")
SRC = Path(__file__).parent
TAB = Path("results/tables")


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, SRC / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


B, M, P = load("b02", "02_build_dataset.py"), load("m04", "04_models.py"), load("p11", "11_panel_models.py")
rows = []


def add(limite, valeur, unite="", cible="", texte="", source=""):
    rows.append({"limite": limite, "cible": cible, "valeur": valeur, "unite": unite, "texte": texte, "source": source})


# ------------------------------------------------------------------ 1. variance des ytd_gap selon le mois
bud = B.build_budget()
cols = [c for c in bud.columns if c.endswith("_ytd_gap") and c.startswith(("dep_", "psr_"))]
sd = bud[cols].groupby(bud.index.month).std()
ratio = sd.loc[12] / sd.loc[1]
for c in cols:
    add("écart-type de l'écart YTD : décembre / janvier", float(ratio[c]), "rapport", c.replace("_ytd_gap", ""),
        source="02_build_dataset.build_budget")
add("écart-type de l'écart YTD : décembre / janvier (médiane des 7 lignes)", float(ratio.median()), "rapport",
    texte=f"min {ratio.min():.1f} ; max {ratio.max():.1f} ; revendiqué : environ x6", source="02_build_dataset.build_budget")


def ytd_gap(flow):
    cum = flow.groupby(flow.index.year).cumsum()
    return (cum - cum.shift(12)) / flow.rolling(12).sum().abs() * 100


# témoin : flux mensuels i.i.d. de même moyenne et de même dispersion que « dépenses totales » ; sous l'hypothèse
# nulle (aucune saisonnalité de variance), la variance d'un écart de cumuls croît linéairement avec le mois
# -> rapport attendu sqrt(12) = 3,46 pour decembre / janvier
rng = np.random.default_rng(0)
idx = pd.period_range("2013-01", "2026-07", freq="M")
tot = bud["dep_totales_12m"].dropna()
mu, sig = float(tot.mean() / 12), float(tot.std() / 12)
rat = []
for _ in range(300):
    g = ytd_gap(pd.Series(rng.normal(mu, sig, len(idx)), index=idx))
    s = g.groupby(g.index.month).std()
    rat.append(s.loc[12] / s.loc[1])
add("témoin : flux i.i.d., écart-type décembre / janvier (moyenne de 300 simulations)", float(np.mean(rat)), "rapport",
    texte=f"attendu sqrt(12) = {np.sqrt(12):.2f} : l'inflation de variance en fin d'année est en grande partie mécanique",
    source="simulation")

# ------------------------------------------------------------------ 2. effectifs
df = pd.read_csv(M.DATA, index_col="mois")
dfy = df.dropna(subset=list(M.TARGETS))
add("observations d'entraînement au premier mois de test", int((dfy.index < M.TEST_START).sum()), "mois",
    texte=f"premier mois de test {M.TEST_START}", source="dataset_monthly.csv")
last = dfy.index[-1]
add("observations d'entraînement au dernier mois de test", int((dfy.index < last).sum()), "mois",
    texte=f"dernier mois de test {last}", source="dataset_monthly.csv")
add("mois de test (04)", int((dfy.index >= M.TEST_START).sum()), "mois", source="dataset_monthly.csv")
ext = TAB / "extensions"
for f, lab, filt in (("E1.csv", "E1 h=3", "h=3"), ("E1.csv", "E1 h=6", "h=6"), ("E1.csv", "E1 h=12", "h=12"),
                     ("E4.csv", "E4", ""), ("E19.csv", "E19 h=1", "h=1"), ("E19.csv", "E19 h=3", "h=3"),
                     ("E15.csv", "E15 (trimestres x pays)", ""), ("E16.csv", "E16 (mois x pays)", ""),
                     ("E17.csv", "E17 (années x pays)", "")):
    d = pd.read_csv(ext / f)
    if filt:
        d = d[d.comparaison.str.contains(filt)]
    add(f"observations de test, {lab}", sorted(d.n_test.unique().tolist())[0], "observations",
        texte=f"valeurs distinctes : {sorted(d.n_test.unique().tolist())}", source=f"extensions/{f}")

# ------------------------------------------------------------------ 3. E16 : séries arrêtées et valeurs imputées
raw = pd.read_csv(P.BASE, index_col="mois")
raw.index = pd.PeriodIndex(raw.index, freq="M")
last_valid = raw.apply(lambda s: s.last_valid_index())
fin = raw.index.max()
add("E16 : séries dans la base élargie", int(raw.shape[1]), "séries", source="large/base_elargie_mensuelle.csv")
for lim in ("2024-06", "2025-01"):
    n = int((last_valid < pd.Period(lim, "M")).sum())
    add(f"E16 : séries dont la dernière valeur observée est antérieure à {lim}", n, "séries",
        texte=f"sur {raw.shape[1]} ; fin de la base {fin}", source="large/base_elargie_mensuelle.csv")
panel = P.build_monthly()
gov_cols = [c for c in panel.columns if "gov_" in c]
feats = [c for c in panel.columns if c not in ("y_level", "y_change", "pays")]
usable = panel[panel.index >= pd.Period("2002-01", "M")]
feats = [c for c in feats if usable[c].notna().mean() >= 0.7]
d = panel.dropna(subset=["y_level", "spread"])
d = d[d.index >= pd.Period("2002-01", "M")]
test = d[d.index >= pd.Period("2012-01", "M")].sort_index()
add("E16 : observations de test (mois x pays)", len(test), "observations", source="11_panel_models.build_monthly")
add("E16 : variables retenues (dont finances publiques)", len(feats), "variables",
    texte=f"dont finances publiques : {len(set(feats) & set(gov_cols))}", source="11_panel_models.build_monthly")
tail = test.iloc[-144:][feats]
add("E16 : part des cellules manquantes (donc imputées) sur les 144 dernières observations de test",
    float(tail.isna().mean().mean() * 100), "%", texte="moyenne de toutes les cellules", source="11_panel_models.build_monthly")
add("E16 : idem, médiane sur les lignes", float(tail.isna().mean(axis=1).median() * 100), "%", source="11_panel_models.build_monthly")
add("E16 : idem, médiane sur les variables", float(tail.isna().mean(axis=0).median() * 100), "%",
    texte="revendiqué : 23,6 % (médiane)", source="11_panel_models.build_monthly")

# ------------------------------------------------------------------ 4. autocorrélation d'ordre 1 des cibles
for t, x in (("y_d_spread", "d_spread"), ("y_d_oat", "d_oat"), ("y_cac_ret", "cac_ret")):
    s = df[x].dropna()
    add("autocorrélation d'ordre 1 de la variation mensuelle", float(acf(s, nlags=1)[1]), "corrélation", t,
        texte="taux : variations de MOYENNES mensuelles (autocorrélation en partie mécanique) ; CAC 40 : fin de mois",
        source="dataset_monthly.csv")

# ------------------------------------------------------------------ 5. puissance (diagnostics de la revue de 04)
res = TAB / "diag_04" / "resume.csv"
if res.exists():
    r = pd.read_csv(res)
    for rho in ("0.3", "0.5"):
        x = r[(r.bloc == "puissance") & r.cle.str.startswith(f"rho={rho} : % tirages où le modèle bat")]
        add(f"puissance : rho = {rho}, % de tirages où le modèle bat la moyenne (min-max sur les 3 cibles)",
            float(x.valeur.mean()), "%", texte=f"{x.valeur.min():.0f}-{x.valeur.max():.0f}", source="diag_04/resume.csv")

out = pd.DataFrame(rows)
out["valeur"] = out["valeur"].astype(float).round(3)
out.to_csv(TAB / "limites_chiffres.csv", index=False)
pd.set_option("display.width", 220)
pd.set_option("display.max_colwidth", 95)
print(out[["limite", "cible", "valeur", "unite", "texte"]].to_string(index=False))
