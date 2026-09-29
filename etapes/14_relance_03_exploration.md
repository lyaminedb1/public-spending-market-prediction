# Étape 14 — Relancer l'exploration (après correction de l'inflation)

**Pourquoi** : `03_exploration.py` lit `dataset_monthly.csv`, modifié le 27/09 ; les chiffres cités dans CLAUDE.md (autocorrélations, Spearman, ADF) datent-ils d'avant ?

**Dépend de** : 13.

## Actions
1. `python tests/snapshot.py save avant14` ; `python src/03_exploration.py` ; `python src/make_eda_notebook.py`.
2. Comparer (`diff`) `eda_correlations_budget.csv` et `eda_statistiques.csv`.
3. Tableau « CLAUDE.md / recalculé » pour : autocorrélations d'ordre 1 (Δspread 0,14 ; ΔOAT 0,23 ; CAC −0,09) ; seuil ±0,16 ; corrélations de Spearman citées (investissement −0,16 ; personnel 0,23 ; charge de la dette 0,21 ; fonctionnement 0,17 ; ces liens à 0,07-0,13 avec l'inflation contrôlée) ; ADF des cibles (p < 0,01), des `_12m` (> 0,7), des `_ytd_gap` (0,01-0,06). Sortie `results/tables/diag_04/verif_chiffres_03.csv`.

## Validation
- [ ] Scripts sans erreur ; figures `fig3_1_*` régénérées ; notebook exécutable : `jupyter nbconvert --to notebook --execute notebooks/03_EDA.ipynb` sans erreur.
- [ ] Le tableau est **généré par script** (le contrôle « inflation contrôlée » est recalculé, pas recopié).
- [ ] Tout chiffre qui change est listé pour l'étape 22.

## Commit
`03 : relance après correction de l'inflation ; vérification des chiffres cités`
