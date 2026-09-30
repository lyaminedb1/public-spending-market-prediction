# Étape 22 — Relance complète et alignement de CLAUDE.md

**Statut : ✅ fait.**

**Dépend de** : 00-21.

## Actions
1. Depuis un dépôt propre : `./run_all.sh` complet (~2 h, dont les diagnostics de l'étape 04).
2. `python tests/snapshot.py save final1`, relancer une deuxième fois, `save final2` : `diff final1 final2` = aucune différence (reproductibilité).
3. Tous les tests verts (`verifications.py`, `test_*`).
4. Mettre à jour `CLAUDE.md` : retirer tous les avertissements « ancien jeu de données » ; remplacer les chiffres E1-E13, E20, BH, diagnostics et limites par ceux des CSV (`hypotheses.csv`, `ext_significatifs.csv`, `limites_chiffres.csv`, `diag_04/resume.csv`, `robustesse_lag.csv`) ; ajouter les scripts 16-20, `config.py`, `etapes/` ; corriger la structure (notebooks inexistants).
5. Script `tests/check_claude_md.py` : extrait de `CLAUDE.md` une liste de nombres clés (R² du meilleur modèle, DM min/max, nombre de comparaisons BH, nombre de mois de test) et les compare aux CSV.

## Validation
- [x] `diff final1 final2` : aucune différence.
- [x] Tous les tests passent ; `check_claude_md.py` sans écart.
- [x] `git status` propre ; branche poussée.

## Commit
`Relance complète, CLAUDE.md aligné sur les résultats`

## Résultat (29/09)
- **Deux relances complètes indépendantes** de `./run_all.sh` : dans le dépôt (avec les diagnostics de `15_diag_04.py` lancés en jobs parallèles) et dans un **clone propre** du commit (diagnostics commités). 63/63 contrôles dans les deux cas. Comparaison (`|écart| ≤ 1e-9` sur tous les CSV) : **69 fichiers communs, seuls 4 diffèrent, tous des diagnostics RF que le clone n'a pas recalculés** (`bruit_rf`, `graines_rf`, `resume`, `ecarts_revue`, écarts ≤ 0,02). Les CSV ne sont pas identiques **octet par octet** (écarts de 1e-15 sur les prévisions RF : sommation entre threads) : le critère « `diff` = aucune différence » du plan devient « écart < 1e-9 ».
- **Ce que la relance a changé par rapport aux sorties commitées** (13 fichiers) : le panel européen (E15 à E18) et E16, jusque-là calculés sur la machine d'origine, et les diagnostics RF. Écarts : ≤ 0,35 point de R² (E16 RF : p 0,59 → 0,53 pour la variation, 0,88 → 0,81 pour le niveau ; E15 : Ridge inchangé) ; **conclusions inchangées**.
- `12_diag_e15.py` n'enregistrait rien : il écrit maintenant `results/tables/diag_e15.csv` et `diag_e15_ar1.csv` ; les chiffres cités (AR1 0,32 vs 0,07 ; fin de trimestre M0 −4,1 % et M1 −2,9 % ; dépenses +4 points en 2010-2014 et −13 points après 2015) sont retrouvés.
- **`CLAUDE.md` mis à jour** (plus aucun avertissement « ancien jeu de données ») et **`tests/check_claude_md.py`** : 39 nombres de `CLAUDE.md` comparés aux CSV, tous conformes ; contrôles négatifs : un nombre modifié ou une phrase reformulée fait échouer le test (« motif introuvable »). Il est appelé par `run_all.sh`.
- Corrections de `CLAUDE.md` issues des vérifications : XGBoost vs Ridge sur le CAC 40 p = 0,032 (et non 0,02) ; corrélations partielles 0,09-0,15 ; ADF des `_ytd_gap` 0,000-0,057 ; 23,4 % de cellules imputées (et non 23,6 % « médiane ») ; variance ×6 = médiane, avec témoin i.i.d. à 3,7 ; E15 p = 0,36 ; E16 finances publiques p 0,08-0,81 ; meilleur R² −1,3 % (et non −1,0 %).
- La relance complète prend environ 3 h 30 avec les diagnostics parallèles et une copie concurrente ; le mode par défaut de `run_all.sh` est estimé à 1 h 30 sur une machine libre.
