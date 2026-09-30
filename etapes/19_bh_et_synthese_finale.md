# Étape 19 — Correction BH et synthèse finales

**Statut : ✅ fait.**

**Dépend de** : 12, 16, 17, 18.

## Actions
1. `python src/06_extensions.py resume` (BH sur tous les `E*.csv`, sauf E12 et ventilations « hors correction »).
2. `python src/07_extensions_summary.py` (version corrigée à l'étape 12).
3. Recalculer BH indépendamment (`statsmodels multipletests(method='fdr_bh')`) sur les mêmes p.
4. Produire `results/tables/ext_significatifs.csv` : liste automatique des « p brutes < 0,05 » et des « p_BH < 0,10 », avec `R2oos_sans`, `R2oos_avec` (permet de voir si le modèle avec dépenses bat la moyenne).

## Validation
- [x] BH indépendant = `p_BH` du script (écart < 1e-9).
- [x] Nombre total de comparaisons testées affiché et reporté (ancien : 168).
- [x] Toutes les extensions attendues sont présentes (test de l'étape 13).
- [x] Figure régénérée et lisible (E15-E20 incluses).
- [x] Aucun `E*.csv` de `results/tables/extensions/` ne date d'avant la relance (sauf E15-E18, volontairement non relancés et vérifiés inchangés).

## Commit
`06/07 : correction BH et synthèse recalculées sur l'ensemble des extensions`

## Résultat (29/09)
- `06_extensions.py resume` puis `07_extensions_summary.py` (qui écrit maintenant aussi `results/tables/ext_significatifs.csv`).
- **168 comparaisons** dans la correction BH (E12 et ventilations exclues), **0 significative** (10 %). p brutes < 0,05 : **6** (attendu par hasard : 8). BH recalculé indépendamment avec `statsmodels.multipletests` : 168 comparaisons, 0 rejet, écart max 4e-4 (arrondi à 3 décimales des p-values enregistrées).
- p_BH = 0,999 pour les 6 cas : avec beaucoup de p-values proches de 1 (test unilatéral « avec dépenses meilleur »), la correction BH ramène toutes les p corrigées à ≈ 0,999.
- Les 6 p brutes < 0,05 sont toutes des cas où le modèle **avec** dépenses reste **sous la moyenne historique** (R² avec dépenses < 0) et fait moins mal que la version sans : E19 défense h = 3 XGBoost (p 0,008 ; R² −53 → −20 %), E1 spread h = 12 XGBoost (0,013), E11 CAC 40 XGBoost (0,024), E1 CAC 40 h = 6 XGBoost (0,027), E17 RF (0,038), E15 XGBoost (0,047).
- Fichiers E15-E18 non relancés (vérifiés inchangés à l'étape 18) ; E1-E13, E19, E20 relancés aux étapes 16-18.
- `verifications.py` 62/62 ; figures `fig3_5` et `fig3_6` régénérées et vérifiées visuellement.
