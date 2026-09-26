"""
07_extensions_summary.py
Figure et tableau de synthèse des extensions (section 3.6).

Pour chaque extension et chaque cible : meilleur R² hors échantillon SANS dépenses (sur les modèles
testés) et meilleur R² AVEC dépenses. Un point à droite de 0 = mieux que la moyenne historique.
Entrées : results/tables/models_metrics.csv, results/tables/ext_summary.csv
Sorties : results/figures/fig3_5_extensions.png, results/tables/ext_synthese.csv
"""
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BLUE, ORANGE, INK2, GRID = "#2a78d6", "#eb6834", "#52514e", "#e4e3df"
TARGETS = {"y_d_spread": "Δ spread OAT–Bund", "y_d_oat": "Δ OAT 10 ans", "y_cac_ret": "Rendement CAC 40"}
plt.rcParams.update({"font.size": 9.5, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.titleweight": "bold", "axes.titlelocation": "left", "axes.titlesize": 10.5,
                     "legend.frameon": False, "savefig.dpi": 200, "savefig.bbox": "tight"})

LABELS = {
    "E0": "Modèle principal (h = 1 mois)",
    "E1 h=3": "E1 Horizon 3 mois", "E1 h=6": "E1 Horizon 6 mois", "E1 h=12": "E1 Horizon 12 mois",
    "E2": "E2 Hausse/baisse (Brier)", "E3": "E3 Volatilité", "E4": "E4 Surprise budgétaire",
    "E5": "E5 Interactions régime", "E6": "E6 Variables réduites / ACP", "E7": "E7 Prévisions tempérées",
    "E8": "E8 Combinaison", "E9": "E9 Elastic Net", "E10": "E10 XGBoost réglé",
    "E11": "E11 Fenêtre 60 mois", "E13": "E13 Notations",
}


def key(row):
    ext = row["extension"].split()[0]
    if ext == "E1":
        h = re.search(r"h=(\d+)", row["comparaison"]).group(1)
        return f"E1 h={h}"
    return ext


def main():
    m = pd.read_csv("results/tables/models_metrics.csv")
    rows = []
    for t in TARGETS:
        mm = m[m.cible == t]
        rows.append({"cle": "E0", "cible": t,
                     "sans": mm[mm.variables == "M0 marchés"]["R2_oos_%"].max(),
                     "avec": mm[mm.variables == "M1 + dépenses"]["R2_oos_%"].max(),
                     "p_min_BH": np.nan})
    s = pd.read_csv("results/tables/ext_summary.csv")
    s = s[~s.extension.str.startswith("E12")].copy()
    s["cle"] = s.apply(key, axis=1)
    g = s.groupby(["cle", "cible"]).agg(sans=("R2oos_sans_%", "max"), avec=("R2oos_avec_%", "max"),
                                        p_min_BH=("p_BH", "min")).reset_index()
    syn = pd.concat([pd.DataFrame(rows), g], ignore_index=True)
    order = [k for k in LABELS if k in set(syn.cle)]
    syn["ordre"] = syn.cle.map({k: i for i, k in enumerate(order)})
    syn = syn.sort_values(["cible", "ordre"])
    syn.round(2).to_csv("results/tables/ext_synthese.csv", index=False)

    fig, axes = plt.subplots(1, 3, figsize=(12, 0.42 * len(order) + 1.2), sharey=True)
    y = np.arange(len(order))
    for ax, (t, lab) in zip(axes, TARGETS.items()):
        d = syn[syn.cible == t].set_index("cle").reindex(order)
        lo = np.clip(d[["sans", "avec"]].min(axis=1), -40, None)
        hi = np.clip(d[["sans", "avec"]].max(axis=1), -40, None)
        ax.hlines(y, lo, hi, color=GRID, lw=3, zorder=1)
        for col, color, leg, dy in (("sans", BLUE, "Sans dépenses", -0.12), ("avec", ORANGE, "Avec dépenses", 0.12)):
            v = d[col].values
            cut = v < -40
            ax.scatter(np.where(cut, np.nan, v), y + dy * 0, s=42, color=color, zorder=3, label=leg,
                       edgecolor="white", linewidth=1.5)
            ax.scatter(np.full(cut.sum(), -40), y[cut] + dy, s=46, color=color, marker="<", zorder=3)
            for yy, vv in zip(y[cut], v[cut]):
                ax.text(-38.5, yy + dy, f"{vv:.0f}", fontsize=7, color=color, va="center")
        ax.axvline(0, color=INK2, lw=1, ls="--")
        ax.set_xlim(-42, 17)
        ax.set_title(lab)
        ax.grid(axis="x", color=GRID)
        ax.set_xlabel("R² hors échantillon (%)")
    axes[0].set_yticks(y)
    axes[0].set_yticklabels([LABELS[k] for k in order])
    axes[0].invert_yaxis()
    axes[0].legend(loc="lower left", fontsize=8.5)
    fig.text(0, -0.03, "Meilleur modèle de chaque configuration. À droite de la ligne pointillée = meilleur que "
             "la moyenne historique. Triangles : valeurs sous -40 % (valeur indiquée). Test 2020-01 → 2026-07 "
             "(E4 : → 2026-02).", fontsize=8, color=INK2)
    fig.tight_layout()
    fig.savefig("results/figures/fig3_5_extensions.png")
    print(syn.round(2).to_string(index=False))


if __name__ == "__main__":
    main()
