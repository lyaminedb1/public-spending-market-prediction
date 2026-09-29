# Étape 15 — Relancer 05 (surprise budgétaire, notations)

**Dépend de** : 14.

## Actions
1. `python tests/snapshot.py save avant15` ; `python src/05_extra_features.py` ; `diff`.
2. Attendu : identique (ces variables ne dépendent pas de l'inflation). Sinon, expliquer.
3. E4 : la dernière surprise disponible est 2026-02 (LFI 2026 absente) : vérifier par script.

## Validation
- [ ] `git diff --stat data/processed/extra_features.csv` vide, ou écart expliqué ligne par ligne.
- [ ] 9 dégradations dans `ratings_france.csv` ; `degradations_12m` ≥ 0 partout.
- [ ] `tests/verifications.py` 31/31 (section C).

## Commit
`05 : relance ; extra_features vérifié` (ou aucun commit si aucun changement)
