# Étape 09 — Décalage budgétaire : source unique et paramétrable

**Statut : ✅ fait.**

**Objet** : préparer la robustesse (décalage de 3 mois) sans copier le code. `BUDGET_LAG = 2` est défini **deux fois** (`src/02_build_dataset.py:27` et `src/05_extra_features.py:22`) : source unique. Aucun changement de résultat par défaut.

**Dépend de** : 05.

## Actions
1. Créer `src/config.py` avec `BUDGET_LAG = 2` et `TEST_START = "2020-01"` ; 02, 05, 04, 06 (et 15) l'importent (chemin `sys.path`).
2. `02_build_dataset.py` : accepter `--lag N` (défaut = config). Sortie `data/processed/dataset_monthly.csv` si N = 2, sinon `dataset_monthly_lagN.csv`. `b_source_month` doit refléter N.
3. `05_extra_features.py` : lire le même paramètre (pas utilisé par la robustesse mais cohérent).
4. `04_models.py` : accepter `--data` et `--suffix` ; les sorties avec suffixe vont dans `results/tables/robustesse/` (rien n'est écrasé).
5. `tests/verifications.py` : le contrôle « b_ = t−2 » lit le lag depuis la config.

## Validation
- [x] `python src/02_build_dataset.py` (sans argument) : `dataset_monthly.csv` **identique octet pour octet** (`git diff --stat` vide).
- [x] `python src/05_extra_features.py` : `extra_features.csv` identique.
- [x] `python src/04_models.py` sans argument : sorties identiques à celles de l'étape 05 (`diff`).
- [x] `--lag 3` : `b_source_month` = mois − 3 ; le nombre de lignes/cibles est noté (attendu : 1 ligne de moins en début de série).
- [x] `verifications.py` 31/31 ; un lag 3 volontairement mal appliqué (colonne non décalée) fait échouer le contrôle.

## Commit
`02/04/05 : décalage budgétaire et date de début de test dans config.py ; chemins de 04 paramétrables`

## Résultat (29/09)
- `src/config.py` (`BUDGET_LAG = 2`, `TEST_START = "2020-01"`) importé par 02, 05 (décalage) et 04, 06 (début du test). 15, 16, 17, 18 utilisent `M.TEST_START` de 04 : inchangés. Le panel (11) garde ses propres paramètres (test 2010T1/2012-01).
- `02_build_dataset.py --lag N` → `dataset_monthly_lagN.csv` (défaut : `dataset_monthly.csv`, **identique octet pour octet**, `extra_features.csv` idem). `04_models.py --data CSV --suffix NOM` → `results/tables/robustesse/` sans SHAP ni figures ; `--from-saved` : `diff` avant/après = aucune différence.
- `--lag 3` : 149 lignes (2014-04 → 2026-08), 148 cibles (−1 mois) ; budget(t) du lag 3 = budget(t−1) du lag 2 ; variables de marché identiques.
- `verifications.py` : 33 contrôles (2 nouveaux, appliqués à tout `dataset_monthly_lag*.csv`) ; contrôle négatif : un fichier lag 3 avec le budget du lag 2 fait échouer le test (écart 83).
- Le smoke-test complet de `04 --suffix` (~10 min) est fait à l'étape 10, qui l'utilise réellement.
