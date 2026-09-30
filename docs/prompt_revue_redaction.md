# Prompt : revue complète de la rédaction (à donner à Claude)

> Copier tout le bloc ci-dessous dans une nouvelle session Claude Code, ouverte sur le dépôt
> `lyaminedb1/public-spending-market-prediction` (branche `main`, à jour).

---

Tu fais la revue complète de la rédaction du mémoire de MSc d'Elyamine Dali Braham (ECE Paris, remise le
**vendredi 2 octobre 2026 à minuit** : le rapport doit être prêt jeudi soir). Le code et les résultats sont terminés et vérifiés ; ta mission porte sur le **texte**.

## À lire d'abord
1. `CLAUDE.md` : contexte, périmètre, tous les chiffres de référence, guide de rédaction ECE, règles.
2. `redaction/README.md` puis les chapitres `redaction/chapitre1_…md` à `redaction/chapitre4_…md`.
3. Les résultats : `results/tables/` (surtout `models_metrics.csv`, `models_dm_tests.csv`, `ext_synthese.csv`,
   `ext_summary.csv`, `robustesse_lag.csv`, `models_permutation_oos.csv`, `diag_04/*.csv`, `extensions/E*.csv`,
   `eda_*.csv`) et les figures `results/figures/`.
4. `docs/plan_chapitre4.md` (plan de la discussion) et `docs/revue_04_models.md`.

## Ce que tu vérifies, dans cet ordre
1. **Chaque chiffre du texte contre les CSV.** R², p-values, RMSE, nombres de mois, de tests, de variables.
   Recalcule quand c'est possible (petit script Python). Signale toute valeur absente des résultats
   ou arrondie de façon trompeuse. Attention : les valeurs RF/XGBoost dépendent des versions de librairies
   (voir `CLAUDE.md`, « Reproductibilité ») ; compare aux CSV du dépôt, pas à une relance sur une autre machine.
2. **Cohérence entre chapitres** : mêmes chiffres, même vocabulaire (M0/M1/M2, « variation nulle »,
   « moyenne historique »), numérotation des tableaux et figures, renvois (« section 3.3 », « tableau 3.5 »).
3. **Méthode décrite = méthode codée** : décalages de publication (budget t-2, IPCH t-1), validation glissante,
   hyperparamètres (ne pas écrire « fixés a priori » ou « pré-enregistrés » pour 04), correction de
   Benjamini-Hochberg, tests DM. Compare le chapitre 2 au code de `src/02`, `04`, `06`, `11`, `14`.
4. **Chapitre 3 sans interprétation** (exigence ECE) : signale toute phrase qui explique « pourquoi ».
5. **Honnêteté des affirmations** : rien ne doit être présenté comme démontré s'il n'est qu'une hypothèse
   (ex. « l'information est déjà connue » : pas d'étude d'événement). Les résultats négatifs doivent être
   formulés avec la bonne portée (puissance faible : on exclut un effet fort, pas un effet faible).
6. **Bibliographie** : chaque citation du texte figure dans les références et inversement ; format APA ;
   les affirmations sur les articles correspondent à ce que disent les articles (les liens sont dans le
   chapitre 1 ; ne cite rien que tu n'as pas pu lire, dis-le).
7. **Conformité au guide ECE** (résumé dans `CLAUDE.md`) : parties manquantes, longueurs, considérations
   éthiques, déclaration d'usage de l'IA, légendes et sources des tableaux et figures.
8. **Langue** : français correct, phrases courtes, style « nous ». Relève les fautes, mais ne réécris pas le
   style d'Elyamine.

## Règles
- **Ne modifie pas les chapitres toi-même.** Écris un rapport : `docs/revue_redaction.md`, avec pour chaque
  problème : fichier, citation exacte du passage, ce qui ne va pas, la source qui le prouve (CSV + ligne,
  ou page de l'article), et une correction proposée. Classe par gravité : **erreur** (chiffre faux, affirmation
  fausse) / **à préciser** / **style**.
- Si tu trouves une vraie erreur dans le **code** ou les **résultats**, ne corrige rien : décris-la en tête du
  rapport, avec un exemple reproductible.
- Ne change jamais un résultat pour qu'il « marche mieux ». Un résultat négatif est un résultat.
- Règle ECE : le mémoire ne doit pas contenir d'interprétations générées par IA sans apport personnel
  d'Elyamine. Ne rédige pas de nouvelles sections d'interprétation ; tu peux proposer des questions à lui poser.
- Pas de caractères de substitution ni aucune technique pour tromper les détecteurs d'IA.
- Termine le rapport par : (a) une note sur 10 par chapitre avec deux lignes de justification,
  (b) les 10 corrections les plus importantes, dans l'ordre où les faire.
- Pousse le rapport sur une branche `revue-redaction` et ouvre une pull request ; ne fusionne pas.
