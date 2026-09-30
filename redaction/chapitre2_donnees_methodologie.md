# Mémoire — Chapitre 2 : Données et méthodologie

Sep 28, 2026 · @elyamine

## Introduction du chapitre

Ce chapitre explique d'où viennent nos données, comment nous les avons transformées et comment nous avons évalué les modèles. Tout le protocole répond à une seule contrainte : ne jamais donner au modèle une information qu'un investisseur n'aurait pas eue au moment de sa décision.

Nous présentons d'abord les sources (2.1), puis la construction du jeu de données mensuel (2.2). Viennent ensuite les variables à prédire (2.3) et les variables explicatives (2.4). La section 2.5 justifie le choix des modèles, et la section 2.6 décrit la façon dont nous les évaluons. Pour finir, la section 2.7 présente les variantes testées pour vérifier la solidité des résultats.

Le code et les données sont publiés sur GitHub. Chaque tableau et chaque figure de ce mémoire peut donc être recalculé à partir des fichiers bruts.

## 2.1 Sources des données

Le sujet impose des données ouvertes. Toutes nos sources sont donc publiques et gratuites. Elles couvrent la période de janvier 2013 à août 2026, en fréquence mensuelle.

| Donnée | Source | Fréquence | Usage |
| --- | --- | --- | --- |
| Situations mensuelles budgétaires de l'État (séries longues) | DGFiP, data.economie.gouv.fr | Mensuelle, cumul depuis janvier | Variables de dépenses, recettes et solde |
| Budget voté (lois de finances initiales) | DGFiP, data.economie.gouv.fr | Annuelle | Surprise budgétaire (extension E4) |
| Taux à 10 ans France (OAT) et Allemagne (Bund) | OCDE, via FRED | Mensuelle (moyenne) | Cibles et contrôles |
| CAC 40 | Yahoo Finance | Quotidienne, ramenée au dernier cours du mois | Cible et contrôle |
| Taux directeurs de la BCE (refinancement, facilité de dépôt) | BCE | À chaque décision, prolongés jusqu'à la suivante | Contrôles |
| VIX (volatilité implicite) | FRED | Quotidienne, moyenne mensuelle | Contrôle : aversion au risque |
| Indice des prix harmonisé France | Eurostat, via FRED | Mensuelle | Contrôle : inflation sur un an |
| Notations souveraines de la France | Communiqués des agences (Fitch, Moody's, S&P) | À chaque décision | Contrôle (extension E13) |

La situation mensuelle budgétaire (SMB) décrit l'exécution du budget de l'État, et seulement de l'État : la Sécurité sociale et les collectivités locales n'y figurent pas. On y trouve les dépenses du budget général par titre (personnel, fonctionnement, charge de la dette, investissement, intervention, opérations financières), les prélèvements sur recettes, les principales recettes et le solde. En revanche, ces fichiers ne donnent pas le détail par mission : il est impossible, par exemple, d'isoler les dépenses de défense.

Quatre caractéristiques de ces données comptent pour la suite :

- **Les taux de l'OCDE sont des moyennes mensuelles**, pas des valeurs de fin de mois. Or la variation d'une moyenne à la suivante est un peu corrélée d'un mois sur l'autre, par simple construction. Le CAC 40, lui, est pris au dernier jour du mois.
- **Le CAC 40 est un indice de prix**, qui ne compte pas les dividendes.
- **Les séries budgétaires sont la dernière version publiée.** Les chiffres de décembre, par exemple, sont d'abord provisoires puis révisés. Nous utilisons donc des valeurs un peu différentes de celles que le marché voyait en temps réel.
- **Le budget voté pour 2026 n'est pas dans les fichiers ouverts.** L'extension qui l'utilise (E4) s'arrête donc en février 2026.

## 2.2 Construction du jeu de données

Le jeu de données final compte **150 mois, de mars 2014 à août 2026**, dont 149 avec une cible (le dernier mois n'a pas encore de « mois suivant »). Une ligne correspond à la fin d'un mois t. Elle ne contient que ce qui était connu à cette date : c'est la règle qui guide toutes les étapes ci-dessous.

### 2.2.1 Des cumuls aux flux mensuels

La DGFiP publie des montants **cumulés depuis le 1er janvier** : le chiffre de mars additionne janvier, février et mars. Pour retrouver ce qui a été dépensé dans le mois, nous soustrayons le cumul du mois précédent. En janvier, le flux est simplement le cumul, puisque le compteur repart de zéro.

### 2.2.2 Neutraliser la saisonnalité

L'État ne dépense pas au même rythme toute l'année. L'impôt sur les sociétés arrive à quelques échéances précises, et certaines dépenses se concentrent en fin d'année. Comparer un mois au mois précédent n'aurait donc pas de sens. Nous avons calculé deux transformations pour chaque ligne budgétaire :

- **La somme des 12 derniers mois** (en milliards d'euros). Elle donne le niveau annuel, sans effet de saison.
- **L'écart du cumul depuis janvier par rapport au même mois de l'année précédente, rapporté au total annuel** (en %). Une valeur de +1,2 en mai veut dire que, fin mai, l'État a dépensé l'équivalent de 1,2 % d'une année de plus que fin mai de l'année précédente. Comme on compare toujours le même mois, la saison s'annule.

Nous n'avons pas utilisé un simple taux de croissance du cumul. En janvier, le cumul est presque nul, et le taux prend des valeurs absurdes : de -902 % à +1 789 % pour l'impôt sur les sociétés. Diviser par le total annuel règle ce problème.

Cette mesure a tout de même une limite. En janvier, elle compare un seul mois de dépenses ; en décembre, une année entière. Ses variations sont donc beaucoup plus fortes en fin d'année : pour les dépenses totales, l'écart-type passe de 0,7 en janvier à 4,4 en décembre. Une même valeur n'a donc pas tout à fait le même sens selon le mois.

Nous avons exclu les opérations financières. Ce sont des prises de participation ou des soutiens exceptionnels, très irréguliers, et non une dépense économique courante. Leur écart annuel atteignait -462 %.

### 2.2.3 Respecter le calendrier de publication

La SMB d'un mois M paraît au début du mois M+2. Nous l'avons vérifié sur plusieurs communiqués du ministère : janvier 2023 publié le 2 mars 2023, décembre 2024 le 4 février 2025, juin 2026 le 4 août 2026, juillet 2026 le 2 septembre 2026. À la fin d'un mois t, un investisseur ne connaît donc que le budget du mois t-2. **Toutes les variables budgétaires sont décalées de deux mois.** Pour les années 2014 à 2022, nous n'avons pas retrouvé les dates exactes, car les archives ne sont plus en ligne : nous supposons le même calendrier.

Le même raisonnement vaut pour l'inflation. L'INSEE publie une estimation provisoire à la fin du mois, puis l'indice définitif vers le milieu du mois suivant (pour août 2026 : le 28 août, puis le 15 septembre). Nos données sont les valeurs définitives. **L'inflation est donc décalée d'un mois.**

Sans ces décalages, le modèle utiliserait des chiffres que personne ne connaissait encore au moment de la prévision. Ses performances seraient alors gonflées artificiellement. C'est le biais d'anticipation, bien connu pour les données macroéconomiques (Croushore, 2011).

### 2.2.4 Vérification de la qualité des données

Premier contrôle : à partir des fichiers mensuels, nous avons recalculé le solde de chaque année. Il correspond aux chiffres officiels, à 0,1 milliard près :

| Année | Solde reconstitué (Md€) |
| --- | --- |
| 2014 | -85,6 |
| 2020 | -178,1 |
| 2023 | -173,0 |
| 2024 | -155,9 |

Second contrôle : un script de vérification (`tests/verifications.py`, 31 contrôles) s'assure automatiquement que chaque cible correspond bien au mois suivant, que chaque variable budgétaire vient du mois t-2, que l'inflation vient du mois t-1, et qu'aucun mois ne manque. Pour nous assurer que ce script détecte vraiment les erreurs, nous l'avons lancé sur une version du code où les décalages avaient été retirés : il les signale tous. Le jeu de données n'a aucune valeur manquante, sauf la cible du dernier mois.

## 2.3 Variables cibles et stationnarité

Nous cherchons à prévoir trois indicateurs **pour le mois suivant (t+1)**. Nous les avons choisis avant d'explorer les données. Si nous avions retenu les cibles les plus corrélées aux dépenses, nous aurions trouvé un lien par construction, même sans lien réel.

| Cible | Définition | Unité | Moyenne | Écart-type |
| --- | --- | --- | --- | --- |
| Variation du spread OAT–Bund (cible principale) | Spread(t+1) − spread(t), où spread = OAT 10 ans − Bund 10 ans | points de base | 0,12 | 5,27 |
| Variation du taux OAT 10 ans | OAT(t+1) − OAT(t) | points de base | 1,24 | 16,99 |
| Rendement du CAC 40 | CAC(t+1) / CAC(t) − 1 | % | 0,53 | 4,55 |

Le spread est notre cible principale. En retirant le taux allemand, on enlève ce qui bouge pour toute la zone euro, par exemple une décision de la BCE. Il reste le risque propre à la France, qui est celui que les finances publiques devraient influencer. Le taux OAT et le CAC 40 servent de points de comparaison : a priori, ils dépendent moins directement du budget de l'État.

### Pourquoi prédire des variations plutôt que des niveaux

Le test de Dickey-Fuller augmenté (ADF) confirme que les trois cibles, en variations, sont stationnaires, alors que les niveaux ne le sont pas :

| Série | p-value ADF | Stationnaire |
| --- | --- | --- |
| Variation du spread, variation de l'OAT, rendement du CAC 40 | < 0,001 | oui |
| Niveau du spread | 0,31 | non |
| Niveau de l'OAT | 0,94 | non |

Pourquoi ne pas prédire directement le niveau du spread ? Parce que le spread d'un mois ressemble beaucoup à celui du mois précédent. Un modèle qui recopie la dernière valeur obtient donc un R² très élevé, sans rien avoir appris. En prédisant la variation, on oblige le modèle à anticiper ce qui change vraiment. Nous verrons au chapitre 3 que ce piège n'est pas théorique : dans le panel européen (extension E16), nos modèles atteignent plus de 90 % de R² sur le niveau du spread, tout en faisant moins bien que la simple recopie du mois précédent.

Nous testons aussi une version plus simple dans les extensions : deviner seulement si le spread va monter ou baisser. Sur notre échantillon, il a monté dans 52 % des mois.

## 2.4 Variables explicatives

Nous n'avons pas choisi les variables une par une selon leurs corrélations. Nous avons construit trois jeux emboités, chacun contenant le précédent. Le test central du mémoire compare M0 et M1 : la seule différence entre les deux, ce sont les dépenses. Si M1 prévoit mieux, l'amélioration vient donc des dépenses, **en plus** de ce que les marchés savent déjà.

| Jeu | Contenu | Nombre de variables |
| --- | --- | --- |
| **M0 « marchés »** | Variation du spread (t et t-1), niveau du spread, variation de l'OAT (t et t-1), rendement du CAC 40 (t et t-1), VIX et sa variation, inflation sur un an (du mois précédent), taux de la facilité de dépôt de la BCE | 11 |
| **M1 « + dépenses »** | M0 + écart annuel des dépenses totales, de personnel, de fonctionnement, de charge de la dette, d'investissement, d'intervention et des prélèvements sur recettes (décalés de 2 mois) | 18 |
| **M2 « + budget complet »** | M1 + recettes totales, recettes fiscales et variation du solde sur un an | 21 |

Les recettes et le solde sont à part, dans M2. Le titre du mémoire parle des **dépenses** : M1 répond à cette question précise, et M2 vérifie simplement si le reste du budget change la conclusion.

### Deux pièges mis en évidence par l'analyse exploratoire

**Premier piège : les variables en niveau.** Les dépenses sur 12 mois, en milliards d'euros, montent presque sans arrêt, avec l'inflation et la dette. Depuis 2022, les taux montent aussi. Or deux séries qui montent en même temps sont corrélées, même si elles n'ont rien à voir : la corrélation entre ces niveaux et la variation de l'OAT atteint 0,34, sans aucun sens économique. Ces niveaux ne sont pas stationnaires (p-value ADF supérieure à 0,7). **Nos modèles utilisent donc les écarts annuels, pas les niveaux.** Ces écarts sont beaucoup plus proches de la stationnarité (p-values ADF entre 0,01 et 0,06).

**Second piège : l'inflation.** À première vue, les dépenses de personnel, de fonctionnement et la charge de la dette annoncent la variation de l'OAT (corrélations de Spearman de 0,17 à 0,23). Mais en 2022-2023, l'inflation a fait monter les deux en même temps : les taux, à cause de la BCE, et ces dépenses, à cause des salaires et de la dette indexée. Quand on retire l'effet de l'inflation et de la variation passée de l'OAT (les deux sont dans M0), ces corrélations tombent entre 0,09 et 0,15, sous le seuil de significativité (0,16). **Nous avons donc mis l'inflation dans M0**, pour ne pas attribuer aux dépenses un effet qui vient en réalité de l'inflation.

## 2.5 Modèles retenus

Nous traitons le problème comme une **régression** : le modèle prédit un nombre, qui donne à la fois le sens et l'ampleur du mouvement. C'est aussi le choix des travaux de référence (Gu, Kelly et Xiu, 2020 ; Bouillot, Candelon et Kool, 2025). Nous comparons cinq approches, des plus simples aux plus flexibles :

| Modèle | Rôle | Justification |
| --- | --- | --- |
| Moyenne historique | Référence minimale | Un modèle qui ne la bat pas n'a pas de pouvoir prédictif (Welch et Goyal, 2008 ; Campbell et Thompson, 2008) |
| Marche aléatoire (variation nulle) | Seconde référence | Prédit que le taux ou l'indice ne bougera pas ; référence classique pour les séries financières |
| Ridge (régression linéaire régularisée) | Approche économétrique | Représente la tradition linéaire ; la régularisation limite le surapprentissage avec 18 variables |
| Forêt aléatoire | Machine learning robuste | Capte les effets non linéaires, stable sur de petits échantillons (Breiman, 2001 ; Medeiros et al., 2021) |
| XGBoost | Machine learning de référence | Meilleur modèle chez Bouillot et al. (2025) pour les spreads européens (Chen et Guestrin, 2016) |

**Nous n'utilisons pas de deep learning.** Avec environ 150 mois de données, un réseau de neurones apprendrait surtout le bruit. Les études qui l'emploient avec succès, comme Fischer et Krauss (2018), travaillent sur des données quotidiennes de centaines d'actions, soit des centaines de milliers d'observations.

### Hyperparamètres

Nous n'avons pas cherché les meilleurs hyperparamètres sur la période de test. Quand on essaie beaucoup de réglages, on finit toujours par en trouver un qui « marche », mais par hasard. Nous avons donc retenu des valeurs usuelles :

- **Ridge** : paramètre de régularisation choisi automatiquement sur les données d'entraînement, parmi 40 valeurs entre 0,01 et 1 000 000. La grille initiale s'arrêtait à 1 000 ; lors de la revue du code, nous avons constaté que cette borne était atteinte la plupart des mois pour le CAC 40, et nous l'avons élargie (le R² de Ridge change d'au plus 1,2 point).
- **Forêt aléatoire** : 300 arbres, profondeur maximale 4, au moins 5 observations par feuille, 50 % des variables tirées à chaque division.
- **XGBoost** : 200 arbres, profondeur maximale 2, taux d'apprentissage 0,05, sous-échantillonnage de 80 % des observations et des variables.

Ces valeurs sont prudentes : des arbres peu profonds apprennent moins le bruit d'un petit échantillon. Nous devons toutefois être transparents sur un point. Contrairement aux extensions (section 2.7), ces réglages n'ont pas été datés dans le dépôt avant les premiers résultats : le code et les résultats ont été enregistrés ensemble. Pour vérifier que ce choix ne change pas les conclusions, nous l'avons remis en cause de deux façons : l'extension E10 règle XGBoost automatiquement par validation croisée temporelle, et un contrôle relance la forêt aléatoire et XGBoost avec plusieurs graines aléatoires (annexe).

## 2.6 Protocole d'évaluation

Nous évaluons les modèles comme s'ils avaient été utilisés en vrai, mois après mois : chaque prévision n'utilise que les données disponibles au moment où elle est faite.

### 2.6.1 Validation glissante

Une validation croisée classique tire les mois au hasard. Le modèle pourrait alors apprendre sur 2024 pour prévoir 2021, ce qui n'a aucun sens pour une prévision. Nous utilisons donc une **validation glissante à fenêtre croissante** :

1. Le modèle est entraîné sur mars 2014 – décembre 2019 (70 mois) et prédit janvier 2020.
2. Il est réentraîné en ajoutant janvier 2020, puis prédit février 2020.
3. L'opération est répétée chaque mois jusqu'à juillet 2026.

La période de test compte **79 mois**, de janvier 2020 à juillet 2026. Elle traverse des contextes très différents : le Covid-19, la hausse des taux de la BCE à partir de 2022, puis les tensions politiques et budgétaires françaises de 2024 à 2026.

### 2.6.2 Mesures de performance

| Mesure | Ce qu'elle mesure |
| --- | --- |
| RMSE (racine de l'erreur quadratique moyenne) | L'erreur typique, dans l'unité de la cible ; pénalise les grosses erreurs |
| MAE (erreur absolue moyenne) | L'erreur moyenne, moins sensible aux mois extrêmes |
| R² hors échantillon | Le gain par rapport à la moyenne historique : positif si le modèle fait mieux, négatif sinon (Campbell et Thompson, 2008) |
| Taux de bonne direction | La part des mois où le sens du mouvement est correctement anticipé |

Notre mesure principale est le R² hors échantillon. Il compare les erreurs du modèle à celles de la moyenne historique :

```latex
R^2_{OOS} = 1 - \frac{\sum_{t} (y_t - \hat{y}_t)^2}{\sum_{t} (y_t - \bar{y}_t)^2}
```

où y\_t est la valeur observée, ŷ\_t la prévision du modèle et ȳ\_t la moyenne historique, calculée uniquement avec les mois antérieurs à t. Un R² positif veut dire que le modèle fait mieux que la moyenne ; un R² négatif, qu'il fait moins bien. Pour les taux, nous regardons aussi une seconde référence, la variation nulle, qui s'avère plus difficile à battre que la moyenne (chapitre 3).

### 2.6.3 Tests statistiques

Un modèle peut faire un peu mieux qu'un autre par pur hasard. Pour le savoir, nous utilisons le **test de Diebold et Mariano (1995)**, avec la correction de Harvey, Leybourne et Newbold (1997) pour les petits échantillons. Il nous dit si l'écart d'erreurs entre deux modèles est assez grand pour ne pas être dû au hasard. Nous l'appliquons à trois comparaisons :

- M1 contre M0 pour chaque modèle (test de l'hypothèse H1) ;
- chaque modèle contre la moyenne historique ;
- forêt aléatoire et XGBoost contre Ridge (hypothèse H3).

### 2.6.4 Importance des variables

Pour savoir quelles dépenses le modèle utilise le plus (hypothèse H4), nous calculons les **valeurs SHAP** de XGBoost (Lundberg et Lee, 2017). Elles indiquent combien chaque variable pèse, en moyenne, dans les prédictions. Deux précautions s'imposent. D'abord, elles sont calculées sur tout l'échantillon : elles décrivent ce que le modèle utilise, pas ce qui améliore la prévision. Ensuite, une part d'importance ne veut rien dire sans point de comparaison. Nous la comparons donc à la part obtenue par sept variables de pur bruit, tirées au hasard, placées au même endroit que les dépenses.

## 2.7 Extensions pré-enregistrées et correction des tests multiples

Un résultat pourrait dépendre d'un choix particulier : l'horizon, le modèle, la période. Pour le vérifier, nous avons décliné le protocole principal en vingt extensions. **Avant de lancer chaque extension, nous avons daté sa liste et son protocole dans le dépôt GitHub**, et nous rapportons tous les résultats, favorables ou non.

Cette précaution répond à un risque bien décrit par Bailey et al. (2014) : à force d'essayer des configurations, on finit toujours par en trouver une qui semble marcher, par hasard.

Le pré-enregistrement s'est fait en plusieurs étapes, et nous préférons le dire clairement. E1 à E13 ont été fixées ensemble le 26 septembre 2026, après les résultats du modèle principal mais avant toute extension. E14 à E16 ont été ajoutées avant leur collecte de données. E17 à E20, en revanche, ont été ajoutées le 27 septembre **après** avoir vu les résultats d'E15 et E16, mais avant leurs propres données. E18 est donc présentée comme exploratoire, car son idée vient directement d'un résultat d'E15.

| # | Extension | Justification |
| --- | --- | --- |
| E1 | Horizons de 3, 6 et 12 mois | Les dépenses agissent lentement sur la dette |
| E2 | Classification hausse ou baisse | Deviner le sens est plus facile que l'ampleur |
| E3 | Volatilité (ampleur du mouvement) | L'incertitude budgétaire peut agiter les marchés |
| E4 | Surprise budgétaire : exécution par rapport au budget voté | Le marché réagit à l'information nouvelle (Ramey, 2011) |
| E5 | Effet selon le régime de taux | La sensibilité aux finances publiques varie dans le temps (Afonso et al., 2015) |
| E6 | Moins de variables, composantes principales | Réduire le surapprentissage |
| E7 | Prévisions tempérées vers la moyenne | Campbell et Thompson (2008) |
| E8 | Combinaison de prévisions | Robustesse des moyennes de modèles |
| E9 | Elastic Net | Sélection automatique des variables |
| E10 | XGBoost réglé par validation croisée temporelle emboitée | Vérifier que le choix des hyperparamètres n'est pas en cause |
| E11 | Fenêtre glissante de 60 mois | S'adapter au changement de régime de 2022 |
| E12 | Évaluation par période (2020-2021, 2022-2026, marchés calmes ou agités) | Un apport peut être limité aux périodes de tension |
| E13 | Notations souveraines de la France | Contrôle du risque perçu par les agences |
| E14 | Étude d'événement autour des dates de publication (non réalisée : taux quotidiens introuvables) | Le marché intègre-t-il l'information budgétaire le jour même ? |
| E15 | Panel européen trimestriel (5 pays, Eurostat) | Plus d'observations, inclusion de la crise de la dette 2010-2012 |
| E16 | Panel européen mensuel avec une base large de variables | Répliquer le cadre de Bouillot et al. (2025) en le comparant à la marche aléatoire |
| E17 | Panel annuel (valeurs de décembre) | Les finances publiques agiraient à basse fréquence |
| E18 | Régime de crise (exploratoire) | Les marchés ne regarderaient le budget qu'en période de tension |
| E19 | Actions des secteurs liés à la dépense publique (BTP, défense) | Canal des revenus des entreprises |
| E20 | Incertitude de politique économique (indice européen de Baker, Bloom et Davis) | Contrôler l'incertitude politique ; l'indice français n'étant pas disponible, nous avons déclaré ce changement avant l'exécution |

Pour les horizons de plus d'un mois (E1), une difficulté apparaît : à la date de la prévision, les dernières cibles ne sont pas encore connues. Le modèle n'est donc entraîné que sur des cibles déjà observées, et le test de Diebold-Mariano tient compte du chevauchement des périodes.

### Correction des tests multiples

Avec plus de 150 comparaisons, environ une sur vingt paraîtrait significative au seuil de 5 %, par pur hasard. Nous corrigeons donc toutes les p-values « avec dépenses contre sans dépenses » par la **procédure de Benjamini et Hochberg (1995)**, avec un taux de fausses découvertes de 10 %. Nous ne considérons comme significatifs que les résultats qui résistent à cette correction.

## 2.8 Considérations éthiques

**Données.** Toutes les données utilisées sont publiques et en accès libre : situations budgétaires de l'État (data.economie.gouv.fr), séries de marché et macroéconomiques (FRED, BCE, Eurostat), indices boursiers. Elles ne contiennent aucune donnée personnelle. Les sources sont citées, et la liste des fichiers bruts est figée dans le dépôt (manifeste des données).

**Transparence et résultats négatifs.** Le code, les données traitées et les résultats sont disponibles dans un dépôt GitHub, et l'ensemble peut être relancé avec un seul script. Le plan des extensions a été daté avant leur exécution. Nous rapportons tous les résultats, y compris négatifs, et corrigeons pour les tests multiples. Ne publier que les résultats favorables donnerait une image fausse de ce que les données permettent ; c'est un problème connu en finance empirique (Bailey et al., 2014).

**Usage des résultats.** Ce travail n'est pas un conseil en investissement. Un modèle qui paraît prédire les marchés peut conduire à des décisions coûteuses s'il est mal évalué ; c'est pourquoi nous insistons sur la comparaison à des références simples.

**Outils d'intelligence artificielle.** Des outils d'IA générative ont été utilisés pour l'aide à la programmation, la relecture du code et l'aide à la rédaction. Leur usage est décrit dans la déclaration prévue par le guide de l'ECE. Les choix de recherche, la validation des résultats et les interprétations relèvent de l'auteur.

## Références ajoutées par ce chapitre

À intégrer à la bibliographie générale (les autres références citées figurent déjà au chapitre 1).

- Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A practical and powerful approach to multiple testing. *Journal of the Royal Statistical Society: Series B*, 57(1), 289–300.
- Dickey, D. A., & Fuller, W. A. (1979). Distribution of the estimators for autoregressive time series with a unit root. *Journal of the American Statistical Association*, 74(366), 427–431.
- Harvey, D., Leybourne, S., & Newbold, P. (1997). Testing the equality of prediction mean squared errors. *International Journal of Forecasting*, 13(2), 281–291.
- Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems*, 30.

## Sources en ligne

- [Situations mensuelles budgétaires de l'État, séries longues](https://data.economie.gouv.fr/explore/assets/situations-mensuelles-budgetaires-series-longues/), data.economie.gouv.fr.
- [La situation mensuelle de l'État](https://www.economie.gouv.fr/dgfip/la-situation-mensuelle-de-letat), DGFiP (dates de publication).
- [Dépôt du projet](https://github.com/lyaminedb1/public-spending-market-prediction), GitHub (code, données, plan pré-enregistré `docs/plan_extensions.md`).
