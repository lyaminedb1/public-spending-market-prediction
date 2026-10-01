"""fr_format.py : virgule décimale dans toutes les figures (le mémoire est en français).
Importer ce module avant de créer les figures : les textes (graduations, annotations, légendes) qui contiennent
un nombre à point décimal (« 0.12 ») s'affichent avec une virgule (« 0,12 »). Aucun effet sur les calculs ni les CSV."""
import re

import matplotlib.text as mtext

_PT = re.compile(r"(?<=\d)\.(?=\d)")
_set_text = mtext.Text.set_text


def _set_text_fr(self, s):
    if isinstance(s, str):
        s = _PT.sub(",", s)
    return _set_text(self, s)


mtext.Text.set_text = _set_text_fr
