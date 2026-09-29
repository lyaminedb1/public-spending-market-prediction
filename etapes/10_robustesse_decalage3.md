# Étape 10 — Robustesse : décalage de 3 mois (SMB 2014-2019 non vérifiée)

**Objet** : montrer si la conclusion dépend de l'hypothèse « publication à M+2 » pour les années non vérifiées (2014-2019).

**Dépend de** : 09.

## Actions
1. `python src/02_build_dataset.py --lag 3` puis `python src/04_models.py --data data/processed/dataset_monthly_lag3.csv --suffix lag3`.
2. Créer `src/19_robustesse_lag.py` : compare `models_metrics.csv` (lag 2) à `robustesse/models_metrics_lag3.csv` (R², RMSE, DM M1 vs M0, p_BH) → `results/tables/robustesse_lag.csv`.
3. **Contrôle de sensibilité** (non commité) : lag 0 (fuite volontaire) : les R² avec dépenses doivent différer de ceux du lag 2 — vérifie que le paramètre agit réellement.
4. Robustesse complémentaire, mêmes commandes : décalage de 1 mois (lag 1), pour encadrer l'hypothèse des deux côtés. Résultat dans le même fichier.

## Validation
- [ ] Même période de test (79 mois, ou 78 si le jeu perd un mois : à noter).
- [ ] Le fichier comparatif est produit par le script.
- [ ] Le lag 0 donne des résultats différents (le paramètre n'est pas ignoré).
- [ ] Conclusion rapportée telle quelle : R² < 0 partout ? DM M1 vs M0 p_BH > 0,10 ? Si non, le signaler avant de continuer.

## Commit
`19_robustesse_lag : 04 avec décalage de 1 et 3 mois, tableau comparatif`
