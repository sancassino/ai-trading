"""Voegt recente M5-bars toe aan data/m5_fwd/<SYM>.csv (bij eerste keer gekopieerd uit de momentopname data/m5, die zelf ongewijzigd blijft) — samenvoegen op tijdstempel: bestaande bars blijven ongewijzigd, ontbrekende tijdstempels
worden toegevoegd (vult ook gaten van een eerdere onvolledige VM-sync); de nieuwste bar per batch kan nog lopen en wordt niet opgeslagen. Invoer = stdout van de bestaande VM-exporter mt5_export_recent.py (I1-formaat 'M5;SYM;time;o;h;l;c;spread',
laatste 2000 bars ≈ 7 handelsdagen; D1-regels worden genegeerd). Gebruik: ssh ... "python mt5_export_recent.py SYMS X" | python update_m5_recent.py"""
import os
import shutil
import sys

rows, added = {}, {}
for line in sys.stdin:
    p = line.strip().replace("\r", "").split(";")
    if p[0] == "M5" and len(p) == 8:
        rows.setdefault(p[1].replace(".cash", "cash"), []).append(";".join(p[2:]))
for sym, lines in rows.items():
    path = f"data/m5_fwd/{sym}.csv"
    if not os.path.exists(path) and os.path.exists(f"data/m5/{sym}.csv"):
        os.makedirs("data/m5_fwd", exist_ok=True); shutil.copyfile(f"data/m5/{sym}.csv", path)
    if not os.path.exists(path):
        print(f"{sym}: geen bestaand bestand, overgeslagen"); continue
    head = [l for l in open(path) if l.startswith("#") or not l[:1].isdigit()]
    have = {l.split(";")[0]: l.rstrip("\n") for l in open(path) if l[:1].isdigit()}
    batch = sorted(lines)[:-1]                                  # nieuwste bar kan nog lopen → niet opslaan
    new = [l for l in batch if l.split(";")[0] not in have]
    if new:
        have.update({l.split(";")[0]: l for l in new})
        with open(path + ".tmp", "w") as f:
            f.write("".join(head) + "\n".join(have[k] for k in sorted(have)) + "\n")
        os.replace(path + ".tmp", path)
    added[sym] = len(new)
print("update_m5_recent:", ", ".join(f"{k} +{v}" for k, v in added.items()))
