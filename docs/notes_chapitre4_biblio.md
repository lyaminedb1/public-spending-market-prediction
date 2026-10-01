# Chapitre 4 et bibliographie : notes de travail (01/10/2026)

> Notes pour Elyamine et son Claude. Les fichiers modifiés sont les exports `redaction/*.md` : ils doivent être reportés dans les documents Claude Docs (source de vérité) avant de régénérer le Word et le PDF (`redaction/README.md`).

## 1. Ce qui a été fait
- **Chapitre 4** (`redaction/chapitre4_discussion_brouillon.md`) : version finale 4.1 à 4.8 (≈ 3 100 mots, soit environ 10-11 pages avec la mise en forme ECE ; le guide demande 6-8). Numérotation des sections conservée (renvois du reste du mémoire). Les explications non testées sont présentées comme des hypothèses. Chaque résultat renvoie à un tableau, une figure ou une section du chapitre 3.
- **Bibliographie** : 37 → 47 références. Ajoutées : Brier (1950), Codogno et al. (2003), Hoerl et Kennard (1970), Leeper et al. (2013), MacKinlay (1997), Newey et West (1987), Pesaran et Timmermann (2007), Strobl et al. (2007), Timmermann (2006), Zou et Hastie (2005). Format APA harmonisé (italiques revue / volume, working papers avec numéro et éditeur). DOI ajoutés **seulement quand ils ont été retrouvés par recherche** ; les autres références n'en ont pas.
- **Citations ajoutées au chapitre 2** : Ridge (Hoerl et Kennard), score de Brier (E2), variance de Newey et West (E1), combinaison de prévisions (E8), Elastic Net (E9), fenêtre glissante (E11), basse fréquence (E17), régime de crise (E18).
- **Chapitre 1** : phrase corrigée sur Medeiros et al. (2021) et Goulet Coulombe et al. (2022) : le premier trouve que la forêt aléatoire domine pour l'inflation américaine ; le second attribue les gains du machine learning à la non-linéarité, surtout en période d'incertitude ou de tension financière (résumé en ligne).
- **Contrôle automatique** : `python redaction/outils/assemble.py` s'exécute sans erreur ; 47 références, toutes citées, 116 citations, aucune citation sans référence.

## 2. À relire ou confirmer avant la remise (non vérifiable dans cette session)
1. **Bouillot, Candelon et Kool (2025)** : l'article est inaccessible depuis cette session. Le résumé en ligne indique des données « 2007-2025 », alors que le chapitre 1 écrit « décembre 2008 à février 2025 » (échantillon d'estimation ?). À relire : RMSE de 7,3 pb pour la France sur 2020-2025, R² de 0,81 à 0,99 (0,86 pour la France), « une variable de finances publiques parmi les cinq plus importantes de chaque pays », comparaison aux régressions pénalisées, absence de marche aléatoire.
2. **Garlanda-Longueville (2023)** : le titre de la thèse vient de `theses.fr` (inaccessible ici) ; la page EconomiX affiche un autre intitulé de sujet. À confirmer.
3. **Attinasi et al. (2009)** : « l'annonce a compté, pas le montant » : confirmé seulement par Elyamine (30/09) ; le résumé en ligne ne le montre pas.
4. **Chiffres de Ridge** (chapitre 4.4) : pénalité supérieure à 10 000 dans 27 % (M0) et 44 % (M1) des mois pour le CAC 40, 90 % avec M2 ; inférieure à 100 dans 72 à 100 % des mois pour le spread. Source : `results/tables/diag_04/alpha_bornes_courant.csv` (script `src/16_diag_alpha.py`).
5. **Événements du 4.2** : début du Covid en mars 2020, présidentielle de 2017 (premier tour le 23 avril, second tour le 7 mai), dissolution annoncée le 9 juin 2024 : dates connues, mais à confirmer avec une source datée si le jury la demande.

6. **Références à contrôler une dernière fois** (non recoupées en ligne ou recoupées partiellement) : pages de Chen et Guestrin (2016), Fama (1970), Ramey (2011) ; Favero (2013) ; Working (1960) ; pages d'Engle (1982 : 987-1007, une source indique 1008) ; Lundberg et Lee (2017) ; Timmermann (2006, sans DOI). **DOI à cliquer pour contrôle** (retrouvés par recherche sans que la page affiche explicitement le couple titre-DOI) : Diebold et Mariano (1995), Harvey et al. (1997), Goulet Coulombe et al. (2022), Fama (1970), Engle (1982).

## 3. Règle ECE sur l'IA : à décider par Elyamine
Le guide interdit de rendre des interprétations générées par l'IA sans relecture critique et apport personnel. Ce chapitre a été rédigé avec l'aide de l'IA à partir de vos idées et de vos choix (par exemple « pas de preuve (pour l'instant) »). Il doit donc être **relu, corrigé et adapté** par Elyamine. La déclaration d'usage de l'IA dit aujourd'hui que « les interprétations relèvent de l'auteur » : cette phrase n'est exacte que si Elyamine a réellement repris les interprétations à son compte. Formulation possible :

> « J'ai utilisé un outil d'intelligence artificielle générative (Claude, d'Anthropic) comme assistant pour la programmation, la relecture du code et l'aide à la rédaction, y compris une première version du chapitre de discussion. J'ai relu, corrigé et validé l'ensemble du texte ; le choix du sujet, de la problématique, de la méthode et les conclusions m'appartiennent. »

## 4. Longueur
Le chapitre 4 fait environ 10-11 pages (guide : 6-8). Pour raccourcir sans perdre de contenu : fusionner 4.6 dans 4.8, ou ramener 4.7 aux trois limites principales.
