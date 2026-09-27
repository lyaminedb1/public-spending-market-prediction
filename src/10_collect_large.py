"""
10_collect_large.py
Collecte de la base élargie pour l'extension E16 (réplication de Bouillot, Candelon et Kool, 2025).
Voir docs/plan_extensions.md.

Sources ouvertes : FRED (séries OCDE « Main Economic Indicators » par pays, séries mondiales).
Les finances publiques viennent d'Eurostat via src/09_collect_panel.py (à lancer aussi).

À lancer sur ton ordinateur, depuis la racine du dépôt :
    python src/10_collect_large.py
puis :  git add data && git commit -m "Base élargie E16" && git push

Le script affiche les séries introuvables : ce n'est pas grave, la base reste large.
"""
from pathlib import Path
import time

import pandas as pd

from fred_http import fred_csv

OUT = Path("data/raw/large")
OUT.mkdir(parents=True, exist_ok=True)
START = "2000-01-01"

# code ISO-2 -> ISO-3 (certaines séries OCDE sur FRED utilisent l'ISO-3)
COUNTRIES = {"FR": "FRA", "DE": "DEU", "IT": "ITA", "ES": "ESP", "PT": "PRT", "BE": "BEL"}

# Séries par pays : (bloc, nom, modèle d'identifiant FRED ; {c2} = ISO-2, {c3} = ISO-3)
COUNTRY_SERIES = [
    ("marches", "taux_long", "IRLTLT01{c2}M156N"),
    ("marches", "taux_3m", "IR3TIB01{c2}M156N"),
    ("marches", "actions", "SPASTT01{c2}M661N"),
    ("macro", "chomage", "LRHUTTTT{c2}M156S"),
    ("macro", "ipch", "CP0000{c2}M086NEST"),
    ("macro", "production_ind", "{c3}PROINDMISMEI"),
    ("macro", "confiance_menages", "CSCICP03{c2}M665S"),
    ("macro", "confiance_entreprises", "BSCICP03{c2}M665S"),
    ("macro", "indicateur_avance", "{c3}LOLITONOSTSAM"),
    ("macro", "production_manuf", "{c3}PRMNTO01IXOBSAM"),
]

GLOBAL_SERIES = [
    ("mondial", "us_taux_10a", "GS10"),
    ("mondial", "us_fed_funds", "FEDFUNDS"),
    ("mondial", "us_pente_10a_2a", "T10Y2Y"),
    ("mondial", "us_ecart_haut_rendement", "BAMLH0A0HYM2"),
    ("mondial", "us_conditions_financieres", "NFCI"),
    ("mondial", "us_production_ind", "INDPRO"),
    ("mondial", "us_inflation", "CPIAUCSL"),
    ("mondial", "us_chomage", "UNRATE"),
    ("mondial", "vix", "VIXCLS"),
    ("mondial", "bce_facilite_depot", "ECBDFR"),
    ("mondial", "petrole_brent", "DCOILBRENTEU"),
    ("mondial", "eur_usd", "DEXUSEU"),
    ("mondial", "zone_euro_chomage", "LRHUTTTTEZM156S"),
    ("mondial", "zone_euro_ipch", "CP0000EZ19M086NEST"),
]


def fred(series_id):
    s = fred_csv(series_id)
    s = s[s.index >= START]
    # tout en mensuel : moyenne du mois pour les séries quotidiennes / hebdomadaires
    return s.groupby(s.index.to_period("M")).mean()


def save(cols, meta):
    df = pd.DataFrame(cols).sort_index()
    df.index = df.index.astype(str)
    df.to_csv(OUT / "base_elargie_mensuelle.csv", index_label="mois")
    pd.DataFrame(meta).to_csv(OUT / "dictionnaire_variables.csv", index=False)
    return df


if __name__ == "__main__":
    cols, meta, fails = {}, [], []
    for c2, c3 in COUNTRIES.items():
        for bloc, nom, pattern in COUNTRY_SERIES:
            sid = pattern.format(c2=c2, c3=c3)
            try:
                cols[f"{c2}_{nom}"] = fred(sid)
                meta.append({"variable": f"{c2}_{nom}", "pays": c2, "bloc": bloc, "fred_id": sid})
                print(f"    OK     {sid}", flush=True)
            except Exception as e:
                fails.append((sid, str(e)[:60]))
                print(f"    ÉCHEC  {sid}", flush=True)
            time.sleep(1.5)
        save(cols, meta)
        print(f"  {c2} : terminé", flush=True)
    for bloc, nom, sid in GLOBAL_SERIES:
        try:
            cols[nom] = fred(sid)
            meta.append({"variable": nom, "pays": "MONDE", "bloc": bloc, "fred_id": sid})
            print(f"    OK     {sid}", flush=True)
        except Exception as e:
            fails.append((sid, str(e)[:60]))
            print(f"    ÉCHEC  {sid}", flush=True)
        time.sleep(1.5)

    df = save(cols, meta)
    print(f"\nSéries récupérées : {len(cols)} ; période {df.index.min()} -> {df.index.max()}")
    if fails:
        print(f"Séries introuvables ({len(fails)}) :")
        for sid, e in fails:
            print(f"  {sid} : {e}")
    print("\nPense à lancer aussi : python src/09_collect_panel.py (finances publiques Eurostat)")
