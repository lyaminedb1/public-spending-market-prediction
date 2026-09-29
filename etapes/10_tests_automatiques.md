# Étape 10 — Étendre les contrôles automatiques

**Objet** : que les futures relances ne puissent pas casser silencieusement.

**Dépend de** : 03, 05.

## Actions
Ajouter à `tests/verifications.py` (ou `tests/test_*.py` lancés par `python -m pytest tests` — ajouter pytest aux requirements si utilisé) :
1. Alignement test : `models_predictions_*.csv` ont 79 lignes, index continu 2020-01 → 2026-07, aucune valeur manquante.
2. Pas de fuite : pour un mois test m, entraînement = mois < m (déjà couvert pour 04 par l'audit ; rendre exécutable : version rapide avec Ridge seulement).
3. Alpha Ridge : la part de mois à la borne haute < 5 % (lit `diag_04/alpha_bornes_apres.csv`).
4. Extensions : `results/tables/extensions/E*.csv` présents pour toutes les clés attendues (E1…E20) et aucune p-value hors [0,1].
5. Cohérence `ext_summary.csv` : nombre de lignes = somme des fichiers extensions ; `p_BH` ≥ `p` brute.
6. Le test de l'étape 03 (walk_forward 06) est appelé.
7. Contrôle négatif : injecter une variable = cible future dans un jeu de test → le test de fuite doit la détecter (R² hors échantillon > 0,9).

## Validation
- [ ] Tous les tests passent sur l'état actuel.
- [ ] Chaque test a été vu **échouer** sur une entrée cassée volontairement (le noter dans le commit).
- [ ] Temps d'exécution total < 3 min (sinon séparer « rapide » / « lent »).

## Commit
`tests : contrôles sur prévisions, alpha, extensions et non-fuite`
