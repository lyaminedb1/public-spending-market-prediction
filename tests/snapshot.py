"""
snapshot.py : photographier les sorties CSV pour comparer avant/après une modification.

  python tests/snapshot.py save NOM      copie data/processed et results/tables dans tests/_snap/NOM/
  python tests/snapshot.py diff A B      liste fichiers ajoutés / supprimés / modifiés, et l'écart
                                         absolu maximum par colonne numérique
Les instantanés (tests/_snap/) ne sont pas suivis par git.
"""
import hashlib
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SNAP = ROOT / "tests" / "_snap"
SOURCES = ["data/processed", "results/tables"]


def csv_files(base: Path):
    return sorted(p for src in SOURCES for p in (base / src).rglob("*.csv"))


def md5(p: Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()


def save(name: str) -> None:
    dest = SNAP / name
    if dest.exists():
        shutil.rmtree(dest)
    rows = []
    for p in csv_files(ROOT):
        rel = p.relative_to(ROOT)
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest / rel)
        d = pd.read_csv(p)
        rows.append({"chemin": str(rel), "lignes": len(d), "colonnes": d.shape[1], "md5": md5(p)})
    pd.DataFrame(rows).to_csv(dest / "manifest.csv", index=False)
    print(f"Instantané '{name}' : {len(rows)} fichiers CSV -> {dest}")


def compare_csv(a: Path, b: Path) -> list[str]:
    da, db = pd.read_csv(a), pd.read_csv(b)
    msgs = []
    if list(da.columns) != list(db.columns):
        msgs.append(f"colonnes différentes : -{sorted(set(da.columns) - set(db.columns))} "
                    f"+{sorted(set(db.columns) - set(da.columns))}")
    if len(da) != len(db):
        msgs.append(f"lignes : {len(da)} -> {len(db)}")
    if msgs:
        return msgs
    for c in da.columns:
        if pd.api.types.is_numeric_dtype(da[c]) and pd.api.types.is_numeric_dtype(db[c]):
            x, y = da[c].to_numpy(float), db[c].to_numpy(float)
            if (np.isnan(x) != np.isnan(y)).any():
                msgs.append(f"{c} : NaN différents")
                continue
            m = ~np.isnan(x)
            e = np.abs(x[m] - y[m]).max() if m.any() else 0.0
            if e > 0:
                msgs.append(f"{c} : écart max {e:.3g}")
        elif not da[c].equals(db[c]):
            msgs.append(f"{c} : valeurs texte différentes")
    return msgs


def diff(a: str, b: str) -> int:
    A, B = SNAP / a, SNAP / b
    fa = {p.relative_to(A): p for p in csv_files(A)}
    fb = {p.relative_to(B): p for p in csv_files(B)}
    n = 0
    for k in sorted(set(fa) - set(fb)):
        print(f"SUPPRIMÉ  {k}"); n += 1
    for k in sorted(set(fb) - set(fa)):
        print(f"AJOUTÉ    {k}"); n += 1
    for k in sorted(set(fa) & set(fb)):
        if md5(fa[k]) != md5(fb[k]):
            msgs = compare_csv(fa[k], fb[k]) or ["octets différents (formatage), valeurs identiques"]
            print(f"MODIFIÉ   {k}")
            for m in msgs:
                print(f"            {m}")
            n += 1
    print("aucune différence" if n == 0 else f"{n} fichier(s) différent(s)")
    return n


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "save":
        save(sys.argv[2])
    elif len(sys.argv) == 4 and sys.argv[1] == "diff":
        sys.exit(1 if diff(sys.argv[2], sys.argv[3]) else 0)
    else:
        print(__doc__)
        sys.exit(2)
