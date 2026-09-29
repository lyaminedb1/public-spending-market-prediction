"""
data_manifest.py : gel des données brutes par hash.
  python tests/data_manifest.py write   écrit data/MANIFEST.csv (chemin, taille, md5) pour data/raw/**
  python tests/data_manifest.py check   vérifie que les données brutes n'ont pas changé (code de sortie 1 sinon)
Les données brutes sont l'entrée de tout le pipeline : si elles changent, les résultats changent.
"""
import hashlib
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "data" / "MANIFEST.csv"


def scan():
    rows = []
    for p in sorted((ROOT / "data" / "raw").rglob("*")):
        if p.is_file() and p.name != ".gitkeep":
            rows.append({"chemin": str(p.relative_to(ROOT)), "taille": p.stat().st_size,
                         "md5": hashlib.md5(p.read_bytes()).hexdigest()})
    return pd.DataFrame(rows)


def check():
    """Renvoie la liste des écarts (vide si les données brutes sont conformes au manifeste)."""
    ref, now = pd.read_csv(MAN).set_index("chemin"), scan().set_index("chemin")
    problems = [f"absent : {c}" for c in ref.index.difference(now.index)]
    problems += [f"nouveau : {c}" for c in now.index.difference(ref.index)]
    common = ref.index.intersection(now.index)
    problems += [f"modifié : {c}" for c in common if ref.loc[c, "md5"] != now.loc[c, "md5"]]
    return problems


if __name__ == "__main__":
    if sys.argv[1:] == ["write"]:
        df = scan()
        df.to_csv(MAN, index=False)
        print(f"{len(df)} fichiers -> {MAN}")
    elif sys.argv[1:] == ["check"]:
        p = check()
        print("données brutes conformes au manifeste" if not p else "\n".join(p))
        sys.exit(1 if p else 0)
    else:
        print(__doc__)
        sys.exit(2)
