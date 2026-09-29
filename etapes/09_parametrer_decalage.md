# Étape 09 — Décalage budgétaire : source unique et paramétrable

**Objet** : préparer la robustesse (décalage de 3 mois) sans copier le code. `BUDGET_LAG = 2` est défini **deux fois** (`src/02_build_dataset.py:27` et `src/05_extra_features.py:22`) : source unique. Aucun changement de résultat par défaut.

**Dépend de** : 05.

## Actions
1. Créer `src/config.py` avec `BUDGET_LAG = 2` et `TEST_START = "2020-01"` ; 02, 05, 04, 06 (et 15) l'importent (chemin `sys.path`).
2. `02_build_dataset.py` : accepter `--lag N` (défaut = config). Sortie `data/processed/dataset_monthly.csv` si N = 2, sinon `dataset_monthly_lagN.csv`. `b_source_month` doit refléter N.
3. `05_extra_features.py` : lire le même paramètre (pas utilisé par la robustesse mais cohérent).
4. `04_models.py` : accepter `--data` et `--suffix` ; les sorties avec suffixe vont dans `results/tables/robustesse/` (rien n'est écrasé).
5. `tests/verifications.py` : le contrôle « b_ = t−2 » lit le lag depuis la config.

## Validation
- [ ] `python src/02_build_dataset.py` (sans argument) : `dataset_monthly.csv` **identique octet pour octet** (`git diff --stat` vide).
- [ ] `python src/05_extra_features.py` : `extra_features.csv` identique.
- [ ] `python src/04_models.py` sans argument : sorties identiques à celles de l'étape 05 (`diff`).
- [ ] `--lag 3` : `b_source_month` = mois − 3 ; le nombre de lignes/cibles est noté (attendu : 1 ligne de moins en début de série).
- [ ] `verifications.py` 31/31 ; un lag 3 volontairement mal appliqué (colonne non décalée) fait échouer le contrôle.

## Commit
`02/04/05 : décalage budgétaire et date de début de test dans config.py ; chemins de 04 paramétrables`
