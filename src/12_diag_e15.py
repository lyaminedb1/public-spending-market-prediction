"""
12_diag_e15.py — Diagnostic NON pré-enregistré de E15 (ajouté après résultat, signalé comme tel).
Compare spread trimestriel en moyenne (protocole) vs fin de trimestre, par sous-période.
Le gain de Ridge M0 (+14 %) vient de l autocorrélation mécanique des variations de moyennes (Working, 1960).
Usage : python src/12_diag_e15.py  (Ridge seul, ~1 min)
"""
import sys, importlib.util, numpy as np, pandas as pd
sys.path.insert(0,"src")
spec=importlib.util.spec_from_file_location("m","src/11_panel_models.py"); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
df=m.build_monthly()
def run(how="mean", start="2010Q1", models=("ridge","rf","xgb")):
    q=df.copy(); q["q"]=q.index.asfreq("Q")
    agg=q.groupby(["pays","q"]).agg(spread=("spread",how),vix=("vix_lvl","mean"),bce=("bce_facilite_depot_lvl","mean"),
        bund=("DE_taux_long_lvl",how),**{c:(c,"last") for c in q.columns if c.startswith("gov_")}).reset_index()
    out=[]
    for c,g in agg.groupby("pays"):
        g=g.sort_values("q").copy(); g["d_spread"]=g.spread.diff(); g["y"]=g.spread.shift(-1)-g.spread; g["d_bund"]=g.bund.diff()
        for p in m.PANEL: g[f"is_{p}"]=float(p==c)
        out.append(g)
    A=pd.concat(out).set_index("q")
    m0=["d_spread","spread","d_bund","vix","bce"]+[f"is_{p}" for p in m.PANEL]
    m1=m0+[c for c in A.columns if c.startswith("gov_")]
    A=A.dropna(subset=["y"]+m0)
    qs=sorted(x for x in A.index.unique() if x>=pd.Period("2010Q1","Q"))
    res={}
    for mod in models:
        for name,cols in (("M0",m0),("M1",m1)):
            recs=[]
            for qq in qs:
                tr=A[A.index<qq]; fit=m.make_model(mod).fit(tr[cols],tr.y); te=A[A.index==qq]
                for (_,r),pv in zip(te.iterrows(),fit.predict(te[cols])):
                    recs.append({"q":qq,"pays":r.pays,"y":r.y,"pred":pv,"moy":tr.loc[tr.pays==r.pays,"y"].mean()})
            res[(mod,name)]=pd.DataFrame(recs)
    rows=[]
    for (mod,name),P in res.items():
        for lab,sub in (("2010Q1+",P),("2015Q1+",P[P.q>=pd.Period(start if start!="2010Q1" else "2015Q1","Q")]),("2010-2014",P[P.q<pd.Period("2015Q1","Q")])):
            r2=(1-((sub.y-sub.pred)**2).sum()/((sub.y-sub.moy)**2).sum())*100
            rw=(1-((sub.y-sub.pred)**2).sum()/(sub.y**2).sum())*100
            rows.append((how,mod,name,lab,len(sub),round(r2,1),round(rw,1)))
    return pd.DataFrame(rows,columns=["agregation","modele","jeu","periode","n","R2_vs_moy","gain_vs_RW"])
pd.set_option("display.width",200)
d_mean, d_last = run("mean",models=("ridge",)), run("last",models=("ridge",))
print(d_mean.to_string(index=False))
print(d_last.to_string(index=False))
pd.concat([d_mean, d_last]).to_csv("results/tables/diag_e15.csv", index=False)
# autocorrélation des variations trimestrielles, moyenne vs fin de trimestre
q=df.copy(); q["q"]=q.index.asfreq("Q")
ar1 = []
for how in ("mean","last"):
    s=q.groupby(["pays","q"]).spread.agg(how).groupby(level=0).diff()
    ar1.append({"agregation": how, "AR1_delta_spread_trimestriel_moyenne_pays": round(s.groupby(level=0).apply(lambda x: x.autocorr()).mean(),3)})
    print(how, "AR1 Δspread trimestriel (panel) :", ar1[-1]["AR1_delta_spread_trimestriel_moyenne_pays"])
pd.DataFrame(ar1).to_csv("results/tables/diag_e15_ar1.csv", index=False)
