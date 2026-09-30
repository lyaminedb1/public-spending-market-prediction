# Étape 04 — Relancer les diagnostics de `15_diag_04.py` qui dépendent de Ridge

**Statut : ✅ fait.**

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
- [x] `identite.csv` : écart max < 1e-9 avec les nouvelles prévisions de 04.
- [x] Puissance (ρ = 1) : 100 % de détection ; contrôle négatif : Ridge, dépenses meilleures que ≲ 10-30 % des tirages (à confirmer).
- [x] `resume.csv` généré **par script** (deux exécutions → mêmes valeurs).
- [x] Chaque écart avec la revue est listé ; ceux qui changent une conclusion (H4, CW) sont signalés dans le message de commit.
- [x] Sorties RF/XGB inchangées (`diff avant04 apres04` : seuls `identite`, `cw`, `positif`, `bruit_ridge`, `cw_bruit_ridge`, `resume`, `ecarts_revue` changent).

## Commit
`15_diag_04 : relance des diagnostics Ridge après élargissement de la grille ; job resume`

## Résultat (29/09)
- Relancés : `identite` (écart 4,4e-16), `ar1`, `cw`, `positif`, `bruit_ridge`, `cw_bruit_ridge` ; nouveaux jobs `resume` (147 lignes, reproductible) et `ecarts_revue` (53 comparaisons, 51 conformes). Les sorties RF/XGBoost (`graines_*`, `shap_bruit`, `bruit_rf`, `bruit_xgb`, `cw_bruit_xgb`) sont inchangées (`diff avant04 apres04`).
- **SHAP bruit** : « 34-38 % » de la revue = **moyenne** sur 10 tirages (spread 38,1 ; OAT 34,2 ; CAC 37,1). L'étendue réelle est 26-47 % : l'incohérence apparente (premier tirage à 41-47 %) était un simple effet de tirage. La conclusion H4 (le bruit obtient autant de SHAP que les dépenses) est inchangée.
- **Seul écart avec la revue** (constat 3) : taille du test de Clark-West sur du bruit avec Ridge : 55 % (spread), 25 % (OAT), 5 % (CAC) contre « 40-50 % pour les taux » dans la revue (20 tirages : incertitude ±11 pts ; la grille Ridge a aussi changé). Conclusion inchangée : Clark-West rejette à tort bien au-delà de 5 % (DM : 0 %, sauf 5 % XGB spread).
- Puissance (revue confirmée) : ρ = 0,3 → le modèle bat la moyenne dans 20-30 % des tirages ; ρ = 0,5 → 80-100 % ; DM détecte 30-80 % ; ρ = 1 → 100 %.
- Contrôle négatif : les vraies dépenses battent 5-10 % des tirages de bruit avec Ridge, 0-20 % avec RF, 40-50 % avec XGBoost.
- Les « p DM minimale » de la revue (0,14 / 0,13) sont des minimums **sur les 3 cibles** (atteints pour le spread) ; le contrôle de conformité les compare donc au spread.
