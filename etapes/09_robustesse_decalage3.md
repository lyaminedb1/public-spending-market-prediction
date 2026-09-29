# Étape 09 — Robustesse : décalage de 3 mois (SMB 2014-2019 non vérifiée)

**Objet** : montrer que la conclusion ne dépend pas de l'hypothèse « publication à M+2 » pour les années non vérifiées.

**Dépend de** : 08.

## Actions
1. `python src/02_build_dataset.py --lag 3` puis `python src/04_models.py --data data/processed/dataset_monthly_lag3.csv --suffix lag3`.
2. Créer `src/19_robustesse_lag.py` qui compare `models_metrics.csv` (lag 2) à `robustesse/models_metrics_lag3.csv` : R², écart, DM M1 vs M0 dans les deux cas → `results/tables/robustesse_lag.csv`.
3. Test de contrôle : avec lag = 0 (fuite volontaire), les R² des modèles avec dépenses ne doivent PAS être identiques au cas lag 2 (sanity check ; documenter, ne pas commiter le fichier lag0).

## Validation
- [ ] Même période de test (79 mois ou 78 si la série perd un mois : le noter).
- [ ] Conclusion comparée : R² < 0 partout ? DM M1 vs M0 p > 0,3 ? (résultat à rapporter tel quel, quel qu'il soit).
- [ ] Le fichier de comparaison est généré par le script, pas à la main.

## Commit
`19_robustesse_lag : 04 avec décalage de 3 mois, tableau comparatif`
