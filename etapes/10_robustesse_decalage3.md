# Étape 10 — Robustesse : décalage de 3 mois (SMB 2014-2019 non vérifiée)

**Statut : ✅ fait.**

**Objet** : montrer si la conclusion dépend de l'hypothèse « publication à M+2 » pour les années non vérifiées (2014-2019).

**Dépend de** : 09.

## Actions
1. `python src/02_build_dataset.py --lag 3` puis `python src/04_models.py --data data/processed/dataset_monthly_lag3.csv --suffix lag3`.
2. Créer `src/19_robustesse_lag.py` : compare `models_metrics.csv` (lag 2) à `robustesse/models_metrics_lag3.csv` (R², RMSE, DM M1 vs M0, p_BH) → `results/tables/robustesse_lag.csv`.
3. **Contrôle de sensibilité** (non commité) : lag 0 (fuite volontaire) : les R² avec dépenses doivent différer de ceux du lag 2 — vérifie que le paramètre agit réellement.
4. Robustesse complémentaire, mêmes commandes : décalage de 1 mois (lag 1), pour encadrer l'hypothèse des deux côtés. Résultat dans le même fichier.

## Validation
- [x] Même période de test (79 mois, ou 78 si le jeu perd un mois : à noter).
- [x] Le fichier comparatif est produit par le script.
- [x] Le lag 0 donne des résultats différents (le paramètre n'est pas ignoré).
- [x] Conclusion rapportée telle quelle : R² < 0 partout ? DM M1 vs M0 p_BH > 0,10 ? Si non, le signaler avant de continuer.

## Commit
`19_robustesse_lag : 04 avec décalage de 1 et 3 mois, tableau comparatif`

## Résultat (29/09) — `src/19_robustesse_lag.py` → `results/tables/robustesse_lag.csv`
Runs complets de `04_models.py --data … --suffix lagN` pour N = 1, 3 (et 0 comme test de sensibilité, supprimé), 79 mois de test dans tous les cas.
| Décalage | Meilleur R² (tous modèles) | R² > 0 quelque part ? | p DM bilatérale minimale M1 vs M0 | p_BH minimale (18 tests) |
|---|---|---|---|---|
| 1 mois | −0,74 % | non | 0,057 | 0,806 |
| **2 mois (principal)** | −1,35 % | non | 0,366 | 0,809 |
| 3 mois | −2,56 % | non | 0,090 | 0,511 |
- **Conclusion identique** : aucun modèle ne bat la moyenne, aucun apport des dépenses après correction BH (p_BH ≥ 0,51), quel que soit le décalage.
- Le paramètre agit : avec un décalage de 0 (fuite volontaire), les R² de M1 diffèrent de ceux du lag 2 de jusqu'à 5,8 points (résultats non conservés).
- **Point d'attention pour la Discussion** : M0 (sans aucune variable budgétaire) bouge lui aussi de jusqu'à 5,7 points (lag 1) et 2,9 (lag 3) selon le jeu, parce que la date de début de l'échantillon change (2014-02 / 2014-03 / 2014-04) : quelques mois d'entraînement de plus ou de moins déplacent le R² de XGBoost de plusieurs points. Les écarts de R² de quelques points entre deux jeux ne sont donc pas interprétables.
- Fichiers commités : `dataset_monthly_lag1.csv`, `dataset_monthly_lag3.csv`, `results/tables/robustesse/*_lag{1,3}.csv`. `verifications.py` : 35/35.
