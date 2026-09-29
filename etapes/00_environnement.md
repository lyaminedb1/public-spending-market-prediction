# Étape 00 — Environnement et tests de base

**Statut : ✅ fait (31/31 contrôles OK).**

**Pourquoi** : l'environnement actuel n'a ni numpy ni pandas ; aucune validation n'est possible sans lui.

## Actions
1. Créer un venv à la racine (hors dépôt, ou `.venv/` déjà ignoré par `.gitignore` — vérifier) :
   `python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt`.
2. Noter les versions installées : `pip freeze > /tmp/freeze_00.txt` (servira à l'étape 18).
3. Vérifier que xgboost et shap s'importent (`python -c "import xgboost, shap"`). Si libomp manque, le signaler.
4. Lancer `python tests/verifications.py`.

## Validation
- [x] `import pandas, numpy, sklearn, xgboost, shap, statsmodels, matplotlib` sans erreur.
- [x] `tests/verifications.py` termine sans échec (noter le nombre de contrôles, ex. « N/N OK »).
- [x] `git status` propre (aucun fichier suivi modifié).

## Commit
Aucun (environnement local). Consigner dans le message de l'étape 01 le nombre de contrôles OK.
