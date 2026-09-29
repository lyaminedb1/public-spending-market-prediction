# Étape 12 — Corriger `07_extensions_summary.py` : E15-E20 absentes

**Erreur constatée** : `LABELS` (`src/07_extensions_summary.py:22-29`) ne contient que E0-E13 → la figure 3.5 et la synthèse ne montrent ni E15, E16, E17, E18, E19 ni E20 (dans `ext_synthese.csv`, E19/E16/E20a/E20b ont `ordre` vide). E16 utilise d'autres noms de colonnes (`R2_vs_moyenne_sans_%`, `R2_vs_moyenne_avec_%`) donc `sans`/`avec` y sont vides. E15/E17/E18 ne sont pas listées.

**Dépend de** : rien (peut être validée sur les CSV actuels). Refait à l'étape 19 avec les résultats relancés.

## Actions
1. Ajouter à `LABELS` : `E15`, `E16` (niveau et variation séparés), `E17`, `E18`, `E19` (BTP et défense séparés), `E20a`, `E20b`.
2. Unifier les colonnes : pour E16, `sans/avec` = `R2_vs_moyenne_sans_%` / `R2_vs_moyenne_avec_%` ; ajouter à la synthèse une colonne `gain_vs_marche_aleatoire_avec_%` pour les extensions qui l'ont, afin de montrer que « tout perd contre la marche aléatoire ».
3. La clé `key()` doit distinguer E16 niveau/variation (colonne `cible`) et E19 par panier.
4. Adapter la légende de la figure (test jusqu'à 2026-07 ; E4 jusqu'à 2026-02 ; E15-E18 : panel, périodes de test 2010/2012).
5. Régénérer `ext_synthese.csv` et `fig3_5_extensions.png`.

## Validation
- [ ] `ext_synthese.csv` contient les 20 extensions (E0-E13 sauf E12, E15-E20) ; aucune ligne sans `sans` et `avec` hors E14.
- [ ] Les valeurs de chaque ligne retrouvées à la main dans `ext_summary.csv` (échantillon de 10).
- [ ] Figure : toutes les extensions apparaissent, lisibles (inspection visuelle).
- [ ] Ne pas modifier `ext_summary.csv` (BH) : `diff` ne montre que `ext_synthese.csv` et la figure.

## Commit
`07 : synthèse et figure des extensions complétées (E15-E20)`
