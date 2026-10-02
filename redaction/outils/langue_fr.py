"""Langue du document Word : français (fr-FR) partout, pour que le correcteur de Word ne souligne pas tout le texte.
Usage : python redaction/outils/langue_fr.py   (à lancer après maj_index_pdf.py)"""
import re
import shutil
import zipfile
from pathlib import Path

DOCX = Path(__file__).resolve().parents[1] / "build" / "Memoire_DaliBraham.docx"
tmp = DOCX.with_suffix(".tmp.docx")
with zipfile.ZipFile(DOCX) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename.startswith("word/") and item.filename.endswith(".xml"):
            txt = data.decode("utf-8")
            txt = re.sub(r'(<w:lang\b[^>]*?w:val=")[^"]*(")', r"\1fr-FR\2", txt)
            txt = re.sub(r'(<w:themeFontLang\b[^>]*?w:val=")[^"]*(")', r"\1fr-FR\2", txt)
            data = txt.encode("utf-8")
        zout.writestr(item, data)
shutil.move(tmp, DOCX)
print("langue du document : fr-FR")
