"""S1: noise-area intraday-momentum (Zarattini–Aziz–Barbon 2024) op US500/US100/US30/GER40, volgens PREREG_S1.md."""
import math
from collections import defaultdict
from datetime import datetime, timedelta

import numpy as np

from b4_sim import NY, SYMS as SESS_SPEC, sessions

SYMS = ["US500cash", "US100cash", "US30cash", "GER40cash"]
VARIANTS = {"a": (30, True, 14), "b": (60, True, 14), "c": (30, False, 14), "d": (30, True, 28)}


def tick_volume(sym):
    out = {}
    for line in open(f"data/m5_vol/{sym}.csv"):
        if line[0].isdigit():
            t, v = line.rstrip().split(";")
            out[datetime.strptime(t, "%Y.%m.%d %H:%M")] = int(v)
    return out


def prepare(sym):
    tv = tick_volume(sym)
    out = []
    for d, s in sessions(sym):
        o = np.array([b[1] for b in s]); h = np.array([b[2] for b in s]); l = np.array([b[3] for b in s])
        c = np.array([b[4] for b in s]); sp = np.array([b[5] for b in s])
        server = [b[0].astimezone(NY).replace(tzinfo=None) + timedelta(hours=7) for b in s]
        v = np.array([tv.get(t, 0) for t in server], float)
        tp = (h + l + c) / 3
        cv = np.cumsum(v)
        vwap = np.where(cv > 0, np.cumsum(tp * v) / np.maximum(cv, 1), np.nan)
        out.append({"d": d, "o": o[0], "c": c, "sp": sp, "vwap": vwap, "move": np.abs(c / o[0] - 1)})
    return out


def run(days, step, use_vwap, win, spread_mult=1.0):
    """geeft trades (datum, bruto, kosten) en dag-P&L per sessie (als fractie van notional, 1× hefboom) + dagdip."""
    trades, daily = [], {}
    n_bars = len(days[0]["c"])
    for t in range(max(win, 14) + 1, len(days)):
        cur = days[t]
        prev = days[t - win:t]
        if any(len(p["c"]) != len(cur["c"]) for p in prev) or len(days[t - 1]["c"]) == 0:
            continue
        sigma = np.mean([p["move"] for p in prev], axis=0)
        base_hi = max(cur["o"], days[t - 1]["c"][-1]); base_lo = min(cur["o"], days[t - 1]["c"][-1])
        UB = base_hi * (1 + sigma); LB = base_lo * (1 - sigma)
        k_step = step // 5
        checks = list(range(k_step - 1, len(cur["c"]) - 1, k_step))  # bar k sluit om open + 5(k+1) min
        pos, ep, ek = 0, None, None
        pnl, path = 0.0, [0.0]
        def close(k):
            nonlocal pos, pnl
            px = cur["c"][k]
            gross = pos * (px / ep - 1)
            cost = spread_mult * (cur["sp"][ek] if pos > 0 else cur["sp"][k]) / ep
            trades.append((cur["d"], gross, cost)); pnl += gross - cost; path.append(pnl); pos = 0
        for k in checks:
            px = cur["c"][k]
            if pos > 0:
                stop = max(UB[k], cur["vwap"][k]) if use_vwap and np.isfinite(cur["vwap"][k]) else UB[k]
                if px < stop:
                    close(k)
            elif pos < 0:
                stop = min(LB[k], cur["vwap"][k]) if use_vwap and np.isfinite(cur["vwap"][k]) else LB[k]
                if px > stop:
                    close(k)
            if pos == 0:
                if px > UB[k]:
                    pos, ep, ek = 1, px, k
                elif px < LB[k]:
                    pos, ep, ek = -1, px, k
            if pos:  # tussentijdse mark-to-market op de beslismomenten
                path.append(pnl + pos * (px / ep - 1))
        if pos:
            close(len(cur["c"]) - 1)
        daily[cur["d"]] = (pnl, -min(path))
    return trades, daily


def tstat(x):
    x = np.asarray(x)
    return x.mean() / x.std(ddof=1) * math.sqrt(len(x)) if len(x) > 2 else float("nan")


def orb_daily():
    r = {}
    prev = None
    for line in open("results/f/F2_ORB_daily.csv"):
        if not line[0].isdigit():
            continue
        f = line.strip().split(";")
        d = datetime.strptime(f[0], "%Y.%m.%d").date(); eq = float(f[4])
        if prev:
            r[d] = eq / prev - 1
        prev = eq
    return r


def main():
    data = {s: prepare(s) for s in SYMS}
    # dagvol per symbool voor de paper-sizing (slot-op-slot, 14 dagen)
    lev = {}
    for s, days in data.items():
        cl = np.array([d["c"][-1] for d in days]); r = np.r_[np.nan, cl[1:] / cl[:-1] - 1]
        for i, d in enumerate(days):
            sd = np.nanstd(r[max(1, i - 14):i], ddof=1) if i > 3 else np.nan
            lev[(s, d["d"])] = min(4.0, 0.02 / sd) / 4 if sd and np.isfinite(sd) and sd > 0 else 0.0
    orb = orb_daily()
    for name, (step, vw, win) in VARIANTS.items():
        res = {s: run(days, step, vw, win) for s, days in data.items()}
        tr = [(s, d, g, c) for s, (t, _) in res.items() for d, g, c in t]
        train = [x for x in tr if x[1].year <= 2023]
        g_tr = np.mean([x[2] for x in train]) * 1e4; c_tr = np.mean([x[3] for x in train]) * 1e4
        gate = g_tr >= 3 * c_tr
        print(f"\nVariant ({name}) stap {step} min, VWAP {'ja' if vw else 'nee'}, σ {win} d: N {len(tr)} | poort train: bruto {g_tr:+.2f} bp vs 3× kosten {3*c_tr:.2f} bp → {'DOOR' if gate else 'STOP (geen trial)'}", flush=True)
        net = lambda xs, m=1.0: np.array([x[2] - m * x[3] for x in xs])
        test = [x for x in tr if x[1].year >= 2024]; oos = [x for x in tr if x[1] >= datetime(2025, 1, 1).date()]
        yrs = defaultdict(list)
        for x in tr:
            yrs[x[1].year].append(x[2] - x[3])
        # +50% spread
        res50 = {s: run(days, step, vw, win, 1.5) for s, days in data.items()}
        test50 = [g - c for s, (t, _) in res50.items() for d, g, c in t if d.year >= 2024]
        # dagreeks (paper-sizing)
        dd = defaultdict(float); dip = defaultdict(float)
        for s, (_, daily) in res.items():
            for d, (p, dp) in daily.items():
                dd[d] += lev[(s, d)] * p; dip[d] += lev[(s, d)] * dp
        days = sorted(dd); r = np.array([dd[d] for d in days])
        sr = r.mean() / r.std() * math.sqrt(252); sk = float((((r - r.mean()) / r.std()) ** 3).mean())
        common = [d for d in days if d in orb]
        corr = np.corrcoef([dd[d] for d in common], [orb[d] for d in common])[0, 1]
        pos_y = sum(np.mean(v) > 0 for v in yrs.values())
        t_tr, t_te, t50 = tstat(net(train)), tstat(net(test)), tstat(test50)
        print(f"   netto bp/trade: train {net(train).mean()*1e4:+.2f} (t {t_tr:+.2f}, N {len(train)}) | test {net(test).mean()*1e4:+.2f} (t {t_te:+.2f}, N {len(test)}) | "
              f"OOS 2025-01…2026-09 {net(oos).mean()*1e4:+.2f} (t {tstat(net(oos)):+.2f}, N {len(oos)}) | +50% spread test t {t50:+.2f}")
        print("   per jaar: " + " ".join(f"{y}:{np.mean(v)*1e4:+.1f}({len(v)})" for y, v in sorted(yrs.items())) + f" → {pos_y}/6 positief")
        print("   per symbool (netto bp / t): " + " ".join(f"{s}:{net(t_ := [(s, d, g, c) for d, g, c in res[s][0]]).mean()*1e4:+.1f}/{tstat(net(t_)):+.1f}" for s in SYMS))
        print(f"   dagreeks (paper-sizing/4): SR {sr:+.2f} | skew {sk:+.2f} | jaarvol {r.std()*math.sqrt(252)*100:.1f}% | max dagdip {max(dip.values())*100:.2f}% | corr met ORB {corr:+.2f}")
        ok = gate and t_tr >= 3.5 and t_te >= 3.5 and len(tr) >= 500 and pos_y >= 4 and t50 >= 2 and net(oos).mean() > 0
        print(f"   → {'GESLAAGD' if ok else 'AFGEWEZEN'}" + ("" if gate else " (poort)"), flush=True)


if __name__ == "__main__":
    main()
