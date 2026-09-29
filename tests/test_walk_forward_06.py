"""
Contrôles de walk_forward (src/06_extensions.py) : entraînement en mois calendaires, fenêtre, cibles à horizon h.
  python tests/test_walk_forward_06.py
Sortie : liste OK/ÉCHEC ; code de sortie 1 si un contrôle échoue.
"""
import importlib.util
import inspect
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


def synthetic(gaps=()):
    idx = pd.period_range("2014-01", "2025-12", freq="M")
    rng = np.random.default_rng(0)
    df = pd.DataFrame({"x1": rng.standard_normal(len(idx)), "y": rng.standard_normal(len(idx))},
                      index=idx.astype(str))
    for g in gaps:
        df.loc[g, "x1"] = np.nan
    return df


class Recorder:
    """Modèle factice : enregistre les mois d'entraînement de chaque appel à fit."""
    log = []

    def fit(self, Xt, y):
        Recorder.log.append(list(Xt.index))
        self.mu = float(np.mean(y))
        return self

    def predict(self, Xt):
        return np.full(len(Xt), self.mu)


def months(strs):
    return [pd.Period(s, "M") for s in strs]


def max_violation(walk, df, h, **kw):
    """Plus grand dépassement : (dernier mois d'entraînement + h) - mois de test, en mois. Doit être <= 0."""
    Recorder.log = []
    res = walk(df, "y", ["x1"], Recorder, h=h, **kw)
    worst = -10 ** 9
    for m, train in zip(res.index, Recorder.log):
        last = months(train)[-1]
        worst = max(worst, (last + h - pd.Period(m, "M")).n)
    return worst


print("A. walk_forward : jamais de mois d'entraînement dans le futur connu")
for label, gaps in (("sans trou", ()), ("2 mois manquants au milieu", ("2018-05", "2021-03"))):
    df = synthetic(gaps)
    for h in (1, 3, 6, 12):
        v = max_violation(X.walk_forward, df, h)
        check(f"{label}, h={h} : dernier mois d'entraînement + h <= mois de test", v <= 0, f"dépassement max {v}")

print("B. contrôle négatif : une version volontairement cassée doit être détectée")
src = inspect.getsource(X.walk_forward).replace("i - h + 1", "i - h + 2")
ns = dict(X.__dict__)
exec(src, ns)
v = max_violation(ns["walk_forward"], synthetic(), 3)
check("version cassée (i-h+2) : fuite détectée à h=3", v > 0, f"dépassement max {v}")

print("C. fenêtre glissante (window=60)")
Recorder.log = []
df = synthetic(("2018-05",))
X.walk_forward(df, "y", ["x1"], Recorder, h=1, window=60)
sizes = {len(t) for t in Recorder.log}
check("60 observations par fenêtre", sizes == {60}, f"tailles {sorted(sizes)}")
span = max((months(t)[-1] - months(t)[0]).n + 1 for t in Recorder.log)
print(f"       (avec un trou dans la série, la fenêtre couvre jusqu'à {span} mois calendaires : ce sont 60 observations)")

print("D. données réelles : trous internes après dropna, par configuration de variables")
real = X.load()
cfgs = {
    "M0": X.MARKETS, "M1": X.MARKETS + X.SPENDING, "réduit": X.REDUCED,
    "M1+surprise": X.MARKETS + X.SPENDING + X.SURPRISE, "M1+notations": X.MARKETS + X.RATINGS + X.SPENDING,
}
tot = 0
for t in ["y_d_spread", "y_d_oat", "y_cac_ret", "y_d_spread_h3", "y_d_oat_h6", "y_cac_ret_h12", "y_d_spread_abs"]:
    for name, cols in cfgs.items():
        d = real.dropna(subset=[t] + cols)
        full = pd.period_range(d.index[0], d.index[-1], freq="M")
        tot += len(full) - len(d)
check("aucun mois manquant à l'intérieur des séries utilisées", tot == 0, f"{tot} mois manquants au total")

print("E. cibles à horizon h = niveaux à t+h moins niveau à t")
lvl = real
for h in (3, 6, 12):
    s = (lvl.spread_bp.shift(-h) - lvl.spread_bp)
    o = (lvl.oat_10y.shift(-h) - lvl.oat_10y) * 100
    growth = (1 + lvl.cac_ret / 100)
    c = sum(np.log(growth.shift(-k)) for k in range(1, h + 1))
    c = (np.exp(c) - 1) * 100
    for name, ref, col in (("spread", s, f"y_d_spread_h{h}"), ("OAT", o, f"y_d_oat_h{h}"), ("CAC 40", c, f"y_cac_ret_h{h}")):
        m = ref.notna() & real[col].notna()
        e = (ref[m] - real.loc[m, col]).abs().max()
        check(f"y horizon {h} mois ({name})", e < 1e-6 and m.sum() > 100, f"écart max {e:.1e}, {int(m.sum())} mois")
        nan = int(real[col].isna().sum())
        check(f"  exactement {h} NaN (les {h} dernières lignes) ({name})",
              nan == h and real[col].iloc[-h:].isna().all(), f"{nan} NaN")

n_ok, n = sum(RESULTS), len(RESULTS)
print(f"\n{n_ok}/{n} contrôles réussis")
sys.exit(0 if n_ok == n else 1)
