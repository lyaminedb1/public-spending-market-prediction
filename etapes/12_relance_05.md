# Étape 12 — Relancer 05 (surprise budgétaire, notations)

**Dépend de** : 11.

## Actions
1. `python src/05_extra_features.py` → `data/processed/extra_features.csv`.
2. Comparer à la version commitée : index, colonnes, NaN. Les variables de 05 ne dépendent en principe pas de l'inflation → attendu : identique. Sinon, expliquer.
3. Vérifier E4 : LFI 2026 absente → dernière valeur de surprise = 2026-02 (documenté).

## Validation
- [ ] `git diff --stat data/processed/extra_features.csv` vide, ou écart expliqué ligne par ligne.
- [ ] 9 dégradations dans `ratings_france.csv` ; variable notation cohérente (aucun décalage négatif).
- [ ] `tests/verifications.py` passe.

## Commit
`05 : relance ; extra_features vérifié` (ou « aucun changement, non commité »)
