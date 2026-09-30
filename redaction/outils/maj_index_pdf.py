"""
Met à jour le sommaire et les listes (tableaux, figures) avec LibreOffice, puis enregistre le Word et le PDF.
Usage : python3 redaction/outils/maj_index_pdf.py      (LibreOffice et python3-uno requis)
Dans Word, on obtient le même résultat avec : Ctrl+A puis F9 (mettre à jour les champs).
"""
import subprocess
import time
from pathlib import Path

import uno
from com.sun.star.beans import PropertyValue

B = Path(__file__).resolve().parents[1] / "build"
DOCX = B / "Memoire_DaliBraham.docx"


def prop(n, v):
    p = PropertyValue(); p.Name = n; p.Value = v
    return p


proc = subprocess.Popen(["soffice", "--headless", "--invisible", "--norestore",
                         "--accept=socket,host=localhost,port=2002;urp;"])
try:
    ctx = None
    for _ in range(60):
        try:
            local = uno.getComponentContext()
            resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
            ctx = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
            break
        except Exception:
            time.sleep(1)
    desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    doc = desktop.loadComponentFromURL(DOCX.as_uri(), "_blank", 0, (prop("Hidden", True),))
    for _ in range(2):  # deux passes : les numéros de page bougent quand les listes se remplissent
        idx = doc.getDocumentIndexes()
        for i in range(idx.getCount()):
            idx.getByIndex(i).update()
        doc.refresh()
    doc.storeToURL(DOCX.as_uri(), (prop("FilterName", "MS Word 2007 XML"),))
    doc.storeToURL(DOCX.with_suffix(".pdf").as_uri(), (prop("FilterName", "writer_pdf_Export"),))
    print("index mis à jour :", idx.getCount())
    doc.close(True)
finally:
    proc.terminate()
