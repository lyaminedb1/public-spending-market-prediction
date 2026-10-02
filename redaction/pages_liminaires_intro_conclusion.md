# Mémoire — Pages liminaires, introduction et conclusion

Sep 30, 2026 · @elyamine

## Page de titre

Prédiction d'indicateurs des marchés financiers à partir des données de dépenses publiques ouvertes : une approche par machine learning

Abdellah Elyamine DALI BRAHAM

ECE Paris, MSc Data Management & Intelligence Artificielle

Mémoire de fin d'études

Encadrante : Dr Yosra Hajjaji

Octobre 2026

## Remerciements

Je remercie d'abord ma famille, qui m'a accompagné et soutenu tout au long de ma vie et de mes études, de l'Algérie jusqu'à Paris. Ce mémoire leur doit beaucoup.

Je remercie également mon encadrante, Dr Yosra Hajjaji, pour son suivi et ses conseils, ainsi que l'équipe pédagogique du MSc Data Management & Intelligence Artificielle de l'ECE Paris.

## Déclaration d'utilisation de l'intelligence artificielle

Conformément au guide de rédaction de l'ECE, je déclare avoir utilisé un outil d'intelligence artificielle générative (Claude, d'Anthropic) comme assistant pour la programmation, la relecture du code et la rédaction. Le choix du sujet, de la problématique et du périmètre et les décisions de méthode relèvent de l'auteur, qui a relu l'ensemble du texte et en assume la responsabilité. Les chiffres cités ont été vérifiés sur les fichiers de résultats.

## Résumé

Ce mémoire cherche à savoir si les données ouvertes de dépenses publiques permettent de prévoir les marchés financiers. Nous utilisons les situations mensuelles budgétaires de l'État français (2013-2026), en tenant compte de leur délai de publication de deux mois, pour prévoir le mois suivant trois indicateurs : la variation du spread OAT-Bund à 10 ans, la variation du taux OAT à 10 ans et le rendement du CAC 40. Nous comparons un modèle qui n'utilise que des variables de marché et macroéconomiques à un modèle qui ajoute les dépenses, avec trois méthodes (régression Ridge, forêt aléatoire, XGBoost), une validation glissante et des tests de Diebold-Mariano. Dix-neuf extensions, dont un panel de cinq pays européens, complètent l'analyse.

Nous ne trouvons aucune preuve que les dépenses améliorent la prévision : aucune des 168 comparaisons n'est significative après correction pour tests multiples. Aucun modèle ne bat la moyenne historique, et pour les taux, la prévision « pas de variation » fait mieux que tous les modèles, même si l'écart est rarement significatif. Des contrôles avec un signal fictif et avec des variables de bruit montrent que notre dispositif aurait le plus souvent détecté un effet fort, mais pas forcément un effet faible. Enfin, nous montrons qu'un R² très élevé sur le niveau du spread, comme dans la littérature récente, ne suffit pas : les modèles perdent face à la simple reconduction du spread du mois précédent.

Mots-clés : dépenses publiques, données ouvertes, spread souverain, prévision, machine learning, validation glissante, marchés efficients.

## Liste des abréviations

| Abréviation | Signification |
| --- | --- |
| ACP | Analyse en composantes principales |
| ADF | Test de Dickey-Fuller augmenté |
| BCE | Banque centrale européenne |
| BH | Correction de Benjamini-Hochberg |
| BTP | Bâtiment et travaux publics |
| CAC 40 | Indice des 40 principales capitalisations de la Bourse de Paris |
| DGFiP | Direction générale des Finances publiques |
| DM | Test de Diebold-Mariano |
| EPU | Economic Policy Uncertainty (indice d'incertitude de politique économique) |
| FMI | Fonds monétaire international |
| FRED | Base de données de la Federal Reserve Bank of St. Louis |
| HLN | Correction de Harvey, Leybourne et Newbold du test DM |
| IA | Intelligence artificielle |
| INSEE | Institut national de la statistique et des études économiques |
| IPCH | Indice des prix à la consommation harmonisé |
| LFI | Loi de finances initiale |
| MAE | Erreur absolue moyenne |
| ML | Machine learning (apprentissage automatique) |
| OAT | Obligation assimilable du Trésor (emprunt d'État français) |
| OCDE | Organisation de coopération et de développement économiques |
| pb | Point de base (0,01 point de pourcentage) |
| PIB | Produit intérieur brut |
| RF | Forêt aléatoire (random forest) |
| RMSE | Racine de l'erreur quadratique moyenne |
| SHAP | SHapley Additive exPlanations (mesure d'importance des variables) |
| SMB | Situation mensuelle budgétaire de l'État |
| VAR | Modèle vectoriel autorégressif |
| VIX | Indice de volatilité implicite du S&P 500 |
| XGB | XGBoost (gradient boosting) |

## Glossaire

Spread OAT-Bund. Écart entre le taux de l'emprunt d'État français à 10 ans et celui de l'emprunt allemand de même durée. Il mesure le supplément de rendement exigé par les investisseurs pour prêter à la France plutôt qu'à l'Allemagne.

R² hors échantillon. Part de l'erreur de la moyenne historique que le modèle évite, sur des données qu'il n'a pas vues. Positif : le modèle fait mieux que la moyenne ; négatif : il fait moins bien.

Marche aléatoire (variation nulle). Prévision naïve selon laquelle la valeur du mois prochain sera égale à celle du mois en cours.

Validation glissante. Méthode d'évaluation où le modèle est réestimé chaque mois avec les seules données passées, puis prévoit le mois suivant.

Biais d'anticipation (look-ahead bias). Erreur qui consiste à utiliser une information qui n'était pas encore publiée à la date de la prévision.

Contrôle positif et contrôle négatif. Test du dispositif avec une variable fictive construite pour contenir un signal (positif), ou avec des variables de pur bruit (négatif).

Puissance d'un test. Probabilité qu'un test détecte un effet qui existe réellement.

# Introduction générale

## Contexte

Les finances publiques françaises sont redevenues un sujet central pour les marchés. Le déficit du budget de l'État a atteint 173 milliards d'euros en 2023 et 156 milliards en 2024 (DGFiP, situations mensuelles budgétaires de l'État). Entre 2023 et 2025, les agences de notation (Fitch, Moody's, S&P) ont abaissé cinq fois la note de la France. Sur les marchés, l'écart de taux entre la France et l'Allemagne à 10 ans (le spread OAT-Bund), qui mesure le supplément de rendement exigé pour prêter à la France, est passé d'environ 26 points de base en 2016 à plus de 80 points de base début 2025. En juin 2024, l'annonce de la dissolution de l'Assemblée nationale l'a fait monter de près de 16 points de base en un mois.

Dans le même temps, les données publiques sont de plus en plus ouvertes. Le ministère de l'Économie publie chaque mois la situation budgétaire de l'État, en séries longues ouvertes depuis 2013 : dépenses de personnel, de fonctionnement, d'investissement, d'intervention, charge de la dette, recettes. Ces séries sont gratuites, détaillées et disponibles environ deux mois après la fin de chaque mois.

Enfin, les méthodes de machine learning sont de plus en plus utilisées pour prévoir les variables financières. Des travaux récents annoncent de très bonnes performances pour la prévision des spreads souverains européens (Bouillot et al., 2025).

## Problématique

Ces trois éléments conduisent à une question simple : peut-on prédire des indicateurs des marchés financiers à partir des données de dépenses publiques ouvertes, en utilisant des techniques de machine learning ?

La réponse n'a rien d'évident. D'un côté, les études européennes montrent que les finances publiques expliquent une partie du niveau des spreads, surtout en période de crise (Afonso et al., 2015). De l'autre, la théorie des marchés efficients (Fama, 1970) et les travaux sur l'anticipation des dépenses (Ramey, 2011) suggèrent qu'une information connue, ou prévisible, est déjà dans les prix. Un résultat négatif est donc aussi plausible qu'un résultat positif, et les deux seraient instructifs.

## Objectif et démarche

Nous étudions trois indicateurs, plus ou moins exposés au risque souverain français : la variation du spread OAT-Bund à 10 ans, la variation du taux OAT à 10 ans et le rendement du CAC 40. Pour chacun, nous prévoyons la valeur du mois suivant, sur la période 2014-2026.

La démarche repose sur une comparaison directe. Un premier modèle n'utilise que des variables de marché et macroéconomiques. Un second ajoute les dépenses de l'État. Si les dépenses contiennent une information utile, le second modèle doit mieux prévoir. Nous testons trois méthodes (régression Ridge, forêt aléatoire, XGBoost), toujours évaluées sur des mois qu'elles n'ont pas vus, avec des tests statistiques pour juger les écarts.

Une attention particulière est portée à la rigueur de l'évaluation. Les données budgétaires sont décalées de leur délai réel de publication, pour ne jamais utiliser une information qui n'était pas encore connue. Dix-neuf extensions testent d'autres horizons, d'autres cibles et un panel de cinq pays européens. Enfin, des contrôles avec un signal fictif et avec des variables de bruit permettent de savoir ce que notre dispositif est capable de détecter.

## Apports

Ce travail apporte trois choses. Il isole l'apport des dépenses publiques, que les études de prévision mélangent d'habitude à des centaines, voire des milliers, d'autres variables. Il utilise les données détaillées d'exécution du budget français, alors que la France est peu étudiée dans cette littérature. Et il montre, chiffres à l'appui, qu'une très bonne performance apparente peut cacher une prévision moins bonne que la plus simple des références.

## Plan du mémoire

Le chapitre 1 présente l'état de l'art : le cadre théorique, les travaux européens sur les finances publiques et les spreads, et l'usage du machine learning pour les prévoir. Le chapitre 2 décrit les données et la méthodologie. Le chapitre 3 présente les résultats, sans les interpréter. Le chapitre 4 les discute : réponse à la problématique, explications possibles, comparaison avec la littérature, implications, limites et pistes de recherche. La conclusion résume les apports du travail.

# Conclusion générale

Ce mémoire posait une question simple : les données ouvertes de dépenses publiques permettent-elles de prévoir les marchés financiers ? Pour y répondre, nous avons construit un jeu de données mensuel à partir des situations budgétaires de l'État français, en respectant leur délai réel de publication, et nous avons comparé des modèles avec et sans dépenses pour trois indicateurs : le spread OAT-Bund, le taux OAT et le CAC 40.

## Principaux résultats

La réponse est négative, pour l'instant. Nous ne trouvons aucune preuve que les dépenses de l'État améliorent la prévision à un mois. Ce résultat tient pour les trois méthodes, pour les dix-neuf extensions réalisées, avec un décalage de publication d'un à trois mois, et après correction pour les tests multiples (168 comparaisons d'extensions et 18 tests du modèle principal). Aucune des hypothèses de départ n'est validée : les dépenses n'apportent pas de gain significatif (H1) ; il n'y a donc pas d'apport à classer entre les indicateurs (H2, non testable) ; le machine learning ne fait pas mieux qu'une régression linéaire (H3) ; et aucune ligne de dépense ne se détache (H4, non soutenue).

Dans le modèle principal, plus généralement, aucun modèle ne bat la moyenne historique, et pour les taux, la prévision « pas de variation » fait mieux que tous les modèles. À un mois, ces marchés restent très difficiles à prévoir.

## Apports

Nous répondons d'abord à une question précise, avec une méthode qui isole l'effet des dépenses, sur un pays peu étudié. Nos contrôles montrent ensuite ce que le dispositif aurait pu détecter (un effet fort, pas forcément un effet faible), et que du pur bruit obtient autant d'importance que les dépenses dans un modèle d'arbres. Enfin, un R² de plus de 90 % sur le niveau du spread, comme dans la littérature récente, peut aller avec une prévision moins bonne que la simple reconduction du dernier spread : la comparaison à une référence naïve est indispensable.

## Limites

Les principales limites sont la taille de l'échantillon (79 mois de test), qui ne permet de détecter qu'un effet fort ; l'utilisation de données budgétaires révisées plutôt que des chiffres connus à chaque date ; l'absence de crise de la dette française sur la période ; et l'absence d'étude d'événement sur le spread, qui aurait permis de tester directement si les marchés réagissent à la publication des chiffres (une vérification préliminaire sur le CAC 40 ne montre pas de réaction).

## Perspectives

Deux pistes nous semblent les plus prometteuses. La première est une étude d'événement à fréquence quotidienne sur le spread, autour des dates de publication des situations budgétaires. La seconde consiste à étudier les annonces budgétaires (projet de loi de finances, programmes de stabilité) plutôt que l'exécution, car c'est au moment de l'annonce que l'information devient nouvelle pour les marchés.

Ce résultat invite à la prudence. Avec des finances publiques françaises qui inquiètent, il est tentant de chercher dans chaque publication budgétaire un signal pour les marchés. Nos résultats suggèrent que ce signal, s'il existe dans l'exécution mensuelle du budget, est trop faible pour être exploité.
