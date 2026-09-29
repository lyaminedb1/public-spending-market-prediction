# Étape 16 — Relancer E1-E9 et E11-E13 (`06_extensions.py`)

**Dépend de** : 02, 03, 13, 15. **Ordre impératif** : E7/E8 et E12 lisent `results/tables/models_predictions_*.csv` (issus de 04) → 04 doit avoir été relancé avant (étape 02). Le test de l'étape 13 (dépendances) le vérifie.

## Actions
1. `python tests/snapshot.py save avant16`.
2. Lancer **une extension à la fois** pour valider chacune : `python src/06_extensions.py E1`, puis `E2 E3 E4 E5 E6 E7E8 E9 E11 E12 E13` (clés du dict `EXTENSIONS`, E10 est l'étape 17). Chaque appel régénère aussi `ext_summary.csv` par `summarize()` : sans risque, le fichier sera recalculé à l'étape 19.
3. Après chaque extension : même nombre de lignes et colonnes que l'ancienne version.
4. Tableau ancien / nouveau des R² sans et avec dépenses : `results/tables/diag_04/verif_extensions.csv`, **généré par script** depuis `avant16` et l'état courant.

## Validation
- [ ] Nombre de comparaisons identique à l'ancienne version, extension par extension.
- [ ] Écarts de R² explicables par l'inflation décalée et la grille Ridge (quelques points au plus, **lignes Ridge seulement** : les lignes RF/XGB sont identiques). Un écart > 5 points → investiguer avant de continuer.
- [ ] Contrôle anti-fuite E1 : le test de l'étape 03 passe sur les vraies données.
- [ ] Le constat (« 0 résultat significatif ? ») est rapporté tel quel, sans en faire un objectif.

## Commit
`06 : relance E1-E9, E11-E13 (données corrigées, grille Ridge élargie)`
