# Étape 17 — Grille Ridge de 11 (conditionnelle)

**Dépend de** : 02 (mesure de l'étape 02 sur 11).

## Actions
1. Lire `alpha_bornes_avant.csv` pour 11 (grille 10⁻²…10⁴).
2. **Si** l'alpha est à la borne haute dans > 25 % des mois : passer à 10⁶, relancer `python src/11_panel_models.py` (~16 min), comparer E15/E16 avant/après.
3. **Sinon** : ne rien changer et l'écrire dans ce fichier (« non nécessaire : x % »).

## Validation
- [ ] Décision consignée avec le pourcentage mesuré.
- [ ] Si relancé : conclusions inchangées (finances publiques p 0,08-0,88 ; tous < marche aléatoire ; niveau R² 90-97 %).
- [ ] `12_diag_e15.py` relancé si E15 change.

## Commit
`11 : grille Ridge …` ou aucun commit (décision « non nécessaire »).
