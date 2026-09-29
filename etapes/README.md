# Étapes de finalisation du code

Chaque fichier = **un petit bloc** : implémenter → tester → valider → commit. Rien de rédactionnel.
À faire **dans l'ordre**. Ne passer à l'étape suivante que si la section « Validation » est entièrement cochée.
Environnement : `. .venv/bin/activate` (étape 00).

## Règles communes
1. Une étape = un commit (message donné dans chaque fichier). Ne jamais mélanger deux étapes.
2. Toute modification doit être justifiée par une **erreur de méthode**, pas par le résultat obtenu (règle du projet).
3. Avant chaque étape qui change un calcul : `python tests/snapshot.py save avantNN` ; après : `save apresNN` puis `diff avantNN apresNN`.
4. Les sorties (`results/`, `data/processed/`) modifiées par une relance sont commitées avec le code qui les produit.
5. Chaque contrôle est vu **échouer** sur une entrée cassée volontairement avant d'être accepté (contrôle négatif).
6. Si une validation échoue : corriger ou s'arrêter et signaler. Jamais désactiver un test.
7. Numérotation des nouveaux scripts (les 01-15 existent déjà) : 16 `diag_alpha`, 17 `permutation_oos`, 18 `hypotheses`, 19 `robustesse_lag`, 20 `limites_chiffres`.

## Ordre

| # | Fichier | Objet | Calcul |
|---|---|---|---|
| 00 ✅ | `00_environnement.md` | Environnement Python + 31 contrôles verts | — |
| 01 ✅ | `01_instantane_reference.md` | Outil d'instantané (`tests/snapshot.py`) | — |
| 02 ✅ | `02_grille_ridge.md` | Élargir la grille RidgeCV (04, 06) + mesure de l'alpha | 5 min |
| 03 ✅ | `03_audit_walk_forward_06.md` | `walk_forward` de 06 en mois ; cibles à horizon h | — |
| 04 ✅ | `04_diagnostics_15_relance.md` | Relancer les diagnostics de `15_diag_04` qui dépendent de Ridge + résumé | ~40 min |
| 05 ✅ | `05_references_et_bh_04.md` | Deux références (moyenne, zéro) + BH sur les tests de 04 | 5 min |
| 06 ✅ | `06_figure_shap_bruit.md` | Référence de bruit sur la figure 3.3 | 1 min |
| 07 ✅ | `07_permutation_oos.md` | Importance par permutation hors échantillon | ~5 min |
| 08 ✅ | `08_table_hypotheses.md` | Tableau H1-H4 généré par script | — |
| 09 ✅ | `09_parametrer_decalage.md` | Décalage budgétaire unique et paramétrable (02, 05, 04) | — |
| 10 ✅ | `10_robustesse_decalage3.md` | Robustesse : décalage de 3 mois | 5 min |
| 11 ✅ | `11_chiffres_limites.md` | Reproduire par script les chiffres des limites | — |
| 12 ✅ | `12_synthese_07_e15_e20.md` | Corriger 07 : E15-E20 absentes de la figure et de la synthèse | — |
| 13 ✅ | `13_tests_automatiques.md` | Étendre les contrôles automatiques | — |
| 14 ✅ | `14_relance_03_exploration.md` | Relancer 03 + notebook | 1 min |
| 15 ✅ | `15_relance_05.md` | Relancer 05 | 1 min |
| 16 | `16_relance_06_rapides.md` | E1-E9, E11-E13 | ~20 min |
| 17 | `17_relance_06_e10.md` | E10 (XGBoost réglé) | ~15 min |
| 18 | `18_relance_14_e19_e20.md` | E19 **et** E20 (Ridge change) | ~5 min |
| 19 | `19_bh_et_synthese_finale.md` | Correction BH + synthèse | 1 min |
| 20 ✅ | `20_panel_11_conditionnel.md` | Sans objet (0 % à la borne, mesuré étape 02) | 0 |
| 21 | `21_reproductibilite.md` | Versions figées, gel des données, `run_all.sh` | — |
| 22 | `22_regression_finale.md` | Relance complète, deux fois, + CLAUDE.md aligné | ~2 h |

## Corrections apportées à la première version du plan (revue du 29/09)
- **Doublon supprimé** : `15_diag_04.py` produit déjà `graines_*.csv` et `shap_bruit.csv`. Les anciennes étapes « graines » et « SHAP bruit » sont remplacées par la relance ciblée des seuls diagnostics qui dépendent de Ridge (`identite`, `cw`, `positif`, `bruit_ridge`, `cw_bruit_ridge`) ; RF et XGBoost ne changent pas.
- **Erreur corrigée** : l'ancienne étape E19/E20 supposait que E19 resterait identique. Or `14_more_extensions.py` utilise `reg_model` de 06 : la grille Ridge change aussi E19 et E20 (lignes Ridge seulement).
- **Trou comblé** : `07_extensions_summary.py` n'affiche que E0-E13 (LABELS ne contient ni E15 à E20 ; les colonnes d'E16 sont différentes). Étape 12.
- **Trou comblé** : E7, E8 et E12 lisent les prévisions de 04 → 04 doit être relancé avant 06 (dépendance explicite étape 16).
- **Trou comblé** : constante `BUDGET_LAG = 2` dupliquée dans 02 et 05 → source unique (étape 09).
- **Trou comblé** : incohérence possible entre `docs/revue_04_models.md` (SHAP bruit « 34-38 % ») et `diag_04/shap_bruit.csv` (premier tirage à 41-47 %) : à recalculer (étape 04).
- **Ajouts** : BH sur les 9+ tests de H1 dans 04 (05) ; tableau H1-H4 par script (08) ; chiffres des limites reproduits par script (11) ; test de cohérence des hyperparamètres 04/06/11 (13) ; gel des données par hash (21).

## Pas dans ce dossier (décidé)
- E14 (étude d'événement) : données quotidiennes introuvables par script, reste en perspectives.
- Collecte réseau (01, 08-10, 13) : les données brutes sont dans le dépôt et gelées (étape 21).
- Toute rédaction.
