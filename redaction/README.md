# Rédaction du mémoire

**Source de vérité : les documents Claude Docs** (liens dans `CLAUDE.md`, section « Rédaction »). Les fichiers
`chapitre*.md` de ce dossier sont des **exports** de ces documents, pour la relecture et la revue dans GitHub.
Une correction faite ici doit être reportée dans le document Claude Docs (ou signalée à Elyamine), sinon elle sera
écrasée au prochain export.

| Fichier | État au 30/09/2026 (soir) |
|---|---|
| `chapitre1_etat_de_l_art.md` | Rédigé ; articles principaux vérifiés contre les PDF le 30/09 (Bouillot, Afonso, Attinasi, Belly, Ramey, Laubach, Garlanda-Longueville ; Barbier-Gauchard via le résumé) |
| `chapitre2_donnees_methodologie.md` | Rédigé ; considérations éthiques ajoutées (2.8) le 30/09 |
| `chapitre3_resultats.md` | Rédigé (≈ 9 pages, trop long pour le guide ECE : 4-6) |
| `chapitre4_discussion_brouillon.md` | **Brouillon complet** (4.1 à 4.6) ; à réécrire par Elyamine (règle ECE sur l'IA) |
| Introduction, conclusion, résumé, déclaration IA, annexes | Pas encore écrits |

## Construire le Word (mise en forme ECE)

```bash
pip install python-docx   # pandoc doit être installé
python redaction/outils/assemble.py
pandoc redaction/build/memoire.md -o redaction/build/brut.docx
python redaction/outils/style.py      # -> redaction/build/Memoire_DaliBraham.docx
```

Les figures viennent de `results/figures/` ; la formule du R² hors échantillon est une image (`outils/formule_r2.png`).
