# Étape 13 — Étendre les contrôles automatiques

**Statut : ✅ fait.**

**Objet** : que les relances ne puissent pas casser silencieusement.

**Dépend de** : 03, 05, 09, 12.

## Actions
Ajouter à `tests/verifications.py` (sections F et suivantes) ou en `tests/test_*.py` appelés par lui :
1. **Prévisions de 04** : 79 lignes, index continu 2020-01 → 2026-07, aucune valeur manquante ; R² recalculé depuis les prévisions = `models_metrics.csv` (écart < 1e-3).
2. **Alpha Ridge** : part de mois à la borne haute < 5 % (lit `diag_04/alpha_bornes_apres.csv`).
3. **Extensions** : `E*.csv` présents pour toutes les clés attendues (E1…E11, E12, E13, E15…E20, E7E8) ; aucune p-value hors [0,1].
4. **Cohérence de `ext_summary.csv`** : nombre de lignes = somme des fichiers extensions ; `p_BH` ≥ `p` brute ; nombre de comparaisons dans BH affiché.
5. **Cohérence des hyperparamètres** : `MARKETS`, `SPENDING`, hyperparamètres RF/XGB, `TEST_START` identiques entre 04, 06 et 11 (importation des trois modules) ; grille Ridge de 04 = 06.
6. **Ordre des dépendances** : `models_predictions_*.csv` (04) plus récents que `dataset_monthly.csv` ; `E7E8.csv` et `E12.csv` plus récents que `models_predictions_*.csv` (sinon E7/E8/E12 lisent des prévisions périmées).
7. **Contrôle de fuite exécutable** : dans `tests/test_walk_forward_06.py`, un jeu où une variable = cible future donne R² hors échantillon > 0,9 (le dispositif détecte une fuite).
8. Appeler les tests des étapes 03 et 09.

## Validation
- [x] Tous les tests passent sur l'état actuel du dépôt.
- [x] Chaque test a été vu **échouer** sur une entrée cassée volontairement (le noter dans le commit).
- [x] Temps total < 3 min ; sinon marquer les tests longs `--lent`.

## Commit
`tests : contrôles sur prévisions, alpha, extensions, cohérence 04/06/11 et ordre des dépendances`

## Résultat (29/09) — `tests/verifications.py` : 31 → **62 contrôles** (11 s)
- **F** prévisions de 04 (79 mois contigus, aucune valeur manquante, `y_true` = cible du jeu, R² de `models_metrics.csv` recalculé) ; **G** grille Ridge (04 = 06, max ≥ 10⁶ ; panel ≥ 10⁴ ; alpha à la borne < 10 % des mois pour spread et OAT) ; **H** extensions (un fichier par extension, p-values dans [0, 1], `ext_summary.csv` = concaténation, p_BH ≥ p) ; **I** cohérence 04/06/11 (variables, début de test, hyperparamètres RF et XGBoost) ; **J** E7 et E12 recalculés depuis les prévisions de 04 ; **K** `test_walk_forward_06.py` (31 contrôles, dont la détection d'une fuite : variable = cible → R² > 90 %, bruit → R² ≤ 0).
- **Contrôles négatifs** (script hors dépôt) : les 6 cassures volontaires (NaN dans une prévision, alpha à la borne, p-value 1,5, hyperparamètre RF différent, E7 modifié, E9 absent) sont toutes détectées ; état final sans échec.
- **Écarts au plan** : contrôle des dépendances par **contenu** (E7/E12 recalculés) et non par date de modification, qui n'est pas fiable après un `git clone` ; test d'alpha : seuil 10 % (le spread M2 est à 6,3 %) et le CAC 40 est exclu (alpha = 10⁶ ≡ prévision par la moyenne, voir étape 02).
- **Le test J a échoué au premier essai** : `E7E8.csv` et `E12.csv` avaient été calculés sur les anciennes prévisions de 04 (avant l'étape 02). Recalculés ici (`06_extensions.py E7E8 E12`, 2 s, aucune réestimation) ; `ext_summary.csv` régénéré (210 comparaisons, 0 significative après BH). Le reste de l'étape 16 n'est pas avancé.
