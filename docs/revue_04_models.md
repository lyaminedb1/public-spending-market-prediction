# Revue de `src/04_models.py` (nuit du 27 au 28/09/2026)

> **Statut (29/09) : les 7 décisions ont été acceptées par Elyamine.** Grille RidgeCV élargie à 10⁶ dans 04 et 06,
> tout relancé ; les chiffres Ridge ci-dessous sont ceux d'avant la relance (écarts ≤ 1,2 pt, conclusions identiques).
> Chiffres à jour : CLAUDE.md et chapitre 3. Clark-West sur du bruit après relance : 5-55 % (Ridge), 45-75 % (XGB).
> Les diagnostics sont dans `src/15_diag_04.py` (nouveau) et leurs sorties dans `results/tables/diag_04/`.
> Méthode (comme pour la préparation des données) : relire, recalculer de façon indépendante, puis **tester en
> cassant** : ajouter exprès un faux signal (doit être trouvé) ou du bruit (ne doit pas être trouvé).

---

## 1. Ce que fait le code, simplement

**Validation glissante (walk-forward), fenêtre croissante.** Pour chaque mois de test m (2020-01 → 2026-07, 79 mois),
le modèle est entraîné sur tous les mois avant m, puis prévoit la cible de m. Le mois suivant, on ajoute m à
l'entraînement et on recommence. *Théorie* : en série temporelle, une validation croisée au hasard mélangerait passé
et futur (fuite). La validation glissante reproduit ce qu'un prévisionniste aurait pu faire à chaque date.

**Trois jeux de variables emboîtés.** M0 = marchés (11 variables), M1 = M0 + 7 dépenses, M2 = M1 + recettes et solde.
« Emboîtés » : M1 contient tout M0. La question H1 est : M1 prévoit-il mieux que M0 ?

**Trois modèles.**
- *Ridge* : régression linéaire avec une pénalité qui rapproche les coefficients de zéro. La force de la pénalité
  (alpha) est choisie par `RidgeCV` sur les données d'entraînement. Les variables sont standardisées sur l'entraînement.
- *Forêt aléatoire* : moyenne de 300 arbres de décision peu profonds (profondeur 4), chacun appris sur un
  échantillon différent. Capture des effets non linéaires.
- *XGBoost* : 200 petits arbres (profondeur 2) appris l'un après l'autre, chacun corrigeant les erreurs des précédents
  (boosting), avec un pas d'apprentissage de 0,05.

**Références naïves.** « Moyenne historique » (moyenne de la cible sur l'entraînement) et « variation nulle » (zéro).

**Métriques.**
- *R² hors échantillon* (Campbell et Thompson, 2008) : 1 − (erreurs² du modèle) / (erreurs² de la moyenne historique).
  Positif = le modèle bat la moyenne ; négatif = il fait pire.
- *RMSE, MAE* : erreur quadratique moyenne (racine) et erreur absolue moyenne.
- *Bonne direction* : part des mois où le signe prévu est le bon.
- *Diebold-Mariano (DM)* avec correction de Harvey, Leybourne et Newbold : teste si la différence d'erreurs² entre deux
  modèles est significativement différente de zéro.

**Importance des variables.** Valeurs SHAP d'un XGBoost estimé sur **tout** l'échantillon (en échantillon).

## 2. Vérifié correct ✅

| Contrôle | Résultat |
|---|---|
| Pas de fuite dans la validation glissante | entraînement = mois < m ; la dernière ligne d'entraînement (m−1) a pour cible la variation de m, connue fin m ✅ |
| Validation recodée indépendamment | mêmes prévisions que 04 (écart 4·10⁻¹⁶) — `diag_04/identite.csv` |
| Métriques recalculées depuis les prévisions sauvegardées | écart max 0,0005 (arrondis) |
| DM recalculé autrement (régression sur une constante) | écart max des p-values 0,0004 |
| Formule HLN pour h = 1 | √((T−1)/T), loi de Student à T−1 degrés : correct |
| Standardisation (Ridge) apprise sur l'entraînement seulement | oui (pipeline) ✅ |
| Affirmation « un AR(1) fait -2 à -3 % » | confirmée : -2,7 % (spread), -2,3 % (OAT), -1,9 % (CAC) — `diag_04/ar1.csv` |

## 3. Constats

### Constat 1 — La puissance du test est faible (contrôle positif) ⚠️ important pour la Discussion
On ajoute à M0 une variable **fictive** corrélée à la cible (corrélation ρ ; ρ = 1 est une fuite totale), Ridge, 10 tirages.

| ρ | R² potentiel (≈ ρ²) | le modèle bat la moyenne | DM détecte l'apport (p < 0,05) |
|---|---|---|---|
| 0,1 | 1 % | 0 % des tirages | 0 % |
| 0,3 | 9 % | 10 à 30 % | 0 à 50 % |
| 0,5 | 25 % | 80 à 100 % | 30 à 80 % |
| 1,0 | 100 % | 100 % (R² = 100 %) | 100 % |

*Théorie* : avec 79 mois de test et des modèles appris sur 70 à 148 mois, un signal modéré est noyé dans le bruit
d'estimation. **Conséquence** : le résultat négatif exclut un fort pouvoir prédictif des dépenses, pas un effet faible
(« absence de preuve n'est pas preuve d'absence »). Le contrôle ρ = 1 montre aussi que le dispositif détecte bien une fuite.

### Constat 2 — Les dépenses ne font pas mieux que du bruit (contrôle négatif)
On remplace les 7 dépenses par 7 variables de **pur bruit** (tirages aléatoires) et on compare le gain par rapport à M0.

| Modèle | Rang des vraies dépenses parmi les tirages de bruit |
|---|---|
| Ridge (20 tirages) | meilleures que seulement **10 %** des tirages de bruit (3 cibles) |
| Forêt aléatoire (5 tirages) | meilleures que 0 à 20 % |
| XGBoost (10 tirages) | meilleures que 40 à 50 % (≈ un tirage moyen) |

Remarque : ajouter du bruit **améliore** souvent Ridge et la forêt par rapport à M0. *Explication partielle, vérifiée pour
Ridge* : avec 7 variables de bruit, `RidgeCV` choisit une pénalité plus forte (alpha médian : spread 28 → 92, OAT 62 → 204),
donc des prévisions plus proches de la moyenne, ce qui est ici un avantage : **M0 sur-apprend un peu**. Mais les dépenses
font aussi monter la pénalité (spread 62, OAT 254) sans ce gain : elles dégradent légèrement les prévisions.
→ Pour H1 : les petites différences M1 − M0 ne sont pas propres aux dépenses.

### Constat 3 — Le test de Clark-West ne convient pas ici ; garder Diebold-Mariano
*Théorie* : quand M1 contient M0 (modèles emboîtés), le test DM est connu pour être **trop prudent** (Clark et West, 2007) :
le grand modèle paie le coût d'estimer des paramètres inutiles. Le test de Clark-West corrige cela. Un jury peut poser la question.

Résultat sur les prévisions de 04 (`diag_04/cw.csv`) : Ridge et forêt : aucun p < 0,05. XGBoost : p = 0,018 (spread), 0,030 (CAC), 0,083 (OAT).

**Mais** le test de taille (`diag_04/cw_bruit_*.csv`) montre que Clark-West « trouve » un apport dans **du pur bruit**
très souvent : XGBoost 45 à 75 % des tirages, Ridge 40 à 50 % pour les taux (5 % attendus). DM : 0 à 5 %.
→ Clark-West est **beaucoup trop permissif** dans notre cadre (petit échantillon, M0 qui sur-apprend, modèles non linéaires).
Les p-values XGBoost ci-dessus ne prouvent donc rien. Même sans ce problème, elles ne survivraient pas à la correction
BH sur les 9 comparaisons (plus petite p = 0,018 > 0,1 × 1/9 = 0,011).

**Proposition** : garder DM (c'est le protocole), et **mentionner** Clark-West + ce test de taille dans la Discussion,
comme réponse anticipée à la question du jury. Pas de changement de code.

### Constat 4 — H4 ne peut pas s'appuyer sur SHAP ❌ à corriger dans le texte
7 variables de **pur bruit** obtiennent **34 à 38 %** de l'importance SHAP en échantillon (10 tirages, `diag_04/shap_bruit.csv`),
contre 31 à 37 % pour les dépenses. La part SHAP des dépenses n'est donc **pas un signe d'information** : c'est ce qu'obtient
n'importe quel groupe de 7 variables dans un XGBoost en échantillon.
- Le constat actuel de CLAUDE.md (« les dépenses pèsent ~30 %… surapprentissage ») reste juste sur le surapprentissage,
  mais on ne peut pas en tirer un classement des dépenses (intervention, investissement…) pour H4.
- **Proposition** : H4 = « non testable / non soutenue » ; la figure 3.3 reste possible, avec une légende qui donne la
  référence du bruit (34-38 %). Option (déclarée comme ajoutée après coup) : importance par permutation **hors échantillon**.

### Constat 5 — Sensibilité à la graine aléatoire
| Modèle | R² M0 selon la graine | R² M1 selon la graine | DM M1 vs M0, p minimale |
|---|---|---|---|
| XGBoost (10 graines) | spread -39,8 à -30,8 ; OAT -33,5 à -27,8 ; CAC -39,1 à -30,3 | spread -32,9 à -25,4 ; OAT -35,4 à -27,6 ; CAC -32,0 à -25,1 | 0,14 |
| Forêt (5 graines) | spread -6,3 à -3,3 ; OAT -6,6 à -5,1 ; CAC -11,5 à -8,4 | spread -9,7 à -6,2 ; OAT -8,0 à -6,9 ; CAC -10,7 à -7,1 | 0,13 |

Les conclusions (R² négatifs, aucun DM significatif) tiennent pour **toutes** les graines. Mais les chiffres exacts de XGBoost
bougent d'environ 9 points. **Proposition** : garder la graine 42 (déclarée) dans le tableau principal et donner ces
fourchettes en annexe.

### Constat 6 — La « variation nulle » bat la moyenne historique pour les taux
R² de la prévision zéro : spread **+1,7 %**, OAT **+2,4 %**, CAC -0,2 %. Pour les taux, la référence la plus exigeante est
donc la variation nulle (marche aléatoire), comme dans E16. **Proposition** : montrer les deux références dans le tableau
du chapitre 3 (la colonne existe déjà : `naif_zero` dans `models_metrics.csv`).

### Constat 7 — Hyperparamètres : « fixés a priori » n'est pas prouvable
`04_models.py` et ses résultats ont été commités **ensemble** (commit 98ab6fc, 26/09 20h43). Contrairement aux extensions,
aucune trace ne montre les hyperparamètres avant les résultats. Les valeurs sont usuelles (pas d'optimisation sur le test).
**Proposition** : au chapitre 2, écrire « fixés sans optimisation sur la période de test, à des valeurs usuelles », pas
« pré-enregistrés ».

### Constat 8 — Grille de pénalité de Ridge trop étroite pour le CAC 40 ⚠️ petite erreur de réglage
`RidgeCV(alphas=np.logspace(-2, 3, 30))` : la pénalité choisie est **bloquée à la borne supérieure (1000)** pour le CAC 40
dans 75 % (M0), 79 % (M1) et 99 % (M2) des mois (spread et OAT : 0 à 10 %). *Théorie* : quand l'optimum est sur le bord de
la grille, le réglage ne fait pas son travail ; il faut élargir la grille. Même grille dans `06_extensions.py`
(`11_panel_models.py` va jusqu'à 10⁴).
Effet mesuré avec une grille 10⁻² à 10⁶ (calcul hors dépôt) : R² Ridge spread -15,0 → -14,9 (M0), -15,1 → -14,7 (M1) ;
OAT -12,0 → -11,3, -10,9 → -11,3 ; CAC -1,0 → -1,3, -2,7 → -3,5 ; DM M1 vs M0 : p = 0,97 / 0,99 / 0,37. **Aucune
conclusion ne change.**
**Proposition** : élargir la grille à 10⁶ dans `04` et `06` lors de la relance finale (vraie correction de méthode, effet
négligeable). À décider.

### Constat 9 — Détails mineurs (pas d'erreur)
- `RidgeCV` choisit alpha par validation « leave-one-out » **à l'intérieur** de l'entraînement : pas une fuite vers le test,
  mais ce n'est pas une validation temporelle. Acceptable ; à mentionner en une phrase.
- « Bonne direction » : descriptif, sans test de significativité (ex. Pesaran-Timmermann). À présenter comme descriptif.
- SHAP est calculé en échantillon, sur la période de test incluse : c'est une description, pas une preuve de prévision.

## 4. Récapitulatif des décisions à prendre (Elyamine)

| # | Proposition | Change des résultats ? |
|---|---|---|
| 1 | Ajouter au chapitre 4 la puissance (constat 1) et le contrôle bruit (constat 2) | non (diagnostics déjà calculés) |
| 2 | Garder DM ; citer Clark-West et son test de taille (constat 3) | non |
| 3 | H4 → « non soutenue » ; légende de la figure 3.3 avec la référence du bruit (constat 4) | texte + légende |
| 4 | Fourchettes par graine en annexe (constat 5) | non |
| 5 | Deux références (moyenne, variation nulle) dans le tableau du ch. 3 (constat 6) | présentation |
| 6 | Formulation des hyperparamètres au ch. 2 (constat 7) | texte |
| 7 | Élargir la grille de Ridge à 10⁶ dans 04 et 06, à la relance finale (constat 8) | oui, moins d'1 point de R² |

Une seule petite erreur de méthode trouvée (grille de Ridge, constat 8), sans effet sur les conclusions. Rien n'a été changé
dans le code en attendant ta décision.

## 5. Sources à ajouter si les points 1-2 sont retenus
- Clark, T. E., & West, K. D. (2007). Approximately normal tests for equal predictive accuracy in nested models. *Journal of Econometrics*, 138(1), 291-311.
- Campbell, J. Y., & Thompson, S. B. (2008). Predicting excess stock returns out of sample: Can anything beat the historical average? *Review of Financial Studies*, 21(4), 1509-1531.
- Harvey, D., Leybourne, S., & Newbold, P. (1997). Testing the equality of prediction mean squared errors. *International Journal of Forecasting*, 13(2), 281-291.
