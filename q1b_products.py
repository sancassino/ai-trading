"""Q1b: frontier per FTMO-product (2-Step, 2-Step+Scaling, 1-Step) en vereiste Sharpe (PREREG_Q1b.md)."""
import numpy as np

import q1_frontier as q

S, FEE, H, BLOCK, NPATH = 80000.0, 540.0, 504, 21, 20000
SCALES = [0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0]


def simulate(r, d, t, product, seed=11):
    rng = np.random.default_rng(seed)
    n = len(r)
    starts = rng.integers(0, n, size=(NPATH, H // BLOCK + 1))
    idx = (starts[:, :, None] + np.arange(BLOCK)[None, None, :]).reshape(NPATH, -1)[:, :H] % n
    R, D = r[idx] * t, d[idx] * t
    one = product == "1step"
    daily_lim = 0.03 if one else 0.05
    phase = np.ones(NPATH, int)
    eq = np.ones(NPATH); peak = np.ones(NPATH)
    days_in = np.zeros(NPATH, int)
    fees = np.full(NPATH, FEE); cash = np.zeros(NPATH)
    refunded = np.zeros(NPATH, bool)
    pos_sum = np.zeros(NPATH); best_day = np.zeros(NPATH)
    months_funded = np.zeros(NPATH, int); funded_profit = np.zeros(NPATH)
    since_pay = np.zeros(NPATH, int)
    funded_ever = np.zeros(NPATH, bool)
    for day in range(H):
        rr, dd = R[:, day], D[:, day]
        floor = (peak - 0.10) if one else np.full(NPATH, 0.90)
        breach = (dd >= daily_lim) | (eq - dd <= floor)
        prev = eq.copy()
        eq = eq * (1 + rr)
        breach |= eq <= floor
        pnl = eq - prev
        pos_sum += np.where(pnl > 0, pnl, 0); best_day = np.maximum(best_day, pnl)
        days_in += 1
        if one:
            peak = np.maximum(peak, eq)
        # breuk → nieuwe fee, opnieuw
        fees += FEE * breach
        phase[breach] = 1; eq[breach] = 1.0; peak[breach] = 1.0; days_in[breach] = 0; refunded[breach] = False
        pos_sum[breach] = 0; best_day[breach] = 0; since_pay[breach] = 0; months_funded[breach] = 0; funded_profit[breach] = 0
        ok = ~breach
        if one:
            bdr = best_day <= 0.5 * np.maximum(pos_sum, 1e-12)
            passed = ok & (phase == 1) & (eq >= 1.10) & bdr
            to_funded = passed
        else:
            p1 = ok & (phase == 1) & (eq >= 1.10) & (days_in >= 4)
            phase[p1] = 2; eq[p1] = 1.0; days_in[p1] = 0
            to_funded = ok & (phase == 2) & (eq >= 1.05) & (days_in >= 4) & ~p1
        phase[to_funded] = 3; eq[to_funded] = 1.0; peak[to_funded] = 1.0; days_in[to_funded] = 0; since_pay[to_funded] = 0
        funded_ever |= to_funded
        f = ok & (phase == 3) & ~to_funded
        since_pay[f] += 1
        pay = f & (since_pay >= BLOCK) & (eq > 1.0)
        months_funded[f & (since_pay >= BLOCK)] += 1
        split = np.where((product == "scaling") & (months_funded >= 5) & (funded_profit > 0), 0.9, 0.9 if one else 0.8)
        amount = np.where(pay, (eq - 1.0) * S * split, 0.0)
        cash += amount; funded_profit += amount
        if not one:
            ref = pay & ~refunded
            cash += np.where(ref, FEE, 0.0); refunded |= ref
        eq[pay] = 1.0; since_pay[f & (since_pay >= BLOCK)] = 0
        if one:
            peak[pay] = np.maximum(peak[pay], 1.0)
    net = cash - fees
    return net.mean() / 24, (net < 0).mean(), funded_ever.mean()


def best(r, d, product):
    res = [(t,) + simulate(r, d, t, product) for t in SCALES]
    return max(res, key=lambda x: x[1])


def main():
    rA, dA = q.load("results/f/F3b_comb_daily.csv")
    z = (rA - rA.mean()) / rA.std()
    sigma = 0.10 / np.sqrt(252)
    series = {"A historisch": (rA, dA)}
    for sr in (1, 1.5, 2, 3, 4):
        series[f"synthetisch SR {sr}"] = (sr * 0.10 / 252 + sigma * z, dA * sigma / rA.std())
    products = ["2step", "scaling", "1step"]
    table = {}
    print(f"{'reeks':<22}" + "".join(f"{p:>30}" for p in products))
    for name, (r, d) in series.items():
        row = []
        for p in products:
            t, net, ploss, fund = best(r, d, p)
            table[(name, p)] = net
            row.append(f"€{net:>6,.0f} (t {t:.2f}, P<0 {ploss*100:>3.0f}%, f {fund*100:>3.0f}%)")
        print(f"{name:<22}" + "".join(f"{x:>30}" for x in row))
    print("\nVereiste SR (lineaire interpolatie tussen de synthetische punten):")
    srs = [1, 1.5, 2, 3, 4]
    for p in products:
        vals = [table[(f"synthetisch SR {s}", p)] for s in srs]
        out = []
        for target in (500, 900):
            req = None
            for (s0, v0), (s1, v1) in zip(zip(srs, vals), zip(srs[1:], vals[1:])):
                if v0 < target <= v1:
                    req = s0 + (target - v0) / (v1 - v0) * (s1 - s0); break
            out.append(f"€{target}: SR ≈ {req:.1f}" if req else f"€{target}: > SR 4 of < SR 1")
        print(f"  {p:<8} " + " | ".join(out))


if __name__ == "__main__":
    main()
