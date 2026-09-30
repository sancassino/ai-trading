"""D3-QA voor data/daily: afronden (6 sign. cijfers), gaten, dubbele datums, OHLC-consistentie, sprongen > 20%, overlap met FTMO-M5 (2022–26).
Schrijft data/DATA_CATALOGUS.md (D2-deel) en data/CHECKSUMS_daily.sha256."""
import glob, hashlib, os
from collections import defaultdict
from datetime import date, timedelta
import numpy as np

def r6(x):
    return "" if x == "" else f"{float(x):.6g}"

rows_out = []
for p in sorted(glob.glob("data/daily/*.csv")):
    lines = open(p).read().splitlines()
    hdr = [l for l in lines if l.startswith("#") or l.startswith("date")]
    body = [l.split(";") for l in lines if l[:1].isdigit()]
    body = [[b[0]] + [r6(x) for x in b[1:6]] + [b[6].split(".")[0] if b[6] else ""] for b in body]
    with open(p, "w") as f:
        f.write("\n".join(hdr) + "\n" + "\n".join(";".join(b) for b in body) + "\n")
    d = [date.fromisoformat(b[0]) for b in body]; c = np.array([float(b[4]) for b in body])
    dup = len(d) - len(set(d))
    gaps = sum(1 for a, b in zip(d, d[1:]) if (b - a).days > 7)
    bad = sum(1 for b in body if b[1] and b[2] and b[3] and not (float(b[3]) <= min(float(b[1]), float(b[4])) + 1e-9 and float(b[2]) >= max(float(b[1]), float(b[4])) - 1e-9))
    nonpos = int((c <= 0).sum())
    r = c[1:] / c[:-1] - 1
    jumps = int((np.abs(r) > 0.20).sum())
    noohlc = sum(1 for b in body if not (b[1] and b[2] and b[3]))
    rows_out.append((os.path.basename(p)[:-4], d[0], d[-1], len(d), dup, gaps, bad, noohlc, nonpos, jumps))

# overlap met FTMO (slot rond 16:00 NY resp. 17:30 Berlijn vs Yahoo-slot), dagrendementen 2022–2026
import b4_sim
def ftmo_close(sym):
    out = {}
    for d, s in b4_sim.sessions(sym):
        out[d] = s[-1][4]
    return out
def yahoo(name):
    return {date.fromisoformat(l.split(";")[0]): float(l.split(";")[4]) for l in open(f"data/daily/{name}.csv") if l[:1].isdigit()}
ov = []
for y, f in (("SPX", "US500cash"), ("NDX", "US100cash"), ("DAX", "GER40cash"), ("GOLD_F", "XAUUSD")):
    a, b = yahoo(y), ftmo_close(f)
    ds = sorted(d for d in a if d in b and d.year >= 2022)
    ra = np.diff(np.log([a[d] for d in ds])); rb = np.diff(np.log([b[d] for d in ds]))
    ov.append((y, f, len(ds), np.corrcoef(ra, rb)[0, 1], np.median(np.abs(np.log(np.array([b[d] for d in ds]) / np.array([a[d] for d in ds])))) * 100))

with open("data/CHECKSUMS_daily.sha256", "w") as f:
    for p in sorted(glob.glob("data/daily/*.csv")):
        f.write(f"{hashlib.sha256(open(p, 'rb').read()).hexdigest()}  {p}\n")
with open("data/DATA_CATALOGUS.md", "w") as f:
    f.write("# DATA_CATALOGUS (Uitvoerder; bijgewerkt 2026-09-30)\n\n## D2 — lange dagdata `data/daily/` (Yahoo chart-API, eerlijke UA, 3 s/verzoek; in de repo)\n")
    f.write("Kolommen: date;open;high;low;close;adjclose;volume (6 sign. cijfers). Checksums: data/CHECKSUMS_daily.sha256.\n\n")
    f.write("| reeks | van | tot | dagen | dubbel | gaten > 7 d | OHLC-inconsistent | zonder OHLC | ≤ 0 | sprongen > 20% |\n|---|---|---|---|---|---|---|---|---|---|\n")
    for r in rows_out:
        f.write("| " + " | ".join(str(x) for x in r) + " |\n")
    f.write("\n**Overlap met FTMO (2022–26, dagrendementen slot-op-slot):**\n\n| Yahoo | FTMO | dagen | corr | mediaan |niveauverschil| % |\n|---|---|---|---|---|\n")
    for y, fsym, n, cr, lv in ov:
        f.write(f"| {y} | {fsym} | {n} | {cr:.3f} | {lv:.2f} |\n")
    f.write("\nNB: Yahoo-indices zijn cash-indexslotkoersen; futures (GC=F e.d.) zijn doorlopende front-month-reeksen (rolsprongen mogelijk); "
            "FX (=X) vanaf 1996/2003. Dagen zonder OHLC (alleen slot) komen vooral voor in vroege jaren.\n\n## D1 — Dukascopy-intraday `data/long_m1/` (lokaal, niet in repo)\n"
            "Zie results/p0/p0_log.txt; SPX 2011 niet op de feed; 2012→ loopt. Wordt bijgewerkt zodra jaren compleet zijn.\n")
for r in rows_out: print(r)
for o in ov: print(o)
