# Mémoire — Chapitre 4 : Discussion

Oct 2, 2026 · @elyamine


## 4.1 Réponse à la problématique

Notre question de départ était simple : les données ouvertes de dépenses publiques permettent-elles de prévoir des indicateurs des marchés financiers avec du machine learning ?

Pour la France et à un mois, la réponse est non. Nous ne trouvons **aucune preuve** que les dépenses de l'État aident à prévoir le spread OAT-Bund, le taux OAT ou le CAC 40. Le résultat reste le même avec les trois modèles, avec un décalage de publication d'un, deux ou trois mois, et dans les dix-neuf extensions une fois les tests multiples corrigés.

Encore faut-il bien lire ce résultat. Nous ne montrons pas que les dépenses n'ont aucun lien avec les marchés. Avec 79 mois de test, un lien faible ou moyen pourrait nous échapper (section 4.3). Nous ne regardons d'ailleurs que l'exécution mensuelle du budget de l'État, ni les annonces budgétaires ni l'ensemble des administrations publiques. C'est pour cela que nous parlons d'absence de preuve plutôt que d'impossibilité : la première formule décrit ce que nos tests montrent, la seconde irait plus loin que ce que nos données permettent de dire.

Un second constat dépasse la question des dépenses : **aucun modèle ne bat la moyenne historique**, même sans elles. Pour les taux, prévoir simplement « pas de variation le mois prochain » fait mieux que la moyenne et mieux que tous nos modèles, même si l'écart n'est significatif que dans quelques cas. À un mois, ces marchés restent très difficiles à prévoir avec les variables dont nous disposons.

## 4.2 Pourquoi les dépenses n'aident pas : des pistes

Plusieurs explications sont possibles, et elles peuvent se cumuler. Aucune n'est démontrée par nos tests, mais certaines sont mieux appuyées que d'autres. Pour chacune, nous indiquons ce qui la soutient et ce qui la limite.

### L'information est peut-être déjà connue

Le budget de l'État est voté en décembre pour l'année suivante. Les marchés peuvent donc connaître le plan de dépenses avant même le début de l'année, et la situation mensuelle, publiée deux mois plus tard, ne ferait alors que confirmer ce qui était prévu. Or un prix réagit à ce qui est nouveau, pas à ce qui est attendu (Fama, 1970). Ramey (2011) le montre pour les dépenses publiques : ce qui compte est le moment où elles sont annoncées, plus que celui où elles sont engagées. Attinasi et al. (2009) observent la même chose pendant la crise de 2007-2009, où ce sont les annonces de plans de sauvetage bancaire qui ont pesé sur les spreads, pas les montants. Notre extension E4 va dans le même sens : même l'écart entre l'exécution et le budget voté, qui mesure une forme de surprise, n'améliore pas la prévision.

Une vérification préliminaire, du type étude d'événement (MacKinlay, 1997), conforte cette idée sans la démontrer. Sur les 40 publications que nous avons pu dater (2017-2026), le CAC 40 ne réagit pas, le jour même, à la variation du solde publiée (corrélation de -0,13, p = 0,42, section 3.5 et annexe F). Ce test ne porte pas sur le spread, faute de taux quotidiens accessibles, et avec si peu d'événements il n'aurait repéré qu'une réaction forte. Le vrai test serait d'observer le spread lui-même le jour de chaque publication (sections 4.7 et 4.8).

### Ce qui fait bouger le spread n'est pas budgétaire

Les plus fortes variations mensuelles du spread tombent en mars 2020 (+20,5 pb), en février et mai 2017 (+16,3 et −18,1 pb) et en juin 2024 (+15,5 pb). Ce sont les mois du début de la crise du Covid-19, de la campagne présidentielle de 2017 et de l'annonce de la dissolution de l'Assemblée nationale le 9 juin 2024. Ce dernier épisode touche bien aux finances publiques, mais par la politique : les investisseurs craignent qu'une nouvelle majorité ne tienne pas la trajectoire budgétaire. C'est une anticipation sur l'avenir, que l'on ne peut lire dans aucune ligne de dépense déjà exécutée.

### Le retard de publication n'est pas en cause

On pourrait penser que les dépenses n'aident pas simplement parce que l'information arrive trop tard, deux mois après les faits. Nous l'avons vérifié : avec un décalage d'un mois seulement, plus favorable aux dépenses, aucun R² ne devient positif (le meilleur vaut -0,7 %) et la plus petite p-value corrigée est de 0,81 (section 3.3). Avec trois mois, elle est de 0,51, et aucun R² n'est positif non plus. Le problème ne tient donc pas à la fraîcheur des chiffres.

### Le sens de l'effet n'est pas évident

La théorie elle-même ne dit pas dans quel sens les dépenses devraient jouer. Une hausse financée par l'emprunt peut faire monter les taux, comme le prévoit la vision keynésienne, ou rester sans effet si les ménages anticipent les impôts futurs, selon l'équivalence ricardienne de Barro (1974), comme le rappelle la section 1.1.1. Si l'effet change de signe d'une période à l'autre, il peut s'annuler dans un modèle estimé sur toute la période. Nous avons tenté d'en tenir compte avec des interactions selon le régime de taux (E5) et selon les périodes de tension (E18). Elles n'améliorent pas la prévision, mais cela ne prouve pas que l'effet est absent dans chaque régime : chaque sous-période contient trop peu de mois pour en juger.

### Une information lente et tardive pour une cible rapide

Les dépenses de l'État reflètent des décisions prises à l'avance et évoluent plus lentement que les marchés, qui réagissent en quelques jours. Nous essayons donc de prévoir un mouvement rapide avec une information lente, qui arrive de surcroît avec deux mois de retard.

La littérature européenne trouve pourtant un lien entre finances publiques et spreads (Bernoth et al., 2012 ; Afonso et al., 2015). Ce n'est pas une contradiction : ces études expliquent le niveau des spreads, en panel et souvent en période de crise, alors que nous cherchons à prévoir la variation du mois suivant, hors échantillon. La France n'a pas connu de crise de la dette sur notre période, contrairement à l'Italie ou à l'Espagne en 2011-2012, et Afonso et al. (2015) montrent que les marchés sanctionnent surtout les finances publiques quand la tension monte. Notre panel trimestriel va un peu dans ce sens : entre 2010 et 2014, ajouter les dépenses améliore le R² de Ridge de 4 points, alors qu'il le dégrade de près de 13 points après 2015 (section 3.6). Ces écarts ne sont toutefois pas testés, et le modèle avec interactions de crise (E18) ne les confirme pas.

## 4.3 Ce que le résultat négatif veut dire, et ce qu'il ne veut pas dire

Un résultat négatif ne vaut que si l'on sait ce que le test aurait été capable de détecter. Quatre éléments permettent d'en juger.

### La puissance du test

Le contrôle positif (section 3.3) ajoute à M0 une variable fictive corrélée à la cible. Avec une corrélation de 0,5, le modèle bat la moyenne historique dans 80 à 100 % des tirages ; avec 0,3, dans 20 à 30 % seulement. Notre dispositif repère donc un signal fort, mais il passerait souvent à côté d'un signal moyen. Nos tests écartent un fort pouvoir prédictif des dépenses, pas un effet faible. La raison principale est la taille de l'échantillon : les séries budgétaires ouvertes commencent en 2013, ce qui ne laisse que 79 mois de test, d'autant que nous avons fait commencer le test en 2020 pour garder assez de mois d'entraînement.

### Plus de données suffiraient-elles ?

On pourrait croire qu'il suffirait d'ajouter des données. Nos panels vont plutôt contre cette idée. E15 compte 330 prévisions trimestrielles, E16 en compte 874 avec 150 variables, dont 18 de finances publiques, et les finances publiques n'y améliorent aucune prévision (p de 0,08 à 0,81). Davantage de données rendrait le test plus sensible et permettrait de repérer un effet plus faible. Rien n'indique en revanche qu'elles feraient apparaître un fort pouvoir prédictif que nous n'avons pas trouvé.

### Le contrôle négatif

Quand on remplace les sept dépenses par sept variables tirées au hasard, 90 à 95 % des tirages de bruit font au moins aussi bien que les vraies dépenses avec Ridge. Les petits écarts entre M1 et M0 ne sont donc pas propres aux dépenses : n'importe quelles variables ajoutées produisent des écarts du même ordre. Ce contrôle change aussi la lecture de l'importance des variables. Les dépenses pèsent 31 à 37 % de l'importance SHAP, ce qui paraît beaucoup, mais du bruit en obtient 34 à 38 %. Une part d'importance élevée dans un modèle d'arbres ne prouve donc pas qu'une variable est utile, d'autant que ces mesures peuvent être biaisées dans les forêts aléatoires (Strobl et al., 2007).

### Le choix de la référence

Pour les taux, la prévision « pas de variation » bat la moyenne historique : la moyenne n'est donc pas la référence la plus exigeante. Le panel trimestriel (E15) montre un autre piège. Son R² de +15 % venait de ce que la cible était une moyenne sur le trimestre, en partie prévisible par construction (Working, 1960) ; avec le spread de fin de trimestre, il devient négatif. Un bon score ne suffit pas : il faut le comparer à une référence simple et à du bruit, et vérifier que la cible ne contient pas de régularité mécanique.

## 4.4 Retour sur les modèles

### Les arbres ne font pas mieux que Ridge (H3)

On pouvait espérer que le machine learning trouve des relations non linéaires que la régression ne voit pas. Ce n'est pas le cas : XGBoost est le moins bon des trois modèles et la forêt aléatoire ne fait pas mieux que Ridge. Deux raisons peuvent l'expliquer.

La première tient au rapport entre le signal et le bruit. Avec 70 à 148 mois d'entraînement et des cibles très bruitées, un modèle flexible peut s'ajuster à des coïncidences de l'échantillon d'apprentissage qui ne se reproduisent pas ensuite. L'instabilité de XGBoost, dont le R² varie d'environ 9 points selon la seule graine aléatoire, va dans ce sens.

La seconde tient au fonctionnement de Ridge. Quand il ne trouve pas de signal, il augmente sa pénalité et ramène sa prévision vers la moyenne. Pour le CAC 40, la pénalité dépasse 10 000 dans 27 % des mois (M0) à 44 % (M1), et Ridge devient presque la moyenne historique, d'où un R² proche de zéro (−1,3 %). Le « meilleur » modèle est donc celui qui renonce le plus à prévoir. Bouillot et al. (2025) font une observation voisine : pour la Belgique et l'Espagne, une régression pénalisée (LASSO, Elastic Net) a un RMSE plus faible que XGBoost. Le machine learning n'est pas inutile pour autant, mais il lui faut plus d'observations ou un signal plus fort que ce que nos données offrent à un mois.

### L'importance des variables ne dit rien ici (H4)

Les valeurs SHAP semblaient d'abord donner raison à H4, avec les dépenses d'intervention en tête parmi les dépenses. Mais des variables de pur bruit obtiennent la même part d'importance, et mélanger les dépenses sur la période de test n'augmente pas l'erreur. Un modèle d'arbres utilise toutes les variables qu'on lui donne, même inutiles : il faut toujours comparer leur importance à celle du bruit avant de conclure.

### Ce qui reste prévisible

Quelques extensions battent la moyenne, sans que les dépenses y apportent un gain significatif : la volatilité (E3 : +9,6 % pour le CAC 40, +3,3 % pour l'OAT), le sens de variation de l'OAT (E2 : score de Brier +2,5 %) et le CAC 40 à 12 mois (E1 : +11,8 %). Ce dernier résultat est fragile, puisqu'il repose sur 68 prévisions qui se chevauchent. Que la volatilité soit en partie prévisible n'a rien d'étonnant : les périodes agitées ont tendance à se suivre (Engle, 1982). Ce qui se prévoit un peu semble donc venir des marchés eux-mêmes plus que du budget.

## 4.5 Comparaison avec la littérature

### Bouillot, Candelon et Kool (2025)

L'étude la plus proche de la nôtre annonce un R² de 0,81 à 0,99 selon les pays (0,86 pour la France) et une erreur de 7,3 points de base pour la France sur 2020-2025. Nos résultats semblent contredire les leurs, mais nous ne mesurons pas la même chose. Ces auteurs prévoient le niveau du spread. Or le spread d'un mois ressemble beaucoup à celui du mois précédent, et recopier simplement le dernier spread donne déjà un R² très élevé face à la moyenne. Leur propre analyse montre d'ailleurs que le spread passé domine les prévisions dans tous les pays. Dans la version de leur document de travail que nous avons consultée, les treize méthodes sont comparées entre elles et à la moyenne, mais pas à la marche aléatoire. Le résumé d'une version plus récente indique que l'AR(1) et la marche aléatoire ont des erreurs plus faibles que les modèles de machine learning dans chaque pays, quand ceux-ci sont réestimés à chaque date.

Nos résultats vont dans le même sens. Dans notre panel européen (E16), nous retrouvons un R² de 92 à 97 % sur le niveau du spread, mais tous nos modèles font moins bien que la marche aléatoire (pour XGBoost, une erreur de 21,1 points de base contre 18,4). Sur la France et sur la même période qu'eux (janvier 2020 à février 2025), la marche aléatoire a une erreur de 5,1 points de base dans nos données, contre 7,3 pour leur XGBoost. La comparaison est à prendre avec prudence, car nos séries sont des moyennes mensuelles et leur définition du spread peut être différente. Un R² sur le niveau ne suffit donc pas à juger une prévision : la comparaison à la marche aléatoire est indispensable. Autre point commun, les finances publiques pèsent très peu chez eux aussi, avec une seule variable de finances publiques parmi les cinq plus importantes de chacun des dix pays, soit 50 au total. Notre apport est d'isoler les dépenses en comparant le même modèle avec et sans elles. Sur le machine learning, en revanche, nous ne retrouvons pas leur résultat, puisque XGBoost est le moins bon de nos modèles (H3).

### Welch et Goyal (2008)

Welch et Goyal montrent que la plupart des variables proposées pour prévoir la bourse américaine ne battent pas la moyenne historique hors échantillon. Nos résultats sur le CAC 40 vont dans le même sens, et la même difficulté se retrouve pour le spread et le taux OAT à un mois.

### Les autres études européennes

Afonso et al. (2015) et Bernoth et al. (2012) trouvent un lien entre finances publiques et spreads, mais sur des périodes qui incluent la crise de la dette, et pour expliquer le niveau des spreads (section 4.2). Belly et al. (2023) montrent que le machine learning suit mieux les spreads que les modèles économétriques sur 2004-2019. Leur question porte sur la supériorité d'une famille de modèles, la nôtre sur l'apport d'un bloc de variables. Garlanda-Longueville (2023) observe, en données quotidiennes, un effet des allocutions du président de la République pendant la crise du Covid sur le CAC 40 et sur le spread. Ce résultat rejoint le nôtre : il suggère que ce sont les annonces, suivies au jour le jour, qui font bouger les marchés, plutôt que l'exécution mensuelle publiée deux mois plus tard.

## 4.6 Implications

Pour la recherche, un résultat de prévision devrait toujours être comparé à une référence simple (la moyenne historique et, pour les taux, la variation nulle) et à du bruit. Sans ces repères, un R² élevé sur un niveau ou une forte part d'importance SHAP peuvent faire croire à un pouvoir prédictif qui n'existe pas. Publier aussi les résultats négatifs, avec des contrôles de puissance, évite que la littérature ne retienne que les configurations qui semblent marcher.

Pour les investisseurs, nos résultats ne donnent aucune raison d'utiliser l'exécution mensuelle du budget de l'État pour prévoir le spread, le taux OAT ou le CAC 40 à un mois. Ils ne disent pas pour autant que les finances publiques sont sans importance pour les marchés : l'information utile se trouve sans doute plutôt dans les annonces et les anticipations.

Pour les producteurs de données ouvertes, enfin, un calendrier de publication archivé et la conservation des versions successives des chiffres permettraient de travailler avec l'information réellement disponible à chaque date.

## 4.7 Limites

Plusieurs limites tiennent aux données. Nous utilisons la dernière version publiée des situations budgétaires, et non les chiffres connus à chaque date ; ceux de décembre, en particulier, sont d'abord provisoires. Le décalage de publication de deux mois n'est vérifié que sur 2023-2026 et reste une hypothèse pour 2014-2022, même si les résultats ne changent pas avec un décalage d'un ou de trois mois (section 3.3). Les données ne couvrent que le budget de l'État, sans la Sécurité sociale ni les collectivités, et ne sont pas ventilées par mission. Le spread et le taux OAT sont des moyennes du mois (OCDE), alors que le CAC 40 est pris en fin de mois, et les variations de moyennes sont un peu autocorrélées par construction. Enfin, l'écart cumulé des variables budgétaires varie beaucoup plus en fin d'année : son écart-type est en médiane 6,3 fois plus grand en décembre qu'en janvier.

D'autres limites tiennent à la méthode. Avec 70 à 148 mois d'entraînement et 79 mois de test, seul un effet fort pouvait être détecté, et les écarts de quelques points de R² entre deux modèles ne sont pas interprétables. Les hyperparamètres ont été fixés à des valeurs usuelles, sans réglage sur la période de test, mais le code et les résultats des modèles principaux ont été enregistrés ensemble : nous ne pouvons pas prouver qu'ils ont été choisis avant de voir les résultats, alors que les extensions, elles, ont un plan daté avant leur exécution. Les chiffres de XGBoost et de la forêt aléatoire dépendent aussi des versions des bibliothèques logicielles, même si les conclusions n'en dépendent pas. Les extensions E17 à E20 ont été ajoutées après avoir vu les résultats d'E15 et E16, et E18 est exploratoire. Pour E16, 25 des 68 séries de l'OCDE ne sont plus mises à jour depuis fin 2022 ou début 2024, si bien qu'environ 23 % des valeurs de la fin de la période de test sont complétées. Pour E19, les prix des actions n'incluent pas les dividendes.

La limite la plus importante pour l'interprétation reste l'absence d'étude d'événement sur le spread. E14 n'a pas pu être réalisée sur le spread, et sa version sur le CAC 40, faite après coup (annexe F), ne repose que sur les 40 publications que nous avons pu dater. L'explication « l'information est déjà connue » (section 4.2) reste donc une hypothèse.

## 4.8 Recherches futures

La suite la plus directe serait une étude d'événement sur le spread : avec des taux quotidiens et les dates exactes de publication des situations budgétaires, on pourrait mesurer la réaction du marché le jour même et tester directement l'idée que l'information est déjà connue.

Il serait aussi intéressant d'étudier les annonces plutôt que l'exécution. Le projet de loi de finances, les lois de finances rectificatives et les programmes de stabilité apportent de l'information nouvelle aux marchés. On pourrait les coder comme des surprises, par exemple par l'écart entre le déficit annoncé et les prévisions des économistes.

Trois autres pistes viendraient compléter ce travail : conserver chaque version publiée des situations budgétaires pour travailler en temps réel ; utiliser un panel de pays plus long, incluant la crise de 2010-2012, avec des cibles de fin de période plutôt que des moyennes ; et s'appuyer sur les données de la commande publique pour relier la dépense aux entreprises qui en bénéficient, ce qui permettrait de mieux tester le canal des actions sectorielles (E19).

## Références ajoutées par ce chapitre

- MacKinlay, A. C. (1997). Event studies in economics and finance. *Journal of Economic Literature*, 35(1), 13–39. [https://www.jstor.org/stable/2729691](https://www.jstor.org/stable/2729691)
- Strobl, C., Boulesteix, A.-L., Zeileis, A., & Hothorn, T. (2007). Bias in random forest variable importance measures: Illustrations, sources and a solution. *BMC Bioinformatics*, 8, Article 25. [https://doi.org/10.1186/1471-2105-8-25](https://doi.org/10.1186/1471-2105-8-25)
- Engle, R. F. (1982). Autoregressive conditional heteroscedasticity with estimates of the variance of United Kingdom inflation. *Econometrica*, 50(4), 987–1007. [https://doi.org/10.2307/1912773](https://doi.org/10.2307/1912773)
- Working, H. (1960). Note on the correlation of first differences of averages in a random chain. *Econometrica*, 28(4), 916–918. [https://doi.org/10.2307/1907574](https://doi.org/10.2307/1907574)
