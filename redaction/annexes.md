# Annexes

## Annexe A – Variables des modèles principaux

**Tableau A.1 – Variables des jeux emboîtés M0, M1 et M2**

| Jeu | Variable | Définition |
|---|---|---|
| M0 | d_spread, d_spread_l1 | Variation du spread OAT–Bund (mois t et t-1), en points de base |
| M0 | spread_bp | Niveau du spread OAT–Bund (mois t) |
| M0 | d_oat, d_oat_l1 | Variation du taux OAT 10 ans (mois t et t-1) |
| M0 | cac_ret, cac_ret_l1 | Rendement du CAC 40 (mois t et t-1) |
| M0 | vix, d_vix | Niveau et variation du VIX (aversion au risque) |
| M0 | inflation_yoy | Inflation IPCH France sur un an (décalée d'un mois) |
| M0 | ecb_dfr | Taux de la facilité de dépôt de la BCE |
| M1 | b_dep_totales, personnel, fonctionnement, charge_dette, investissement, intervention (_ytd_gap) | Écart du cumul depuis janvier par rapport à l'année précédente, en % du total annuel (décalé de 2 mois) |
| M1 | b_psr_total_ytd_gap | Prélèvements sur recettes, même transformation |
| M2 | b_rec_totales, b_rec_fiscales (_ytd_gap) | Recettes totales et fiscales, même transformation |
| M2 | b_solde_ytd_diff_yoy | Solde d'exécution cumulé, écart sur un an |

*Source : `src/04_models.py`. M1 = M0 + dépenses ; M2 = M1 + recettes et solde.*

## Annexe B – Détail des extensions E1 à E20

Chaque ligne compare le même modèle sans et avec les dépenses (ou les finances publiques). « p brute » : test de Diebold-Mariano unilatéral « avec meilleur que sans » ; « p corrigée » : correction de Benjamini-Hochberg sur les 168 comparaisons retenues (E12 et ventilations exclues : « — »). E16 : R² par rapport à la moyenne.

**Tableau B.1 – Résultats des 210 comparaisons**

| Extension | Cible | Comparaison | n | R² sans (%) | R² avec (%) | p brute | p corrigée (BH) |
|---|---|---|---|---|---|---|---|
| E1 horizon | Δ spread | ridge h=3 : M1 vs M0 | 77 | -61,8 | -199,1 | 0,999 | 0,999 |
| E1 horizon | Δ spread | rf h=3 : M1 vs M0 | 77 | 2,3 | -8,6 | 0,945 | 0,999 |
| E1 horizon | Δ spread | xgb h=3 : M1 vs M0 | 77 | -26,2 | -35,4 | 0,714 | 0,999 |
| E1 horizon | Δ OAT | ridge h=3 : M1 vs M0 | 77 | -51,7 | -92,8 | 0,983 | 0,999 |
| E1 horizon | Δ OAT | rf h=3 : M1 vs M0 | 77 | -2,7 | -7,6 | 0,661 | 0,999 |
| E1 horizon | Δ OAT | xgb h=3 : M1 vs M0 | 77 | -14,9 | -19,6 | 0,593 | 0,999 |
| E1 horizon | CAC 40 | ridge h=3 : M1 vs M0 | 77 | -38,5 | -140,6 | 0,982 | 0,999 |
| E1 horizon | CAC 40 | rf h=3 : M1 vs M0 | 77 | -9,1 | -14,7 | 0,908 | 0,999 |
| E1 horizon | CAC 40 | xgb h=3 : M1 vs M0 | 77 | -49,1 | -45,5 | 0,356 | 0,999 |
| E1 horizon | Δ spread | ridge h=6 : M1 vs M0 | 74 | -107,1 | -193,0 | 0,993 | 0,999 |
| E1 horizon | Δ spread | rf h=6 : M1 vs M0 | 74 | -12,1 | -20,6 | 0,945 | 0,999 |
| E1 horizon | Δ spread | xgb h=6 : M1 vs M0 | 74 | -36,9 | -30,5 | 0,271 | 0,999 |
| E1 horizon | Δ OAT | ridge h=6 : M1 vs M0 | 74 | -157,5 | -265,6 | 0,968 | 0,999 |
| E1 horizon | Δ OAT | rf h=6 : M1 vs M0 | 74 | -27,5 | -38,0 | 0,835 | 0,999 |
| E1 horizon | Δ OAT | xgb h=6 : M1 vs M0 | 74 | -46,9 | -61,5 | 0,770 | 0,999 |
| E1 horizon | CAC 40 | ridge h=6 : M1 vs M0 | 74 | -115,5 | -257,3 | 0,969 | 0,999 |
| E1 horizon | CAC 40 | rf h=6 : M1 vs M0 | 74 | -30,3 | -39,5 | 0,872 | 0,999 |
| E1 horizon | CAC 40 | xgb h=6 : M1 vs M0 | 74 | -89,7 | -53,2 | 0,027 | 0,999 |
| E1 horizon | Δ spread | ridge h=12 : M1 vs M0 | 68 | -638,2 | -524,5 | 0,365 | 0,999 |
| E1 horizon | Δ spread | rf h=12 : M1 vs M0 | 68 | -93,9 | -97,3 | 0,667 | 0,999 |
| E1 horizon | Δ spread | xgb h=12 : M1 vs M0 | 68 | -195,8 | -152,6 | 0,013 | 0,999 |
| E1 horizon | Δ OAT | ridge h=12 : M1 vs M0 | 68 | -686,4 | -869,4 | 0,849 | 0,999 |
| E1 horizon | Δ OAT | rf h=12 : M1 vs M0 | 68 | -29,8 | -28,2 | 0,438 | 0,999 |
| E1 horizon | Δ OAT | xgb h=12 : M1 vs M0 | 68 | -70,0 | -53,2 | 0,140 | 0,999 |
| E1 horizon | CAC 40 | ridge h=12 : M1 vs M0 | 68 | -515,9 | -463,7 | 0,284 | 0,999 |
| E1 horizon | CAC 40 | rf h=12 : M1 vs M0 | 68 | 2,7 | -16,5 | 0,895 | 0,999 |
| E1 horizon | CAC 40 | xgb h=12 : M1 vs M0 | 68 | 11,8 | -26,8 | 0,787 | 0,999 |
| E10 XGB réglé | Δ spread | xgb réglé : M1 vs M0 | 79 | -4,4 | -6,2 | 0,844 | 0,999 |
| E10 XGB réglé | Δ OAT | xgb réglé : M1 vs M0 | 79 | -4,8 | -5,4 | 0,549 | 0,999 |
| E10 XGB réglé | CAC 40 | xgb réglé : M1 vs M0 | 79 | -6,2 | -3,0 | 0,175 | 0,999 |
| E11 fenêtre 60 mois | Δ spread | ridge : M1 vs M0 | 79 | -11,8 | -14,3 | 0,639 | 0,999 |
| E11 fenêtre 60 mois | Δ spread | rf : M1 vs M0 | 79 | -6,2 | -8,9 | 0,755 | 0,999 |
| E11 fenêtre 60 mois | Δ spread | xgb : M1 vs M0 | 79 | -25,9 | -25,6 | 0,490 | 0,999 |
| E11 fenêtre 60 mois | Δ OAT | ridge : M1 vs M0 | 79 | -8,7 | -17,6 | 0,931 | 0,999 |
| E11 fenêtre 60 mois | Δ OAT | rf : M1 vs M0 | 79 | -9,5 | -10,4 | 0,609 | 0,999 |
| E11 fenêtre 60 mois | Δ OAT | xgb : M1 vs M0 | 79 | -43,4 | -36,7 | 0,256 | 0,999 |
| E11 fenêtre 60 mois | CAC 40 | ridge : M1 vs M0 | 79 | -4,0 | -7,6 | 0,756 | 0,999 |
| E11 fenêtre 60 mois | CAC 40 | rf : M1 vs M0 | 79 | -14,0 | -12,9 | 0,400 | 0,999 |
| E11 fenêtre 60 mois | CAC 40 | xgb : M1 vs M0 | 79 | -45,4 | -28,2 | 0,024 | 0,999 |
| E12 par période | Δ spread | ridge [2020-2021] : M1 vs M0 | 24 | 7,6 | -1,4 | 0,957 | — |
| E12 par période | Δ spread | ridge [2022-2026] : M1 vs M0 | 55 | -28,0 | -22,5 | 0,230 | — |
| E12 par période | Δ spread | ridge [VIX ≤ 20] : M1 vs M0 | 46 | -10,9 | -7,9 | 0,295 | — |
| E12 par période | Δ spread | ridge [VIX > 20] : M1 vs M0 | 33 | -27,1 | -35,8 | 0,783 | — |
| E12 par période | Δ spread | rf [2020-2021] : M1 vs M0 | 24 | -3,7 | -7,9 | 0,804 | — |
| E12 par période | Δ spread | rf [2022-2026] : M1 vs M0 | 55 | -8,6 | -8,7 | 0,512 | — |
| E12 par période | Δ spread | rf [VIX ≤ 20] : M1 vs M0 | 46 | -3,2 | -5,1 | 0,738 | — |
| E12 par période | Δ spread | rf [VIX > 20] : M1 vs M0 | 33 | -18,0 | -18,7 | 0,536 | — |
| E12 par période | Δ spread | xgb [2020-2021] : M1 vs M0 | 24 | -26,7 | -39,7 | 0,726 | — |
| E12 par période | Δ spread | xgb [2022-2026] : M1 vs M0 | 55 | -40,5 | -24,5 | 0,064 | — |
| E12 par période | Δ spread | xgb [VIX ≤ 20] : M1 vs M0 | 46 | -24,0 | -22,4 | 0,440 | — |
| E12 par période | Δ spread | xgb [VIX > 20] : M1 vs M0 | 33 | -70,5 | -54,0 | 0,260 | — |
| E12 par période | Δ OAT | ridge [2020-2021] : M1 vs M0 | 24 | -13,7 | -15,1 | 0,563 | — |
| E12 par période | Δ OAT | ridge [2022-2026] : M1 vs M0 | 55 | -11,0 | -10,7 | 0,473 | — |
| E12 par période | Δ OAT | ridge [VIX ≤ 20] : M1 vs M0 | 46 | -16,4 | -10,0 | 0,200 | — |
| E12 par période | Δ OAT | ridge [VIX > 20] : M1 vs M0 | 33 | -8,2 | -12,0 | 0,892 | — |
| E12 par période | Δ OAT | rf [2020-2021] : M1 vs M0 | 24 | -0,9 | 7,7 | 0,229 | — |
| E12 par période | Δ OAT | rf [2022-2026] : M1 vs M0 | 55 | -7,8 | -9,0 | 0,620 | — |
| E12 par période | Δ OAT | rf [VIX ≤ 20] : M1 vs M0 | 46 | -20,2 | -14,6 | 0,223 | — |
| E12 par période | Δ OAT | rf [VIX > 20] : M1 vs M0 | 33 | 1,2 | -2,2 | 0,799 | — |
| E12 par période | Δ OAT | xgb [2020-2021] : M1 vs M0 | 24 | -24,3 | -22,4 | 0,456 | — |
| E12 par période | Δ OAT | xgb [2022-2026] : M1 vs M0 | 55 | -31,1 | -31,5 | 0,524 | — |
| E12 par période | Δ OAT | xgb [VIX ≤ 20] : M1 vs M0 | 46 | -48,8 | -36,3 | 0,106 | — |
| E12 par période | Δ OAT | xgb [VIX > 20] : M1 vs M0 | 33 | -18,8 | -26,8 | 0,808 | — |
| E12 par période | CAC 40 | ridge [2020-2021] : M1 vs M0 | 24 | -0,5 | -0,7 | 0,664 | — |
| E12 par période | CAC 40 | ridge [2022-2026] : M1 vs M0 | 55 | -2,2 | -6,5 | 0,804 | — |
| E12 par période | CAC 40 | ridge [VIX ≤ 20] : M1 vs M0 | 46 | -1,3 | -1,0 | 0,278 | — |
| E12 par période | CAC 40 | ridge [VIX > 20] : M1 vs M0 | 33 | -1,4 | -5,6 | 0,834 | — |
| E12 par période | CAC 40 | rf [2020-2021] : M1 vs M0 | 24 | -11,0 | -11,2 | 0,512 | — |
| E12 par période | CAC 40 | rf [2022-2026] : M1 vs M0 | 55 | -8,1 | -10,3 | 0,737 | — |
| E12 par période | CAC 40 | rf [VIX ≤ 20] : M1 vs M0 | 46 | -12,8 | -11,4 | 0,372 | — |
| E12 par période | CAC 40 | rf [VIX > 20] : M1 vs M0 | 33 | -7,0 | -10,3 | 0,702 | — |
| E12 par période | CAC 40 | xgb [2020-2021] : M1 vs M0 | 24 | -27,8 | -34,6 | 0,740 | — |
| E12 par période | CAC 40 | xgb [2022-2026] : M1 vs M0 | 55 | -35,9 | -20,4 | 0,097 | — |
| E12 par période | CAC 40 | xgb [VIX ≤ 20] : M1 vs M0 | 46 | -26,2 | -34,7 | 0,902 | — |
| E12 par période | CAC 40 | xgb [VIX > 20] : M1 vs M0 | 33 | -36,1 | -22,2 | 0,149 | — |
| E13 notations | Δ spread | ridge : M1 + notations vs M0 + notations | 79 | -8,8 | -8,6 | 0,475 | 0,999 |
| E13 notations | Δ spread | rf : M1 + notations vs M0 + notations | 79 | -5,7 | -9,2 | 0,827 | 0,999 |
| E13 notations | Δ spread | xgb : M1 + notations vs M0 + notations | 79 | -35,5 | -27,5 | 0,195 | 0,999 |
| E13 notations | Δ OAT | ridge : M1 + notations vs M0 + notations | 79 | -8,9 | -11,0 | 0,785 | 0,999 |
| E13 notations | Δ OAT | rf : M1 + notations vs M0 + notations | 79 | -5,2 | -6,8 | 0,673 | 0,999 |
| E13 notations | Δ OAT | xgb : M1 + notations vs M0 + notations | 79 | -27,3 | -36,3 | 0,832 | 0,999 |
| E13 notations | CAC 40 | ridge : M1 + notations vs M0 + notations | 79 | 0,0 | -21,4 | 0,901 | 0,999 |
| E13 notations | CAC 40 | rf : M1 + notations vs M0 + notations | 79 | -9,8 | -10,8 | 0,609 | 0,999 |
| E13 notations | CAC 40 | xgb : M1 + notations vs M0 + notations | 79 | -34,1 | -26,7 | 0,196 | 0,999 |
| E15 panel trimestriel | Δ spread trimestriel (5 pays) | ridge : M1 vs M0 | 330 | 13,9 | 15,5 | 0,365 | 0,999 |
| E15 panel trimestriel | Δ spread trimestriel (5 pays) | rf : M1 vs M0 | 330 | -5,3 | 4,0 | 0,057 | 0,999 |
| E15 panel trimestriel | Δ spread trimestriel (5 pays) | xgb : M1 vs M0 | 330 | -29,3 | -2,9 | 0,047 | 0,999 |
| E16 réplication élargie | spread variation | rf : complet vs sans finances publiques | 874 | -3,7 | -3,8 | 0,527 | 0,999 |
| E16 réplication élargie | spread variation | ridge : complet vs sans finances publiques | 874 | -238,2 | -162,8 | 0,079 | 0,999 |
| E16 réplication élargie | spread variation | xgb : complet vs sans finances publiques | 874 | -12,4 | -13,1 | 0,586 | 0,999 |
| E16 réplication élargie | spread niveau | rf : complet vs sans finances publiques | 874 | 94,8 | 94,5 | 0,814 | 0,999 |
| E16 réplication élargie | spread niveau | ridge : complet vs sans finances publiques | 874 | 90,0 | 92,4 | 0,121 | 0,999 |
| E16 réplication élargie | spread niveau | xgb : complet vs sans finances publiques | 874 | 97,0 | 97,0 | 0,392 | 0,999 |
| E17 panel annuel | Δ spread annuel (5 pays) | ridge : M1 vs M0 | 75 | -330,6 | -338,4 | 0,753 | 0,999 |
| E17 panel annuel | Δ spread annuel (5 pays) | rf : M1 vs M0 | 75 | -45,4 | -19,8 | 0,039 | 0,999 |
| E17 panel annuel | Δ spread annuel (5 pays) | xgb : M1 vs M0 | 75 | -108,1 | -51,5 | 0,077 | 0,999 |
| E18 régime de crise (exploratoire) | Δ spread trimestriel fin de trimestre (5 pays) | ridge : M1 vs M0 | 330 | -3,3 | -19,7 | 0,816 | 0,999 |
| E18 ventilation (hors correction) | Δ spread trimestriel fin de trimestre (5 pays) | ridge : M1 vs M0, 2010-2014 | 100 | -4,1 | -22,4 | 0,799 | — |
| E18 ventilation (hors correction) | Δ spread trimestriel fin de trimestre (5 pays) | ridge : M1 vs M0, 2015+ | 230 | 1,1 | -4,3 | 0,875 | — |
| E18 régime de crise (exploratoire) | Δ spread trimestriel fin de trimestre (5 pays) | rf : M1 vs M0 | 330 | -10,4 | -4,9 | 0,195 | 0,999 |
| E18 ventilation (hors correction) | Δ spread trimestriel fin de trimestre (5 pays) | rf : M1 vs M0, 2010-2014 | 100 | -12,4 | -5,2 | 0,169 | — |
| E18 ventilation (hors correction) | Δ spread trimestriel fin de trimestre (5 pays) | rf : M1 vs M0, 2015+ | 230 | 0,8 | -3,3 | 0,675 | — |
| E18 régime de crise (exploratoire) | Δ spread trimestriel fin de trimestre (5 pays) | xgb : M1 vs M0 | 330 | -20,2 | -26,2 | 0,719 | 0,999 |
| E18 ventilation (hors correction) | Δ spread trimestriel fin de trimestre (5 pays) | xgb : M1 vs M0, 2010-2014 | 100 | -20,3 | -28,2 | 0,744 | — |
| E18 ventilation (hors correction) | Δ spread trimestriel fin de trimestre (5 pays) | xgb : M1 vs M0, 2015+ | 230 | -19,7 | -14,4 | 0,365 | — |
| E19 actions sectorielles | btp_concessions (excès CAC 40) | ridge h=1 : M1 vs M0 | 79 | -0,0 | -1,2 | 0,844 | 0,999 |
| E19 actions sectorielles | btp_concessions (excès CAC 40) | rf h=1 : M1 vs M0 | 79 | -5,3 | -9,9 | 0,950 | 0,999 |
| E19 actions sectorielles | btp_concessions (excès CAC 40) | xgb h=1 : M1 vs M0 | 79 | -18,6 | -31,5 | 0,968 | 0,999 |
| E19 actions sectorielles | btp_concessions (excès CAC 40) | ridge h=3 : M1 vs M0 | 77 | -6,4 | -23,7 | 0,962 | 0,999 |
| E19 actions sectorielles | btp_concessions (excès CAC 40) | rf h=3 : M1 vs M0 | 77 | 1,4 | -0,7 | 0,686 | 0,999 |
| E19 actions sectorielles | btp_concessions (excès CAC 40) | xgb h=3 : M1 vs M0 | 77 | -8,8 | -8,7 | 0,495 | 0,999 |
| E19 actions sectorielles | defense (excès CAC 40) | ridge h=1 : M1 vs M0 | 79 | -0,0 | -1,7 | 0,728 | 0,999 |
| E19 actions sectorielles | defense (excès CAC 40) | rf h=1 : M1 vs M0 | 79 | -6,3 | -6,0 | 0,455 | 0,999 |
| E19 actions sectorielles | defense (excès CAC 40) | xgb h=1 : M1 vs M0 | 79 | -13,2 | -11,6 | 0,417 | 0,999 |
| E19 actions sectorielles | defense (excès CAC 40) | ridge h=3 : M1 vs M0 | 77 | -10,1 | -65,8 | 0,927 | 0,999 |
| E19 actions sectorielles | defense (excès CAC 40) | rf h=3 : M1 vs M0 | 77 | -19,4 | -10,8 | 0,061 | 0,999 |
| E19 actions sectorielles | defense (excès CAC 40) | xgb h=3 : M1 vs M0 | 77 | -53,3 | -19,9 | 0,008 | 0,999 |
| E2 classification | Δ spread | logit : M1 vs M0 (perte de Brier) | 79 | -24,4 | -25,6 | 0,549 | 0,999 |
| E2 classification | Δ spread | rf : M1 vs M0 (perte de Brier) | 79 | -2,4 | 0,5 | 0,257 | 0,999 |
| E2 classification | Δ spread | xgb : M1 vs M0 (perte de Brier) | 79 | -12,9 | -7,5 | 0,236 | 0,999 |
| E2 classification | Δ OAT | logit : M1 vs M0 (perte de Brier) | 79 | -16,1 | -30,1 | 0,980 | 0,999 |
| E2 classification | Δ OAT | rf : M1 vs M0 (perte de Brier) | 79 | 2,5 | 5,8 | 0,186 | 0,999 |
| E2 classification | Δ OAT | xgb : M1 vs M0 (perte de Brier) | 79 | -4,7 | -2,3 | 0,323 | 0,999 |
| E2 classification | CAC 40 | logit : M1 vs M0 (perte de Brier) | 79 | -3,7 | -17,1 | 0,939 | 0,999 |
| E2 classification | CAC 40 | rf : M1 vs M0 (perte de Brier) | 79 | -6,1 | -6,8 | 0,600 | 0,999 |
| E2 classification | CAC 40 | xgb : M1 vs M0 (perte de Brier) | 79 | -24,1 | -20,6 | 0,237 | 0,999 |
| E20a incertitude politique | Δ spread | ridge : M0+EPU vs M0 | 79 | -14,9 | -13,6 | 0,187 | 0,999 |
| E20b dépenses + incertitude | Δ spread | ridge : M1+EPU vs M0+EPU | 79 | -13,6 | -13,9 | 0,529 | 0,999 |
| E20a incertitude politique | Δ spread | rf : M0+EPU vs M0 | 79 | -6,8 | -6,1 | 0,313 | 0,999 |
| E20b dépenses + incertitude | Δ spread | rf : M1+EPU vs M0+EPU | 79 | -6,1 | -7,5 | 0,684 | 0,999 |
| E20a incertitude politique | Δ spread | xgb : M0+EPU vs M0 | 79 | -35,4 | -38,9 | 0,818 | 0,999 |
| E20b dépenses + incertitude | Δ spread | xgb : M1+EPU vs M0+EPU | 79 | -38,9 | -31,9 | 0,284 | 0,999 |
| E20a incertitude politique | Δ OAT | ridge : M0+EPU vs M0 | 79 | -11,3 | -8,7 | 0,134 | 0,999 |
| E20b dépenses + incertitude | Δ OAT | ridge : M1+EPU vs M0+EPU | 79 | -8,7 | -10,7 | 0,734 | 0,999 |
| E20a incertitude politique | Δ OAT | rf : M0+EPU vs M0 | 79 | -6,9 | -4,8 | 0,136 | 0,999 |
| E20b dépenses + incertitude | Δ OAT | rf : M1+EPU vs M0+EPU | 79 | -4,8 | -5,9 | 0,637 | 0,999 |
| E20a incertitude politique | Δ OAT | xgb : M0+EPU vs M0 | 79 | -30,2 | -32,8 | 0,706 | 0,999 |
| E20b dépenses + incertitude | Δ OAT | xgb : M1+EPU vs M0+EPU | 79 | -32,8 | -30,2 | 0,310 | 0,999 |
| E20a incertitude politique | CAC 40 | ridge : M0+EPU vs M0 | 79 | -1,3 | -0,3 | 0,208 | 0,999 |
| E20b dépenses + incertitude | CAC 40 | ridge : M1+EPU vs M0+EPU | 79 | -0,3 | -2,6 | 0,904 | 0,999 |
| E20a incertitude politique | CAC 40 | rf : M0+EPU vs M0 | 79 | -9,6 | -12,0 | 0,990 | 0,999 |
| E20b dépenses + incertitude | CAC 40 | rf : M1+EPU vs M0+EPU | 79 | -12,0 | -11,2 | 0,416 | 0,999 |
| E20a incertitude politique | CAC 40 | xgb : M0+EPU vs M0 | 79 | -31,7 | -38,6 | 0,972 | 0,999 |
| E20b dépenses + incertitude | CAC 40 | xgb : M1+EPU vs M0+EPU | 79 | -38,6 | -29,6 | 0,134 | 0,999 |
| E3 volatilité | Δ spread | ridge : M1 vs M0 | 79 | -4,3 | -7,7 | 0,937 | 0,999 |
| E3 volatilité | Δ spread | rf : M1 vs M0 | 79 | -17,9 | -14,0 | 0,157 | 0,999 |
| E3 volatilité | Δ spread | xgb : M1 vs M0 | 79 | -51,4 | -37,6 | 0,118 | 0,999 |
| E3 volatilité | Δ OAT | ridge : M1 vs M0 | 79 | 3,3 | 2,0 | 0,710 | 0,999 |
| E3 volatilité | Δ OAT | rf : M1 vs M0 | 79 | 2,8 | 4,2 | 0,346 | 0,999 |
| E3 volatilité | Δ OAT | xgb : M1 vs M0 | 79 | -7,0 | -6,5 | 0,466 | 0,999 |
| E3 volatilité | CAC 40 | ridge : M1 vs M0 | 79 | -1,3 | -3,4 | 0,783 | 0,999 |
| E3 volatilité | CAC 40 | rf : M1 vs M0 | 79 | 9,6 | 6,4 | 0,876 | 0,999 |
| E3 volatilité | CAC 40 | xgb : M1 vs M0 | 79 | 3,8 | 0,4 | 0,677 | 0,999 |
| E4 surprise | Δ spread | ridge : M0 + surprise vs M0 | 74 | -13,5 | -16,4 | 0,791 | 0,999 |
| E4 surprise | Δ spread | ridge : M1 + surprise vs M0 | 74 | -13,5 | -16,2 | 0,650 | 0,999 |
| E4 surprise | Δ spread | rf : M0 + surprise vs M0 | 74 | -6,0 | -11,1 | 0,928 | 0,999 |
| E4 surprise | Δ spread | rf : M1 + surprise vs M0 | 74 | -6,0 | -12,4 | 0,901 | 0,999 |
| E4 surprise | Δ spread | xgb : M0 + surprise vs M0 | 74 | -34,0 | -51,0 | 0,942 | 0,999 |
| E4 surprise | Δ spread | xgb : M1 + surprise vs M0 | 74 | -34,0 | -39,3 | 0,662 | 0,999 |
| E4 surprise | Δ OAT | ridge : M0 + surprise vs M0 | 74 | -11,9 | -14,2 | 0,943 | 0,999 |
| E4 surprise | Δ OAT | ridge : M1 + surprise vs M0 | 74 | -11,9 | -12,0 | 0,502 | 0,999 |
| E4 surprise | Δ OAT | rf : M0 + surprise vs M0 | 74 | -7,1 | -7,2 | 0,541 | 0,999 |
| E4 surprise | Δ OAT | rf : M1 + surprise vs M0 | 74 | -7,1 | -8,5 | 0,634 | 0,999 |
| E4 surprise | Δ OAT | xgb : M0 + surprise vs M0 | 74 | -29,6 | -30,7 | 0,584 | 0,999 |
| E4 surprise | Δ OAT | xgb : M1 + surprise vs M0 | 74 | -29,6 | -35,2 | 0,759 | 0,999 |
| E4 surprise | CAC 40 | ridge : M0 + surprise vs M0 | 74 | -1,4 | -0,4 | 0,208 | 0,999 |
| E4 surprise | CAC 40 | ridge : M1 + surprise vs M0 | 74 | -1,4 | -2,1 | 0,656 | 0,999 |
| E4 surprise | CAC 40 | rf : M0 + surprise vs M0 | 74 | -9,5 | -11,6 | 0,925 | 0,999 |
| E4 surprise | CAC 40 | rf : M1 + surprise vs M0 | 74 | -9,5 | -10,2 | 0,583 | 0,999 |
| E4 surprise | CAC 40 | xgb : M0 + surprise vs M0 | 74 | -31,6 | -35,6 | 0,871 | 0,999 |
| E4 surprise | CAC 40 | xgb : M1 + surprise vs M0 | 74 | -31,6 | -30,6 | 0,446 | 0,999 |
| E5 régime | Δ spread | ridge : M1 + interactions régime vs M0 + régime | 79 | -14,0 | -29,5 | 0,831 | 0,999 |
| E5 régime | Δ OAT | ridge : M1 + interactions régime vs M0 + régime | 79 | -12,2 | -19,0 | 0,914 | 0,999 |
| E5 régime | CAC 40 | ridge : M1 + interactions régime vs M0 + régime | 79 | -4,8 | -13,7 | 0,956 | 0,999 |
| E6 réduit | Δ spread | ridge : réduit + 2 dépenses vs réduit | 79 | -5,3 | -4,7 | 0,322 | 0,999 |
| E6 réduit | Δ spread | ridge : réduit + 2 CP des dépenses vs réduit | 79 | -5,3 | -5,2 | 0,462 | 0,999 |
| E6 réduit | Δ spread | rf : réduit + 2 dépenses vs réduit | 79 | -11,2 | -13,5 | 0,747 | 0,999 |
| E6 réduit | Δ spread | rf : réduit + 2 CP des dépenses vs réduit | 79 | -11,2 | -14,9 | 0,874 | 0,999 |
| E6 réduit | Δ spread | xgb : réduit + 2 dépenses vs réduit | 79 | -37,4 | -41,9 | 0,650 | 0,999 |
| E6 réduit | Δ spread | xgb : réduit + 2 CP des dépenses vs réduit | 79 | -37,4 | -40,3 | 0,618 | 0,999 |
| E6 réduit | Δ OAT | ridge : réduit + 2 dépenses vs réduit | 79 | -6,1 | -4,6 | 0,321 | 0,999 |
| E6 réduit | Δ OAT | ridge : réduit + 2 CP des dépenses vs réduit | 79 | -6,1 | -6,3 | 0,539 | 0,999 |
| E6 réduit | Δ OAT | rf : réduit + 2 dépenses vs réduit | 79 | -5,7 | -8,9 | 0,836 | 0,999 |
| E6 réduit | Δ OAT | rf : réduit + 2 CP des dépenses vs réduit | 79 | -5,7 | -10,0 | 0,876 | 0,999 |
| E6 réduit | Δ OAT | xgb : réduit + 2 dépenses vs réduit | 79 | -24,6 | -34,5 | 0,924 | 0,999 |
| E6 réduit | Δ OAT | xgb : réduit + 2 CP des dépenses vs réduit | 79 | -24,6 | -32,8 | 0,805 | 0,999 |
| E6 réduit | CAC 40 | ridge : réduit + 2 dépenses vs réduit | 79 | -3,6 | -2,6 | 0,161 | 0,999 |
| E6 réduit | CAC 40 | ridge : réduit + 2 CP des dépenses vs réduit | 79 | -3,6 | -2,6 | 0,224 | 0,999 |
| E6 réduit | CAC 40 | rf : réduit + 2 dépenses vs réduit | 79 | -8,9 | -8,2 | 0,418 | 0,999 |
| E6 réduit | CAC 40 | rf : réduit + 2 CP des dépenses vs réduit | 79 | -8,9 | -6,6 | 0,195 | 0,999 |
| E6 réduit | CAC 40 | xgb : réduit + 2 dépenses vs réduit | 79 | -34,7 | -31,5 | 0,351 | 0,999 |
| E6 réduit | CAC 40 | xgb : réduit + 2 CP des dépenses vs réduit | 79 | -34,7 | -30,9 | 0,271 | 0,999 |
| E7 tempérée | Δ spread | ridge 50/50 avec la moyenne : M1 vs M0 | 79 | -2,6 | -4,0 | 0,716 | 0,999 |
| E7 tempérée | Δ spread | rf 50/50 avec la moyenne : M1 vs M0 | 79 | -1,5 | -2,8 | 0,825 | 0,999 |
| E7 tempérée | Δ spread | xgb 50/50 avec la moyenne : M1 vs M0 | 79 | -10,5 | -9,6 | 0,425 | 0,999 |
| E8 combinaison | Δ spread | moyenne Ridge/RF/XGB : M1 vs M0 | 79 | -13,4 | -13,0 | 0,468 | 0,999 |
| E8 combinaison | Δ spread | combinaison tempérée 50/50 : M1 vs M0 | 79 | -3,5 | -4,3 | 0,638 | 0,999 |
| E7 tempérée | Δ OAT | ridge 50/50 avec la moyenne : M1 vs M0 | 79 | -2,5 | -2,7 | 0,539 | 0,999 |
| E7 tempérée | Δ OAT | rf 50/50 avec la moyenne : M1 vs M0 | 79 | -0,0 | 0,1 | 0,481 | 0,999 |
| E7 tempérée | Δ OAT | xgb 50/50 avec la moyenne : M1 vs M0 | 79 | -5,7 | -6,1 | 0,557 | 0,999 |
| E8 combinaison | Δ OAT | moyenne Ridge/RF/XGB : M1 vs M0 | 79 | -12,3 | -12,7 | 0,540 | 0,999 |
| E8 combinaison | Δ OAT | combinaison tempérée 50/50 : M1 vs M0 | 79 | -1,8 | -2,0 | 0,556 | 0,999 |
| E7 tempérée | CAC 40 | ridge 50/50 avec la moyenne : M1 vs M0 | 79 | -0,6 | -1,6 | 0,820 | 0,999 |
| E7 tempérée | CAC 40 | rf 50/50 avec la moyenne : M1 vs M0 | 79 | -3,7 | -4,4 | 0,625 | 0,999 |
| E7 tempérée | CAC 40 | xgb 50/50 avec la moyenne : M1 vs M0 | 79 | -10,4 | -9,1 | 0,362 | 0,999 |
| E8 combinaison | CAC 40 | moyenne Ridge/RF/XGB : M1 vs M0 | 79 | -10,2 | -10,6 | 0,540 | 0,999 |
| E8 combinaison | CAC 40 | combinaison tempérée 50/50 : M1 vs M0 | 79 | -3,9 | -4,2 | 0,556 | 0,999 |
| E9 Elastic Net | Δ spread | enet : M1 vs M0 | 79 | -2,7 | -4,9 | 0,815 | 0,999 |
| E9 Elastic Net | Δ OAT | enet : M1 vs M0 | 79 | -6,7 | -7,6 | 0,631 | 0,999 |
| E9 Elastic Net | CAC 40 | enet : M1 vs M0 | 79 | -0,3 | -3,8 | 0,922 | 0,999 |

*Source : `results/tables/ext_summary.csv`.*

## Annexe C – Sensibilité à la graine aléatoire

**Tableau C.1 – R² hors échantillon (%) selon la graine**

| Modèle | Cible | R² M0 (min à max) | R² M1 (min à max) | Plus petite p DM (M1 contre M0) |
|---|---|---|---|---|
| Forêt aléatoire (5 graines) | Δ spread | -6,3 à -3,3 | -9,7 à -6,2 | 0,13 |
| Forêt aléatoire (5 graines) | Δ OAT | -6,6 à -5,1 | -8,0 à -6,9 | 0,50 |
| Forêt aléatoire (5 graines) | CAC 40 | -11,5 à -8,4 | -10,7 à -7,1 | 0,52 |
| XGBoost (10 graines) | Δ spread | -39,8 à -30,8 | -32,9 à -25,4 | 0,14 |
| XGBoost (10 graines) | Δ OAT | -33,5 à -27,8 | -35,4 à -27,6 | 0,46 |
| XGBoost (10 graines) | CAC 40 | -39,1 à -30,3 | -32,0 à -25,1 | 0,16 |

*Source : `results/tables/diag_04/graines_rf.csv`, `graines_xgb.csv`.*

## Annexe D – Contrôle négatif : dépenses contre variables de bruit

**Tableau D.1 – Gain de R² par rapport à M0 (points) : vraies dépenses et sept variables de bruit**

| Modèle | Cible | Tirages | Dépenses réelles | Bruit (min à max) | Tirages de bruit ≥ dépenses |
|---|---|---|---|---|---|
| Ridge | Δ spread | 20 | 0,2 | -2,6 à 10,8 | 90 % |
| Ridge | Δ OAT | 20 | 0,0 | -2,8 à 6,2 | 90 % |
| Ridge | CAC 40 | 20 | -2,2 | -3,3 à 1,9 | 95 % |
| Forêt aléatoire | Δ spread | 5 | -1,7 | -3,2 à 4,4 | 80 % |
| Forêt aléatoire | Δ OAT | 5 | 0,0 | 1,0 à 5,4 | 100 % |
| Forêt aléatoire | CAC 40 | 5 | -1,1 | -0,5 à 6,3 | 100 % |
| XGBoost | Δ spread | 10 | 5,3 | -6,3 à 15,4 | 50 % |
| XGBoost | Δ OAT | 10 | -0,2 | -10,4 à 13,9 | 60 % |
| XGBoost | CAC 40 | 10 | 3,8 | -6,0 à 18,0 | 50 % |

*Source : `results/tables/diag_04/bruit_*.csv`.*

## Annexe E – Robustesse au décalage de publication

**Tableau E.1 – Modèles principaux avec un décalage budgétaire de 1, 2 et 3 mois**

| Décalage (mois) | Cible | Modèle | R² M0 (%) | R² M1 (%) | p DM (M1 contre M0) | p corrigée (BH) |
|---|---|---|---|---|---|---|
| 1 | Δ spread | ridge | -15,2 | -18,9 | 0,46 | 0,97 |
| 1 | Δ spread | rf | -3,9 | -10,4 | 0,06 | 0,97 |
| 1 | Δ spread | xgb | -29,7 | -41,3 | 0,30 | 0,97 |
| 1 | Δ OAT | ridge | -10,9 | -11,2 | 0,96 | 0,85 |
| 1 | Δ OAT | rf | -5,5 | -4,2 | 0,78 | 0,81 |
| 1 | Δ OAT | xgb | -26,6 | -19,3 | 0,56 | 0,81 |
| 1 | CAC 40 | ridge | -1,4 | -0,7 | 0,62 | 0,81 |
| 1 | CAC 40 | rf | -9,7 | -9,3 | 0,91 | 0,81 |
| 1 | CAC 40 | xgb | -37,2 | -34,2 | 0,78 | 0,81 |
| 2 | Δ spread | ridge | -14,9 | -14,7 | 0,97 | 0,81 |
| 2 | Δ spread | rf | -6,8 | -8,4 | 0,58 | 0,85 |
| 2 | Δ spread | xgb | -35,4 | -30,1 | 0,60 | 0,81 |
| 2 | Δ OAT | ridge | -11,3 | -11,3 | 0,99 | 0,81 |
| 2 | Δ OAT | rf | -6,9 | -6,9 | 0,99 | 0,81 |
| 2 | Δ OAT | xgb | -30,2 | -30,4 | 0,98 | 0,81 |
| 2 | CAC 40 | ridge | -1,3 | -3,5 | 0,37 | 0,86 |
| 2 | CAC 40 | rf | -9,6 | -10,8 | 0,77 | 0,81 |
| 2 | CAC 40 | xgb | -31,7 | -27,8 | 0,63 | 0,81 |
| 3 | Δ spread | ridge | -14,2 | -24,4 | 0,14 | 0,98 |
| 3 | Δ spread | rf | -5,2 | -5,7 | 0,87 | 0,89 |
| 3 | Δ spread | xgb | -35,0 | -31,3 | 0,60 | 0,68 |
| 3 | Δ OAT | ridge | -12,2 | -14,5 | 0,61 | 0,90 |
| 3 | Δ OAT | rf | -7,5 | -3,7 | 0,32 | 0,51 |
| 3 | Δ OAT | xgb | -28,4 | -11,9 | 0,09 | 0,51 |
| 3 | CAC 40 | ridge | -4,2 | -2,7 | 0,33 | 0,51 |
| 3 | CAC 40 | rf | -9,4 | -11,4 | 0,49 | 0,91 |
| 3 | CAC 40 | xgb | -32,2 | -35,5 | 0,63 | 0,90 |
| 1 | nan | synthèse | — | — | 0,06 | 0,81 |
| 2 | nan | synthèse | — | — | 0,37 | 0,81 |
| 3 | nan | synthèse | — | — | 0,09 | 0,51 |

*Source : `results/tables/robustesse_lag.csv`.*

## Annexe F – Code et reproductibilité

Le code, les données et les résultats sont conservés dans le dépôt GitHub du projet (`lyaminedb1/public-spending-market-prediction`, accessible sur demande). Le script `run_all.sh` relance l'ensemble de la chaîne ; les versions des librairies sont figées dans `requirements.txt` et les fichiers de données brutes dans `data/MANIFEST.csv`. Le script `tests/verifications.py` exécute 63 contrôles automatiques (alignement des cibles, décalages de publication, absence de fuite d'information dans la validation glissante, mois incomplets). Les valeurs exactes des forêts aléatoires et de XGBoost peuvent varier légèrement selon les versions des librairies ; les conclusions n'en dépendent pas.
