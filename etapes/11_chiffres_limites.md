# Étape 11 — Reproduire par script les chiffres des limites

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
- [ ] Chaque valeur est comparée à celle de `CLAUDE.md` ; les écarts sont listés dans le message de commit (les chiffres de CLAUDE.md seront corrigés à l'étape 22, pas ici).
- [ ] Le script s'exécute en < 2 min et est reproductible.
- [ ] Contrôle négatif : sur des données `_ytd_gap` remplacées par du bruit blanc, le rapport de variances ≈ 1.

## Commit
`20_limites_chiffres : chiffres des limites calculés par script`
