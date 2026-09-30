"""Q7 (geen trial): verhoogt ORB + RSI(2) samen de FTMO-uitkomst t.o.v. ORB alleen? Q1b-mechaniek, onder aanname fee €540/€80k.
Reeksen: MT5 F2 (ORB, 1/7 per trade) en F1 RSI(2) swap-gecorrigeerd; beide genormaliseerd op gelijke jaarvol; mix = aandeel RSI(2)
in het volatiliteitsbudget; dip = gewogen som van de dagdips (conservatief: dips vallen samen)."""
import csv
import numpy as np
import q1b_products as qb

S = 80000.0


def load(path):
    out, prev = {}, S
    for x in csv.DictReader(open(path), delimiter=";"):
        sb, mn, en = (float(x[k]) for k in ("start_balance", "min_equity", "end_equity"))
        out[x["date"]] = (en / prev - 1, max(0.0, (sb - mn) / S)); prev = en
    return out


orb, rsi = load("results/f/F2_ORB_daily.csv"), load("results/f/F1_RSI2_swapcorr_daily.csv")
days = sorted(set(orb) & set(rsi))
rO = np.array([orb[d][0] for d in days]); dO = np.array([orb[d][1] for d in days])
rR = np.array([rsi[d][0] for d in days]); dR = np.array([rsi[d][1] for d in days])
kR = rO.std() / rR.std()          # RSI(2) op dezelfde vol als ORB
rR, dR = rR * kR, dR * kR
sr = lambda r: r.mean() / r.std() * np.sqrt(252)
sk = lambda r: float((((r - r.mean()) / r.std()) ** 3).mean())
print(f"{len(days)} gemeenschappelijke dagen ({days[0]} … {days[-1]}) | ORB SR {sr(rO):.2f} skew {sk(rO):+.2f} | RSI(2) SR {sr(rR):.2f} skew {sk(rR):+.2f} | corr {np.corrcoef(rO, rR)[0,1]:+.2f}")
qb.SCALES = [1, 2, 3, 4, 5, 6, 8, 10]
for label, drift in (("historisch", 1.0), ("ORB-drift −50%", 0.5), ("ORB-drift 0", 0.0)):
    ro = rO - (1 - drift) * rO.mean()
    print(f"\n{label}:")
    for m in (0.0, 0.25, 0.5, 0.75, 1.0):
        r = (1 - m) * ro + m * rR; d = (1 - m) * dO + m * dR
        for p in ("2step",):
            t, net, pl, fu = qb.best(r, d, p)
            print(f"  RSI(2)-aandeel {m:.2f}: SR {sr(r):+.2f} skew {sk(r):+.2f} max dip {d.max()*t*100:.1f}% | beste schaal {t}× → €{net:,.0f}/mnd, P(netto<0) {pl*100:.0f}%, funded {fu*100:.0f}%", flush=True)
