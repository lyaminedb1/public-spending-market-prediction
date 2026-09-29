# Étape 21 — Versions figées, gel des données, relance en une commande

**Dépend de** : toutes les étapes de code jusqu'à 20.

## Actions
1. `requirements.txt` : figer les versions (à partir de `pip freeze`, étape 00) pour les paquets utilisés + `scipy`, `pytest` si utilisé.
2. **Gel des données** : `tests/data_manifest.py` écrit `data/MANIFEST.csv` (chemin, taille, md5) pour tout `data/raw/**` et `data/processed/**` ; les tests vérifient que les données brutes n'ont pas changé.
3. `run_all.sh` : `set -e`, dans l'ordre 02 → 05 → 03 → 04 → 16 → 15 (jobs Ridge) → 06 (E1…E13 dans l'ordre) → 14 (E19, E20) → 06 resume → 07 → 17 → 18 → 19 → 20 → tests. Option `--rapide` : 02, 05, 04 sur une cible, tests. Les scripts de collecte (01, 08-10, 13) sont derrière `--collecte`.
4. README : remplacer « Utilisation » par les commandes de reproduction ; corriger la structure (les notebooks 01, 02 et 04 n'existent pas : ne lister que `03_EDA.ipynb`).

## Validation
- [ ] Environnement neuf (`python -m venv /tmp/venv_test`) + `pip install -r requirements.txt` réussit.
- [ ] `./run_all.sh --rapide` réussit dans l'environnement neuf.
- [ ] Le script s'arrête à la première erreur.
- [ ] Modifier un octet d'un fichier brut fait échouer le contrôle du manifeste (contrôle négatif).

## Commit
`Reproductibilité : versions figées, manifeste des données, run_all.sh, README à jour`
