# Étape 07 — Importance par permutation hors échantillon (option, à déclarer comme ajout post hoc)

**Objet** : H4 (classement des dépenses) ne peut pas s'appuyer sur SHAP en échantillon. Une importance par permutation **hors échantillon** répond directement.

**Dépend de** : 02.

## Actions
1. Créer `src/18_permutation_oos.py` : à chaque mois de test, modèle M1 entraîné sur le passé (mêmes réglages que 04) ; permuter chaque variable **sur l'ensemble des mois de test** (pas seulement le mois courant) pour mesurer la hausse de RMSE. Implémentation simple : stocker les prévisions du walk-forward, puis pour chaque variable, ré-prédire avec la colonne mélangée (30 permutations, graine fixe), en réutilisant les modèles entraînés à chaque mois (ne pas ré-entraîner).
2. Sortie : `results/tables/models_permutation_oos.csv` (variable, cible, modèle, Δ RMSE moyen, écart-type, part des dépenses).
3. Contrôle négatif intégré : inclure 7 variables de bruit ; leur Δ RMSE doit être ≈ 0 (ou négatif).

## Validation
- [ ] Bruit : Δ RMSE moyen proche de 0 (±1 écart-type).
- [ ] Contrôle positif : en ajoutant une variable = cible future + bruit (ρ ≈ 0,5), son importance est nettement > 0.
- [ ] Reproductible.
- [ ] Décision consignée : si aucune dépense n'a d'importance distincte du bruit → H4 « non soutenue » confirmée par une deuxième méthode.

## Commit
`18_permutation_oos : importance par permutation hors échantillon avec contrôles bruit et positif`
