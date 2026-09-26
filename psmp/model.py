"""Walk-forward prediction of post-announcement CAR[+1,+5]."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import RidgeCV
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from .features import FEATURES

HOLD_DAYS = 5
# Drop training events whose label window overlaps the test year.
PURGE_DAYS = HOLD_DAYS + 2


def make_models() -> dict:
    return {
        "size_rule": ("log_surprise", None),
        "ridge": (
            FEATURES,
            lambda: make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-2, 3, 12))),
        ),
        "gbm": (
            FEATURES,
            lambda: HistGradientBoostingRegressor(
                max_iter=300,
                learning_rate=0.04,
                max_leaf_nodes=15,
                min_samples_leaf=80,
                l2_regularization=1.0,
                random_state=0,
            ),
        ),
    }


@dataclass
class WalkForward:
    predictions: pd.DataFrame  # event index -> one column per model, OOS only
    yearly: pd.DataFrame  # per test year, per model metrics
    thresholds: dict = field(default_factory=dict)  # (model, year) -> entry threshold
    importances: pd.Series | None = None


def _winsorize(y: pd.Series, q: float = 0.01) -> pd.Series:
    lo, hi = y.quantile(q), y.quantile(1 - q)
    return y.clip(lo, hi)


def walk_forward(
    X: pd.DataFrame,
    y: pd.Series,
    day0: pd.Series,
    day0_idx: pd.Series,
    first_test_year: int,
    top_frac: float = 0.2,
) -> WalkForward:
    ok = X.notna().all(axis=1) & y.notna()
    X, y, day0, day0_idx = X[ok], y[ok], day0[ok], day0_idx[ok]
    years = sorted(yr for yr in day0.dt.year.unique() if yr >= first_test_year)
    models = make_models()
    preds = pd.DataFrame(index=X.index, columns=list(models), dtype=float)
    rows, thresholds = [], {}
    gbm_last = None

    for year in years:
        test = day0.dt.year == year
        test_start = day0_idx[test].min()
        train = (day0.dt.year < year) & (day0_idx < test_start - PURGE_DAYS)
        if train.sum() < 500:
            continue
        y_train = _winsorize(y[train])
        for name, (cols, factory) in models.items():
            if factory is None:
                p_train = X.loc[train, cols].to_numpy()
                p_test = X.loc[test, cols].to_numpy()
            else:
                m = factory()
                m.fit(X.loc[train, cols], y_train)
                p_train = m.predict(X.loc[train, cols])
                p_test = m.predict(X.loc[test, cols])
                if name == "gbm":
                    gbm_last = (m, X.loc[test, cols], y[test])
            preds.loc[test, name] = p_test
            # Entry threshold is fixed from training predictions: no peeking at
            # the test year's distribution.
            thr = float(np.quantile(p_train, 1 - top_frac))
            thresholds[(name, year)] = thr
            yt = y[test]
            ic = stats.spearmanr(p_test, yt).statistic
            auc = roc_auc_score(yt > 0, p_test) if (yt > 0).nunique() == 2 else np.nan
            picked = p_test >= thr
            rows.append(
                {
                    "year": year,
                    "model": name,
                    "n_test": int(test.sum()),
                    "ic": ic,
                    "auc": auc,
                    "picked": int(picked.sum()),
                    "picked_car": float(yt[picked].mean()) if picked.any() else np.nan,
                    "all_car": float(yt.mean()),
                }
            )

    importances = None
    if gbm_last is not None:
        from sklearn.inspection import permutation_importance

        m, Xt, yt = gbm_last
        pi = permutation_importance(m, Xt, yt, n_repeats=5, random_state=0, scoring="r2")
        importances = pd.Series(pi.importances_mean, index=Xt.columns).sort_values(ascending=False)

    return WalkForward(preds, pd.DataFrame(rows), thresholds, importances)
