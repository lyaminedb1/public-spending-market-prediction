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
