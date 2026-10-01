"""Voegt recente M5-bars (uit mt5_export_recent.py op de VM) toe aan data/m5/<SYM>.csv — append-only: alleen bars met een servertijd ná de laatste
bestaande bar; de lopende (onvolledige) bar wordt niet opgeslagen. Gebruik: ssh ... mt5_export_recent.py | python update_m5_recent.py"""
import sys
from datetime import datetime, timedelta

cur, rows, added = None, {}, {}
for line in sys.stdin:
    line = line.strip().replace("\r", "")
    if line.startswith("## "):
        cur = line.split()[1]; rows[cur] = []; continue
    if cur and line[:1].isdigit():
        rows[cur].append(line)
now_server = datetime.utcnow() + timedelta(hours=3)          # FTMO-server ≈ UTC+3 (zomer) — ruime marge hieronder
for sym, lines in rows.items():
    path = f"data/m5/{sym}.csv"
    try:
        last = max(l.split(";")[0] for l in open(path) if l[:1].isdigit())
    except FileNotFoundError:
        print(f"{sym}: geen bestaand bestand, overgeslagen"); continue
    new = sorted(l for l in lines if l.split(";")[0] > last)
    if new:
        new = new[:-1]                                          # laatste bar kan nog lopen → niet opslaan
    if new:
        with open(path, "a") as f:
            f.write("\n".join(new) + "\n")
    added[sym] = len(new)
print("update_m5_recent:", ", ".join(f"{k} +{v}" for k, v in added.items()))
