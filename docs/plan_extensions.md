# Plan pré-enregistré des extensions (section 3.6 du mémoire)

**Date de rédaction : 26 septembre 2026, avant l'exécution de tout test d'extension.**
Ce fichier est commité avant les résultats : la liste ci-dessous est fixée et **tous** les résultats
seront rapportés, favorables ou non.

## Contexte
Les modèles principaux (`src/04_models.py`) ne battent pas la moyenne historique à l'horizon d'un mois,
et l'ajout des dépenses publiques (M1) n'améliore pas la prévision par rapport aux seules variables de
marché (M0). Les extensions ci-dessous testent si ce résultat tient sous d'autres formulations,
justifiées par la littérature ou par le diagnostic (surapprentissage, changement de régime).

## Protocole commun (inchangé)
- Période de test : 2020-01 → 2026-07, réestimation mensuelle, aucune donnée future dans l'entraînement.
- Budget toujours décalé de 2 mois (délai de publication).
- Question évaluée dans chaque extension : **la version avec dépenses bat-elle la version sans dépenses ?**
  et **bat-elle la moyenne historique ?**
- Critère : R² hors échantillon, test de Diebold-Mariano (perte quadratique ; Brier pour la classification).
- **Tests multiples** : les p-values « avec dépenses vs sans » de toutes les extensions sont corrigées
  par la procédure de Benjamini-Hochberg (taux de fausses découvertes 10 %). Seuls les résultats qui
  survivent à la correction seront présentés comme significatifs.

## Liste des extensions

| # | Extension | Justification |
|---|---|---|
| E1 | Horizons 3, 6 et 12 mois (variation cumulée) | Les dépenses agissent lentement sur la dette. Entraînement limité aux cibles déjà observées ; DM avec correction de Newey-West (h-1 retards). |
| E2 | Classification hausse/baisse (logistique, forêt, XGBoost) | Deviner le sens est plus facile que l'ampleur. Référence : classe majoritaire. Critères : taux de bonne classification, AUC, score de Brier. |
| E3 | Volatilité : cible = valeur absolue de la variation du mois suivant | La volatilité est persistante ; l'incertitude budgétaire peut agiter les marchés. |
| E4 | Surprise budgétaire : taux d'exécution des dépenses par rapport au budget voté (LFI), comparé au même mois de l'année précédente | Les marchés intègrent les annonces (Ramey, 2011) ; l'information nouvelle est l'écart à ce qui a été voté. |
| E5 | Effet selon le régime de taux : interactions dépenses × période de taux positifs (facilité de dépôt BCE > 0) | Afonso, Arghyrou et Kontonikas (2015) : la sensibilité des spreads aux finances publiques varie dans le temps. |
| E6 | Moins de variables : (a) jeu réduit, (b) 2 composantes principales des dépenses (ACP estimée sur l'entraînement uniquement) | Réduire le surapprentissage (environ 70 à 150 mois d'entraînement). |
| E7 | Prévisions tempérées : moyenne 50/50 entre la prévision du modèle et la moyenne historique (poids fixé a priori) | Campbell et Thompson (2008). |
| E8 | Combinaison de prévisions : moyenne de Ridge, forêt aléatoire et XGBoost | Robustesse classique des combinaisons en prévision. |
| E9 | Elastic Net avec validation croisée temporelle interne | Sélection automatique des variables. |
| E10 | XGBoost avec réglage des hyperparamètres par validation croisée temporelle emboîtée (réglage refait tous les 12 mois, sur l'entraînement uniquement) | Le XGBoost de base est peut-être trop complexe. |
| E11 | Fenêtre glissante de 60 mois au lieu d'une fenêtre croissante | S'adapter au changement de régime de 2022. |
| E12 | Évaluation par période : 2020-2021 (taux bas, Covid) contre 2022-2026 (hausse des taux, tensions politiques) ; mois calmes contre agités (VIX > 20) | Un apport éventuel peut être limité aux périodes de tension. |
| E13 | Notations souveraines de la France (Fitch, Moody's, S&P) comme variable de contrôle pour le spread | Les dégradations de notation font bouger le spread ; à tester dans M0 et M1. |

## Ce qui ne sera pas fait (hors délai ou hors sujet), à citer en perspectives
- Données de la commande publique (DECP) : nettoyage trop long.
- Panel de plusieurs pays (comme Bouillot et al., 2025) : données budgétaires mensuelles hétérogènes.
- Sentiment des actualités, Google Trends : hors du périmètre « dépenses publiques » du titre.
