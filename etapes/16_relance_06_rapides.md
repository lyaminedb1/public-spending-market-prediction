# Étape 16 — Relancer E1-E9 et E11-E13 (`06_extensions.py`)

**Statut : ✅ fait** (E7E8 et E12 avaient été recalculés à l'étape 13, refaits ici).

**Dépend de** : 02, 03, 13, 15. **Ordre impératif** : E7/E8 et E12 lisent `results/tables/models_predictions_*.csv` (issus de 04) → 04 doit avoir été relancé avant (étape 02). Le test de l'étape 13 (dépendances) le vérifie.

## Actions
1. `python tests/snapshot.py save avant16`.
2. Lancer **une extension à la fois** pour valider chacune : `python src/06_extensions.py E1`, puis `E2 E3 E4 E5 E6 E7E8 E9 E11 E12 E13` (clés du dict `EXTENSIONS`, E10 est l'étape 17). Chaque appel régénère aussi `ext_summary.csv` par `summarize()` : sans risque, le fichier sera recalculé à l'étape 19.
3. Après chaque extension : même nombre de lignes et colonnes que l'ancienne version.
4. Tableau ancien / nouveau des R² sans et avec dépenses : `results/tables/diag_04/verif_extensions.csv`, **généré par script** depuis `avant16` et l'état courant.

## Validation
- [x] Nombre de comparaisons identique à l'ancienne version, extension par extension.
- [x] Écarts de R² explicables par l'inflation décalée et la grille Ridge (quelques points au plus, **lignes Ridge seulement** : les lignes RF/XGB sont identiques). Un écart > 5 points → investiguer avant de continuer.
- [x] Contrôle anti-fuite E1 : le test de l'étape 03 passe sur les vraies données.
- [x] Le constat (« 0 résultat significatif ? ») est rapporté tel quel, sans en faire un objectif.

## Commit
`06 : relance E1-E9, E11-E13 (données corrigées, grille Ridge élargie)`

## Résultat (29/09) — durée : E1 18 min, E2 8, E3 6, E4 10, E6 10, E9 4, E11 7, E13 10 (deux jobs en parallèle sur 4 cœurs)
- Comme à l'étape 02, un **état de référence « ancienne grille » a été recalculé dans le même environnement** (copie du dépôt) : sans lui on ne peut pas séparer l'effet de la grille de celui des versions de bibliothèques. `src/22_verif_extensions.py` compare trois états (commité / ancienne grille ici / nouveau) → `results/tables/diag_04/verif_extensions.csv` (159 comparaisons ; E10 relancée à l'étape 17).
- **Comparaisons sans Ridge : écart nouveau − ancienne grille = 0,0** (102 comparaisons identiques) → aucun effet de bord de la grille. Comparaisons avec Ridge (54, y compris les combinaisons d'E8) : écart médian **0,42 point** de R², maximum 10,5 points (E1 h = 6/12, R² déjà entre −100 % et −870 %).
- **Effet de l'environnement** (ancienne grille ici − commité) : médiane 0,8 point, mais 27 comparaisons sur 159 dépassent 5 points, surtout E1 à horizons longs et XGBoost (max 107 points sur des R² très négatifs) : les valeurs de RF/XGBoost dépendent des versions de bibliothèques ; **les valeurs exactes des extensions ne sont pas transférables d'une machine à l'autre**, seules les conclusions le sont.
- Conclusion inchangée : **168 comparaisons dans la correction BH, 0 significative** ; p brutes < 0,05 : 6 (avant : 5 ; 8 attendues par hasard) ; p_BH minimale 0,999 (avant 0,627, toujours > 0,10).
- Contrôle E1 : `test_walk_forward_06.py` (29/29) et `verifications.py` (62/62).
