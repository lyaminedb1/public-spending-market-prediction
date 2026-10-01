# Revue de la rédaction du mémoire

> **Statut : rapport de revue, rien n'a été modifié dans les chapitres, le code ni les résultats.**
> Revue du 01/10/2026 (jeudi), demandée par `docs/prompt_revue_redaction.md`. Les passages à corriger sont à reporter
> dans les documents Claude Docs (source de vérité, voir `redaction/README.md`), pas dans les exports `.md`.
> Règle ECE : ce rapport ne propose aucune nouvelle interprétation ; les questions pour Elyamine sont marquées « ? ».

## 0. Périmètre et limites de cette revue

**Lu en entier** : `redaction/chapitre1…md` à `chapitre4…md`, `pages_liminaires_intro_conclusion.md`, le début et la fin de `annexes.md`
(généré par script), et le texte du PDF commité `redaction/build/Memoire_DaliBraham.pdf` (88 pages, état de `355b0c6`).

**Vérifié contre le dépôt** : les chiffres des chapitres 2 à 4, de l'introduction et du résumé contre `results/tables/**` et
`data/processed/dataset_monthly.csv` ; la méthode du chapitre 2 contre `src/02`, `04`, `15`, `17` ; les dates du plan des extensions contre
l'historique git ; la liste des références contre les citations du PDF.

**Non vérifié (à dire clairement)** :
- Les affirmations sur le contenu des articles (Bouillot et al., Attinasi et al., Afonso et al., Belly et al., Garlanda-Longueville,
  Favero, Goulet Coulombe et al., etc.) : les articles ne sont pas dans le dépôt et la sortie réseau de cette session est bloquée. Je n'en cite aucun de mémoire.
- La mise en forme du Word (police, interligne, marges, numérotation) : seul le texte du PDF a été lu.
- Je n'ai pas relancé les modèles ; les chiffres sont comparés aux CSV du dépôt, comme demandé.

## 1. Code et résultats : aucune erreur trouvée

- Tous les chiffres de résultats cités dans les chapitres 3 et 4, l'introduction, le résumé et la conclusion correspondent aux CSV (liste en 6).
- Les chiffres du chapitre 2 qui ne sont reproduits par aucun script du dépôt se retrouvent en recalculant avec `src/02_build_dataset.py`
  (`read_budget_file`, `build_budget`) : −902 % / +1 789 % (impôt sur les sociétés), −462 % (opérations financières), écart-type de
  `dep_totales_ytd_gap` de 0,7 en janvier et 4,42 en décembre (rapport 6,3).
- Point mineur, sans effet sur le mémoire : dans `results/tables/diag_04/verif_chiffres_03.csv`, la ligne « corrélation partielle personnel / ΔOAT »
  affiche `conforme = False` (valeur recalculée 0,147, fourchette citée 0,07–0,13). Le mémoire cite 0,15, qui est correct ; seule la fourchette
  codée dans `src/21_verif_chiffres_03.py` est périmée.

## 2. Problèmes classés par gravité

### 2.1 Erreurs (affirmation inexacte ou non soutenue)

**E1. Déclaration d'usage de l'IA : la phrase sur la littérature dit plus que ce qui a été fait.** *(pages liminaires, p. 3 du PDF)*
> « Les chiffres cités ont été vérifiés sur les fichiers de résultats, et les affirmations sur la littérature ont été vérifiées dans les articles originaux. »

- Source : `redaction/README.md` : « articles principaux vérifiés contre les PDF le 30/09 (Bouillot, Afonso, Attinasi, Belly, Ramey, Laubach,
  Garlanda-Longueville ; Barbier-Gauchard via le résumé) ». Favero, Bernoth et al., Welch et Goyal, Fama, Gu et al., etc. ne figurent pas dans cette liste, et
  `CLAUDE.md` indique encore « Résumés des articles : à vérifier sur les articles ».
- La même déclaration dit aussi que l'auteur « a relu et validé l'ensemble du texte » ; or le chapitre 4 est, dans l'export, un « brouillon de travail, à réécrire par Elyamine ».
- Correction proposée : n'affirmer que ce qui est vrai à la date de remise, par exemple « les articles centraux (liste) ont été relus dans leur version originale ; les autres références
  sont citées d'après leurs résumés ». Ne garder « a relu et validé l'ensemble du texte » que si c'est vrai pour le chapitre 4 (voir E2).

**E2. Chapitre 4 : texte d'interprétation rédigé par l'IA, présenté comme final dans le PDF.** *(chapitre 4, ensemble)*
- Le guide ECE interdit de rendre des interprétations générées par l'IA sans relecture critique et apport personnel. L'export du chapitre porte la mention
  « Statut : brouillon de travail, à réécrire par Elyamine. Les idées viennent de nos discussions ». Cette mention n'apparaît pas dans le PDF : le texte y figure sans réserve.
- Correction proposée : relire chaque paragraphe d'interprétation (4.1 à 4.6) et décider « garder / couper / contredire » avec ses propres mots (consigne déjà écrite dans l'en-tête de l'export).
  Questions à poser à Elyamine : « Quelle explication de la section 4.2 te semble la plus plausible, et pourquoi ? », « Quelle limite te paraît la plus grave ? », « Que dirais-tu à un investisseur ? ».

**E3. Chapitre 2, 2.7 : « avant leurs propres données » est inexact pour E17 et E18.**
> « E17 à E20, en revanche, ont été ajoutées le 27 septembre **après** avoir vu les résultats d'E15 et E16, mais avant leurs propres données. »

- Sources (`git log`) : résultats E15 commités le 27/09 à 12:57 (`03c109b`) ; pré-enregistrement d'E17-E20 à 13:03 (`79c7a4c`) ; résultats E17/E18 à 13:06 (`2f49506`).
  Le plan (`docs/plan_extensions.md`) définit E18 comme « Panel trimestriel d'E15, mais spread en fin de trimestre » : ses données étaient déjà collectées. E17 s'appuie sur
  les mêmes sources (Eurostat, FRED) que E15/E16. Seules E19 (actions) et E20 (indice d'incertitude) ont de nouvelles données collectées après le pré-enregistrement (commit `2652132`, 13:04).
- Correction proposée : « E17 à E20 ont été ajoutées après avoir vu les résultats d'E15 et E16 ; E19 et E20 ont été pré-enregistrées avant la collecte de leurs données, alors que E17 et E18
  réutilisent le panel déjà collecté pour E15 et E16. » (À vérifier par Elyamine pour E17 : je n'ai pas relu `src/14_more_extensions.py` ligne par ligne.)

**E4. Chapitre 2, 2.2.2 : fourchette de taux de croissance attribuée à janvier.**
> « En janvier, le cumul est presque nul, et le taux prend des valeurs absurdes : de -902 % à +1 789 % pour l'impôt sur les sociétés. »

- Source (recalcul, `src/02`) : −902 % et +1 789 % sont les extrêmes sur l'ensemble des mois ; pour janvier seul, la fourchette est −449 % à +470 %.
- Correction proposée : « …des valeurs absurdes : sur l'ensemble des mois, de −902 % à +1 789 % pour l'impôt sur les sociétés ».

**E5. Chapitre 3, 3.4 : la permutation n'est pas faite sur « un modèle » qui contient bruit et signal.**
> « …l'importance par permutation, calculée sur un modèle M1 auquel on ajoute les variables de bruit et le signal fictif, qui servent de repères. »

- Source : `src/17_permutation_oos.py` l. 81-84 : deux configurations distinctes, `M1+bruit` (7 variables de bruit) et `M1+signal` (1 variable fictive de corrélation 0,5).
- Correction proposée : « …calculée sur deux modèles : M1 auquel on ajoute sept variables de bruit, et M1 auquel on ajoute un signal fictif… ».

**E6. Chapitre 3, 3.4 : « en tête » est vrai parmi les dépenses seulement.**
> « Les dépenses d'intervention arrivent en tête pour le spread et l'OAT, l'investissement pour le CAC 40. »

- Source : `results/tables/models_shap_importance.csv` et figure 3.3 : parmi les sept dépenses, c'est exact ; sur l'ensemble des variables, l'intervention est 4ᵉ pour le spread (derrière `d_oat`, `spread_bp`, `cac_ret_l1`) et 1ʳᵉ pour l'OAT.
- Correction proposée : ajouter « parmi les dépenses ».

**E7. Chapitre 2, 2.6.5 : nombre de tirages du contrôle positif.**
> « …(ρ = 0,1 à 1), avec 10 tirages par valeur, … »

- Source : `src/15_diag_04.py` l. 140 : `range(10 if rho < 1 else 1)` ; la légende du tableau 3.4 (« 1 pour ρ = 1 ») est correcte.
- Correction proposée : « avec 10 tirages par valeur de ρ inférieure à 1 (un seul pour ρ = 1) ».

### 2.2 À préciser

**P1. Chapitre 4, 4.4 : le chiffre sur la pénalité de Ridge ne porte que sur deux jeux de variables.**
> « …la pénalité choisie est souvent très forte (supérieure à 10 000 dans 27 à 44 % des mois, contre moins de 100 le plus souvent pour le spread) »

- Source : `results/tables/diag_04/alpha_bornes_courant.csv` (script 4) : CAC 40, α > 10 000 dans 26,6 % (M0), 44,3 % (M1) et **89,9 % (M2)** des mois ; spread, α < 100 dans 100 % (M0), 72,2 % (M1), 77,2 % (M2).
- Correction proposée : préciser « pour M0 et M1 » ou ajouter le chiffre de M2 (qui renforce l'argument).

**P2. Chapitre 4, 4.4 : « mais sans les dépenses » est plus fort que les résultats.**
> « Certaines extensions battent la moyenne, mais **sans les dépenses** : »

- Source : tableau 3.6 / `ext_synthese.csv` : E2 pour l'OAT (+5,8 avec dépenses contre +2,5 sans) et E3 pour l'OAT (+4,2 contre +3,3) sont *meilleurs avec* les dépenses, sans différence significative. Le chapitre 3 le dit correctement ; le chapitre 4 aussi plus bas (« Dans aucun de ces cas l'ajout des dépenses n'apporte un gain significatif »), mais la phrase d'ouverture et la phrase « Ce qui est prévisible vient des marchés eux-mêmes, pas du budget de l'État » les contredisent un peu.
- Correction proposée : « Certaines extensions battent la moyenne, sans que les dépenses y apportent un gain significatif ».

**P3. Garlanda-Longueville (2023) : deux descriptions différentes.**
- Chapitre 1 : « …aux allocutions du président de la République pendant la crise du Covid (mars 2020 à décembre 2021), qui contenaient des engagements budgétaires ».
- Chapitre 4 : « …trouve un effet des annonces budgétaires françaises sur le spread, avec des données quotidiennes » et, en 4.8, « montre qu'une telle approche trouve des effets pour les annonces budgétaires ».
- Correction proposée : aligner le chapitre 4 sur le chapitre 1 (annonces présidentielles liées au Covid), et ne pas généraliser aux « annonces budgétaires françaises ». Non vérifié dans la thèse (non accessible).

**P4. Affirmations sur Bouillot et al. (2025) : centrales pour le mémoire, non vérifiables ici.**
- Ch. 1 et 4 : « pas à la prévision naïve "spread du mois précédent" » ; RMSE 7,3 pb pour la France sur 2020-2025 ; R² de 0,81 à 0,99 (0,86 pour la France) ; « une seule [variable] parmi les 50 plus importantes » ; régressions pénalisées meilleures que XGBoost en Belgique et en Espagne (ch. 4).
- Ces points soutiennent la critique principale du mémoire. Ils sont déclarés vérifiés le 30/09 (`README`, `CLAUDE.md`), mais je n'ai pas pu les relire. À re-vérifier une dernière fois sur le PDF (pages des tableaux 11 et 12 citées dans `CLAUDE.md`) avant la remise.
- Autres affirmations sur des articles que je n'ai pas pu vérifier : Attinasi et al. (« c'est l'annonce elle-même qui a compté, et non le montant engagé »), Afonso et al. (rupture de mars 2009), Belly et al. (« y compris en variation mensuelle, sur 2004-2019 »), Goulet Coulombe et al. (« prévoient bien l'inflation »).

**P5. Chapitre 3, tableau 3.1 : dates ambiguës.**
> « Tableau 3.1 – Statistiques des variables cibles (mars 2014 – juillet 2026, 149 mois) »

- « mars 2014 – juillet 2026 » est la date du mois où la prévision est faite ; les variations vont d'avril 2014 à août 2026 (même convention que 2.6.1 : « variations prévues de février 2020 à août 2026 »).
- Correction proposée : « 149 mois, prévisions faites de mars 2014 à juillet 2026 » ou indiquer les mois des variations.

**P6. Chapitre 3, 3.7 : les verdicts sur les hypothèses.**
- Le guide ECE demande des résultats sans interprétation. Le tableau 3.8 (« Non validée », « Non testable », « Non soutenue ») est à la limite : ce sont des conclusions sur les hypothèses. Option : garder le tableau en 3.7 mais ne présenter que les éléments chiffrés, et porter les verdicts en 4.1. ? Quelle option préfère l'encadrante ?

**P7. Introduction : chiffres sans source.**
> « Le déficit du budget de l'État a atteint 173 milliards d'euros en 2023 et 156 milliards en 2024. Entre 2023 et 2025, les agences de notation ont abaissé cinq fois la note de la France. »

- Les chiffres sont corrects : soldes reconstitués −173,0 et −155,9 Md€ (tableau 2.2) ; cinq dégradations entre avril 2023 et octobre 2025 dans `data/raw/ratings_france.csv`. Mais l'introduction ne cite aucune source. Correction proposée : renvoyer à la DGFiP et aux communiqués des agences (sources déjà dans le dépôt).

**P8. Valeurs de p qui diffèrent entre documents.**
- E15, Ridge M1 contre M0 : `E15.csv` donne 0,365 ; le chapitre 3 écrit « p = 0,37 » et `CLAUDE.md` « p 0,36 ». Choisir un arrondi unique : 0,365 s'arrondit à 0,37 selon l'arrondi usuel.

**P9. Annonce des sections et nombre de contrôles.**
- Chapitre 2, introduction : « Pour finir, la section 2.7 présente les variantes testées… » ; la section 2.8 (éthique) n'est pas annoncée.
- Chapitre 2, 2.6.5 : « nous avons ajouté cinq contrôles » ; chapitre 3, 3.3 : « Quatre contrôles complètent le tableau 3.2 » (le cinquième, la permutation, est en 3.4). Cohérent mais à signaler au lecteur (« quatre ici, le cinquième en 3.4 »).

**P10. Dépôt « accessible sur demande » et lien public.**
- Ch. 2 et annexe F : « dépôt GitHub (accessible sur demande) », mais les « Sources en ligne » donnent le lien `github.com/lyaminedb1/…` sans réserve. Dire si le dépôt est public ou privé, et rendre les deux phrases cohérentes (et s'assurer que le dépôt contient bien les fichiers cités, dont `docs/plan_extensions.md`).

### 2.3 Style et mise en forme

- **Longueurs (PDF, 88 pages)** : introduction 3 p. (guide : 3-5) ; chapitre 1 : 13 p. (10-15) ; **chapitre 2 : 16 p. (5-8)** ; **chapitre 3 : 10 p. (4-6)** ; **chapitre 4 : 12 p. (6-8)** ; conclusion 2 p. (2-3). Résumé : 233 mots (150-300), 7 mots-clés (5-7). Les chapitres 2, 3 et 4 dépassent le guide ; l'abandon du raccourcissement du chapitre 3 est noté dans `CLAUDE.md` (décision d'Elyamine).
- **Figures** : axes avec points décimaux (« 1.20 »), noms de variables du code (`d_oat`, `spread_bp`, `cac_ret_l1`) non définis dans le chapitre 3 (ils le sont à l'annexe A). Les légendes et sources sont présentes (« Source : calculs de l'auteur »).
- **Références** : numéros [n] cliquables (type IEEE) avec notices au format APA, classées par ordre alphabétique. Le guide accepte APA, IEEE ou Harvard ; le mélange n'est pas un format pur. Les 37 références sont toutes citées et toutes les citations ont une notice (vérifié sur le PDF).
- **Résidus d'export** : les en-têtes « Sep 29, 2026 · @elyamine », la note « Volumes et pages à vérifier sur Google Scholar avant le dépôt » et les marques de figure `[Figure 3.1 … fichier.png]` n'apparaissent pas dans le PDF (vérifié par recherche dans le texte). Le nom « Walid » n'apparaît pas dans le PDF (consigne de `CLAUDE.md`).
- **Langue** : pas de faute d'orthographe ou de grammaire relevée à la lecture. Quelques variantes de notation (« Δ spread », « variation du spread », « p », « p-value ») sont sans conséquence.
- **Citation de seconde main** : « Working, 1960 » est citée comme source d'une explication (autocorrélation mécanique des moyennes) ; la citation est bien présente au chapitre 4 et dans la liste.

## 3. Cohérence entre chapitres

| Point | Résultat |
|---|---|
| Vocabulaire M0/M1/M2, « variation nulle », « moyenne historique » | cohérent partout |
| Numérotation des tableaux et figures, renvois (« tableau 3.3 », « tableau 3.5 », « section 3.3 », « sections 4.7 et 4.8 ») | tous corrects |
| Nombre d'extensions (« dix-neuf réalisées ») | cohérent (20 − E14) |
| 168 comparaisons / 18 tests de H1 / 6 p brutes < 0,05 sur 8,4 attendues | cohérent (ch. 2, 3, 4, résumé, conclusion) |
| Périodes de test (79 mois ; 70 à 148 mois d'entraînement) | cohérent |
| Garlanda-Longueville | incohérent entre ch. 1 et 4 (P3) |
| Cinq / quatre contrôles | à expliciter (P9) |

## 4. Méthode décrite et méthode codée

Concordance vérifiée, sans écart :
- Décalage du budget de 2 mois (`config.BUDGET_LAG`) et de l'inflation de 1 mois (`02`, `.shift(1)`) ; dates de publication citées : janv. 2023 (2 mars), déc. 2024 (4 févr. 2025), juin 2026 (4 août), **juillet 2026 (2 sept.)** : ces dates se retrouvent dans `data/raw/events_html/presse_*.html`, qui donnent aussi février à mai 2026 avec un décalage de deux mois.
- Validation glissante à fenêtre croissante, première prévision fin janv. 2020 avec 70 mois, dernière fin juil. 2026 (79 mois) : conforme à `04` (`train = index < m`).
- Hyperparamètres du texte = ceux de `make_model` (Ridge : 40 valeurs de 10⁻² à 10⁶, leave-one-out ; forêt : 300 arbres, profondeur 4, feuille ≥ 5, 50 % des variables ; XGBoost : 200 arbres, profondeur 2, taux 0,05, sous-échantillons 0,8, `min_child_weight` 5, L2 = 1). Le texte n'écrit ni « fixés a priori » ni « pré-enregistrés » pour `04` : il le dit explicitement (« ces réglages n'ont pas été datés dans le dépôt avant les premiers résultats »).
- DM avec correction de Harvey, Leybourne et Newbold, variance `ddof=0`, loi de Student à T−1 degrés ; BH sur p unilatérales, 168 comparaisons et, séparément, 18 tests de H1.
- Dates du pré-enregistrement : E1-E13 (plan 26/09 21:26 ; `04` et ses résultats commités à 20:43, donc avant le plan, comme le texte l'écrit) ; E14 (23:15), E15 (27/09 11:21), E16 (11:34), E17-E20 (13:03), écart E20 (20:52) : conformes au texte, sauf la nuance E3 ci-dessus.

## 5. Honnêteté des affirmations

- Les résultats négatifs sont formulés avec la bonne portée : « pas de preuve », « un effet fort » exclu, pas un effet faible (4.1, 4.3, résumé, conclusion).
- « L'information est déjà connue » est présentée comme une hypothèse faute d'étude d'événement (4.2, 4.7). Correct.
- E15 : le +15 % est expliqué par l'autocorrélation des moyennes ; le texte rappelle que le diagnostic est non prévu au départ (3.6). À garder ainsi.
- Points à surveiller : la phrase 4.2 « Les marchés connaissent donc le plan de dépenses avant le début de l'année » et la phrase 4.3 « La cause principale est la taille de l'échantillon » sont des interprétations (E2).

## 6. Chiffres vérifiés (échantillon représentatif, tous conformes)

Tableau 3.1 (moyenne, écart-type, min, max, autocorrélation, ADF) ; niveau du spread 26,4 pb (sept. 2016) et 83,6 pb (janv. 2025) ; plus fortes variations (mars 2020 +20,5 ; mai 2017 −18,1 ; févr. 2017 +16,3 ;
juin 2024 +15,5 ; nov. 2016 +15,3) ; part de hausses du spread 51,7 % (« 52 % ») ; corrélations de Spearman et corrélations partielles (0,15 / 0,09 / 0,10 ; p de 0,08 à 0,26 ; investissement −0,15, p = 0,06) ;
tableau 3.2 en entier (33 cases) ; bonne direction (42 à 59 % ; moyenne 53 / 57 / 61 %) ; tableau 3.3 en entier ; « 2 cas sur 6 » contre la variation nulle ; BH minimale 0,81 ; graines (fourchettes et p minimales 0,13) ;
tableau 3.4 (plages sur les trois cibles) ; contrôle négatif (90-95 %, 80-100 %, 50-60 %) ; décalage de 1 et 3 mois (−0,7 %, −2,7 %, p corrigée 0,51) ; tableau 3.5 (32,8 / 36,8 / 30,6 ; 38,1 / 34,2 / 37,1 ; étendues) ; permutation (0,1 à 2,5 % ;
7,6 à 18,8 %) ; tableau 3.6 en entier ; « 34 cases sur 45 » ; 168 comparaisons, 6 p brutes < 0,05, 8,4 attendues ; E15 (13,9 / 15,5 ; AR(1) 0,32 / 0,07 ; +4,1 / +3,4 puis −12,8 / −11,2 points ; −4,1 / −2,9) ;
E16 (92 à 97 %, tableau 3.7, p de 0,08 à 0,81) ; marche aléatoire France 2020-01 à 2025-02 : RMSE 5,1 pb ; E17 (−20 à −338 % ; −19,8 contre −45,4 ; p 0,04) ; E18 (−3,3 → −19,7 ; −20,2 → −26,2 ; −10,4 → −4,9 ; p 0,20) ;
chapitre 2 : solde annuels (−85,6 ; −178,1 ; −173,0 ; −155,9), 0,7 → 4,4, ×6,3, −462 %, hyperparamètres ; chapitre 4 : 21,1 contre 18,4 pb, E3 (+9,6 / +3,3), E2 (+2,5), E1 (+11,8) ; intro : cinq dégradations 2023-2025 et déficits 173 / 156.

## 7. Notes par chapitre

| Partie | Note | Justification |
|---|---|---|
| Pages liminaires, introduction, conclusion | 8/10 | Structure conforme au guide, résumé de bonne longueur, conclusion fidèle aux résultats. Déclaration IA à corriger (E1), sources de l'introduction à ajouter (P7). |
| Chapitre 1 – État de l'art | 8/10 | Bien structuré, tableau 1.1 utile, 37 références toutes citées. Plusieurs affirmations sur les articles restent non vérifiables ici (P4) ; format des références mixte. |
| Chapitre 2 – Données et méthodologie | 8/10 | Très transparent (limites, hyperparamètres non datés, pré-enregistrement), méthode conforme au code. Trois inexactitudes à corriger (E3, E4, E7) ; 16 pages pour 5-8 attendues. |
| Chapitre 3 – Résultats | 8,5/10 | Tous les chiffres sont conformes aux CSV ; peu d'interprétation. À corriger : E5, E6, P5 ; tableau des hypothèses à la limite de l'interprétation (P6) ; 10 pages pour 4-6. |
| Chapitre 4 – Discussion | 6,5/10 | Contenu pertinent et nuancé, chiffres exacts. Mais texte d'interprétation rédigé par l'IA (E2), plusieurs formulations à resserrer (P1, P2, P3), 12 pages pour 6-8. |
| Annexes | 9/10 | Générées depuis les CSV, donc fidèles ; tableaux lisibles. |

## 8. Les 10 corrections les plus importantes, dans l'ordre

1. **Chapitre 4 (E2)** : relire et réécrire chaque paragraphe d'interprétation avec ses propres mots (garder / couper / contredire). C'est l'exigence ECE la plus risquée.
2. **Déclaration d'usage de l'IA (E1)** : ne déclarer comme vérifié que ce qui l'a été ; accorder « a relu et validé l'ensemble du texte » avec la réalité du chapitre 4.
3. **Chapitre 2, 2.7 (E3)** : corriger la phrase sur la date des données de E17 et E18 (le pré-enregistrement honnête est une force du mémoire ; une inexactitude vérifiable dans git l'affaiblirait).
4. **Bouillot et al. (P4)** : relire une dernière fois les cinq affirmations qui fondent la critique (marche aléatoire, 7,3 pb, R², 1 variable sur 50, Belgique/Espagne).
5. **Chapitre 2, 2.2.2 (E4)** et **2.6.5 (E7)** : corriger la fourchette « −902 % à +1 789 % » et les « 10 tirages ».
6. **Chapitre 3, 3.4 (E5, E6)** et **tableau 3.1 (P5)** : préciser les trois formulations.
7. **Chapitre 4 (P1, P2, P3)** : alpha sur M0 et M1, « sans que les dépenses y apportent un gain significatif », Garlanda-Longueville aligné sur le chapitre 1.
8. **Introduction (P7)** : ajouter les sources du déficit et des dégradations de note.
9. **Longueurs** : si le temps le permet, déplacer en annexe le détail des tableaux 3.4 et 3.6 (chapitre 3) ; sinon le déclarer dans les remarques à l'encadrante.
10. **Détails de cohérence** : p de 0,36/0,37 pour E15 (P8), section 2.8 annoncée, « quatre/cinq contrôles » (P9), dépôt « accessible sur demande » (P10), virgules décimales dans les figures, format des références, et contrôle final de la mise en forme Word contre le guide (police, interligne, marges, numéros de page).

## 9. Reproduire les vérifications principales

```bash
# Chapitre 2 : chiffres de construction des variables (rapport 6,3 ; -902 / +1789 ; -462)
python - <<'EOF'
import importlib.util, pandas as pd
spec = importlib.util.spec_from_file_location("b02", "src/02_build_dataset.py")
B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
cum = pd.concat([B.read_budget_file(B.RAW/"budget"/f) for f in B.BUDGET_FILES]).sort_index() / 1e9
is_ = cum["Impôt sur les sociétés"]; g = (is_ / is_.shift(12) - 1) * 100
print(g.min(), g.max(), g[g.index.month == 1].min(), g[g.index.month == 1].max())
EOF
# Dates du pré-enregistrement
git log --format='%h %ad %s' --date=format:'%m-%d %H:%M' -- docs/plan_extensions.md results/tables/extensions/E15.csv results/tables/extensions/E17.csv
# Références citées dans le PDF : toutes les notices [1] à [37] sont citées (extraction de texte du PDF)
```

## 10. Corrections appliquées (01/10/2026, commits suivants de la branche)

**Appliquées** (exports `redaction/*.md` ; à reporter dans les documents Claude Docs, source de vérité) :
E1 (déclaration IA, formulation prudente **à valider par Elyamine** : liste exacte des articles relus ; la phrase « a relu et validé l'ensemble du texte » est inchangée et n'est vraie que si le chapitre 4 a été relu), E3, E4, E5, E6, E7, P1, P2, P3 (chapitre 4 : précisions factuelles seulement, aucune nouvelle interprétation), P5, P7, P8 (`CLAUDE.md` : p = 0,37), P9 ; fourchette périmée de la corrélation partielle dans `src/21_verif_chiffres_03.py` (relancé : seules ces trois lignes de `verif_chiffres_03.csv` changent, `conforme = True`).
**Figures** : nouveau module `src/fr_format.py` ; figures 3.1 (distributions), 3.2 et 3.3 régénérées avec la virgule décimale (`03`, `04 --from-saved`, `07`). Aucun CSV de résultats ne change ; `tests/verifications.py` et `tests/check_claude_md.py` passent.

**Non appliquées** (décision de l'auteur ou impossible ici) : E2 (réécriture du chapitre 4 par Elyamine), P4 (relecture des articles : réseau bloqué), P6 (verdicts du tableau 3.8), P10 (dépôt public ou privé), longueurs des chapitres 2 à 4, format des références, mise en forme du Word. Le Word et le PDF de `redaction/build/` ne sont **pas reconstruits** (`pandoc` absent de cette session) : il faut reporter les corrections dans Claude Docs puis relancer la chaîne décrite dans `redaction/README.md`.
