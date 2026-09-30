# Étape 05 — Deux références naïves et correction BH sur les tests de 04

**Statut : ✅ fait.**

**Objet** : (a) la variation nulle bat la moyenne pour les taux (spread +1,7 %, OAT +2,4 %) → le tableau de 04 doit donner les deux références ; (b) les tests de H1 dans 04 (9 comparaisons M1/M2 vs M0) n'ont pas de correction pour tests multiples, alors que les extensions en ont une (le message « survit à BH » manque pour le cœur du mémoire).

**Dépend de** : 02.

## Actions
1. Lire `src/04_models.py:121-165` (`metrics`, `dm_tests`). `naif_zero` existe déjà dans les lignes de `models_metrics.csv`.
2. `metrics` : ajouter `R2_vs_moyenne_%` (= colonne actuelle, inchangée) et `R2_vs_zero_%` (relatif à la variation nulle). Ne rien supprimer.
3. `dm_tests` : ajouter « chaque modèle M1 vs variation nulle » (pour le CAC 40, la variation nulle n'est pas la référence pertinente : l'indiquer dans une colonne `note`).
4. Ajouter dans `dm_tests` une colonne `p_BH_H1` : correction de Benjamini-Hochberg (10 %, même fonction que `06_extensions.benjamini_hochberg`, à **importer**, pas recopier) sur l'ensemble des tests « M1 vs M0 » et « M2 vs M0 » (3 modèles × 2 jeux × 3 cibles = 18 tests, p unilatérale « avec dépenses meilleur »). Les autres lignes : NaN.
5. Relancer 04 ; `diff apres02 nouveau` : les anciennes colonnes sont **identiques**, seules des colonnes sont ajoutées.
6. Figure 3.2 (`fig_relative_rmse`) : ajouter un repère pour la variation nulle (RMSE relatif de `naif_zero`), sans changer le reste.

## Validation
- [x] R² vs zéro recalculé à la main sur `models_predictions_*.csv` (pandas seul) : écart < 1e-3 ; spread ≈ +1,7 %, OAT ≈ +2,4 %, CAC ≈ -0,2 % (à confirmer après le changement de grille).
- [x] BH recalculé avec `statsmodels.stats.multitest.multipletests(method='fdr_bh')` : écart < 1e-9.
- [x] Anciennes colonnes de `models_metrics.csv` et `models_dm_tests.csv` strictement identiques (`diff`).
- [x] La figure s'ouvre et montre les deux références (inspection visuelle du PNG).

## Commit
`04 : R² aussi contre la variation nulle ; correction BH sur les tests de H1`

## Résultat (29/09)
- `04_models.py` : colonne `R2_vs_zero_%` (la colonne `R2_oos_%` reste celle relative à la moyenne, inchangée : pas de doublon `R2_vs_moyenne_%`), 3 lignes DM « M1 vs variation nulle » avec colonne `note`, colonne `p_BH_H1` (18 tests M1/M2 vs M0, fonction `benjamini_hochberg` importée de 06), repère « variation nulle » sur la figure 3.2 (légende déplacée sous les graphiques).
- Nouvelle option `python src/04_models.py --from-saved` : recalcule tableaux et figures depuis les prévisions sauvegardées (5 s, aucun modèle réestimé) ; c'est elle qui a servi à valider l'étape sans relancer les 10 minutes de calcul.
- Anciennes colonnes et lignes strictement identiques (33 lignes de métriques ; 33 anciennes lignes de DM sur 42).
- R² de la variation nulle vs moyenne : spread +1,73 %, OAT +2,42 %, CAC 40 −0,22 % ; recalcul manuel des R² vs zéro : écart max 5e-4 (arrondi).
- **BH sur H1 (18 tests)** : p_BH minimale = **0,81** → aucun apport des dépenses significatif.
- BH indépendant (statsmodels) : écart max 4e-4, dû à l'arrondi à 3 décimales des p-values enregistrées (le critère « < 1e-9 » du plan n'est pas atteignable sur des p arrondies).
- DM « M1 vs variation nulle » : XGBoost significativement moins bon que la variation nulle pour le spread (p = 0,033) et le CAC 40 (0,020) ; Ridge aussi pour le spread (0,044).
