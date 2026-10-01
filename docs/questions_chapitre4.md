# Chapitre 4 : questions pour Elyamine

> But : te permettre de réécrire la discussion **avec tes propres mots** (règle ECE : pas d'interprétation rédigée par l'IA sans apport personnel).
> Le brouillon actuel (`redaction/chapitre4_discussion_brouillon.md`) peut servir de liste d'idées. Pour chaque paragraphe : garder, couper ou contredire.
> Réponds en quelques phrases, comme à l'oral ; tu en tires ensuite le texte. Les chiffres à citer sont dans les chapitres 2 et 3.

## 4.1 Réponse à la problématique
1. En une phrase, que répondrais-tu à quelqu'un qui te demande « alors, les dépenses publiques prédisent-elles les marchés ? »
2. Pourquoi préfères-tu « pas de preuve (pour l'instant) » à « non » ? Qu'est-ce qui te ferait changer d'avis ?
3. Le résultat te surprend-il ? Qu'attendais-tu avant de voir les chiffres ?

## 4.2 Pourquoi les dépenses n'aident pas
4. Parmi les trois pistes (information déjà connue, causes non budgétaires, variable lente), laquelle te semble la plus convaincante, et sur quoi te fondes-tu ?
5. Le budget est voté avant l'année et publié avec deux mois de retard. Qu'est-ce que cela change pour un investisseur, selon toi ?
6. Pour les plus fortes variations du spread (mars 2020, présidentielle 2017, juin 2024), que s'est-il passé selon toi ? Quelles sources datées peux-tu citer ?
7. La France n'a pas connu de crise de la dette sur la période. Penses-tu que l'effet des dépenses serait différent en crise ? Qu'est-ce qui, dans tes résultats (E15, E18), t'y fait penser ou non ?

## 4.3 Ce que le résultat négatif veut dire
8. Avec 79 mois de test, jusqu'où peut-on conclure ? Comment l'expliquerais-tu à l'encadrante sans jargon ?
9. Que t'ont appris les contrôles avec du bruit et un signal fictif ? Qu'aurais-tu conclu sans eux ?
10. Pourquoi la variation nulle est-elle une référence plus exigeante que la moyenne pour les taux ?

## 4.4 Les modèles
11. Pourquoi XGBoost fait-il moins bien que Ridge ici ? Quelle est ton explication, et qu'est-ce qui la soutient dans tes résultats ?
12. Les prévisibilités trouvées (volatilité, sens de l'OAT) te semblent-elles utiles en pratique ? Pour qui ?

## 4.5 Comparaison avec la littérature
13. Quelle est la différence essentielle entre ton approche et celle de Bouillot et al. ? Pourquoi un R² de 95 % sur le niveau ne prouve-t-il pas une bonne prévision ?
14. Comment tes résultats s'articulent-ils avec Afonso et al. et Bernoth et al. (niveau des spreads, périodes de crise) ?
15. Relis Garlanda-Longueville (2023) : qu'est-ce qui, précisément, rapproche ou éloigne son résultat du tien ?

## 4.6 Implications, limites, suites
16. Quelle conséquence pratique tires-tu pour la recherche, pour un investisseur, pour les producteurs de données ouvertes ?
17. Quelle limite te paraît la plus sérieuse, et laquelle règlerais-tu en premier avec plus de temps ?
18. Si tu avais trois mois de plus, que ferais-tu en priorité (étude d'événement, annonces budgétaires, données en temps réel) ?

## Pour vérifier avant de rédiger
- Les affirmations sur Bouillot et al. (RMSE 7,3 pb pour la France, 1 variable de finances publiques sur 50, comparaison à la marche aléatoire) : à relire dans l'article.
- Les dates des événements citées en 4.2 : à confirmer avec une source datée.
