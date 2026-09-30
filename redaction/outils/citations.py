"""Citations numérotées (style IEEE, liste des références en ordre alphabétique, comme le demande le guide ECE).
Chaque citation « Auteur (année) » ou « (Auteur, année) » devient un numéro [n] cliquable qui renvoie à la
référence n de la bibliographie. Les documents sources gardent le format auteur-année ; la conversion se fait
à l'assemblage.
"""
import re

ANNEE = r"(?:19|20)\d\d"


def premier_auteur(ref):
    """Nom du premier auteur et année d'une référence APA."""
    nom = "Goulet Coulombe" if ref.startswith("Goulet Coulombe") else re.match(r"[^,]+", ref).group(0).strip()
    annee = re.search(r"\((%s)\)" % ANNEE, ref).group(1)
    return nom, annee


def numeroter(texte, biblio):
    """Remplace les citations du texte par des numéros ; renvoie le texte et la liste des références numérotées."""
    cle = {}
    for n, ref in enumerate(biblio, 1):
        k = premier_auteur(ref)
        assert k not in cle, k
        cle[k] = n
    noms = sorted({k[0] for k in cle}, key=len, reverse=True)
    alt = "|".join(re.escape(x) for x in noms)
    # noms d'auteurs suivants : lettres, espaces, virgules, « et », « al. », particules ; jamais de chiffres ni de parenthèses
    suite = r"(?:(?:,\s|\s)(?:et al\.|et|von|de|[A-ZÉ][\w’'\-.]*|López|Büchner))*"
    utilises = set()

    def lien(n):
        utilises.add(n)
        return f"[{n}](#ref{n})"

    def num(nom, annee, brut):
        n = cle.get((nom, annee))
        if n is None:
            raise KeyError(f"citation sans référence : {brut!r}")
        return n

    # 0. titres : pas de numéro dans un titre ; le numéro va à la première mention dans le paragraphe qui suit
    def titre(m):
        h, corps = m.group(1), m.group(2)
        mm = re.search(rf"\s?\((?P<nom>{alt}){suite},\s(?P<an>{ANNEE})\)", h) or \
            re.search(rf"(?P<nom>{alt}){suite}(?P<p>\s\((?P<an>{ANNEE})\))", h)
        if not mm:
            return m.group(0)
        n = num(mm["nom"], mm["an"], mm.group(0))
        h = h.replace(mm.group(0), "") if "p" not in mm.groupdict() or mm.group("p") is None else h.replace(mm.group("p"), "")
        auteurs = re.match(rf"{re.escape(mm['nom'])}{suite}", corps)
        if auteurs:
            corps = corps[:auteurs.end()] + f" [{lien(n)}]" + corps[auteurs.end():]
        else:
            fin = re.search(r"\s*[.:](\s|$)", corps).start()
            corps = corps[:fin] + f" [{lien(n)}]" + corps[fin:]
        return h + "\n\n" + corps

    texte = re.sub(r"^(#{1,4} [^\n]+)\n\n([^#\n][^\n]*)", titre, texte, flags=re.M)

    # 1. citations entre parenthèses : (A, 2015) ; (A et B, 2008 ; C et al., 2012) ; (voir A, 2015)
    par = re.compile(rf"(?P<nom>{alt}){suite},\s(?P<an>{ANNEE})")

    def parenthese(m):
        contenu = m.group(1)
        if not par.search(contenu):
            return m.group(0)
        morceaux = [c.strip() for c in contenu.split(";")]
        nums, reste = [], []
        for c in morceaux:
            mm = par.fullmatch(c)
            if mm:
                nums.append(num(mm["nom"], mm["an"], c))
            else:
                reste.append(c)
        if reste:  # texte libre dans la parenthèse : on remplace sur place
            return "(" + par.sub(lambda mm: "[" + lien(num(mm["nom"], mm["an"], mm.group(0))) + "]", contenu) + ")"
        return "[" + ", ".join(lien(n) for n in nums) + "]"

    texte = re.sub(r"\(([^()\n]{0,300}?)\)", parenthese, texte)

    # 2. citations dans la phrase : A (2015), A et B (2008), A et al. (2012) → A et al. [n]
    nar = re.compile(rf"(?P<auteurs>(?P<nom>{alt}){suite})\s\((?P<an>{ANNEE})\)")
    texte = nar.sub(lambda m: f"{m['auteurs']} [{lien(num(m['nom'], m['an'], m.group(0)))}]", texte)

    # contrôle : plus aucune citation auteur-année
    reste = re.findall(rf"(?:{alt})[^\n|\[\]]{{0,60}}?(?:\({ANNEE}\)|,\s{ANNEE}\b)", texte)
    assert not reste, reste
    non_cites = [biblio[n - 1][:50] for n in range(1, len(biblio) + 1) if n not in utilises]
    refs = [f"[]{{#ref{n}}}\\[{n}\\] {r}" for n, r in enumerate(biblio, 1)]
    return texte, refs, non_cites
