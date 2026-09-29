# Étape 02 — Grille RidgeCV trop étroite (constat 8 de la revue de 04)

**Erreur de méthode** : `RidgeCV(alphas=np.logspace(-2, 3, 30))` (`src/04_models.py:71`, `src/06_extensions.py:53`) est bloquée à la borne 1000 pour le CAC 40 dans 75-99 % des mois. Effet mesuré hors dépôt : < 1 point de R². On corrige quand même (le réglage ne fait pas son travail).

**Dépend de** : 00, 01.

## Actions
1. `python tests/snapshot.py save avant02`.
2. Créer `src/16_diag_alpha.py` : pour 04 (3 cibles × M0/M1/M2), 06 (M0/M1, cible h=1) et 11 (grille 10⁻²…10⁴, E16 variation), refaire la validation glissante en Ridge seul et enregistrer `model[-1].alpha_` de chaque mois. Sortie : `results/tables/diag_04/alpha_bornes.csv` (`script, cible, jeu, mois, alpha, borne_haute` booléen ; `borne_haute` = alpha ≥ 0,99 × maximum de la grille) + résumé par groupe. Le script importe `make_model` du script visé (importlib, comme `15_diag_04.py`) → il mesure la grille **actuelle** de chaque script.
3. Lancer `16_diag_alpha.py` **avant** le changement → renommer la sortie `alpha_bornes_avant.csv`.
4. Remplacer `np.logspace(-2, 3, 30)` par `np.logspace(-2, 6, 40)` dans `04` et `06` (≈ 5 points par décade, comme avant).
5. Relancer `16_diag_alpha.py` (→ `alpha_bornes_apres.csv`) puis `python src/04_models.py` (~5 min).
6. `python tests/snapshot.py save apres02` ; `diff avant02 apres02`.

## Validation
- [ ] « Avant » : reproduit la revue (CAC 40 : ≈ 75 % M0, 79 % M1, 99 % M2 à la borne ; spread/OAT : 0 à 10 %). Sinon comprendre l'écart avant de continuer.
- [ ] « Après » : < 5 % des mois à la borne 10⁶, pour les 3 cibles et 3 jeux.
- [ ] Ridge : R² et DM bougent de moins de ~1 point de R² (revue : spread -15,0→-14,9 ; CAC M1 -2,7→-3,5). Sinon investiguer.
- [ ] RF et XGBoost : colonnes de `models_predictions_*.csv` **identiques** (`diff` : seules les colonnes `ridge|…` changent).
- [ ] Conclusions inchangées : R² < 0 partout, DM M1 vs M0 p > 0,3.
- [ ] Contrôle négatif du diagnostic : avec une grille volontairement tronquée (10⁻²…10⁻¹), il signale ~100 % à la borne.
- [ ] `python tests/verifications.py` passe (31/31).

## Commit
`04/06 : grille RidgeCV élargie à 10^6 (alpha bloqué à la borne pour le CAC 40) ; diagnostic 16_diag_alpha ; relance de 04`
