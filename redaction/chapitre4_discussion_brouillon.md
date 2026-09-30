# Mémoire — Chapitre 4 : Discussion

Sep 30, 2026 · @elyamine

> **Statut : brouillon de travail, à réécrire par Elyamine.** Les idées viennent de nos discussions ; le guide ECE interdit de rendre des interprétations rédigées par l'IA sans relecture critique et apport personnel. Pour chaque paragraphe : garder, couper ou contredire, puis reformuler avec tes mots. Les chiffres, eux, sont vérifiés dans le dépôt.

## 4.1 Réponse à la problématique

Notre question était la suivante : peut-on prédire des indicateurs des marchés financiers à partir des données ouvertes de dépenses publiques, en utilisant le machine learning ?

Sur les données françaises, à un horizon d'un mois, la réponse est négative. Nous ne trouvons **aucune preuve** que les dépenses de l'État améliorent la prévision du spread OAT–Bund, du taux OAT ou du CAC 40. Ce résultat tient pour les trois modèles, pour les vingt extensions, avec un décalage de publication de un à trois mois, et après correction pour les tests multiples.

Cette réponse a une portée précise. Elle ne dit pas que les dépenses n'ont aucun lien avec les marchés. Elle dit que, si ce lien existe, il est trop faible pour être détecté avec 79 mois de test (section 4.3). Elle porte sur l'exécution mensuelle du budget de l'État, et non sur les annonces budgétaires ni sur l'ensemble des administrations publiques.

Un second constat dépasse la question des dépenses : **aucun modèle ne bat la moyenne historique**, même sans les dépenses. Pour les taux, la prévision la plus simple, « pas de variation le mois prochain », fait même mieux que la moyenne et que tous nos modèles. À un mois, ces marchés sont donc très difficiles à prévoir, quelles que soient les variables utilisées.

## 4.2 Pourquoi les dépenses n'aident pas : trois explications

Le chapitre 3 montre que les dépenses de l'État n'améliorent la prévision d'aucune des trois cibles. Nous proposons trois explications. Elles ne s'excluent pas.

### L'information est déjà connue au moment de la publication

Le budget de l'État est voté en décembre, dans la loi de finances de l'année suivante. Les marchés connaissent donc le plan de dépenses avant le début de l'année. De plus, les grandes lignes évoluent lentement : les dépenses de personnel ou la charge de la dette ne changent pas brutalement d'un mois à l'autre. Quand la situation mensuelle est publiée, deux mois plus tard, elle confirme surtout ce qui était attendu.

Or un prix de marché réagit à l'information nouvelle, pas à ce qui est déjà prévu (Fama, 1970). Ramey (2011) montre que, pour les dépenses publiques, ce qui compte est le moment de l'annonce, et non celui où l'argent est dépensé. L'extension E4 va dans ce sens : même l'écart entre l'exécution et le budget voté, qui mesure une forme de surprise, n'améliore pas la prévision. On retrouve la même idée chez Attinasi et al. (2009) : pendant la crise de 2007-2009, c'est l'annonce des plans de sauvetage bancaire qui a fait monter les spreads, et non le montant engagé.

Cette explication reste une hypothèse. Pour la démontrer, il faudrait observer le spread le jour même de chaque publication (étude d'événement). Cette étude n'a pas pu être réalisée, faute de taux quotidiens accessibles (section 4.6).

### Ce qui fait bouger le spread n'est pas budgétaire

Les plus fortes variations mensuelles du spread OAT–Bund correspondent à des chocs politiques ou mondiaux : mars 2020 (+20,5 pb, Covid), la période de l'élection présidentielle de 2017 (+16,3 pb en février, -18,1 pb en mai), juin 2024 (+15,5 pb, dissolution de l'Assemblée nationale). Ces mouvements s'expliquent par des événements identifiés, sans lien avec le contenu des situations budgétaires mensuelles. \[À vérifier avant la version finale : dates et sources de chaque événement.\]

Le cas de juin 2024 est intéressant. Il concerne bien les finances publiques, mais par un canal politique : la crainte qu'une nouvelle majorité ne tienne pas la trajectoire budgétaire. Cette crainte est une anticipation sur l'avenir ; elle n'apparaît dans aucune ligne de dépense déjà exécutée.

### Une variable lente pour une cible rapide

Les dépenses publiques évoluent sur plusieurs années. Le spread, le taux OAT et le CAC 40 réagissent en quelques jours. Nous cherchons donc à prévoir un mouvement rapide avec une information lente, et disponible avec deux mois de retard.

La littérature européenne trouve pourtant un lien entre finances publiques et spreads (Bernoth et al., 2012 ; Afonso et al., 2015). Ce n'est pas une contradiction : ces études **expliquent le niveau** des spreads, en coupe ou en panel, souvent sur des périodes de crise. Nous cherchons à **prévoir leur variation** le mois suivant, hors échantillon. Une variable peut expliquer un niveau sur dix ans sans aider à prévoir le mois prochain. Le panel annuel (E17) teste une fréquence plus basse ; il ne fait pas mieux, mais il ne compte que 75 prévisions.

Enfin, la France n'a pas connu de crise de la dette pendant notre période (2014-2026), contrairement à l'Italie ou à l'Espagne en 2011-2012. Il est possible que les dépenses ne comptent pour les marchés qu'en période de tension (Afonso et al., 2015). Le panel trimestriel allait dans ce sens (+4 points de R² en 2010-2014), mais l'écart n'est pas significatif (p = 0,36) et disparaît avec le spread de fin de trimestre (E18).

## 4.3 Ce que le résultat négatif veut dire, et ce qu'il ne veut pas dire

Un résultat négatif n'a de valeur que si l'on sait ce que le test aurait pu détecter. Trois contrôles permettent d'en juger.

### Ce que le test aurait trouvé : la puissance

Le contrôle positif (section 3.3) ajoute à M0 une variable fictive, construite pour être corrélée à la cible. Avec une corrélation de 0,5, le modèle bat la moyenne historique dans 80 à 100 % des tirages. Avec une corrélation de 0,3, il ne la bat que dans 20 à 30 % des tirages. Notre dispositif repère donc un signal fort, mais il manquerait souvent un signal modéré.

Cela définit la portée de notre conclusion : les dépenses n'ont pas un pouvoir prédictif fort ; un effet faible reste possible. La cause principale est la taille de l'échantillon : les séries budgétaires ouvertes commencent en 2013, ce qui laisse 79 mois de test. Ce n'est pas un choix de méthode, c'est une limite des données disponibles.

### Ce que fait du pur bruit : le contrôle négatif

Quand on remplace les sept dépenses par sept variables tirées au hasard, 90 à 95 % des tirages de bruit font au moins aussi bien que les vraies dépenses avec Ridge. Les petites différences entre M1 et M0 ne sont donc pas propres aux dépenses : n'importe quelles variables ajoutées produisent des écarts du même ordre.

Le même contrôle change la lecture de l'importance des variables. Les dépenses pèsent 31 à 37 % de l'importance SHAP, ce qui paraît beaucoup ; mais du bruit obtient 34 à 38 %. Une part d'importance élevée dans un modèle d'arbres ne montre donc pas qu'une variable est utile. C'est une leçon de méthode plus générale : sans comparaison à du bruit, les mesures d'importance peuvent tromper.

### Contre quoi comparer : le choix de la référence

Pour les taux, la prévision « pas de variation » bat la moyenne historique. La moyenne n'est donc pas la référence la plus exigeante. Le panel trimestriel (E15) montre un autre piège : un R² de +15 % venait du fait que la cible était une moyenne sur le trimestre, ce qui la rend en partie prévisible de façon mécanique (Working, 1960). Avec le spread de fin de trimestre, le R² devient négatif.

Ces trois points ont un même message : un bon score ne suffit pas. Il faut toujours le comparer à une référence simple et à du bruit, et vérifier que la cible ne contient pas une régularité mécanique.

## 4.4 Comparaison avec la littérature

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

Enfin, Garlanda-Longueville (2023) trouve un effet des annonces budgétaires françaises sur le spread, avec des données quotidiennes. Ce résultat est cohérent avec le nôtre : ce sont les annonces, observées au jour le jour, qui font bouger les marchés, et non l'exécution mensuelle publiée deux mois plus tard.

## 4.5 Limites

### Limites des données

- **Données révisées.** Nous utilisons la dernière version publiée des situations budgétaires, et non les chiffres tels qu'ils étaient connus à chaque date. Les montants de décembre, en particulier, sont d'abord provisoires puis révisés.
- **Date de publication.** Le décalage de deux mois est vérifié sur 2023-2026 seulement ; pour 2014-2019, c'est une hypothèse. Les résultats ne changent pas avec un décalage de un ou de trois mois (section 3.3).
- **Périmètre.** Les données couvrent le budget de l'État, pas la Sécurité sociale ni les collectivités locales. Elles ne sont pas ventilées par mission (défense, éducation, etc.).
- **Cibles de taux en moyennes mensuelles.** Le spread et le taux OAT sont des moyennes du mois (source OCDE), alors que le CAC 40 est pris en fin de mois. Les variations de moyennes sont légèrement autocorrélées de façon mécanique.
- **Variables budgétaires hétérogènes dans l'année.** L'écart cumulé depuis janvier varie beaucoup plus en fin d'année qu'en début d'année : en médiane, son écart-type en décembre est 6,3 fois celui de janvier.

### Limites de méthode

- **Petit échantillon.** Avec 70 à 148 mois d'entraînement et 79 mois de test, seul un effet fort pouvait être détecté (section 4.3). Les écarts de quelques points de R² entre deux modèles ne sont pas interprétables.
- **Hyperparamètres.** Ils ont été fixés à des valeurs usuelles, sans réglage sur la période de test. Mais le code et les résultats des modèles principaux ont été enregistrés en même temps : nous ne pouvons pas prouver qu'ils ont été choisis avant de voir les résultats. Seules les extensions ont un plan daté avant leur exécution.
- **Instabilité de XGBoost.** Son R² varie d'environ 9 points selon la graine aléatoire. Les conclusions ne changent pas, mais les chiffres précis dépendent aussi des versions des librairies.
- **Extensions ajoutées en cours de route.** Les extensions E15 à E20 ont été décidées après les premiers résultats, et E18 est explicitement exploratoire.
- **Panel européen.** Pour E16, 25 des 68 séries de l'OCDE ne sont plus mises à jour depuis fin 2022 ou début 2024 ; environ 23 % des valeurs de la fin de la période de test sont donc complétées. Pour E19, les prix des actions n'incluent pas les dividendes.
- **Pas d'étude d'événement.** Faute de taux quotidiens accessibles, nous n'avons pas pu mesurer la réaction du marché le jour de chaque publication. L'explication « l'information est déjà connue » (section 4.2) reste donc une hypothèse.

## 4.6 Recherches futures

- **Étude d'événement.** Avec des taux quotidiens (Banque de France, Bundesbank) et les dates exactes de publication des situations budgétaires, on pourrait mesurer la réaction du spread le jour même. C'est le test direct de l'explication « l'information est déjà connue ». Garlanda-Longueville (2023) montre qu'une telle approche trouve des effets pour les annonces budgétaires.
- **Les annonces plutôt que l'exécution.** Le projet de loi de finances, les lois de finances rectificatives et les programmes de stabilité sont de l'information nouvelle pour les marchés. Ils pourraient être codés comme des surprises, par exemple l'écart entre le déficit annoncé et les prévisions des économistes.
- **Données en temps réel.** Conserver chaque version publiée des situations budgétaires permettrait de travailler avec l'information réellement disponible à chaque date.
- **Plus d'observations.** Un panel de pays plus long, incluant la crise de 2010-2012, avec des cibles de fin de période (et non des moyennes), augmenterait la puissance des tests.
- **Ventilation sectorielle.** Les données de la commande publique (marchés publics) permettraient de relier la dépense aux entreprises qui en bénéficient, et de mieux tester le canal des actions sectorielles (E19).

## Références ajoutées par ce chapitre

- Working, H. (1960). Note on the correlation of first differences of averages in a random chain. *Econometrica*, 28(4), 916–918.
