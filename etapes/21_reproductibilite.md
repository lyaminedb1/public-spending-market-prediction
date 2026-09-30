# Étape 21 — Versions figées, gel des données, relance en une commande

**Statut : ✅ fait.**

**Dépend de** : toutes les étapes de code jusqu'à 20.

## Actions
1. `requirements.txt` : figer les versions (à partir de `pip freeze`, étape 00) pour les paquets utilisés + `scipy`, `pytest` si utilisé.
2. **Gel des données** : `tests/data_manifest.py` écrit `data/MANIFEST.csv` (chemin, taille, md5) pour tout `data/raw/**` et `data/processed/**` ; les tests vérifient que les données brutes n'ont pas changé.
3. `run_all.sh` : `set -e`, dans l'ordre 02 → 05 → 03 → 04 → 16 → 15 (jobs Ridge) → 06 (E1…E13 dans l'ordre) → 14 (E19, E20) → 06 resume → 07 → 17 → 18 → 19 → 20 → tests. Option `--rapide` : 02, 05, 04 sur une cible, tests. Les scripts de collecte (01, 08-10, 13) sont derrière `--collecte`.
4. README : remplacer « Utilisation » par les commandes de reproduction ; corriger la structure (les notebooks 01, 02 et 04 n'existent pas : ne lister que `03_EDA.ipynb`).

## Validation
- [x] Environnement neuf (`python -m venv /tmp/venv_test`) + `pip install -r requirements.txt` réussit.
- [x] `./run_all.sh --rapide` réussit dans l'environnement neuf.
- [x] Le script s'arrête à la première erreur.
- [x] Modifier un octet d'un fichier brut fait échouer le contrôle du manifeste (contrôle négatif).

## Commit
`Reproductibilité : versions figées, manifeste des données, run_all.sh, README à jour`

## Résultat (29/09)
- `requirements.txt` : 14 paquets aux versions exactes utilisées (pandas 3.0.6, numpy 2.4.6, scikit-learn 1.9.1, xgboost 3.2.0, statsmodels 0.15.0, shap 0.51.0, scipy 1.17.1…). Environnement neuf (`python -m venv`) : installation en 2 min 40 s sans erreur.
- `data/MANIFEST.csv` (41 fichiers de `data/raw/`, md5) et `tests/data_manifest.py write|check` ; contrôle « 0 » de `verifications.py` (63 contrôles) : un octet ajouté à `data/raw/vix.csv` est détecté (« modifié : data/raw/vix.csv »).
- `run_all.sh` : options `--rapide` (jeu de données, exploration, `04 --from-saved`, synthèses, contrôles : **56 s** dans l'environnement neuf, 63/63), défaut (tout sauf diagnostics longs et collecte), `--diag`, `--collecte`. `set -e` : un échec s'arrête immédiatement (testé avec `PYTHON=false`, code 1 ; option inconnue : code 2). La relance complète est validée à l'étape 22.
- Les sorties versionnées n'ont pas changé après `--rapide` (`git status` : seul le notebook, régénéré avec ses horodatages, diffère ; restauré).
- README : utilisation, tableau des scripts, structure réelle (un seul notebook), tests. Le mode « sur une seule cible » du plan est remplacé par `--from-saved` (plus rapide et plus utile).
