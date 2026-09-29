# Étape 17 — Relancer E10 (XGBoost réglé)

**Statut : ✅ fait.**

**Dépend de** : 16. E10 n'utilise pas Ridge : si le dataset (inflation) n'a pas changé depuis la dernière exécution, le résultat doit être **identique** à l'ancien ; sinon il change à cause de l'inflation.

## Actions
1. `python src/06_extensions.py E10` (réglage refait tous les 12 mois, sur l'entraînement uniquement, `TunedXGB.tune` ligne 109).
2. Test de non-fuite du réglage : sur un petit échantillon, vérifier que `TimeSeriesSplit` n'utilise que des lignes de l'entraînement (jamais le mois de test).
3. Stabilité : relancer avec une autre graine (paramètre `SEED` surchargé par variable d'environnement, sans changer la valeur par défaut) et noter l'écart de R².

## Validation
- [x] Aucun mois de test dans les jeux de réglage (assert dans le test).
- [x] Écart entre deux graines documenté (attendu : quelques points).
- [x] 3 comparaisons, comme avant.

## Commit
`06 : relance E10 ; test de non-fuite du réglage`

## Résultat (29/09)
- `src/06_extensions.py` : graine surchargeable par `SEED_06` (défaut 42, inchangé). `tests/test_tuned_xgb.py` (3 contrôles) : à chaque prévision, ni le réglage ni l'ajustement n'ont vu le mois prévu ou un mois postérieur (144 prévisions, 12 réglages = 6 par jeu de variables, tous les 12 mois) ; contrôle négatif (réglage sur toutes les données) détecté.
- E10 : 2 min 30 (et non 15). Résultat **identique** à la référence « ancienne grille, même environnement » (E10 n'utilise pas Ridge) ; écart avec le fichier commité (autre machine) 0,1 à 1,3 point de R² (avec dépenses).
- **Stabilité** (graine 7 contre 42) : écart de R² de 0,2 à 2,6 points sans dépenses et 0,8 à 2,9 points avec ; signes et conclusions inchangés (R² < 0 partout ; p « avec dépenses meilleur » : 0,84 / 0,55 / 0,17 avec la graine 42, 1,00 / 0,39 / 0,44 avec la graine 7).
- Nombre de comparaisons : 3, comme avant.
