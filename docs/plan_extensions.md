# Plan pré-enregistré des extensions (section 3.6 du mémoire)

**Date de rédaction : 26 septembre 2026, avant l'exécution de tout test d'extension.**
Ce fichier est commité avant les résultats : la liste ci-dessous est fixée et **tous** les résultats
seront rapportés, favorables ou non.

## Contexte
Les modèles principaux (`src/04_models.py`) ne battent pas la moyenne historique à l'horizon d'un mois,
et l'ajout des dépenses publiques (M1) n'améliore pas la prévision par rapport aux seules variables de
marché (M0). Les extensions ci-dessous testent si ce résultat tient sous d'autres formulations,
justifiées par la littérature ou par le diagnostic (surapprentissage, changement de régime).

## Protocole commun (inchangé)
- Période de test : 2020-01 → 2026-07, réestimation mensuelle, aucune donnée future dans l'entraînement.
- Budget toujours décalé de 2 mois (délai de publication).
- Question évaluée dans chaque extension : **la version avec dépenses bat-elle la version sans dépenses ?**
  et **bat-elle la moyenne historique ?**
- Critère : R² hors échantillon, test de Diebold-Mariano (perte quadratique ; Brier pour la classification).
- **Tests multiples** : les p-values « avec dépenses vs sans » de toutes les extensions sont corrigées
  par la procédure de Benjamini-Hochberg (taux de fausses découvertes 10 %). Seuls les résultats qui
  survivent à la correction seront présentés comme significatifs.

## Liste des extensions

| # | Extension | Justification |
|---|---|---|
| E1 | Horizons 3, 6 et 12 mois (variation cumulée) | Les dépenses agissent lentement sur la dette. Entraînement limité aux cibles déjà observées ; DM avec correction de Newey-West (h-1 retards). |
| E2 | Classification hausse/baisse (logistique, forêt, XGBoost) | Deviner le sens est plus facile que l'ampleur. Référence : classe majoritaire. Critères : taux de bonne classification, AUC, score de Brier. |
| E3 | Volatilité : cible = valeur absolue de la variation du mois suivant | La volatilité est persistante ; l'incertitude budgétaire peut agiter les marchés. |
| E4 | Surprise budgétaire : taux d'exécution des dépenses par rapport au budget voté (LFI), comparé au même mois de l'année précédente | Les marchés intègrent les annonces (Ramey, 2011) ; l'information nouvelle est l'écart à ce qui a été voté. |
| E5 | Effet selon le régime de taux : interactions dépenses × période de taux positifs (facilité de dépôt BCE > 0) | Afonso, Arghyrou et Kontonikas (2015) : la sensibilité des spreads aux finances publiques varie dans le temps. |
| E6 | Moins de variables : (a) jeu réduit, (b) 2 composantes principales des dépenses (ACP estimée sur l'entraînement uniquement) | Réduire le surapprentissage (environ 70 à 150 mois d'entraînement). |
| E7 | Prévisions tempérées : moyenne 50/50 entre la prévision du modèle et la moyenne historique (poids fixé a priori) | Campbell et Thompson (2008). |
| E8 | Combinaison de prévisions : moyenne de Ridge, forêt aléatoire et XGBoost | Robustesse classique des combinaisons en prévision. |
| E9 | Elastic Net avec validation croisée temporelle interne | Sélection automatique des variables. |
| E10 | XGBoost avec réglage des hyperparamètres par validation croisée temporelle emboîtée (réglage refait tous les 12 mois, sur l'entraînement uniquement) | Le XGBoost de base est peut-être trop complexe. |
| E11 | Fenêtre glissante de 60 mois au lieu d'une fenêtre croissante | S'adapter au changement de régime de 2022. |
| E12 | Évaluation par période : 2020-2021 (taux bas, Covid) contre 2022-2026 (hausse des taux, tensions politiques) ; mois calmes contre agités (VIX > 20) | Un apport éventuel peut être limité aux périodes de tension. |
| E13 | Notations souveraines de la France (Fitch, Moody's, S&P) comme variable de contrôle pour le spread | Les dégradations de notation font bouger le spread ; à tester dans M0 et M1. |

## Ce qui ne sera pas fait (hors délai ou hors sujet), à citer en perspectives
- Données de la commande publique (DECP) : nettoyage trop long.
- Panel de plusieurs pays (comme Bouillot et al., 2025) : données budgétaires mensuelles hétérogènes.
- Sentiment des actualités, Google Trends : hors du périmètre « dépenses publiques » du titre.

## Ajout du 26 septembre 2026, 23h20 (avant tout résultat de ce test)

| # | Extension | Justification |
|---|---|---|
| E14 | **Étude d'événement** : réaction quotidienne du spread OAT–Bund (et de l'OAT, du CAC 40) le jour de la publication de la situation mensuelle budgétaire | Si les marchés intègrent l'information budgétaire dès sa publication (Fama, 1970 ; Ramey, 2011), l'effet doit apparaître le jour même et non un mois plus tard. Complète le résultat négatif des prévisions mensuelles. |

Protocole E14, fixé avant l'analyse :
- **Dates d'événement** : communiqués de presse du ministère « Situation mensuelle budgétaire » (presse.economie.gouv.fr) ; à défaut, dates de publication DGFiP avec une fenêtre élargie [-2 ; +1] jours ouvrés.
- **Données** : taux à 10 ans quotidiens France et Allemagne (BCE / Banque de France / Bundesbank), CAC 40 quotidien.
- **Tests** : (1) la variation absolue du spread sur la fenêtre [0 ; +1] est-elle plus grande les jours de publication que les autres jours (test de Mann-Whitney, test de permutation) ? (2) la variation du spread sur la fenêtre est-elle liée à la surprise budgétaire du mois publié (corrélation de Spearman, régression) ?
- Résultat rapporté quel qu'il soit.

## Ajout du 27 septembre 2026, 11h30 (avant collecte et avant tout résultat)

| # | Extension | Justification |
|---|---|---|
| E15 | **Panel européen trimestriel** : France, Italie, Espagne, Portugal, Belgique ; dépenses publiques harmonisées Eurostat (`gov_10q_ggnfa`) | Plus d'observations (réduire le surapprentissage), inclusion de la crise de la dette 2010-2012 (absente des données françaises mensuelles), pays plus sensibles aux finances publiques. Réplique le cadre de Bouillot, Candelon et Kool (2025) en corrigeant trois points : cible en variation, comparaison à la marche aléatoire, délai de publication. |

Protocole E15, fixé avant l'analyse :
- **Cible** : variation du spread (taux 10 ans du pays − Bund, moyenne trimestrielle des données mensuelles OCDE/FRED) entre le trimestre q et q+1, en points de base.
- **Dépenses (Eurostat, administrations publiques S13, millions d'euros, non désaisonnalisé)** : dépenses totales (TE), rémunérations (D1PAY), intérêts (D41PAY), investissement (P51G), prestations sociales (D62PAY), consommations intermédiaires (P2). Transformation : croissance sur un an de la somme sur 4 trimestres. Décalage de publication : **2 trimestres**.
- **M0** : variation passée du spread, niveau du spread, variation du Bund, VIX, taux de dépôt BCE, indicatrices pays. **M1** = M0 + dépenses.
- **Modèles** : Ridge, forêt aléatoire, XGBoost (hyperparamètres de `src/04_models.py`), modèle groupé sur les pays ; références : moyenne historique par pays et marche aléatoire (variation nulle).
- **Validation glissante** trimestrielle, fenêtre croissante, **test à partir de 2010T1** (inclut la crise de la dette) ; sous-période 2015T1+ rapportée aussi.
- **Tests** : Diebold-Mariano sur la perte quadratique sommée sur les pays à chaque trimestre ; résultats par pays rapportés. Les p-values s'ajoutent à la correction Benjamini-Hochberg de l'ensemble des extensions.
- Résultat rapporté quel qu'il soit ; les résultats France mensuels restent le cœur du mémoire.

## Ajout du 27 septembre 2026, 11h40 (avant collecte et avant tout résultat)

| # | Extension | Justification |
|---|---|---|
| E16 | **Réplication élargie de Bouillot, Candelon et Kool (2025)** : panel mensuel de 5 pays (France, Italie, Espagne, Portugal, Belgique ; spread face au Bund), 2008-2026, base de plusieurs centaines de variables ouvertes organisées en blocs thématiques | Tester si une base large, dans le cadre de la référence la plus proche, fait apparaître un apport des finances publiques. |

Protocole E16, fixé avant l'analyse :
- **Blocs** : (1) taux et marchés du pays (taux court, taux long, indice boursier) ; (2) macroéconomie du pays (chômage, inflation, production industrielle, confiance des ménages et des entreprises, indicateur avancé OCDE) ; (3) variables mondiales (taux et activité américains, pétrole, euro-dollar, VIX, écart de crédit) ; (4) **finances publiques** (Eurostat trimestriel : dépenses totales, rémunérations, intérêts, investissement, prestations, consommations intermédiaires, recettes, solde ; décalage de 2 trimestres puis prolongé mensuellement). Chaque variable entre en niveau et en variation, avec 1 retard. Variables publiées avec retard (macro) décalées d'1 mois ; finances publiques de 2 trimestres.
- **Cibles** : (a) **niveau** du spread au mois t+1 (comme Bouillot et al.) ; (b) **variation** du spread entre t et t+1.
- **Modèles** : XGBoost (modèle de référence de Bouillot et al.), forêt aléatoire, Ridge ; modèle groupé sur les pays, indicatrices pays.
- **Références** : moyenne historique du pays **et marche aléatoire** (spread inchangé). Le R² par rapport à la moyenne ET le gain par rapport à la marche aléatoire sont rapportés tous les deux.
- **Test clé** : modèle complet contre modèle sans le bloc finances publiques (Diebold-Mariano sur la perte sommée sur les pays), ajouté à la correction Benjamini-Hochberg.
- Validation glissante mensuelle, fenêtre croissante, test à partir de 2012-01 (entraînement 2008-2011), réestimation tous les 3 mois pour tenir le temps de calcul.
- Résultat rapporté quel qu'il soit.

## Ajout du 27 septembre 2026, 13h00 (après les résultats E15/E16, avant toute donnée et tout résultat des tests ci-dessous)

Motivation déclarée : après le résultat négatif d'E1–E16, nous testons quatre dernières pistes, chacune justifiée
par un mécanisme économique. **Toutes** les p-values s'ajoutent à la correction Benjamini-Hochberg (10 %) de l'ensemble
des extensions. Limite fixée : résultats au plus tard le 29/09/2026 au soir ; ce qui n'est pas terminé passe en perspectives.
E14 (étude d'événement, pré-enregistrée le 26/09) est exécutée avec ce lot si les données quotidiennes sont obtenues.

| # | Extension | Justification |
|---|---|---|
| E17 | **Panel annuel** (5 pays) : variation du spread sur l'année suivante | Les finances publiques expliquent les spreads à basse fréquence (Codogno et al., 2003 ; Afonso et al., 2015) ; la fréquence mensuelle est surtout du bruit pour une variable lente. |
| E18 | **Régime de crise** (panel trimestriel) : dépenses × indicatrice de tension | Les marchés ne regardent les finances publiques qu'en période de tension (Bernoth et Erdogan, 2012). **Exploratoire** : l'idée vient de la ventilation par sous-période d'E15. |
| E19 | **Actions sectorielles exposées à la dépense publique** (France) | Canal des revenus : l'investissement et la commande publics sont des recettes pour le BTP-concessions et la défense ; le CAC 40 est trop agrégé. |
| E20 | **Incertitude de politique économique** (Baker, Bloom et Davis, 2016), France | Tester si l'apport des dépenses apparaît une fois l'incertitude politique contrôlée, et si cette incertitude aide elle-même. |

Protocole E17 :
- Pays : FR, IT, ES, PT, BE (spread face au Bund, en pb). Valeur annuelle = **décembre** (pas de moyenne annuelle, pour éviter l'autocorrélation mécanique mise en évidence par le diagnostic d'E15).
- Cible : spread de décembre t+1 − spread de décembre t.
- M0 : spread de décembre t, variation du spread sur l'année t, variation du Bund sur l'année t, VIX (décembre), taux de dépôt BCE (décembre), indicatrices pays.
- M1 = M0 + finances publiques connues fin décembre t (Eurostat, décalage de 2 trimestres, donc sommes sur 4 trimestres se terminant au T2 de l'année t) : croissance sur un an de TE, D1PAY, D41PAY, P51G, D62PAY, P2, TR ; solde en % des dépenses ; part des intérêts ; variation du solde en % des dépenses sur un an.
- Modèles : Ridge, forêt aléatoire, XGBoost (hyperparamètres de `src/04_models.py`), modèle groupé. Références : moyenne historique par pays et marche aléatoire (variation nulle).
- Validation glissante annuelle, fenêtre croissante ; origines de prévision 2010 à 2024 (cibles 2011 à 2025), 75 prévisions.
- DM sur la perte sommée sur les pays chaque année.

Protocole E18 (exploratoire) :
- Panel trimestriel d'E15, mais spread en **fin de trimestre** (dernier mois du trimestre) pour la cible et les retards.
- Tension = 1 si le spread du pays en fin de trimestre q dépasse 200 pb.
- M0 = variables d'E15 + indicatrice de tension ; M1 = M0 + finances publiques + finances publiques × tension.
- Test à partir de 2010T1 ; résultats rapportés aussi pour 2010-2014 et 2015+.

Protocole E19 :
- Cibles (France, mensuel, prix de clôture de fin de mois hors dividendes comme le CAC 40) : rendement du mois suivant **en excès du CAC 40** de deux paniers équipondérés : (a) BTP-concessions : Vinci (DG.PA), Eiffage (FGR.PA), Bouygues (EN.PA) ; (b) défense : Thales (HO.PA), Dassault Aviation (AM.PA).
- Horizons 1 et 3 mois.
- M0 = variables de marché du modèle principal + rendement en excès du panier (t et t-1) ; M1 = M0 + les 7 dépenses `_ytd_gap` (décalage de 2 mois). Les données DGFiP ne ventilent pas la défense : pas de ligne dédiée.
- Ridge, forêt aléatoire, XGBoost ; test 2020-01 → 2026-07 ; 12 comparaisons. Actions individuelles : descriptif seulement, hors tests.

Protocole E20 :
- Indice mensuel d'incertitude de politique économique pour la France (Baker, Bloom et Davis ; via FRED), en logarithme, décalé d'1 mois.
- (a) M0 + incertitude contre M0 ; (b) M1 + incertitude contre M0 + incertitude. Trois cibles principales, trois modèles, test 2020-01 → 2026-07 ; 18 comparaisons.
