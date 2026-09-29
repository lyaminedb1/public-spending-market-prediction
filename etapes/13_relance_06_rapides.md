# Étape 13 — Relancer E1-E9, E11-E13 (06_extensions)

**Dépend de** : 02, 03, 12. E10 est séparée (étape 14).

## Actions
1. Lancer par extension pour pouvoir valider chacune : `python src/06_extensions.py E1`, puis E2, E3, E4, E5, E6, E7E8, E9, E11, E12, E13 (clés du dict `EXTENSIONS`). Ne pas lancer sans argument (cela relancerait E10 et écrase `ext_summary.csv` en cours de route).
2. Après chaque extension : comparer `results/tables/extensions/<clé>.csv` à la version précédente (nombre de lignes identique, colonnes identiques).
3. Consigner l'ancien vs nouveau R² « sans » et « avec » dépenses dans `results/tables/diag_04/verif_extensions.csv` (un tableau, généré par script).

## Validation
- [ ] Chaque extension produit le même nombre de comparaisons qu'avant (E1 : h=3,6,12 × 3 cibles × modèles, etc.).
- [ ] Les variations de R² par rapport à l'ancienne version sont **explicables** par l'inflation décalée et la grille Ridge (quelques points au plus). Un écart > 5 points → investiguer avant de continuer.
- [ ] Contrôle anti-fuite E1 : la dernière ligne d'entraînement est ≥ h mois avant le mois de test (test de l'étape 03).
- [ ] Toujours 0 résultat « avec dépenses > moyenne » significatif ? (constat, pas objectif ; rapporter tel quel).

## Commit
`06 : relance E1-E9, E11-E13 (données corrigées, grille Ridge élargie)`
