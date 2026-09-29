# Étapes de finalisation du code

Chaque fichier = **un petit bloc** : implémenter → tester → valider → commit. Rien de rédactionnel.
À faire **dans l'ordre** (les dépendances sont indiquées). Ne passer à l'étape suivante que si la section
« Validation » est entièrement cochée.

## Règles communes
1. Une étape = un commit (message donné dans chaque fichier). Ne jamais mélanger deux étapes.
2. Toute modification doit être justifiée par une **erreur de méthode**, pas par le résultat obtenu (règle du projet).
3. Avant de changer un calcul, on a un instantané de référence (étape 01) ; après, on compare avec `git diff` / script de comparaison.
4. Les sorties (`results/`, `data/processed/`) modifiées par une relance sont commitées avec le code qui les produit.
5. Chaque étape ajoute si possible un contrôle automatique dans `tests/verifications.py` (ou `tests/`), pour ne pas régresser.
6. Si une validation échoue : corriger ou s'arrêter et signaler. Jamais désactiver un test.

## Ordre

| # | Fichier | Objet | Durée de calcul |
|---|---|---|---|
| 00 | `00_environnement.md` | Environnement Python + tests de base verts | — |
| 01 | `01_instantane_reference.md` | Photographier les sorties actuelles | — |
| 02 | `02_grille_ridge.md` | Élargir la grille RidgeCV (04, 06) | 5 min |
| 03 | `03_audit_walk_forward_06.md` | Vérifier que `walk_forward` de 06 compte en mois | — |
| 04 | `04_graines.md` | Fourchettes par graine (RF, XGB) | ~10 min |
| 05 | `05_references_naives.md` | Deux références (moyenne, variation nulle) + DM | — |
| 06 | `06_shap_bruit.md` | Référence de bruit pour SHAP | ~3 min |
| 07 | `07_importance_permutation.md` | Importance par permutation hors échantillon | ~5 min |
| 08 | `08_parametrer_decalage.md` | Décalage budgétaire paramétrable (02) + chemins (04) | — |
| 09 | `09_robustesse_decalage3.md` | Robustesse : décalage de 3 mois | 5 min |
| 10 | `10_tests_automatiques.md` | Étendre les contrôles automatiques | — |
| 11 | `11_relance_03_exploration.md` | Relancer 03 + notebook | 1 min |
| 12 | `12_relance_05.md` | Relancer 05 (variables supplémentaires) | 1 min |
| 13 | `13_relance_06_rapides.md` | E1-E9, E11-E13 | ~20 min |
| 14 | `14_relance_06_e10.md` | E10 (XGBoost réglé) | ~15 min |
| 15 | `15_relance_14_e20.md` | E20 (+ contrôle E17-E19) | ~5 min |
| 16 | `16_bh_et_synthese.md` | Correction BH + tableau/figure de synthèse | 1 min |
| 17 | `17_panel_11_conditionnel.md` | Grille Ridge de 11 (seulement si nécessaire) | 0 ou 16 min |
| 18 | `18_reproductibilite.md` | Versions figées + script de relance complet | — |
| 19 | `19_regression_finale.md` | Relance de bout en bout + mise à jour de CLAUDE.md | ~1 h |

## Pas dans ce dossier (décidé)
- E14 (étude d'événement) : données quotidiennes introuvables par script, reste en perspectives.
- Toute rédaction (chapitres, résumé, soutenance).
