"""
fr_format.py : virgule décimale dans les figures (usage français du mémoire).

fr(fig) : à appeler juste avant fig.savefig(...).
  - graduations numériques (ScalarFormatter) : « 1.20 » -> « 1,20 » ;
  - textes libres (annotations, notes de bas de figure) : « 0.12 » -> « 0,12 » (chiffre.point.chiffre seulement).
Les valeurs ne changent pas, seulement le format d'affichage.
"""
import re

from matplotlib.ticker import ScalarFormatter

_DECIMAL = re.compile(r"(\d)\.(\d)")


class _FrScalar(ScalarFormatter):
    def __call__(self, x, pos=None):
        return super().__call__(x, pos).replace(".", ",")


def _fr_text(s: str) -> str:
    return _DECIMAL.sub(r"\1,\2", s)


def fr(fig):
    for ax in fig.axes:
        for axis in (ax.xaxis, ax.yaxis):
            if type(axis.get_major_formatter()) is ScalarFormatter:
                axis.set_major_formatter(_FrScalar())
        for t in ax.texts:
            t.set_text(_fr_text(t.get_text()))
    for t in fig.texts:
        t.set_text(_fr_text(t.get_text()))
    return fig
