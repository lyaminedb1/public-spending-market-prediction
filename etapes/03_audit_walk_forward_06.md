# Étape 03 — `walk_forward` de 06 : lignes ou mois ? cibles à horizon h

**Statut : ✅ fait.** Code de `walk_forward` **inchangé** : avec des trous, il est seulement plus prudent (jamais de fuite) ; 0 mois manquant sur les vraies données ; 29/29 contrôles (`python tests/test_walk_forward_06.py`).

**Point non revu** (CLAUDE.md) : `src/06_extensions.py:135-152` coupe l'entraînement avec `d.iloc[: i-h+1]` où `d = df.dropna(subset=[target]+cols)`. Si `dropna` supprime des lignes au milieu, « h lignes » ≠ « h mois » (fuite ou trou). Même question pour `window=60` (lignes). De plus, `load()` construit les cibles cumulées h = 3, 6, 12 par `rolling` sur `y_*` : à vérifier contre les niveaux.

**Dépend de** : 00.

## Actions
1. Créer `tests/test_walk_forward_06.py` (lancé aussi par `verifications.py`, étape 13).
   - Jeu synthétique mensuel avec 2 mois manquants au milieu d'une colonne ; `factory` instrumentée pour enregistrer les index d'entraînement ; pour h ∈ {1, 3, 6, 12} vérifier `dernier_mois_entraînement + h ≤ mois_test` **en mois calendaires**.
   - `window=60` : la fenêtre couvre 60 mois calendaires (ou documenter que ce sont 60 observations).
2. Vérifier les cibles à horizon h sur le vrai jeu : `y_d_spread_h{h}(t) = spread_bp(t+h) − spread_bp(t)` ; `y_d_oat_h{h}(t) = (oat_10y(t+h) − oat_10y(t))×100` ; `y_cac_ret_h{h}(t)` = cours(t+h)/cours(t)−1 (à partir de `cac_ret`, en composé). Écart max < 1e-8 (les NaN de fin de série exclus). La colonne `cac40` n'est pas dans le jeu : reconstruire par cumul des `cac_ret`.
3. Sur le vrai jeu : compter, pour chaque extension de 06, les mois supprimés par `dropna` **à l'intérieur** de la période (hors début). Si > 0, corriger `walk_forward` en travaillant sur l'index mensuel (`train = d[d.index <= m − h]`).
4. Si le code change : `diff` des résultats de E1 avant/après ; sinon « code inchangé, test ajouté ».

## Validation
- [x] Le test synthétique **échoue** sur une version volontairement cassée (entraînement sur `i-h+2` lignes) et **passe** sur le code final.
- [x] Les cibles h = 3, 6, 12 correspondent aux niveaux (écart max noté dans le commit).
- [x] Nombre de mois supprimés à l'intérieur : reporté dans le message de commit (attendu 0).
- [x] `python tests/verifications.py` toujours 31/31.

## Commit
`06 : tests de non-fuite de walk_forward en mois calendaires et de cohérence des cibles à horizon h` (+ correction si nécessaire)
