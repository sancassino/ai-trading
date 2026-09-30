"""AUDIT_1 §3: eigen BH-FDR + p-waarde-controle op catalogus/TRIALS.csv (main en uitvoerder2-r)."""
import sys, numpy as np, pandas as pd
from scipy.stats import norm
def bh(p):
    p = np.asarray(p, float); n = len(p); o = np.argsort(p); q = np.empty(n); run = 1.0
    for rank in range(n, 0, -1):
        i = o[rank - 1]; run = min(run, p[i] * n / rank); q[i] = run
    return q
KEY = ("C02_faber:basis","C52_allweather:lang","C52_allweather:basis","C55_daa:basis","C44_krediet:basis","C16_halloween:basis","C33_trend_lowvol:basis","C54_carver:qa","C57_gtaa:basis")
for label, path in (("main", "catalogus/TRIALS.csv"), ("uitvoerder2-r", "/tmp/claude-0/u2/catalogus/TRIALS.csv")):
    import csv
    rows = list(csv.reader(open(path), delimiter=";")); hdr = rows[0]
    d = pd.DataFrame([r[:len(hdr) - 1] + [";".join(r[len(hdr) - 1:])] for r in rows[1:]], columns=hdr)
    d["p_"] = pd.to_numeric(d["p"], errors="coerce"); d["q_"] = pd.to_numeric(d["FDR_q"], errors="coerce"); d["t_"] = pd.to_numeric(d["t_geclusterd"], errors="coerce")
    m = d[d.p_.notna()].copy()
    m["q_eigen"] = bh(m.p_.values)
    m["p_uit_t"] = norm.sf(m.t_)
    print(f"\n== {label}: {len(d)} rijen, {len(m)} met p (BH-familie m={len(m)}) ==")
    print("max |q_file - q_eigen| =", round((m.q_ - m.q_eigen).abs().max(), 5))
    bad = m[(m.q_ - m.q_eigen).abs() > 5e-4]
    print("rijen met q-afwijking > 0,0005:", len(bad)); print(bad[["regel_id","variant","p_","q_","q_eigen"]].to_string())
    pt = m[m.t_.notna()]; print("max |p - p(t)| =", (pt.p_ - pt.p_uit_t).abs().max())
    print("rijen zonder t maar met p:", m[m.t_.isna()][["regel_id","p_"]].values.tolist())
    primary = d[(d.fase == "ontdekking") & d.p_.notna() & ~d.dataset.str.contains("telt niet")]
    print("primaire trial-rijen (ontdekking, p, niet 'telt niet'):", len(primary))
    names = (m.regel_id + ":" + m.variant).values
    for extra in (0, 100, 414):
        p2 = np.r_[m.p_.values, np.full(extra, 0.5)]; q2 = bh(p2)[:len(m)]
        print(f"  familie +{extra} nulhyp (p=0,5): #q<=0,10 = {(q2<=0.10).sum()} ; " + ", ".join(f"{n.split('_')[0]}{n.split(':')[1][:4]}={q:.3f}" for n, q in zip(names, q2) if n in KEY))
