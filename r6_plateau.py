"""R6 (PREREG_CAT6 §1): plateau-/gevoeligheidsanalyse C02 (SMA 8/10/12) en C52 (venster/target/goud). Geen trial, geen optimalisatie. Ontdekking ≤ 2024."""
import importlib, math
import numpy as np
from datetime import date
from engine.forward import series
import r5_crossmarket as R5
DISC = date(2024, 12, 31)
out = ["# R6 — plateau-/gevoeligheidsanalyse (PREREG_CAT6 §1; geen optimalisatie, geen trial; ontdekking ≤ 2024)", ""]
# ---------- C02
prim = list(R5.PRIMARY); US5 = ["SPX", "NDX", "DJI", "DAX", "N225"]
M = {m: R5.load_market(m) for m in prim + US5}
out += ["## C02 Faber — SMA-venster (maanden)", "", "| venster | SPX 1928→: SR / ΔSR / maxDD / ΔmaxDD | 5 ontdekkingsindices gepoold: SR / ΔSR / ΔmaxDD | 12 buitenlandse markten gepoold: SR / ΔSR / ΔmaxDD | markten met ΔmaxDD<0 | markten met SR>0 |", "|---|---|---|---|---|---|"]
rows = {}
for n in (8, 10, 12):
    res = {}
    for m, D in M.items():
        me = R5.month_end_idx(D["dates"]); xf, _ = R5.faber(D["r"], D["rfd"], me, nwin=n); xb = R5.bh(D["r"], D["rfd"]); s0 = me[n - 1] + 1
        res[m] = (R5.sr(xf[s0:]), R5.sr(xb[s0:]), R5.maxdd(xf[s0:], D["rfd"][s0:]), R5.maxdd(xb[s0:], D["rfd"][s0:]))
    g = lambda ms, i: np.mean([res[m][i] for m in ms])
    us = res["SPX"]; ndd = sum(res[m][2] < res[m][3] for m in prim); npos = sum(res[m][0] > 0 for m in prim)
    rows[n] = dict(dsr_x=g(prim, 0) - g(prim, 1), dd_x=g(prim, 2) - g(prim, 3), dsr_us=g(US5, 0) - g(US5, 1), ndd=ndd, spx_sr=us[0])
    out.append(f"| {n}{' (basis)' if n == 10 else ''} | {us[0]:+.2f} / {us[0]-us[1]:+.2f} / {us[2]*100:.0f}% / {(us[2]-us[3])*100:+.0f} pp | {g(US5,0):+.2f} / {g(US5,0)-g(US5,1):+.2f} / {(g(US5,2)-g(US5,3))*100:+.0f} pp | {g(prim,0):+.2f} / {g(prim,0)-g(prim,1):+.2f} / {(g(prim,2)-g(prim,3))*100:+.0f} pp | {ndd}/12 | {npos}/12 |")
sign_ok = all(rows[n]["dsr_x"] > 0 for n in rows) or all(rows[n]["dsr_x"] <= 0 for n in rows)
dd_ok = all(rows[n]["ndd"] >= 9 for n in rows)
nb = np.mean([rows[8]["spx_sr"], rows[12]["spx_sr"]])
out.append(f"\nLeesregel: teken gepoold ΔSR (buitenland) gelijk over 8/10/12: **{'ja' if sign_ok else 'nee'}** (ΔSR {rows[8]['dsr_x']:+.3f} / {rows[10]['dsr_x']:+.3f} / {rows[12]['dsr_x']:+.3f}); ΔmaxDD < 0 in ≥ 9/12 voor alle vensters: **{'ja' if dd_ok else 'nee'}**; SPX-SR basis {rows[10]['spx_sr']:+.2f} vs buren gem. {nb:+.2f} → {'PIEK' if rows[10]['spx_sr'] - nb > 0.10 else 'geen piek'}.")
# ---------- C52
mod = importlib.import_module("catalogus.C52_allweather"); RULE = mod.RULE
RULE["instrumenten"] = list(dict.fromkeys(RULE["instrumenten"] + ["SPY", "BOND10_SYN", "GOLD_F"]))
cfgs = [("basis", {}), ("venster 30", {"win": 30}), ("venster 90", {"win": 90}), ("target 10%", {"tgt": 0.10}), ("target 12%", {"tgt": 0.12}), ("goud × 0,5", {"gold_mult": 0.5}), ("goud × 1,5", {"gold_mult": 1.5})]
def st(s):
    days = sorted(s); ex = np.array([s[d][0] for d in days]); tot = np.array([s[d][1] for d in days]); eq = np.cumprod(1 + tot)
    return ex.mean() / ex.std() * math.sqrt(252), eq[-1] ** (252 / len(tot)) - 1, float(np.max(1 - eq / np.maximum.accumulate(eq)))
for lab, base in (("lang (SPY + BOND10_SYN + GOLD_F, 2001→)", {"assets": ["SPY", "BOND10_SYN", "GOLD_F"], "start_jaar": 2001}), ("basis (SPY, IEF, GLD, DBC, 2003→)", {"start_jaar": 2003})):
    out += ["", f"## C52 {lab} — één parameter tegelijk", "", "| configuratie | SR (excess) | CAGR totaal | maxDD |", "|---|---|---|---|"]; srs = {}
    for name, extra in cfgs:
        RULE["varianten"]["p_" + name] = {**base, **extra}; s = series("C52_allweather", "p_" + name, "etf", end=DISC); a, b, c = st(s); srs[name] = a
        out.append(f"| {name} | {a:+.2f} | {b*100:.1f}% | {c*100:.1f}% |")
    nbrs = [v for k, v in srs.items() if k != "basis"]
    out.append(f"\nLeesregel: buren-SR {min(nbrs):+.2f}…{max(nbrs):+.2f} (basis {srs['basis']:+.2f}); alle binnen ±0,10 van basis: **{'ja → plateau' if all(abs(v - srs['basis']) <= 0.10 for v in nbrs) else 'nee'}**; basis − gem. buren = {srs['basis'] - np.mean(nbrs):+.2f} → {'PIEK' if srs['basis'] - np.mean(nbrs) > 0.10 else 'geen piek'}. (Vol-target 10/12% kan door de cap ≤ 1× gelijk zijn aan de basis.)")
open("results/R2/run6_plateau.md", "w").write("\n".join(out) + "\n"); print("\n".join(out))
