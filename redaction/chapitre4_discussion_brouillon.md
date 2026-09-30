# Mémoire — Chapitre 4 : Discussion

Sep 30, 2026 · @elyamine

> **Statut : brouillon de travail, à réécrire par Elyamine.** Les idées viennent de nos discussions ; le guide ECE interdit de rendre des interprétations rédigées par l'IA sans relecture critique et apport personnel. Pour chaque paragraphe : garder, couper ou contredire, puis reformuler avec tes mots. Les chiffres, eux, sont vérifiés dans le dépôt.

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
