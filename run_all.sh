#!/usr/bin/env bash
# Relance complète du pipeline (données brutes déjà présentes dans data/raw/).
#   ./run_all.sh --rapide      contrôles + construction du jeu + tableaux/figures depuis les prévisions sauvegardées (~2 min)
#   ./run_all.sh               tout, sauf les diagnostics longs de la revue de 04 et la collecte (~1 h 30)
#   ./run_all.sh --diag        ajoute les diagnostics de 15_diag_04.py (~1 h 30 de plus)
#   ./run_all.sh --collecte    ajoute la collecte réseau (01, 08-10, 13 : dépend de sites externes, FRED via curl)
# Arrêt à la première erreur (set -e). Environnement : pip install -r requirements.txt
set -euo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-python}"
RAPIDE=0; DIAG=0; COLLECTE=0
for a in "$@"; do
  case "$a" in
    --rapide) RAPIDE=1 ;;
    --diag) DIAG=1 ;;
    --collecte) COLLECTE=1 ;;
    *) echo "option inconnue : $a"; exit 2 ;;
  esac
done
step() { echo; echo "=== $* ==="; }

if [ "$COLLECTE" = 1 ]; then
  step "Collecte des données (réseau)"
  for s in 01_collect_data 09_collect_panel 10_collect_large 13_collect_more; do $PY "src/$s.py"; done
fi

step "Jeu de données et variables supplémentaires"
$PY src/02_build_dataset.py
$PY src/05_extra_features.py
step "Exploration"
$PY src/03_exploration.py
$PY src/make_eda_notebook.py
$PY -m jupyter nbconvert --to notebook --execute notebooks/03_EDA.ipynb --output 03_EDA.ipynb --ExecutePreprocessor.timeout=600

if [ "$RAPIDE" = 1 ]; then
  step "Modèles principaux (depuis les prévisions sauvegardées)"
  $PY src/04_models.py --from-saved
else
  step "Modèles principaux (04) et diagnostics légers"
  $PY src/04_models.py
  $PY src/16_diag_alpha.py courant
  $PY src/17_permutation_oos.py
  $PY src/15_diag_04.py identite ar1 cw shap_bruit
  if [ "$DIAG" = 1 ]; then
    $PY src/15_diag_04.py positif bruit_ridge bruit_rf bruit_xgb graines_rf graines_xgb cw_bruit_ridge cw_bruit_xgb
  fi
  $PY src/15_diag_04.py resume ecarts_revue
  step "Robustesse au décalage budgétaire"
  for lag in 1 3; do
    $PY src/02_build_dataset.py --lag "$lag"
    $PY src/04_models.py --data "data/processed/dataset_monthly_lag${lag}.csv" --suffix "lag${lag}"
  done
  $PY src/19_robustesse_lag.py
  step "Extensions France (06) puis E19-E20 (14)"
  for k in E1 E2 E3 E4 E5 E6 E7E8 E9 E10 E11 E12 E13; do $PY src/06_extensions.py "$k"; done
  $PY src/14_more_extensions.py E19 E20
  step "Panel européen (11) et extensions E17-E18 (14)"
  $PY src/11_panel_models.py
  $PY src/12_diag_e15.py
  $PY src/14_more_extensions.py E17 E18
  $PY src/06_extensions.py resume
fi

step "Synthèses et tableaux dérivés"
$PY src/07_extensions_summary.py
$PY src/18_hypotheses.py
$PY src/20_limites_chiffres.py
$PY src/21_verif_chiffres_03.py
$PY src/23_event_study.py

step "Contrôles automatiques"
$PY tests/verifications.py
$PY tests/check_claude_md.py
echo; echo "Pipeline terminé."
