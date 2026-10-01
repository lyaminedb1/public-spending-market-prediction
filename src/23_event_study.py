"""Étude d'événement (plan daté : docs/plan_etude_evenement.md, écrit avant l'exécution).
Test principal : Spearman entre l'innovation budgétaire publiée (variation du solde cumulé vs année précédente, % du total annuel)
et le rendement du CAC 40 le jour de la publication. Secondaires : |rendement| jour 0 vs tous les jours ; Spearman au jour +1."""
import json, subprocess
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
TAB = ROOT / "results" / "tables"


def cac_daily() -> pd.Series:
    p = ROOT / "data" / "raw" / "cac40_daily.csv"
    if not p.exists():
        url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EFCHI?period1=1388534400&period2=1790000000&interval=1d"
        out = subprocess.run(["curl", "-s", "-m", "60", "-A", "Mozilla/5.0", url], capture_output=True, text=True).stdout
        r = json.loads(out)["chart"]["result"][0]
        s = pd.Series(r["indicators"]["quote"][0]["close"], index=pd.to_datetime(r["timestamp"], unit="s").normalize(), name="close")
        s.dropna().rename_axis("date").to_csv(p)
    return pd.read_csv(p, index_col="date", parse_dates=True)["close"]


def main() -> None:
    px = cac_daily()
    ret = px.pct_change().dropna() * 100
    ev = pd.read_csv(ROOT / "data" / "raw" / "smb_publication_dates.csv")
    ds = pd.read_csv(ROOT / "data" / "processed" / "dataset_monthly.csv", parse_dates=["mois"]).set_index("mois")
    gap = ds["b_solde_ytd_diff_yoy"]  # ligne t = situation du mois t-2
    rows = []
    for _, e in ev.iterrows():
        m = pd.Timestamp(int(e.annee_situation), int(e.mois_situation), 1)
        t, tp = m + pd.DateOffset(months=2), m + pd.DateOffset(months=1)
        if t not in gap.index or tp not in gap.index:
            continue
        d0 = pd.Timestamp(e.date_publication)
        i = ret.index.searchsorted(d0)  # premier jour de bourse >= date de publication
        if i + 1 >= len(ret):
            continue
        rows.append({"publication": d0.date(), "situation": m.strftime("%Y-%m"), "innovation": gap[t] - gap[tp],
                     "ret_j0": ret.iloc[i], "ret_j1": ret.iloc[i + 1], "jour_bourse_j0": ret.index[i].date()})
    df = pd.DataFrame(rows).dropna()
    df.to_csv(TAB / "event_study_events.csv", index=False)
    r0, p0 = stats.spearmanr(df.innovation, df.ret_j0)
    r1, p1 = stats.spearmanr(df.innovation, df.ret_j1)
    # secondaire : |rendement| au jour 0 contre tous les jours (permutation)
    rng = np.random.default_rng(42)
    allabs = ret.abs().values
    obs = df.ret_j0.abs().mean()
    perm = np.array([rng.choice(allabs, len(df), replace=False).mean() for _ in range(20000)])
    p_abs = (perm >= obs).mean()
    res = pd.DataFrame([
        {"test": "PRINCIPAL : Spearman innovation vs rendement CAC 40 jour 0", "n": len(df), "stat": r0, "p_bilaterale": p0},
        {"test": "secondaire : Spearman innovation vs rendement jour +1", "n": len(df), "stat": r1, "p_bilaterale": p1},
        {"test": "secondaire : |rendement| moyen jour 0 (%) vs tous les jours (permutation, unilatéral)", "n": len(df),
         "stat": obs, "p_bilaterale": p_abs},
    ])
    res["reference"] = ["", "", f"moyenne tous jours = {allabs.mean():.3f} %"]
    res.round(4).to_csv(TAB / "event_study.csv", index=False)
    print(res.round(4).to_string(index=False))
    print(df.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
