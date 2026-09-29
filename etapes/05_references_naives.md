# Étape 05 — Deux références : moyenne historique et variation nulle (constat 6)

**Objet** : la variation nulle bat la moyenne pour les taux (spread +1,7 %, OAT +2,4 %). Le tableau doit montrer les deux, et les tests DM doivent aussi comparer aux deux.

**Dépend de** : 02.

## Actions
1. Lire `src/04_models.py:121-165` (`metrics`, `dm_tests`) : vérifier que `naif_zero` est bien présent dans `models_metrics.csv` et ce que fait `dm_tests` (référence = moyenne ?).
2. Ajouter dans `metrics` les colonnes `r2_vs_moyenne` et `r2_vs_zero` (R² hors échantillon relatif à chaque référence) — sans supprimer les colonnes existantes.
3. Ajouter dans `dm_tests` les comparaisons « chaque modèle M0/M1 vs variation nulle » (pour le CAC 40, la variation nulle = rendement 0 ; noter que ce n'est pas la référence pertinente).
4. Relancer 04 ; `diff apres02 nouveau` : les anciennes colonnes sont inchangées, seules des colonnes/lignes sont ajoutées.

## Validation
- [ ] R² de la variation nulle recalculé à la main sur `models_predictions_*.csv` (pandas seul) = valeur de la table (écart < 1e-3).
- [ ] Anciennes colonnes et anciennes lignes de `models_metrics.csv` / `models_dm_tests.csv` strictement identiques.
- [ ] Un test dans `tests/verifications.py` recalcule `r2_vs_moyenne` depuis les prévisions sauvegardées.

## Commit
`04 : R² et DM aussi contre la variation nulle (référence exigeante pour les taux)`
