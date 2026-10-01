"""
03_exploration.py
Analyse exploratoire du jeu de données mensuel (section 3.1 du mémoire).

Entrée  : data/processed/dataset_monthly.csv
Sorties : results/figures/fig3_1_*.png  et  results/tables/eda_*.csv

Rappel méthodologique : les corrélations ci-dessous sont descriptives. Elles ne servent
PAS à choisir les cibles ni les variables (fixées a priori), pour éviter le data snooping.

Lancer depuis la racine du dépôt :  python src/03_exploration.py
"""

from pathlib import Path

import matplotlib.pyplot as plt

import fr_format  # noqa: F401  (virgule décimale dans les figures)
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller, acf

DATA = Path("data/processed/dataset_monthly.csv")
FIG = Path("results/figures")
TAB = Path("results/tables")
FIG.mkdir(parents=True, exist_ok=True)
TAB.mkdir(parents=True, exist_ok=True)

# Palette de référence (3 premières teintes validées pour la vision des couleurs)
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.edgecolor": INK2,
    "axes.labelcolor": INK,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.titlelocation": "left",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "axes.axisbelow": True,
    "grid.color": GRID,
    "grid.linewidth": 0.8,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "legend.frameon": False,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
})

TARGETS = {
    "y_d_spread": "Variation du spread\nOAT–Bund (pb)",
    "y_d_oat": "Variation du taux\nOAT 10 ans (pb)",
    "y_cac_ret": "Rendement\ndu CAC 40 (%)",
}

BUDGET_LABELS = {
    "b_dep_totales": "Dépenses totales",
    "b_dep_personnel": "Personnel",
    "b_dep_fonctionnement": "Fonctionnement",
    "b_dep_charge_dette": "Charge de la dette",
    "b_dep_investissement": "Investissement",
    "b_dep_intervention": "Intervention",
    "b_psr_total": "Prélèvements sur recettes",
}


def load() -> pd.DataFrame:
    df = pd.read_csv(DATA, index_col="mois")
    df.index = pd.PeriodIndex(df.index, freq="M")
    return df


# ---------------------------------------------------------------------------
# Figure 3.1 : spread et finances publiques dans le temps (deux panneaux, un axe chacun)
# ---------------------------------------------------------------------------
def fig_spread_budget(df: pd.DataFrame) -> None:
    t = df.index.to_timestamp()
    # Le budget est stocké décalé de 2 mois : pour la description, on le replace à son mois réel
    t_budget = pd.PeriodIndex(df["b_source_month"], freq="M").to_timestamp()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6.2), sharex=True,
                                   gridspec_kw={"height_ratios": [1, 1], "hspace": 0.25})

    ax1.plot(t, df["spread_bp"], color=BLUE, lw=2)
    ax1.set_ylim(15, 100)
    ax1.set_title("A. Spread OAT–Bund à 10 ans", pad=10)
    ax1.set_ylabel("points de base")
    events = [("2017-04", "Présidentielle\n2017"), ("2020-03", "Covid-19"),
              ("2022-07", "Hausse des\ntaux BCE"), ("2024-06", "Dissolution")]
    for date, label in events:
        x = pd.Timestamp(date)
        ax1.axvline(x, color=INK2, lw=0.8, ls=":", zorder=0)
        ax1.text(x, 98, label, fontsize=8, color=INK2, ha="center", va="top",
                 bbox=dict(facecolor="white", edgecolor="none", pad=1))

    ax2.plot(t_budget, df["b_solde_12m"], color=ORANGE, lw=2, label="Solde budgétaire")
    ax2.plot(t_budget, df["b_dep_charge_dette_12m"], color=AQUA, lw=2, label="Charge de la dette")
    ax2.axhline(0, color=INK2, lw=0.8)
    ax2.set_title("B. Budget de l'État (cumul sur 12 mois glissants)")
    ax2.set_ylabel("milliards d'euros")
    ax2.legend(loc="lower left", ncol=2)
    ax2.xaxis.set_major_locator(mdates.YearLocator(2))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    fig.text(0, -0.02, "Sources : FRED (OCDE), DGFiP – situations mensuelles budgétaires. "
             "Taux : moyennes mensuelles.", fontsize=8, color=INK2)
    fig.savefig(FIG / "fig3_1_spread_budget.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 3.2 : distribution des trois cibles
# ---------------------------------------------------------------------------
def fig_target_distributions(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.2))
    for ax, (col, label) in zip(axes, TARGETS.items()):
        y = df[col].dropna()
        ax.hist(y, bins=25, color=BLUE, edgecolor="white", linewidth=1)
        ax.axvline(0, color=INK2, lw=0.8)
        ax.set_title(label, fontsize=9.5)
        ax.set_ylabel("nombre de mois" if col == "y_d_spread" else "")
        ax.text(0.98, 0.95, f"moyenne {y.mean():.2f}\nécart-type {y.std():.2f}\nn = {len(y)}",
                transform=ax.transAxes, ha="right", va="top", fontsize=8, color=INK2)
        ax.grid(axis="x", visible=False)
    fig.tight_layout()
    fig.savefig(FIG / "fig3_1_distributions_cibles.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 3.3 : corrélations (Spearman) entre variables budgétaires et cibles
# ---------------------------------------------------------------------------
def fig_correlations(df: pd.DataFrame) -> pd.DataFrame:
    feats = {f"{k}_ytd_gap": v for k, v in BUDGET_LABELS.items()}
    sub = df[list(feats) + list(TARGETS)].dropna()
    n = len(sub)
    corr = sub.corr(method="spearman").loc[list(feats), list(TARGETS)]
    band = 1.96 / np.sqrt(n)  # seuil approximatif de significativité à 5 %

    fig, axes = plt.subplots(1, 3, figsize=(10, 3.6), sharey=True)
    ypos = np.arange(len(feats))
    for ax, (col, label) in zip(axes, TARGETS.items()):
        ax.axvspan(-band, band, color=GRID, alpha=0.7, lw=0, zorder=0)
        ax.barh(ypos, corr[col].values, height=0.6, color=BLUE, edgecolor="white", linewidth=2)
        ax.axvline(0, color=INK2, lw=0.8)
        ax.set_xlim(-0.35, 0.35)
        ax.set_title(label, fontsize=9.5)
        ax.grid(axis="y", visible=False)
        for y, v in zip(ypos, corr[col].values):
            if abs(v) > band:
                ax.text(v + (0.01 if v > 0 else -0.01), y, f"{v:.2f}", va="center",
                        ha="left" if v > 0 else "right", fontsize=8, color=INK)
    axes[0].set_yticks(ypos)
    axes[0].set_yticklabels(list(feats.values()))
    axes[0].invert_yaxis()
    fig.text(0, -0.04, f"Corrélation de Spearman, n = {n} mois. Zone grise : non significatif à 5 % "
             f"(±{band:.2f}). Variables budgétaires : écart sur un an, décalées de 2 mois.",
             fontsize=8, color=INK2)
    fig.tight_layout()
    fig.savefig(FIG / "fig3_1_correlations_budget.png")
    plt.close(fig)

    out = corr.rename(index=feats).round(3)
    out.to_csv(TAB / "eda_correlations_budget.csv")
    return out


def partial_correlations(df: pd.DataFrame) -> pd.DataFrame:
    """Corrélation de Spearman partielle budget / cible, en retirant l'inflation (IPCH t-1) et la variation passée
    de la cible (les deux sont dans M0). Méthode : corrélation de Pearson entre les résidus des rangs après
    régression sur les rangs des contrôles (même calcul que src/21_verif_chiffres_03.py)."""
    from scipy import stats
    feats = {f"{k}_ytd_gap": v for k, v in BUDGET_LABELS.items()}
    rows = []
    lagged = {"y_d_spread": "d_spread", "y_d_oat": "d_oat", "y_cac_ret": "cac_ret"}
    for t in TARGETS:
        ctrl = ["inflation_yoy", lagged[t]]
        sub = df[list(feats) + [t] + ctrl].dropna().rank()
        X = np.c_[np.ones(len(sub)), sub[ctrl]]
        res = lambda c: sub[c] - X @ np.linalg.lstsq(X, sub[c], rcond=None)[0]
        n = len(sub)
        for f, lab in feats.items():
            rho = np.corrcoef(res(f), res(t))[0, 1]
            tstat = rho * np.sqrt((n - 4) / (1 - rho ** 2))
            rows.append({"cible": t, "variable": lab, "rho_partiel": rho,
                         "p": 2 * (1 - stats.t.cdf(abs(tstat), n - 4)), "n": n})
    out = pd.DataFrame(rows).round(3)
    out.to_csv(TAB / "eda_correlations_partielles.csv", index=False)
    return out


# ---------------------------------------------------------------------------
# Tableau : statistiques descriptives, stationnarité, autocorrélation
# ---------------------------------------------------------------------------
def stats_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    cols = list(TARGETS) + ["spread_bp", "oat_10y", "b_solde_12m", "b_dep_charge_dette_12m"]
    for col in cols:
        y = df[col].dropna()
        adf_p = adfuller(y, autolag="AIC")[1]
        ac1 = acf(y, nlags=1, fft=False)[1]
        rows.append({
            "variable": col, "n": len(y), "moyenne": y.mean(), "ecart_type": y.std(),
            "min": y.min(), "max": y.max(), "autocorr_1": ac1, "adf_pvalue": adf_p,
            "stationnaire_5pct": adf_p < 0.05,
        })
    out = pd.DataFrame(rows).set_index("variable").round(3)
    out.to_csv(TAB / "eda_statistiques.csv")
    return out


if __name__ == "__main__":
    df = load()
    fig_spread_budget(df)
    fig_target_distributions(df)
    corr = fig_correlations(df)
    stats = stats_table(df)
    part = partial_correlations(df)
    pd.set_option("display.width", 160)
    print("Corrélations partielles (inflation et variation passée retirées) :\n", part, "\n")
    print("Statistiques descriptives et stationnarité :\n", stats, "\n")
    print("Corrélations de Spearman (budget t-2 / cibles t+1) :\n", corr)
    print(f"\nFigures enregistrées dans {FIG}/, tableaux dans {TAB}/")
