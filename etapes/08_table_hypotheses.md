# Étape 08 — Tableau H1-H4 généré par script

**Objet** : une seule table, produite par code, qui donne pour chaque hypothèse la preuve chiffrée (pas de chiffres recopiés à la main dans le texte). Couvre aussi H2, aujourd'hui « non testable ».

**Dépend de** : 05, 06, 07.

## Actions
1. Créer `src/18_hypotheses.py` → `results/tables/hypotheses.csv`, à partir des CSV existants (aucun calcul de modèle) :
   - **H1** : par cible, meilleur gain M1 vs M0 (RMSE et R²), DM p bilatérale min, `p_BH_H1` min ; verdict mécanique « rejetée » si aucun p_BH < 0,10.
   - **H2** : gain de RMSE relatif (M1 vs M0) par cible et par modèle, rangé du spread au CAC ; verdict « non évaluable » si aucun gain n'est positif (règle écrite dans le script).
   - **H3** : DM RF vs Ridge et XGB vs Ridge (M1), RMSE relatif à la moyenne.
   - **H4** : part SHAP des dépenses vs bande de bruit (`shap_bruit.csv`) ; Δ RMSE par permutation des 7 dépenses vs bruit (`models_permutation_oos.csv`) ; verdict.
2. Chaque ligne cite le fichier source dans une colonne `source`.

## Validation
- [ ] Toutes les valeurs de `hypotheses.csv` retrouvées à la main dans les CSV sources (échantillon de 10, écart < 1e-6).
- [ ] Le script échoue explicitement si un fichier source manque (pas de valeur silencieuse).
- [ ] Verdicts conformes à la lecture actuelle (H1 rejetée, H3 rejetée, H4 non soutenue) — sinon expliquer l'écart dans le commit.

## Commit
`18_hypotheses : tableau H1-H4 généré depuis les résultats`
