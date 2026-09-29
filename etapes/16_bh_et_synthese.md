# Étape 16 — Correction Benjamini-Hochberg et synthèse

**Dépend de** : 13, 14, 15 (et 17 si exécutée).

## Actions
1. `python src/06_extensions.py resume` (BH sur tous les `E*.csv`, E12 et ventilations exclues).
2. `python src/07_extensions_summary.py` → `ext_synthese.csv` et `fig3_5_extensions.png`.
3. Vérifier que la synthèse contient E0…E20 (E14 absente, à documenter dans un commentaire ou un fichier `notes`).
4. Recalculer BH indépendamment (scipy `false_discovery_control`, ou statsmodels `multipletests(method='fdr_bh')`) sur les mêmes p-values.

## Validation
- [ ] BH indépendant = `p_BH` du script (écart < 1e-9).
- [ ] Le nombre de comparaisons testées est affiché et reporté (ancien : 168).
- [ ] Liste des « p brutes < 0,05 » et « p_BH < 0,10 » produite automatiquement (`results/tables/ext_significatifs.csv`).
- [ ] Figure régénérée (inspection visuelle).
- [ ] Aucun fichier dans `results/tables/extensions/` ne date d'avant la relance (contrôle de date de dernière modification dans le test étape 10, ou hash).

## Commit
`06/07 : correction BH et synthèse recalculées sur l'ensemble des extensions`
