# Étape 01 — Instantané de référence

**Statut : ✅ fait (45 CSV, `.gitignore` : `tests/_snap/`).**

**Pourquoi** : pouvoir prouver, après chaque changement, ce qui a bougé et ce qui n'a pas bougé.

## Actions
1. Créer `tests/snapshot.py` avec deux commandes :
   - `python tests/snapshot.py save NOM` : copie `data/processed/*.csv` et `results/tables/**/*.csv` dans `/tmp/snap_NOM/` (ou `tests/_snap/NOM/`, ignoré par git) et écrit un `manifest.csv` (chemin, lignes, colonnes, hash).
   - `python tests/snapshot.py diff A B` : liste les fichiers ajoutés/supprimés/modifiés et, pour les CSV numériques modifiés, l'écart absolu maximum par colonne.
2. `python tests/snapshot.py save base` sur l'état actuel.
3. Vérifier l'outil : `diff base base` doit dire « aucune différence » ; modifier une valeur dans une copie et vérifier qu'elle est détectée.

## Validation
- [x] `diff base base` : 0 différence.
- [x] Différence artificielle détectée (fichier, colonne, écart).
- [x] Le manifeste liste tous les CSV de `results/tables` (comparer avec `find results/tables -name '*.csv' | wc -l`).

## Commit
`tests : outil d'instantané pour comparer les sorties avant/après`
