# Étape 20 — Grille Ridge de `11_panel_models.py` (conditionnelle)

**Dépend de** : 02 (mesure de l'alpha sur 11 dans `alpha_bornes_avant.csv`).

## Actions
1. Lire, pour 11 (grille 10⁻²…10⁴), la part de mois à la borne haute (E16 variation, E15).
2. **Si > 25 %** : passer à 10⁶ dans 11, relancer `python src/11_panel_models.py` (~16 min) puis `python src/12_diag_e15.py` et **E17/E18** (`14_more_extensions.py E17 E18`, qui utilisent aussi `P.make_model`), puis répéter l'étape 19.
3. **Sinon** : ne rien changer ; écrire « non nécessaire : x % » dans ce fichier.

## Validation
- [ ] Décision consignée avec le pourcentage mesuré.
- [ ] Si relancé : conclusions inchangées (finances publiques p 0,08-0,88 ; tous < marche aléatoire ; niveau R² 90-97 % vs moyenne).
- [ ] `verifications.py` (section D) passe.

## Commit
`11 : grille Ridge …` ou aucun commit (décision « non nécessaire »).
