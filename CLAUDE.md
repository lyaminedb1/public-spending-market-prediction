# Contexte du projet — Mémoire MSc (ECE Paris)

## Le mémoire
- **Titre validé** : « Prédiction d'indicateurs des marchés financiers à partir des données de dépenses publiques ouvertes : une approche par machine learning »
- **Problématique validée** : Peut-on prédire des indicateurs des marchés financiers à partir des données de dépenses publiques ouvertes en utilisant des techniques de machine learning ?
- **Auteur** : Abdellah Elyamine DALI BRAHAM — MSc Data Management & IA, ECE Paris
- **Encadrante** : Dr. Yosra Hajjaji
- **Date limite de remise** : **vendredi 2 octobre 2026, minuit** (le report au 10/10 a été refusé, info du 30/09)
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
- **Décalage de publication** : la situation du mois M est publiée début M+2 (juin 2026 publié le 4 août 2026 ; janv. 2023 le 2 mars ; déc. 2024 le 4 févr. 2025 ; vérifié lors de la revue du 27/09). À la fin du mois t, seul le budget de t-2 est connu : les variables budgétaires sont décalées de 2 mois (`BUDGET_LAG = 2`). Sinon biais d'anticipation (look-ahead bias).
- **Inflation (IPCH) décalée d'1 mois** (correction de la revue du 27/09) : l'INSEE publie une estimation provisoire en fin de mois t (août 2026 : le 28/08) et l'IPCH définitif mi-t+1 (août 2026 : le 15/09) ; les données FRED/Eurostat sont les valeurs définitives → décalage d'1 mois, même règle qu'E16/E20. Effet sur 04_models : R² bougent de quelques points, conclusions inchangées.
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
- Corrélations de Spearman budget (t-2) / cibles (t+1), seuil 5 % = ±0,16 : spread → seul l'investissement (-0,16) ; ΔOAT → personnel 0,23, charge de la dette 0,21, fonctionnement 0,17, mais ces liens tombent à 0,15 (personnel), 0,09 (fonctionnement) et 0,10 (charge de la dette) une fois l'inflation et la ΔOAT passée contrôlées (confusion avec le régime d'inflation 2022-2023) ; CAC 40 → rien de significatif (max 0,125).
- Les niveaux `_12m` (Md€) sont non stationnaires (ADF p de 0,23 à 1,00 ; > 0,7 pour 10 lignes sur 12) et produisent des corrélations fallacieuses (jusqu'à 0,34 avec la ΔOAT du mois suivant, 0,85 avec le niveau de l'OAT : tendance commune) → **dans les modèles, utiliser les `_ytd_gap`, pas les `_12m`**. Les `_ytd_gap` sont stationnaires ou presque (ADF p de 0,000 à 0,057 ; seules les dépenses totales dépassent 0,05).
- Chiffres recalculés par script : `python src/21_verif_chiffres_03.py` → `results/tables/diag_04/verif_chiffres_03.csv`.
- Corrélations partielles (inflation + variation passée de la cible, comme dans M0) aussi produites par `03_exploration.py` → `results/tables/eda_correlations_partielles.csv` (ΔOAT : personnel 0,147 p 0,075 ; fonctionnement 0,094 ; charge de la dette 0,098 ; spread : investissement -0,153 p 0,064). Attention : ne contrôler que l'inflation donne 0,11-0,165 (personnel p 0,046) ; la version retenue est celle qui correspond à M0.
- Notebook pédagogique : `notebooks/03_EDA.ipynb` (généré par `src/make_eda_notebook.py`).
- Conclusion d'étape : signal budgétaire faible et en partie confondu avec l'inflation → l'inflation doit rester dans le modèle « contrôles seuls ».

## Modèles et évaluation
- Modèles : naïf (marche aléatoire / moyenne), régression linéaire avec retards, forêt aléatoire, XGBoost. **Pas de deep learning** (trop peu d'observations).
- Comparaison clé : modèle « contrôles seuls » contre « contrôles + dépenses ».
- Validation glissante (walk-forward), jamais de validation croisée aléatoire.
- Métriques : RMSE, MAE, taux de bonne direction ; test de Diebold-Mariano.
- Importance des variables : SHAP (en échantillon) et permutation hors échantillon (`17_permutation_oos.py`, ajout post hoc).

## Résultats de la modélisation (`python src/04_models.py`, ~10 min)
- Jeux de variables emboîtés : M0 marchés (11 var.) ; M1 = M0 + 7 dépenses `_ytd_gap` ; M2 = M1 + recettes et solde. Test H1 = M1 vs M0.
- Hyperparamètres fixés **sans optimisation sur la période de test, à des valeurs usuelles** (RF : 300 arbres, profondeur 4 ; XGB : 200 arbres, profondeur 2, lr 0,05 ; Ridge : alpha par RidgeCV, grille 10⁻²–10⁶). Ne pas écrire « pré-enregistrés » : code et résultats de 04 ont été commités ensemble. La grille de Ridge a été élargie le 29/09 (elle était bornée à 1000, atteinte 75-99 % des mois pour le CAC 40) ; à 10⁶ la prévision Ridge égale la moyenne d'entraînement à 0,002 point près : rester à la borne signifie « aucun signal ».
- Validation glissante, fenêtre croissante, test 2020-01 → 2026-07 (79 mois ; 70 → 148 mois d'entraînement).
- *Tous les chiffres de cette section sont ceux de la relance complète du 29/09 (`./run_all.sh`), environnement figé dans `requirements.txt`.*
- **Aucun modèle ne bat la moyenne historique** (R² hors échantillon < 0 partout ; meilleur : Ridge M0 sur CAC 40, -1,3 % ; meilleurs par cible : spread -6,8 %, OAT -5,9 %, CAC 40 -1,3 %). Même un AR(1) simple fait -1,9 à -2,7 % → pas un bug, imprévisibilité mensuelle (Welch & Goyal 2008). La **variation nulle** bat la moyenne pour les taux (R² +1,7 % spread, +2,4 % OAT ; -0,2 % CAC 40) : référence la plus exigeante pour les taux (colonne `R2_vs_zero_%`, tests DM « vs variation nulle »).
- **H1 rejetée** : ajouter les dépenses n'améliore aucune cible (DM M1 vs M0 : p bilatérale 0,37 à 0,99) ; **correction BH sur les 18 tests M1/M2 vs M0 : p_BH minimale 0,81** (`p_BH_H1` dans `models_dm_tests.csv`). Robuste au décalage budgétaire : avec 1 ou 3 mois au lieu de 2, aucun R² positif et p_BH ≥ 0,51 (`results/tables/robustesse_lag.csv`).
- **H2 non évaluable** (rien à classer ; gains moyens de R² M1 vs M0 : spread +1,3, CAC 40 +0,2, OAT -0,03 point).
- **H3 rejetée** : XGBoost est le pire (RMSE +12,6 à +16,4 % vs moyenne ; significativement pire que Ridge sur le CAC 40, p bilatérale 0,032 ; OAT 0,055) ; la forêt aléatoire (+2,9 à +5,4 %) n'est pas significativement meilleure que Ridge. XGBoost instable : R² varie d'environ 9 points selon la graine (10 graines : -25 à -40 %), conclusions stables ; graine 42 déclarée.
- **H4 non soutenue** : en échantillon, les dépenses pèsent 31 à 37 % de la part SHAP, mais 7 variables de pur bruit obtiennent 34 à 38 % en moyenne (étendue 26-47 %) → la part SHAP ne montre aucune information ; en permutation hors échantillon, le groupe des dépenses a un ΔRMSE négatif pour les 6 combinaisons cible × modèle (XGBoost : z de -1,04 à -0,66 ; Ridge jusqu'à -1,64), comme le bruit ; le contrôle positif (signal fictif ρ = 0,5) ressort à +7,6 % / +18,8 % de RMSE. Aucun classement des dépenses (charge de la dette, intervention) n'est donc défendable.
- **Diagnostics de la revue de `04`** (`docs/revue_04_models.md`, `results/tables/diag_04/resume.csv`, 51 chiffres sur 53 conformes à la revue) : puissance faible (avec ρ = 0,3 le modèle bat la moyenne dans 20-30 % des tirages seulement ; avec ρ = 0,5, 80-100 %) → le résultat exclut un fort pouvoir prédictif, pas un effet faible ; les vraies dépenses font moins bien que 90-95 % des tirages de bruit avec Ridge ; Clark-West trop permissif (bruit « significatif » dans 25-75 % des cas contre 0-5 % pour DM) → on garde DM.
- Sorties : `results/tables/models_*.csv` (dont `models_permutation_oos.csv`, `hypotheses.csv` : tableau H1-H4 généré par `18_hypotheses.py`), figures `fig3_2_rmse_relatif` (avec repère « variation nulle »), `fig3_3_importance_shap` (avec bande de bruit), `fig3_4_previsions_spread`.

## Extensions pré-enregistrées (`docs/plan_extensions.md`, commit b136e8f avant exécution)
> Chiffres à jour (relance complète du 29/09).
- `python src/05_extra_features.py` (surprise budgétaire vs LFI, notations) puis `python src/06_extensions.py` (E1-E13, ~1 h) puis `python src/07_extensions_summary.py`.
- Sorties : `results/tables/extensions/E*.csv`, `results/tables/ext_summary.csv` (210 comparaisons dont 168 dans la correction BH), `ext_synthese.csv`, `ext_significatifs.csv`, figures `fig3_5_extensions.png` (3 cibles françaises) et `fig3_6_extensions_autres.png` (panel et actions).
- **Résultat : 0 comparaison significative après correction Benjamini-Hochberg (10 %) sur 168 comparaisons** ; 6 p brutes < 0,05 (≈ 8 attendues par hasard), **toutes des cas où le modèle avec dépenses reste sous la moyenne historique** (il fait moins mal que la version sans : E19 défense h=3 XGBoost p 0,008 ; E1 spread h=12 XGBoost 0,013 ; E11 CAC 40 XGBoost 0,024 ; E1 CAC 40 h=6 XGBoost 0,027 ; E17 RF 0,039 ; E15 XGBoost 0,047). p_BH = 0,999 pour tous.
- Ce qui bat la moyenne historique, **sans les dépenses** : volatilité (E3 : CAC 40 +9,6 %, OAT +3,3 %), classification OAT (E2 : score de Brier +2,5 %, +5,8 % avec dépenses, non significatif), spread à 3 mois (E1 : +2,3 %), CAC 40 à 12 mois (E1 : +11,8 %, 68 obs. chevauchantes, fragile), BTP h=3 (E19 : +1,4 % ; avec dépenses -0,7 %).
- Surprise budgétaire (E4) : LFI 2026 absente de l'open data → test jusqu'à 2026-02 (74 obs.) ; aucun apport.
- Notations (E13) : 9 dégradations 2013-2025 (`data/raw/ratings_france.csv`, sources en lien) ; aucun apport.
- Contrôle anti-fuite vérifié et automatisé (`tests/test_walk_forward_06.py`, `tests/test_tuned_xgb.py`) : pour l'horizon h, la dernière ligne d'entraînement est toujours ≥ h mois avant le mois de test ; le réglage d'E10 ne voit jamais le mois prévu.
- Conclusion : résultat négatif robuste à 13 variantes.

## Panel européen E15/E16 (`python src/11_panel_models.py`, ~16 min ; collecte `09_collect_panel.py`, `10_collect_large.py`)
- FRED bloque `requests` depuis le 27/09 : téléchargement via `curl` (`src/fred_http.py`). 68 séries (6 pays × 9 + 14 mondiales), Eurostat gov_10q_ggnfa.
- **E15** (trimestriel, 5 pays, test 2010T1-2026T2, 330 obs.) : Ridge M0 +13,9 %, M1 +15,5 % vs moyenne, MAIS diagnostic non pré-enregistré (`src/12_diag_e15.py` → `results/tables/diag_e15.csv`, `diag_e15_ar1.csv`) : c'est l'autocorrélation mécanique des variations de moyennes trimestrielles (AR1 0,32 vs 0,07 en fin de trimestre, Working 1960). En fin de trimestre : tout négatif (M0 -4,1 %, M1 -2,9 %). Dépenses : +4 pts en 2010-2014 (crise), -13 pts après 2015 → piste « effet en période de crise » (Afonso et al. 2015), non significatif (p 0,36).
- **E16** (mensuel, 5 pays, 150 variables dont 18 finances publiques, test 2012-01 → 874 obs.) : niveau du spread R² 92-97 % vs moyenne (comme Bouillot et al.) mais **tous les modèles perdent contre la marche aléatoire** (niveau : XGB -31 %, RF -142 %, Ridge -232 % ; RMSE XGB 21,1 pb vs 18,4 pb). Variation : R² négatif partout. Finances publiques : aucun apport (p 0,08-0,81). *À jour après correction des décalages macro (27/09) et relance dans l'environnement figé (29/09).*
- **E17** panel annuel (déc., 75 prév.) : tous < moyenne (-20 à -338 %) et < marche aléatoire ; RF M1 moins mauvais que M0 (p 0,04) mais toujours perdant.
- **E18** régime de crise (fin de trimestre, exploratoire) : les interactions dépenses × tension dégradent partout ; le « +4 pts en crise » d'E15 disparaît sans moyennes.
- **E19** actions sectorielles (excès vs CAC 40, BTP : Vinci/Eiffage/Bouygues ; défense : Thales/Dassault) : tout < moyenne sauf RF BTP h=3 sans dépenses (+1,4 % ; avec : -0,7 %) ; défense h=3 : dépenses moins mauvaises (RF p 0,06, XGB p 0,008) mais R² -11 à -20 %. *À jour (mois incomplet retiré, inflation corrigée, grille Ridge élargie : lignes RF/XGBoost identiques, Ridge ±3 points au plus).*
- **E20** incertitude politique (indice **européen**, écart déclaré : France absente de FRED) : ni l'EPU ni les dépenses n'aident (meilleur R² -0,28 %, p brute minimale 0,134). *Relancé le 29/09 sur les données corrigées.*
- E14 (étude d'événement) : taux quotidiens introuvables par script (BCE 404, stooq bloqué) → perspectives.
- **BH sur 168 comparaisons** (E12 et ventilations exclues) : voir la section précédente (0 significative ; `python src/06_extensions.py resume` recalcule la correction). Les 6 « avec dépenses meilleur que sans » à p brute < 0,05 restent tous sous la moyenne historique.
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

## Revue du code — état au 29/09 (code terminé)
- **Préparation des données revue en entier** (01, 02, 05, 08, 09, 10, 13 + préparation dans 11 et 14). Corrections :
  1. `02` : inflation (IPCH) décalée d'1 mois (commit f1f834c).
  2. `11` (E16) : production industrielle et chômage décalés de **2 mois** (publiés début m+2), au lieu d'1. Conclusions inchangées.
  3. `14` (E19) : dernier mois des actions (sept. 2026, arrêté au 25/09) retiré car incomplet → 79 mois de test (h=1), 77 (h=3).
  4. `08` (E14) : collecte ratée documentée (clés BCE 404 ; pages presse identiques, pagination en JavaScript). Sans effet : E14 non exécutée.
- **Revue de `04_models` (28/09) appliquée le 29/09** : grille RidgeCV élargie à 10⁶ (04 et 06 ; effet ≤ 1,2 point de R²) ; R² et DM aussi contre la variation nulle ; correction BH sur les 18 tests de H1 ; référence de bruit sur la figure SHAP ; H4 « non soutenue » (deuxième méthode : permutation hors échantillon) ; fourchettes par graine, puissance et taille de Clark-West dans `results/tables/diag_04/resume.csv` ; robustesse au décalage budgétaire de 1 et 3 mois (conclusions inchangées). Audit de `walk_forward` de 06 : jamais de fuite (avec des trous il est seulement plus prudent), 0 mois manquant sur les données réelles.
- Vérifié correct : notations E13 (9 dégradations), LFI E4, décalage Eurostat 2 trimestres (E15-E18), EPU E20 décalé. Délais sourcés : IPI INSEE juillet 2025 paru le 09/09/2025, chômage zone euro juillet 2025 le 01/09/2025 (→ 2 mois dans E16). IPCH provisoire INSEE fin de mois / définitif mi-t+1 ; Eurostat finances publiques trimestrielles publiées vers le 21-23 du 4e mois après le trimestre (→ 2 trimestres).
- **Non vérifié** : dates de publication de la SMB 2014-2019 (archives inaccessibles ; décalage de 2 mois vérifié seulement sur 2023-2026) → à écrire comme hypothèse ; la robustesse à 1 et 3 mois ne change pas les conclusions (aucun R² > 0, p_BH ≥ 0,51).
- Attention à l'argument : corriger une fuite ne rend pas forcément les modèles moins bons. On corrige parce que c'est une erreur de méthode, quel que soit l'effet.
- **Reproductibilité** : `./run_all.sh` (versions figées dans `requirements.txt`, données brutes gelées par `data/MANIFEST.csv`), 63 contrôles automatiques (`python tests/verifications.py`), deux relances complètes indépendantes identiques à 1e-9 près (les CSV ne sont pas identiques octet par octet : RF, sommation entre threads, écarts de 1e-15). **Les valeurs exactes de RandomForest/XGBoost dépendent des versions de scikit-learn/numpy** : sur la machine d'origine, 27 comparaisons d'extensions sur 159 différaient de plus de 5 points de R² (surtout E1 aux horizons longs) ; seules les conclusions se transfèrent. Ne pas citer de chiffres de RF/XGBoost issus d'un autre environnement.
- **Limites à écrire (chiffres reproduits par `src/20_limites_chiffres.py`)** : données budgétaires révisées (vintage final) ; cibles taux en moyennes mensuelles (AR(1) 0,146 Δspread, 0,236 ΔOAT ; en partie mécanique) ; `_ytd_gap` : l'écart-type de décembre est en médiane 6,3 fois celui de janvier (de 1,0 pour l'investissement à 12,4 pour la charge de la dette), dont environ la moitié est mécanique (flux i.i.d. : 3,7 ≈ √12) ; E16 : 25/68 séries OCDE MEI arrêtées sur FRED fin 2022-début 2024 → environ 23 % des cellules imputées (23,4 % en moyenne) sur les 144 dernières observations de test ; E19 : prix hors dividendes ; puissance faible (79 mois de test) ; variation du R² de plusieurs points selon la date de début de l'échantillon (M0 sans budget : jusqu'à 5,7 points de variation entre décalages) → les écarts de quelques points entre deux jeux ne sont pas interprétables.
- Plan du chapitre 4 (structure + faits sourcés, sans interprétation) : `docs/plan_chapitre4.md` (chiffres à recouper avec les CSV ci-dessus).
- Étapes de finalisation du code : `etapes/` (22 étapes, toutes faites ; chaque fichier consigne le résultat et les écarts au plan).

## Rédaction (état au 30/09)
- Liens Claude Docs : ch. 1 https://claude.ai/code/artifact/8e4a6819-0106-4901-acda-9eddf1735daa · ch. 2 https://claude.ai/code/artifact/7744f999-cd6d-4e6a-a73b-c204c41ba55b · ch. 3 https://claude.ai/code/artifact/8bb0b5ba-85e9-47e5-a6bd-df4fb6edf006.
- **Ch. 1** restructuré le 29/09 selon la décision bibliographie (1.1 cadre · 1.2 finances publiques et spreads · 1.3 ML · 1.4 données ouvertes · 1.5 synthèse, tableau 1.1). Résumés des articles : à vérifier sur les articles.
- **Ch. 2** à jour (grille Ridge 10⁶ ; corrélations partielles inflation + variation passée : 0,09 à 0,15). **Manque : considérations éthiques** (exigées par le guide ECE).
- **Ch. 3** rédigé le 29/09 (3.1 descriptif · 3.2 modèles, tab. 3.2-3.3 · 3.3 solidité, tab. 3.4 · 3.4 SHAP vs bruit, tab. 3.5 · 3.5 extensions + BH, tab. 3.6 · 3.6 panel, tab. 3.7 · 3.7 hypothèses, tab. 3.8). Environ 9 pages : à réduire à 4-6 (annexes). Ajouter : robustesse du décalage (1 et 3 mois), BH sur H1, permutation hors échantillon (H4).
- Exports Markdown des chapitres et outil de construction du Word (mise en forme ECE) : `redaction/` (voir `redaction/README.md`). Chapitre 1 vérifié contre les PDF des articles le 30/09 (corrigés : Garlanda-Longueville = communiqués annonçant les allocutions, pas des « fuites » ; Laubach ≈ 25 pb). Chapitre 4 (brouillon complet 4.1-4.6 le 30/09 soir, à réécrire par Elyamine) : https://claude.ai/code/artifact/1404f95c-5b3d-4674-b6bf-26bd0aac23d2.
- Fait pour la 4.4 : sur 2020-01 → 2025-02, la marche aléatoire (spread France, moyennes mensuelles OCDE) a un RMSE de 5,1 pb contre 7,3 pb pour le XGBoost de Bouillot et al. (tableau 11) ; définitions de série peut-être différentes. Chez Bouillot, 1 seule variable de finances publiques parmi les 50 principales (tableau 12).
- Revue externe de la rédaction : prompt dans `docs/prompt_revue_redaction.md`.
- 30/09 soir : grande revue du texte (2 relecteurs indépendants + seconde passe) ; corrigé : chiffres (tab. 3.6, 3.7, p E16 0,08-0,81, ADF, 63 contrôles, E17/E18), datation du test (prévisions faites de fin janv. 2020 à fin juil. 2026, variations de févr. 2020 à août 2026), « dix-neuf extensions réalisées » (E14 non faite), H1/H3 « non validées », 2.6.5 contrôles de solidité, BH sur p unilatérales, DM contre variation nulle (2/6 significatifs sur les taux), 4.5 Implications (limites → 4.6, futures → 4.7), formulations prudentes, abréviations, sources, annexes nettoyées. Reste : longueur (ch. 2 ≈ 15 p., ch. 3 ≈ 10, ch. 4 ≈ 10), virgule décimale dans les figures.
- 30/09 soir : mémoire complet assemblé (80 p.) : pages liminaires, introduction et conclusion (Claude Docs https://claude.ai/code/artifact/1d897e2d-db9f-4996-9856-02e4a42b31df), annexes générées depuis les CSV, sommaire et listes mis à jour par LibreOffice (`redaction/outils/maj_index_pdf.py`). Choix d'Elyamine pour la 4.1 : « pas de preuve (pour l'instant) » plutôt que « ne permettent pas ». Remerciements : sa famille. Déclaration IA : version courte (demande d’Elyamine), sans détail ; ne jamais nommer Walid dans le mémoire ; pas d’abstract anglais.
- Citations : numérotées [n] cliquables dans le Word/PDF (style IEEE, liste alphabétique), conversion automatique par `redaction/outils/citations.py` ; les sources restent en auteur-année.
- Refus : pas de substitution de caractères (omicron) pour tromper les détecteurs ; déclaration d'usage de l'IA à rédiger.
- 30/09 : PR n°1 (travail parallèle de Walid, 29-30/09) fusionnée dans main ; résultats identiques aux nôtres (écart max 0,15 pt de R²).

## Mise à jour du 1/10 (soir)
- **Bouillot et al. (2025) : article relu en entier le 1/10 (fichier LFIN_DP_2025-04_2) : chiffres confirmés (13 méthodes, 4 948 séries, 10 pays, déc. 2008-févr. 2025 ; R² XGBoost 0,81-0,99, France 0,864 ; RMSE France 7,27 pb, tableau 11, jan. 2020-févr. 2025 ; 1 variable « Government Finance & Debt » sur 50, tableau 12 ; Belgique et Espagne : LASSO/Elastic Net ont un RMSE plus faible que XGBoost, tableau 7). Cette version ne compare pas à la marche aléatoire ; le résumé d'une version plus récente en ligne dit que AR(1) et marche aléatoire font mieux que le ML dans chaque pays : les deux sont dits dans les ch. 1 et 4.** Définition du spread (moyenne ou fin de mois) non précisée (source Bloomberg).
- Chapitre 4 réécrit et raccourci (9 p.) ; déclaration IA : version courte voulue par Elyamine (usage déclaré, sans détail ; on n'y affirme plus que les interprétations « relèvent de l'auteur », il réécrira le ch. 4 lui-même après la remise).
- Références : DOI vérifiés par Crossref (31 liens), pages ECB, NeurIPS, theses.fr vérifiées ; numérotées [n] et cliquables. Figures en virgule décimale (`src/fr_format.py`). PDF : 86 p.
- **Avant l'envoi : le PDF de ce dépôt est mis en page avec Liberation Serif (substitut de Times New Roman, absent du conteneur). Le Word (`Memoire_DaliBraham.docx`) est déjà en Times New Roman : l'ouvrir dans Word, mettre à jour les champs (Ctrl+A, F9) et exporter le PDF.**
- Construction du Word/PDF : `pip install python-docx pypandoc_binary`, `apt install libreoffice-writer fonts-liberation`.

## Mise à jour du 2/10 (nuit)
- Revue globale : jeu de données reconstruit à l'identique (écart 0), Ridge M0/M1/M2, DM et BH (H1 et 168 comparaisons) recalculés indépendamment (écarts < 0,001) ; 63 contrôles OK ; chiffres de ch. 2-3 recoupés (IS −449/+470 % janv., −902/+1 789 % févr., opérations financières −462 %, écart-type 0,7 → 4,4). Seule correction : 2.2.4 (le script de vérification signale un échec quand on modifie le décalage, il ne « les signale pas tous »).
- Dates de publication de la SMB 2017-2026 (40 publications, 29 à 47 jours après la fin du mois) : `data/raw/smb_publication_dates.csv` (branche `claude/relaxed-gauss-3dvh8s` uniquement). Étude d'événement CAC 40 (plan daté `docs/plan_etude_evenement.md`, `src/23_event_study.py`) : nulle (ρ = −0,13, p = 0,42, n = 40) ; rien ajouté au mémoire. Spread quotidien : sources inaccessibles.
- Style (demande d'Elyamine : moins de tics typographiques) : passe de lisibilité sur tout le mémoire : gras retiré du texte courant (sauf deux résultats clés), légendes « Tableau 3.1 : … » et titres « Chapitre 1 : … » avec deux-points, plus de tirets demi-cadratins ni de barres obliques entre mots, listes « Ce que nous en retenons » du ch. 1 en paragraphes. Déclaration IA inchangée (courte). Pas de manœuvre contre les détecteurs.

## Mise à jour du 2/10 (matin)
- Étude d'événement préliminaire sur le CAC 40 intégrée au mémoire (annexe G, section 3.5, ch. 4.2) : 40 publications 2017-2026, ρ = −0,13 (p = 0,42), jour +1 ρ = 0,00 (p = 0,99), |rendement| 0,70 % vs 0,79 % (p = 0,74). Plan daté avant exécution (`docs/plan_etude_evenement.md`), `src/23_event_study.py`, `data/raw/smb_publication_dates.csv`, `data/raw/cac40_daily.csv` ; manifeste régénéré. Le spread reste non testé en quotidien (E14 non réalisée sur le spread). Les « dix-neuf extensions » restent les 19 pré-enregistrées.
- Chapitre 4 : arguments ajoutés (retard de publication non en cause : lag 1 et 3 mois ; sens de l'effet ambigu, E5/E18 ; plus de données ne suffiraient probablement pas : E15/E16).

## Prochaines étapes (au 30/09 soir ; remise le 2/10 à minuit)
0. Plan serré : mercredi soir ch. 4 complet (brouillon) + éthique (ch. 2, fait : 2.8) ; jeudi introduction, conclusion, résumé, annexes, pages de garde, revue de Walid en parallèle ; vendredi corrections, PDF, envoi en fin d'après-midi. Abandonné : raccourcir le ch. 3, glossaire détaillé.
1. Chapitre 4 (Discussion, 6-8 p.) à partir de `docs/plan_chapitre4.md` : l'interprétation vient d'Elyamine (règle ECE) ; méthode : questions guidées, il répond, Claude vérifie et corrige la langue.
2. Ch. 2 : considérations éthiques ; ch. 3 : raccourcir + ajouts ci-dessus.
3. Introduction, conclusion, résumé + mots-clés, déclaration d'usage de l'IA, annexes (détail E1-E20, graines, bruit), pages de garde.
4. Vérifier sur les articles les chiffres cités au ch. 1 (Bouillot, Laubach…) ; dates des événements du ch. 4.
5. Mise en forme finale, PDF, envoi à l'encadrante et au responsable du MSc ; puis soutenance.

## Référence la plus proche
Bouillot, Candelon & Kool (2025), *Forecasting European sovereign spreads using machine learning*, UCLouvain : prévision à un mois des spreads de 10 pays dont la France, XGBoost en tête, le spread passé domine.

## Structure du dépôt
- `data/raw/` : données brutes (`src/01_collect_data.py` télécharge FRED, BCE, CAC 40 ; `09`, `10`, `13` : panel, base élargie, actions/EPU), gelées par `data/MANIFEST.csv` ; `data/raw/budget/` : CSV budgétaires téléchargés à la main.
- `data/processed/` : jeu de données mensuel (`dataset_monthly.csv`, variantes `_lag1` et `_lag3` pour la robustesse), `extra_features.csv`.
- `notebooks/` : `03_EDA.ipynb` seulement (généré par `src/make_eda_notebook.py`).
- `src/` : scripts numérotés 01-22, `config.py` (décalage budgétaire, début du test), `fred_http.py`.
- `tests/` : `verifications.py` (63 contrôles), `test_walk_forward_06.py`, `test_tuned_xgb.py`, `snapshot.py` (comparaison avant/après), `data_manifest.py`.
- `results/figures/`, `results/tables/` (dont `extensions/`, `diag_04/`, `robustesse/`) ; `docs/` ; `etapes/` ; `run_all.sh` ; `requirements.txt`.

## Guide ECE de rédaction (Student Guide for Dissertation 2025-2026)
- Ordre : page de titre (titre, nom complet, ECE, MSc Data Management & IA, encadrante, mois/année) · remerciements · résumé 150-300 mots + 5-7 mots-clés · sommaire · listes des figures et des tableaux · abréviations · glossaire · Introduction (3-5 p.) · État de l'art (10-15 p., ≥ 10 sources académiques, finir sur le manque/gap) · Méthodologie (5-8 p., inclure considérations éthiques) · Résultats (**4-6 p., sans interprétation**) · Discussion (6-8 p. : implications, limites, recherches futures) · Conclusion (2-3 p.) · Références (APA, IEEE ou Harvard, ordre alphabétique) · Annexes.
- Mise en forme : Times New Roman ou Arial 12, double interligne (tableaux/notes/références simple), marges 2,54 cm, numéros de page en bas au centre ou en haut à droite ; titre niveau 1 centré gras, niveau 2 aligné à gauche gras, niveau 3 en retrait gras terminé par un point ; figures/tableaux numérotés par chapitre avec source.
- **IA** : déclarer l'usage des outils d'IA (méthodologie ou remerciements) ; interdit de rendre des hypothèses, interprétations ou paragraphes générés par IA sans relecture critique et apport personnel.
- Remise en PDF par e-mail à l'encadrante et au responsable du MSc ; retard = note F. Date du guide (15/09/2026) ; report demandé au 10/10 **refusé** : remise le **2 octobre 2026 à minuit** ; rédaction en français. Soutenance 20-30 min (10-20 min de présentation + 10-15 min de questions). Écrit 50 % / oral 50 %.
- Conséquence : les 20 extensions tiennent dans les Résultats sous forme d'un tableau de synthèse + figure ; le détail va en annexe ; les diagnostics (moyennes trimestrielles, marche aléatoire) sont interprétés dans la Discussion.

## Plan du mémoire
Introduction · Ch.1 État de l'art (rédigé) · Ch.2 Données et méthodologie · Ch.3 Résultats · Ch.4 Discussion · Conclusion · Bibliographie · Annexes.
