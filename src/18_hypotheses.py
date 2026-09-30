"""
18_hypotheses.py
Tableau H1-H4 généré depuis les résultats déjà calculés (aucun modèle réestimé).
Chaque ligne cite son fichier source ; les verdicts suivent des règles écrites ci-dessous (pas de lecture à la main).

  H1 : ajouter les dépenses améliore la prévision  -> rejetée si aucun test M1/M2 vs M0 n'a p_BH < 0,10
  H2 : l'apport décroît du spread à l'OAT puis au CAC 40 -> non évaluable si H1 est rejetée (rien à classer) ;
       les gains ponctuels sont donnés à titre descriptif
  H3 : forêt/XGBoost font mieux que le linéaire -> rejetée si aucun test « ML vs Ridge (M1) » n'a p unilatérale < 0,05
  H4 : charge de la dette et intervention sont les dépenses les plus prédictives -> soutenue seulement si la
       permutation hors échantillon distingue le groupe des dépenses du bruit (z > 2) ; la part SHAP ne compte pas
       si elle est dans l'étendue du bruit

Entrées : results/tables/models_metrics.csv, models_dm_tests.csv, models_shap_importance.csv,
          models_permutation_oos.csv, diag_04/shap_bruit.csv  (échoue explicitement si l'un manque)
Sortie  : results/tables/hypotheses.csv
"""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd

TAB = Path("results/tables")
spec = importlib.util.spec_from_file_location("m04", Path(__file__).parent / "04_models.py")
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
TARGETS, SPENDING = list(M.TARGETS), M.SPENDING


def read(name):
    f = TAB / name
    if not f.exists():
        raise FileNotFoundError(f"{f} manquant : le tableau des hypothèses ne peut pas être produit")
    return pd.read_csv(f)


met, dm = read("models_metrics.csv"), read("models_dm_tests.csv")
shap_imp = pd.read_csv(TAB / "models_shap_importance.csv", index_col=0) if (TAB / "models_shap_importance.csv").exists() \
    else read("models_shap_importance.csv")
perm, noise = read("models_permutation_oos.csv"), read("diag_04/shap_bruit.csv")

rows = []


def add(h, cible, indicateur, valeur=np.nan, texte="", source=""):
    rows.append({"hypothese": h, "cible": cible, "indicateur": indicateur, "valeur": valeur, "texte": texte,
                 "source": source})


# ---------------------------------------------------------------------------- H1
S1 = "models_metrics.csv ; models_dm_tests.csv"
h1 = dm[dm.test.str.contains(r" vs M0$")]
for t in TARGETS:
    m = met[met.cible == t]
    gains, r2g = [], []
    for mod in ("ridge", "rf", "xgb"):
        a = m[(m.modele == mod) & (m.variables == "M0 marchés")].iloc[0]
        b = m[(m.modele == mod) & (m.variables == "M1 + dépenses")].iloc[0]
        gains.append((b.RMSE / a.RMSE - 1) * 100)
        r2g.append(b["R2_oos_%"] - a["R2_oos_%"])
    add("H1", t, "meilleur gain de RMSE de M1 vs M0 (%, négatif = M1 meilleur)", min(gains), source=S1)
    add("H1", t, "meilleur gain de R² de M1 vs M0 (points)", max(r2g), source=S1)
    x = h1[(h1.cible == t) & h1.test.str.contains("M1")]
    add("H1", t, "p bilatérale DM minimale M1 vs M0", x.p_bilaterale.min(), source=S1)
    add("H1", t, "p unilatérale DM minimale M1 vs M0 (M1 meilleur)", x.p_unilaterale.min(), source=S1)
pmin = h1.p_BH_H1.min()
add("H1", "toutes", "p_BH minimale (18 tests M1/M2 vs M0)", pmin, source="models_dm_tests.csv")
v1 = "rejetée" if pmin >= 0.10 else "non rejetée (au moins un test significatif après BH)"
add("H1", "toutes", "VERDICT", texte=v1, source="règle : rejetée si p_BH min >= 0,10")

# ---------------------------------------------------------------------------- H2
gain = {}
for t in TARGETS:
    m = met[met.cible == t]
    d = [m[(m.modele == mod) & (m.variables == "M1 + dépenses")]["R2_oos_%"].iloc[0]
         - m[(m.modele == mod) & (m.variables == "M0 marchés")]["R2_oos_%"].iloc[0] for mod in ("ridge", "rf", "xgb")]
    gain[t] = float(np.mean(d))
    add("H2", t, "gain moyen de R² de M1 vs M0 sur les 3 modèles (points, descriptif)", gain[t], source="models_metrics.csv")
ordre = " > ".join(sorted(gain, key=gain.get, reverse=True))
add("H2", "toutes", "classement descriptif des gains moyens", texte=ordre, source="models_metrics.csv")
add("H2", "toutes", "VERDICT", texte="non évaluable (H1 rejetée : aucun apport significatif à classer)" if v1 == "rejetée"
    else "à évaluer sur le classement des gains", source="règle : non évaluable si H1 rejetée")

# ---------------------------------------------------------------------------- H3
S3 = "models_dm_tests.csv ; models_metrics.csv"
h3 = dm[dm.test.str.contains(" vs Ridge")]
for t in TARGETS:
    for name, lab in (("Forêt aléatoire", "rf"), ("XGBoost", "xgb")):
        r = h3[(h3.cible == t) & h3.test.str.startswith(name)].iloc[0]
        m = met[(met.cible == t) & (met.modele == lab) & (met.variables == "M1 + dépenses")].iloc[0]
        add("H3", t, f"{name} vs Ridge (M1) : p unilatérale (ML meilleur)", r.p_unilaterale, source=S3)
        add("H3", t, f"{name} vs Ridge (M1) : p bilatérale", r.p_bilaterale, source=S3)
        add("H3", t, f"{name} M1 : RMSE relatif à la moyenne historique (%)",
            (m.RMSE / met[(met.cible == t) & (met.modele == "naif_moyenne")].RMSE.iloc[0] - 1) * 100, source=S3)
best = h3.p_unilaterale.min()
worse = h3[(h3.p_bilaterale < 0.05) & (h3.DM < 0)]
add("H3", "toutes", "nombre de tests où le ML est significativement PIRE que Ridge (p bilatérale < 0,05)", len(worse),
    texte="; ".join(f"{r.cible} {r.test}" for r in worse.itertuples()), source="models_dm_tests.csv")
add("H3", "toutes", "VERDICT", texte="rejetée" if best >= 0.05 else "non rejetée",
    source="règle : rejetée si aucun test ML vs Ridge n'a p unilatérale < 0,05")

# ---------------------------------------------------------------------------- H4
S4 = "models_shap_importance.csv ; diag_04/shap_bruit.csv ; models_permutation_oos.csv"
shap_ok = True
for t in TARGETS:
    part = shap_imp.loc[SPENDING, t].sum() / shap_imp[t].sum() * 100
    nz = noise[noise.cible == t]["part_SHAP_bruit_%"]
    inside = nz.min() <= part <= nz.max()
    shap_ok &= inside
    add("H4", t, "part SHAP des 7 dépenses (%)", part, source=S4)
    add("H4", t, "part SHAP de 7 variables de bruit : min / moyenne / max (%)", nz.mean(),
        texte=f"{nz.min():.1f} / {nz.mean():.1f} / {nz.max():.1f}", source=S4)
    add("H4", t, "part des dépenses dans l'étendue du bruit", float(inside), source=S4)
    g = perm[(perm.cible == t) & (perm.config == "M1+bruit") & (perm.modele == "xgb")]
    gd = g[g.variable == "[groupe] dépenses"].iloc[0]
    gb = g[g.variable == "[groupe] bruit"].iloc[0]
    add("H4", t, "permutation hors échantillon, groupe dépenses : ΔRMSE (z)", gd.dRMSE_moyen,
        texte=f"z = {gd.dRMSE_moyen / gd.dRMSE_ecart_type:.2f}", source=S4)
    add("H4", t, "permutation hors échantillon, groupe bruit : ΔRMSE (z)", gb.dRMSE_moyen,
        texte=f"z = {gb.dRMSE_moyen / gb.dRMSE_ecart_type:.2f}", source=S4)
z = perm[(perm.config == "M1+bruit") & (perm.variable == "[groupe] dépenses")].eval("dRMSE_moyen / dRMSE_ecart_type")
detect = bool((z > 2).any())
top2 = perm[(perm.config == "M1+bruit") & (perm.modele == "xgb") & (perm.groupe == "dépenses")]
rang = (top2.groupby("variable").dRMSE_moyen.mean().sort_values(ascending=False))
add("H4", "toutes", "classement des dépenses par ΔRMSE moyen (XGBoost, 3 cibles) — descriptif",
    texte=" > ".join(v.replace("b_", "").replace("_ytd_gap", "") for v in rang.index), source="models_permutation_oos.csv")
add("H4", "toutes", "VERDICT", texte="soutenue" if detect else "non soutenue",
    source="règle : soutenue seulement si la permutation hors échantillon distingue le groupe des dépenses du bruit "
           "(z > 2 pour une cible) ; SHAP ignoré s'il est dans l'étendue du bruit")

out = pd.DataFrame(rows)
out["valeur"] = out["valeur"].astype(float).round(4)
out.to_csv(TAB / "hypotheses.csv", index=False)
print(out[out.indicateur == "VERDICT"][["hypothese", "texte"]].to_string(index=False))
print(f"-> {TAB / 'hypotheses.csv'} ({len(out)} lignes)")
