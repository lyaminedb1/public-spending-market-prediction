# Étape 18 — Versions figées et relance en une commande

**Dépend de** : toutes les étapes de code.

## Actions
1. `requirements.txt` : fixer les versions (à partir de `pip freeze` de l'étape 00) pour les paquets utilisés (pandas, numpy, scikit-learn, xgboost, statsmodels, shap, matplotlib, scipy, jupyter, pytest si utilisé).
2. `run_all.sh` (ou `Makefile`) : enchaîne 02 → 03 → 04 → 16_seeds → … → 05 → 06 → 14 → 06 resume → 07, avec une option `--rapide` qui lance seulement les vérifications et 04 sur une seule cible.
3. Ne pas inclure les scripts de collecte (01, 08-10, 13) par défaut : réseau et FRED bloqué ; les données brutes sont dans le dépôt. Option `--collecte` séparée.
4. README : remplacer la section « Utilisation » par les commandes de reproduction (une section factuelle, pas de rédaction du mémoire).

## Validation
- [ ] Environnement neuf (`python -m venv /tmp/venv_test`) + `pip install -r requirements.txt` réussit.
- [ ] `./run_all.sh --rapide` réussit dans cet environnement neuf.
- [ ] Le script s'arrête à la première erreur (`set -e`).

## Commit
`Reproductibilité : versions figées, run_all.sh, README à jour`
