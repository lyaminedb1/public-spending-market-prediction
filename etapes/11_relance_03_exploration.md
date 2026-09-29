# Étape 11 — Relancer l'exploration (après correction de l'inflation)

**Dépend de** : 10. Les chiffres de CLAUDE.md (autocorrélations, Spearman, ADF) datent-ils d'avant la correction ? À vérifier.

## Actions
1. `python src/03_exploration.py` puis `python src/make_eda_notebook.py`.
2. Comparer avec `apres02` : listes des corrélations qui changent (`eda_correlations_budget.csv`), autocorrélations d'ordre 1, ADF.
3. Vérifier les chiffres cités dans CLAUDE.md : Δspread 0,14 ; ΔOAT 0,23 ; CAC -0,09 ; seuil ±0,16 ; ADF cibles p < 0,01 ; `_12m` p > 0,7 ; `_ytd_gap` p 0,01-0,06. Produire un tableau « ancien / nouveau ».

## Validation
- [ ] Scripts sans erreur ; figures `fig3_1_*` régénérées ; notebook exécutable (`jupyter nbconvert --execute` sans erreur).
- [ ] Tableau ancien/nouveau écrit dans `results/tables/diag_04/verif_chiffres_03.csv`.
- [ ] Si un chiffre a changé, il est listé pour la mise à jour de CLAUDE.md (étape 19), sans réinterprétation.

## Commit
`03 : relance après correction de l'inflation, vérification des chiffres cités`
