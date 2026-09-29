# Étape 03 — `walk_forward` de 06 : lignes ou mois ?

**Point non revu** (CLAUDE.md) : `src/06_extensions.py:135` coupe l'entraînement avec `d.iloc[: i-h+1]` où `d = df.dropna(subset=[target]+cols)`.
Si `dropna` supprime des lignes au milieu, « h lignes » ≠ « h mois » et une fuite (ou un trou) est possible. Même question pour `window=60` (lignes, pas mois).

**Dépend de** : 00.

## Actions
1. Écrire `tests/test_walk_forward_06.py` : jeu synthétique mensuel avec des NaN au milieu (ex. 2 mois manquants dans une colonne) ;
   pour h ∈ {1, 3, 6, 12}, instrumenter `factory` pour enregistrer les index d'entraînement et vérifier :
   `dernier_mois_entrainement + h <= mois_test` **en mois calendaires**.
2. Vérifier aussi `window=60` : la fenêtre couvre bien 60 mois calendaires (ou documenter que ce sont 60 observations).
3. Sur le vrai jeu (`dataset_monthly.csv`) : compter les mois supprimés par `dropna` dans chaque extension (E1…E13). Si 0 dans la période de test, le test synthétique suffit à documenter le risque ; sinon corriger.
4. Si le test échoue : corriger `walk_forward` en travaillant sur l'index mensuel (`train = d[d.index <= m - h]`), puis relancer le test.

## Validation
- [ ] Test synthétique **échoue** sur une version volontairement cassée (contrôle négatif : entraîner sur `i-h+2` lignes) et **passe** sur le code final.
- [ ] Nombre de mois supprimés par `dropna` sur les vraies données : reporté dans le message de commit.
- [ ] Si le code a changé : `diff` des résultats E1 (horizons) avant/après documenté ; sinon « code inchangé, test ajouté ».

## Commit
`06 : test de non-fuite de walk_forward en mois calendaires (h = 1 à 12, fenêtre glissante)` (+ correction si nécessaire)
