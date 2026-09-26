"""Robustness sweep: rerun the synthetic pipeline across seeds and effect sizes.

A single synthetic draw can flatter or punish a strategy by luck; the spread of
Sharpe ratios across independent worlds is the honest answer.
"""

from __future__ import annotations

import contextlib
import io
import multiprocessing
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from . import report
from .pipeline import run


def _one(args):
    es, seed, out_dir = args
    with contextlib.redirect_stdout(io.StringIO()):
        s = run(source="synthetic", out_dir=out_dir, seed=seed, effect_scale=es)
    post = s["event_study"]["post_car[+1,+5]"]
    return [
        {
            "effect_scale": es,
            "seed": seed,
            "strategy": strat,
            "sharpe": st["sharpe"],
            "ann_return": st["ann_return"],
            "max_drawdown": st["max_drawdown"],
            "hit_rate": st["hit_rate"],
            "event_t": post["t"],
            "ic": s["models"].get(strat, {}).get("ic", np.nan),
        }
        for strat, st in s["backtests"].items()
    ]


def sweep(
    seeds: int = 20,
    effect_scales=(0.0, 0.15, 0.3, 0.5),
    out_dir: str = "results/sweep",
    workers: int | None = None,
) -> pd.DataFrame:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    jobs = [(es, seed, str(out / "runs" / f"es{es}_seed{seed}")) for es in effect_scales for seed in range(seeds)]
    workers = workers or os.cpu_count() or 1
    rows = []
    # One BLAS/OpenMP thread per process, otherwise workers fight over cores.
    # Spawn, don't fork: a forked child inherits OpenMP state from the parent
    # and can spin forever inside scikit-learn's thread pool.
    for var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[var] = "1"
    ctx = multiprocessing.get_context("spawn")
    with ProcessPoolExecutor(workers, mp_context=ctx) as pool:
        futures = {pool.submit(_one, j): j for j in jobs}
        for k, fut in enumerate(as_completed(futures), start=1):
            rows.extend(fut.result())
            es, seed, _ = futures[fut]
            print(f"  [{k}/{len(jobs)}] effect_scale={es} seed={seed} done", flush=True)
    df = pd.DataFrame(rows).sort_values(["effect_scale", "seed", "strategy"]).reset_index(drop=True)
    df.to_csv(out / "sweep.csv", index=False)
    _write(df, out)
    return df


def _write(df: pd.DataFrame, out: Path) -> None:
    order = ["all awards", "size_rule", "ridge", "gbm", "random 20%"]
    g = df.groupby(["effect_scale", "strategy"])["sharpe"]
    tbl = g.agg(
        median="median",
        p10=lambda s: s.quantile(0.1),
        p90=lambda s: s.quantile(0.9),
        pct_positive=lambda s: (s > 0).mean(),
    ).reset_index()
    tbl["strategy"] = pd.Categorical(tbl["strategy"], order, ordered=True)
    tbl = tbl.sort_values(["effect_scale", "strategy"])
    ic = df.dropna(subset=["ic"]).groupby(["effect_scale", "strategy"])["ic"].median()

    # Median Sharpe vs injected effect size, one line per strategy.
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for i, strat in enumerate(order):
        sub = tbl[tbl["strategy"] == strat]
        c = report.MUTED if strat.startswith("random") else report.SERIES[i]
        ls = ":" if strat.startswith("random") else "-"
        ax.fill_between(sub["effect_scale"], sub["p10"], sub["p90"], color=c, alpha=0.1, lw=0)
        ax.plot(sub["effect_scale"], sub["median"], color=c, ls=ls, marker="o", ms=5, label=strat)
    ax.axhline(0, color=report.MUTED, lw=0.8)
    ax.set_xlabel("Injected effect scale (0 = no real signal)")
    ax.set_ylabel("Out-of-sample Sharpe")
    ax.set_title("Sharpe across independent synthetic worlds (median, 10th-90th pct band)")
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(out / "sharpe_vs_effect.png", dpi=150)
    plt.close(fig)

    n_seeds = df["seed"].nunique()
    rows = pd.DataFrame(
        {
            "effect scale": tbl["effect_scale"],
            "strategy": tbl["strategy"].astype(str),
            "median Sharpe": tbl["median"].map("{:.2f}".format),
            "10th pct": tbl["p10"].map("{:.2f}".format),
            "90th pct": tbl["p90"].map("{:.2f}".format),
            "worlds with Sharpe > 0": tbl["pct_positive"].map("{:.0%}".format),
            "median IC": [
                f"{ic.get((e, s), np.nan):.3f}" if (e, s) in ic.index else "—"
                for e, s in zip(tbl["effect_scale"], tbl["strategy"].astype(str))
            ],
        }
    )
    md = [
        "# Robustness sweep",
        "",
        f"{n_seeds} independent synthetic worlds per effect scale. Effect scale 0 injects no "
        "award effect at all, so any Sharpe there is pure noise (or a bug).",
        "",
        "Reading it: with no effect, hedged returns average zero and every strategy pays 10 bps "
        "per side on a book that turns over every 5 days. That is roughly -10%/yr for the "
        "always-invested `all awards` book, hence its Sharpe near -1.5. Negative Sharpe at "
        "scale 0 is the cost drag, not a false signal. The models only beat `random 20%` once "
        "a real effect exists, and the simple size rule is the most robust of the three.",
        "",
        report.md_table(rows),
        "",
        "![Sharpe vs effect](sharpe_vs_effect.png)",
        "",
    ]
    (out / "SWEEP.md").write_text("\n".join(md))
