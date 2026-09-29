# Étape 19 — Correction BH et synthèse finales

**Dépend de** : 12, 16, 17, 18.

## Actions
1. `python src/06_extensions.py resume` (BH sur tous les `E*.csv`, sauf E12 et ventilations « hors correction »).
2. `python src/07_extensions_summary.py` (version corrigée à l'étape 12).
3. Recalculer BH indépendamment (`statsmodels multipletests(method='fdr_bh')`) sur les mêmes p.
4. Produire `results/tables/ext_significatifs.csv` : liste automatique des « p brutes < 0,05 » et des « p_BH < 0,10 », avec `R2oos_sans`, `R2oos_avec` (permet de voir si le modèle avec dépenses bat la moyenne).

## Validation
- [ ] BH indépendant = `p_BH` du script (écart < 1e-9).
- [ ] Nombre total de comparaisons testées affiché et reporté (ancien : 168).
- [ ] Toutes les extensions attendues sont présentes (test de l'étape 13).
- [ ] Figure régénérée et lisible (E15-E20 incluses).
- [ ] Aucun `E*.csv` de `results/tables/extensions/` ne date d'avant la relance (sauf E15-E18, volontairement non relancés et vérifiés inchangés).

## Commit
`06/07 : correction BH et synthèse recalculées sur l'ensemble des extensions`
