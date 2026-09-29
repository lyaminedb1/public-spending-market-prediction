# Étape 14 — Relancer E10 (XGBoost réglé, le plus long)

**Dépend de** : 13.

## Actions
1. `python src/06_extensions.py E10` (réglage refait tous les 12 mois, sur l'entraînement uniquement).
2. Vérifier dans le code que la validation interne (TimeSeriesSplit) n'utilise jamais de mois ≥ mois de test (lire `tune`, `src/06_extensions.py:109`).
3. Vérifier la stabilité : relancer avec une autre graine (variable d'environnement ou paramètre) et noter l'écart de R².

## Validation
- [ ] Aucun mois de test dans les jeux de réglage (assert ajouté dans un test rapide sur un petit échantillon).
- [ ] Écart de R² entre deux graines documenté (attendu : quelques points).
- [ ] Nombre de comparaisons identique à l'ancienne version.

## Commit
`06 : relance E10 ; test de non-fuite du réglage`
