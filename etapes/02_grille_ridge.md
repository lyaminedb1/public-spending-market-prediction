# Étape 02 — Grille RidgeCV trop étroite (constat 8 de la revue de 04)

**Statut : ✅ fait.** Résultats et écarts au plan ci-dessous (section « Résultat »).

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
- [x] « Avant » : reproduit la revue (CAC 40 : ≈ 75 % M0, 79 % M1, 99 % M2 à la borne ; spread/OAT : 0 à 10 %). Sinon comprendre l'écart avant de continuer.
- [x] « Après » : spread/OAT ≤ 6 % ; CAC 40 reste à la borne (équivaut à la prévision par la moyenne, voir Résultat) — critère remplacé par la vérification que alpha = 10⁶ ≡ moyenne.
- [x] Ridge : R² et DM bougent de moins de ~1 point de R² (revue : spread -15,0→-14,9 ; CAC M1 -2,7→-3,5). Sinon investiguer.
- [x] RF et XGBoost : colonnes de `models_predictions_*.csv` **identiques** (`diff` : seules les colonnes `ridge|…` changent).
- [x] Conclusions inchangées : R² < 0 partout, DM M1 vs M0 p > 0,3.
- [x] Contrôle négatif du diagnostic : avec une grille volontairement tronquée (10⁻²…10⁻¹), il signale ~100 % à la borne.
- [x] `python tests/verifications.py` passe (31/31).

## Commit
`04/06 : grille RidgeCV élargie à 10^6 (alpha bloqué à la borne pour le CAC 40) ; diagnostic 16_diag_alpha ; relance de 04`

## Résultat (29/09)
- **Avant** : reproduit la revue (CAC 40 : 74,7 % M0, 78,5 % M1, 98,7 % M2 à la borne 1000 ; spread/OAT : 0 à 10 %). Panel (11, grille 10⁴) : 0 % à la borne → **l'étape 20 est inutile**.
- **Après** (grille 10⁻²…10⁶) : spread/OAT 0 à 6 % ; CAC 40 encore 25 % (M0), 35 % (M1), 90 % (M2) à la borne 10⁶. **Écart au critère prévu (< 5 %)** : ce n'est pas un défaut de réglage. À alpha = 10⁶ la prévision Ridge est égale à la moyenne d'entraînement (écart max 0,0018 point sur 79 mois) : le critère de validation croisée préfère « ne rien prédire » ; élargir davantage ne change rien.
- **Différences de versions de bibliothèques** : les colonnes RF des sorties commitées (machine d'origine) diffèrent de celles recalculées ici (jusqu'à 0,05 sur ΔOAT). Le contrôle « RF/XGBoost identiques » a donc été fait contre un état de référence recalculé **dans cet environnement avec l'ancienne grille** : RF et XGBoost identiques à 1e-15 près ; seul Ridge change.
- Ridge : écarts de R² de -1,15 à +1,20 point (spread M0 -14,99 → -14,89 ; CAC M1 -2,66 → -3,50). Conclusions inchangées : R² < 0 partout ; DM M1 vs M0, p bilatérale minimale 0,366.
- Environnement : numpy 2.4.6, pandas 3.0.6, scikit-learn 1.9.1, xgboost 3.2.0. `04_models.py` prend ~10 min (pas 5).
- Conséquence pour les étapes suivantes : après une relance, les colonnes RF (et éventuellement XGBoost) peuvent différer légèrement des sorties commitées **sans que le code ait changé** ; toujours comparer à un état de référence produit dans le même environnement.
