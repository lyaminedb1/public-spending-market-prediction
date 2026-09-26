"""Command line entry point: `psmp run` or `python -m psmp run`."""

from __future__ import annotations

import argparse


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="psmp", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="run the full pipeline")
    r.add_argument("--source", choices=["synthetic", "live"], default="synthetic")
    r.add_argument("--start", default="2015-01-01")
    r.add_argument("--end", default="2025-12-31")
    r.add_argument("--first-test-year", type=int, default=2019)
    r.add_argument("--top-frac", type=float, default=0.2)
    r.add_argument("--cost-bps", type=float, default=10.0)
    r.add_argument("--scale", type=float, default=1.0, help="synthetic: award-rate multiplier")
    r.add_argument("--seed", type=int, default=7, help="synthetic: RNG seed")
    r.add_argument("--effect-scale", type=float, default=0.3, help="synthetic: injected effect size")
    r.add_argument("--out", default="results")
    sw = sub.add_parser("sweep", help="synthetic robustness sweep over seeds and effect sizes")
    sw.add_argument("--seeds", type=int, default=20)
    sw.add_argument("--effect-scales", default="0,0.15,0.3,0.5")
    sw.add_argument("--out", default="results/sweep")
    sw.add_argument("--workers", type=int, default=None)
    a = p.parse_args(argv)

    if a.cmd == "sweep":
        from .sweep import sweep

        sweep(a.seeds, tuple(float(x) for x in a.effect_scales.split(",")), a.out, a.workers)
        return

    from .pipeline import run

    run(
        source=a.source,
        start=a.start,
        end=a.end,
        first_test_year=a.first_test_year,
        top_frac=a.top_frac,
        cost_bps=a.cost_bps,
        out_dir=a.out,
        scale=a.scale,
        seed=a.seed,
        effect_scale=a.effect_scale,
    )


if __name__ == "__main__":
    main()
