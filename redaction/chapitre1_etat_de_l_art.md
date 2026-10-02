# Mémoire — Chapitre 1 : État de l'art

Sep 29, 2026 · @elyamine

## Introduction du chapitre

Ce chapitre fait le point sur ce que l'on sait déjà. Il part d'une question simple : quelqu'un a-t-il déjà utilisé les données ouvertes de dépenses de l'État français, avec du machine learning, pour prévoir les marchés financiers ? À notre connaissance, non. Les sections qui suivent expliquent pourquoi ce vide existe et pourquoi il vaut la peine d'être exploré.

Nous étudions trois indicateurs, plus ou moins liés aux finances publiques :

- **Le spread OAT-Bund à 10 ans** : l'écart entre le taux auquel la France emprunte sur dix ans (OAT, Obligation assimilable du Trésor) et celui de l'Allemagne (Bund). Comme la politique monétaire est la même pour les deux pays, cet écart mesure surtout le risque propre à la France.
- **Le taux OAT à 10 ans** : le coût d'emprunt de l'État français. Il dépend à la fois des finances publiques et de la politique de la BCE.
- **Le rendement mensuel du CAC 40** : l'évolution de la valeur des grandes entreprises cotées à Paris.

Ces trois indicateurs vont du plus exposé au moins exposé aux finances publiques. Les comparer permet de voir où les dépenses apportent, ou non, de l'information.

Notre terrain est la France, dans la zone euro. Nous donnons donc la priorité aux études européennes. Les grands travaux américains restent utiles, mais surtout comme cadre théorique ou comme référence de méthode : nous les présentons plus brièvement.

La section 1.1 pose le cadre théorique. La section 1.2 présente les travaux européens sur le lien entre finances publiques et spreads. La section 1.3 porte sur le machine learning appliqué à la prévision des spreads. La section 1.4, plus courte, traite des données ouvertes et des précautions de méthode. La section 1.5 fait la synthèse et formule nos hypothèses.

## 1.1 Cadre théorique : ce que l'on peut attendre

La théorie ne promet pas grand-chose à une prévision fondée sur des données budgétaires publiques. Trois travaux, généraux même s'ils portent surtout sur les États-Unis, en donnent les raisons.

### 1.1.1 Dépenses publiques et taux : deux visions

Dans la vision keynésienne, une hausse des dépenses financée par l'emprunt augmente la demande de fonds et fait monter les taux d'intérêt. Elle peut alors évincer une partie de l'investissement privé. À l'inverse, l'équivalence ricardienne de Barro (1974) suppose que les ménages anticipent les impôts futurs et épargnent davantage, ce qui annule l'effet sur les taux. La théorie ne tranche donc pas : la question est empirique.

### 1.1.2 L'efficience des marchés (Fama, 1970)

Selon l'hypothèse d'efficience, dans sa forme semi-forte, les prix reflètent déjà toute l'information publique. Aucune donnée publique ne devrait alors permettre de prévoir de façon régulière les variations des prix.

Cela nous concerne directement. Les situations budgétaires de l'État sont publiques. Si le marché obligataire est efficient, elles sont intégrées dans le spread dès leur publication, et elles ne servent plus à prévoir le mois suivant.

### 1.1.3 Les dépenses sont anticipées (Ramey, 2011)

Ramey montre que les chocs de dépenses publiques mesurés par les modèles classiques sont en partie connus à l'avance. Une dépense est annoncée, votée, puis exécutée des mois plus tard. La mesurer au moment de l'exécution, c'est la mesurer trop tard.

C'est exactement le type de données que nous utilisons : l'exécution mensuelle du budget. Si les marchés réagissent aux annonces, ces données apportent peu d'information nouvelle. Ramey nous donne donc une raison claire de s'attendre à un pouvoir prédictif faible.

### 1.1.4 Peu de prédicteurs résistent hors échantillon (Welch et Goyal, 2008)

Welch et Goyal testent les variables les plus connues pour prévoir le rendement des actions. La plupart semblent fonctionner sur les données qui ont servi à les estimer. Mais sur des données nouvelles, elles font rarement mieux qu'une simple moyenne historique. Campbell et Thompson (2008) nuancent ce constat : avec quelques contraintes de bon sens, certains prédicteurs battent légèrement la moyenne, et même un petit gain peut avoir de la valeur.

### 1.1.5 Ce que nous en retenons

Un pouvoir prédictif faible, voire nul, est donc plausible dès le départ, et un résultat négatif serait cohérent avec Fama et Ramey. Il faudra évaluer les modèles hors échantillon, sur des mois qu'ils n'ont jamais vus, et les comparer à une référence simple : la moyenne historique et, pour les taux, la variation nulle. Un modèle qui ne la bat pas n'a pas de pouvoir prédictif utile.

## 1.2 Finances publiques et spreads souverains en zone euro

En Europe, plusieurs travaux montrent que les finances publiques expliquent une partie des spreads face à l'Allemagne. Mais ils cherchent à expliquer, pas à prévoir, et l'effet change beaucoup selon les périodes.

### 1.2.1 Pourquoi le spread

Dans une union monétaire, tous les pays ont la même banque centrale. L'écart de taux avec l'Allemagne reflète donc surtout ce qui est propre à chaque État : son risque de crédit et la liquidité de sa dette. C'est pour cela que le spread est la variable la plus logique pour mesurer l'effet des finances publiques d'un pays de la zone euro.

### 1.2.2 Ce que montrent les travaux européens

Bernoth, von Hagen et Schuknecht (2012) étudient les spreads des obligations européennes face à l'Allemagne. La dette, le déficit et la charge de la dette en expliquent une partie, y compris après l'entrée dans l'euro. L'aversion au risque mondiale renforce cet effet.

Attinasi, Checherita et Nickel (2009) cherchent ce qui a fait monter les spreads pendant la crise, de fin juillet 2007 à fin mars 2009. Ils trouvent trois moteurs : l'aversion au risque internationale, la liquidité des marchés obligataires et les positions budgétaires attendues. Les annonces de plans de sauvetage bancaire ont aussi pesé. Pour nous, ce qui compte, c'est que l'annonce elle-même a compté, et non le montant engagé, dont l'effet n'est pas significatif.

Afonso, Arghyrou et Kontonikas (2015) couvrent la zone euro de 1999 à 2010. Les marchés tiennent compte des déficits attendus sur toute la période, mais les sanctionnent beaucoup plus fort après mars 2009. La dette, elle, ne compte vraiment qu'à partir de la crise des dettes souveraines. L'effet des finances publiques sur les spreads n'est donc pas stable dans le temps : il apparaît surtout en période de tension.

Favero (2013) est l'un des rares à prévoir les spreads, et non seulement à les expliquer. Avec un modèle économétrique (un VAR global), il fait dépendre le spread de chaque pays de ceux des autres, pondérés selon la ressemblance de leurs finances publiques. Son modèle prévoit mieux, hors échantillon, que les spécifications classiques.

### 1.2.3 Le cas français

Les études consacrées à la France sont rares. Garlanda-Longueville (2023) consacre un chapitre de sa thèse aux allocutions du président de la République pendant la crise du Covid (mars 2020 à décembre 2021), qui contenaient des engagements budgétaires. Avec des données quotidiennes, elle montre que ces annonces ont en général fait monter le CAC 40 et baisser le spread France–Allemagne. Les communiqués annonçant à l'avance une allocution ont un effet plus significatif que l'allocution elle-même. Ce résultat va dans le sens de Ramey (2011) : le marché réagit aux annonces.

L'actualité récente le confirme. Après la dissolution de l'Assemblée nationale en juin 2024, l'incertitude sur la trajectoire budgétaire a nettement élargi le spread OAT-Bund : dans nos données, sa moyenne mensuelle augmente de 15,5 points de base en juin 2024, l'une des plus fortes hausses de la période.

### 1.2.4 Les travaux fondateurs, surtout américains

Ces travaux européens s'appuient sur une littérature plus ancienne, surtout américaine, que nous résumons brièvement. Blanchard et Perotti (2002) proposent une méthode de référence pour isoler les chocs budgétaires, et trouvent qu'une hausse des dépenses réduit l'investissement privé. Laubach (2009) estime qu'un point de PIB de déficit prévu en plus fait monter les taux longs américains d'environ 25 points de base. Afonso et Sousa (2011) montrent que les chocs de dépenses pèsent sur le prix des actions, et Ardagna (2009) que les fortes consolidations budgétaires dans l'OCDE s'accompagnent d'une baisse des taux et d'une hausse des actions.

### 1.2.5 Ce que nous en retenons

Le spread OAT-Bund est la cible la plus directement liée aux finances publiques françaises. L'aversion au risque et la liquidité comptent beaucoup, et doivent donc figurer dans le modèle comme variables de contrôle. Comme l'effet des finances publiques dépend de la période, il faudra regarder séparément les périodes calmes et les périodes agitées. Enfin, presque tous ces travaux utilisent des modèles linéaires et des données annuelles ou trimestrielles, et cherchent à expliquer plutôt qu'à prévoir. Aucun ne teste le machine learning sur des données budgétaires mensuelles.

## 1.3 Machine learning et prévision des spreads

Le machine learning améliore souvent les prévisions financières, surtout quand les relations entre variables ne sont pas linéaires. Appliqué aux spreads européens, il donne de bons résultats. Mais dans ces travaux, c'est surtout le passé du spread qui fait le travail, et l'apport des finances publiques n'est jamais isolé.

### 1.3.1 Les travaux européens

Belly et al. (2023) utilisent le machine learning pour évaluer le risque souverain de dix pays de la zone euro, sur des données mensuelles de 2004 à 2019, en niveau et en variation mensuelle. Leurs méthodes suivent la dynamique des spreads bien mieux que les modèles économétriques habituels. Le sentiment des actualités financières, le risque de sortie de l'euro et la communication de la BCE ressortent comme des déterminants importants.

Bouillot, Candelon et Kool (2025) sont les plus proches de notre travail. Ils prévoient à un mois le spread à 10 ans face au Bund de dix pays de la zone euro, dont la France, sur des données mensuelles de décembre 2008 à février 2025. Ils comparent treize méthodes sur près de 5 000 variables (4 948 séries), dont des variables de finances publiques. XGBoost donne les meilleures prévisions : sur 2020-2025, son erreur (RMSE) est de 4 à 8 points de base pour les pays du cœur de la zone euro, et de 7,3 points de base pour la France. La cible est le niveau du spread. Dans la version du document de travail que nous avons consultée, les modèles sont comparés entre eux, à la moyenne et à des régressions linéaires, mais pas à la prévision naïve « spread du mois précédent ». Le résumé d'une version plus récente indique que l'AR(1) et la marche aléatoire ont des erreurs plus faibles que les modèles de machine learning dans chaque pays, quand les modèles sont réestimés à chaque date.

Deux de leurs résultats comptent pour nous. D'abord, c'est le spread passé qui domine les prévisions, complété par les conditions financières, les prix et les indicateurs de marché mondiaux. Les finances publiques y pèsent très peu : parmi les cinq variables les plus importantes de chacun des dix pays (50 au total), une seule relève des finances publiques. Ensuite, la France et la Belgique se détachent des autres pays du cœur de la zone euro à partir de mi-2024.

Enfin, Barbier-Gauchard et Sofianos (2025) appliquent le machine learning aux finances publiques elles-mêmes. Ils prévoient la dette publique de 17 pays de la zone euro, et XGBoost y fait mieux que les projections de la Commission européenne et du FMI.

### 1.3.2 Le contexte américain, en bref

Ces travaux européens suivent une littérature américaine plus large. Gu, Kelly et Xiu (2020) montrent que les arbres de décision et les réseaux de neurones prévoient mieux les rendements des actions que les modèles linéaires, grâce aux effets non linéaires. Bianchi, Büchner et Tamoni (2021) trouvent le même type de gain pour les obligations d'État. En macroéconomie, Medeiros et al. (2021) trouvent que la forêt aléatoire domine les autres modèles pour prévoir l'inflation américaine, et Goulet Coulombe et al. (2022) que les gains du machine learning sur les variables macroéconomiques viennent surtout de la non-linéarité, plus utile en période d'incertitude ou de tension financière.

### 1.3.3 Quels modèles avec peu de données

Les modèles à base d'arbres, comme les forêts aléatoires (Breiman, 2001) et XGBoost (Chen et Guestrin, 2016), fonctionnent bien sur des tableaux de données de taille moyenne. Le deep learning demande beaucoup plus d'observations : Fischer et Krauss (2018) obtiennent de bons résultats avec des réseaux LSTM, mais sur des données quotidiennes de centaines d'actions pendant plus de vingt ans. Avec environ 150 mois, un tel modèle apprendrait surtout le bruit.

### 1.3.4 Ce que nous en retenons

Le machine learning doit être comparé à des références simples : la moyenne historique, la variation nulle et un modèle linéaire. Le spread passé, qui est le principal prédicteur chez Bouillot et al., doit figurer dans tous les modèles, sinon on attribuerait aux dépenses ce qui vient en réalité du spread lui-même. La forêt aléatoire et XGBoost conviennent à notre volume de données, pas le deep learning. Enfin, aucun de ces travaux ne mesure séparément ce qu'apportent les dépenses publiques, et c'est la question précise de ce mémoire.

## 1.4 Données ouvertes et précautions de méthode

Les données publiques ouvertes sont gratuites, officielles et régulières. Pour la prévision, elles posent pourtant trois problèmes : le délai de publication, les révisions et la forme des données.

### 1.4.1 Les données budgétaires ouvertes

Janssen, Charalabidis et Zuiderwijk (2012) rappellent que publier des données ne suffit pas à ce qu'elles soient utilisées : leur qualité, leur format et leur documentation comptent autant. En France, la loi pour une République numérique de 2016 fait de l'ouverture des données publiques la règle. Le ministère de l'Économie diffuse ainsi, sur data.economie.gouv.fr, la situation mensuelle budgétaire de l'État en séries longues depuis 2013 : dépenses par titre, recettes et solde.

Cette source a trois particularités. Les montants sont cumulés depuis janvier. Ils sont très saisonniers, par exemple l'impôt sur les sociétés, concentré sur quelques échéances. Et la situation d'un mois M ne paraît qu'au début du mois M+2 : celle de juin 2026 a été publiée le 4 août 2026.

### 1.4.2 Calendrier de publication et révisions

Giannone, Reichlin et Small (2008) montrent qu'une donnée n'apporte de l'information qu'à partir du moment où elle est publiée : son calendrier compte autant que son contenu. Croushore (2011) ajoute que beaucoup de données sont révisées après leur première publication. Évaluer un modèle avec les chiffres définitifs surestime donc ses performances, puisque le prévisionniste n'avait que les chiffres provisoires. La situation budgétaire est concernée : le mois de décembre paraît d'abord en version provisoire.

Aux États-Unis, McCracken et Ng (2016) ont construit FRED-MD, une base mensuelle de plus d'une centaine d'indicateurs macroéconomiques. Il n'existe pas d'équivalent français qui intègre l'exécution budgétaire.

### 1.4.3 Éviter de se tromper soi-même

Bailey et al. (2014) mettent en garde contre un piège fréquent : à force de tester des configurations sur les mêmes données, on finit toujours par en trouver une qui semble marcher, par hasard. Pour des séries temporelles, il faut aussi une validation glissante, où le modèle n'apprend que sur le passé. Enfin, un petit écart d'erreur entre deux modèles peut être dû au hasard : le test de Diebold et Mariano (1995) permet de le vérifier.

### 1.4.4 Ce que nous en retenons

Les données budgétaires d'un mois ne peuvent servir qu'après leur publication, nous les décalons donc de deux mois. Les montants cumulés doivent être transformés pour enlever la saisonnalité, et les révisions seront discutées comme une limite. Construire un jeu de données mensuel français qui croise budget et marchés est déjà, en soi, une contribution.

## 1.5 Synthèse et positionnement du mémoire

À notre connaissance, aucun travail ne prévoit des indicateurs des marchés financiers français à partir des données ouvertes de dépenses publiques mensuelles avec du machine learning. Le tableau 1.1 résume les travaux clés, classés selon leur rôle dans ce mémoire.

**Tableau 1.1 : Principaux travaux recensés**

| Rôle | Auteurs (année) | Pays et données | Méthode | Résultat principal | Limite pour ce mémoire |
| --- | --- | --- | --- | --- | --- |
| Noyau européen | Bouillot, Candelon et Kool (2025) | 10 pays de la zone euro dont la France ; mensuel, 2008-2025 | 13 méthodes de ML, XGBoost en tête | Prévision à un mois ; le spread passé domine | Apport des finances publiques non isolé (1 des 50 variables principales) ; cible en niveau, sans comparaison à la marche aléatoire dans la version consultée |
| Noyau européen | Belly et al. (2023) | 10 pays de la zone euro ; mensuel, 2004-2019 | ML contre économétrie | Le ML suit mieux la dynamique des spreads | Pas centré sur les dépenses |
| Noyau européen | Favero (2013) | Zone euro ; spreads | VAR global | Meilleure prévision hors échantillon que les modèles classiques | Linéaire, pas de données d'exécution |
| Noyau européen | Afonso, Arghyrou et Kontonikas (2015) | Zone euro, 1999-2010 | Panel | Déficits attendus sanctionnés ; dette prise en compte seulement après 2009 | Explique, ne prévoit pas |
| Noyau européen | Bernoth, von Hagen et Schuknecht (2012) | Europe ; spreads face à l'Allemagne | Panel | Dette et déficit expliquent une partie des spreads | Linéaire, données annuelles |
| Noyau européen | Attinasi, Checherita et Nickel (2009) | Zone euro, 2007-2009 | Panel dynamique | Risque, liquidité, positions budgétaires attendues et annonces de sauvetage bancaire expliquent les spreads | Période de crise seulement |
| Noyau européen | Garlanda-Longueville (2023) | France ; annonces du Covid | Étude d'événements | Les annonces du président de la République font en général monter les actions et baisser le spread | Annonces, pas dépenses exécutées |
| Noyau européen | Barbier-Gauchard et Sofianos (2025) | 17 pays de la zone euro ; dette publique | ML (XGBoost) | Prévoit mieux la dette que la Commission et le FMI | Cible budgétaire, pas financière |
| Cadre théorique | Fama (1970) | Général (études surtout américaines) | Synthèse théorique et empirique | Les prix intègrent l'information publique | Ne porte pas sur les données budgétaires |
| Cadre théorique | Ramey (2011) | États-Unis ; trimestriel | VAR, chocs narratifs | Les chocs de dépenses sont anticipés | Explique, ne prévoit pas |
| Cadre théorique | Welch et Goyal (2008) | États-Unis ; actions | Régressions hors échantillon | Peu de prédicteurs battent la moyenne historique | Pas de ML, pas d'obligations |
| Méthode | Gu, Kelly et Xiu (2020) | États-Unis ; actions | ML (arbres, réseaux de neurones) | Gain grâce à la non-linéarité | Pas de variables budgétaires |
| Méthode | Bianchi, Büchner et Tamoni (2021) | États-Unis ; obligations d'État | ML, variables macroéconomiques | Meilleure prévision des rendements obligataires | Pas de données budgétaires, pas la France |
| Méthode | Giannone, Reichlin et Small (2008) | États-Unis ; mensuel | Modèle à facteurs | Le calendrier de publication fixe la valeur d'une donnée | Cible : le PIB |
| Méthode | Croushore (2011) | États-Unis ; données en temps réel | Synthèse | Les révisions faussent l'évaluation des modèles | Pas de marchés financiers |

*Source : élaboration de l'auteur.*

### 1.5.1 Le vide identifié

La littérature se partage en deux blocs qui se croisent peu :

- **Le bloc macro-budgétaire** relie finances publiques et taux souverains. Il utilise des modèles linéaires et des données annuelles ou trimestrielles, et il cherche à expliquer plutôt qu'à prévoir.
- **Le bloc machine learning** montre des gains de prévision sur les marchés financiers. Mais il n'utilise pas les données d'exécution budgétaire.

Un troisième constat s'ajoute : la France est peu étudiée. Six des quinze travaux du tableau portent uniquement sur les États-Unis. Un seul, Garlanda-Longueville (2023), se concentre sur la France, et il porte sur les annonces, pas sur les dépenses exécutées. Même Bouillot et al. (2025) traitent la France comme un pays parmi dix. Pourtant, la question budgétaire française est devenue centrale pour les marchés : la note de la France a été abaissée cinq fois par les agences entre 2023 et 2025. Et ses données d'exécution budgétaire sont disponibles en séries longues ouvertes.

Bouillot, Candelon et Kool (2025) commencent à rapprocher les deux blocs. Notre travail s'en distingue sur trois points :

- **Nous isolons l'apport des dépenses publiques.** Chez eux, les finances publiques sont mêlées à près de 5 000 variables. Ici, nous comparons explicitement le même modèle avec et sans dépenses.
- **Nous utilisons les données détaillées d'exécution du budget français**, par catégorie de dépense, en données ouvertes.
- **Nous comparons trois indicateurs** plus ou moins exposés au risque souverain : le spread, le taux OAT et le CAC 40.

### 1.5.2 Problématique et hypothèses

Notre problématique est la suivante : peut-on prédire des indicateurs des marchés financiers à partir des données de dépenses publiques ouvertes en utilisant des techniques de machine learning ?

Concrètement, nous testons si les dépenses de l'État améliorent la prévision mensuelle de trois indicateurs : la variation du spread OAT-Bund à 10 ans, la variation du taux OAT à 10 ans et le rendement du CAC 40. L'apport est mesuré par rapport à des modèles qui n'utilisent que des variables de marché et macroéconomiques.

Nous formulons quatre hypothèses :

- **H1.** Pour au moins un des trois indicateurs, un modèle qui intègre les dépenses publiques prévoit mieux qu'un modèle qui n'utilise que les variables de contrôle.
- **H2.** L'apport des dépenses diminue du spread au taux OAT, puis au CAC 40, à mesure que l'indicateur est moins exposé au risque souverain.
- **H3.** Les modèles de machine learning (forêt aléatoire, XGBoost) prévoient mieux que les modèles linéaires.
- **H4.** Parmi les dépenses, la charge de la dette et les dépenses d'intervention sont les plus prédictives.

En suivant Fama (1970) et Ramey (2011), un rejet de H1 reste un résultat plausible, et il nous apprendrait quelque chose.

## Références bibliographiques

Format APA. Volumes et pages à vérifier sur Google Scholar avant le dépôt.

- Afonso, A., Arghyrou, M. G., & Kontonikas, A. (2015). *[The determinants of sovereign bond yield spreads in the EMU](https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp1781.en.pdf)*. ECB Working Paper No. 1781.
- Afonso, A., & Sousa, R. M. (2011). What are the effects of fiscal policy on asset markets? *Economic Modelling*, 28(4), 1871–1890. [https://doi.org/10.1016/j.econmod.2011.03.018](https://doi.org/10.1016/j.econmod.2011.03.018)
- Ardagna, S. (2009). Financial markets' behavior around episodes of large changes in the fiscal stance. *European Economic Review*, 53(1), 37–55. [https://doi.org/10.1016/j.euroecorev.2008.07.003](https://doi.org/10.1016/j.euroecorev.2008.07.003)
- Attinasi, M.-G., Checherita, C., & Nickel, C. (2009). *What explains the surge in euro area sovereign spreads during the financial crisis of 2007-09?* ECB Working Paper No. 1131. [https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp1131.pdf](https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp1131.pdf)
- Bailey, D. H., Borwein, J. M., López de Prado, M., & Zhu, Q. J. (2014). Pseudo-mathematics and financial charlatanism: The effects of backtest overfitting on out-of-sample performance. *Notices of the American Mathematical Society*, 61(5), 458–471. [https://doi.org/10.1090/noti1105](https://doi.org/10.1090/noti1105)
- Barbier-Gauchard, A., & Sofianos, E. (2025). [Forecasting public debt in the euro area using machine learning: Decision tools for financial markets](https://link.springer.com/article/10.1007/s10614-025-11106-9). *Computational Economics*. https://doi.org/10.1007/s10614-025-11106-9
- Barro, R. J. (1974). Are government bonds net wealth? *Journal of Political Economy*, 82(6), 1095–1117. [https://doi.org/10.1086/260266](https://doi.org/10.1086/260266)
- Belly, G., Boeckelmann, L., Caicedo Graciano, C. M., Di Iorio, A., Istrefi, K., Siakoulis, V., & Stalla-Bourdillon, A. (2023). [Forecasting sovereign risk in the Euro area via machine learning](https://ideas.repec.org/a/wly/jforec/v42y2023i3p657-684.html). *Journal of Forecasting*, 42(3), 657–684. [https://doi.org/10.1002/for.2938](https://doi.org/10.1002/for.2938)
- Bernoth, K., von Hagen, J., & Schuknecht, L. (2012). Sovereign risk premiums in the European government bond market. *Journal of International Money and Finance*, 31(5), 975–995. [https://doi.org/10.1016/j.jimonfin.2011.12.006](https://doi.org/10.1016/j.jimonfin.2011.12.006)
- Bianchi, D., Büchner, M., & Tamoni, A. (2021). [Bond risk premiums with machine learning](https://academic.oup.com/rfs/article-abstract/34/2/1046/5843806). *The Review of Financial Studies*, 34(2), 1046–1089. [https://doi.org/10.1093/rfs/hhaa062](https://doi.org/10.1093/rfs/hhaa062)
- Blanchard, O., & Perotti, R. (2002). An empirical characterization of the dynamic effects of changes in government spending and taxes on output. *The Quarterly Journal of Economics*, 117(4), 1329–1368. [https://doi.org/10.1162/003355302320935043](https://doi.org/10.1162/003355302320935043)
- Bouillot, R., Candelon, B., & Kool, C. (2025). *[Forecasting European sovereign spreads using machine learning](https://research.dial.uclouvain.be/server/api/core/bitstreams/f99c9d92-b208-429f-84ec-256595aa55a5/content)*. LIDAM Discussion Paper LFIN 2025/04, UCLouvain.
- Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5–32. [https://doi.org/10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324)
- Campbell, J. Y., & Thompson, S. B. (2008). Predicting excess stock returns out of sample: Can anything beat the historical average? *The Review of Financial Studies*, 21(4), 1509–1531. [https://doi.org/10.1093/rfs/hhm055](https://doi.org/10.1093/rfs/hhm055)
- Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 785–794. [https://doi.org/10.1145/2939672.2939785](https://doi.org/10.1145/2939672.2939785)
- Croushore, D. (2011). Frontiers of real-time data analysis. *Journal of Economic Literature*, 49(1), 72–100. [https://doi.org/10.1257/jel.49.1.72](https://doi.org/10.1257/jel.49.1.72)
- Diebold, F. X., & Mariano, R. S. (1995). Comparing predictive accuracy. *Journal of Business & Economic Statistics*, 13(3), 253–263. [https://doi.org/10.1080/07350015.1995.10524599](https://doi.org/10.1080/07350015.1995.10524599)
- Fama, E. F. (1970). Efficient capital markets: A review of theory and empirical work. *The Journal of Finance*, 25(2), 383–417. [https://doi.org/10.1111/j.1540-6261.1970.tb00518.x](https://doi.org/10.1111/j.1540-6261.1970.tb00518.x)
- Favero, C. A. (2013). [Modelling and forecasting government bond spreads in the euro area: A GVAR model](https://www.sciencedirect.com/science/article/abs/pii/S030440761300081X). *Journal of Econometrics*, 177(2), 343–356. [https://doi.org/10.1016/j.jeconom.2013.04.004](https://doi.org/10.1016/j.jeconom.2013.04.004)
- Fischer, T., & Krauss, C. (2018). Deep learning with long short-term memory networks for financial market predictions. *European Journal of Operational Research*, 270(2), 654–669. [https://doi.org/10.1016/j.ejor.2017.11.054](https://doi.org/10.1016/j.ejor.2017.11.054)
- Garlanda-Longueville, L. (2023). *[Fiscalité bancaire, politique monétaire et annonces budgétaires : trois essais en économie bancaire et financière internationale](https://theses.fr/2023PA100145)* \[Thèse de doctorat, Université Paris Nanterre, dir. V. Mignon\].
- Giannone, D., Reichlin, L., & Small, D. (2008). Nowcasting: The real-time informational content of macroeconomic data. *Journal of Monetary Economics*, 55(4), 665–676. [https://doi.org/10.1016/j.jmoneco.2008.05.010](https://doi.org/10.1016/j.jmoneco.2008.05.010)
- Goulet Coulombe, P., Leroux, M., Stevanovic, D., & Surprenant, S. (2022). How is machine learning useful for macroeconomic forecasting? *Journal of Applied Econometrics*, 37(5), 920–964. [https://doi.org/10.1002/jae.2910](https://doi.org/10.1002/jae.2910)
- Gu, S., Kelly, B., & Xiu, D. (2020). Empirical asset pricing via machine learning. *The Review of Financial Studies*, 33(5), 2223–2273. [https://doi.org/10.1093/rfs/hhaa009](https://doi.org/10.1093/rfs/hhaa009)
- Janssen, M., Charalabidis, Y., & Zuiderwijk, A. (2012). Benefits, adoption barriers and myths of open data and open government. *Information Systems Management*, 29(4), 258–268. [https://doi.org/10.1080/10580530.2012.716740](https://doi.org/10.1080/10580530.2012.716740)
- Laubach, T. (2009). New evidence on the interest rate effects of budget deficits and debt. *Journal of the European Economic Association*, 7(4), 858–885. [https://doi.org/10.1162/jeea.2009.7.4.858](https://doi.org/10.1162/jeea.2009.7.4.858)
- McCracken, M. W., & Ng, S. (2016). FRED-MD: A monthly database for macroeconomic research. *Journal of Business & Economic Statistics*, 34(4), 574–589. [https://doi.org/10.1080/07350015.2015.1086655](https://doi.org/10.1080/07350015.2015.1086655)
- Medeiros, M. C., Vasconcelos, G. F. R., Veiga, Á., & Zilberman, E. (2021). Forecasting inflation in a data-rich environment: The benefits of machine learning methods. *Journal of Business & Economic Statistics*, 39(1), 98–119. [https://doi.org/10.1080/07350015.2019.1637745](https://doi.org/10.1080/07350015.2019.1637745)
- Ramey, V. A. (2011). Identifying government spending shocks: It's all in the timing. *The Quarterly Journal of Economics*, 126(1), 1–50. [https://doi.org/10.1093/qje/qjq008](https://doi.org/10.1093/qje/qjq008)
- Welch, I., & Goyal, A. (2008). A comprehensive look at the empirical performance of equity premium prediction. *The Review of Financial Studies*, 21(4), 1455–1508. [https://doi.org/10.1093/rfs/hhm014](https://doi.org/10.1093/rfs/hhm014)

### Sources en ligne

- Ministère de l'Économie. [Situations mensuelles budgétaires de l'État, séries longues depuis 2013](https://data.economie.gouv.fr/explore/assets/situations-mensuelles-budgetaires-series-longues/). data.economie.gouv.fr.
- DGFiP. [La situation mensuelle de l'État](https://www.economie.gouv.fr/dgfip/la-situation-mensuelle-de-letat). economie.gouv.fr.
