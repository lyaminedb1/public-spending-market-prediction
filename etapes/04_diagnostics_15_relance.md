# Étape 04 — Relancer les diagnostics de `15_diag_04.py` qui dépendent de Ridge

**Pourquoi** : `15_diag_04.py` réutilise `make_model` de 04. Après l'étape 02, les diagnostics qui utilisent Ridge sont périmés. `graines_*`, `bruit_rf`, `bruit_xgb`, `cw_bruit_xgb`, `shap_bruit` n'utilisent que RF/XGBoost (inchangés) : **pas de relance**. Ceci remplace les anciens blocs « graines » et « SHAP bruit » (déjà faits par 15).

**Dépend de** : 02.

## Actions
1. `python tests/snapshot.py save avant04`.
2. Relancer (les durées sont celles annoncées dans l'en-tête de 15) : `python src/15_diag_04.py identite ar1 cw` puis `positif` (~10 min), `bruit_ridge` et `cw_bruit_ridge` (~20 min).
3. Ajouter à `15_diag_04.py` un job `resume` qui **agrège** tous les CSV de `results/tables/diag_04/` en un tableau `resume.csv` :
   - puissance : par cible et ρ, part des tirages où le modèle bat la moyenne et où DM p < 0,05 ;
   - contrôle négatif : rang des vraies dépenses parmi les tirages de bruit (Ridge/RF/XGB) ;
   - Clark-West : p vs DM, et taille du test sur le bruit ;
   - SHAP bruit : min / moyenne / max de la part par cible ;
   - graines : min / max de R² M0 et M1 par modèle et cible, p DM minimale ;
   - AR(1) et variation nulle.
4. Comparer `resume.csv` aux chiffres de `docs/revue_04_models.md` (constats 1 à 6) ; écrire les écarts dans `results/tables/diag_04/ecarts_revue.csv`. **Point à vérifier en particulier** : « SHAP bruit 34-38 % » (revue) contre le fichier `shap_bruit.csv` (premier tirage 41-47 % pour les 3 cibles).

## Validation
- [ ] `identite.csv` : écart max < 1e-9 avec les nouvelles prévisions de 04.
- [ ] Puissance (ρ = 1) : 100 % de détection ; contrôle négatif : Ridge, dépenses meilleures que ≲ 10-30 % des tirages (à confirmer).
- [ ] `resume.csv` généré **par script** (deux exécutions → mêmes valeurs).
- [ ] Chaque écart avec la revue est listé ; ceux qui changent une conclusion (H4, CW) sont signalés dans le message de commit.
- [ ] Sorties RF/XGB inchangées (`diff avant04 apres04` : seuls `identite`, `cw`, `positif`, `bruit_ridge`, `cw_bruit_ridge`, `resume`, `ecarts_revue` changent).

## Commit
`15_diag_04 : relance des diagnostics Ridge après élargissement de la grille ; job resume`
