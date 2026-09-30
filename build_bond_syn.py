"""R2: synthetisch 10j-Treasury-total-return-index uit ^TNX (Yahoo, data/daily/TNX_10Y.csv) — vast: modified duration 8, convexiteit 80,
dagrendement = yield_{t-1}/365 × kalenderdagen − D·Δy + ½·C·Δy². Schrijft data/derived/BOND10_SYN.csv (zelfde formaat als data/daily).
Validatie tegen IEF (2002→) en TLT-duratieverschil: zie results/R2/bond_syn_validatie.txt."""
import numpy as np
from datetime import date
D, C = 8.0, 80.0
rows = [l.rstrip("\n").split(";") for l in open("data/daily/TNX_10Y.csv") if l[:1].isdigit()]
ds = [date.fromisoformat(r[0]) for r in rows]; y = np.array([float(r[4]) for r in rows]) / 100
idx = [1.0]
for i in range(1, len(y)):
    dy = y[i] - y[i - 1]; cd = (ds[i] - ds[i - 1]).days
    idx.append(idx[-1] * (1 + y[i - 1] * cd / 365 - D * dy + 0.5 * C * dy * dy))
with open("data/derived/BOND10_SYN.csv", "w") as f:
    f.write("# synthetisch (build_bond_syn.py): 10j Treasury total return uit ^TNX, D=8, C=80; index start 1962 = 1\ndate;open;high;low;close;adjclose;volume\n")
    for d, v in zip(ds, idx):
        f.write(f"{d};{v:.6f};{v:.6f};{v:.6f};{v:.6f};{v:.6f};0\n")
# validatie
def ld(p):
    out = {}
    for l in open(p):
        if l[:1].isdigit():
            a = l.rstrip().replace(".", "-", 2).split(";") if "yahoo" in p else l.rstrip().split(";")
            out[a[0]] = float(a[1] if "yahoo" in p else a[5])
    return out
ief = ld("data/yahoo/IEF.csv"); syn = {str(d): v for d, v in zip(ds, idx)}
common = sorted(set(ief) & set(syn)); a = np.array([ief[k] for k in common]); b = np.array([syn[k] for k in common])
ra, rb = a[1:] / a[:-1] - 1, b[1:] / b[:-1] - 1
yrs = {}
for k, u, v in zip(common[1:], ra, rb):
    yrs.setdefault(k[:4], [0, 0]); yrs[k[:4]][0] += u; yrs[k[:4]][1] += v
txt = [f"dagcorrelatie IEF vs BOND10_SYN {np.corrcoef(ra, rb)[0,1]:.3f}; vol IEF {ra.std()*252**.5:.3f} syn {rb.std()*252**.5:.3f}; CAGR IEF {(a[-1]/a[0])**(252/len(a))-1:.4f} syn {(b[-1]/b[0])**(252/len(b))-1:.4f}"]
open("results/R2/bond_syn_validatie.txt", "w").write("\n".join(txt) + "\n")
print(txt[0])
