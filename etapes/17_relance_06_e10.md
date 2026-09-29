# Étape 17 — Relancer E10 (XGBoost réglé, le plus long)

**Dépend de** : 16. E10 n'utilise pas Ridge : si le dataset (inflation) n'a pas changé depuis la dernière exécution, le résultat doit être **identique** à l'ancien ; sinon il change à cause de l'inflation.

## Actions
1. `python src/06_extensions.py E10` (réglage refait tous les 12 mois, sur l'entraînement uniquement, `TunedXGB.tune` ligne 109).
2. Test de non-fuite du réglage : sur un petit échantillon, vérifier que `TimeSeriesSplit` n'utilise que des lignes de l'entraînement (jamais le mois de test).
3. Stabilité : relancer avec une autre graine (paramètre `SEED` surchargé par variable d'environnement, sans changer la valeur par défaut) et noter l'écart de R².

## Validation
- [ ] Aucun mois de test dans les jeux de réglage (assert dans le test).
- [ ] Écart entre deux graines documenté (attendu : quelques points).
- [ ] 3 comparaisons, comme avant.

## Commit
`06 : relance E10 ; test de non-fuite du réglage`
