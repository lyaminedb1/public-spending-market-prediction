# Prédiction d'indicateurs des marchés financiers à partir des données de dépenses publiques ouvertes

Mémoire de MSc Data Management & IA — ECE Paris (2026).
Auteur : Abdellah Elyamine Dali Braham · Encadrante : Dr. Yosra Hajjaji

## Objectif
Tester si les données ouvertes d'exécution budgétaire de l'État français améliorent la prévision mensuelle de trois indicateurs de marché :

| Cible (mois suivant) | Unité |
| --- | --- |
| Variation du spread OAT–Bund 10 ans | points de base |
| Variation du taux OAT 10 ans | points de base |
| Rendement du CAC 40 | % |

Modèles comparés : naïf, régression linéaire, forêt aléatoire, XGBoost — avec et sans variables de dépenses publiques, en validation glissante.

## Données
| Source | Contenu | Obtention |
| --- | --- | --- |
| [data.economie.gouv.fr](https://data.economie.gouv.fr/explore/assets/situations-mensuelles-budgetaires-series-longues/) | Situations mensuelles budgétaires de l'État (séries longues, 2013–) | Téléchargement manuel → `data/raw/budget/` |
| FRED | Taux 10 ans France et Allemagne (OCDE), VIX, IPCH France | `src/01_collect_data.py` |
| BCE | Taux MRO et facilité de dépôt | `src/01_collect_data.py` |
| Yahoo Finance | CAC 40 (`^FCHI`) | `src/01_collect_data.py` |

## Utilisation
Travailler dans un environnement dédié (Python 3.11 ; ne pas installer dans l'environnement `base` d'Anaconda) :
```bash
python -m venv .venv && . .venv/bin/activate      # ou : conda create -n memoire python=3.11
pip install -r requirements.txt                    # versions figées : les sorties de RandomForest/XGBoost en dépendent
./run_all.sh --rapide                              # ~2 min : jeu de données, exploration, tableaux depuis les prévisions sauvegardées, contrôles
./run_all.sh                                       # ~1 h 30 : tout recalculer (hors diagnostics longs et collecte)
./run_all.sh --diag                                # ajoute les diagnostics de la revue de 04 (~1 h 30 de plus)
./run_all.sh --collecte                            # ajoute la collecte réseau (FRED via curl, BCE, Yahoo Finance, Eurostat)
python tests/verifications.py                      # 63 contrôles automatiques (données, décalages, fuite, cohérence des résultats)
python tests/check_claude_md.py                    # les nombres cités dans CLAUDE.md correspondent aux CSV
```
Les données brutes sont dans le dépôt et gelées par `data/MANIFEST.csv` (`python tests/data_manifest.py check`).

## Scripts (`src/`)
| Script | Rôle | Sorties |
| --- | --- | --- |
| `01_collect_data.py`, `09`, `10`, `13` | collecte (réseau) | `data/raw/` |
| `02_build_dataset.py` (`--lag N`) | jeu mensuel, budget décalé de 2 mois | `data/processed/dataset_monthly*.csv` |
| `03_exploration.py`, `make_eda_notebook.py` | exploration | `results/figures/fig3_1_*`, `notebooks/03_EDA.ipynb` |
| `04_models.py` (`--from-saved`, `--data --suffix`) | modèles principaux M0/M1/M2, DM, BH, SHAP | `results/tables/models_*.csv`, `fig3_2` à `fig3_4` |
| `05_extra_features.py`, `06_extensions.py` (E1-E13), `14_more_extensions.py` (E17-E20), `07_extensions_summary.py` | extensions pré-enregistrées (`docs/plan_extensions.md`) | `results/tables/extensions/`, `ext_summary.csv`, `ext_synthese.csv`, `ext_significatifs.csv`, `fig3_5`, `fig3_6` |
| `11_panel_models.py` (E15-E16), `12_diag_e15.py` | panel européen | `results/tables/extensions/E15*.csv`, `E16*.csv` |
| `15_diag_04.py`, `16_diag_alpha.py`, `17_permutation_oos.py` | diagnostics de la revue de `04` | `results/tables/diag_04/`, `models_permutation_oos.csv` |
| `18_hypotheses.py`, `19_robustesse_lag.py`, `20_limites_chiffres.py`, `21_verif_chiffres_03.py`, `22_verif_extensions.py` | tableaux dérivés et vérifications | `hypotheses.csv`, `robustesse_lag.csv`, `limites_chiffres.csv`, `diag_04/verif_*.csv` |
| `config.py` | constantes communes (décalage budgétaire, début du test) | |

## Structure
```
data/raw/           données brutes (gelées par data/MANIFEST.csv) ; data/raw/budget/ : CSV budgétaires téléchargés à la main
data/processed/     jeu de données mensuel et variables supplémentaires
notebooks/          03_EDA.ipynb (exploration)
src/                scripts numérotés
tests/              verifications.py, test_walk_forward_06.py, test_tuned_xgb.py, snapshot.py, data_manifest.py
results/            figures/ et tables/ (dont extensions/, diag_04/, robustesse/)
docs/               plan des extensions, revue de 04, plan du chapitre 4
etapes/             plan de finalisation du code, une étape par fichier
```
