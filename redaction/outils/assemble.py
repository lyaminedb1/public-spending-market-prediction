"""Assemble les chapitres (exports Markdown des documents Claude Docs) en un seul Markdown pour pandoc.
Usage : python redaction/outils/assemble.py && pandoc redaction/build/memoire.md -o redaction/build/brut.docx && python redaction/outils/style.py"""
import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
MD = ROOT / "redaction"
OUT = ROOT / "redaction" / "build"
OUT.mkdir(exist_ok=True)
c1 = (MD/"chapitre1_etat_de_l_art.md").read_text()
c2 = (MD/"chapitre2_donnees_methodologie.md").read_text()

def split_body(txt, cut_titles):
    lines = txt.split("\n")
    # enlever le titre (ligne 1) et la ligne auteur/date (ligne 3)
    assert lines[0].startswith("# ")
    body = "\n".join(lines[3:])
    idx = min(body.find(t) for t in cut_titles if body.find(t) >= 0)
    return body[:idx].strip(), body[idx:]

b1, refs1 = split_body(c1, ["## Références bibliographiques"])
b2, refs2 = split_body(c2, ["## Références ajoutées par ce chapitre"])

def items(block):
    return [l[2:].strip() for l in block.split("\n") if l.startswith("- ")]

def section(block, title):
    i = block.find(title)
    if i < 0: return ""
    rest = block[i+len(title):]
    j = rest.find("\n#")
    return rest if j < 0 else rest[:j]

biblio = items(section(refs1, "## Références bibliographiques")) + items(section(refs2, "## Références ajoutées par ce chapitre"))
web = items(section(refs1, "### Sources en ligne")) + items(section(refs2, "## Sources en ligne"))
key = lambda s: re.sub(r"[^a-z]", "", s.lower().replace("é","e").replace("ü","u"))
biblio = sorted(set(biblio), key=key)
seen, web2 = set(), []
for w in web:
    k = re.findall(r"\((https?://[^)]+)\)", w)
    k = k[0].rstrip("/") if k else w
    if k not in seen:
        seen.add(k); web2.append(w)

# Chapitre 2 : légendes et sources des tableaux (guide ECE)
caps = [("Tableau 2.1 – Sources des données", "élaboration de l'auteur."),
        ("Tableau 2.2 – Soldes annuels reconstitués", "calculs de l'auteur à partir des situations mensuelles budgétaires (DGFiP)."),
        ("Tableau 2.3 – Variables cibles", "calculs de l'auteur (OCDE via FRED, Yahoo Finance), mars 2014 – juillet 2026."),
        ("Tableau 2.4 – Test de stationnarité (Dickey-Fuller augmenté)", "calculs de l'auteur."),
        ("Tableau 2.5 – Jeux de variables emboîtés", "élaboration de l'auteur."),
        ("Tableau 2.6 – Modèles comparés", "élaboration de l'auteur."),
        ("Tableau 2.7 – Mesures de performance", "élaboration de l'auteur."),
        ("Tableau 2.8 – Extensions testées", "élaboration de l'auteur ; plan daté dans docs/plan_extensions.md.")]
out, lines, k, i = [], b2.split("\n"), 0, 0
while i < len(lines):
    l = lines[i]
    if l.startswith("|") and (i == 0 or not lines[i-1].startswith("|")):
        out += [f"**{caps[k][0]}**", ""]
        while i < len(lines) and lines[i].startswith("|"):
            out.append(lines[i]); i += 1
        out += ["", f"*Source : {caps[k][1]}*"]
        k += 1
        continue
    out.append(l); i += 1
assert k == len(caps), k
b2 = "\n".join(out)
# formule : bloc latex -> équation
b2 = re.sub(r"```latex\n(.*?)\n```", "![](" + str(ROOT / "redaction" / "outils" / "formule_r2.png") + "){width=7.5cm}", b2, flags=re.S)
b2 = b2.replace("où y\\_t est", "où *y*~t~ est").replace("ŷ\\_t la", "*ŷ*~t~ la").replace("ȳ\\_t la", "*ȳ*~t~ la")


c3 = (MD/"chapitre3_resultats.md").read_text().split("\n")
assert c3[0].startswith("# ")
b3 = "\n".join(c3[3:]).replace("Figure 3.5 – Synthèse", "Figure 3.4 – Synthèse").replace("## Introduction du chapitre\n\n", "")
FIG = str(ROOT / "results" / "figures") + "/"
def fig(m):
    return f"![]({FIG}{m.group(2)}){{width=15.5cm}}\n\n**{m.group(1)}**\n\n*Source : calculs de l'auteur.*"
b3 = re.sub(r"\*\\\[(Figure 3\.\d – [^:]+?) : `results/figures/([^`]+)`\\\]\*", fig, b3)
assert "\\[Figure" not in b3, re.findall(r".*Figure.*", b3)

PB = ["```{=openxml}", '<w:p><w:r><w:br w:type="page"/></w:r></w:p>', "```", ""]
def field(instr):
    return ["```{=openxml}",
            '<w:p><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r><w:r><w:instrText xml:space="preserve"> '
            + instr + ' </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>'
            '(Clic droit puis « Mettre à jour les champs » dans Word)</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>',
            "```", ""]

lim = (MD / "pages_liminaires_intro_conclusion.md").read_text()
def sec(title, level="## "):
    i = lim.index(level + title)
    j = min([k for k in (lim.find("\n## ", i + 3), lim.find("\n# ", i + 3)) if k > 0] + [len(lim)])
    return lim[i + len(level + title):j].strip()
titre = [l for l in sec("Page de titre").split("\n") if l.strip()]
intro = lim[lim.index("# Introduction générale"):lim.index("# Conclusion générale")].strip()
concl = lim[lim.index("# Conclusion générale"):].strip()

doc = []
for k, l in enumerate(titre):
    doc += [f"::: {{custom-style=\"TitlePage{1 if k == 0 else 2}\"}}", l.replace("**", ""), ":::", ""]
doc += PB
for t in ("Remerciements", "Déclaration d'utilisation de l'intelligence artificielle"):
    doc += [f"# {t}", "", sec(t), ""] + PB
doc += ["# Résumé", "", sec("Résumé"), "", "# Abstract", "", sec("Abstract"), ""] + PB
doc += ["# Sommaire", ""] + field('TOC \\o "1-2" \\h \\z \\u') + PB
doc += ["# Liste des tableaux", ""] + field('TOC \\h \\z \\t "CaptionTable,1"')
doc += ["# Liste des figures", ""] + field('TOC \\h \\z \\t "CaptionFigure,1"') + PB
doc += ["# Liste des abréviations", "", sec("Liste des abréviations"), "", "# Glossaire", "", sec("Glossaire"), ""] + PB
doc += [intro, ""] + PB
doc += ["# Chapitre 1 – État de l'art", "", b1.strip(), ""] + PB
doc += ["# Chapitre 2 – Données et méthodologie", "", b2.strip(), ""] + PB
doc += ["# Chapitre 3 – Résultats", "", b3.strip(), ""] + PB
c4 = (MD/"chapitre4_discussion_brouillon.md").read_text().split("\n")
b4 = "\n".join(l for l in c4[3:] if not l.startswith("> **Statut")).strip()
if "## Références ajoutées par ce chapitre" in b4:
    b4, refs4 = b4.split("## Références ajoutées par ce chapitre", 1)
    biblio = sorted(set(biblio + items(refs4)), key=key)
doc += ["# Chapitre 4 – Discussion", "", b4.strip(), ""] + PB
doc += [concl, ""] + PB
doc += ["# Références", ""] + [f"::: {{custom-style=\"Bibliography\"}}\n{b}\n:::\n" for b in biblio]
doc += ["## Sources en ligne", ""] + [f"::: {{custom-style=\"Bibliography\"}}\n{w}\n:::\n" for w in web2]
doc += PB + [(MD / "annexes.md").read_text()]
(OUT / "memoire.md").write_text("\n".join(doc))
print("références:", len(biblio))
