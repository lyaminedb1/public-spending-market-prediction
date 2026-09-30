# Étape 07 — Importance par permutation hors échantillon (ajout post hoc, à déclarer)

**Statut : ✅ fait.**

**Objet** : H4 (classement des dépenses) ne peut pas s'appuyer sur SHAP en échantillon. Une importance par permutation **hors échantillon** répond directement, avec un contrôle bruit.

**Dépend de** : 02, 04.

## Actions
1. Créer `src/17_permutation_oos.py`. À chaque mois de test, le modèle M1 (XGBoost ; option Ridge) est entraîné sur le passé (mêmes réglages que 04) et **conservé**. Pour chaque variable, permuter sa colonne **sur l'ensemble des 79 mois de test** (30 permutations, graine fixe), ré-prédire avec les modèles conservés (pas de ré-entraînement) et mesurer la hausse de RMSE.
2. Inclure 7 variables de bruit dans le jeu (mêmes que `15_diag_04.noise`) : leur Δ RMSE donne la référence.
3. Sortie : `results/tables/models_permutation_oos.csv` (cible, modèle, variable, Δ RMSE moyen, écart-type, groupe dépenses/marchés/bruit).

## Validation
- [x] Bruit : Δ RMSE moyen ≈ 0 (dans ±1 écart-type).
- [x] Contrôle positif : une variable = cible future + bruit (ρ ≈ 0,5) ajoutée à M1 a un Δ RMSE nettement > 0 (la méthode détecte un vrai signal).
- [x] Reproductible (deux exécutions → même fichier).
- [x] Résultat consigné dans le message de commit : une dépense se distingue-t-elle du bruit ? (constat, pas objectif).

## Commit
`17_permutation_oos : importance par permutation hors échantillon avec contrôles bruit et positif`

## Résultat (29/09) — `src/17_permutation_oos.py` (1 min 40 s), `results/tables/models_permutation_oos.csv`
- Modèles M1 (XGBoost et Ridge) conservés mois par mois (79), 30 permutations sur les 79 mois de test, deux configurations : M1 + 7 variables de bruit, M1 + 1 signal fictif (ρ = 0,5).
- **Contrôle négatif** : les 7 variables de bruit prises ensemble ont un ΔRMSE dans ±1 écart-type de 0 pour les 6 combinaisons cible × modèle ; individuellement 1 variable de bruit sur 42 dépasse z = 2 (attendu par hasard : ~2).
- **Contrôle positif** : le signal fictif fait monter le RMSE de +7,6 % à +18,8 % (z de 3 à 5) → la méthode détecte un vrai signal.
- **Dépenses** : le groupe des 7 dépenses a un ΔRMSE **négatif** (le RMSE baisse quand on les mélange) pour toutes les combinaisons (−1,1 % à −2,5 % ; ridge CAC −0,1 %) ; 1 dépense sur 42 dépasse z = 2 (fonctionnement pour le spread avec XGBoost, ΔRMSE +0,064 pb), autant que le bruit. → **aucun contenu prédictif hors échantillon distinguable du bruit** ; H4 non soutenue par une deuxième méthode.
- Le groupe « marchés » est informatif pour Ridge (spread +25 %, OAT +18 %) mais pas pour le CAC 40.
- Reproductible (deux exécutions → fichier identique octet pour octet).
