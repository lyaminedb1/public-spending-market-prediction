# Étape 15 — Relancer E20 et vérifier E17-E19

**Dépend de** : 13. Seule E20 lit `dataset_monthly.csv` ; E17-E19 sont déjà à jour, elles ne doivent pas bouger.

## Actions
1. `python src/14_more_extensions.py E20` (vérifier les clés de `RUN` ; ne pas lancer E17-E19 si elles sont à jour).
2. Lancer aussi `python src/14_more_extensions.py E19` sur une copie pour vérifier la reproductibilité (les fichiers ne doivent pas changer).
3. Vérifier que l'indice EPU européen est décalé d'1 mois (`tests/verifications.py`).

## Validation
- [ ] E20 : 18 comparaisons, index de test 2020-01 → 2026-07.
- [ ] E19 reproduit à l'identique (0 différence avec `diff`).
- [ ] Écart déclaré (indice européen au lieu de France) toujours indiqué dans le fichier de résultats ou son en-tête.

## Commit
`14 : relance E20 ; E19 reproductible`
