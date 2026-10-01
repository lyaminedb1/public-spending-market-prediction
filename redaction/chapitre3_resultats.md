# Mémoire — Chapitre 3 : Résultats

Sep 29, 2026 · @elyamine

## Introduction du chapitre

Ce chapitre présente les résultats, sans les interpréter : l'interprétation vient au chapitre 4. Nous décrivons d'abord les données (3.1), puis les performances des modèles principaux (3.2). Nous vérifions ensuite la solidité de ces résultats (3.3) et l'importance des variables (3.4). Les sections 3.5 et 3.6 résument les dix-neuf extensions réalisées ; leur détail est en annexe. La section 3.7 fait le point sur les hypothèses.

Tous les résultats portent sur la période de test de janvier 2020 à juillet 2026 (79 mois), en validation glissante. Un R² hors échantillon positif signifie que le modèle fait mieux que la moyenne historique ; un R² négatif, qu'il fait moins bien.

## 3.1 Statistiques descriptives

Les trois cibles, en variations, sont stationnaires (p-value ADF inférieure à 0,001). Elles sont très dispersées par rapport à leur moyenne, et peu corrélées d'un mois sur l'autre.

**Tableau 3.1 – Statistiques des variables cibles (mars 2014 – juillet 2026, 149 mois)**

| Cible | Moyenne | Écart-type | Minimum | Maximum | Autocorrélation d'ordre 1 |
| --- | --- | --- | --- | --- | --- |
| Variation du spread OAT–Bund (pb) | 0,12 | 5,27 | -18,1 | 20,5 | 0,14 |
| Variation du taux OAT (pb) | 1,24 | 16,99 | -54,0 | 72,0 | 0,23 |
| Rendement du CAC 40 (%) | 0,53 | 4,55 | -17,2 | 20,1 | -0,09 |

*Source : calculs de l'auteur (OCDE via FRED, Yahoo Finance).*

Le niveau du spread varie entre 26,4 points de base (septembre 2016) et 83,6 points de base (janvier 2025). Les plus fortes variations mensuelles du spread sont observées en mars 2020 (+20,5 pb), mai 2017 (-18,1 pb), février 2017 (+16,3 pb), juin 2024 (+15,5 pb) et novembre 2016 (+15,3 pb).

Les corrélations de Spearman entre les dépenses (mois t-2) et les cibles (mois t+1) sont faibles. Pour le spread, seule la ligne investissement atteint le seuil de 5 % (-0,16). Pour la variation de l'OAT, trois lignes le dépassent : personnel (0,23), charge de la dette (0,21) et fonctionnement (0,17). Une fois l'inflation et la variation passée de la cible contrôlées (corrélation partielle ; ces deux variables sont dans M0), elles descendent à 0,15 (personnel), 0,09 (fonctionnement) et 0,10 (charge de la dette), sous le seuil (p de 0,08 à 0,26). Pour le spread, l'investissement passe à -0,15 (p = 0,06). Pour le CAC 40, aucune corrélation n'est significative.

*\[Figure 3.1 – Distribution des trois cibles : `results/figures/fig3_1_distributions_cibles.png`\]*

## 3.2 Modèles principaux

**Aucun modèle ne bat la moyenne historique**, pour aucune des trois cibles. Le meilleur R² hors échantillon est celui de Ridge M0 sur le CAC 40 : -1,3 %. Pour les deux taux, la prévision « variation nulle » fait mieux que la moyenne (+1,7 % et +2,4 %).

**Tableau 3.2 – R² hors échantillon par rapport à la moyenne historique (%), janvier 2020 – juillet 2026**

| Modèle | Jeu de variables | Δ spread | Δ OAT | CAC 40 |
| --- | --- | --- | --- | --- |
| Moyenne historique | — | 0,0 | 0,0 | 0,0 |
| Variation nulle | — | +1,7 | +2,4 | -0,2 |
| Ridge | M0 marchés | -14,9 | -11,3 | -1,3 |
| Ridge | M1 + dépenses | -14,7 | -11,3 | -3,5 |
| Ridge | M2 + budget complet | -27,8 | -9,0 | -1,8 |
| Forêt aléatoire | M0 marchés | -6,8 | -6,9 | -9,6 |
| Forêt aléatoire | M1 + dépenses | -8,4 | -6,9 | -10,8 |
| Forêt aléatoire | M2 + budget complet | -10,5 | -5,9 | -11,2 |
| XGBoost | M0 marchés | -35,4 | -30,2 | -31,7 |
| XGBoost | M1 + dépenses | -30,1 | -30,4 | -27,8 |
| XGBoost | M2 + budget complet | -28,4 | -33,1 | -26,7 |

*Source : calculs de l'auteur (`results/tables/models_metrics.csv`). Graine aléatoire 42 pour la forêt et XGBoost.*

Le taux de bonne direction varie entre 42 % et 59 % selon les modèles. La moyenne historique obtient 53 % (spread), 57 % (OAT) et 61 % (CAC 40).

Le tableau 3.3 donne les tests de Diebold-Mariano (DM) pour les deux questions centrales : les dépenses améliorent-elles la prévision (H1), et le machine learning fait-il mieux que Ridge (H3) ?

**Tableau 3.3 – Tests de Diebold-Mariano (p-values bilatérales)**

| Comparaison | Δ spread | Δ OAT | CAC 40 |
| --- | --- | --- | --- |
| Ridge : M1 contre M0 | 0,97 | 0,99 | 0,37 |
| Forêt aléatoire : M1 contre M0 | 0,58 | 0,99 | 0,77 |
| XGBoost : M1 contre M0 | 0,61 | 0,98 | 0,63 |
| Forêt aléatoire contre Ridge (M1) | 0,35 | 0,41 | 0,18 |
| XGBoost contre Ridge (M1) | 0,22 | 0,06 | **0,03** (XGBoost moins bon) |

*Source : calculs de l'auteur (`results/tables/models_dm_tests.csv`).*

Aucune comparaison M1 contre M0 n'est significative : les p-values vont de 0,37 à 0,99. Entre modèles, la seule différence significative au seuil de 5 % concerne le CAC 40 : XGBoost y fait moins bien que Ridge (p = 0,03). Face à la prévision « variation nulle », les modèles avec dépenses (M1) sont significativement moins bons dans deux cas sur six pour les taux (Ridge et XGBoost sur le spread, p = 0,04 et 0,03) ; les autres écarts ne sont pas significatifs.

Nous avons aussi appliqué la correction de Benjamini et Hochberg aux 18 tests de H1 (M1 et M2 contre M0, trois modèles, trois cibles). La plus petite p-value corrigée vaut 0,81.

*\[Figure 3.2 – RMSE relatif à la moyenne historique : `results/figures/fig3_2_rmse_relatif.png`\]*

## 3.3 Solidité des résultats

Quatre contrôles complètent le tableau 3.2. Ils ont été ajoutés après les premiers résultats, lors d'une vérification du code.

**Graine aléatoire.** La forêt aléatoire et XGBoost dépendent d'un tirage au hasard. Nous les avons réestimés avec 5 graines (forêt) et 10 graines (XGBoost). Le R² de XGBoost varie d'environ 9 points selon la graine (par exemple de -39,8 % à -30,8 % pour le spread, jeu M0), celui de la forêt d'environ 3 points. Avec toutes les graines, le R² reste négatif, et aucun test DM M1 contre M0 n'est significatif (plus petite p-value : 0,13).

**Puissance du test (contrôle positif).** Pour savoir si notre dispositif peut détecter un vrai signal, nous avons ajouté à M0 une variable fictive corrélée à la cible (corrélation ρ), avec Ridge et 10 tirages par valeur de ρ, un seul pour ρ = 1 (tableau 3.4).

**Tableau 3.4 – Contrôle positif : part des tirages où le signal est retrouvé (Ridge, 10 tirages par valeur de ρ, 1 pour ρ = 1)**

| Corrélation ρ du signal fictif | Bat la moyenne historique | Test DM significatif (5 %) avec gain |
| --- | --- | --- |
| 0,1 | 0 % | 0 % |
| 0,2 | 0 à 20 % | 0 à 30 % |
| 0,3 | 20 à 30 % | 0 à 50 % |
| 0,5 | 80 à 100 % | 30 à 80 % |
| 1,0 | 100 % | 100 % |

*Source : calculs de l'auteur (`results/tables/diag_04/positif.csv`). Plages sur les trois cibles.*

Un signal de corrélation 0,3 avec la cible n'est retrouvé que dans une minorité de tirages. Un signal de corrélation 0,5 bat presque toujours la moyenne, mais le test DM ne le détecte pas toujours.

**Contrôle négatif (variables de bruit).** Nous avons remplacé les sept dépenses par sept variables de pur bruit, puis comparé le gain par rapport à M0. Avec Ridge (20 tirages), 90 à 95 % des tirages de bruit font au moins aussi bien que les vraies dépenses. Avec la forêt aléatoire (5 tirages), c'est 80 à 100 %. Avec XGBoost (10 tirages), c'est 50 à 60 %.

**Décalage de publication.** La date de publication des situations budgétaires n'est vérifiée que pour 2023-2026. Nous avons donc relancé les modèles principaux avec un décalage de 1 mois et de 3 mois, au lieu de 2. Aucun R² ne devient positif (meilleur R² : -0,7 % avec 1 mois, -2,7 % avec 3 mois, jeu M1). Aucun test M1 contre M0 n'est significatif après correction (plus petite p-value corrigée : 0,51).

*Source : `results/tables/diag_04/bruit_*.csv`, `graines_*.csv` et `results/tables/robustesse_lag.csv`. Le détail des tirages est en annexe.*

## 3.4 Importance des variables

Dans un XGBoost estimé sur tout l'échantillon (jeu M1), les sept variables de dépenses représentent **31 à 37 %** de l'importance SHAP totale. Parmi les sept dépenses, les dépenses d'intervention arrivent en tête pour le spread et l'OAT, l'investissement pour le CAC 40.

Nous avons aussi remplacé les sept dépenses par sept variables de pur bruit, tirées au hasard (10 tirages). Ces variables obtiennent en moyenne **34 à 38 %** de l'importance SHAP.

**Tableau 3.5 – Part de l'importance SHAP des sept variables ajoutées à M0 (%)**

| Variables ajoutées | Δ spread | Δ OAT | CAC 40 |
| --- | --- | --- | --- |
| Sept dépenses publiques | 32,8 | 36,8 | 30,6 |
| Sept variables de bruit (moyenne de 10 tirages) | 38,1 | 34,2 | 37,1 |
| Sept variables de bruit (minimum – maximum) | 34,3 – 43,5 | 26,5 – 41,6 | 28,6 – 46,8 |

*Source : calculs de l'auteur (`results/tables/models_shap_importance.csv`, `results/tables/diag_04/shap_bruit.csv`).*

Pour l'OAT et le CAC 40, la part des dépenses se situe dans l'intervalle obtenu avec du bruit. Pour le spread, elle est inférieure au plus petit des dix tirages de bruit.

Une seconde mesure, calculée hors échantillon, a été ajoutée après les premiers résultats : l'importance par permutation, calculée avec Ridge et XGBoost sur deux versions de M1, qui servent de repères : l'une avec sept variables de bruit, l'autre avec le signal fictif (ρ = 0,5). On mélange au hasard les valeurs d'un groupe de variables sur la période de test, puis on mesure la hausse de l'erreur. Quand on mélange les sept dépenses dans la version avec bruit, l'erreur n'augmente pas : le RMSE baisse légèrement, de 0,1 % à 2,5 % selon la cible et le modèle. Dans la version avec signal, l'effet des dépenses va de -3,9 % à +0,1 %. Quand on mélange le signal fictif du contrôle positif (ρ = 0,5), le RMSE augmente de 7,6 % à 18,8 %.

*Source : calculs de l'auteur (`results/tables/models_permutation_oos.csv`).*

*\[Figure 3.3 – Importance SHAP des variables : `results/figures/fig3_3_importance_shap.png`\]*

## 3.5 Extensions sur les données françaises

Les extensions E1 à E13 changent un seul élément à la fois : l'horizon, la forme de la cible, les variables, le modèle ou la fenêtre d'entraînement. Elles ont été décrites avant leur exécution (chapitre 2). Le tableau 3.6 donne, pour chaque extension, le meilleur R² hors échantillon obtenu sans les dépenses, puis avec les dépenses. E12, qui découpe la période de test en sous-périodes, n'y figure pas. Le détail par modèle est en annexe B.

**Tableau 3.6 – Meilleur R² hors échantillon sans / avec dépenses, par extension (%)**

| Extension | Δ spread | Δ OAT | CAC 40 |
| --- | --- | --- | --- |
| Modèle principal (h = 1) | -6,8 / -8,4 | -6,9 / -6,9 | -1,3 / -3,5 |
| E1 Horizon 3 mois | +2,3 / -8,6 | -2,7 / -7,6 | -9,1 / -14,7 |
| E1 Horizon 6 mois | -12,1 / -20,6 | -27,5 / -38,0 | -30,3 / -39,5 |
| E1 Horizon 12 mois | -93,9 / -97,3 | -29,8 / -28,2 | +11,8 / -16,5 |
| E2 Hausse / baisse (score de Brier) | -2,4 / +0,5 | +2,5 / +5,8 | -3,7 / -6,8 |
| E3 Volatilité | -4,3 / -7,7 | +3,3 / +4,2 | +9,6 / +6,4 |
| E4 Surprise budgétaire | -6,0 / -11,1 | -7,1 / -7,2 | -1,4 / -0,4 |
| E5 Interactions avec le régime de taux | -14,0 / -29,5 | -12,2 / -19,0 | -4,8 / -13,7 |
| E6 Variables réduites / ACP | -5,3 / -4,7 | -5,7 / -4,6 | -3,6 / -2,6 |
| E7 Prévisions tempérées | -1,5 / -2,8 | 0,0 / +0,1 | -0,6 / -1,6 |
| E8 Combinaison des modèles | -3,5 / -4,3 | -1,8 / -2,0 | -3,9 / -4,2 |
| E9 Elastic Net | -2,7 / -4,9 | -6,7 / -7,6 | -0,3 / -3,8 |
| E10 XGBoost réglé | -4,4 / -6,2 | -4,8 / -5,4 | -6,2 / -3,0 |
| E11 Fenêtre glissante de 60 mois | -6,2 / -8,9 | -8,7 / -10,4 | -4,0 / -7,6 |
| E13 Notations souveraines | -5,7 / -8,6 | -5,2 / -6,8 | 0,0 / -10,8 |

*Source : calculs de l'auteur (`results/tables/ext_synthese.csv`). Test de janvier 2020 à juillet 2026 (E4 : jusqu'à février 2026). E2 : amélioration du score de Brier par rapport à la fréquence historique. Pour E2, E3 et E7, la référence est différente de celle du tableau 3.2.*

Sur 45 cases, le modèle sans dépenses fait mieux que le modèle avec dépenses dans 34 cas. Les cases positives sans dépenses sont : la volatilité (E3) pour l'OAT et le CAC 40, la classification de l'OAT (E2), le spread à 3 mois (+2,3 %) et le CAC 40 à 12 mois (+11,8 %, sur 68 prévisions qui se chevauchent). Avec les dépenses, quatre cases sont positives et meilleures que sans : E2 pour le spread (+0,5 contre -2,4) et pour l'OAT (+5,8 contre +2,5), E3 pour l'OAT (+4,2 contre +3,3) et E7 pour l'OAT (+0,1 contre 0,0). Aucune de ces différences n'est significative (voir ci-dessous).

Pour les actions sectorielles (E19, rendement en excès du CAC 40, horizons 1 et 3 mois), le meilleur R² est de +1,4 % sans dépenses et -0,7 % avec pour le BTP, de 0,0 % et -1,7 % pour la défense. Avec l'indice d'incertitude politique (E20), aucune cible n'a de R² positif, avec ou sans dépenses.

**Correction pour tests multiples.** Au total, 168 comparaisons « avec contre sans dépenses » entrent dans la correction de Benjamini et Hochberg (taux de fausses découvertes de 10 %). Aucune n'est significative après correction ; la plus petite p-value corrigée vaut 0,999. Avant correction, 6 p-values sont inférieures à 0,05, alors que 8,4 sont attendues par le seul hasard. Dans ces 6 cas, le modèle avec dépenses est moins mauvais que le modèle sans, mais son R² reste négatif.

*\[Figure 3.4 – Synthèse des extensions : `results/figures/fig3_5_extensions.png`\]*

## 3.6 Panel européen et marche aléatoire (E15 à E18)

Les extensions E15 à E18 utilisent un panel de cinq pays (France, Italie, Espagne, Portugal, Belgique), avec des finances publiques harmonisées par Eurostat. La cible est le spread de chaque pays face au Bund.

**E15 – panel trimestriel.** Sur 330 prévisions (2010T1 à 2026T2), Ridge obtient +13,9 % sans dépenses et +15,5 % avec dépenses (p = 0,37). Un diagnostic complémentaire, non prévu au départ, donne l'autocorrélation d'ordre 1 de la cible : 0,32 en moyenne trimestrielle, contre 0,07 pour le spread de fin de trimestre. Sur 2010-2014, ajouter les dépenses améliore le R² de Ridge de 4,1 points en moyenne trimestrielle et de 3,4 points en fin de trimestre ; après 2015, il le dégrade de 12,8 et 11,2 points. Ces écarts par sous-période ne sont pas testés. Avec le spread de fin de trimestre, les deux R² deviennent négatifs : -4,1 % sans dépenses et -2,9 % avec.

**E16 – réplication élargie de Bouillot et al. (2025).** Le panel mensuel compte 150 variables, dont 18 de finances publiques, et 874 prévisions. Sur le **niveau** du spread, le R² par rapport à la moyenne atteint 92 à 97 % avec les finances publiques. Mais tous les modèles font moins bien que la marche aléatoire, qui prévoit le spread du mois dernier (tableau 3.7). Sur la **variation** du spread, le R² est négatif pour tous les modèles. Les finances publiques n'améliorent aucune prévision (p de 0,08 à 0,81). Sur la France seule, de janvier 2020 à février 2025, la marche aléatoire a une erreur (RMSE) de 5,1 points de base sur le niveau du spread mensuel moyen.

**Tableau 3.7 – E16 : niveau du spread, comparaison à la marche aléatoire (avec finances publiques)**

| Modèle | R² vs moyenne (%) | Gain vs marche aléatoire (%) | RMSE (pb) |
| --- | --- | --- | --- |
| Marche aléatoire | — | 0 | 18,4 |
| XGBoost | 97,0 | -30,9 | 21,1 |
| Forêt aléatoire | 94,5 | -141,6 | 28,6 |
| Ridge | 92,4 | -232,3 | 33,6 |

*Source : calculs de l'auteur (`results/tables/extensions/E16.csv`). Test à partir de janvier 2012, 5 pays.*

**E17 – panel annuel.** Sur 75 prévisions annuelles, tous les modèles font moins bien que la moyenne (R² de -20 % à -338 %) et que la marche aléatoire. La forêt aléatoire avec dépenses est moins mauvaise que sans (-19,8 % contre -45,4 %, p = 0,04 avant correction).

**E18 – régime de crise (exploratoire).** L'ajout d'interactions entre dépenses et période de tension (spread supérieur à 200 pb) dégrade la prévision pour Ridge (le R² passe de -3,3 % à -19,7 %) et pour XGBoost (de -20,2 % à -26,2 %). La forêt aléatoire passe de -10,4 % à -4,9 % (p = 0,20).

## 3.7 Synthèse : état des hypothèses

**Tableau 3.8 – État des hypothèses**

| Hypothèse | Résultat | Éléments |
| --- | --- | --- |
| H1 : les dépenses améliorent la prévision d'au moins un indicateur | Non validée | DM M1 contre M0 : p de 0,37 à 0,99 (tableau 3.3) ; p corrigée ≥ 0,81 sur les 18 tests de H1 ; 0 comparaison significative sur 168 dans les extensions (3.5) ; même résultat avec un décalage de 1 ou 3 mois (3.3) |
| H2 : l'apport décroît du spread à l'OAT, puis au CAC 40 | Non testable | Aucun apport à classer |
| H3 : forêt aléatoire et XGBoost font mieux que les modèles linéaires | Non validée | Forêt ≈ Ridge (p de 0,18 à 0,41) ; XGBoost moins bon que Ridge sur le CAC 40 (p = 0,03) |
| H4 : charge de la dette et dépenses d'intervention sont les plus prédictives | Non soutenue | Part SHAP des dépenses (31 à 37 %) comparable à celle de variables de bruit (34 à 38 %) (tableau 3.5) ; permuter les dépenses n'augmente pas l'erreur hors échantillon |

*Source : sections 3.2 à 3.5.*
