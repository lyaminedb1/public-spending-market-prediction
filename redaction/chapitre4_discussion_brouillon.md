# Mémoire — Chapitre 4 : Discussion

Sep 30, 2026 · @elyamine

> **Statut : brouillon de travail, à réécrire par Elyamine.** Les idées viennent de nos discussions ; le guide ECE interdit de rendre des interprétations rédigées par l'IA sans relecture critique et apport personnel. Pour chaque paragraphe : garder, couper ou contredire, puis reformuler avec tes mots. Les chiffres, eux, sont vérifiés dans le dépôt.

## 4.1 Réponse à la problématique

Notre question était la suivante : peut-on prédire des indicateurs des marchés financiers à partir des données ouvertes de dépenses publiques, en utilisant le machine learning ?

Sur les données françaises, à un horizon d'un mois, la réponse est négative. Nous ne trouvons **aucune preuve** que les dépenses de l'État améliorent la prévision du spread OAT–Bund, du taux OAT ou du CAC 40. Ce résultat tient pour les trois modèles, pour les dix-neuf extensions réalisées, avec un décalage de publication d'un à trois mois, et après correction pour les tests multiples.

Cette réponse a une portée précise. Elle ne dit pas que les dépenses n'ont aucun lien avec les marchés. Elle dit que, avec 79 mois de test, un lien faible ou modéré pourrait nous échapper (section 4.3). Elle porte sur l'exécution mensuelle du budget de l'État, et non sur les annonces budgétaires ni sur l'ensemble des administrations publiques. Nous préférons donc écrire « pas de preuve » plutôt que « les dépenses ne permettent pas de prédire » : la première formulation décrit ce que nos tests montrent ; la seconde affirmerait une impossibilité que nos données ne peuvent pas démontrer. C'est une conclusion « pour l'instant » : avec des séries plus longues ou des données quotidiennes, un effet faible pourrait apparaître.

Un second constat dépasse la question des dépenses : **aucun modèle ne bat la moyenne historique**, même sans les dépenses. Pour les taux, la prévision la plus simple, « pas de variation le mois prochain », fait même mieux que la moyenne et que tous nos modèles, même si l'écart n'est significatif que dans quelques cas. À un mois, ces marchés sont donc très difficiles à prévoir, quelles que soient les variables utilisées.

## 4.2 Pourquoi les dépenses n'aident pas : trois explications

Le chapitre 3 montre que les dépenses de l'État n'améliorent la prévision d'aucune des trois cibles. Nous proposons trois explications. Elles ne s'excluent pas.

### L'information est déjà connue au moment de la publication

Le budget de l'État est voté en décembre, dans la loi de finances de l'année suivante. Les marchés connaissent donc le plan de dépenses avant le début de l'année. De plus, les grandes lignes évoluent lentement : les dépenses de personnel ou la charge de la dette ne changent pas brutalement d'un mois à l'autre. Quand la situation mensuelle est publiée, deux mois plus tard, elle confirmerait surtout ce qui était attendu.

Or un prix de marché réagit à l'information nouvelle, pas à ce qui est déjà prévu (Fama, 1970). Ramey (2011) montre que, pour les dépenses publiques, ce qui compte est le moment de l'annonce, et non celui où l'argent est dépensé. L'extension E4 va dans ce sens : même l'écart entre l'exécution et le budget voté, qui mesure une forme de surprise, n'améliore pas la prévision. On retrouve la même idée chez Attinasi et al. (2009) : pendant la crise de 2007-2009, c'est l'annonce des plans de sauvetage bancaire qui a fait monter les spreads, et non le montant engagé.

Cette explication reste une hypothèse. Pour la démontrer, il faudrait observer le spread le jour même de chaque publication (étude d'événement). Cette étude n'a pas pu être réalisée, faute de taux quotidiens accessibles (sections 4.7 et 4.8).

### Ce qui fait bouger le spread n'est pas budgétaire

Les plus fortes variations mensuelles du spread OAT–Bund sont observées en mars 2020 (+20,5 pb), autour de l'élection présidentielle de 2017 (+16,3 pb en février, -18,1 pb en mai) et en juin 2024 (+15,5 pb). Ces mouvements coïncident avec des événements politiques ou mondiaux : le début de la crise du Covid-19 en mars 2020, la campagne présidentielle de 2017 (premier tour le 23 avril, second tour le 7 mai) et l'annonce de la dissolution de l'Assemblée nationale le 9 juin 2024.

Le cas de juin 2024 est intéressant. Il concerne bien les finances publiques, mais par un canal politique : la crainte qu'une nouvelle majorité ne tienne pas la trajectoire budgétaire. Cette crainte est une anticipation sur l'avenir ; elle n'apparaît dans aucune ligne de dépense déjà exécutée.

### Une variable lente pour une cible rapide

Les dépenses publiques évoluent sur plusieurs années. Le spread, le taux OAT et le CAC 40 réagissent en quelques jours. Nous cherchons donc à prévoir un mouvement rapide avec une information lente, et disponible avec deux mois de retard.

La littérature européenne trouve pourtant un lien entre finances publiques et spreads (Bernoth et al., 2012 ; Afonso et al., 2015). Ce n'est pas une contradiction : ces études **expliquent le niveau** des spreads, en coupe ou en panel, souvent sur des périodes de crise. Nous cherchons à **prévoir leur variation** le mois suivant, hors échantillon. Une variable peut expliquer un niveau sur dix ans sans aider à prévoir le mois prochain. Le panel annuel (E17) teste une fréquence plus basse ; il ne fait pas mieux, mais il ne compte que 75 prévisions.

Enfin, la France n'a pas connu de crise de la dette pendant notre période (2014-2026), contrairement à l'Italie ou à l'Espagne en 2011-2012. Il est possible que les dépenses ne comptent pour les marchés qu'en période de tension (Afonso et al., 2015). Le panel trimestriel va dans ce sens : sur 2010-2014, ajouter les dépenses améliore le R² de 3 à 4 points, alors qu'il le dégrade après 2015 (section 3.6). Mais ces écarts ne sont pas testés, et le modèle qui introduit explicitement des interactions avec les périodes de tension (E18) ne les confirme pas.

## 4.3 Ce que le résultat négatif veut dire, et ce qu'il ne veut pas dire

Un résultat négatif n'a de valeur que si l'on sait ce que le test aurait pu détecter. Trois contrôles permettent d'en juger.

### Ce que le test aurait trouvé : la puissance

Le contrôle positif (section 3.3) ajoute à M0 une variable fictive, construite pour être corrélée à la cible. Avec une corrélation de 0,5, le modèle bat la moyenne historique dans 80 à 100 % des tirages. Avec une corrélation de 0,3, il ne la bat que dans 20 à 30 % des tirages. Notre dispositif repère donc un signal fort, mais il manquerait souvent un signal modéré.

Cela définit la portée de notre conclusion : nos tests ne montrent pas de pouvoir prédictif fort des dépenses ; un effet faible reste possible. La cause principale est la taille de l'échantillon : les séries budgétaires ouvertes commencent en 2013, ce qui laisse 79 mois de test. C'est d'abord une limite des données disponibles ; le choix de commencer le test en 2020, pour garder assez de mois d'entraînement, y contribue aussi.

### Ce que fait du pur bruit : le contrôle négatif

Quand on remplace les sept dépenses par sept variables tirées au hasard, 90 à 95 % des tirages de bruit font au moins aussi bien que les vraies dépenses avec Ridge. Les petites différences entre M1 et M0 ne sont donc pas propres aux dépenses : n'importe quelles variables ajoutées produisent des écarts du même ordre.

Le même contrôle change la lecture de l'importance des variables. Les dépenses pèsent 31 à 37 % de l'importance SHAP, ce qui paraît beaucoup ; mais du bruit obtient 34 à 38 %. Une part d'importance élevée dans un modèle d'arbres ne montre donc pas qu'une variable est utile. C'est une leçon de méthode plus générale : sans comparaison à du bruit, les mesures d'importance peuvent tromper.

### Contre quoi comparer : le choix de la référence

Pour les taux, la prévision « pas de variation » bat la moyenne historique. La moyenne n'est donc pas la référence la plus exigeante. Le panel trimestriel (E15) montre un autre piège : un R² de +15 % venait du fait que la cible était une moyenne sur le trimestre, ce qui la rend en partie prévisible de façon mécanique (Working, 1960). Avec le spread de fin de trimestre, le R² devient négatif.

Ces trois points ont un même message : un bon score ne suffit pas. Il faut toujours le comparer à une référence simple et à du bruit, et vérifier que la cible ne contient pas une régularité mécanique.

## 4.4 Retour sur les modèles : pourquoi le machine learning ne fait pas mieux, et ce qui reste prévisible

### Pourquoi les modèles d'arbres font moins bien que Ridge (H3)

On aurait pu attendre du machine learning qu'il trouve des relations non linéaires que la régression ne voit pas. C'est l'inverse qui se produit : XGBoost est le moins bon des trois modèles, et la forêt aléatoire ne fait pas mieux que Ridge. Deux éléments peuvent l'expliquer.

Le premier est le rapport entre le signal et le bruit. Avec 70 à 148 mois d'entraînement et des cibles très bruitées, un modèle flexible trouve toujours des régularités dans l'échantillon d'apprentissage, mais ce sont surtout des coïncidences qui ne se répètent pas. L'instabilité de XGBoost en est un indice : son R² varie d'environ 9 points selon la seule graine aléatoire. Un modèle qui change autant avec le hasard du tirage apprend surtout du bruit.

Le second est le comportement de Ridge. Quand il ne trouve pas de signal, Ridge augmente sa pénalité et rapproche sa prévision de la moyenne. C'est ce qui se passe pour le CAC 40 : la pénalité choisie est souvent très forte (supérieure à 10 000 dans 27 à 44 % des mois, contre moins de 100 le plus souvent pour le spread), et Ridge devient presque la moyenne historique, d'où son R² proche de zéro (-1,3 %). Autrement dit, le « meilleur » modèle est celui qui renonce le plus à prévoir. Ce résultat rejoint une observation de Bouillot et al. (2025) : même dans leur étude, des régressions pénalisées simples font mieux que XGBoost dans certains pays (Belgique, Espagne).

Le machine learning n'est donc pas inutile en soi ; il a besoin de plus d'observations et d'un signal plus fort que ce que nos données offrent à un mois.

### Pourquoi l'importance des variables ne dit rien ici (H4)

L'hypothèse H4 supposait que la charge de la dette et les dépenses d'intervention seraient les plus prédictives. Les valeurs SHAP semblaient d'abord aller dans ce sens, avec les dépenses d'intervention en tête. Mais des variables de pur bruit obtiennent la même part d'importance, et mélanger les dépenses sur la période de test n'augmente pas l'erreur. Un modèle d'arbres utilise toutes les variables qu'on lui donne, même inutiles ; il faut donc toujours comparer leur importance à celle du bruit avant d'en tirer une conclusion.

### Ce qui reste prévisible

Le résultat n'est pas entièrement négatif. Certaines extensions battent la moyenne, mais **sans les dépenses** :

- **La volatilité** (E3) : l'ampleur des mouvements du mois suivant est en partie prévisible (R² de +9,6 % pour le CAC 40, +3,3 % pour l'OAT). C'est cohérent avec un fait bien connu des marchés : les périodes agitées se suivent, et les périodes calmes aussi (Engle, 1982). On prévoit mieux l'intensité d'un mouvement que sa direction.
- **Le sens de variation de l'OAT** (E2) : la classification hausse / baisse fait un peu mieux que la fréquence historique (score de Brier +2,5 %).
- **Le CAC 40 à 12 mois** (E1 : +11,8 %). Ce résultat est fragile : il repose sur 68 prévisions qui se chevauchent, donc sur très peu d'informations indépendantes.

Dans aucun de ces cas l'ajout des dépenses n'apporte un gain significatif. Ce qui est prévisible vient des marchés eux-mêmes, pas du budget de l'État.

## 4.5 Comparaison avec la littérature

### Bouillot, Candelon et Kool (2025) : un R² élevé n'est pas une bonne prévision

L'étude la plus proche de la nôtre annonce d'excellents résultats : un R² de 0,81 à 0,99 selon les pays (0,86 pour la France), et une erreur de 7,3 points de base pour la France sur 2020-2025. Nos résultats semblent contraires aux leurs. En réalité, ils ne mesurent pas la même chose.

Bouillot et al. prévoient le **niveau** du spread, et comparent leurs modèles à la moyenne et à des régressions linéaires. Or le spread d'un mois est très proche de celui du mois précédent. Un modèle qui recopie simplement le dernier spread obtient déjà un R² très élevé face à la moyenne. Leur propre analyse le confirme : le spread passé est la variable dominante dans tous les pays.

Nous avons testé cette comparaison de deux façons. D'abord, dans notre panel européen (E16), nous retrouvons un R² de 92 à 97 % sur le niveau du spread, comme eux ; mais tous nos modèles font moins bien que la marche aléatoire, qui prévoit le spread du mois précédent (XGBoost : erreur de 21,1 points de base contre 18,4). Ensuite, sur la France et la même période qu'eux (janvier 2020 à février 2025), la marche aléatoire a une erreur de 5,1 points de base dans nos données, contre 7,3 pour leur XGBoost. Cette dernière comparaison doit être lue avec prudence : nos séries sont des moyennes mensuelles, et leur définition exacte du spread peut différer.

Notre conclusion n'est pas que leur travail est faux, mais qu'un R² sur le niveau ne suffit pas à juger une prévision. La comparaison à la marche aléatoire est indispensable. Il faut aussi noter un point commun : chez eux aussi, les finances publiques pèsent très peu (une seule variable parmi les 50 plus importantes).

### Welch et Goyal (2008) : un résultat attendu

Welch et Goyal montrent que la plupart des variables proposées pour prévoir la bourse américaine ne battent pas la moyenne historique hors échantillon. Nos résultats sur le CAC 40 vont exactement dans ce sens. Nous montrons que la même difficulté existe pour le spread et le taux OAT à un mois.

### Les études européennes sur les finances publiques

Afonso et al. (2015) et Bernoth et al. (2012) trouvent un lien entre finances publiques et spreads. Comme expliqué en section 4.2, ces études expliquent le niveau des spreads, sur des périodes qui incluent la crise de la dette, alors que nous prévoyons leur variation hors échantillon. Afonso et al. montrent d'ailleurs que la dette ne compte qu'après mars 2009 : le lien dépend de la période, et notre période française ne contient pas de crise de la dette.

Belly et al. (2023) trouvent que le machine learning suit mieux les spreads que les modèles économétriques, y compris en variation mensuelle, sur 2004-2019. Notre question est différente : nous testons l'apport d'un bloc de variables, pas la supériorité d'une famille de modèles. Sur ce second point, nous ne trouvons pas d'avantage du machine learning (H3) : XGBoost est même le moins bon de nos modèles.

Enfin, Garlanda-Longueville (2023) trouve un effet des annonces budgétaires françaises sur le spread, avec des données quotidiennes. Ce résultat est compatible avec le nôtre : il suggère que ce sont les annonces, observées au jour le jour, qui font bouger les marchés, plutôt que l'exécution mensuelle publiée deux mois plus tard.

## 4.6 Implications

**Pour la recherche.** Un résultat de prévision doit toujours être comparé à une référence naïve (moyenne historique et, pour les taux, variation nulle) et à du bruit. Sans ces deux repères, un R² élevé sur un niveau ou une forte part d'importance SHAP peuvent donner une impression de pouvoir prédictif qui n'existe pas. Publier les résultats négatifs, avec des contrôles de puissance, évite que la littérature ne retienne que les configurations qui semblent marcher.

**Pour les investisseurs.** Nos résultats ne donnent pas de raison d'utiliser l'exécution mensuelle du budget de l'État pour prévoir le spread, le taux OAT ou le CAC 40 à un mois. Ils n'indiquent pas que les finances publiques sont sans importance pour les marchés : l'information utile semble plutôt se trouver dans les annonces et les anticipations.

**Pour les producteurs de données ouvertes.** L'intérêt des situations budgétaires pour la recherche serait plus grand avec un calendrier de publication archivé et la conservation des versions successives des chiffres. Ces deux éléments permettraient de travailler avec l'information réellement disponible à chaque date.

## 4.7 Limites

### Limites des données

- **Données révisées.** Nous utilisons la dernière version publiée des situations budgétaires, et non les chiffres tels qu'ils étaient connus à chaque date. Les montants de décembre, en particulier, sont d'abord provisoires puis révisés.
- **Date de publication.** Le décalage de deux mois est vérifié sur 2023-2026 seulement ; pour 2014-2022, c'est une hypothèse. Les résultats ne changent pas avec un décalage d'un ou de trois mois (section 3.3).
- **Périmètre.** Les données couvrent le budget de l'État, pas la Sécurité sociale ni les collectivités locales. Elles ne sont pas ventilées par mission (défense, éducation, etc.).
- **Cibles de taux en moyennes mensuelles.** Le spread et le taux OAT sont des moyennes du mois (source OCDE), alors que le CAC 40 est pris en fin de mois. Les variations de moyennes sont légèrement autocorrélées de façon mécanique.
- **Variables budgétaires hétérogènes dans l'année.** L'écart cumulé depuis janvier varie beaucoup plus en fin d'année qu'en début d'année : en médiane, son écart-type en décembre est 6,3 fois celui de janvier.

### Limites de méthode

- **Petit échantillon.** Avec 70 à 148 mois d'entraînement et 79 mois de test, seul un effet fort pouvait être détecté (section 4.3). Les écarts de quelques points de R² entre deux modèles ne sont pas interprétables.
- **Hyperparamètres.** Ils ont été fixés à des valeurs usuelles, sans réglage sur la période de test. Mais le code et les résultats des modèles principaux ont été enregistrés en même temps : nous ne pouvons pas prouver qu'ils ont été choisis avant de voir les résultats. Seules les extensions ont un plan daté avant leur exécution.
- **Instabilité de XGBoost.** Son R² varie d'environ 9 points selon la graine aléatoire. Les conclusions ne changent pas, mais les chiffres précis dépendent aussi des versions des bibliothèques logicielles.
- **Extensions ajoutées en cours de route.** Toutes les extensions ont été définies après les résultats du modèle principal, mais datées avant leur exécution. E17 à E20 ont été ajoutées après avoir vu les résultats d'E15 et E16, et E18 est explicitement exploratoire. E14 (étude d'événement) n'a pas pu être réalisée.
- **Panel européen.** Pour E16, 25 des 68 séries de l'OCDE ne sont plus mises à jour depuis fin 2022 ou début 2024 ; environ 23 % des valeurs de la fin de la période de test sont donc complétées. Pour E19, les prix des actions n'incluent pas les dividendes.
- **Pas d'étude d'événement.** Faute de taux quotidiens accessibles, nous n'avons pas pu mesurer la réaction du marché le jour de chaque publication. L'explication « l'information est déjà connue » (section 4.2) reste donc une hypothèse.

## 4.8 Recherches futures

- **Étude d'événement.** Avec des taux quotidiens (Banque de France, Bundesbank) et les dates exactes de publication des situations budgétaires, on pourrait mesurer la réaction du spread le jour même. C'est le test direct de l'explication « l'information est déjà connue ». Garlanda-Longueville (2023) montre qu'une telle approche trouve des effets pour les annonces budgétaires.
- **Les annonces plutôt que l'exécution.** Le projet de loi de finances, les lois de finances rectificatives et les programmes de stabilité sont de l'information nouvelle pour les marchés. Ils pourraient être codés comme des surprises, par exemple l'écart entre le déficit annoncé et les prévisions des économistes.
- **Données en temps réel.** Conserver chaque version publiée des situations budgétaires permettrait de travailler avec l'information réellement disponible à chaque date.
- **Plus d'observations.** Un panel de pays plus long, incluant la crise de 2010-2012, avec des cibles de fin de période (et non des moyennes), augmenterait la puissance des tests.
- **Ventilation sectorielle.** Les données de la commande publique (marchés publics) permettraient de relier la dépense aux entreprises qui en bénéficient, et de mieux tester le canal des actions sectorielles (E19).

## Références ajoutées par ce chapitre

- Engle, R. F. (1982). Autoregressive conditional heteroscedasticity with estimates of the variance of United Kingdom inflation. *Econometrica*, 50(4), 987–1007.
- Working, H. (1960). Note on the correlation of first differences of averages in a random chain. *Econometrica*, 28(4), 916–918.
