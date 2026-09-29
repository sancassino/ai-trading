"""G1 (kostengevoeligheid) + G2 (beta/stresscorrelatie) op de F3b-combinatie, volgens PREREG_G1G2.md."""
import csv, statistics
from collections import defaultdict
from datetime import datetime
import stats_tools as st
import e1_rsi2_ftmo as e1

S, T = 80000.0, 0.45
RSI_F, ORB_F = 1.3865 * T, 0.9635 * T          # factoren t.o.v. F1 (1/6) en F2 (1/7)
SLIP_PT = {"XAUUSD": 0.10, "EURUSD": 0.0001}     # overige: 1 indexpunt

def median_m5_spread(sym):
    pt, v = None, []
    for line in open(f"data/m5/{sym}.csv"):
        if line.startswith("#"): pt = float(line.split("point=")[1].split(";")[0]); continue
        if line[0].isdigit():
            p = line.rstrip().split(";"); v.append(int(p[5]) * pt / float(p[4]))
    v.sort(); return v[len(v) // 2]

def rd(p): return {r["date"]: r for r in csv.DictReader(open(p), delimiter=";") if r["date"] >= "2021.09.14"}

def base():
    a, b = rd("results/f/F1_RSI2_swapcorr_daily.csv"), rd("results/f/F2_ORB_daily.csv")
    days = sorted(set(a) & set(b))
    return days, {d: (float(a[d]["end_equity"]) - S, float(b[d]["end_equity"]) - S, float(a[d]["start_balance"]) - S,
                      float(b[d]["start_balance"]) - S, float(a[d]["min_equity"]) - S, float(b[d]["min_equity"]) - S) for d in days}

def extra_costs(slip):
    """extra kosten in € per dag (op F1/F2-basisschaal), cumulatief geboekt op sluitdatum"""
    cost = defaultdict(float)
    for r in csv.DictReader(open("results/f/F1_RSI2.csv", encoding="utf-8-sig"), delimiter=";"):
        if not r.get("close_time"): continue
        sym = r["symbol"].replace(".cash", "cash")
        notional = S / 6  # benadering: 1/6 van de startequity
        cost[r["close_time"][:10]] += 0.5 * e1.eod_spread_frac(sym) * 2 * notional
    sp = {}
    for r in csv.DictReader(open("results/f/F2_ORB.csv", encoding="utf-8-sig"), delimiter=";"):
        if not r.get("close_time"): continue
        sym = r["symbol"].replace(".cash", "cash")
        if sym not in sp: sp[sym] = median_m5_spread(sym)
        pin = float(r["price_in"]); notional = S / 7
        extra = 0.5 * sp[sym] * notional
        if slip: extra += SLIP_PT.get(sym, 1.0) / pin * notional
        cost[r["close_time"][:10]] += extra * (ORB_F / RSI_F)  # ORB-kosten later met ORB_F, hier genormaliseerd
    return cost

def evaluate(label, extra=None):
    days, v = base()
    cum, eq_prev = 0.0, S
    rets, worst, peak, dd, eqs = [], 0.0, S, 0.0, []
    for d in days:
        ra, rb, ba, bb, ma, mb = v[d]
        cost_today = RSI_F * extra.get(d, 0.0) if extra else 0.0
        bal = S + RSI_F * ba + ORB_F * bb - cum
        mn = S + RSI_F * ma + ORB_F * mb - cum - cost_today
        cum += cost_today
        eq = S + RSI_F * ra + ORB_F * rb - cum
        worst = max(worst, (bal - mn) / S); dd = max(dd, (peak - mn) / peak); peak = max(peak, eq)
        rets.append(eq / eq_prev - 1); eq_prev = eq; eqs.append((d, eq))
    yrs = len(rets) / 252; cagr = (eqs[-1][1] / S) ** (1 / yrs) - 1
    print(f"{label:<44} SR {st.sharpe(rets)[0]:.2f} | €/mnd {cagr*S/12:,.0f} | dag-DD {dd*100:.1f}% | slechtste dag {worst*100:.2f}%")
    return dict(zip([d for d, _ in eqs], rets))

print("G1 kostengevoeligheid (F3b-schaal):")
basis = evaluate("basis (MT5, F3b)")
evaluate("+50% spread", extra_costs(False))
evaluate("+50% spread + 1 punt slippage/ORB-trade", extra_costs(True))
print("\nG2 correlatie met US500 (FTMO-D1):")
us = {r["date"]: float(r["close"]) for r in csv.DictReader(open("US500cash_rates.csv"), delimiter=";")}
ks = sorted(k for k in basis if k in us)
us_r = {}
for i in range(1, len(ks)): us_r[ks[i]] = us[ks[i]] / us[ks[i - 1]] - 1
ks = [k for k in ks if k in us_r]
def cb(sub):
    x = [basis[k] for k in sub]; y = [us_r[k] for k in sub]
    c = statistics.correlation(x, y); beta = statistics.covariance(x, y) / statistics.variance(y)
    return c, beta
for lbl, lo, hi in (("volledig", "2021.09.14", "2026.12.31"), ("stress 2022-01..10", "2022.01.01", "2022.10.31"), ("stress 2025-03..04", "2025.03.01", "2025.04.30")):
    c, b = cb([k for k in ks if lo <= k <= hi])
    print(f"  {lbl:<20} corr {c:+.2f} | beta {b:+.3f}")
roll = [cb(ks[i - 63:i])[0] for i in range(63, len(ks))]
print(f"  rollende 63d-correlatie: min {min(roll):+.2f}, mediaan {statistics.median(roll):+.2f}, max {max(roll):+.2f}")
