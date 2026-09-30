# Étape 11 — Reproduire par script les chiffres des limites

**Statut : ✅ fait.**

**Objet** : plusieurs limites citées dans `CLAUDE.md` reposent sur des chiffres jamais calculés par un script versionné (« ×6 », « 23,6 % imputé », « 25/68 séries arrêtées », « ~70-148 mois d'entraînement »). Un seul script les produit.

**Dépend de** : 09.

## Actions
Créer `src/20_limites_chiffres.py` → `results/tables/limites_chiffres.csv` (`limite, valeur, unite, source_script`) :
1. **Variance de `_ytd_gap` par mois de l'année** : écart-type par mois civil pour les 7 dépenses ; rapport max/min (revendiqué ≈ ×6 de janvier à décembre).
2. **Effectifs** : nombre d'observations d'entraînement au premier et au dernier mois de test ; nombre de mois de test par script (04 : 79 ; E1 h=3 : 77 ; E4 : jusqu'à 2026-02 ; E19 : 79 et 77).
3. **E16 – séries arrêtées** : parmi les 68 séries de la base élargie, nombre dont la dernière valeur observée est antérieure à 2024-06 (revendiqué 25/68) ; part médiane des valeurs imputées par la médiane d'entraînement sur les 144 dernières lignes de test (revendiqué 23,6 %).
4. **Autocorrélation mécanique** des moyennes mensuelles : AR(1) du Δspread et du ΔOAT (moyennes) comparés à celui du spread fin de mois **si** des données fin de mois existent (sinon note « non disponible »).
5. **Puissance** : reprend le résumé de l'étape 04 (une ligne par ρ).

## Validation
- [x] Chaque valeur est comparée à celle de `CLAUDE.md` ; les écarts sont listés dans le message de commit (les chiffres de CLAUDE.md seront corrigés à l'étape 22, pas ici).
- [x] Le script s'exécute en < 2 min et est reproductible.
- [x] Témoin (remplace « bruit blanc → ≈ 1 », qui était faux : la variance d'un écart de cumuls croît mécaniquement avec le mois) : des flux i.i.d. donnent décembre/janvier ≈ √12 = 3,46 (simulé : 3,66).

## Commit
`20_limites_chiffres : chiffres des limites calculés par script`

## Résultat (29/09) — `src/20_limites_chiffres.py` → `results/tables/limites_chiffres.csv` (7 s, reproductible)
| Chiffre de CLAUDE.md | Recalculé | Verdict |
|---|---|---|
| `_ytd_gap` : variance ×6 de janv. à déc. | écart-type déc./janv. : **médiane 6,3** sur les 7 lignes (min **0,96** investissement ; max 12,4 charge de la dette) | confirmé en médiane, **mais très hétérogène** ; **témoin i.i.d. : 3,66** (≈ √12) → environ la moitié de l'inflation de variance est mécanique |
| 25/68 séries arrêtées fin 2022-début 2024 | **25**/68 dont la dernière valeur est antérieure à 2024-06 (2022-11 : 2 ; 2023-01 : 1 ; 2023-12 : 1 ; 2024-01 : 16 ; 2024-03 : 5) | confirmé |
| 23,6 % de valeurs imputées (médiane, 144 dernières lignes de test) | **23,4 %** (moyenne des cellules) ; médiane des lignes 24,0 % ; médiane des variables 0 % | ≈ confirmé : écrire « environ 23 % des cellules » (la définition « médiane » ne se reproduit pas) |
| 70 à 148 mois d'entraînement, 79 de test | 70 → 148 ; 79 | confirmé |
| E1 h=12 : 68 obs. chevauchantes | 68 (h=3 : 77 ; h=6 : 74) ; E4 : 74 ; E19 : 79 / 77 ; E15 : 330 ; E16 : 874 ; E17 : 75 | confirmé |
| AR(1) : Δspread 0,14 ; ΔOAT 0,23 ; CAC −0,09 | 0,146 ; 0,236 ; −0,090 | confirmé |
| Puissance : ρ = 0,3 → 10-30 % ; ρ = 0,5 → 80-100 % | 20-30 % ; 80-100 % | confirmé |
- À corriger à l'étape 22 dans `CLAUDE.md` : « 23,6 % » → « ≈ 23 % (moyenne des cellules) » ; nuancer « ×6 ».
- Vérifié au passage : la base d'E16 va jusqu'en 2026-09 pour 7 séries (mois incomplet) mais le dernier mois de test d'E16 est 2026-07 (cible = août) : aucune valeur de septembre n'entre dans l'entraînement ni dans le test.
