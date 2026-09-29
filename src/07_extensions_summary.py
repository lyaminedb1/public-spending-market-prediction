"""
07_extensions_summary.py
Figure et tableau de synthèse des extensions (section 3.6).

Pour chaque extension et chaque cible : meilleur R² hors échantillon SANS dépenses (sur les modèles
testés) et meilleur R² AVEC dépenses. Un point à droite de 0 = mieux que la moyenne historique.
Couvre E0 (modèle principal), E1-E13 et E20 (3 cibles françaises) ainsi que E15-E19 (autres cibles : panel de
spreads européens, actions sectorielles). Pour le panel (E15-E18), le gain contre la marche aléatoire est aussi
donné : c'est la référence exigeante (R² contre la moyenne = 90-97 % sur le niveau d'E16, mais négatif face à la
marche aléatoire).
Entrées : results/tables/models_metrics.csv, results/tables/ext_summary.csv
Sorties : results/figures/fig3_5_extensions.png (3 cibles françaises), results/figures/fig3_6_extensions_autres.png
          (panel et actions), results/tables/ext_synthese.csv
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
    "E20a": "E20 Incertitude politique (M0+EPU vs M0)", "E20b": "E20 Dépenses | incertitude (M1+EPU vs M0+EPU)",
}
# extensions dont la cible n'est pas l'une des trois cibles françaises : (clé, cible dans ext_summary) -> libellé
OTHER = {
    ("E15", "Δ spread trimestriel (5 pays)"): "E15 Panel trimestriel (moyennes)",
    ("E16", "spread niveau"): "E16 Panel mensuel, niveau du spread",
    ("E16", "spread variation"): "E16 Panel mensuel, variation du spread",
    ("E17", "Δ spread annuel (5 pays)"): "E17 Panel annuel (décembre)",
    ("E18", "Δ spread trimestriel fin de trimestre (5 pays)"): "E18 Panel, régime de crise (exploratoire)",
    ("E19", "btp_concessions (excès CAC 40)"): "E19 Actions BTP-concessions (excès CAC 40)",
    ("E19", "defense (excès CAC 40)"): "E19 Actions défense (excès CAC 40)",
}
XCOL = {"sans": ["R2oos_sans_%", "R2_vs_moyenne_sans_%"], "avec": ["R2oos_avec_%", "R2_vs_moyenne_avec_%"]}


def key(row):
    ext = row["extension"].split()[0]
    if ext == "E1":
        h = re.search(r"h=(\d+)", row["comparaison"]).group(1)
        return f"E1 h={h}"
    return ext


def first_col(df, names):
    """Première colonne existante non vide de la liste (E16 nomme ses R² autrement)."""
    out = pd.Series(np.nan, index=df.index)
    for n in names:
        if n in df:
            out = out.fillna(df[n])
    return out


def build():
    m = pd.read_csv("results/tables/models_metrics.csv")
    rows = []
    for t in TARGETS:
        mm = m[m.cible == t]
        rows.append({"cle": "E0", "cible": t,
                     "sans": mm[mm.variables == "M0 marchés"]["R2_oos_%"].max(),
                     "avec": mm[mm.variables == "M1 + dépenses"]["R2_oos_%"].max(),
                     "p_min_BH": np.nan})
    s = pd.read_csv("results/tables/ext_summary.csv")
    # ventilations (E12, sous-périodes d'E18) : hors correction, ce ne sont pas des tests indépendants
    s = s[~s.extension.str.startswith("E12") & ~s.extension.str.contains("hors correction")].copy()
    s["cle"] = s.apply(key, axis=1)
    s["sans"], s["avec"] = first_col(s, XCOL["sans"]), first_col(s, XCOL["avec"])
    s["mrw_sans"] = s.get("gain_vs_marche_aleatoire_sans_%", np.nan)
    s["mrw_avec"] = s.get("gain_vs_marche_aleatoire_avec_%", np.nan)
    g = s.groupby(["cle", "cible"]).agg(sans=("sans", "max"), avec=("avec", "max"), mrw_sans=("mrw_sans", "max"),
                                        mrw_avec=("mrw_avec", "max"), p_min_BH=("p_BH", "min"),
                                        n_comparaisons=("p_BH", "size")).reset_index()
    syn = pd.concat([pd.DataFrame(rows), g], ignore_index=True)
    order = [k for k in LABELS if k in set(syn.cle)]
    syn["ordre"] = np.nan
    for i, k in enumerate(order):
        syn.loc[syn.cle == k, "ordre"] = i
    other_keys = list(OTHER)
    for j, (k, c) in enumerate(other_keys):
        syn.loc[(syn.cle == k) & (syn.cible == c), "ordre"] = 100 + j
    syn["libelle"] = [LABELS.get(k) if c in TARGETS else OTHER.get((k, c)) for k, c in zip(syn.cle, syn.cible)]
    return syn, order, other_keys


def dot_panel(ax, d, y, xlim, colors=(("sans", BLUE, "Sans dépenses", -0.13), ("avec", ORANGE, "Avec dépenses", 0.13))):
    lo_, hi_ = xlim
    v = d[[c[0] for c in colors]]
    ax.hlines(y, np.clip(v.min(axis=1), lo_, hi_), np.clip(v.max(axis=1), lo_, hi_), color=GRID, lw=3, zorder=1)
    for col, color, leg, dy in colors:
        x = d[col].values
        low, high = x < lo_, x > hi_
        ax.scatter(np.where(low | high | np.isnan(x), np.nan, x), y, s=42, color=color, zorder=3, label=leg,
                   edgecolor="white", linewidth=1.5)
        ax.scatter(np.full(low.sum(), lo_), y[low] + dy, s=46, color=color, marker="<", zorder=3)
        ax.scatter(np.full(high.sum(), hi_), y[high] + dy, s=46, color=color, marker=">", zorder=3)
        for yy, vv in zip(y[low], x[low]):
            ax.text(lo_ + 1.5, yy + dy, f"{vv:.0f}", fontsize=7, color=color, va="center")
        for yy, vv in zip(y[high], x[high]):
            ax.text(hi_ - 1.5, yy + dy, f"{vv:.0f}", fontsize=7, color=color, va="center", ha="right")
    ax.axvline(0, color=INK2, lw=1, ls="--")
    ax.set_xlim(lo_ - 2, hi_ + 2)
    ax.grid(axis="x", color=GRID)


def main():
    syn, order, other_keys = build()
    out = syn.sort_values(["ordre", "cible"])[["cle", "cible", "libelle", "sans", "avec", "mrw_sans", "mrw_avec",
                                                 "p_min_BH", "n_comparaisons", "ordre"]]
    out.round(2).to_csv("results/tables/ext_synthese.csv", index=False)

    # ---- figure 3.5 : les 3 cibles françaises (E0-E13, E20)
    fig, axes = plt.subplots(1, 3, figsize=(12, 0.42 * len(order) + 1.2), sharey=True)
    y = np.arange(len(order))
    for ax, (t, lab) in zip(axes, TARGETS.items()):
        d = syn[syn.cible == t].set_index("cle").reindex(order)
        dot_panel(ax, d, y, (-40, 15))
        ax.set_title(lab)
        ax.set_xlabel("R² hors échantillon (%)")
    axes[0].set_yticks(y)
    axes[0].set_yticklabels([LABELS[k] for k in order])
    axes[0].invert_yaxis()
    axes[0].legend(loc="lower left", fontsize=8.5)
    fig.text(0, -0.03, "Meilleur modèle de chaque configuration. À droite de la ligne pointillée = meilleur que "
             "la moyenne historique. Triangles : valeurs hors de l'échelle (valeur indiquée). Test 2020-01 → 2026-07 "
             "(E4 : → 2026-02).", fontsize=8, color=INK2)
    fig.tight_layout()
    fig.savefig("results/figures/fig3_5_extensions.png")
    plt.close(fig)

    # ---- figure 3.6 : panel européen et actions sectorielles (autres cibles)
    o = syn[[(k, c) in OTHER for k, c in zip(syn.cle, syn.cible)]].sort_values("ordre").reset_index(drop=True)
    fig, axes = plt.subplots(1, 2, figsize=(12, 0.5 * len(o) + 1.6), sharey=True)
    y = np.arange(len(o))
    dot_panel(axes[0], o, y, (-40, 20))
    axes[0].set_title("R² hors échantillon contre la moyenne historique (%)")
    dot_panel(axes[1], o.assign(sans=o.mrw_sans, avec=o.mrw_avec), y, (-40, 20))
    axes[1].set_title("Gain contre la marche aléatoire (%) — panel seulement")
    axes[0].set_yticks(y)
    axes[0].set_yticklabels(o.libelle)
    axes[0].invert_yaxis()
    axes[0].legend(loc="lower left", fontsize=8.5)
    fig.text(0, -0.02, "Meilleur modèle de chaque configuration ; triangles : hors échelle (E16 niveau : 90 % et plus "
             "contre la moyenne, mais négatif contre la marche aléatoire). Périodes de test : E15 2010T1, E16 2012-01, E17 "
             "2010-2024, E18 2010T1 (exploratoire), E19 2020-01 → 2026-07. E15 : gain apparent dû à l'autocorrélation mécanique des "
             "moyennes trimestrielles (il disparaît en fin de trimestre).", fontsize=8, color=INK2)
    fig.tight_layout()
    fig.savefig("results/figures/fig3_6_extensions_autres.png")
    plt.close(fig)
    pd.set_option("display.width", 220)
    print(out.round(2).to_string(index=False))


if __name__ == "__main__":
    main()
