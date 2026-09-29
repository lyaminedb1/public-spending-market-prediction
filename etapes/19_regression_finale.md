# Étape 19 — Relance de bout en bout et mise à jour de CLAUDE.md

**Dépend de** : 00-18.

## Actions
1. Depuis un dépôt propre : `./run_all.sh` complet (~1 h).
2. `python tests/snapshot.py save final` ; `diff` contre l'état des étapes précédentes : aucune sortie inattendue.
3. `python tests/verifications.py` et tous les tests : verts.
4. Mettre à jour `CLAUDE.md` : retirer tous les avertissements « ancien jeu de données » ; remplacer les chiffres E1-E13, E20, BH par ceux des CSV ; ajouter les nouveaux scripts (16-19) et le dossier `etapes/`. Chaque chiffre est copié d'un fichier de `results/tables`, jamais ré-écrit de mémoire.
5. Vérification croisée : script qui extrait de `CLAUDE.md` les nombres clés (R² du meilleur modèle, DM min/max, nombre de comparaisons BH) et les compare aux CSV.

## Validation
- [ ] Deux relances complètes consécutives produisent des CSV identiques (reproductibilité).
- [ ] Tous les tests passent.
- [ ] Les nombres de CLAUDE.md correspondent aux CSV (script de l'action 5).
- [ ] `git status` propre ; branche poussée.

## Commit
`Relance complète, CLAUDE.md aligné sur les résultats`
