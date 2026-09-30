# Étape 18 — Relancer E19 et E20 (Ridge change), vérifier E17-E18

**Statut : ✅ fait.**

**Correction du plan initial** : `14_more_extensions.py` utilise `X.reg_model` (06). Après l'étape 02, **E19 et E20 changent sur les lignes Ridge** (grille 10⁶). E17 et E18 utilisent `P.make_model` (11, grille 10⁴) : inchangés.

**Dépend de** : 16.

## Actions
1. `python tests/snapshot.py save avant18`.
2. `python src/14_more_extensions.py E19 E20` (~5 min). Ne pas relancer E17 ni E18.
3. Comparer : les lignes RF et XGB d'E19 sont **identiques** (E19 était à jour) ; les lignes Ridge changent légèrement ; E20 est relancé sur les données corrigées.
4. Vérifier que l'EPU (indice **européen**, écart déclaré) est décalé d'1 mois et que l'écart au protocole reste indiqué (`notes` ou en-tête).

## Validation
- [x] E19 : 12 comparaisons, n_test = 79 (h=1) et 77 (h=3), comme le contrôle E de `verifications.py`.
- [x] E20 : 18 comparaisons, test 2020-01 → 2026-07.
- [x] Lignes RF/XGB d'E19 identiques à avant ; différences Ridge < quelques points.
- [x] `E17.csv` et `E18.csv` inchangés (`diff`).

## Commit
`14 : relance E19 (Ridge) et E20 ; E17-E18 inchangés`

## Résultat (29/09) — 18 min pour les deux (avec le run de référence en parallèle)
- Référence « ancienne grille, même environnement » recalculée comme aux étapes 02 et 16.
- **E19** (12 comparaisons ; n_test 79 pour h = 1, 77 pour h = 3, contrôle de `verifications.py` OK) : lignes RF/XGBoost **identiques** à la référence (écart 0,0) ; lignes Ridge : écart médian 1,1 point, max 3,0 ; recalculé ici avec l'ancienne grille, E19 reproduit le fichier commité à 0,01 point près (E19 était déjà à jour). Aucune comparaison « avec dépenses » au-dessus de 0 (meilleur R² avec dépenses : −0,74 %) ; p brute minimale 0,008 (défense h = 3, XGBoost : dépenses moins mauvaises, R² −53 → −20 %).
- **E20** (18 comparaisons, 79 mois) : relancée sur les données corrigées (inflation décalée) ; hors Ridge identique à la référence, Ridge écart médian 0,6 point ; par rapport au commité (ancien jeu de données) écart médian 2,0 points, max 6,0. Meilleur R² −0,28 %, p brute minimale 0,134 : ni l'incertitude politique (indice **européen**, écart déclaré) ni les dépenses n'aident.
- **E17 et E18 inchangés** (`E17.csv`, `E18.csv` identiques au commit précédent).
