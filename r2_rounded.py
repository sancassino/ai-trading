"""R2 (D-047 pt 2): C54qa als `future_rounded` bij €80k — hele micro-contracten. Vehikelrapport, GEEN trial. Periode 2015-01→2024-12 (ontdekking; realistisch kapitaal: vaste $90.000 ≈ €80k).
Contractspecs = eigen kennis (ᵉ, onbevestigd): MES 5×, MNQ 2×, micro-DAX €1×, MGC 10 oz, SIL 1.000 oz, MHG 2.500 lb, M6E 12.500 EUR, M6B 6.250 GBP, M6A 10.000 AUD, MCD 10.000 CAD, MSF 12.500 CHF, MJY 1,25 mln JPY;
N225/FTSE/obligatie: geen micro bekend → 0 contracten. Blootstelling_i = k_t·pos_i/N (k_t = min(3, 10%/σ60 van de fractionele sleeve, maandelijks, vertraagd)). Afronding: dichtstbij, herzien alleen bij afwijking ≥ 0,6 contract."""
import math, sys
import numpy as np
from datetime import date
from engine.run_rule import load_daily, net_returns_vehicle, rf_on
import catalogus.C54_carver as m
CAP = 90000.0
QA = [n for n in m.RULE["instrumenten"] if n != "WTI_F"]
SUB8 = ["SPX", "NDX", "GOLD_F", "FX_EURUSD", "FX_USDJPY", "FX_GBPUSD", "FX_AUDUSD", "FX_USDCAD"]
SUB6 = ["SPX", "NDX", "GOLD_F", "FX_EURUSD", "FX_USDJPY", "FX_GBPUSD"]
def cvalue(name, price, d_fx):
    """contractwaarde in USD"""
    if name == "SPX": return 5 * price
    if name == "NDX": return 2 * price
    if name == "DAX": return 1 * price * d_fx["EURUSD"]
    if name == "GOLD_F": return 10 * price
    if name == "SILVER_F": return 1000 * price
    if name == "COPPER_F": return 2500 * price
    if name == "FX_EURUSD": return 12500 * price
    if name == "FX_GBPUSD": return 6250 * price
    if name == "FX_AUDUSD": return 10000 * price
    if name == "FX_USDCAD": return 10000 / price
    if name == "FX_USDCHF": return 12500 / price
    if name == "FX_USDJPY": return 1250000 / price
    return float("inf")
def run(names, start=date(2015, 1, 1), end=date(2024, 12, 31)):
    data = {n: load_daily(n, "adjclose") for n in QA}
    pos = {n: np.clip(m.positions(data[n], {"start_jaar": 1990, "excl": ["WTI_F"]}), -3, 3) for n in QA}
    pos = {n: np.where(np.array([d.year >= 1990 for d in data[n]["date"]]), pos[n], 0.0) for n in QA}
    eur = load_daily("FX_EURUSD", "close"); eurmap = dict(zip(eur["date"], eur["close"]))
    N = len(names)
    # fractionele sleeve (gemiddelde over de gekozen instrumenten, elk 10% vol), overschot
    ex = {}
    for n in names:
        net, *_ = net_returns_vehicle(data[n], pos[n], 1.0, "future", False)
        for d, v in zip(data[n]["date"], net):
            if np.isfinite(v): ex.setdefault(d, []).append(v)
    days_all = sorted(ex); xf = np.array([np.sum(ex[d]) / N for d in days_all])
    # k_t maandelijks
    k = {}; cur = 1.0; prev_m = None
    for i, d in enumerate(days_all):
        if (d.year, d.month) != prev_m and i > 60:
            s = xf[i - 60:i].std() * math.sqrt(252); cur = min(3.0, 0.10 / s) if s > 0 else 1.0
        prev_m = (d.year, d.month); k[d] = cur
    # blootstelling per instrument (fractie van kapitaal), fractioneel en afgerond
    res = {}
    for label in ("frac", "round"):
        tot = {}; zero_days = 0; ndays = 0
        for n in names:
            df = data[n]; exp = np.array([k.get(d, 1.0) * p / N for d, p in zip(df["date"], pos[n])])
            if label == "round":
                cur_c = 0.0; e2 = np.zeros(len(exp))
                for i, d in enumerate(df["date"]):
                    cv = cvalue(n, df["close"][i], {"EURUSD": eurmap.get(d, 1.1)})
                    if not math.isfinite(cv) or cv <= 0: e2[i] = 0.0; continue
                    tgt = exp[i] * CAP / cv
                    if abs(tgt - cur_c) >= 0.6: cur_c = float(round(tgt))
                    e2[i] = cur_c * cv / CAP
                exp = e2
            net, *_ = net_returns_vehicle(df, exp, 1.0, "future", False)
            ok = np.isfinite(net) & np.array([start <= d <= end for d in df["date"]])
            for d, v in zip(df["date"][ok], net[ok]): tot[d] = tot.get(d, 0.0) + v
            if label == "round":
                sel = np.array([start <= d <= end for d in df["date"]]); ndays += 1
                zero_days += float((np.abs(exp[sel]) < 1e-12).mean())
        res[label] = (tot, zero_days / max(1, ndays))
    days = sorted(set(res["frac"][0]) & set(res["round"][0]))
    a = np.array([res["frac"][0][d] for d in days]); b = np.array([res["round"][0][d] for d in days])
    sr = lambda x: x.mean() / x.std() * math.sqrt(252)
    cagr = lambda x: (np.prod(1 + x)) ** (252 / len(x)) - 1
    return dict(n=N, dagen=len(days), SR_frac=sr(a), SR_round=sr(b), vol_frac=a.std() * math.sqrt(252), vol_round=b.std() * math.sqrt(252),
                exc_frac=cagr(a), exc_round=cagr(b), TE=(a - b).std() * math.sqrt(252), zero_share=res["round"][1], corr=float(np.corrcoef(a, b)[0, 1]))
if __name__ == "__main__":
    out = ["# future_rounded — C54qa met hele micro-contracten (D-047 pt 2), 2015–2024, kapitaal $90k ≈ €80k; overschotrendement bij 10%-vol-doel (k ≤ 3); vehikelrapport, geen trial", "",
           "| set | #instr. | SR fractioneel | SR afgerond | vol frac/afg | overschot-CAGR frac/afg | tracking-error | correlatie | gem. aandeel instrument-dagen met 0 contracten |", "|---|---|---|---|---|---|---|---|---|"]
    for lab, nm in (("15 (qa-universum)", QA), ("8 micro-beschikbaar", SUB8), ("6 micro-beschikbaar", SUB6)):
        r = run(nm)
        out.append(f"| {lab} | {r['n']} | {r['SR_frac']:.2f} | {r['SR_round']:.2f} | {r['vol_frac']*100:.1f}% / {r['vol_round']*100:.1f}% | {r['exc_frac']*100:.1f}% / {r['exc_round']*100:.1f}% | {r['TE']*100:.1f}% | {r['corr']:.2f} | {r['zero_share']*100:.0f}% |")
        print(out[-1])
    open("results/R2/future_rounded.md", "w").write("\n".join(out) + "\n")
