# Étape 06 — Référence de bruit sur la figure d'importance SHAP (constat 4)

**Statut : ✅ fait.**

**Objet** : la part SHAP des dépenses (31-37 %) n'est pas un signe d'information : 7 variables de bruit font autant. `15_diag_04.py shap_bruit` écrit déjà `diag_04/shap_bruit.csv` ; il reste à porter la référence sur la figure 3.3 et à la rendre traçable.

**Dépend de** : 04 (résumé validé), 05.

## Actions
1. `fig_shap` (`src/04_models.py:220`) : lire `results/tables/diag_04/shap_bruit.csv` s'il existe et tracer, pour chaque cible, la bande min-max de la part de bruit à côté de la part des dépenses ; sinon avertir sans échouer.
2. Ne pas relancer le calcul du bruit dans 04 (lent, déjà fait par 15). La graine du tirage est celle de 15 (`default_rng(1)`).
3. Régénérer `fig3_3_importance_shap.png` en relançant seulement la partie figures (fonction dédiée `python src/04_models.py --figures` qui relit les CSV, sans réestimer les modèles).

## Validation
- [x] La figure s'ouvre et affiche la référence (inspection visuelle).
- [x] `models_shap_importance.csv` **identique** (`diff`).
- [x] `--figures` s'exécute en < 30 s sans réestimer les modèles.
- [x] Les nombres de la bande = min/max de `shap_bruit.csv` (assert dans le script).

## Commit
`04 : référence de bruit sur la figure d'importance SHAP ; option --figures`

## Résultat (29/09)
- `fig_shap` lit `diag_04/shap_bruit.csv` (fonction `shap_noise_reference`) et affiche dans chaque panneau la part des dépenses (33 / 37 / 31 %) et la part de 7 variables de bruit : étendue 34-43 % (spread), 26-42 % (OAT), 29-47 % (CAC 40), moyennes 38 / 34 / 37 %. Sans le fichier : avertissement, figure sans référence.
- Pas d'option `--figures` séparée : `python src/04_models.py --from-saved` (étape 05) régénère déjà les figures en 5 s sans réestimer.
- `models_shap_importance.csv` et tous les CSV : `diff` = aucune différence ; bornes de l'encadré = min/max du CSV (vérifié par script).
