# Étape 13 — Étendre les contrôles automatiques

**Objet** : que les relances ne puissent pas casser silencieusement.

**Dépend de** : 03, 05, 09, 12.

## Actions
Ajouter à `tests/verifications.py` (sections F et suivantes) ou en `tests/test_*.py` appelés par lui :
1. **Prévisions de 04** : 79 lignes, index continu 2020-01 → 2026-07, aucune valeur manquante ; R² recalculé depuis les prévisions = `models_metrics.csv` (écart < 1e-3).
2. **Alpha Ridge** : part de mois à la borne haute < 5 % (lit `diag_04/alpha_bornes_apres.csv`).
3. **Extensions** : `E*.csv` présents pour toutes les clés attendues (E1…E11, E12, E13, E15…E20, E7E8) ; aucune p-value hors [0,1].
4. **Cohérence de `ext_summary.csv`** : nombre de lignes = somme des fichiers extensions ; `p_BH` ≥ `p` brute ; nombre de comparaisons dans BH affiché.
5. **Cohérence des hyperparamètres** : `MARKETS`, `SPENDING`, hyperparamètres RF/XGB, `TEST_START` identiques entre 04, 06 et 11 (importation des trois modules) ; grille Ridge de 04 = 06.
6. **Ordre des dépendances** : `models_predictions_*.csv` (04) plus récents que `dataset_monthly.csv` ; `E7E8.csv` et `E12.csv` plus récents que `models_predictions_*.csv` (sinon E7/E8/E12 lisent des prévisions périmées).
7. **Contrôle de fuite exécutable** : dans `tests/test_walk_forward_06.py`, un jeu où une variable = cible future donne R² hors échantillon > 0,9 (le dispositif détecte une fuite).
8. Appeler les tests des étapes 03 et 09.

## Validation
- [ ] Tous les tests passent sur l'état actuel du dépôt.
- [ ] Chaque test a été vu **échouer** sur une entrée cassée volontairement (le noter dans le commit).
- [ ] Temps total < 3 min ; sinon marquer les tests longs `--lent`.

## Commit
`tests : contrôles sur prévisions, alpha, extensions, cohérence 04/06/11 et ordre des dépendances`
