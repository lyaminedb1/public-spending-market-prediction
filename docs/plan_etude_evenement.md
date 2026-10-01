# Étude d'événement (E14) — plan daté avant exécution

Écrit le 2/10/2026 (nuit), **avant** tout calcul. Branche exploratoire, hors mémoire remis le 2/10.

## Données
- Dates de publication de la situation mensuelle budgétaire : `data/raw/smb_publication_dates.csv`, récupérées sur presse.economie.gouv.fr (40 publications, oct. 2017 – janv. 2026 ; le moteur de recherche du site n'en renvoie pas plus). Délai observé entre la fin du mois et la publication : 29 à 47 jours (médiane 33), ce qui confirme le décalage de 2 mois utilisé dans le mémoire sur 2017-2026.
- CAC 40 quotidien (Yahoo Finance, `^FCHI`, prix de clôture).
- Pas de taux OAT/Bund quotidiens accessibles (BCE : courbe zone euro seulement ; Banque de France, AFT, Bundesbank, stooq : bloqués). **Le spread ne peut donc pas être testé en quotidien.**

## Question et test principal (un seul)
Le rendement du CAC 40 le jour de la publication est-il lié à l'« innovation » budgétaire publiée ce jour-là ?
- Innovation = variation, entre deux publications consécutives, de l'écart du solde cumulé par rapport à l'année précédente (`b_solde_ytd_diff_yoy`, en % du total annuel). Signe : positif = solde plus favorable que le mois précédent.
- Variable expliquée : rendement du CAC 40 de clôture à clôture le jour de la publication (jour 0).
- Statistique : corrélation de Spearman, test bilatéral au seuil de 5 %. Un seul test principal : pas de correction.

## Tests secondaires (descriptifs, non corrigés, rapportés tous)
1. Rendement absolu moyen du jour 0 contre l'ensemble des jours de bourse (test de permutation).
2. Même corrélation au jour +1.

## Règle de décision
- « Positif » seulement si le test principal est significatif à 5 % **et** que le signe est cohérent avec l'économie (solde plus favorable → hausse). Même alors, avec ~40 événements, ce serait un résultat exploratoire, à ne pas mettre dans le mémoire remis sans accord.
- Sinon : résultat nul, rapporté tel quel. On n'ajoute aucune variante après avoir vu le résultat.

## Limites connues
~40 événements (puissance faible), heure de publication non vérifiée (une réaction intrajournalière peut être absente de la clôture), pas de spread quotidien.

## Résultat (exécuté après le plan, `python src/23_event_study.py`)
- **Test principal : nul.** 40 événements, Spearman = −0,13, p bilatérale = 0,42. Aucun lien entre l'innovation budgétaire publiée et le rendement du CAC 40 le jour de la publication.
- Secondaires (non corrigés) : jour +1, ρ = 0,00 (p = 0,99) ; |rendement| moyen au jour 0 = 0,70 % contre 0,79 % pour l'ensemble des jours (p = 0,74) : pas de réaction particulière les jours de publication.
- Règle de décision du plan : résultat non positif → rien n'est ajouté au mémoire. Aucune variante testée après coup.
- Par construction, ce test n'a de puissance que contre un effet fort (40 événements, rendements quotidiens bruités).
- Pistes non testables faute de données accessibles ici : spread OAT–Bund quotidien (sources bloquées), annonces budgétaires codées en surprises (pas de séries d'attentes d'économistes), versions successives des chiffres budgétaires (non archivées).
