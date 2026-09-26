# Contexte du projet — Mémoire MSc (ECE Paris)

## Le mémoire
- **Titre validé** : « Prédiction d'indicateurs des marchés financiers à partir des données de dépenses publiques ouvertes : une approche par machine learning »
- **Problématique validée** : Peut-on prédire des indicateurs des marchés financiers à partir des données de dépenses publiques ouvertes en utilisant des techniques de machine learning ?
- **Auteur** : Abdellah Elyamine DALI BRAHAM — MSc Data Management & IA, ECE Paris
- **Encadrante** : Dr. Yosra Hajjaji
- **Date limite de remise** : 10 octobre 2026
- **Langue de rédaction** : français. Rédaction finale prévue en LaTeX.

## Périmètre (décidé, ne pas changer sans accord)
- **Pays** : France. **Fréquence** : mensuelle. **Période** : 2013 à aujourd'hui (environ 150 mois).
- **Trois variables cibles** (horizon : mois suivant, t+1) :
  1. Variation mensuelle du spread OAT–Bund 10 ans (en points de base) — cible principale
  2. Variation mensuelle du taux OAT 10 ans (en points de base)
  3. Rendement mensuel du CAC 40 (en %)
  Variante secondaire : classification hausse/baisse.
- Les cibles sont fixées a priori. Ne pas choisir les cibles en fonction des corrélations observées (data snooping).

## Variables explicatives
- **Principales — dépenses de l'État** (situation mensuelle budgétaire, séries longues, data.economie.gouv.fr, jan. 2013 – juil. 2026) : dépenses par titre (personnel, fonctionnement, charge de la dette, investissement, intervention) et prélèvements sur recettes. Pas de ventilation par mission dans ces fichiers. Les opérations financières sont exclues (montants irréguliers, pas une dépense économique).
- **Contrôles** : recettes, solde d'exécution, valeur passée de la cible, taux directeurs BCE (MRO, facilité de dépôt), taux Bund, VIX (aversion au risque), inflation France (IPCH).

## Règles de construction des données
- Les montants budgétaires sont **cumulés depuis janvier** : les différencier pour obtenir des flux mensuels.
- Forte saisonnalité : deux transformations par ligne budgétaire : somme glissante sur 12 mois (`_12m`, Md€) et écart du cumul depuis janvier par rapport au même mois de l'année précédente, en % du total annuel (`_ytd_gap`). Pas de taux de croissance du cumul : il explose en début d'année (base proche de zéro).
- **Décalage de publication** : la situation du mois M est publiée environ 5 semaines après (juin 2026 publié le 6 août 2026). À la fin du mois t, seul le budget de t-2 est connu : les variables budgétaires sont décalées de 2 mois (`BUDGET_LAG = 2`). Sinon biais d'anticipation (look-ahead bias).
- Décembre : version provisoire puis définitive (révisions, à mentionner comme limite).
- OAT/Bund FRED = moyennes mensuelles (OCDE). CAC 40 `^FCHI` = indice de prix, hors dividendes.

## Jeu de données construit
- `python src/02_build_dataset.py` → `data/processed/dataset_monthly.csv` : 150 mois (2014-03 → 2026-08), 149 avec cible. Préfixe `y_` = cibles, `b_` = budget (décalé de 2 mois), le reste = marchés et contrôles en t.
- Vérification : les soldes annuels reconstitués correspondent aux chiffres officiels (-85,6 Md€ en 2014, -178,1 en 2020, -173,0 en 2023, -155,9 en 2024).
- Taux OAT/Bund = moyennes mensuelles : les variations de moyennes sont mécaniquement un peu autocorrélées (à signaler, et raison de toujours inclure la variation passée).

## Analyse exploratoire (`python src/03_exploration.py`)
- Figures : `results/figures/fig3_1_*.png` ; tableaux : `results/tables/eda_*.csv`.
- Cibles stationnaires (ADF p < 0,01) ; niveaux (spread, OAT, solde, charge de la dette) non stationnaires → on modélise des variations.
- Autocorrélation d'ordre 1 : Δspread 0,14 ; ΔOAT 0,23 ; CAC 40 -0,09.
- Corrélations de Spearman budget (t-2) / cibles (t+1), seuil 5 % = ±0,16 : spread → seul l'investissement (-0,16) ; ΔOAT → personnel 0,23, charge de la dette 0,21, fonctionnement 0,17, mais ces liens tombent à 0,07–0,13 une fois l'inflation contrôlée (confusion avec le régime d'inflation 2022-2023) ; CAC 40 → rien de significatif.
- Conclusion d'étape : signal budgétaire faible et en partie confondu avec l'inflation → l'inflation doit rester dans le modèle « contrôles seuls ».

## Modèles et évaluation
- Modèles : naïf (marche aléatoire / moyenne), régression linéaire avec retards, forêt aléatoire, XGBoost. **Pas de deep learning** (trop peu d'observations).
- Comparaison clé : modèle « contrôles seuls » contre « contrôles + dépenses ».
- Validation glissante (walk-forward), jamais de validation croisée aléatoire.
- Métriques : RMSE, MAE, taux de bonne direction ; test de Diebold-Mariano.
- Importance des variables : SHAP ou permutation importance.

## Hypothèses
- H1 : pour au moins un indicateur, ajouter les dépenses améliore la prévision.
- H2 : l'apport décroît du spread, au taux OAT, puis au CAC 40.
- H3 : forêt aléatoire / XGBoost font mieux que les modèles linéaires.
- H4 : parmi les dépenses, la charge de la dette et les dépenses d'intervention sont les plus prédictives.
- Un résultat négatif pour H1 est plausible (efficience des marchés, Fama 1970 ; anticipation, Ramey 2011) et reste valable.

## Référence la plus proche
Bouillot, Candelon & Kool (2025), *Forecasting European sovereign spreads using machine learning*, UCLouvain : prévision à un mois des spreads de 10 pays dont la France, XGBoost en tête, le spread passé domine.

## Structure du dépôt
- `data/raw/` : données brutes (`src/01_collect_data.py` télécharge FRED, BCE, CAC 40) ; `data/raw/budget/` : CSV budgétaires téléchargés à la main.
- `data/processed/` : jeu de données mensuel nettoyé.
- `notebooks/` : 01_collecte, 02_nettoyage, 03_exploration, 04_modeles.
- `src/` : scripts et fonctions réutilisables.
- `results/figures/` : graphiques pour le mémoire ; `results/tables/` : tableaux.

## Plan du mémoire
Introduction · Ch.1 État de l'art (rédigé) · Ch.2 Données et méthodologie · Ch.3 Résultats · Ch.4 Discussion · Conclusion · Bibliographie · Annexes.
