# Étape 14 — Relancer l'exploration (après correction de l'inflation)

**Statut : ✅ fait.**

**Pourquoi** : `03_exploration.py` lit `dataset_monthly.csv`, modifié le 27/09 ; les chiffres cités dans CLAUDE.md (autocorrélations, Spearman, ADF) datent-ils d'avant ?

**Dépend de** : 13.

## Actions
1. `python tests/snapshot.py save avant14` ; `python src/03_exploration.py` ; `python src/make_eda_notebook.py`.
2. Comparer (`diff`) `eda_correlations_budget.csv` et `eda_statistiques.csv`.
3. Tableau « CLAUDE.md / recalculé » pour : autocorrélations d'ordre 1 (Δspread 0,14 ; ΔOAT 0,23 ; CAC −0,09) ; seuil ±0,16 ; corrélations de Spearman citées (investissement −0,16 ; personnel 0,23 ; charge de la dette 0,21 ; fonctionnement 0,17 ; ces liens à 0,07-0,13 avec l'inflation contrôlée) ; ADF des cibles (p < 0,01), des `_12m` (> 0,7), des `_ytd_gap` (0,01-0,06). Sortie `results/tables/diag_04/verif_chiffres_03.csv`.

## Validation
- [x] Scripts sans erreur ; figures `fig3_1_*` régénérées ; notebook exécutable : `jupyter nbconvert --to notebook --execute notebooks/03_EDA.ipynb` sans erreur.
- [x] Le tableau est **généré par script** (le contrôle « inflation contrôlée » est recalculé, pas recopié).
- [x] Tout chiffre qui change est listé pour l'étape 22.

## Commit
`03 : relance après correction de l'inflation ; vérification des chiffres cités`

## Résultat (29/09) — `src/21_verif_chiffres_03.py` → `results/tables/diag_04/verif_chiffres_03.csv` (38 chiffres, 29 conformes)
- `03_exploration.py` relancé : `eda_correlations_budget.csv` et `eda_statistiques.csv` **identiques** aux versions commitées (03 n'est pas affecté par la correction de l'inflation) ; 3 figures `fig3_1_*` régénérées (rendu matplotlib) ; notebook régénéré puis exécuté sans erreur (16 cellules avec sorties).
- **Confirmés** : autocorrélations (0,138 ; 0,233 ; −0,089), seuil 0,16, Spearman (−0,161 ; 0,232 ; 0,208 ; 0,173), CAC 40 (plus forte |ρ| = 0,125 < 0,16), ADF des cibles (p < 0,01), niveaux `_12m` non stationnaires.
- **Écarts à corriger dans CLAUDE.md (étape 22)** :
  1. corrélations partielles (inflation et ΔOAT passée contrôlées) : **0,15** (personnel), 0,09 (fonctionnement), 0,10 (charge de la dette) — et non « 0,07-0,13 » ; toujours sous le seuil 0,16 ;
  2. ADF des `_ytd_gap` : **0,000 à 0,057** (six sur sept < 0,05, donc stationnaires ; seules les dépenses totales à 0,057) — et non « 0,01-0,06 » ni « proches de la stationnarité » ;
  3. ADF des niveaux `_12m` : p > 0,7 pour 10 lignes sur 12 ; dépenses d'intervention 0,60 et prélèvements sur recettes 0,23 (toujours non stationnaires) ; spread 0,31 ; OAT 0,94 ;
  4. « corrélations fallacieuses jusqu'à 0,34 » : 0,34 est la |ρ| entre un niveau `_12m` et la **variation** ΔOAT(t+1) ; avec le **niveau** de l'OAT elle atteint **0,85**.
- Texte inexact corrigé dans `make_eda_notebook.py` (« niveaux non stationnaires, p > 0,7 » → « p entre 0,2 et 1,0 » ; « `_ytd_gap` p entre 0,01 et 0,06 » → « 0,000 à 0,057 »).
