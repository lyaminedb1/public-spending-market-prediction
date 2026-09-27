# Contexte du projet — Mémoire MSc (ECE Paris)

## Le mémoire
- **Titre validé** : « Prédiction d'indicateurs des marchés financiers à partir des données de dépenses publiques ouvertes : une approche par machine learning »
- **Problématique validée** : Peut-on prédire des indicateurs des marchés financiers à partir des données de dépenses publiques ouvertes en utilisant des techniques de machine learning ?
- **Auteur** : Abdellah Elyamine DALI BRAHAM — MSc Data Management & IA, ECE Paris
- **Encadrante** : Dr. Yosra Hajjaji
- **Date limite de remise** : 10 octobre 2026
- **Langue de rédaction** : français. Rédaction finale prévue en LaTeX.

## Périmètre (décidé, ne pas changer sans accord)
- **Pays** : France. **Fréquence** : mensuelle. **Période** : 2013 à aujourd'hui (environ 150 mois).
- **Trois variables cibles** (horizon : mois suivant, t+1) :
  1. Variation mensuelle du spread OAT–Bund 10 ans (en points de base) — cible principale
  2. Variation mensuelle du taux OAT 10 ans (en points de base)
  3. Rendement mensuel du CAC 40 (en %)
  Variante secondaire : classification hausse/baisse.
- Les cibles sont fixées a priori. Ne pas choisir les cibles en fonction des corrélations observées (data snooping).

## Variables explicatives
- **Principales — dépenses de l'État** (situation mensuelle budgétaire, séries longues, data.economie.gouv.fr, jan. 2013 – juil. 2026) : dépenses par titre (personnel, fonctionnement, charge de la dette, investissement, intervention) et prélèvements sur recettes. Pas de ventilation par mission dans ces fichiers. Les opérations financières sont exclues (montants irréguliers, pas une dépense économique).
- **Contrôles** : recettes, solde d'exécution, valeur passée de la cible, taux directeurs BCE (MRO, facilité de dépôt), taux Bund, VIX (aversion au risque), inflation France (IPCH).

## Règles de construction des données
- Les montants budgétaires sont **cumulés depuis janvier** : les différencier pour obtenir des flux mensuels.
- Forte saisonnalité : deux transformations par ligne budgétaire : somme glissante sur 12 mois (`_12m`, Md€) et écart du cumul depuis janvier par rapport au même mois de l'année précédente, en % du total annuel (`_ytd_gap`). Pas de taux de croissance du cumul : il explose en début d'année (base proche de zéro).
- **Décalage de publication** : la situation du mois M est publiée début M+2 (juin 2026 publié le 4 août 2026 ; janv. 2023 le 2 mars ; déc. 2024 le 4 févr. 2025 ; vérifié lors de la revue du 27/09).
- **Inflation (IPCH) décalée d'1 mois** (correction de la revue du 27/09) : l'IPCH définitif du mois t paraît mi-t+1 ; même règle qu'E16/E20. Effet sur 04_models : R² bougent de quelques points, conclusions inchangées (meilleur R² -1,0 %, DM M1 vs M0 p ≥ 0,33). À la fin du mois t, seul le budget de t-2 est connu : les variables budgétaires sont décalées de 2 mois (`BUDGET_LAG = 2`). Sinon biais d'anticipation (look-ahead bias).
- Décembre : version provisoire puis définitive (révisions, à mentionner comme limite).
- OAT/Bund FRED = moyennes mensuelles (OCDE). CAC 40 `^FCHI` = indice de prix, hors dividendes.

## Jeu de données construit
- `python src/02_build_dataset.py` → `data/processed/dataset_monthly.csv` : 150 mois (2014-03 → 2026-08), 149 avec cible. Préfixe `y_` = cibles, `b_` = budget (décalé de 2 mois), le reste = marchés et contrôles en t.
- Vérification : les soldes annuels reconstitués correspondent aux chiffres officiels (-85,6 Md€ en 2014, -178,1 en 2020, -173,0 en 2023, -155,9 en 2024).
- Taux OAT/Bund = moyennes mensuelles : les variations de moyennes sont mécaniquement un peu autocorrélées (à signaler, et raison de toujours inclure la variation passée).

## Analyse exploratoire (`python src/03_exploration.py`)
- Figures : `results/figures/fig3_1_*.png` ; tableaux : `results/tables/eda_*.csv`.
- Cibles stationnaires (ADF p < 0,01) ; niveaux (spread, OAT, solde, charge de la dette) non stationnaires → on modélise des variations.
- Autocorrélation d'ordre 1 : Δspread 0,14 ; ΔOAT 0,23 ; CAC 40 -0,09.
- Corrélations de Spearman budget (t-2) / cibles (t+1), seuil 5 % = ±0,16 : spread → seul l'investissement (-0,16) ; ΔOAT → personnel 0,23, charge de la dette 0,21, fonctionnement 0,17, mais ces liens tombent à 0,07–0,13 une fois l'inflation contrôlée (confusion avec le régime d'inflation 2022-2023) ; CAC 40 → rien de significatif.
- Les niveaux `_12m` (Md€) sont non stationnaires (ADF p > 0,7) et produisent des corrélations fallacieuses avec l'OAT (jusqu'à 0,34, tendance commune) → **dans les modèles, utiliser les `_ytd_gap`, pas les `_12m`**. Les `_ytd_gap` sont proches de la stationnarité (p 0,01–0,06).
- Notebook pédagogique : `notebooks/03_EDA.ipynb` (généré par `src/make_eda_notebook.py`).
- Conclusion d'étape : signal budgétaire faible et en partie confondu avec l'inflation → l'inflation doit rester dans le modèle « contrôles seuls ».

## Modèles et évaluation
- Modèles : naïf (marche aléatoire / moyenne), régression linéaire avec retards, forêt aléatoire, XGBoost. **Pas de deep learning** (trop peu d'observations).
- Comparaison clé : modèle « contrôles seuls » contre « contrôles + dépenses ».
- Validation glissante (walk-forward), jamais de validation croisée aléatoire.
- Métriques : RMSE, MAE, taux de bonne direction ; test de Diebold-Mariano.
- Importance des variables : SHAP ou permutation importance.

## Résultats de la modélisation (`python src/04_models.py`, ~5 min)
- Jeux de variables emboîtés : M0 marchés (11 var.) ; M1 = M0 + 7 dépenses `_ytd_gap` ; M2 = M1 + recettes et solde. Test H1 = M1 vs M0.
- Hyperparamètres fixés a priori (Ridge : alpha par RidgeCV ; RF : 300 arbres, profondeur 4 ; XGB : 200 arbres, profondeur 2, lr 0,05).
- Validation glissante, fenêtre croissante, test 2020-01 → 2026-07 (79 mois).
- *Chiffres de cette section à jour après la correction de l'inflation (27/09, commit f1f834c).*
- **Aucun modèle ne bat la moyenne historique** (R² hors échantillon < 0 partout ; meilleur : Ridge M0 sur CAC 40, -1,0 %, était -0,3 % avant correction). Même un AR(1) simple fait -2 à -3 % (tests depuis 2020 et depuis 2017) → pas un bug, imprévisibilité mensuelle (Welch & Goyal 2008).
- **H1 rejetée** : ajouter les dépenses n'améliore aucune cible (DM M1 vs M0 : p bilatérale 0,33 à 0,99).
- **H2 non testable** en l'état (pas d'apport à comparer).
- **H3 rejetée** : XGBoost est le pire (RMSE +13 à +16 % vs moyenne ; significativement pire que Ridge sur le CAC 40, p 0,02) ; la forêt aléatoire n'est pas significativement meilleure que Ridge. XGBoost instable : R² OAT -22 % → -30 % pour le seul décalage de l'inflation (une seule graine ; à examiner dans la revue de 04).
- **H4** : en échantillon (SHAP), les dépenses pèsent 31 à 37 % de l'importance (intervention et investissement en tête) mais cela ne se traduit pas hors échantillon → surapprentissage : point clé de la discussion.
- Sorties : `results/tables/models_*.csv`, figures `fig3_2_rmse_relatif`, `fig3_3_importance_shap`, `fig3_4_previsions_spread`.

## Extensions pré-enregistrées (`docs/plan_extensions.md`, commit b136e8f avant exécution)
> ⚠️ **Chiffres E1-E13 et BH ci-dessous = ANCIEN jeu de données** (avant correction de l'inflation). Ne pas les citer : relancer `05`, `06`, `06 resume`, `07` à la fin de la revue, puis mettre à jour.
- `python src/05_extra_features.py` (surprise budgétaire vs LFI, notations) puis `python src/06_extensions.py` (~35 min) puis `python src/07_extensions_summary.py`.
- Sorties : `results/tables/extensions/E*.csv`, `results/tables/ext_summary.csv` (123 comparaisons avec/sans dépenses + 36 ventilations E12), `results/tables/ext_synthese.csv`, figure `fig3_5_extensions.png`.
- **Résultat : 0 comparaison significative après correction Benjamini-Hochberg (10 %)** ; 2 p brutes < 0,05 sur 123 (≈ 6 attendues par hasard).
- Ce qui bat la moyenne historique, **sans les dépenses** : volatilité (E3 : CAC 40 +9,3 %, OAT +3 à +4,5 %), classification OAT (E2 : score de Brier +5 à +7 %), spread à 3 mois (RF M0 +3,1 %), CAC à 12 mois (XGB M0 +14 %, 68 obs. chevauchantes, fragile).
- Surprise budgétaire (E4) : LFI 2026 absente de l'open data → test jusqu'à 2026-02 ; aucun apport.
- Notations (E13) : 9 dégradations 2013-2025 (`data/raw/ratings_france.csv`, sources en lien) ; aucun apport.
- Contrôle anti-fuite vérifié : pour l'horizon h, la dernière ligne d'entraînement est toujours ≥ h mois avant le mois de test.
- Conclusion : résultat négatif robuste à 13 variantes.

## Panel européen E15/E16 (`python src/11_panel_models.py`, ~16 min ; collecte `09_collect_panel.py`, `10_collect_large.py`)
- FRED bloque `requests` depuis le 27/09 : téléchargement via `curl` (`src/fred_http.py`). 68 séries (6 pays × 9 + 14 mondiales), Eurostat gov_10q_ggnfa.
- **E15** (trimestriel, 5 pays, test 2010T1-2026T2, 330 obs.) : Ridge M0 +13,9 %, M1 +15,5 % vs moyenne, MAIS diagnostic non pré-enregistré (`src/12_diag_e15.py`) : c'est l'autocorrélation mécanique des variations de moyennes trimestrielles (AR1 0,32 vs 0,07 en fin de trimestre, Working 1960). En fin de trimestre : tout négatif (M0 -4,1 %, M1 -2,9 %). Dépenses : +4 pts en 2010-2014 (crise), -13 pts après 2015 → piste « effet en période de crise » (Afonso et al. 2015), non significatif (p 0,37).
- **E16** (mensuel, 5 pays, 150 variables dont 18 finances publiques, test 2012-01 → 874 obs.) : niveau du spread R² 90-97 % vs moyenne (comme Bouillot et al.) mais **tous les modèles perdent contre la marche aléatoire** (niveau : XGB -31 %, RF -140 %, Ridge -232 % ; RMSE XGB 21,1 pb vs 18,4 pb). Variation : R² négatif partout. Finances publiques : aucun apport (p 0,08-0,88). *À jour après correction des décalages macro (27/09, commit 62b067b).*
- **E17** panel annuel (déc., 75 prév.) : tous < moyenne (-20 à -338 %) et < marche aléatoire ; RF M1 moins mauvais que M0 (p 0,04) mais toujours perdant.
- **E18** régime de crise (fin de trimestre, exploratoire) : les interactions dépenses × tension dégradent partout ; le « +4 pts en crise » d'E15 disparaît sans moyennes.
- **E19** actions sectorielles (excès vs CAC 40, BTP : Vinci/Eiffage/Bouygues ; défense : Thales/Dassault) : tout < moyenne sauf RF BTP h=3 sans dépenses (+1,4 % ; avec : -0,7 %) ; défense h=3 : dépenses moins mauvaises (RF p 0,06, XGB p 0,008) mais R² -11 à -20 %. *À jour (27/09, commit 62b067b : mois incomplet retiré + inflation corrigée ; effets des deux corrections non séparés).*
- **E20** incertitude politique (indice **européen**, écart déclaré : France absente de FRED) : ni l'EPU ni les dépenses n'aident. ⚠️ *Ancien jeu de données, à relancer.*
- E14 (étude d'événement) : taux quotidiens introuvables par script (BCE 404, stooq bloqué) → perspectives.
- ⚠️ *BH ci-dessous = ancienne version (E19 et E16 ont changé depuis ; E1-E13 et E20 à relancer). À recalculer avec `06_extensions.py resume` en fin de revue.*
- **BH sur 168 comparaisons** (E12 et ventilations exclues) : 0 significative (p_BH min 0,84) ; 6 p brutes < 0,05 (≈ 8 attendues par hasard), toutes des cas où le modèle avec dépenses reste sous la moyenne. 6 cas où « avec dépenses » bat la moyenne et la version sans, tous non significatifs (E2/E3 RF +1 à +2 pts, E15 = artefact des moyennes). `python src/06_extensions.py resume` recalcule la correction.
- Message clé : un R² de 95 % sur le niveau n'est pas une prévision ; la comparaison à la marche aléatoire est indispensable (critique de Bouillot et al.).

## Hypothèses
- H1 : pour au moins un indicateur, ajouter les dépenses améliore la prévision.
- H2 : l'apport décroît du spread, au taux OAT, puis au CAC 40.
- H3 : forêt aléatoire / XGBoost font mieux que les modèles linéaires.
- H4 : parmi les dépenses, la charge de la dette et les dépenses d'intervention sont les plus prédictives.
- Un résultat négatif pour H1 est plausible (efficience des marchés, Fama 1970 ; anticipation, Ramey 2011) et reste valable.

## Décision bibliographie (27/09/2026, à appliquer au chapitre 1)
- Priorité aux études **européennes** ; ~10 sources principales, le reste en soutien méthodologique court.
- Noyau européen : Bouillot, Candelon & Kool (2025) ; Afonso, Arghyrou & Kontonikas (2015) ; Bernoth, von Hagen & Schuknecht (2012) ; Belly et al. (2023) ; Garlanda-Longueville (2023, France) ; Attinasi, Checherita & Nickel (2009) ; Favero (2013) ; Barbier-Gauchard & Sofianos (2025).
- Cadre théorique (américain mais général) : Fama (1970), Ramey (2011), Welch & Goyal (2008).
- Soutien bref : Diebold-Mariano, Bailey et al., Breiman, Chen-Guestrin, Croushore, Giannone et al., Janssen et al. ; raccourcir Blanchard-Perotti, Laubach, Afonso-Sousa, Medeiros, Gu-Kelly-Xiu, Bianchi.
- Ajouter dans 1.4 : domination des études américaines → la France est peu étudiée (fait partie du vide) ; colonne « Pays » et séparation noyau / cadre / méthode dans le tableau 1.1.
- Brouillon du chapitre 1 : `/home/claude/memoire/chapitre1.md` (hors dépôt) et Claude Docs https://claude.ai/code/artifact/8e4a6819-0106-4901-acda-9eddf1735daa ; chapitre 2 : https://claude.ai/code/artifact/7744f999-cd6d-4e6a-a73b-c204c41ba55b.

## Revue du code (27/09 soir) — état
- **Préparation des données revue en entier** (01, 02, 05, 08, 09, 10, 13 + préparation dans 11 et 14). Corrections :
  1. `02` : inflation (IPCH) décalée d'1 mois (commit f1f834c).
  2. `11` (E16) : production industrielle et chômage décalés de **2 mois** (publiés début m+2), au lieu d'1. Relancé : conclusions inchangées (finances publiques : p 0,08-0,88 ; tous < marche aléatoire).
  3. `14` (E19) : dernier mois des actions (sept. 2026, arrêté au 25/09) retiré car incomplet → 79 mois de test (h=1), 77 (h=3), conforme au protocole. Relancé : plus aucun cas « avec dépenses » > moyenne (RF BTP h=3 : -0,7 %) ; défense h=3 RF/XGB : dépenses moins mauvaises (p 0,06 / 0,008) mais R² -11 à -20 %.
  4. `08` (E14) : collecte ratée documentée (clés BCE 404 ; pages presse identiques, pagination en JavaScript). Sans effet : E14 non exécutée.
- Vérifié correct : notations E13 (9 dégradations), LFI E4, décalage Eurostat 2 trimestres (E15-E18), EPU E20 décalé. Délais sourcés : IPI INSEE juillet 2025 paru le 09/09/2025, chômage zone euro juillet 2025 le 01/09/2025 (→ 2 mois dans E16).
- **Non vérifié** : dates de publication de la SMB 2014-2019 (archives inaccessibles ; décalage de 2 mois vérifié seulement sur 2023-2026) ; estimation provisoire de l'IPCH en fin de mois par l'INSEE (non sourcée).
- Attention à l'argument : corriger une fuite ne rend pas forcément les modèles moins bons (Ridge M1 ΔOAT : -15,1 % → -10,9 % après correction de l'inflation). On corrige parce que c'est une erreur de méthode, quel que soit l'effet.
- Contrôles automatiques : `python tests/verifications.py` (alignement des cibles, décalages, doublons, mois incomplets).
- **Limites à écrire** : données budgétaires révisées (vintage final) ; cibles taux en moyennes mensuelles ; `_ytd_gap` de variance croissante sur l'année (×6 janv.→déc.) ; E16 : 25/68 séries OCDE MEI arrêtées sur FRED fin 2022-début 2024 → 23,6 % de valeurs imputées (médiane) sur les 144 dernières lignes de test ; E19 : prix hors dividendes (détachements à dates différentes du CAC 40).
- **À relancer une fois la revue finie** (lisent `dataset_monthly.csv` corrigé) : `03_exploration`, `05`, `06_extensions` (E1-E13), `14` E20, puis `06_extensions.py resume` (BH) et `07`. E16 et E19 sont déjà à jour.
- Reste à revoir : `03_exploration` (chiffres cités dans le mémoire), `04_models` (prévu le 28/09), `06_extensions` (dont `walk_forward` qui compte en lignes et non en mois), modèles de `11` et `14`.

## Prochaines étapes (au 27/09 soir)
0. **D'abord : revue du code pas à pas** (demande d'Elyamine) — 02_build_dataset → 04_models → 06/11/14 : vérifier construction des variables, décalages, absence de fuite, validation glissante, hyperparamètres, métriques, DM et BH ; expliquer chaque choix de ML ; corriger tout bug trouvé et relancer. Toute modification doit être justifiée par une erreur de méthode, pas par le résultat obtenu. La conclusion « négative » n'est pas rédigée avant cette revue ; chapitre 1 (liste des sources) en attente.
1. Restructurer le chapitre 1 selon la décision ci-dessus.
2. Rédiger le chapitre 3 (Résultats, 4-6 p.) : 3.1 descriptif, 3.2 modèles principaux (H1, H3, H4), 3.3 extensions (tableau de synthèse + fig3_5, détail en annexe), 3.4 panel européen et marche aléatoire.
3. Chapitre 4 (Discussion) : ce qui fait bouger le spread (10 plus gros mois : Covid 03/2020, présidentielle 2017, dissolution 06/2024, Trump 11/2016, Ukraine 02/2022… aucun lié au budget ; dates à vérifier), critique de Bouillot et al., artefact des moyennes, limites, perspectives (étude d'événement E14, annonces PLF).

## Référence la plus proche
Bouillot, Candelon & Kool (2025), *Forecasting European sovereign spreads using machine learning*, UCLouvain : prévision à un mois des spreads de 10 pays dont la France, XGBoost en tête, le spread passé domine.

## Structure du dépôt
- `data/raw/` : données brutes (`src/01_collect_data.py` télécharge FRED, BCE, CAC 40) ; `data/raw/budget/` : CSV budgétaires téléchargés à la main.
- `data/processed/` : jeu de données mensuel nettoyé.
- `notebooks/` : 01_collecte, 02_nettoyage, 03_exploration, 04_modeles.
- `src/` : scripts et fonctions réutilisables.
- `results/figures/` : graphiques pour le mémoire ; `results/tables/` : tableaux.

## Guide ECE de rédaction (Student Guide for Dissertation 2025-2026)
- Ordre : page de titre (titre, nom complet, ECE, MSc Data Management & IA, encadrante, mois/année) · remerciements · résumé 150-300 mots + 5-7 mots-clés · sommaire · listes des figures et des tableaux · abréviations · glossaire · Introduction (3-5 p.) · État de l'art (10-15 p., ≥ 10 sources académiques, finir sur le manque/gap) · Méthodologie (5-8 p., inclure considérations éthiques) · Résultats (**4-6 p., sans interprétation**) · Discussion (6-8 p. : implications, limites, recherches futures) · Conclusion (2-3 p.) · Références (APA, IEEE ou Harvard, ordre alphabétique) · Annexes.
- Mise en forme : Times New Roman ou Arial 12, double interligne (tableaux/notes/références simple), marges 2,54 cm, numéros de page en bas au centre ou en haut à droite ; titre niveau 1 centré gras, niveau 2 aligné à gauche gras, niveau 3 en retrait gras terminé par un point ; figures/tableaux numérotés par chapitre avec source.
- **IA** : déclarer l'usage des outils d'IA (méthodologie ou remerciements) ; interdit de rendre des hypothèses, interprétations ou paragraphes générés par IA sans relecture critique et apport personnel.
- Remise en PDF par e-mail à l'encadrante et au responsable du MSc ; retard = note F. Date du guide (15/09/2026) reportée au **10 octobre 2026** (confirmé par Elyamine) ; rédaction en français. Soutenance 20-30 min (10-20 min de présentation + 10-15 min de questions). Écrit 50 % / oral 50 %.
- Conséquence : les 20 extensions tiennent dans les Résultats sous forme d'un tableau de synthèse + figure ; le détail va en annexe ; les diagnostics (moyennes trimestrielles, marche aléatoire) sont interprétés dans la Discussion.

## Plan du mémoire
Introduction · Ch.1 État de l'art (rédigé) · Ch.2 Données et méthodologie · Ch.3 Résultats · Ch.4 Discussion · Conclusion · Bibliographie · Annexes.
