# Mémoire — Chapitre 4 : Discussion

Oct 1, 2026 · @elyamine

## 4.1 Réponse à la problématique

Notre question était la suivante : peut-on prédire des indicateurs des marchés financiers à partir des données ouvertes de dépenses publiques, en utilisant des techniques de machine learning ?

Sur les données françaises, à un horizon d'un mois, nous ne trouvons **aucune preuve** que les dépenses de l'État améliorent la prévision du spread OAT–Bund, du taux OAT ou du CAC 40. Ce résultat tient pour les trois modèles, pour les dix-neuf extensions réalisées, avec un décalage de publication d'un à trois mois et après correction pour les tests multiples. Aucune des quatre hypothèses n'est validée (tableau 3.8).

Cette réponse a une portée précise. Elle ne dit pas que les dépenses n'ont aucun lien avec les marchés : avec 79 mois de test, un lien faible ou modéré pourrait nous échapper (section 4.3). Elle porte sur l'exécution mensuelle du budget de l'État, pas sur les annonces budgétaires. Nous écrivons donc « pas de preuve (pour l'instant) » plutôt que « les dépenses ne permettent pas de prédire » : la première formulation décrit ce que nos tests montrent, la seconde affirmerait une impossibilité que nos données ne peuvent pas établir.

Un second constat dépasse la question des dépenses : aucun des modèles principaux ne bat la moyenne historique, même sans les dépenses (tableau 3.2). Pour les deux taux, la prévision « pas de variation le mois prochain » fait mieux que la moyenne et que tous nos modèles, même si l'écart n'est significatif que dans deux cas sur six (section 3.2). Ce résultat rejoint celui de Welch et Goyal (2008) : la plupart des prédicteurs proposés pour les marchés financiers ne battent pas une référence simple hors échantillon.

## 4.2 Pourquoi les dépenses n'aident pas : trois hypothèses

Nous proposons trois explications. Elles ne s'excluent pas, et aucune n'est démontrée.

### L'information est déjà connue au moment de la publication

Le budget de l'État est en principe voté avant le début de l'année, dans la loi de finances initiale : les marchés connaissent l'essentiel du plan de dépenses avant la première situation mensuelle. Publiée deux mois plus tard, celle-ci confirmerait surtout ce qui était attendu. Or un prix de marché réagit à l'information nouvelle, pas à ce qui est déjà prévu (Fama, 1970). Ramey (2011) montre que les chocs de dépenses publiques sont en partie anticipés : ce qui compte est le moment de l'annonce, non celui de la dépense. Leeper et al. (2013) montrent de même que l'anticipation des mesures budgétaires fausse l'estimation de leurs effets quand on ne la prend pas en compte, et Attinasi et al. (2009) que, pendant la crise de 2007-2009, l'annonce des plans de sauvetage bancaire a pesé sur les spreads alors que le montant engagé n'a pas d'effet significatif. Notre extension E4 va dans le même sens : même l'écart entre l'exécution et le budget voté, qui mesure une forme de surprise, n'améliore pas la prévision (section 3.5).

Cette explication reste une hypothèse : la tester demanderait une étude d'événement, que nous n'avons pas pu réaliser faute de taux quotidiens accessibles (sections 4.7 et 4.8).

### Les grands mouvements du spread auraient d'autres causes

Les plus fortes variations mensuelles du spread OAT–Bund coïncident avec des événements politiques ou mondiaux (section 3.1) : le début de la crise du Covid-19 en mars 2020 (+20,5 pb), la campagne présidentielle de 2017 (+16,3 pb en février, puis -18,1 pb en mai, après le second tour du 7 mai) et l'annonce de la dissolution de l'Assemblée nationale le 9 juin 2024 (+15,5 pb). Ce sont des variations de moyennes mensuelles : un choc de fin de mois peut apparaître en partie le mois suivant. Le cas de juin 2024 concerne bien les finances publiques, mais par un canal politique : l'incertitude sur la trajectoire budgétaire. C'est une anticipation sur l'avenir, absente de toute ligne de dépense déjà exécutée.

### Une variable lente pour une cible rapide

Les dépenses publiques évoluent sur plusieurs années, alors que le spread, le taux OAT et le CAC 40 réagissent en quelques jours : nous prévoyons un mouvement rapide avec une information lente, disponible avec deux mois de retard. La littérature européenne trouve pourtant un lien entre finances publiques et spreads (Bernoth et al., 2012 ; Afonso et al., 2015). Ce n'est pas une contradiction : ces études **expliquent le niveau** des spreads, avec des panels de pays et des périodes qui incluent la crise de la dette, alors que nous cherchons à **prévoir leur variation** le mois suivant, hors échantillon. Le panel annuel (E17) teste une fréquence plus basse et ne fait pas mieux, mais il ne compte que 75 prévisions (section 3.6).

Enfin, la France n'a pas connu de crise de la dette entre 2014 et 2026, contrairement à l'Italie ou à l'Espagne en 2011-2012. Afonso et al. (2015) montrent que les marchés sanctionnent beaucoup plus fortement les déficits attendus à partir de mars 2009 : le lien dépend de la période, et les dépenses ne comptent peut-être qu'en période de tension. Dans le panel trimestriel, ajouter les dépenses améliore le R² de Ridge de 3 à 4 points sur 2010-2014 et le dégrade de 11 à 13 points après 2015 (section 3.6). Ces écarts ne sont toutefois pas testés, et l'extension avec interactions de tension (E18) ne les confirme pas.

## 4.3 Ce que le résultat négatif veut dire, et ce qu'il ne veut pas dire

Un résultat négatif n'a de valeur que si l'on sait ce que le test aurait pu détecter. Trois contrôles permettent d'en juger.

### Ce que le test aurait trouvé : la puissance

Le contrôle positif (section 3.3, tableau 3.4) ajoute à M0 une variable fictive corrélée à la cible. Avec une corrélation de 0,5, le modèle bat la moyenne historique dans 80 à 100 % des tirages ; avec une corrélation de 0,3, dans 20 à 30 % seulement. Notre dispositif repère donc un signal fort, mais manquerait souvent un signal modéré.

Nos tests écartent un pouvoir prédictif fort des dépenses, mais pas un effet faible. La cause principale est la taille de l'échantillon : les séries budgétaires ouvertes commencent en 2013, ce qui laisse 79 mois de test, le choix de commencer le test en 2020 pour garder assez d'entraînement y contribuant aussi.

### Ce que fait du pur bruit : le contrôle négatif

Quand on remplace les sept dépenses par sept variables tirées au hasard, 90 à 95 % des tirages de bruit font au moins aussi bien que les vraies dépenses avec Ridge (section 3.3). Les petites différences entre M1 et M0 ne sont donc pas propres aux dépenses.

Le même contrôle change la lecture de l'importance des variables. Les dépenses pèsent 31 à 37 % de l'importance SHAP, ce qui paraît beaucoup, mais sept variables de bruit en obtiennent en moyenne 34 à 38 % (tableau 3.5). Cela rejoint les mises en garde sur la fiabilité des mesures d'importance des forêts aléatoires (Strobl et al., 2007) : une part d'importance élevée dans un modèle d'arbres ne prouve pas qu'une variable est utile. Sans comparaison à du bruit, ces mesures peuvent tromper.

### Contre quoi comparer : le choix de la référence

Pour les taux, la prévision « pas de variation » bat la moyenne historique (tableau 3.2) : la moyenne n'est donc pas la référence la plus exigeante. Le panel trimestriel (E15) montre un autre piège : un R² de +15 % venait du fait que la cible était une moyenne sur le trimestre, en partie prévisible de façon mécanique (Working, 1960) ; l'autocorrélation d'ordre 1 passe de 0,32 en moyenne trimestrielle à 0,07 en fin de trimestre, et le R² devient négatif (section 3.6). Nos cibles de taux sont aussi des moyennes mensuelles, ce qui justifie d'inclure toujours la variation passée dans les modèles.

Ces trois points ont un même message : un bon score ne suffit pas, il faut le comparer à une référence simple et à du bruit.

## 4.4 Retour sur les modèles : pourquoi le machine learning ne fait pas mieux, et ce qui reste prévisible

### Pourquoi les modèles d'arbres font moins bien que Ridge (H3)

On aurait pu attendre du machine learning qu'il trouve des relations non linéaires que la régression ne voit pas, comme dans les travaux sur les rendements d'actions (Gu et al., 2020). C'est l'inverse : XGBoost est le moins bon des trois modèles, et la forêt aléatoire ne fait pas mieux que Ridge (tableau 3.3). Deux éléments peuvent l'expliquer.

Le premier est le rapport entre signal et bruit. Avec 70 à 148 mois d'entraînement et des cibles très bruitées, un modèle flexible trouve surtout des coïncidences qui ne se répètent pas. L'instabilité de XGBoost en est un indice : son R² varie d'environ 9 points selon la seule graine aléatoire (section 3.3).

Le second est le comportement de Ridge (Hoerl et Kennard, 1970). Quand il ne trouve pas de signal, Ridge augmente sa pénalité et rapproche sa prévision de la moyenne. C'est ce qui se passe pour le CAC 40 : avec les jeux M0 et M1, la pénalité choisie dépasse 10 000 dans 27 à 44 % des mois (90 % avec M2), alors qu'elle reste inférieure à 100 dans 72 à 100 % des mois pour le spread. Ridge devient alors presque la moyenne historique, d'où son R² proche de zéro (-1,3 %) : le « meilleur » modèle est celui qui renonce le plus à prévoir. Bouillot et al. (2025) observent aussi que des régressions pénalisées font mieux que XGBoost dans certains pays. Le machine learning demande plus d'observations et un signal plus fort que ce que nos données offrent à un mois.

### Pourquoi l'importance des variables ne dit rien ici (H4)

L'hypothèse H4 supposait que la charge de la dette et les dépenses d'intervention seraient les plus prédictives. Les valeurs SHAP semblaient d'abord aller dans ce sens, avec les dépenses d'intervention en tête parmi les dépenses pour le spread et l'OAT (figure 3.3). Mais des variables de pur bruit obtiennent la même part d'importance, et mélanger les dépenses sur la période de test n'augmente pas l'erreur (section 3.4). Un modèle d'arbres utilise toutes les variables qu'on lui donne, même inutiles.

### Ce qui reste prévisible

Le résultat n'est pas entièrement négatif : certaines extensions battent la moyenne, sans que les dépenses y apportent un gain significatif (tableau 3.6).

- **La volatilité** (E3 : R² de +9,6 % pour le CAC 40 et +3,3 % pour l'OAT, sans les dépenses). C'est cohérent avec un fait bien connu : les périodes agitées se suivent (Engle, 1982). On prévoit mieux l'intensité d'un mouvement que sa direction.
- **Le sens de variation de l'OAT** (E2 : score de Brier +2,5 % sans les dépenses, +5,8 % avec, sans différence significative).
- **Le CAC 40 à 12 mois** (E1 : +11,8 % sans les dépenses). Ce résultat est fragile : il repose sur 68 prévisions qui se chevauchent.

Ce qui est prévisible semble donc venir des marchés eux-mêmes plutôt que du budget de l'État.

## 4.5 Comparaison avec la littérature

### Bouillot, Candelon et Kool (2025) : un R² élevé n'est pas une bonne prévision

L'étude la plus proche de la nôtre annonce d'excellents résultats : un R² de 0,81 à 0,99 selon les pays (0,86 pour la France), et une erreur de 7,3 points de base pour la France sur 2020-2025. Nos résultats semblent contraires aux leurs, mais ils ne mesurent pas la même chose.

Bouillot et al. prévoient le **niveau** du spread, mesurent leur R² par rapport à la moyenne et comparent treize méthodes entre elles (régressions pénalisées, arbres, réseaux de neurones), sans comparaison à la marche aléatoire. Or le spread d'un mois est très proche de celui du mois précédent. Un modèle qui recopie simplement le dernier spread obtient déjà un R² très élevé face à la moyenne. Leur propre analyse le confirme : le spread passé est la variable dominante dans tous les pays.

Nous avons testé cette comparaison de deux façons. Dans notre panel européen (E16), nous retrouvons un R² de 92 à 97 % sur le niveau du spread, comme eux ; mais tous nos modèles font moins bien que la marche aléatoire (XGBoost : erreur de 21,1 points de base contre 18,4, tableau 3.7). Sur la France et la même période qu'eux (janvier 2020 à février 2025), la marche aléatoire a une erreur de 5,1 points de base dans nos données, contre 7,3 pour leur XGBoost ; cette comparaison doit être lue avec prudence, car nos séries sont des moyennes mensuelles et leur définition du spread peut différer.

Notre conclusion n'est pas que leur travail est faux, mais qu'un R² sur le niveau ne suffit pas à juger une prévision : la comparaison à la marche aléatoire est indispensable. Un point commun mérite d'être noté : chez eux aussi, les finances publiques pèsent très peu (une seule variable de finances publiques parmi les cinq plus importantes de chacun des dix pays, soit 50 au total).

### Les autres études européennes

Afonso et al. (2015) et Bernoth et al. (2012) trouvent un lien entre finances publiques et spreads, mais sur le niveau des spreads et des périodes qui incluent la crise de la dette (section 4.2). Belly et al. (2023) trouvent que le machine learning suit mieux les spreads que les modèles économétriques, y compris en variation mensuelle, sur 2004-2019. Notre question est différente : nous testons l'apport d'un bloc de variables, pas la supériorité d'une famille de modèles, et nous ne trouvons pas d'avantage du machine learning (H3).

Enfin, Garlanda-Longueville (2023) étudie, avec des données quotidiennes, les allocutions du président de la République pendant la crise du Covid, qui contenaient des engagements budgétaires : ces annonces ont en général fait baisser le spread. Ce résultat est compatible avec le nôtre : ce sont peut-être les annonces, observées au jour le jour, qui font bouger les marchés, plutôt que l'exécution mensuelle publiée deux mois plus tard.

## 4.6 Implications

**Pour la recherche.** Un résultat de prévision doit toujours être comparé à une référence naïve (moyenne historique et, pour les taux, variation nulle) et à du bruit. Sans ces deux repères, un R² élevé sur un niveau ou une forte part d'importance SHAP peuvent donner une impression de pouvoir prédictif qui n'existe pas. Publier les résultats négatifs, avec des contrôles de puissance, évite que la littérature ne retienne que les configurations qui semblent marcher (Bailey et al., 2014).

**Pour les investisseurs.** Nos résultats ne donnent pas de raison d'utiliser l'exécution mensuelle du budget de l'État pour prévoir le spread, le taux OAT ou le CAC 40 à un mois. Ils n'indiquent pas que les finances publiques sont sans importance : l'information utile semble plutôt se trouver dans les annonces et les anticipations.

**Pour les producteurs de données ouvertes.** Un calendrier de publication archivé et la conservation des versions successives des chiffres permettraient de travailler avec l'information réellement disponible à chaque date (Croushore, 2011).

## 4.7 Limites

### Limites des données

- **Données révisées.** Nous utilisons la dernière version publiée des situations budgétaires, et non les chiffres connus à chaque date (les montants de décembre sont d'abord provisoires).
- **Date de publication.** Le décalage de deux mois est vérifié sur 2023-2026 seulement ; pour 2014-2022, c'est une hypothèse. Les résultats ne changent pas avec un décalage d'un ou de trois mois (section 3.3).
- **Périmètre.** Les données couvrent le budget de l'État, pas la Sécurité sociale ni les collectivités locales, et ne sont pas ventilées par mission.
- **Cibles de taux en moyennes mensuelles**, alors que le CAC 40 est pris en fin de mois : les variations de moyennes sont légèrement autocorrélées de façon mécanique.
- **Variables budgétaires hétérogènes dans l'année.** En médiane, l'écart-type de l'écart cumulé en décembre est 6,3 fois celui de janvier.

### Limites de méthode

- **Petit échantillon.** Avec 70 à 148 mois d'entraînement et 79 mois de test, seul un effet fort pouvait être détecté (section 4.3). Les écarts de quelques points de R² entre deux modèles ne sont pas interprétables.
- **Hyperparamètres.** Ils ont été fixés à des valeurs usuelles, sans réglage sur la période de test, mais le code et les résultats des modèles principaux ont été enregistrés ensemble : nous ne pouvons pas prouver qu'ils ont été choisis avant de voir les résultats. Seules les extensions ont un plan daté avant leur exécution.
- **Instabilité de XGBoost.** Son R² varie d'environ 9 points selon la graine ; les conclusions ne changent pas, mais les chiffres précis dépendent aussi des versions des bibliothèques logicielles.
- **Extensions ajoutées en cours de route.** E17 à E20 ont été ajoutées après avoir vu les résultats d'E15 et E16, et E18 est explicitement exploratoire. E14 (étude d'événement) n'a pas pu être réalisée : l'explication « l'information est déjà connue » (section 4.2) reste donc une hypothèse.
- **Panel européen et actions.** Pour E16, 25 des 68 séries de l'OCDE ne sont plus mises à jour depuis fin 2022 ou début 2024, ce qui conduit à compléter environ 23 % des valeurs de la fin de la période de test. Pour E19, les prix des actions n'incluent pas les dividendes.

## 4.8 Recherches futures

- **Étude d'événement.** Avec des taux quotidiens (Banque de France, Bundesbank) et les dates exactes de publication des situations budgétaires, on pourrait mesurer la réaction du spread le jour même, selon la méthode des études d'événement (MacKinlay, 1997). C'est le test direct de l'explication « l'information est déjà connue ». Garlanda-Longueville (2023) montre qu'une approche à fréquence quotidienne trouve des effets pour les annonces liées au Covid.
- **Les annonces plutôt que l'exécution.** Le projet de loi de finances, les lois de finances rectificatives et les programmes de stabilité sont de l'information nouvelle pour les marchés : ils pourraient être codés comme des surprises, par exemple l'écart entre le déficit annoncé et les prévisions des économistes.
- **Données en temps réel.** Conserver chaque version publiée des situations budgétaires permettrait de travailler avec l'information disponible à chaque date (Croushore, 2011).
- **Plus d'observations.** Un panel de pays plus long, incluant la crise de 2010-2012, avec des cibles de fin de période, augmenterait la puissance des tests.
- **Ventilation sectorielle.** Les données de la commande publique permettraient de relier la dépense aux entreprises qui en bénéficient et de mieux tester le canal des actions sectorielles (E19).

## Références ajoutées par ce chapitre

- Engle, R. F. (1982). Autoregressive conditional heteroscedasticity with estimates of the variance of United Kingdom inflation. *Econometrica*, *50*(4), 987–1007. https://doi.org/10.2307/1912773
- Leeper, E. M., Walker, T. B., & Yang, S.-C. S. (2013). Fiscal foresight and information flows. *Econometrica*, *81*(3), 1115–1145. https://doi.org/10.3982/ECTA8337
- MacKinlay, A. C. (1997). Event studies in economics and finance. *Journal of Economic Literature*, *35*(1), 13–39.
- Strobl, C., Boulesteix, A.-L., Zeileis, A., & Hothorn, T. (2007). Bias in random forest variable importance measures: Illustrations, sources and a solution. *BMC Bioinformatics*, *8*, Article 25. https://doi.org/10.1186/1471-2105-8-25
- Working, H. (1960). Note on the correlation of first differences of averages in a random chain. *Econometrica*, *28*(4), 916–918.
