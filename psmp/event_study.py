"""Market-model event study around contract announcements.

Day 0 is the first trading day on or after the announcement date. DoD posts
contract announcements at 5pm ET, after the close, so day 0's return is not
tradable on the news; a position opened at the day-0 close earns days +1 onward.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats

from .data import MARKET

EST_WINDOW = (-250, -21)
WINDOW = (-10, 20)
MIN_EST_OBS = 120


def build_events(awards: pd.DataFrame, trading_days: pd.DatetimeIndex) -> pd.DataFrame:
    """Collapse awards to one event per (ticker, day 0)."""
    a = awards.copy()
    pos = trading_days.searchsorted(a["announce_date"].values, side="left")
    a = a[pos < len(trading_days)].copy()
    a["day0_idx"] = pos[pos < len(trading_days)]
    a["day0"] = trading_days[a["day0_idx"]]
    a["is_dod"] = a["agency"].str.contains("Defense", case=False, na=False)
    a["competed_f"] = pd.to_numeric(a["competed"], errors="coerce")
    a["new_amount"] = a["amount"].where(a["is_new"], 0.0)

    g = a.groupby(["ticker", "day0"], sort=True)
    ev = g.agg(
        day0_idx=("day0_idx", "first"),
        amount=("amount", "sum"),
        max_amount=("amount", "max"),
        n_awards=("award_id", "size"),
        new_amount=("new_amount", "sum"),
        any_new=("is_new", "max"),
        competed_share=("competed_f", "mean"),
        dod_share=("is_dod", "mean"),
        award_ids=("award_id", list),
    ).reset_index()
    ev["event_id"] = ev["ticker"] + "@" + ev["day0"].dt.strftime("%Y-%m-%d")
    return ev.sort_values(["day0", "ticker"]).reset_index(drop=True)


def abnormal_returns(events: pd.DataFrame, prices: pd.DataFrame) -> pd.DataFrame:
    """Abnormal returns for each event over WINDOW, rows aligned with `events`.

    Also returns market-model beta and residual vol in extra columns.
    """
    rets = prices.pct_change()
    mkt = rets[MARKET].to_numpy()
    offsets = np.arange(WINDOW[0], WINDOW[1] + 1)
    out = np.full((len(events), len(offsets)), np.nan)
    betas = np.full(len(events), np.nan)
    sigmas = np.full(len(events), np.nan)
    n = len(rets)

    cache = {t: rets[t].to_numpy() for t in events["ticker"].unique() if t in rets}
    for row, (ticker, i0) in enumerate(zip(events["ticker"], events["day0_idx"])):
        r = cache.get(ticker)
        if r is None:
            continue
        lo, hi = i0 + EST_WINDOW[0], i0 + EST_WINDOW[1]
        if lo < 1 or i0 + WINDOW[1] >= n:
            continue
        y, x = r[lo : hi + 1], mkt[lo : hi + 1]
        ok = np.isfinite(y) & np.isfinite(x)
        if ok.sum() < MIN_EST_OBS:
            continue
        beta, alpha = np.polyfit(x[ok], y[ok], 1)
        resid = y[ok] - alpha - beta * x[ok]
        betas[row] = beta
        sigmas[row] = resid.std(ddof=2)
        win = slice(i0 + WINDOW[0], i0 + WINDOW[1] + 1)
        out[row] = r[win] - alpha - beta * mkt[win]

    ar = pd.DataFrame(out, columns=[f"ar{o:+d}" for o in offsets], index=events.index)
    ar["beta"] = betas
    ar["sigma"] = sigmas
    return ar


def car(ar: pd.DataFrame, start: int, end: int) -> pd.Series:
    cols = [f"ar{o:+d}" for o in range(start, end + 1)]
    return ar[cols].sum(axis=1, min_count=len(cols))


@dataclass
class CaarResult:
    offsets: np.ndarray
    caar: np.ndarray
    lo: np.ndarray
    hi: np.ndarray


def caar_path(ar: pd.DataFrame, mask: pd.Series | None = None) -> CaarResult:
    """Cumulative average abnormal return with a 95% band, cumulated from day -10."""
    cols = [c for c in ar.columns if c.startswith("ar")]
    m = ar[cols]
    if mask is not None:
        m = m[mask]
    m = m.dropna()
    cum = m.cumsum(axis=1)
    mean = cum.mean().to_numpy()
    se = cum.std(ddof=1).to_numpy() / np.sqrt(len(cum))
    offsets = np.array([int(c[2:]) for c in cols])
    return CaarResult(offsets, mean, mean - 1.96 * se, mean + 1.96 * se)


def summarize(values: pd.Series, sigma: pd.Series | None = None, days: int = 1) -> dict:
    """Mean, t-stat, sign test, and a standardized (Patell-style) z."""
    v = values.dropna()
    res = {
        "n": int(len(v)),
        "mean": float(v.mean()),
        "median": float(v.median()),
        "t": float(stats.ttest_1samp(v, 0).statistic) if len(v) > 2 else np.nan,
        "pct_positive": float((v > 0).mean()),
    }
    res["sign_p"] = float(stats.binomtest(int((v > 0).sum()), len(v), 0.5).pvalue) if len(v) else np.nan
    if sigma is not None:
        s = sigma.reindex(v.index)
        z = v / (s * np.sqrt(days))
        z = z[np.isfinite(z)]
        res["patell_z"] = float(z.sum() / np.sqrt(len(z))) if len(z) else np.nan
    return res
