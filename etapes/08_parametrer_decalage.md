# Étape 08 — Rendre le décalage budgétaire et les chemins paramétrables

**Objet** : préparer le test de robustesse (décalage de 3 mois) sans copier le code. Aucun changement de résultat par défaut.

**Dépend de** : 02, 05.

## Actions
1. `src/02_build_dataset.py` : lire `BUDGET_LAG` depuis un argument (`--lag 3`) ou une variable d'environnement, défaut = 2. Sortie : `data/processed/dataset_monthly.csv` si lag = 2, sinon `data/processed/dataset_monthly_lag3.csv`.
2. `src/04_models.py` : accepter `--data` et `--suffix` (défaut : chemins actuels) ; les sorties avec suffixe vont dans `results/tables/robustesse/` pour ne rien écraser.
3. Vérifier que `b_source_month` reflète le décalage.

## Validation
- [ ] `python src/02_build_dataset.py` (sans argument) : `dataset_monthly.csv` **identique octet pour octet** (`git diff --stat` vide).
- [ ] `--lag 3` : la colonne `b_source_month` = mois − 3 ; 1 mois de plus de budget manquant en début de série (vérifier le nombre de lignes/cibles).
- [ ] `python src/04_models.py` sans argument : sorties identiques à `apres02` (+ colonnes de l'étape 05).
- [ ] `tests/verifications.py` passe (adapter le contrôle des décalages pour accepter un lag ≠ 2 uniquement sur le fichier lag3).

## Commit
`02/04 : décalage budgétaire et chemins paramétrables (défaut inchangé)`
