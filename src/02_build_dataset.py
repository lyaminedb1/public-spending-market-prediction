"""
02_build_dataset.py
Construit le jeu de données mensuel du mémoire à partir des fichiers bruts.

Entrées  : data/raw/*.csv (marchés, contrôles) et data/raw/budget/ (situations mensuelles budgétaires)
Sortie   : data/processed/dataset_monthly.csv  (une ligne par mois t)

Convention temporelle (ligne = fin du mois t) :
- cibles      : variation entre t et t+1 (mois suivant)
- marchés     : valeurs connues à la fin du mois t
- inflation   : IPCH du mois t-1 (le mois t n'est publié en version définitive qu'en t+1)
- budget      : données du mois t-2 (la situation du mois M est publiée début M+2,
                ex. juin 2026 publié le 4 août 2026) -> pas de biais d'anticipation

Lancer depuis la racine du dépôt :  python src/02_build_dataset.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

RAW = Path("data/raw")
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)

BUDGET_LAG = 2  # mois

# ---------------------------------------------------------------------------
# 1. Budget de l'État : situations mensuelles budgétaires (cumuls depuis janvier, en euros)
# ---------------------------------------------------------------------------
BUDGET_FILES = [
    "Séries longues SMB_DGFiP_2013-2023.csv",
    "Serie longue SMB_DGFiP_2024-xx.csv",
]

# Nom court de chaque ligne retenue
BUDGET_LINES = {
    "Solde budgétaire": "solde",
    "Total dépenses nettes du budget général": "dep_totales",
    "Dépenses de personnel": "dep_personnel",
    "Dépenses de fonctionnement": "dep_fonctionnement",
    "Charges de la dette de l’Etat": "dep_charge_dette",
    "Dépenses d’investissement": "dep_investissement",
    "Dépenses d’intervention": "dep_intervention",
    "Total prélèvements sur recettes": "psr_total",
    "Total recettes nettes du budget général": "rec_totales",
    "Total recettes fiscales": "rec_fiscales",
    "Impôt sur les sociétés": "rec_is",
    "Taxe sur la valeur ajoutée": "rec_tva",
}
SPENDING = [v for v in BUDGET_LINES.values() if v.startswith(("dep_", "psr_"))]
CONTROLS_BUDGET = ["solde", "rec_totales", "rec_fiscales", "rec_is", "rec_tva"]


def read_budget_file(path: Path) -> pd.DataFrame:
    """Lit un fichier SMB (UTF-16, ';', virgule décimale) et renvoie un tableau mois x ligne."""
    df = pd.read_csv(path, sep=";", encoding="utf-16", decimal=",")
    df = df.dropna(subset=["Ligne d'information"])
    df["ligne"] = df["Ligne d'information"].str.strip()
    date_cols = [c for c in df.columns if isinstance(c, str) and c.count("/") == 2]
    long = df.melt(id_vars="ligne", value_vars=date_cols, var_name="date", value_name="valeur")
    long["mois"] = pd.to_datetime(long["date"], format="%d/%m/%Y").dt.to_period("M")
    long["valeur"] = pd.to_numeric(long["valeur"], errors="coerce")
    return long.pivot_table(index="mois", columns="ligne", values="valeur", aggfunc="first")


def build_budget() -> pd.DataFrame:
    parts = [read_budget_file(RAW / "budget" / f) for f in BUDGET_FILES]
    cumul = pd.concat(parts).sort_index()
    cumul = cumul[~cumul.index.duplicated(keep="last")]
    missing = set(BUDGET_LINES) - set(cumul.columns)
    if missing:
        raise ValueError(f"Lignes budgétaires introuvables : {missing}")
    cumul = cumul[list(BUDGET_LINES)].rename(columns=BUDGET_LINES) / 1e9  # en milliards d'euros

    full = pd.period_range(cumul.index.min(), cumul.index.max(), freq="M")
    if len(full) != len(cumul):
        raise ValueError("Mois manquants dans les données budgétaires")

    feats = pd.DataFrame(index=cumul.index)
    same_month_last_year = cumul.shift(12)
    for col in cumul.columns:
        # Flux mensuel : différence des cumuls au sein d'une même année (janvier = cumul de janvier)
        flow = cumul[col].diff()
        flow[cumul.index.month == 1] = cumul[col][cumul.index.month == 1]
        # Somme glissante sur 12 mois (niveau annuel, sans saisonnalité)
        feats[f"{col}_12m"] = flow.rolling(12).sum()
        # Écart du cumul depuis janvier par rapport au même mois de l'année précédente,
        # en % du total annuel (12 mois glissants). Un taux de croissance classique explose
        # en début d'année quand le cumul est proche de zéro (ex. impôt sur les sociétés).
        if col != "solde":
            feats[f"{col}_ytd_gap"] = (
                (cumul[col] - same_month_last_year[col]) / feats[f"{col}_12m"].abs() * 100
            )
    # Le solde est négatif : on suit sa variation sur un an en milliards
    feats["solde_ytd_diff_yoy"] = cumul["solde"] - same_month_last_year["solde"]
    # Part de la charge de la dette dans les dépenses (12 mois glissants)
    feats["part_charge_dette_12m"] = feats["dep_charge_dette_12m"] / feats["dep_totales_12m"] * 100
    return feats


# ---------------------------------------------------------------------------
# 2. Marchés et contrôles
# ---------------------------------------------------------------------------
def read_raw(name: str) -> pd.Series:
    s = pd.read_csv(RAW / f"{name}.csv", index_col="date", parse_dates=True).iloc[:, 0]
    return s.dropna()


def build_markets() -> pd.DataFrame:
    m = pd.DataFrame()
    # Taux souverains FRED/OCDE : moyennes mensuelles, date au 1er du mois
    m["oat_10y"] = read_raw("oat_10y").to_period("M").groupby(level=0).last()
    m["bund_10y"] = read_raw("bund_10y").to_period("M").groupby(level=0).last()
    m["spread_bp"] = (m["oat_10y"] - m["bund_10y"]) * 100

    # CAC 40 : dernier cours du mois
    cac = read_raw("cac40")
    m["cac40"] = cac.groupby(cac.index.to_period("M")).last()

    # VIX : moyenne mensuelle
    vix = read_raw("vix")
    m["vix"] = vix.groupby(vix.index.to_period("M")).mean()

    # Inflation France sur un an (IPCH)
    hicp = read_raw("hicp_fr").to_period("M").groupby(level=0).last()
    m["inflation_yoy"] = (hicp / hicp.shift(12) - 1) * 100

    # Taux BCE : publiés à chaque décision -> valeur en vigueur en fin de mois
    for name in ["ecb_mro", "ecb_dfr"]:
        s = read_raw(name)
        idx = pd.period_range(s.index.min().to_period("M"), m.index.max(), freq="M")
        m[name] = s.groupby(s.index.to_period("M")).last().reindex(idx).ffill()
    return m.sort_index()


# ---------------------------------------------------------------------------
# 3. Assemblage : cibles, retards, décalage de publication
# ---------------------------------------------------------------------------
def main() -> None:
    mk = build_markets()
    bud = build_budget()

    df = pd.DataFrame(index=mk.index)

    # Cibles (mois suivant)
    df["y_d_spread"] = mk["spread_bp"].shift(-1) - mk["spread_bp"]
    df["y_d_oat"] = (mk["oat_10y"].shift(-1) - mk["oat_10y"]) * 100
    df["y_cac_ret"] = (mk["cac40"].shift(-1) / mk["cac40"] - 1) * 100
    df["y_spread_up"] = (df["y_d_spread"] > 0).astype(float).where(df["y_d_spread"].notna())

    # Variables de marché connues en t (dont valeurs passées des cibles)
    df["spread_bp"] = mk["spread_bp"]
    df["oat_10y"] = mk["oat_10y"]
    df["bund_10y"] = mk["bund_10y"]
    df["d_spread"] = mk["spread_bp"].diff()
    df["d_spread_l1"] = df["d_spread"].shift(1)
    df["d_oat"] = mk["oat_10y"].diff() * 100
    df["d_oat_l1"] = df["d_oat"].shift(1)
    df["cac_ret"] = mk["cac40"].pct_change() * 100
    df["cac_ret_l1"] = df["cac_ret"].shift(1)
    df["vix"] = mk["vix"]
    df["d_vix"] = mk["vix"].diff()
    # Inflation décalée d'1 mois : l'IPCH définitif du mois t est publié vers le milieu de t+1
    # (même règle que les variables macro d'E16 et l'EPU d'E20) -> pas de biais d'anticipation
    df["inflation_yoy"] = mk["inflation_yoy"].shift(1)
    df["ecb_mro"] = mk["ecb_mro"]
    df["ecb_dfr"] = mk["ecb_dfr"]

    # Budget décalé de 2 mois
    bud_lag = bud.copy()
    bud_lag.index = bud_lag.index + BUDGET_LAG
    df = df.join(bud_lag.add_prefix("b_"), how="left")
    df["b_source_month"] = (df.index - BUDGET_LAG).astype(str)

    # Période d'étude : premières lignes où toutes les variables budgétaires existent
    b_cols = [c for c in df.columns if c.startswith("b_") and c != "b_source_month"]
    first = df[b_cols].dropna().index.min()
    df = df.loc[first:]

    df.index = df.index.astype(str)
    df.index.name = "mois"
    df.to_csv(OUT / "dataset_monthly.csv")

    n_train = df["y_d_spread"].notna().sum()
    print(f"Jeu de données : {df.shape[0]} mois ({df.index[0]} -> {df.index[-1]}), {df.shape[1]} colonnes")
    print(f"Mois avec cible spread disponible : {n_train}")
    print("Valeurs manquantes par colonne (hors dernière ligne) :")
    na = df.iloc[:-1].isna().sum()
    print(na[na > 0].to_string() if (na > 0).any() else "  aucune")


if __name__ == "__main__":
    main()
