"""
04_models.py
Modélisation : les dépenses publiques améliorent-elles la prévision des marchés ? (chapitre 3)

Protocole
- 3 cibles (mois suivant) : Δ spread OAT–Bund, Δ OAT 10 ans, rendement CAC 40.
- 3 jeux de variables, emboîtés :
    M0 « marchés »        : valeurs passées des 3 indicateurs, VIX, inflation, taux BCE
    M1 « + dépenses »     : M0 + dépenses de l'État par titre (écart sur un an, t-2)
    M2 « + budget complet »: M1 + recettes et solde budgétaire
  La comparaison M1 vs M0 teste H1 (apport des dépenses).
- Modèles : naïf (moyenne historique ; zéro), Ridge, forêt aléatoire, XGBoost.
  Hyperparamètres fixés a priori (pas d'optimisation sur la période de test).
- Validation glissante à fenêtre croissante : entraînement 2014-03 → mois t-1, prévision du mois t,
  premier mois de test = 2020-01, réestimation chaque mois.
- Évaluation : RMSE, MAE, R² hors échantillon (vs moyenne historique), taux de bonne direction,
  test de Diebold-Mariano (correction Harvey-Leybourne-Newbold).
- Importance des variables : valeurs SHAP de XGBoost estimé sur tout l'échantillon.

Lancer depuis la racine du dépôt :  python src/04_models.py
"""

from pathlib import Path
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import RidgeCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor

warnings.filterwarnings("ignore")

DATA = Path("data/processed/dataset_monthly.csv")
FIG = Path("results/figures")
TAB = Path("results/tables")
FIG.mkdir(parents=True, exist_ok=True)
TAB.mkdir(parents=True, exist_ok=True)

TEST_START = "2020-01"
SEED = 42

TARGETS = {
    "y_d_spread": "Δ spread OAT–Bund (pb)",
    "y_d_oat": "Δ OAT 10 ans (pb)",
    "y_cac_ret": "Rendement CAC 40 (%)",
}

MARKETS = ["d_spread", "d_spread_l1", "spread_bp", "d_oat", "d_oat_l1", "cac_ret", "cac_ret_l1",
           "vix", "d_vix", "inflation_yoy", "ecb_dfr"]
SPENDING = ["b_dep_totales_ytd_gap", "b_dep_personnel_ytd_gap", "b_dep_fonctionnement_ytd_gap",
            "b_dep_charge_dette_ytd_gap", "b_dep_investissement_ytd_gap", "b_dep_intervention_ytd_gap",
            "b_psr_total_ytd_gap"]
OTHER_BUDGET = ["b_rec_totales_ytd_gap", "b_rec_fiscales_ytd_gap", "b_solde_ytd_diff_yoy"]

FEATURE_SETS = {
    "M0 marchés": MARKETS,
    "M1 + dépenses": MARKETS + SPENDING,
    "M2 + budget complet": MARKETS + SPENDING + OTHER_BUDGET,
}

MODEL_LABELS = {"ridge": "Ridge", "rf": "Forêt aléatoire", "xgb": "XGBoost"}


def make_model(name: str):
    if name == "ridge":
        return make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-2, 6, 40)))
    if name == "rf":
        return RandomForestRegressor(n_estimators=300, max_depth=4, min_samples_leaf=5,
                                     max_features=0.5, random_state=SEED, n_jobs=-1)
    if name == "xgb":
        return XGBRegressor(n_estimators=200, max_depth=2, learning_rate=0.05, subsample=0.8,
                            colsample_bytree=0.8, min_child_weight=5, reg_lambda=1.0,
                            random_state=SEED, n_jobs=1, verbosity=0)
    raise ValueError(name)


# ---------------------------------------------------------------------------
# Validation glissante
# ---------------------------------------------------------------------------
def walk_forward(df: pd.DataFrame, target: str) -> pd.DataFrame:
    """Renvoie un tableau (mois de test x prévisions) pour tous les modèles et jeux de variables."""
    test_idx = df.index[df.index >= TEST_START]
    preds = {"y_true": df.loc[test_idx, target]}
    preds["naif_moyenne"] = pd.Series(
        [df.loc[df.index < m, target].mean() for m in test_idx], index=test_idx)
    preds["naif_zero"] = pd.Series(0.0, index=test_idx)

    for set_name, cols in FEATURE_SETS.items():
        for model_name in MODEL_LABELS:
            out = []
            for m in test_idx:
                train = df[df.index < m]
                model = make_model(model_name)
                model.fit(train[cols], train[target])
                out.append(model.predict(df.loc[[m], cols])[0])
            preds[f"{model_name}|{set_name}"] = pd.Series(out, index=test_idx)
    return pd.DataFrame(preds)


# ---------------------------------------------------------------------------
# Évaluation
# ---------------------------------------------------------------------------
def diebold_mariano(e1: np.ndarray, e2: np.ndarray) -> tuple[float, float, float]:
    """DM avec correction HLN, horizon 1, perte quadratique.
    Statistique > 0 : le modèle 2 fait mieux que le modèle 1.
    Renvoie (statistique, p-value bilatérale, p-value unilatérale « modèle 2 meilleur »)."""
    d = e1 ** 2 - e2 ** 2
    T = len(d)
    dm = d.mean() / np.sqrt(d.var(ddof=0) / T)
    dm *= np.sqrt((T - 1) / T)  # HLN, h = 1
    p_two = 2 * (1 - stats.t.cdf(abs(dm), df=T - 1))
    p_one = 1 - stats.t.cdf(dm, df=T - 1)
    return dm, p_two, p_one


def metrics(preds: pd.DataFrame, target: str) -> pd.DataFrame:
    y = preds["y_true"].values
    sse_mean = ((y - preds["naif_moyenne"].values) ** 2).sum()
    rows = []
    for col in preds.columns.drop("y_true"):
        p = preds[col].values
        e = y - p
        model, _, fset = col.partition("|")
        nonzero = y != 0
        rows.append({
            "cible": target,
            "modele": model,
            "variables": fset or "—",
            "RMSE": np.sqrt((e ** 2).mean()),
            "MAE": np.abs(e).mean(),
            "R2_oos_%": (1 - (e ** 2).sum() / sse_mean) * 100,
            "bonne_direction_%": (np.sign(p[nonzero]) == np.sign(y[nonzero])).mean() * 100
            if model != "naif_zero" else np.nan,
        })
    return pd.DataFrame(rows)


def dm_tests(preds: pd.DataFrame, target: str) -> pd.DataFrame:
    y = preds["y_true"].values
    err = lambda c: y - preds[c].values
    rows = []
    for model in MODEL_LABELS:
        base = f"{model}|M0 marchés"
        for other in ["M1 + dépenses", "M2 + budget complet"]:
            s, p2, p1 = diebold_mariano(err(base), err(f"{model}|{other}"))
            rows.append({"cible": target, "test": f"{MODEL_LABELS[model]} : {other} vs M0",
                         "DM": s, "p_bilaterale": p2, "p_unilaterale": p1})
        # chaque modèle contre la moyenne historique (jeu M1)
        s, p2, p1 = diebold_mariano(err("naif_moyenne"), err(f"{model}|M1 + dépenses"))
        rows.append({"cible": target, "test": f"{MODEL_LABELS[model]} M1 vs moyenne historique",
                     "DM": s, "p_bilaterale": p2, "p_unilaterale": p1})
    # H3 : ML contre linéaire (jeu M1)
    for model in ["rf", "xgb"]:
        s, p2, p1 = diebold_mariano(err("ridge|M1 + dépenses"), err(f"{model}|M1 + dépenses"))
        rows.append({"cible": target, "test": f"{MODEL_LABELS[model]} vs Ridge (M1)",
                     "DM": s, "p_bilaterale": p2, "p_unilaterale": p1})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Importance des variables (SHAP, XGBoost, jeu M1, tout l'échantillon)
# ---------------------------------------------------------------------------
def shap_importance(df: pd.DataFrame) -> pd.DataFrame:
    import shap
    cols = FEATURE_SETS["M1 + dépenses"]
    res = {}
    for target in TARGETS:
        model = make_model("xgb").fit(df[cols], df[target])
        sv = shap.TreeExplainer(model).shap_values(df[cols])
        res[target] = np.abs(sv).mean(axis=0)
    out = pd.DataFrame(res, index=cols)
    out.to_csv(TAB / "models_shap_importance.csv")
    return out


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK2, GRID = "#52514e", "#e4e3df"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "axes.axisbelow": True,
                     "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "legend.frameon": False, "savefig.dpi": 200, "savefig.bbox": "tight"})


def fig_relative_rmse(met: pd.DataFrame) -> None:
    """RMSE relatif à la moyenne historique (< 1 = meilleur que la moyenne)."""
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.6), sharey=True)
    colors = dict(zip(FEATURE_SETS, [BLUE, ORANGE, AQUA]))
    w = 0.26
    for ax, (target, label) in zip(axes, TARGETS.items()):
        m = met[met.cible == target]
        ref = m.loc[m.modele == "naif_moyenne", "RMSE"].iloc[0]
        x = np.arange(len(MODEL_LABELS))
        for k, fset in enumerate(FEATURE_SETS):
            vals = [m[(m.modele == mod) & (m.variables == fset)]["RMSE"].iloc[0] / ref for mod in MODEL_LABELS]
            ax.bar(x + (k - 1) * w, vals, width=w, color=colors[fset], edgecolor="white", linewidth=1.5,
                   label=fset)
        ax.axhline(1, color=INK2, lw=1, ls="--")
        ax.set_xticks(x)
        ax.set_xticklabels(MODEL_LABELS.values())
        ax.set_title(label)
        ax.set_ylim(0.8, 1.2)
        ax.grid(axis="x", visible=False)
    axes[0].set_ylabel("RMSE / RMSE moyenne historique")
    axes[0].legend(loc="upper left", fontsize=8.5)
    fig.text(0, -0.05, f"Validation glissante, test {TEST_START} → 2026-07. Ligne pointillée : moyenne historique "
             "(sous 1 = meilleur que la moyenne).", fontsize=8, color=INK2)
    fig.tight_layout()
    fig.savefig(FIG / "fig3_2_rmse_relatif.png")
    plt.close(fig)


def fig_shap(imp: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.2))
    for ax, (target, label) in zip(axes, TARGETS.items()):
        s = imp[target].sort_values()
        colors = [ORANGE if c in SPENDING else BLUE for c in s.index]
        ax.barh(range(len(s)), s.values, color=colors, edgecolor="white", linewidth=1.5, height=0.7)
        ax.set_yticks(range(len(s)))
        ax.set_yticklabels([c.replace("b_dep_", "dép. ").replace("b_psr_total", "prélèv. recettes")
                            .replace("_ytd_gap", "") for c in s.index], fontsize=7.5)
        ax.set_title(label)
        ax.grid(axis="y", visible=False)
    handles = [plt.Rectangle((0, 0), 1, 1, color=BLUE), plt.Rectangle((0, 0), 1, 1, color=ORANGE)]
    fig.legend(handles, ["Marchés et macro", "Dépenses publiques"], loc="lower center", ncol=2,
               bbox_to_anchor=(0.5, -0.06))
    fig.text(0, -0.1, "Valeur SHAP absolue moyenne, XGBoost estimé sur tout l'échantillon, jeu M1.",
             fontsize=8, color=INK2)
    fig.tight_layout()
    fig.savefig(FIG / "fig3_3_importance_shap.png")
    plt.close(fig)


def fig_predictions(all_preds: dict) -> None:
    p = all_preds["y_d_spread"]
    t = pd.PeriodIndex(p.index, freq="M").to_timestamp()
    fig, ax = plt.subplots(figsize=(10, 3.6))
    ax.bar(t, p["y_true"], width=20, color=GRID, label="Variation observée")
    ax.plot(t, p["xgb|M0 marchés"], color=BLUE, lw=1.8, label="XGBoost M0 marchés")
    ax.plot(t, p["xgb|M1 + dépenses"], color=ORANGE, lw=1.8, label="XGBoost M1 + dépenses")
    ax.axhline(0, color=INK2, lw=0.8)
    ax.set_ylabel("points de base")
    ax.set_title("Variation mensuelle du spread OAT–Bund : observée et prévue (hors échantillon)")
    ax.legend(ncol=3, loc="upper left", fontsize=8.5)
    fig.savefig(FIG / "fig3_4_previsions_spread.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
def main() -> None:
    df = pd.read_csv(DATA, index_col="mois")
    df = df.dropna(subset=list(TARGETS))  # la dernière ligne n'a pas de cible

    all_preds, all_met, all_dm = {}, [], []
    for target in TARGETS:
        print(f"Validation glissante : {target} …", flush=True)
        preds = walk_forward(df, target)
        preds.to_csv(TAB / f"models_predictions_{target}.csv")
        all_preds[target] = preds
        all_met.append(metrics(preds, target))
        all_dm.append(dm_tests(preds, target))

    met = pd.concat(all_met).round(3)
    dm = pd.concat(all_dm).round(3)
    met.to_csv(TAB / "models_metrics.csv", index=False)
    dm.to_csv(TAB / "models_dm_tests.csv", index=False)

    imp = shap_importance(df)
    fig_relative_rmse(met)
    fig_shap(imp)
    fig_predictions(all_preds)

    pd.set_option("display.width", 200)
    pd.set_option("display.max_rows", 100)
    n_test = len(all_preds["y_d_spread"])
    print(f"\nPériode de test : {TEST_START} → {df.index[-1]} ({n_test} mois)\n")
    print(met.to_string(index=False))
    print("\nTests de Diebold-Mariano (DM > 0 : le second modèle fait mieux)\n")
    print(dm.to_string(index=False))
    grp = pd.DataFrame({t: [imp.loc[SPENDING, t].sum() / imp[t].sum() * 100] for t in TARGETS},
                       index=["part des dépenses dans l'importance SHAP (%)"]).round(1)
    print("\n", grp.to_string())


if __name__ == "__main__":
    main()
