"""S3-parser: HistData M1 ASCII-zips (data/long_m1/*.zip) → data/long_m5/<SYM>.csv in het b4_sim-formaat (PREREG_S3.md).

HistData-tijd = EST zonder zomertijd (UTC−5). Doel = FTMO-servertijd = New York-lokaal + 7 u.
Spread = FTMO-mediaan 2021–26 per symbool en lokaal tijdstip (fractie van de koers) × koers.
Gebruik: python s3_histdata.py [invoermap] [uitvoermap]
"""
import glob
import io
import os
import re
import sys
import zipfile
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import numpy as np

import b4_sim

MAP = {"SPXUSD": "US500cash", "NSXUSD": "US100cash", "GRXEUR": "GER40cash", "XAUUSD": "XAUUSD"}
EST = timezone(timedelta(hours=-5))
NY = ZoneInfo("America/New_York")
POINT = 0.001


def spread_profile(sym):
    """mediane FTMO-spread (fractie) per lokaal (uur, minuut) in de sessie-tijdzone; fallback = totale mediaan."""
    tz = ZoneInfo(b4_sim.SYMS[sym][0])
    by = defaultdict(list); allv = []
    for b in b4_sim.load(sym):
        local = (b[0] - timedelta(hours=7)).replace(tzinfo=NY).astimezone(tz)
        f = b[5] / b[4]
        by[(local.hour, local.minute)].append(f); allv.append(f)
    prof = {k: float(np.median(v)) for k, v in by.items()}
    return prof, float(np.median(allv))


def to_server(est_naive):
    return est_naive.replace(tzinfo=EST).astimezone(NY).replace(tzinfo=None) + timedelta(hours=7)


def parse_lines(text):
    for line in text.splitlines():
        p = line.strip().split(";")
        if len(p) < 5 or not p[0][:8].isdigit():
            continue
        yield datetime.strptime(p[0], "%Y%m%d %H%M%S"), float(p[1]), float(p[2]), float(p[3]), float(p[4])


def convert(src_dir, out_dir, years=(2011, 2020)):
    os.makedirs(out_dir, exist_ok=True)
    files = defaultdict(list)
    for z in sorted(glob.glob(os.path.join(src_dir, "*.zip"))):
        m = re.search(r"(SPXUSD|NSXUSD|GRXEUR|XAUUSD)", os.path.basename(z).upper())
        if m:
            files[m.group(1)].append(z)
    report = {}
    for hd, zips in files.items():
        sym = MAP[hd]
        prof, fallback = spread_profile(sym)
        tz = ZoneInfo(b4_sim.SYMS[sym][0])
        _, (oh, om), (ch, cm), _ = b4_sim.SYMS[sym]
        bars = {}
        outside = inside = 0
        for z in zips:
            with zipfile.ZipFile(z) as zf:
                for name in zf.namelist():
                    if not name.lower().endswith(".csv"):
                        continue
                    for t, o, h, l, c in parse_lines(zf.read(name).decode("latin-1")):
                        srv = to_server(t)
                        ny = srv - timedelta(hours=7)
                        if not (years[0] <= ny.year <= years[1]):
                            continue
                        local = ny.replace(tzinfo=NY).astimezone(tz)
                        mins = local.hour * 60 + local.minute
                        if oh * 60 + om <= mins < ch * 60 + cm:
                            inside += 1
                        else:
                            outside += 1
                        k = srv.replace(minute=srv.minute // 5 * 5, second=0)
                        if k in bars:
                            b = bars[k]; b[1] = max(b[1], h); b[2] = min(b[2], l); b[3] = c
                        else:
                            bars[k] = [o, h, l, c]
        out = os.path.join(out_dir, f"{sym}.csv")
        with open(out, "w") as f:
            f.write(f"# bron: HistData M1 {hd} → M5 servertijd; spread = FTMO-mediaan 2021–26 per tijdstip;point={POINT};\n")
            f.write("time;open;high;low;close;spread\n")
            for k in sorted(bars):
                o, h, l, c = bars[k]
                local = (k - timedelta(hours=7)).replace(tzinfo=NY).astimezone(tz)
                sp = prof.get((local.hour, local.minute), fallback) * c
                f.write(f"{k:%Y.%m.%d %H:%M};{o};{h};{l};{c};{int(round(sp / POINT))}\n")
        report[sym] = (len(bars), inside, outside, min(bars) if bars else None, max(bars) if bars else None)
        print(f"{hd} → {sym}: {len(bars)} M5-bars ({report[sym][3]} … {report[sym][4]}), M1 binnen cash-uren {inside}, "
              f"erbuiten {outside} → {'24-uurs (futures-/CFD-afgeleid): OR op cash-open' if outside > inside * 0.2 else 'alleen cash-uren'}", flush=True)
    return report


if __name__ == "__main__":
    convert(sys.argv[1] if len(sys.argv) > 1 else "data/long_m1", sys.argv[2] if len(sys.argv) > 2 else "data/long_m5")
