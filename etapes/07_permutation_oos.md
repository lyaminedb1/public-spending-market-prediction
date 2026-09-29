# Étape 07 — Importance par permutation hors échantillon (ajout post hoc, à déclarer)

**Objet** : H4 (classement des dépenses) ne peut pas s'appuyer sur SHAP en échantillon. Une importance par permutation **hors échantillon** répond directement, avec un contrôle bruit.

**Dépend de** : 02, 04.

## Actions
1. Créer `src/17_permutation_oos.py`. À chaque mois de test, le modèle M1 (XGBoost ; option Ridge) est entraîné sur le passé (mêmes réglages que 04) et **conservé**. Pour chaque variable, permuter sa colonne **sur l'ensemble des 79 mois de test** (30 permutations, graine fixe), ré-prédire avec les modèles conservés (pas de ré-entraînement) et mesurer la hausse de RMSE.
2. Inclure 7 variables de bruit dans le jeu (mêmes que `15_diag_04.noise`) : leur Δ RMSE donne la référence.
3. Sortie : `results/tables/models_permutation_oos.csv` (cible, modèle, variable, Δ RMSE moyen, écart-type, groupe dépenses/marchés/bruit).

## Validation
- [ ] Bruit : Δ RMSE moyen ≈ 0 (dans ±1 écart-type).
- [ ] Contrôle positif : une variable = cible future + bruit (ρ ≈ 0,5) ajoutée à M1 a un Δ RMSE nettement > 0 (la méthode détecte un vrai signal).
- [ ] Reproductible (deux exécutions → même fichier).
- [ ] Résultat consigné dans le message de commit : une dépense se distingue-t-elle du bruit ? (constat, pas objectif).

## Commit
`17_permutation_oos : importance par permutation hors échantillon avec contrôles bruit et positif`
