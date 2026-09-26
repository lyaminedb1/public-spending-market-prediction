"""End-to-end run: data -> events -> event study -> model -> backtest -> report."""

from __future__ import annotations

import json
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from . import backtest, report
from .event_study import abnormal_returns, build_events, caar_path, car, summarize
from .features import build_features
from .model import HOLD_DAYS, walk_forward


def run(
    source: str = "synthetic",
    start: str = "2015-01-01",
    end: str = "2025-12-31",
    first_test_year: int = 2019,
    top_frac: float = 0.2,
    cost_bps: float = 10.0,
    out_dir: str = "results",
    scale: float = 1.0,
    seed: int = 7,
    effect_scale: float = 0.3,
) -> dict:
    t0 = time.time()
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    truth = None

    print(f"[1/6] loading {source} data {start}..{end}")
    if source == "synthetic":
        from .data.synthetic import generate

        awards, prices, truth = generate(
            start, end, awards_per_year_scale=scale, effect_scale=effect_scale, seed=seed
        )
    elif source == "live":
        from .data.live import load

        awards, prices = load(start, end)
    else:
        raise ValueError(f"unknown source {source!r}")
    awards = awards[awards["ticker"].isin(prices.columns)]
    print(f"      {len(awards):,} awards, {prices.shape[1] - 1} stocks, {len(prices):,} trading days")

    print("[2/6] building events and abnormal returns")
    events = build_events(awards, prices.index)
    ar = abnormal_returns(events, prices)
    events = events.join(ar[["beta", "sigma"]])
    post = car(ar, 1, HOLD_DAYS)
    pre = car(ar, -2, 0)
    valid = post.notna()
    print(f"      {len(events):,} events ({valid.sum():,} with full windows)")

    print("[3/6] event study")
    es = {
        "pre_car[-2,0]": summarize(pre, ar["sigma"], 3),
        "post_car[+1,+5]": summarize(post, ar["sigma"], HOLD_DAYS),
    }
    X = build_features(events, ar, prices)
    dec = pd.qcut(X["log_surprise"], 10, labels=False)
    dec_table = post.groupby(dec).agg(["mean", "std", "count"])
    dec_table["se"] = dec_table["std"] / np.sqrt(dec_table["count"])
    q = pd.qcut(X["log_surprise"], 5, labels=False)
    report.caar_chart(
        {
            "all events": caar_path(ar),
            "top surprise quintile": caar_path(ar, q == 4),
            "bottom surprise quintile": caar_path(ar, q == 0),
        },
        out / "caar.png",
    )
    report.decile_chart(dec_table, out / "car_by_decile.png")

    print(f"[4/6] walk-forward models (test years >= {first_test_year})")
    wf = walk_forward(X, post, events["day0"], events["day0_idx"], first_test_year, top_frac)
    report.ic_chart(wf.yearly, out / "ic_by_year.png")
    if wf.importances is not None:
        report.importance_chart(wf.importances, out / "importance.png")

    print("[5/6] backtests")
    oos = wf.predictions.notna().all(axis=1)
    year = events["day0"].dt.year
    strategies = {"all awards": oos}
    for name in wf.predictions.columns:
        thr = pd.Series([wf.thresholds.get((name, y), np.inf) for y in year], index=events.index)
        strategies[name] = oos & (wf.predictions[name] >= thr)
    rng = np.random.default_rng(0)
    strategies["random 20%"] = oos & pd.Series(rng.random(len(events)) < top_frac, index=events.index)
    results = {k: backtest.run(events, sel, prices, HOLD_DAYS, cost_bps) for k, sel in strategies.items()}
    report.equity_chart({k: r["equity"] for k, r in results.items()}, out / "equity.png")

    validation = None
    if truth is not None:
        # With effect_scale=0 the truth is all zeros and correlations are undefined.
        warnings.filterwarnings("ignore", category=stats.ConstantInputWarning)
        true_post = events["award_ids"].map(lambda ids: float(sum(truth.get(i, 0.0) for i in ids)))
        validation = {
            "true_mean_post_effect": float(true_post[valid].mean()),
            "estimated_mean_post_car": float(post[valid].mean()),
            "corr_realized_vs_true": float(stats.spearmanr(post[valid], true_post[valid]).statistic),
        }
        for name in wf.predictions.columns:
            m = oos & wf.predictions[name].notna()
            validation[f"ic_vs_truth_{name}"] = float(
                stats.spearmanr(wf.predictions.loc[m, name], true_post[m]).statistic
            )

    print("[6/6] writing report")
    summary = {
        "source": source,
        "period": [start, end],
        "awards": int(len(awards)),
        "events": int(len(events)),
        "event_study": es,
        "models": wf.yearly.groupby("model")[["ic", "auc", "picked_car", "all_car"]].mean().to_dict("index"),
        "backtests": {k: r["stats"] for k, r in results.items()},
        "synthetic_validation": validation,
        "runtime_s": round(time.time() - t0, 1),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=float))
    wf.yearly.to_csv(out / "yearly_model_metrics.csv", index=False)
    _write_markdown(out, summary, dec_table, wf, prices, awards)
    print(f"done in {summary['runtime_s']}s -> {out}/REPORT.md")
    return summary


def _write_markdown(out, s, dec_table, wf, prices, awards):
    P = report.fmt_pct
    es = s["event_study"]
    es_rows = pd.DataFrame(
        [
            {
                "window": k,
                "events": f"{v['n']:,}",
                "mean CAR": P(v["mean"], 3),
                "median": P(v["median"], 3),
                "t": f"{v['t']:.2f}",
                "Patell z": f"{v.get('patell_z', float('nan')):.2f}",
                "% positive": P(v["pct_positive"], 1),
            }
            for k, v in es.items()
        ]
    )
    dec_rows = pd.DataFrame(
        {
            "decile": [f"D{i + 1}" for i in dec_table.index],
            "events": dec_table["count"].map("{:,}".format),
            "mean CAR[+1,+5]": dec_table["mean"].map(lambda x: P(x, 3)),
            "95% CI ±": (1.96 * dec_table["se"]).map(lambda x: P(x, 3)),
        }
    )
    model_rows = pd.DataFrame(
        [
            {
                "model": m,
                "mean IC": f"{v['ic']:.3f}",
                "mean AUC": f"{v['auc']:.3f}",
                "CAR of picks": P(v["picked_car"], 3),
                "CAR of all": P(v["all_car"], 3),
            }
            for m, v in s["models"].items()
        ]
    )
    bt_rows = pd.DataFrame(
        [
            {
                "strategy": k,
                "trades": f"{v['trades']:,}",
                "hit rate": P(v["hit_rate"], 1),
                "avg trade": P(v["avg_trade"], 3),
                "ann. return": P(v["ann_return"], 1),
                "ann. vol": P(v["ann_vol"], 1),
                "Sharpe": f"{v['sharpe']:.2f}",
                "max DD": P(v["max_drawdown"], 1),
                "exposure": P(v["exposure"], 0),
            }
            for k, v in s["backtests"].items()
        ]
    )

    lines = [
        "# Public spending → market reaction: run report",
        "",
        f"Source: **{s['source']}** · period {s['period'][0]} to {s['period'][1]} · "
        f"{s['awards']:,} contract actions ≥ $7.5M collapsed into {s['events']:,} firm-day events · "
        f"{prices.shape[1] - 1} stocks · runtime {s['runtime_s']}s",
        "",
    ]
    if s["source"] == "synthetic":
        lines += [
            "> **These numbers come from synthetic data with a known, injected award effect.** "
            "They show that the pipeline works and recovers a signal when one exists. They say "
            "nothing about real markets. Run `psmp run --source live` with network access to "
            "api.usaspending.gov and a price source to get real results.",
            "",
        ]
    lines += [
        "## 1. Event study",
        "",
        "Market model fit on days −250..−21. Day 0 is the announcement date; the DoD posts awards "
        "after the close, so a trade can only start earning on day +1.",
        "",
        report.md_table(es_rows),
        "",
        "![CAAR](caar.png)",
        "",
        report.md_table(dec_rows),
        "",
        "![CAR by decile](car_by_decile.png)",
        "",
        "## 2. Walk-forward prediction of CAR[+1,+5]",
        "",
        "Train on all years before the test year (purged of events whose label window "
        "crosses into it), predict the test year, roll forward. `size_rule` ranks by "
        "award $ / market cap alone.",
        "",
        report.md_table(model_rows),
        "",
        "![IC by year](ic_by_year.png)",
        "",
    ]
    if wf.importances is not None:
        lines += ["![Importance](importance.png)", ""]
    lines += [
        "## 3. Backtest (out-of-sample years only)",
        "",
        "Enter at the day-0 close, hold 5 trading days, hedge with the estimation-window beta, "
        "equal weight across open positions, 10 bps cost per side. Model strategies take events "
        "whose prediction clears the top-20% threshold of that model's *training-set* predictions.",
        "",
        report.md_table(bt_rows),
        "",
        "![Equity](equity.png)",
        "",
    ]
    v = s.get("synthetic_validation")
    if v:
        lines += [
            "## 4. Synthetic ground-truth check",
            "",
            f"- Injected mean post-announcement effect: {P(v['true_mean_post_effect'], 3)}; "
            f"event study estimate: {P(v['estimated_mean_post_car'], 3)}",
            f"- Rank correlation of realized CAR with the injected effect: "
            f"{v['corr_realized_vs_true']:.3f} (this is the ceiling on achievable IC: noise dominates)",
        ]
        for k, val in v.items():
            if k.startswith("ic_vs_truth_"):
                lines.append(f"- Rank correlation of `{k[12:]}` predictions with the injected effect: {val:.3f}")
        lines.append("")
    lines += [
        "## Caveats",
        "",
        "- USAspending action dates are the signing date, not always the public announcement date. "
        "Announcements can lag by a day, which blurs day 0.",
        "- Market caps are static approximations in `psmp/universe.py`, so the surprise measure is "
        "order-of-magnitude only.",
        "- Contract modifications and option exercises are often expected by the market. The "
        "`any_new` feature separates them only where the modification number is available.",
        "- The backtest has no borrow or capacity limits, and it assumes you can trade at the close "
        "right after the announcement.",
        "",
    ]
    (out / "REPORT.md").write_text("\n".join(lines))
