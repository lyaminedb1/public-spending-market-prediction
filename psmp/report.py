"""Charts and a markdown report."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

SURFACE = "#fcfcfb"
TEXT = "#0b0b0b"
TEXT_2 = "#52514e"
GRID = "#e4e3df"
MUTED = "#8a8984"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
SEQ_BLUE = ["#cfe0f6", "#a5c6ee", "#79a9e4", "#4f8cdb", "#2a78d6", "#1d5fb0", "#154889"]

plt.rcParams.update(
    {
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "axes.edgecolor": GRID,
        "axes.labelcolor": TEXT_2,
        "axes.titlecolor": TEXT,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "xtick.color": TEXT_2,
        "ytick.color": TEXT_2,
        "font.size": 10,
        "legend.frameon": False,
        "legend.labelcolor": TEXT_2,
        "lines.linewidth": 2,
    }
)


def _pct(ax, axis="y", decimals=1):
    from matplotlib.ticker import PercentFormatter

    fmt = PercentFormatter(1.0, decimals=decimals)
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(fmt)


def _end_labels(ax, items, min_gap=0.045):
    """Direct labels at line ends, nudged apart so they never overlap.

    items: (label, x, y) in data coordinates; min_gap is in axes-fraction units.
    """
    ax.figure.canvas.draw()
    to_ax = ax.transAxes.inverted()
    pts = []
    for label, x, y in items:
        disp = ax.transData.transform((x, y))
        pts.append([label, x, to_ax.transform(disp)[1]])
    pts.sort(key=lambda p: p[2])
    for i in range(1, len(pts)):
        pts[i][2] = max(pts[i][2], pts[i - 1][2] + min_gap)
    for label, x, yf in pts:
        ax.annotate(
            label, xy=(x, yf), xycoords=("data", "axes fraction"), xytext=(6, 0),
            textcoords="offset points", va="center", color=TEXT_2, fontsize=9,
        )


def caar_chart(paths: dict, out: Path) -> None:
    """paths: label -> CaarResult."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for k, (label, p) in enumerate(paths.items()):
        c = SERIES[k]
        ax.fill_between(p.offsets, p.lo, p.hi, color=c, alpha=0.12, lw=0)
        ax.plot(p.offsets, p.caar, color=c, label=label)
    ax.axvline(0, color=MUTED, lw=1, ls="--")
    ax.axvspan(0.5, 5.5, color=GRID, alpha=0.5, lw=0)
    ax.text(3, ax.get_ylim()[1], "holding window", ha="center", va="top", color=TEXT_2, fontsize=9)
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.set_xlabel("Trading days relative to announcement (day 0 = announcement, after close)")
    ax.set_title("Cumulative abnormal return around contract announcements")
    ax.legend(loc="upper left")
    _pct(ax, decimals=2)
    ax.set_xlim(p.offsets[0], p.offsets[-1] + 6)
    _end_labels(ax, [(lbl, q.offsets[-1], q.caar[-1]) for lbl, q in paths.items()])
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


def decile_chart(table: pd.DataFrame, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.arange(len(table))
    colors = [SEQ_BLUE[min(int(i * len(SEQ_BLUE) / len(table)), len(SEQ_BLUE) - 1)] for i in x]
    ax.bar(x, table["mean"], color=colors, width=0.8, edgecolor=SURFACE, linewidth=2)
    ax.errorbar(x, table["mean"], yerr=1.96 * table["se"], fmt="none", ecolor=TEXT_2, lw=1, capsize=3)
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.set_xticks(x, [f"D{i + 1}" for i in x])
    ax.set_xlabel("Award surprise decile (award $ / market cap), D1 = smallest")
    ax.set_title("Post-announcement CAR[+1,+5] by award surprise")
    ax.grid(axis="x", visible=False)
    _pct(ax, decimals=2)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


def equity_chart(curves: dict, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for k, (label, eq) in enumerate(curves.items()):
        c = MUTED if label.startswith("random") else SERIES[k]
        ls = ":" if label.startswith("random") else "-"
        ax.plot(eq.index, eq.values, color=c, ls=ls, label=label)
    ax.axhline(1, color=MUTED, lw=0.8)
    ax.set_title("Out-of-sample equity, market-hedged, 10 bps per side")
    ax.set_ylabel("Growth of $1")
    ax.legend(loc="upper left")
    ax.margins(x=0.12)
    _end_labels(ax, [(lbl, eq.index[-1], eq.values[-1]) for lbl, eq in curves.items()])
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


def importance_chart(imp: pd.Series, out: Path, top: int = 12) -> None:
    s = imp.head(top)[::-1]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.barh(s.index, s.values, color=SERIES[0], height=0.7, edgecolor=SURFACE, linewidth=2)
    ax.set_title("Gradient boosting: permutation importance (last test year)")
    ax.set_xlabel("Drop in R² when feature is shuffled")
    ax.grid(axis="y", visible=False)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


def ic_chart(yearly: pd.DataFrame, out: Path) -> None:
    piv = yearly.pivot(index="year", columns="model", values="ic")
    fig, ax = plt.subplots(figsize=(8, 4))
    models = list(piv.columns)
    w = 0.8 / len(models)
    for k, m in enumerate(models):
        ax.bar(piv.index + (k - (len(models) - 1) / 2) * w, piv[m], width=w, color=SERIES[k],
               label=m, edgecolor=SURFACE, linewidth=1.5)
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.set_title("Out-of-sample rank IC by year (prediction vs realized CAR[+1,+5])")
    ax.set_xticks(piv.index)
    ax.grid(axis="x", visible=False)
    ax.legend(ncol=len(models), loc="upper left")
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


def fmt_pct(x: float, d: int = 2) -> str:
    return "n/a" if pd.isna(x) else f"{x * 100:.{d}f}%"


def md_table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(str(c) for c in cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(str(v) for v in r.values) + " |")
    return "\n".join(lines)
