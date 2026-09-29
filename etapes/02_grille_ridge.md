# Étape 02 — Grille RidgeCV trop étroite (constat 8 de la revue de 04)

**Erreur de méthode** : `RidgeCV(alphas=np.logspace(-2, 3, 30))` est bloquée à la borne 1000 pour le CAC 40 dans 75-99 % des mois.
Effet mesuré hors dépôt : < 1 point de R², aucune conclusion ne change. On corrige quand même (le réglage ne fait pas son travail).

**Dépend de** : 00, 01.

## Actions
1. **Diagnostic avant** : dans `src/15_diag_04.py` (ou un petit script), mesurer la part de mois où l'alpha choisi est à la borne haute
   pour 04 (3 cibles × M0/M1/M2), 06 (M0/M1) et 11 (grille 10⁻² à 10⁴). Sauver dans `results/tables/diag_04/alpha_bornes_avant.csv`.
2. Remplacer `np.logspace(-2, 3, 30)` par `np.logspace(-2, 6, 40)` dans `src/04_models.py:71` et `src/06_extensions.py:53`
   (garder la même densité de points par décade, ≈ 5).
3. Relancer `python src/04_models.py` (~5 min).
4. **Diagnostic après** : même mesure → `alpha_bornes_apres.csv`. Attendu : < 5 % des mois à la borne 10⁶.
5. `python tests/snapshot.py save apres02` puis `diff base apres02`.

## Validation
- [ ] Part de mois à la borne haute avant : reproduit 75/79/99 % (CAC) ; après : < 5 % partout.
- [ ] Ridge : R² et DM bougent de moins de ~1 point de R² (revue : spread -15,0→-14,9 ; CAC M1 -2,7→-3,5). Sinon, comprendre avant de continuer.
- [ ] RF et XGBoost : sorties **identiques** (mêmes graines) — vérifier via `diff`.
- [ ] Conclusions inchangées : R² < 0 partout, DM M1 vs M0 p > 0,3.
- [ ] `tests/verifications.py` passe.

## Commit
`04/06 : grille RidgeCV élargie à 10^6 (alpha bloqué à la borne pour le CAC 40) ; relance de 04`
