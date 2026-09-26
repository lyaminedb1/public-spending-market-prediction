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
- **Principales — dépenses de l'État** (situation mensuelle budgétaire, séries longues, data.economie.gouv.fr) : dépenses par titre (personnel, fonctionnement, investissement, intervention, charge de la dette) et par grande mission.
- **Contrôles** : recettes, solde d'exécution, valeur passée de la cible, taux directeurs BCE (MRO, facilité de dépôt), taux Bund, VIX (aversion au risque), inflation France (IPCH).

## Règles de construction des données
- Les montants budgétaires sont **cumulés depuis janvier** : les différencier pour obtenir des flux mensuels.
- Forte saisonnalité : utiliser des **variations sur un an** (glissement annuel).
- **Décalage de publication** : la situation du mois M est publiée environ 5 semaines après. Pour prédire t+1, n'utiliser que le budget de t-1 au plus (décalage d'au moins 2 mois par rapport à la cible). Sinon biais d'anticipation (look-ahead bias).
- Décembre : version provisoire puis définitive (révisions, à mentionner comme limite).
- OAT/Bund FRED = moyennes mensuelles (OCDE). CAC 40 `^FCHI` = indice de prix, hors dividendes.

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
- `results/figures/` : graphiques pour le mémoire.

## Plan du mémoire
Introduction · Ch.1 État de l'art (rédigé) · Ch.2 Données et méthodologie · Ch.3 Résultats · Ch.4 Discussion · Conclusion · Bibliographie · Annexes.
