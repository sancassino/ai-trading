"""R2 (D-056): P-ETF-a met échte obligatiefondsen (IEF/TLT vanaf 2002/03) vs synthetische obligatie (D=8,C=80); SR alleen op excess; per periode. Aanvulling op results/port/QA_PETF_decompositie.md (Uitvoerder-1). Geen trial."""
import importlib, math
import numpy as np
from datetime import date
from engine.forward import series
import forward_portfolio as FP
DISC = date(2024, 12, 31)
mod = importlib.import_module("catalogus.C52_allweather"); R = mod.RULE
R["instrumenten"] = list(dict.fromkeys(R["instrumenten"] + ["TLT", "IEF", "BOND10_SYN", "GOLD_F", "SPY"]))
for nm, bond in (("syn", "BOND10_SYN"), ("ief", "IEF"), ("tlt", "TLT")):
    R["varianten"]["d_" + nm] = {"assets": ["SPY", bond, "GOLD_F"], "start_jaar": 2003}
S = {nm: series("C52_allweather", "d_" + nm, "etf", end=DISC) for nm in ("syn", "ief", "tlt")}
S["C02"] = series("C02_faber", "basis", "etf", end=DISC)
out = ["# R2 — decompositie P-ETF-a: obligatiebron (D-056; ontdekking ≤ 2024; SR op excess; geen trial)", "",
       "C52 = SPY + obligatie + GOLD_F (∝ 1/σ60, vol-target 8%, geen hefboom, etf-kosten 13 bp/TER 0,07%), sample 2003→ zodat IEF/TLT overal beschikbaar zijn; P-ETF-a = C52 + C02, gewogen ∝ 1/σ (PREREG_PORT).", "",
       "| obligatiebron | C52 SR | C52 CAGR tot. | C52 maxDD | P-ETF-a SR | P-ETF-a CAGR tot. | P-ETF-a maxDD | P-ETF-a 2022 |", "|---|---|---|---|---|---|---|---|"]
for nm, lab in (("syn", "synthetisch (D=8, C=80)"), ("ief", "IEF (echt fonds, 7–10j)"), ("tlt", "TLT (echt fonds, 20j+)")):
    s = S[nm]; days = sorted(s); ex = np.array([s[d][0] for d in days]); tot = np.array([s[d][1] for d in days]); eq = np.cumprod(1 + tot)
    dd = float(np.max(1 - eq / np.maximum.accumulate(eq))); c = eq[-1] ** (252 / len(tot)) - 1
    Sx = {"a": s, "C02": S["C02"]}; d2, o = FP.run_petf(Sx, ["a", "C02"]); t2, x2, _ = o["P-ETF-a"]; ok = np.isfinite(x2); dd2 = [d for d, k in zip(d2, ok) if k]
    st = FP.stats(d2, t2, x2, lo=dd2[0]); r22 = float(np.prod([1 + v for d, v in zip(d2, t2) if d.year == 2022 and np.isfinite(v)]) - 1)
    out.append(f"| {lab} | {ex.mean()/ex.std()*math.sqrt(252):.2f} | {c*100:.1f}% | {dd*100:.1f}% | {st['SR']:.2f} | {st['CAGR']*100:.1f}% | {st['maxDD']*100:.1f}% | {r22*100:+.1f}% |")
out += ["", "Lezing: zie RUNLOG_R2 (D-056). Uitsplitsing per activum, per decennium, 'zonder obligatiepoot' en C02 zonder SPX_TR staan in `results/port/QA_PETF_decompositie.md`."]
open("results/R2/decompositie.md", "w").write("\n".join(out) + "\n"); print("\n".join(out))
