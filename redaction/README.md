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
| `pages_liminaires_intro_conclusion.md` | Page de titre, remerciements, déclaration IA courte (à valider par Elyamine), résumé (sans abstract anglais : non demandé par le guide), abréviations, glossaire, introduction, conclusion (30/09 soir) |
| `annexes.md` | Généré par `outils/annexes.py` depuis les CSV (variables, 210 comparaisons, graines, bruit, décalage, reproductibilité) |

## Construire le Word (mise en forme ECE)

```bash
pip install python-docx   # pandoc doit être installé
python redaction/outils/annexes.py
python redaction/outils/assemble.py
pandoc redaction/build/memoire.md -o redaction/build/brut.docx
python redaction/outils/style.py         # -> redaction/build/Memoire_DaliBraham.docx
python3 redaction/outils/maj_index_pdf.py  # sommaire + listes (LibreOffice) -> .docx et .pdf à jour
```

Les figures viennent de `results/figures/` ; la formule du R² hors échantillon est une image (`outils/formule_r2.png`).
