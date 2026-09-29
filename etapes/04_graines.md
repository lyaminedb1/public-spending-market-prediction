# Étape 04 — Sensibilité à la graine aléatoire (constat 5)

**Objet** : produire un tableau propre des fourchettes de R² selon la graine, au lieu de chiffres dans un markdown.
La graine 42 reste celle du tableau principal.

**Dépend de** : 02.

## Actions
1. Créer `src/16_seeds_04.py` : importe `walk_forward`/`make_model` de 04 (importlib, car nom commençant par un chiffre) et relance RF (5 graines) et XGBoost (10 graines) pour M0 et M1, 3 cibles.
   Ne touche pas aux fichiers de 04.
2. Sortie : `results/tables/models_seeds.csv` — colonnes `modele, cible, jeu, graine, r2_oos, rmse` + un tableau agrégé `models_seeds_resume.csv` (min, max, médiane par modèle/cible/jeu) + p-value DM M1 vs M0 minimale.
3. Vérifier la graine 42 : les valeurs correspondent à `models_metrics.csv`.

## Validation
- [ ] Ligne graine 42 = `models_metrics.csv` (écart < 1e-9).
- [ ] Fourchettes proches de la revue (XGBoost : ±9 pts, R² négatifs partout, DM p min ≈ 0,14 ; RF p min ≈ 0,13).
- [ ] Le script est reproductible (deux exécutions → mêmes fichiers).
- [ ] Aucun fichier de résultats de 04 modifié (`git diff --stat results/tables/models_*.csv` vide hors `models_seeds*`).

## Commit
`16_seeds_04 : fourchettes de R² par graine (RF, XGBoost)`
