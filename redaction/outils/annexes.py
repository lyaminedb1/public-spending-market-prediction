"""
Génère redaction/annexes.md à partir des fichiers de résultats (aucun chiffre saisi à la main).
Usage : python redaction/outils/annexes.py
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
T = ROOT / "results" / "tables"
CIBLES = {"y_d_spread": "Δ spread", "y_d_oat": "Δ OAT", "y_cac_ret": "CAC 40",
          "btp_concessions (excès CAC 40)": "BTP-concessions (excès sur le CAC 40)",
          "defense (excès CAC 40)": "Défense (excès sur le CAC 40)",
          "spread niveau": "Spread (niveau)", "spread variation": "Spread (variation)"}
MODELES = {"ridge": "Ridge", "rf": "forêt", "xgb": "XGBoost", "enet": "Elastic Net", "logit": "logistique",
           "combinaison": "combinaison"}


def lib(c):
    c = str(c)
    for k, v in MODELES.items():
        c = __import__("re").sub(rf"\b{k}\b", v, c)
    return c.replace("vs", "contre").replace("2 CP", "2 composantes principales")


def f(x, d=1):
    """Arrondi commercial (0,605 -> 0,61), comme dans le texte."""
    from decimal import Decimal, ROUND_HALF_UP
    if pd.isna(x):
        return "sans objet"
    q = Decimal(str(x)).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP)
    return f"{q:.{d}f}".replace(".", ",")


def md_table(df):
    lines = ["| " + " | ".join(df.columns) + " |", "|" + "---|" * len(df.columns)]
    lines += ["| " + " | ".join(str(v) for v in row) + " |" for row in df.itertuples(index=False)]
    return "\n".join(lines)


out = ["# Annexes", ""]

# A. Variables
out += ["## Annexe A : Variables des modèles principaux", "",
        "**Tableau A.1 : Variables des jeux emboîtés M0, M1 et M2**", ""]
var = [
    ("M0", "d_spread, d_spread_l1", "Variation du spread OAT-Bund (mois t et t-1), en points de base"),
    ("M0", "spread_bp", "Niveau du spread OAT-Bund (mois t)"),
    ("M0", "d_oat, d_oat_l1", "Variation du taux OAT 10 ans (mois t et t-1)"),
    ("M0", "cac_ret, cac_ret_l1", "Rendement du CAC 40 (mois t et t-1)"),
    ("M0", "vix, d_vix", "Niveau et variation du VIX (aversion au risque)"),
    ("M0", "inflation_yoy", "Inflation IPCH France sur un an (décalée d'un mois)"),
    ("M0", "ecb_dfr", "Taux de la facilité de dépôt de la BCE"),
    ("M1", "b_dep_totales, personnel, fonctionnement, charge_dette, investissement, intervention (_ytd_gap)",
     "Écart du cumul depuis janvier par rapport à l'année précédente, en % du montant des douze derniers mois (décalé de 2 mois)"),
    ("M1", "b_psr_total_ytd_gap", "Prélèvements sur recettes, même transformation"),
    ("M2", "b_rec_totales, b_rec_fiscales (_ytd_gap)", "Recettes totales et fiscales, même transformation"),
    ("M2", "b_solde_ytd_diff_yoy", "Solde d'exécution cumulé, écart sur un an"),
]
out += [md_table(pd.DataFrame(var, columns=["Jeu", "Variable", "Définition"])), "",
        "*Source : élaboration de l'auteur. M1 = M0 + dépenses ; M2 = M1 + recettes et solde.*", ""]

# B. Extensions
s = pd.read_csv(T / "ext_summary.csv")
s["sans"] = s["R2oos_sans_%"].fillna(s.get("R2_vs_moyenne_sans_%"))
s["avec"] = s["R2oos_avec_%"].fillna(s.get("R2_vs_moyenne_avec_%"))
s["cible"] = s["cible"].map(lambda c: CIBLES.get(c, c))
s["num"] = s["extension"].str.extract(r"E(\d+)")[0].astype(int)
s = s.sort_values(["num", "extension"], kind="stable")
b = pd.DataFrame({
    "Extension": s["extension"], "Cible": s["cible"], "Comparaison": s["comparaison"].map(lib),
    "n": s["n_test"].map(lambda x: "sans objet" if pd.isna(x) else int(x)),
    "R² sans (%)": s["sans"].map(f), "R² avec (%)": s["avec"].map(f),
    "p brute": s["p_avec_meilleur"].map(lambda x: f(x, 3)), "p corrigée (BH)": s["p_BH"].map(lambda x: f(x, 3)),
})
out += ["## Annexe B : Détail des extensions E1 à E20", "",
        "Chaque ligne compare le même modèle sans et avec les dépenses (ou les finances publiques). « p brute » : test de "
        "Diebold-Mariano unilatéral « avec meilleur que sans » ; « p corrigée » : correction de Benjamini-Hochberg sur "
        "les 168 comparaisons retenues (E12 et ventilations exclues : « sans objet »). E16 : R² par rapport à la moyenne.", "",
        f"**Tableau B.1 : Résultats des {len(b)} comparaisons**", "", md_table(b), "",
        "*Source : calculs de l'auteur.*", ""]

# C. Graines
rows = []
for m, lab in (("rf", "Forêt aléatoire (5 graines)"), ("xgb", "XGBoost (10 graines)")):
    g = pd.read_csv(T / "diag_04" / f"graines_{m}.csv")
    for t, d in g.groupby("cible", sort=False):
        rows.append([lab, CIBLES[t], f"{f(d['R2_M0_%'].min())} à {f(d['R2_M0_%'].max())}",
                     f"{f(d['R2_M1_%'].min())} à {f(d['R2_M1_%'].max())}", f(d["p_DM"].min(), 2)])
out += ["## Annexe C : Sensibilité à la graine aléatoire", "",
        "**Tableau C.1 : R² hors échantillon (%) selon la graine**", "",
        md_table(pd.DataFrame(rows, columns=["Modèle", "Cible", "R² M0 (min à max)", "R² M1 (min à max)",
                                             "Plus petite p DM (M1 contre M0)"])), "",
        "*Source : calculs de l'auteur.*", ""]

# D. Bruit
rows = []
for m, lab in (("ridge", "Ridge"), ("rf", "Forêt aléatoire"), ("xgb", "XGBoost")):
    g = pd.read_csv(T / "diag_04" / f"bruit_{m}.csv")
    for t, d in g.groupby("cible", sort=False):
        reel = d.loc[d.jeu == "dépenses réelles", "gain_vs_M0_pts"].iloc[0]
        br = d.loc[d.jeu != "dépenses réelles", "gain_vs_M0_pts"]
        rows.append([lab, CIBLES[t], len(br), f(reel), f"{f(br.min())} à {f(br.max())}",
                     f"{(br >= reel).mean() * 100:.0f} %"])
out += ["## Annexe D : Contrôle négatif : dépenses contre variables de bruit", "",
        "**Tableau D.1 : Gain de R² par rapport à M0 (points) : vraies dépenses et sept variables de bruit**", "",
        md_table(pd.DataFrame(rows, columns=["Modèle", "Cible", "Tirages", "Dépenses réelles",
                                             "Bruit (min à max)", "Tirages de bruit ≥ dépenses"])), "",
        "*Source : calculs de l'auteur.*", ""]

# E. Décalage
r = pd.read_csv(T / "robustesse_lag.csv"); r = r[r.cible != "TOUTES"]
r = pd.DataFrame({"Décalage (mois)": r["lag_mois"], "Cible": r["cible"].map(CIBLES), "Modèle": r["modele"].map(lib),
                  "R² M0 (%)": r["R2_M0_%"].map(f), "R² M1 (%)": r["R2_M1_%"].map(f),
                  "p DM bilatérale (M1 contre M0)": r["p_DM_bilaterale_M1_vs_M0"].map(lambda x: f(x, 2)),
                  "p corrigée (BH, unilatérale)": r["p_BH_H1"].map(lambda x: f(x, 2))})
out += ["## Annexe E : Robustesse au décalage de publication", "",
        "**Tableau E.1 : Modèles principaux avec un décalage budgétaire de 1, 2 et 3 mois**", "", md_table(r), "",
        "*Source : calculs de l'auteur. La correction BH porte sur les p-values unilatérales « avec dépenses meilleur que sans » ; elle peut donc être inférieure à la p-value bilatérale affichée.*", ""]

# F. Étude d'événement préliminaire (CAC 40)
es = pd.read_csv(T / "event_study.csv")
lab = {0: "Corrélation de Spearman entre l'innovation budgétaire et le rendement du CAC 40 le jour de la publication",
       1: "Corrélation de Spearman entre l'innovation budgétaire et le rendement du CAC 40 le jour suivant",
       2: "Rendement absolu moyen du CAC 40 le jour de la publication (%), comparé à tous les jours de bourse"}
g = pd.DataFrame({"Test": [lab[i] for i in range(3)], "Événements": es["n"].astype(int),
                  "Statistique": [f(es.stat[0], 2), f(abs(es.stat[1]) if abs(es.stat[1]) < 0.005 else es.stat[1], 2), f(es.stat[2], 2)],
                  "p-value": [f(x, 2) for x in es["p_bilaterale"]]})
out += ["## Annexe F : Étude d'événement préliminaire sur le CAC 40", "",
        "Les dates de publication de la situation mensuelle budgétaire ont été relevées sur le site de presse du ministère de "
        "l'Économie : 40 publications, d'octobre 2017 à janvier 2026 (le moteur de recherche du site n'en renvoie pas davantage). "
        "Le délai entre la fin du mois concerné et la publication va de 29 à 47 jours (médiane de 33). "
        "L'innovation budgétaire est la variation, entre deux publications consécutives, de l'écart du solde cumulé par rapport "
        "à l'année précédente (en % du total annuel). Le plan du test a été fixé avant son exécution. Faute de taux quotidiens accessibles, le test ne porte pas sur le spread.", "",
        "**Tableau F.1 : Réaction du CAC 40 aux publications de la situation mensuelle budgétaire**", "", md_table(g), "",
        "*Source : calculs de l'auteur ; dates : presse.economie.gouv.fr ; "
        "cours : Yahoo Finance. Le dernier test est unilatéral (rendement absolu plus élevé les jours de publication).*", ""]

(ROOT / "redaction" / "annexes.md").write_text("\n".join(out))
print("annexes.md :", len(b), "comparaisons")
