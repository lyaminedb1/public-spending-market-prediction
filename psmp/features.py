"""Per-event features. Everything here is known at the day-0 close."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .universe import BY_TICKER

SECTORS = ("defense", "services", "tech", "health", "infrastructure")

FEATURES = [
    "log_amount",
    "log_surprise",
    "log_new_surprise",
    "log_max_surprise",
    "n_awards",
    "any_new",
    "competed_share",
    "dod_share",
    "log_mcap",
    "pre_car",
    "day0_ar",
    "momentum_60",
    "sigma",
    "beta",
    "awards_30d",
    "surprise_vs_own_median",
    *[f"sector_{s}" for s in SECTORS],
]


def build_features(events: pd.DataFrame, ar: pd.DataFrame, prices: pd.DataFrame) -> pd.DataFrame:
    ev = events
    mcap = ev["ticker"].map(lambda t: BY_TICKER[t].market_cap_bn * 1e9)
    f = pd.DataFrame(index=ev.index)
    f["log_amount"] = np.log(ev["amount"])
    surprise = ev["amount"] / mcap
    f["log_surprise"] = np.log(surprise)
    f["log_new_surprise"] = np.log1p(ev["new_amount"] / mcap * 1e4)
    f["log_max_surprise"] = np.log(ev["max_amount"] / mcap)
    f["n_awards"] = ev["n_awards"]
    f["any_new"] = ev["any_new"].astype(float)
    f["competed_share"] = ev["competed_share"].fillna(0.5)
    f["dod_share"] = ev["dod_share"]
    f["log_mcap"] = np.log(mcap)
    # Pre-announcement run-up and the day-0 move: if the market already moved,
    # less is left to capture.
    f["pre_car"] = ar[["ar-2", "ar-1"]].sum(axis=1, min_count=2)
    f["day0_ar"] = ar["ar+0"]
    f["sigma"] = ar["sigma"]
    f["beta"] = ar["beta"]

    rets = prices.pct_change()
    mom = np.full(len(ev), np.nan)
    for row, (t, i0) in enumerate(zip(ev["ticker"], ev["day0_idx"])):
        if t in rets and i0 >= 61:
            mom[row] = rets[t].iloc[i0 - 60 : i0].sum()
    f["momentum_60"] = mom

    # Award flow to the same firm in the previous 30 calendar days (excl. today).
    f["awards_30d"] = 0.0
    f["surprise_vs_own_median"] = 0.0
    for t, grp in ev.groupby("ticker"):
        s = grp.set_index("day0")["n_awards"].astype(float)
        rolled = s.rolling("30D").sum() - s
        f.loc[grp.index, "awards_30d"] = rolled.to_numpy()
        # Surprise relative to the firm's own trailing median (expanding, lagged).
        ls = f.loc[grp.index, "log_surprise"]
        med = ls.expanding().median().shift(1)
        f.loc[grp.index, "surprise_vs_own_median"] = (ls - med).fillna(0).to_numpy()

    sector = ev["ticker"].map(lambda t: BY_TICKER[t].sector)
    for s in SECTORS:
        f[f"sector_{s}"] = (sector == s).astype(float)
    return f[FEATURES]
