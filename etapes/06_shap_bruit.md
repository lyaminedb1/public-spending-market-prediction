# Étape 06 — Référence de bruit pour SHAP (constat 4)

**Objet** : la part SHAP des dépenses (31-37 %) n'est pas un signe d'information : 7 variables de bruit font 34-38 %. Le graphique doit porter cette référence.

**Dépend de** : 02.

## Actions
1. Récupérer la logique de `src/15_diag_04.py` (`shap_bruit`) et la mettre dans une fonction réutilisable de `src/04_models.py` (ou du nouveau `src/17_shap_bruit.py` pour ne pas alourdir 04).
2. Sortie : `results/tables/models_shap_bruit.csv` (10 tirages × 3 cibles : part SHAP des 7 variables de bruit) + résumé (min, médiane, max).
3. Modifier `fig_shap` pour tracer une ligne/bande « référence bruit » à côté de la part des dépenses ; régénérer `fig3_3_importance_shap.png`.
4. Bruit tiré avec une graine fixe, même XGBoost que 04.

## Validation
- [ ] Reproduit la revue : part de bruit 34-38 % ; part des dépenses 31-37 % (`models_shap_importance.csv` inchangé).
- [ ] La figure s'ouvre et affiche la référence (inspection visuelle du PNG).
- [ ] Deux exécutions donnent le même CSV.

## Commit
`04/17 : référence de bruit pour l'importance SHAP (figure 3.3)`
