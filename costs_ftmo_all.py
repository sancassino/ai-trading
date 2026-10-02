"""Spreads + rondreiskosten voor alle FTMO-symbolen met M5-data (D-086 → uitgebreid naar 166 symbolen, spoor 6 / C-028 'eerlijke RT vóór promote').
Zelfde definities als COSTS_FTMO_alle.csv (c4b2e24): periode 2024-01-01 → einde momentopname; spread = M5-barspread × point / close (bp);
bars met spread 0 = ontbrekend; beste uur = NY-uur met laagste mediaan (≥ 200 bars); rondreis = mediaan + 2× commissie.
Commissie per kant: FX €2,25/lot (MT5-deals), XAUUSD €2,00/lot (MT5-deals), overige metalen €2,00/lot (aangenomen); omrekening via tick_value uit de
FTMO-snapshot (notional_EUR = prijs × tick_value / point). Aandelen + crypto 0,002 %/kant (Q2-aanname). Indices/olie 0 (indices bevestigd);
agri/overige grondstoffen 0 = NIET bevestigd (vlag in commissie_bron). Uitvoer: COSTS_FTMO_alle.csv + COSTS_FTMO_alle_per_uur.csv."""
import csv
import glob
import os
from collections import defaultdict
from datetime import datetime, timedelta
from statistics import median

START = datetime(2024, 1, 1)
spec_file = sorted(glob.glob("data/ftmo_specs/*.csv"))[-1]
spec = {r["symbol"].replace(".cash", "cash"): r for r in csv.DictReader(open(spec_file), delimiter=";")}
path = {r["symbol"].replace(".cash", "cash"): r["path"] for r in csv.DictReader(open("SymbolList_FTMO.csv"), delimiter=";")}


def p90(x):
    x = sorted(x); return x[min(len(x) - 1, int(0.9 * len(x)))]


def commission(sym):
    cat = path.get(sym, "")
    sp = spec.get(sym)
    if cat.startswith(("Forex", "Exotics")):
        eur, src = 2.25, "FX €2,25/lot/kant (MT5-deals)"
    elif cat.startswith("Metals") and sym[:3] in ("XAU", "XAG", "XPT", "XPD"):
        eur, src = 2.00, "€2,00/lot/kant (MT5-deals)" if sym == "XAUUSD" else "€2,00/lot/kant (aangenomen)"
    elif cat.startswith(("Equities", "Crypto")):
        return 0.20, "0,002%/kant (aandelen/crypto, Q2-aanname)"
    elif cat.startswith(("Cash", )) or sym in ("USOILcash", "UKOILcash"):
        return 0.0, "0 (indices/olie; indices bevestigd)"
    else:
        return 0.0, "0 (grondstof-CFD; NIET bevestigd)"
    if not sp:
        return float("nan"), src + " — geen spec"
    notional = float(sp["bid"]) * float(sp["tick_value"]) / float(sp["point"])
    return eur / notional * 1e4, src


rows, per_uur = [], []
for f in sorted(glob.glob("data/m5/*.csv")):
    sym = os.path.basename(f)[:-4]
    point, allsp, byh, zero, n = None, [], defaultdict(list), 0, 0
    for line in open(f):
        if line.startswith("#"):
            point = float(line.split("point=")[1].split(";")[0]); continue
        if not line[:1].isdigit():
            continue
        t, o, h, l, c, s = line.rstrip().split(";")
        ts = datetime.strptime(t, "%Y.%m.%d %H:%M")
        if ts < START:
            continue
        n += 1
        if int(s) == 0:
            zero += 1; continue
        bp = int(s) * point / float(c) * 1e4
        allsp.append(bp); byh[(ts - timedelta(hours=7)).hour].append(bp)
    if not allsp:
        print(f"{sym}: geen spreads ≥ 2024"); continue
    hrs = {hh: v for hh, v in byh.items() if len(v) >= 200}
    best = min(hrs, key=lambda hh: median(hrs[hh])) if hrs else None
    com, src = commission(sym)
    med = median(allsp)
    rows.append([sym, f"{med:.2f}", f"{p90(allsp):.2f}", f"{median(hrs[best]):.2f}" if best is not None else "", "" if best is None else str(best),
                 f"{com:.2f}", f"{med + 2 * com:.2f}", src, f"{zero / n:.2f}"])
    for hh in sorted(byh):
        per_uur.append([sym, hh, f"{median(byh[hh]):.2f}", f"{p90(byh[hh]):.2f}", len(byh[hh])])

with open("COSTS_FTMO_alle.csv", "w") as f:
    f.write(f"# FTMO-kosten alle symbolen met M5-data (2024–2026, D-086; uitgebreid 2026-10-01 naar {len(rows)} symbolen, costs_ftmo_all.py). Spread = M5-barspread (bp), bars met spread 0 = ontbrekend (aandeel in 'aandeel_spread0');\n")
    f.write("# beste uur = NY-uur met laagste mediaan (≥ 200 bars); rondreis = mediaan + 2× commissie. Aandelen: veel spread-0-bars → mediaan onzeker (Q2 mat ≈ 2,9 bp rondreis). Swap apart: data/ftmo_specs/ + results/ceo/swap_side_map.csv.\n")
    f.write("symbol;spread_med_bp;spread_p90_bp;spread_med_beste_uur_bp;beste_uur_NY;commissie_bp_per_kant;rondreis_bp;commissie_bron;aandeel_spread0\n")
    for r in rows:
        f.write(";".join(r) + "\n")
with open("COSTS_FTMO_alle_per_uur.csv", "w") as f:
    f.write("symbol;uur_NY;spread_med_bp;spread_p90_bp;bars_met_spread\n")
    for r in per_uur:
        f.write(";".join(map(str, r)) + "\n")
print(len(rows), "symbolen")
