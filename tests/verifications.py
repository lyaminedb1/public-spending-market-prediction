"""
tests/verifications.py
Contrôles automatiques de la préparation des données (revue du 27/09/2026).

Chaque contrôle affiche OK ou ÉCHEC. Le script s'arrête avec un code d'erreur si un contrôle échoue.
À lancer depuis la racine du dépôt, après `python src/02_build_dataset.py` et `python src/05_extra_features.py` :
    python tests/verifications.py

Ce qui est vérifié :
  A. Données budgétaires brutes : pas de doublon, pas de mois manquant, soldes annuels officiels.
  B. Jeu de données France : cibles = mois suivant, budget = mois t-2, inflation = mois t-1.
  C. Variables E4/E13 : surprise budgétaire décalée de 2 mois, notations cohérentes.
  D. Panel (E15-E18) : finances publiques du trimestre q utilisées à partir de q+2 ;
     E16 : production et chômage décalés de 2 mois, autres variables macro d'1 mois.
  E. E19 : le dernier mois des actions est retiré s'il est incomplet.
"""
import importlib.util
from pathlib import Path
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
SRC = Path("src")
sys.path.insert(0, str(SRC))
RESULTS = []

# Les contrôles portent sur les données, pas sur les modèles : si XGBoost ne se charge pas
# (ex. Mac sans libomp), on le remplace par un module vide pour pouvoir importer les scripts.
try:
    import xgboost  # noqa: F401
except Exception:
    import types
    _fake = types.ModuleType("xgboost")
    _fake.XGBRegressor = _fake.XGBClassifier = None
    sys.modules["xgboost"] = _fake
    print("(XGBoost indisponible sur cette machine : ignoré, inutile pour ces contrôles)\n")


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, SRC / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check(label, ok, detail=""):
    RESULTS.append(bool(ok))
    print(f"  {'OK    ' if ok else 'ÉCHEC '} {label}" + (f"  ({detail})" if detail else ""))


def contiguous(index):
    p = pd.PeriodIndex(index, freq="M")
    return bool((np.diff(p.asi8) == 1).all())


# ---------------------------------------------------------------------------
print("0. Gel des données brutes (data/MANIFEST.csv)")
sys.path.insert(0, "tests")
import data_manifest  # noqa: E402
ecarts = data_manifest.check()
check("données brutes identiques au manifeste (aucun fichier ajouté, retiré ou modifié)", not ecarts,
      "; ".join(ecarts[:3]))

# ---------------------------------------------------------------------------
print("A. Données budgétaires brutes")
B = load("b02", "02_build_dataset.py")
for f in B.BUDGET_FILES:
    raw = pd.read_csv(B.RAW / "budget" / f, sep=";", encoding="utf-16", decimal=",")
    lignes = raw.dropna(subset=["Ligne d'information"])["Ligne d'information"].str.strip()
    dup = [k for k in B.BUDGET_LINES if (lignes == k).sum() != 1]
    check(f"chaque ligne retenue apparaît une seule fois — {f}", not dup, f"problème : {dup}" if dup else "")
parts = [B.read_budget_file(B.RAW / "budget" / f) for f in B.BUDGET_FILES]
cumul = pd.concat(parts).sort_index()
cumul = cumul[~cumul.index.duplicated(keep="last")][list(B.BUDGET_LINES)].rename(columns=B.BUDGET_LINES) / 1e9
check("mois budgétaires contigus", contiguous(cumul.index), f"{cumul.index.min()} → {cumul.index.max()}")
check("aucune valeur budgétaire manquante", cumul.isna().sum().sum() == 0)
officiels = {2014: -85.6, 2020: -178.1, 2023: -173.0, 2024: -155.9}
ecarts = {a: round(cumul.loc[pd.Period(f"{a}-12", "M"), "solde"] - v, 2) for a, v in officiels.items()}
check("soldes annuels = chiffres officiels (±0,1 Md€)", all(abs(e) <= 0.1 for e in ecarts.values()), f"écarts {ecarts}")

# ---------------------------------------------------------------------------
print("B. Jeu de données France (data/processed/dataset_monthly.csv)")
d = pd.read_csv("data/processed/dataset_monthly.csv", index_col="mois")
check("mois contigus", contiguous(d.index), f"{d.index[0]} → {d.index[-1]}, {len(d)} mois")
for y, x in [("y_d_spread", "d_spread"), ("y_d_oat", "d_oat"), ("y_cac_ret", "cac_ret")]:
    err = np.nanmax(np.abs(d[y].iloc[:-1].values - d[x].iloc[1:].values))
    check(f"{y}(t) = {x}(t+1) : la cible est bien le mois suivant", err < 1e-9, f"écart max {err:.2e}")
cibles = ["y_d_spread", "y_d_oat", "y_cac_ret"]
check("seule la dernière ligne n'a pas de cible", d[cibles].iloc[:-1].notna().all().all() and d[cibles].iloc[-1].isna().all())
up_ok = ((d.y_spread_up == 1) == (d.y_d_spread > 0))[d.y_d_spread.notna()].all()
check("y_spread_up = 1 si et seulement si le spread monte", up_ok)
bud = B.build_budget()
idx = pd.PeriodIndex(d.index, freq="M")
b_cols = [c for c in bud.columns]
attendu = bud.reindex(idx - B.BUDGET_LAG)
ecart = np.nanmax(np.abs(d[[f"b_{c}" for c in b_cols]].values - attendu.values))
check(f"toutes les variables b_ = budget du mois t-{B.BUDGET_LAG}", ecart < 1e-9, f"écart max {ecart:.2e}")
check(f"b_source_month = t-{B.BUDGET_LAG}", (d.b_source_month == (idx - B.BUDGET_LAG).astype(str)).all())
# variantes de robustesse du décalage budgétaire (dataset_monthly_lagN.csv, produites par 02 --lag N)
for f in sorted(Path("data/processed").glob("dataset_monthly_lag*.csv")):
    n = int(f.stem.split("lag")[-1])
    dn = pd.read_csv(f, index_col="mois")
    ixn = pd.PeriodIndex(dn.index, freq="M")
    ecart_n = np.nanmax(np.abs(dn[[f"b_{c}" for c in b_cols]].values - bud.reindex(ixn - n).values))
    check(f"{f.name} : budget = mois t-{n}", ecart_n < 1e-9 and (dn.b_source_month == (ixn - n).astype(str)).all(),
          f"écart max {ecart_n:.2e}")
    m_ = dn.index.intersection(d.index)
    marche = [c for c in d.columns if not c.startswith("b_")]
    check(f"{f.name} : variables de marché identiques au jeu principal",
          np.nanmax(np.abs(dn.loc[m_, marche].values - d.loc[m_, marche].values)) < 1e-12)
mk = B.build_markets()
infl_attendue = mk["inflation_yoy"].shift(1).reindex(idx)
ecart = np.nanmax(np.abs(d.inflation_yoy.values - infl_attendue.values))
check("inflation_yoy(t) = inflation du mois t-1 (publication mi-t+1)", ecart < 1e-9, f"écart max {ecart:.2e}")
na_mid = d.iloc[:-1].isna().sum().sum()
check("aucune valeur manquante hors dernière ligne (validation glissante qui compte en lignes)", na_mid == 0)

# ---------------------------------------------------------------------------
print("C. Variables E4 / E13 (data/processed/extra_features.csv)")
E = load("e05", "05_extra_features.py")
x = pd.read_csv("data/processed/extra_features.csv", index_col="mois")
check("mêmes mois que le jeu principal", list(x.index) == list(d.index))
s = E.surprise()
attendu = s.reindex(idx)
ecart = np.nanmax(np.abs(x[attendu.columns].values - attendu.values))
check("surprise budgétaire alignée (décalage de 2 mois déjà appliqué dans surprise())", ecart < 1e-9)
brut = s.copy()
brut.index = brut.index - E.BUDGET_LAG
check("surprise de la ligne t = données du mois t-2", brut.index.min() == pd.Period("2013-01", "M") and s.index.min() == pd.Period("2013-03", "M"),
      f"premier mois source {brut.index.min()}, première ligne {s.index.min()}")
ev = pd.read_csv("data/raw/ratings_france.csv")
check("9 dégradations de notation dans le fichier", len(ev) == 9, f"{len(ev)} lignes")
check("notation moyenne entre 0 et 4 crans sous AAA", x.rating_crans_moyen.between(0, 4).all(),
      f"min {x.rating_crans_moyen.min():.2f}, max {x.rating_crans_moyen.max():.2f}")

# ---------------------------------------------------------------------------
print("D. Panel européen (E15-E18) et base élargie (E16)")
P = load("p11", "11_panel_models.py")
panel = P.build_monthly()
gov = P.gov_quarterly()
fr = panel[panel.pays == "FR"]
g = gov[gov.geo == "FR"].drop(columns="geo")
col = "gov_TE_yoy"
ok, n = True, 0
for m in fr.index[fr.index >= pd.Period("2005-01", "M")]:
    q_source = m.asfreq("Q") - 2
    if q_source in g.index and not np.isnan(fr.loc[m, col]):
        ok &= abs(fr.loc[m, col] - g.loc[q_source, col]) < 1e-9
        n += 1
check("finances publiques du trimestre q utilisées à partir de q+2", ok and n > 0, f"{n} mois contrôlés")
raw = pd.read_csv(P.BASE, index_col="mois")
raw.index = pd.PeriodIndex(raw.index, freq="M")
cas = {"FR_production_ind": 2, "FR_chomage": 2, "zone_euro_chomage": 2, "FR_ipch": 1,
       "FR_confiance_menages": 1, "us_inflation": 1, "FR_taux_long": 0, "vix": 0}
for name, lag in cas.items():
    if name not in raw:
        continue
    ref = P.transform(raw[name], name)          # transformation + décalage du code
    key = next(iter(ref))                        # "yoy", "r1" ou "lvl"
    s0 = raw[name]
    # valeur attendue : transformation calculée à la main, puis décalée de `lag` mois
    if name.split("_", 1)[-1] in P.YOY or name in P.YOY:
        brut_t = (s0 / s0.shift(12) - 1) * 100
    elif name.split("_", 1)[-1] in P.LOGRET or name in P.LOGRET:
        brut_t = np.log(s0).diff() * 100
    else:
        brut_t = s0
    diff = (ref[key] - brut_t.shift(lag)).abs().max()
    check(f"E16 : {name} décalé de {lag} mois", diff < 1e-9 or np.isnan(diff), f"écart max {diff:.2e}")

# ---------------------------------------------------------------------------
print("E. Actions sectorielles (E19)")
q = pd.read_csv("data/raw/more/actions_quotidien.csv", index_col="date", parse_dates=True)
M14 = load("m14", "14_more_extensions.py")
px = M14.actions_mensuelles()
dernier_mois = pd.Period(px.index.max(), "M")
jours = q[q.index.to_period("M") == dernier_mois].index
dernier_ouvre = dernier_mois.to_timestamp() + pd.offsets.BMonthEnd(0)   # dernier jour ouvré du mois
# tolérance d'1 jour ouvré pour un jour férié en fin de mois (ex. Vendredi saint le 29/03/2024)
complet = len(jours) > 0 and jours.max() >= dernier_ouvre - pd.offsets.BDay(1)
check("dernier mois utilisé pour E19 complet (données jusqu'à la fin du mois)", complet,
      f"dernier jour de données {q.index.max().date()}, dernier mois utilisé {dernier_mois} (dernier jour {jours.max().date()})")
e19 = pd.read_csv("results/tables/extensions/E19.csv")
n1 = e19[e19.comparaison.str.contains("h=1")].n_test.unique().tolist()
n3 = e19[e19.comparaison.str.contains("h=3")].n_test.unique().tolist()
check("E19 : 79 mois de test à h=1 (2020-01 → 2026-07, protocole)", n1 == [79], f"n_test h=1 {n1}, h=3 {n3}")

# ---------------------------------------------------------------------------
print("F. Prévisions de 04 (results/tables/models_predictions_*.csv)")
M4 = load("m04", "04_models.py")
X6 = load("x06", "06_extensions.py")
met = pd.read_csv("results/tables/models_metrics.csv")
main_ds = pd.read_csv("data/processed/dataset_monthly.csv", index_col="mois")
for t in M4.TARGETS:
    pr = pd.read_csv(f"results/tables/models_predictions_{t}.csv", index_col=0)
    check(f"{t} : 79 mois de test contigus 2020-01 → 2026-07",
          len(pr) == 79 and pr.index[0] == "2020-01" and pr.index[-1] == "2026-07" and contiguous(pr.index),
          f"{len(pr)} lignes, {pr.index[0]} → {pr.index[-1]}")
    check(f"{t} : aucune valeur manquante dans les prévisions", not pr.isna().any().any())
    check(f"{t} : y_true = cible du jeu de données", np.nanmax(np.abs(pr.y_true.values - main_ds.loc[pr.index, t].values)) < 1e-9)
    ecart = 0.0
    for c in pr.columns.drop("y_true"):
        mod, _, fs = c.partition("|")
        ref = met[(met.cible == t) & (met.modele == mod) & (met.variables == (fs or "—"))]["R2_oos_%"].iloc[0]
        val = (1 - ((pr.y_true - pr[c]) ** 2).sum() / ((pr.y_true - pr.naif_moyenne) ** 2).sum()) * 100
        ecart = max(ecart, abs(ref - val))
    check(f"{t} : R² de models_metrics.csv recalculé depuis les prévisions", ecart < 1e-2, f"écart max {ecart:.1e} (arrondi)")

print("G. Réglage de Ridge (grille RidgeCV)")
P11 = load("p11", "11_panel_models.py")
g04 = M4.make_model("ridge")[-1].alphas
g06 = X6.reg_model("ridge")[-1].alphas
g11 = P11.make_model("ridge")[-1].alphas
check("grille de Ridge : 04 = 06, maximum >= 10^6", np.allclose(g04, g06) and g04.max() >= 1e6, f"maximum {g04.max():.0e}")
check("grille de Ridge (panel 11) : maximum >= 10^4", g11.max() >= 1e4, f"maximum {g11.max():.0e}")
alpha = pd.read_csv("results/tables/diag_04/alpha_bornes_apres.csv")
for t in ("y_d_spread", "y_d_oat"):
    part = alpha[(alpha.script.astype(str).str.zfill(2) == "04") & (alpha.cible == t)].borne_haute.mean() * 100
    check(f"{t} : alpha à la borne haute dans moins de 10 % des mois (04)", part < 10, f"{part:.1f} %")

print("H. Extensions : fichiers et p-values")
EXT = Path("results/tables/extensions")
attendus = ["E1", "E2", "E3", "E4", "E5", "E6", "E7E8", "E9", "E10", "E11", "E12", "E13", "E15", "E16", "E17", "E18", "E19", "E20"]
manque = [k for k in attendus if not (EXT / f"{k}.csv").exists()]
check("un fichier de résultats par extension (E1…E20 sauf E14, non exécutée)", not manque, f"manquants : {manque}")
hors = []
for k in attendus:
    e = pd.read_csv(EXT / f"{k}.csv")
    for c in [c for c in e.columns if c.startswith("p_") and e[c].dtype != object]:
        if ((e[c] < 0) | (e[c] > 1)).any():
            hors.append((k, c))
check("toutes les p-values dans [0, 1]", not hors, f"{hors}" if hors else "")
files = sorted(f for f in EXT.glob("E*.csv") if "_" not in f.stem)
summ = pd.read_csv("results/tables/ext_summary.csv")
check("ext_summary.csv = concaténation des fichiers d'extensions", len(summ) == sum(len(pd.read_csv(f)) for f in files),
      f"{len(summ)} comparaisons")
bh = summ.dropna(subset=["p_BH"])
check("p corrigée BH >= p brute", (bh.p_BH >= bh.p_avec_meilleur - 1e-3).all(), f"{len(bh)} comparaisons corrigées (E12 et ventilations exclues)")

print("I. Cohérence entre 04, 06 et 11")
check("mêmes variables MARKETS et SPENDING dans 04 et 06", M4.MARKETS == X6.MARKETS and M4.SPENDING == X6.SPENDING)
check("même début de test dans 04 et 06 (config.py)", M4.TEST_START == X6.TEST_START == "2020-01")


def params(model):
    est = model[-1] if hasattr(model, "steps") else model
    p = est.get_params()
    return {k: v for k, v in p.items() if k not in ("n_jobs", "alphas", "verbosity")}


for name in ("rf", "xgb"):
    a, b, c = params(M4.make_model(name)), params(X6.reg_model(name)), params(P11.make_model(name))
    check(f"hyperparamètres {name} identiques dans 04, 06 et 11", a == b == c,
          "" if a == b == c else f"différences : {[k for k in a if a[k] != b.get(k) or a[k] != c.get(k)]}")

print("J. Extensions lisant les prévisions de 04 (E7, E8, E12) : à jour")
for t in ("y_d_spread",):
    pr = pd.read_csv(f"results/tables/models_predictions_{t}.csv", index_col=0)
    base = lambda col: pd.DataFrame({"y": pr.y_true, "pred": pr[col], "moyenne": pr.naif_moyenne})
    a, b = base("ridge|M0 marchés"), base("ridge|M1 + dépenses")
    a.pred, b.pred = 0.5 * a.pred + 0.5 * a.moyenne, 0.5 * b.pred + 0.5 * b.moyenne
    ref = X6.compare("E7", t, "x", a, b)
    e78 = pd.read_csv(EXT / "E7E8.csv")
    row = e78[(e78.cible == t) & e78.comparaison.str.startswith("ridge 50/50")].iloc[0]
    check("E7 (Ridge, spread) = recalcul depuis les prévisions de 04",
          abs(row["R2oos_sans_%"] - ref["R2oos_sans_%"]) < 0.01 and abs(row["R2oos_avec_%"] - ref["R2oos_avec_%"]) < 0.01,
          f"R² sans/avec fichier {row['R2oos_sans_%']:.2f}/{row['R2oos_avec_%']:.2f} ; recalculé {ref['R2oos_sans_%']:.2f}/{ref['R2oos_avec_%']:.2f}")
    e12 = pd.read_csv(EXT / "E12.csv")
    q = pr[pr.index < "2022-01"]
    a12 = pd.DataFrame({"y": q.y_true, "pred": q["ridge|M0 marchés"], "moyenne": q.naif_moyenne})
    b12 = pd.DataFrame({"y": q.y_true, "pred": q["ridge|M1 + dépenses"], "moyenne": q.naif_moyenne})
    ref12 = X6.compare("E12", t, "x", a12, b12)
    r12 = e12[(e12.cible == t) & e12.comparaison.str.startswith("ridge [2020-2021]")].iloc[0]
    check("E12 (Ridge, spread, 2020-2021) = recalcul depuis les prévisions de 04",
          abs(r12["R2oos_sans_%"] - ref12["R2oos_sans_%"]) < 0.01 and abs(r12["R2oos_avec_%"] - ref12["R2oos_avec_%"]) < 0.01,
          f"fichier {r12['R2oos_avec_%']:.2f} ; recalculé {ref12['R2oos_avec_%']:.2f}")

print("K. Tests de non-fuite de walk_forward (tests/test_walk_forward_06.py)")
import subprocess
r = subprocess.run([sys.executable, "tests/test_walk_forward_06.py"], capture_output=True, text=True)
check("walk_forward de 06 : mois calendaires, cibles à horizon h, détection d'une fuite", r.returncode == 0,
      r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()[-200:])

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
n_ok, n_tot = sum(RESULTS), len(RESULTS)
print(f"\n{n_ok}/{n_tot} contrôles réussis")
sys.exit(0 if n_ok == n_tot else 1)
