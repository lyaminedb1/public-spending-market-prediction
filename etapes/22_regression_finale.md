# Étape 22 — Relance complète et alignement de CLAUDE.md

**Dépend de** : 00-21.

## Actions
1. Depuis un dépôt propre : `./run_all.sh` complet (~2 h, dont les diagnostics de l'étape 04).
2. `python tests/snapshot.py save final1`, relancer une deuxième fois, `save final2` : `diff final1 final2` = aucune différence (reproductibilité).
3. Tous les tests verts (`verifications.py`, `test_*`).
4. Mettre à jour `CLAUDE.md` : retirer tous les avertissements « ancien jeu de données » ; remplacer les chiffres E1-E13, E20, BH, diagnostics et limites par ceux des CSV (`hypotheses.csv`, `ext_significatifs.csv`, `limites_chiffres.csv`, `diag_04/resume.csv`, `robustesse_lag.csv`) ; ajouter les scripts 16-20, `config.py`, `etapes/` ; corriger la structure (notebooks inexistants).
5. Script `tests/check_claude_md.py` : extrait de `CLAUDE.md` une liste de nombres clés (R² du meilleur modèle, DM min/max, nombre de comparaisons BH, nombre de mois de test) et les compare aux CSV.

## Validation
- [ ] `diff final1 final2` : aucune différence.
- [ ] Tous les tests passent ; `check_claude_md.py` sans écart.
- [ ] `git status` propre ; branche poussée.

## Commit
`Relance complète, CLAUDE.md aligné sur les résultats`
