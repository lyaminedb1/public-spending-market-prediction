"""
13_collect_more.py
Collecte pour E19 (actions sectorielles), E20 (incertitude politique) et E14 (étude d'événement, données quotidiennes).
Protocoles : docs/plan_extensions.md.

À lancer sur ton ordinateur, depuis la racine du dépôt :
    python src/13_collect_more.py
puis :  git add data && git commit -m "Données E14 E19 E20" && git push
"""
from io import StringIO
from pathlib import Path
import subprocess

import pandas as pd
import yfinance as yf

from fred_http import fred_csv

OUT = Path("data/raw/more")
OUT.mkdir(parents=True, exist_ok=True)

STOCKS = {"DG.PA": "vinci", "FGR.PA": "eiffage", "EN.PA": "bouygues",
          "HO.PA": "thales", "AM.PA": "dassault_aviation", "^FCHI": "cac40"}


def curl(url, timeout=30):
    r = subprocess.run(["curl", "-s", "-L", "--max-time", str(timeout), "-A", "Mozilla/5.0", url],
                       capture_output=True, text=True, timeout=timeout + 5)
    return r.stdout


print("1. Actions (Yahoo Finance), clôture non ajustée, quotidien depuis 2012")
px = {}
for tk, name in STOCKS.items():
    try:
        h = yf.download(tk, start="2012-01-01", auto_adjust=False, progress=False)
        s = h["Close"].squeeze().dropna()
        px[name] = s
        print(f"  OK     {tk:7s} {s.index.min().date()} -> {s.index.max().date()} ({len(s)} jours)")
    except Exception as e:
        print(f"  ÉCHEC  {tk} : {e}")
daily = pd.DataFrame(px)
daily.index.name = "date"
daily.to_csv(OUT / "actions_quotidien.csv")
monthly = daily.resample("ME").last()
monthly.index = monthly.index.to_period("M").astype(str)
monthly.to_csv(OUT / "actions_mensuel.csv", index_label="mois")

print("2. Incertitude de politique économique, France (Baker-Bloom-Davis, via FRED)")
for sid in ("FRAEPUINDXM", "EUEPUINDXM"):
    try:
        s = fred_csv(sid)
        s.to_frame(sid).to_csv(OUT / f"epu_{sid}.csv", index_label="date")
        print(f"  OK     {sid} {s.index.min().date()} -> {s.index.max().date()}")
    except Exception as e:
        print(f"  ÉCHEC  {sid} : {str(e)[:80]}")

print("3. Taux à 10 ans quotidiens France / Allemagne (E14)")
for code, name in (("10fry.b", "oat_10y"), ("10dey.b", "bund_10y")):
    txt = curl(f"https://stooq.com/q/d/l/?s={code}&i=d")
    try:
        df = pd.read_csv(StringIO(txt))
        assert "Close" in df.columns and len(df) > 1000
        df[["Date", "Close"]].rename(columns={"Date": "date", "Close": name}).to_csv(OUT / f"{name}_quotidien.csv", index=False)
        print(f"  OK     {name} (stooq) {df.Date.min()} -> {df.Date.max()} ({len(df)} jours)")
    except Exception:
        print(f"  ÉCHEC  {name} (stooq) : réponse = {txt[:80]!r}")

print("\nTerminé. Pousse le dossier data/ sur GitHub.")
