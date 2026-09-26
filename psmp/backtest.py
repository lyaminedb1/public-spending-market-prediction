"""Event-driven backtest on out-of-sample signals.

Each selected event opens a position at the day-0 close and holds it for
HOLD_DAYS trading days. Positions are market-hedged with the event's
estimation-window beta. The book is equal-weighted across open positions and
sits in cash on days with nothing open.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .data import MARKET

TRADING_DAYS = 252


def run(
    events: pd.DataFrame,
    selected: pd.Series,
    prices: pd.DataFrame,
    hold: int = 5,
    cost_bps: float = 10.0,
    hedge: bool = True,
) -> dict:
    """`selected` is a boolean Series aligned with `events`."""
    rets = prices.pct_change().fillna(0.0)
    n_days = len(rets)
    mkt = rets[MARKET].to_numpy()
    pnl = np.zeros(n_days)
    count = np.zeros(n_days)
    trade_returns = []
    cost = cost_bps / 1e4

    ev = events[selected.reindex(events.index).fillna(False).astype(bool)]
    for t, i0, beta in zip(ev["ticker"], ev["day0_idx"], ev["beta"]):
        if t not in rets or i0 + hold >= n_days or not np.isfinite(beta):
            continue
        r = rets[t].to_numpy()[i0 + 1 : i0 + hold + 1].copy()
        if hedge:
            r -= beta * mkt[i0 + 1 : i0 + hold + 1]
        r[0] -= cost
        r[-1] -= cost
        pnl[i0 + 1 : i0 + hold + 1] += r
        count[i0 + 1 : i0 + hold + 1] += 1
        trade_returns.append(float(np.prod(1 + r) - 1))

    daily = np.divide(pnl, count, out=np.zeros(n_days), where=count > 0)
    daily = pd.Series(daily, index=rets.index)
    first = np.argmax(count > 0) if (count > 0).any() else 0
    daily = daily.iloc[first:]
    invested = count[first:] > 0

    equity = (1 + daily).cumprod()
    years = len(daily) / TRADING_DAYS
    ann_ret = equity.iloc[-1] ** (1 / years) - 1 if years > 0 else np.nan
    ann_vol = daily.std() * np.sqrt(TRADING_DAYS)
    dd = equity / equity.cummax() - 1
    tr = np.array(trade_returns)
    return {
        "equity": equity,
        "daily": daily,
        "stats": {
            "trades": int(len(tr)),
            "hit_rate": float((tr > 0).mean()) if len(tr) else np.nan,
            "avg_trade": float(tr.mean()) if len(tr) else np.nan,
            "ann_return": float(ann_ret),
            "ann_vol": float(ann_vol),
            "sharpe": float(daily.mean() / daily.std() * np.sqrt(TRADING_DAYS)) if daily.std() > 0 else np.nan,
            "max_drawdown": float(dd.min()),
            "exposure": float(invested.mean()),
            "avg_positions": float(count[first:][invested].mean()) if invested.any() else 0.0,
        },
    }
