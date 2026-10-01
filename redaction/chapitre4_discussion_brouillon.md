# Mémoire — Chapitre 4 : Discussion

Oct 1, 2026 · @elyamine

> **Statut : version rédigée le 1/10 avec l'aide de Claude, à partir des idées discutées avec Elyamine, pour tenir la date de remise. À relire et reformuler par l'auteur si le temps le permet (règle ECE sur l'IA). Chiffres et références vérifiés dans le dépôt et les sources.**

## 4.1 Réponse à la problématique

Notre question était la suivante : peut-on prédire des indicateurs des marchés financiers à partir des données ouvertes de dépenses publiques, en utilisant le machine learning ?

Sur les données françaises, à un horizon d'un mois, la réponse est négative. Nous ne trouvons **aucune preuve** que les dépenses de l'État améliorent la prévision du spread OAT–Bund, du taux OAT ou du CAC 40. Ce résultat tient pour les trois modèles, avec un décalage de publication d'un à trois mois, et dans les dix-neuf extensions après correction pour les tests multiples.

Cette réponse a une portée précise. Elle ne dit pas que les dépenses n'ont aucun lien avec les marchés : avec 79 mois de test, un lien faible ou modéré pourrait nous échapper (section 4.3). Elle porte sur l'exécution mensuelle du budget de l'État, et non sur les annonces budgétaires ni sur l'ensemble des administrations publiques. Nous écrivons donc « pas de preuve » plutôt que « les dépenses ne permettent pas de prédire » : la première formulation décrit ce que nos tests montrent, la seconde affirmerait une impossibilité que nos données ne peuvent pas démontrer.

Un second constat dépasse la question des dépenses : **aucun modèle ne bat la moyenne historique**, même sans les dépenses. Pour les taux, la prévision « pas de variation le mois prochain » fait mieux que la moyenne et que tous nos modèles, même si l'écart n'est significatif que dans quelques cas. À un mois, ces marchés sont très difficiles à prévoir avec les variables utilisées.

## 4.2 Pourquoi les dépenses n'aident pas : trois explications possibles

Nous proposons trois explications, qui ne s'excluent pas. Ce sont des hypothèses : aucune n'est démontrée par nos tests.

### L'information est peut-être déjà connue

Le budget de l'État est voté en décembre, dans la loi de finances de l'année suivante. Les marchés peuvent donc tenir compte du plan de dépenses avant le début de l'année, et la situation mensuelle, publiée deux mois plus tard, confirmerait surtout ce qui était attendu. Or un prix réagit à l'information nouvelle, pas à ce qui est déjà prévu (Fama, 1970). Ramey (2011) montre que, pour les dépenses publiques, ce qui compte est le moment de l'annonce plutôt que celui de la dépense. Attinasi et al. (2009) trouvent la même chose pendant la crise de 2007-2009 : c'est l'annonce des plans de sauvetage bancaire qui a pesé sur les spreads, non le montant engagé. L'extension E4 va dans ce sens : même l'écart entre l'exécution et le budget voté, qui mesure une forme de surprise, n'améliore pas la prévision.

Pour tester directement cette explication, il faudrait observer le spread le jour même de chaque publication (étude d'événement). Nous n'avons pas pu la réaliser, faute de taux quotidiens accessibles (sections 4.7 et 4.8).

### Ce qui fait bouger le spread n'est pas budgétaire

Les plus fortes variations mensuelles du spread sont observées en mars 2020 (+20,5 pb), en février et mai 2017 (+16,3 et −18,1 pb) et en juin 2024 (+15,5 pb). Ces mois coïncident avec le début de la crise du Covid-19, la campagne présidentielle de 2017 et l'annonce de la dissolution de l'Assemblée nationale le 9 juin 2024. Le cas de juin 2024 concerne bien les finances publiques, mais par un canal politique : la crainte qu'une nouvelle majorité ne tienne pas la trajectoire budgétaire. C'est une anticipation, qui n'apparaît dans aucune ligne de dépense déjà exécutée.

### Une variable lente et tardive pour une cible rapide

Les dépenses de l'État reflètent des décisions budgétaires prises à l'avance et évoluent plus lentement que les marchés, qui réagissent en quelques jours. Nous cherchons donc à prévoir un mouvement rapide avec une information lente, disponible avec deux mois de retard.

La littérature européenne trouve pourtant un lien entre finances publiques et spreads (Bernoth et al., 2012 ; Afonso et al., 2015). Il n'y a pas de contradiction : ces études **expliquent le niveau** des spreads, en panel et souvent en période de crise, alors que nous cherchons à **prévoir leur variation** le mois suivant, hors échantillon. Par ailleurs, la France n'a pas connu de crise de la dette sur notre période, contrairement à l'Italie ou à l'Espagne en 2011-2012, et Afonso et al. (2015) montrent que les marchés sanctionnent surtout les finances publiques en période de tension. Le panel trimestriel va dans ce sens : sur 2010-2014, ajouter les dépenses améliore le R² de Ridge de 4 points, alors qu'il le dégrade de près de 13 points après 2015 (section 3.6). Mais ces écarts ne sont pas testés, et le modèle qui introduit explicitement des interactions avec les périodes de tension (E18) ne les confirme pas.

## 4.3 Ce que le résultat négatif veut dire, et ce qu'il ne veut pas dire

Un résultat négatif n'a de valeur que si l'on sait ce que le test aurait pu détecter. Trois contrôles permettent d'en juger.

### La puissance du test

Le contrôle positif (section 3.3) ajoute à M0 une variable fictive corrélée à la cible. Avec une corrélation de 0,5, le modèle bat la moyenne historique dans 80 à 100 % des tirages ; avec 0,3, dans 20 à 30 % seulement. Notre dispositif repère donc un signal fort, mais manquerait souvent un signal modéré. Nos tests excluent un fort pouvoir prédictif des dépenses, pas un effet faible. La cause principale est la taille de l'échantillon : les séries budgétaires ouvertes commencent en 2013, ce qui laisse 79 mois de test, et le choix de commencer le test en 2020 pour garder assez de mois d'entraînement y contribue.

### Le contrôle négatif

Quand on remplace les sept dépenses par sept variables tirées au hasard, 90 à 95 % des tirages de bruit font au moins aussi bien que les vraies dépenses avec Ridge. Les petits écarts entre M1 et M0 ne sont donc pas propres aux dépenses : n'importe quelles variables ajoutées produisent des écarts du même ordre. Le même contrôle change la lecture de l'importance des variables : les dépenses pèsent 31 à 37 % de l'importance SHAP, mais du bruit obtient 34 à 38 %. Une part d'importance élevée dans un modèle d'arbres ne montre donc pas qu'une variable est utile.

### Le choix de la référence

Pour les taux, la prévision « pas de variation » bat la moyenne historique : la moyenne n'est pas la référence la plus exigeante. Le panel trimestriel (E15) montre un autre piège : un R² de +15 % venait du fait que la cible était une moyenne sur le trimestre, en partie prévisible de façon mécanique (Working, 1960) ; avec le spread de fin de trimestre, il devient négatif. Un bon score ne suffit donc pas : il faut le comparer à une référence simple et à du bruit, et vérifier que la cible ne contient pas de régularité mécanique.

## 4.4 Retour sur les modèles

### Les arbres ne font pas mieux que Ridge (H3)

On pouvait attendre du machine learning qu'il trouve des relations non linéaires. C'est l'inverse : XGBoost est le moins bon des trois modèles, et la forêt aléatoire ne fait pas mieux que Ridge. Deux éléments peuvent l'expliquer.

Le premier est le rapport entre signal et bruit. Avec 70 à 148 mois d'entraînement et des cibles très bruitées, un modèle flexible peut s'ajuster à des coïncidences de l'échantillon d'apprentissage qui ne se répètent pas. L'instabilité de XGBoost, dont le R² varie d'environ 9 points selon la seule graine aléatoire, est compatible avec cette idée.

Le second est le comportement de Ridge. Quand il ne trouve pas de signal, il augmente sa pénalité et rapproche sa prévision de la moyenne. Pour le CAC 40, la pénalité dépasse 10 000 dans 27 % (M0) à 44 % (M1) des mois, et Ridge devient presque la moyenne historique : son R² est proche de zéro (−1,3 %). Autrement dit, le « meilleur » modèle est celui qui renonce le plus à prévoir. Le machine learning n'est pas inutile en soi, mais il demande plus d'observations ou un signal plus fort que ce que nos données offrent à un mois.

### L'importance des variables ne dit rien ici (H4)

Les valeurs SHAP semblaient d'abord soutenir H4, avec les dépenses d'intervention en tête parmi les dépenses. Mais des variables de pur bruit obtiennent la même part d'importance, et mélanger les dépenses sur la période de test n'augmente pas l'erreur. Un modèle d'arbres utilise toutes les variables qu'on lui donne, même inutiles : il faut comparer leur importance à celle du bruit avant d'en tirer une conclusion.

### Ce qui reste prévisible

Quelques extensions battent la moyenne, mais **sans les dépenses** : la volatilité (E3 : +9,6 % pour le CAC 40, +3,3 % pour l'OAT), le sens de variation de l'OAT (E2 : score de Brier +2,5 %) et le CAC 40 à 12 mois (E1 : +11,8 %). Ce dernier résultat est fragile : il repose sur 68 prévisions qui se chevauchent. Que la volatilité soit en partie prévisible est cohérent avec un fait bien connu : les périodes agitées se suivent (Engle, 1982). Dans aucun de ces cas les dépenses n'apportent un gain significatif : ce qui est prévisible vient des marchés eux-mêmes.

## 4.5 Comparaison avec la littérature

### Bouillot, Candelon et Kool (2025)

L'étude la plus proche de la nôtre annonce un R² de 0,81 à 0,99 selon les pays (0,86 pour la France) et une erreur de 7,3 points de base pour la France sur 2020-2025. Nos résultats semblent contraires aux leurs, mais ils ne mesurent pas la même chose. Ces auteurs prévoient le **niveau** du spread, et le spread d'un mois est très proche de celui du mois précédent : une simple recopie du dernier spread obtient déjà un R² très élevé face à la moyenne. Leur propre analyse montre que le spread passé domine les prévisions dans tous les pays. Selon le résumé de leur article, d'ailleurs, l'AR(1) et la marche aléatoire ont des erreurs plus faibles que les modèles de machine learning dans chaque pays quand ceux-ci sont réestimés à chaque date, et XGBoost n'est jamais significativement battu par les autres modèles de machine learning.

Nos résultats vont dans le même sens. Dans notre panel européen (E16), nous retrouvons un R² de 92 à 97 % sur le niveau du spread, mais tous nos modèles font moins bien que la marche aléatoire (XGBoost : erreur de 21,1 points de base contre 18,4). Sur la France et la même période qu'eux (janvier 2020 à février 2025), la marche aléatoire a une erreur de 5,1 points de base dans nos données, contre 7,3 pour leur XGBoost ; cette comparaison est à lire avec prudence, car nos séries sont des moyennes mensuelles et leur définition du spread peut différer. Un R² sur le niveau ne suffit donc pas à juger une prévision : la comparaison à la marche aléatoire est indispensable. Autre point commun : chez eux aussi, les finances publiques pèsent très peu (une seule variable de finances publiques parmi les cinq plus importantes de chacun des dix pays, soit 50 au total). Notre apport est d'avoir isolé les dépenses, avec et sans elles dans le même modèle. Sur le machine learning, nous ne retrouvons pas leur résultat : XGBoost est le moins bon de nos modèles (H3).

### Welch et Goyal (2008)

Welch et Goyal montrent que la plupart des variables proposées pour prévoir la bourse américaine ne battent pas la moyenne historique hors échantillon. Nos résultats sur le CAC 40 vont dans le même sens, et la même difficulté apparaît pour le spread et le taux OAT à un mois.

### Les autres études européennes

Afonso et al. (2015) et Bernoth et al. (2012) trouvent un lien entre finances publiques et spreads, mais sur des périodes qui incluent la crise de la dette et pour expliquer le niveau des spreads (section 4.2). Belly et al. (2023) trouvent que le machine learning suit mieux les spreads que les modèles économétriques, sur 2004-2019 ; leur question est la supériorité d'une famille de modèles, la nôtre l'apport d'un bloc de variables. Garlanda-Longueville (2023) trouve, en données quotidiennes, un effet des allocutions du président de la République pendant la crise du Covid sur le CAC 40 et sur le spread. Ce résultat est compatible avec le nôtre : il suggère que ce sont les annonces, observées au jour le jour, qui font bouger les marchés plutôt que l'exécution mensuelle publiée deux mois plus tard.

## 4.6 Implications

**Pour la recherche.** Un résultat de prévision doit être comparé à une référence naïve (la moyenne historique et, pour les taux, la variation nulle) et à du bruit. Sans ces repères, un R² élevé sur un niveau ou une forte part d'importance SHAP peuvent donner une impression de pouvoir prédictif qui n'existe pas. Publier les résultats négatifs, avec des contrôles de puissance, évite que la littérature ne retienne que les configurations qui semblent marcher.

**Pour les investisseurs.** Nos résultats ne donnent pas de raison d'utiliser l'exécution mensuelle du budget de l'État pour prévoir le spread, le taux OAT ou le CAC 40 à un mois. Ils n'indiquent pas que les finances publiques sont sans importance pour les marchés : l'information utile se trouve peut-être plutôt dans les annonces et les anticipations.

**Pour les producteurs de données ouvertes.** Un calendrier de publication archivé et la conservation des versions successives des chiffres permettraient de travailler avec l'information réellement disponible à chaque date.

## 4.7 Limites

- **Données révisées.** Nous utilisons la dernière version publiée des situations budgétaires, et non les chiffres connus à chaque date (les montants de décembre sont d'abord provisoires).
- **Date de publication.** Le décalage de deux mois est vérifié sur 2023-2026 seulement ; pour 2014-2022, c'est une hypothèse. Les résultats ne changent pas avec un décalage d'un ou de trois mois (section 3.3).
- **Périmètre.** Les données couvrent le budget de l'État, pas la Sécurité sociale ni les collectivités, et ne sont pas ventilées par mission.
- **Cibles de taux en moyennes mensuelles.** Le spread et le taux OAT sont des moyennes du mois (OCDE), alors que le CAC 40 est pris en fin de mois ; les variations de moyennes sont légèrement autocorrélées de façon mécanique.
- **Variables budgétaires hétérogènes dans l'année.** L'écart-type de l'écart cumulé est en médiane 6,3 fois plus grand en décembre qu'en janvier.
- **Petit échantillon.** Avec 70 à 148 mois d'entraînement et 79 mois de test, seul un effet fort pouvait être détecté. Les écarts de quelques points de R² entre deux modèles ne sont pas interprétables.
- **Hyperparamètres.** Ils ont été fixés à des valeurs usuelles, sans réglage sur la période de test, mais le code et les résultats des modèles principaux ont été enregistrés ensemble : nous ne pouvons pas prouver qu'ils ont été choisis avant de voir les résultats. Seules les extensions ont un plan daté avant leur exécution. Les chiffres de XGBoost et de la forêt aléatoire dépendent aussi des versions des bibliothèques logicielles ; les conclusions, non.
- **Extensions ajoutées en cours de route.** E17 à E20 ont été ajoutées après avoir vu les résultats d'E15 et E16, et E18 est exploratoire. E14 (étude d'événement) n'a pas pu être réalisée.
- **Panel européen.** Pour E16, 25 des 68 séries de l'OCDE ne sont plus mises à jour depuis fin 2022 ou début 2024 : environ 23 % des valeurs de la fin de la période de test sont complétées. Pour E19, les prix des actions n'incluent pas les dividendes.
- **Pas d'étude d'événement.** L'explication « l'information est déjà connue » (section 4.2) reste donc une hypothèse.

## 4.8 Recherches futures

- **Étude d'événement.** Avec des taux quotidiens et les dates exactes de publication des situations budgétaires, mesurer la réaction du spread le jour même : c'est le test direct de l'explication « l'information est déjà connue ».
- **Les annonces plutôt que l'exécution.** Le projet de loi de finances, les lois de finances rectificatives et les programmes de stabilité sont de l'information nouvelle pour les marchés ; ils pourraient être codés comme des surprises (par exemple l'écart entre le déficit annoncé et les prévisions des économistes).
- **Données en temps réel.** Conserver chaque version publiée des situations budgétaires.
- **Plus d'observations.** Un panel de pays plus long, incluant la crise de 2010-2012, avec des cibles de fin de période plutôt que des moyennes.
- **Ventilation sectorielle.** Les données de la commande publique permettraient de relier la dépense aux entreprises bénéficiaires et de mieux tester le canal des actions sectorielles (E19).

## Références ajoutées par ce chapitre

- Engle, R. F. (1982). Autoregressive conditional heteroscedasticity with estimates of the variance of United Kingdom inflation. *Econometrica*, 50(4), 987–1007. [https://doi.org/10.2307/1912773](https://doi.org/10.2307/1912773)
- Working, H. (1960). Note on the correlation of first differences of averages in a random chain. *Econometrica*, 28(4), 916–918. [https://doi.org/10.2307/1907574](https://doi.org/10.2307/1907574)
