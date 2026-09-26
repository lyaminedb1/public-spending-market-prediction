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
Travailler dans un environnement dédié (ne pas installer dans l'environnement `base` d'Anaconda) :
```bash
conda create -n memoire python=3.11 -y
conda activate memoire
pip install -r requirements.txt
python src/01_collect_data.py
```

## Structure
```
data/raw/           données brutes
data/raw/budget/    CSV budgétaires (téléchargement manuel)
data/processed/     jeu de données mensuel nettoyé
notebooks/          exploration et modélisation
src/                scripts
results/figures/    graphiques
```
