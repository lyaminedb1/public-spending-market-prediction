"""
check_claude_md.py : compare les nombres clés cités dans CLAUDE.md aux CSV de results/.
  python tests/check_claude_md.py [CHEMIN_VERS_UN_AUTRE_CLAUDE.md]
Chaque contrôle cherche une phrase (motif) dans CLAUDE.md, en extrait le nombre, le compare à la valeur recalculée depuis
les tableaux ; il échoue aussi si le motif est introuvable (la phrase a changé sans mise à jour du contrôle).
Code de sortie 1 si un écart dépasse la tolérance.
"""
from pathlib import Path
import re
import subprocess
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "results" / "tables"
doc = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "CLAUDE.md"
text = doc.read_text(encoding="utf-8")
RESULTS = []


def num(x):
    return float(x.replace(",", ".").replace("−", "-"))


def check(label, pattern, expected, tol, group=1):
    m = re.search(pattern, text)
    if not m:
        RESULTS.append(False)
        print(f"  ÉCHEC  {label} : motif introuvable dans {doc.name}")
        return
    cited = num(m.group(group))
    ok = abs(cited - expected) <= tol
    RESULTS.append(ok)
    print(f"  {'OK    ' if ok else 'ÉCHEC '} {label}  (cité {cited:g} ; recalculé {expected:.4g})")


met, dm = pd.read_csv(T / "models_metrics.csv"), pd.read_csv(T / "models_dm_tests.csv")
mod = met[met.modele.isin(["ridge", "rf", "xgb"])]
ref = met[met.modele == "naif_moyenne"].set_index("cible").RMSE
mod = mod.assign(rel=(mod.RMSE / mod.cible.map(ref) - 1) * 100)
h1 = dm[dm.test.str.contains(r"M1 \+ dépenses vs M0")]
hyp, lim = pd.read_csv(T / "hypotheses.csv"), pd.read_csv(T / "limites_chiffres.csv")
summ, syn = pd.read_csv(T / "ext_summary.csv"), pd.read_csv(T / "ext_synthese.csv")
sig = pd.read_csv(T / "ext_significatifs.csv")
rob = pd.read_csv(T / "robustesse_lag.csv")
shap = pd.read_csv(T / "models_shap_importance.csv", index_col=0)
sp = [c for c in shap.index if c.startswith(("b_dep", "b_psr"))]
part = shap.loc[sp].sum() / shap.sum() * 100
noise = pd.read_csv(T / "diag_04" / "shap_bruit.csv").groupby("cible")["part_SHAP_bruit_%"].mean()
perm = pd.read_csv(T / "models_permutation_oos.csv")
gd = perm[(perm.config == "M1+bruit") & (perm.variable == "[groupe] dépenses")]
gz = gd[gd.modele == "xgb"].eval("dRMSE_moyen / dRMSE_ecart_type")
gz_all = gd.eval("dRMSE_moyen / dRMSE_ecart_type")
mask = ~summ.extension.str.startswith("E12") & ~summ.extension.str.contains("hors correction")
L = lambda key, cible="": float(lim[(lim.limite.str.startswith(key)) & (lim.cible.fillna("") == cible)].valeur.iloc[0])
S = lambda cle, cible, col: float(syn[(syn.cle == cle) & (syn.cible == cible)][col].iloc[0])
e16 = pd.read_csv(T / "extensions" / "E16.csv")

print("Modèles principaux")
check("meilleur R² (Ridge M0, CAC 40)", r"meilleur : Ridge M0 sur CAC 40, (-?[\d,]+) %", mod["R2_oos_%"].max(), 0.06)
for t, lab, pat in (("y_d_spread", "spread", r"meilleurs par cible : spread (-[\d,]+) %"),
                    ("y_d_oat", "OAT", r"meilleurs par cible : spread [-\d,]+ %, OAT (-[\d,]+) %"),
                    ("y_cac_ret", "CAC 40", r"meilleurs par cible : spread [-\d,]+ %, OAT [-\d,]+ %, CAC 40 (-[\d,]+) %")):
    check(f"meilleur R² {lab}", pat, mod[mod.cible == t]["R2_oos_%"].max(), 0.06)
check("DM M1 vs M0 : p bilatérale minimale", r"p bilatérale ([\d,]+) à [\d,]+\) ;", h1.p_bilaterale.min(), 0.006)
check("DM M1 vs M0 : p bilatérale maximale", r"p bilatérale [\d,]+ à ([\d,]+)\) ;", h1.p_bilaterale.max(), 0.006)
check("p_BH minimale sur les 18 tests de H1", r"p_BH minimale ([\d,]+)\*\*", float(hyp[(hyp.hypothese == "H1") & hyp.indicateur.str.startswith("p_BH")].valeur.iloc[0]), 0.006)
check("robustesse au décalage : p_BH minimale", r"p_BH ≥ ([\d,]+)\)", rob[rob.cible == "TOUTES"].p_BH_H1.min(), 0.006)
check("XGBoost vs Ridge, CAC 40 : p bilatérale", r"sur le CAC 40, p bilatérale ([\d,]+)",
      float(dm[(dm.cible == "y_cac_ret") & dm.test.str.startswith("XGBoost vs Ridge")].p_bilaterale.iloc[0]), 0.0006)
check("RMSE de XGBoost vs moyenne : minimum", r"RMSE \+([\d,]+) à \+[\d,]+ % vs moyenne", mod[mod.modele == "xgb"].rel.min(), 0.06)
check("RMSE de XGBoost vs moyenne : maximum", r"RMSE \+[\d,]+ à \+([\d,]+) % vs moyenne", mod[mod.modele == "xgb"].rel.max(), 0.06)
check("R² de la variation nulle (spread)", r"R² \+([\d,]+) % spread", float(met[(met.cible == "y_d_spread") & (met.modele == "naif_zero")]["R2_oos_%"].iloc[0]), 0.06)
check("part SHAP des dépenses : minimum", r"pèsent (\d+) à \d+ % de la part SHAP", part.min(), 0.6)
check("part SHAP des dépenses : maximum", r"pèsent \d+ à (\d+) % de la part SHAP", part.max(), 0.6)
check("part SHAP du bruit : minimum des moyennes", r"obtiennent (\d+) à \d+ % en moyenne", noise.min(), 0.6)
check("part SHAP du bruit : maximum des moyennes", r"obtiennent \d+ à (\d+) % en moyenne", noise.max(), 0.6)
check("permutation, groupe dépenses : ΔRMSE négatif pour les 6 combinaisons", r"pour les (6) combinaisons cible", float((gd.dRMSE_moyen < 0).sum()), 0)
check("permutation, groupe dépenses (XGBoost) : z minimal", r"XGBoost : z de (-[\d,]+) à -[\d,]+ ;", gz.min(), 0.011)
check("permutation, groupe dépenses (XGBoost) : z maximal", r"z de -[\d,]+ à (-[\d,]+) ;", gz.max(), 0.011)
check("permutation, groupe dépenses (Ridge) : z minimal", r"Ridge jusqu'à (-[\d,]+)\)", gz_all.min(), 0.011)

print("Extensions et panel")
check("comparaisons dans ext_summary.csv", r"\((\d+) comparaisons dont", len(summ), 0)
check("comparaisons dans la correction BH", r"comparaisons dont (\d+) dans la correction BH", int(mask.sum()), 0)
check("p brutes < 0,05", r"; (\d+) p brutes < 0,05", int((summ[mask].p_avec_meilleur < 0.05).sum()), 0)
check("significatives après BH", r"\*\*Résultat : (\d+) comparaison significative", int(summ[mask]["significatif_BH_10%"].sum()), 0)
check("E3 volatilité, CAC 40 (sans dépenses)", r"E3 : CAC 40 \+([\d,]+) %", S("E3", "y_cac_ret", "sans"), 0.06)
check("E3 volatilité, OAT (sans dépenses)", r"OAT \+([\d,]+) %\), classification", S("E3", "y_d_oat", "sans"), 0.06)
check("E1 h=3 spread (sans dépenses)", r"spread à 3 mois \(E1 : \+([\d,]+) %", S("E1 h=3", "y_d_spread", "sans"), 0.06)
check("E1 h=12 CAC 40 (sans dépenses)", r"CAC 40 à 12 mois \(E1 : \+([\d,]+) %", S("E1 h=12", "y_cac_ret", "sans"), 0.06)
check("E16 niveau : RMSE XGBoost", r"RMSE XGB ([\d,]+) pb vs", float(e16[(e16.cible == "spread niveau") & e16.comparaison.str.startswith("xgb")].RMSE_niveau_avec_pb.iloc[0]), 0.06)
check("E16 niveau : RMSE marche aléatoire", r"RMSE XGB [\d,]+ pb vs ([\d,]+) pb", float(e16.RMSE_marche_aleatoire_pb.iloc[0]), 0.06)
check("E15 : Ridge M0", r"Ridge M0 \+([\d,]+) %, M1", float(pd.read_csv(T / "extensions" / "E15.csv").iloc[0]["R2oos_sans_%"]), 0.06)

print("Limites")
check("écart-type déc./janv. de `_ytd_gap` (médiane)", r"en médiane ([\d,]+) fois", L("écart-type de l'écart YTD : décembre / janvier (médiane"), 0.06)
check("valeurs imputées d'E16 (moyenne des cellules)", r"\(([\d,]+) % en moyenne\) sur les 144", L("E16 : part des cellules manquantes"), 0.06)
check("séries d'E16 arrêtées", r"(\d+)/68 séries OCDE MEI arrêtées", L("E16 : séries dont la dernière valeur observée est antérieure à 2024-06"), 0)
check("AR(1) du Δspread", r"AR\(1\) ([\d,]+) Δspread", L("autocorrélation d'ordre 1 de la variation mensuelle", "y_d_spread"), 0.0006)
check("AR(1) de la ΔOAT", r"([\d,]+) ΔOAT ; en partie", L("autocorrélation d'ordre 1 de la variation mensuelle", "y_d_oat"), 0.0006)
check("mois de test", r"test 2020-01 → 2026-07 \((\d+) mois", L("mois de test (04)"), 0)

print("Contrôles automatiques")
r = subprocess.run([sys.executable, "tests/verifications.py"], capture_output=True, text=True, cwd=ROOT)
last = [l for l in r.stdout.splitlines() if "contrôles réussis" in l][-1]
n = int(last.split("/")[1].split()[0])
check("nombre de contrôles de verifications.py", r"(\d+) contrôles automatiques", n, 0)
check("tous les contrôles automatiques réussissent", r"(\d+) contrôles automatiques", int(last.split("/")[0].strip()), 0)

n_ok, n_tot = sum(RESULTS), len(RESULTS)
print(f"\n{n_ok}/{n_tot} nombres de {doc.name} conformes aux CSV")
sys.exit(0 if n_ok == n_tot else 1)
