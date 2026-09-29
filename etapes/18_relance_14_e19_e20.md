# Étape 18 — Relancer E19 et E20 (Ridge change), vérifier E17-E18

**Correction du plan initial** : `14_more_extensions.py` utilise `X.reg_model` (06). Après l'étape 02, **E19 et E20 changent sur les lignes Ridge** (grille 10⁶). E17 et E18 utilisent `P.make_model` (11, grille 10⁴) : inchangés.

**Dépend de** : 16.

## Actions
1. `python tests/snapshot.py save avant18`.
2. `python src/14_more_extensions.py E19 E20` (~5 min). Ne pas relancer E17 ni E18.
3. Comparer : les lignes RF et XGB d'E19 sont **identiques** (E19 était à jour) ; les lignes Ridge changent légèrement ; E20 est relancé sur les données corrigées.
4. Vérifier que l'EPU (indice **européen**, écart déclaré) est décalé d'1 mois et que l'écart au protocole reste indiqué (`notes` ou en-tête).

## Validation
- [ ] E19 : 12 comparaisons, n_test = 79 (h=1) et 77 (h=3), comme le contrôle E de `verifications.py`.
- [ ] E20 : 18 comparaisons, test 2020-01 → 2026-07.
- [ ] Lignes RF/XGB d'E19 identiques à avant ; différences Ridge < quelques points.
- [ ] `E17.csv` et `E18.csv` inchangés (`diff`).

## Commit
`14 : relance E19 (Ridge) et E20 ; E17-E18 inchangés`
