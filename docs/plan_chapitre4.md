# Chapitre 4 — Discussion : plan de travail (brouillon du 28/09, nuit)

> **Statut : PLAN, pas du texte.** Rédigé par Claude pendant la revue du code, à relire et décider par Elyamine.
> Règle ECE : pas d'interprétation générée par IA rendue telle quelle. Ce fichier donne la **structure**, les
> **faits établis** (avec leur source dans le dépôt) et les **questions à trancher**. Les phrases d'interprétation
> sont à écrire par toi.
>
> Chiffres à jour de la relance finale du 29/09 (grille Ridge 10⁶). Tableaux cités = chapitre 3.

Longueur cible (guide ECE) : 6 à 8 pages. Contenu attendu : implications, limites, recherches futures.

---

## 4.1 Réponse à la problématique (≈ 1 p.)

**Faits établis**
- Aucun modèle ne bat la moyenne historique à un mois ; meilleur R² hors échantillon : -1,3 % (Ridge M0, CAC 40). Source : `results/tables/models_metrics.csv`.
- Ajouter les dépenses (M1 vs M0) : DM p bilatérale 0,37 à 0,99. Source : `models_dm_tests.csv`.
- Extensions : 0 comparaison significative sur 168 après BH (p_BH min 0,999 ; 6 p brutes < 0,05 pour 8,4 attendues).

**Hypothèses : état**
| Hyp. | Verdict actuel | Preuve | Nuance à discuter |
|---|---|---|---|
| H1 | rejetée | DM M1 vs M0 ; contrôle négatif (§4.3) | puissance faible : voir §4.3 |
| H2 | non testable | aucun apport à classer | le dire simplement |
| H3 | rejetée | XGB pire que Ridge sur le CAC 40 (p 0,03) ; RF ≈ Ridge | XGB instable selon la graine (§4.3) |
| H4 | **non soutenue par SHAP** | 7 variables de bruit obtiennent autant de SHAP (34-38 %) que les dépenses (31-37 %) | voir revue de 04, point 4 |

**À trancher par toi** : formulation de la réponse (« non » vs « pas de preuve, avec la puissance disponible »).

## 4.2 Pourquoi les dépenses n'aident pas : pistes (≈ 1,5 p.)

**Piste A — l'information est déjà dans les prix** (Fama, 1970 ; Ramey, 2011)
- Fait : la SMB du mois M paraît début M+2 (vérifié 2023-2026) ; le budget est voté en LFI avant l'année.
- Fait : E4 (surprise par rapport à la LFI) n'apporte rien (meilleur R² avec surprise : -11,1 / -7,2 / -0,4 %).
- Limite de l'argument : E14 (étude d'événement le jour de publication) n'a pas pu être faite → on ne peut pas montrer directement que le marché réagit à la publication. À écrire comme perspective.

**Piste B — ce qui fait bouger le spread n'est pas budgétaire**
- Fait (calcul sur `dataset_monthly.csv`, variation de la moyenne mensuelle, écart-type 5,3 pb) : plus gros mouvements
  2020-03 (+20,5), 2017-05 (-18,1), 2017-02 (+16,3), 2024-06 (+15,5), 2016-11 (+15,3), 2021-05 (+11,8), 2017-01 (+11,1),
  2022-02 (+10,5), 2017-03 (-10,0), 2020-06 (-9,2), 2025-02 (-9,2), 2014-12 (-9,0).
- Événements probables (**à vérifier avec des sources datées avant de les écrire**) : Covid (03/2020), présidentielle 2017
  (01 à 05/2017), dissolution de l'Assemblée (06/2024), élection américaine (11/2016), invasion de l'Ukraine et tournant de la
  BCE (02/2022). Non identifiés : 2021-05, 2025-02, 2014-12, 2020-06.
- Attention : ce sont des variations de **moyennes** mensuelles ; un choc de fin de mois apparaît en partie le mois suivant.

**Piste C — variable lente, cible rapide**
- Fait : même à basse fréquence (E17 panel annuel, 75 prévisions), tout perd contre la moyenne et la marche aléatoire.
- À discuter : la littérature (Afonso et al., 2015 ; Bernoth et al., 2012) trouve des effets des finances publiques sur le
  **niveau** des spreads, en coupe ou en panel, pas en **prévision** hors échantillon à un mois.

## 4.3 Ce que le résultat négatif veut dire — et ne veut pas dire (≈ 1,5 p.) — *nouveau, issu de la revue de 04*

**Puissance du test (contrôle positif, revue du 28/09)**
- Expérience : on ajoute à M0 une variable fictive corrélée à la cible (corrélation ρ), avec Ridge, 10 tirages.
- Résultat : avec ρ = 0,3 (R² potentiel ≈ 9 %), le modèle bat la moyenne dans seulement 20 à 30 % des tirages et DM
  détecte l'apport dans 0 à 50 % des tirages. Avec ρ = 0,5 (R² potentiel ≈ 25 %), le modèle bat la moyenne dans 80 à
  100 % des tirages, mais DM ne détecte encore l'apport que dans 30 à 80 % des cas (Clark-West : 100 %).
- Conséquence à écrire : avec 79 mois de test, on peut exclure un **fort** pouvoir prédictif des dépenses, pas un effet faible.
  Source : `docs/revue_04_models.md`.

**Contrôle négatif (7 variables de bruit à la place des 7 dépenses)**
- Ridge : 90 à 95 % des tirages de bruit font au moins aussi bien que les dépenses ; forêt : 80 à 100 %.
- XGBoost : 50 à 60 % (les dépenses se comportent comme un tirage de bruit moyen).
- Conséquence : les petites différences M1 − M0 ne sont pas propres aux dépenses.

**Choix de la référence**
- Prévoir une variation nulle bat la moyenne historique pour le spread (+1,7 %) et l'OAT (+2,4 %). La référence
  « moyenne » n'est donc pas la plus exigeante pour les taux. (Déjà vu dans E16 : marche aléatoire.)

**Test pour modèles emboîtés (Clark et West, 2007)** — décision du 29/09 : on garde DM ; CW jugerait « significatif » du bruit dans 5-55 % (Ridge) et 45-75 % (XGB) des tirages. À mentionner comme choix de méthode.

**Artefact des moyennes** (E15, Working 1960) : un gain apparent venait de l'autocorrélation mécanique des moyennes
trimestrielles ; il disparaît en fin de trimestre. Même mécanisme, plus faible, dans les cibles mensuelles en moyennes.

## 4.4 Comparaison avec la littérature (≈ 1 p.)

- Bouillot, Candelon et Kool (2025) : R² élevé sur le **niveau** du spread. Fait (E16) : on retrouve 90-97 % sur le niveau,
  mais tous les modèles perdent contre la marche aléatoire (XGB -31 %, RMSE 21,1 pb contre 18,4 pb). → Un R² sur le niveau
  n'est pas une prévision.
- Welch et Goyal (2008) : la plupart des prédicteurs ne battent pas la moyenne hors échantillon → résultat cohérent.
- Campbell et Thompson (2008) : prévisions tempérées (E7) : meilleur R² -1,5 / 0,0 / -0,6 % sans dépenses, -2,8 / +0,1 / -1,6 % avec.
- **À ajouter à la bibliographie si on garde le point Clark-West** : Clark, T. E., & West, K. D. (2007). *Approximately
  normal tests for equal predictive accuracy in nested models*. Journal of Econometrics, 138(1), 291-311.

## 4.5 Limites (≈ 1,5 p.) — liste établie pendant la revue

1. Données budgétaires **révisées** (dernière version), pas en temps réel ; décembre provisoire puis définitif.
2. Décalage de 2 mois **vérifié seulement sur 2023-2026** ; 2014-2019 = hypothèse.
3. Cibles de taux en **moyennes mensuelles** (OCDE) ; CAC 40 en fin de mois : cibles pas homogènes.
4. `_ytd_gap` : variance ×6 de janvier à décembre (sens qui change selon le mois).
5. Petit échantillon : 70 à 148 mois d'entraînement, 79 mois de test → **puissance faible** (§4.3).
6. Une seule graine aléatoire dans les résultats principaux ; XGB : R² varie d'environ 9 points selon la graine.
7. Hyperparamètres : présentés comme fixés a priori, mais code et résultats de 04 commités ensemble (pas de trace d'un
   pré-enregistrement, contrairement aux extensions).
8. E16 : 25 des 68 séries arrêtées fin 2022-début 2024 (23,6 % de valeurs imputées en fin de test).
9. E19 : prix hors dividendes.
10. Pré-enregistrement séquentiel : E14-E20 ajoutées après certains résultats ; E18 exploratoire.
11. Pas de ventilation des dépenses par mission (défense, etc.) dans les SMB.

## 4.6 Recherches futures (≈ 1 p.)

- Étude d'événement (E14) avec des taux quotidiens (Banque de France, Bundesbank) et les dates de publication de la SMB.
- Annonces budgétaires (PLF, LFR, programmes de stabilité) plutôt que l'exécution mensuelle.
- Données en temps réel (vintages) des situations budgétaires.
- Commande publique (DECP) pour une ventilation sectorielle.
- Panel plus long incluant la crise 2010-2012 avec des cibles en fin de période (pas en moyennes).

---
*Sources des faits : fichiers du dépôt cités ; diagnostics détaillés dans `docs/revue_04_models.md`.*
