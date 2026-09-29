# Étape 15 — Relancer 05 (surprise budgétaire, notations)

**Statut : ✅ fait — aucun changement de données.**

**Dépend de** : 14.

## Actions
1. `python tests/snapshot.py save avant15` ; `python src/05_extra_features.py` ; `diff`.
2. Attendu : identique (ces variables ne dépendent pas de l'inflation). Sinon, expliquer.
3. E4 : la dernière surprise disponible est 2026-02 (LFI 2026 absente) : vérifier par script.

## Validation
- [x] `git diff --stat data/processed/extra_features.csv` vide, ou écart expliqué ligne par ligne.
- [x] 9 dégradations dans `ratings_france.csv` ; `degradations_12m` ≥ 0 partout.
- [x] `tests/verifications.py` 31/31 (section C).

## Commit
`05 : relance ; extra_features vérifié` (ou aucun commit si aucun changement)

## Résultat (29/09)
`05_extra_features.py` relancé : `extra_features.csv` **identique octet pour octet** (`git diff` vide, `snapshot diff` : aucune différence). Dernière surprise budgétaire disponible : **2026-02** (LFI 2026 absente) ; 144 mois renseignés, 6 manquants (mars-août 2026) ; 9 dégradations de notation ; `degradations_12m` ≥ 0 (max 3) ; `verifications.py` 62/62. Aucun commit de données.
