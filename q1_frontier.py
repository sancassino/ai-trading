"""Q1: inkomens-frontier onder FTMO-regels (PREREG_Q1.md). Gevectoriseerd over paden met numpy.
Gebruik: .venv/bin/python q1_frontier.py"""
import csv

import numpy as np

S, FEE, SPLIT = 80000.0, 540.0, 0.8
H, BLOCK, NPATH = 504, 21, 20000
SCALES = [0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0]


def load(path, base_scale=1.0):
    rows = [r for r in csv.DictReader(open(path), delimiter=";")]
    r, d, prev = [], [], S
    for x in rows:
        sb, mn, en = (S + base_scale * (float(x[k]) - S) for k in ("start_balance", "min_equity", "end_equity"))
        r.append(en / prev - 1); d.append(max(0.0, (sb - mn) / S)); prev = en
    return np.array(r), np.array(d)


def simulate(r, d, t, seed=11):
    rng = np.random.default_rng(seed)
    n = len(r)
    starts = rng.integers(0, n, size=(NPATH, H // BLOCK + 1))
    idx = (starts[:, :, None] + np.arange(BLOCK)[None, None, :]).reshape(NPATH, -1)[:, :H] % n
    R, D = r[idx] * t, d[idx] * t
    phase = np.ones(NPATH, int)          # 1, 2, 3 = funded
    eq = np.ones(NPATH)                  # als fractie van startkapitaal
    days_in = np.zeros(NPATH, int)
    fees = np.full(NPATH, FEE)
    cash = np.zeros(NPATH)
    refunded = np.zeros(NPATH, bool)     # fee al terug voor dit funded account
    attempts = np.ones(NPATH)
    funded_ever = np.zeros(NPATH, bool)
    funded_day = np.full(NPATH, -1)
    breach_12m = np.zeros(NPATH, bool)
    first_pay = np.full(NPATH, -1)
    since_pay = np.zeros(NPATH, int)
    for day in range(H):
        rr, dd = R[:, day], D[:, day]
        breach = (dd >= 0.05) | (eq - dd <= 0.90)
        eq = eq * (1 + rr)
        breach |= eq <= 0.90
        days_in += 1
        # breuk → nieuwe fee, opnieuw fase 1
        was_funded = phase == 3
        breach_12m |= breach & was_funded & (funded_day >= 0) & (day - funded_day <= 252)
        restart = breach
        fees += FEE * restart; attempts += restart
        phase[restart] = 1; eq[restart] = 1.0; days_in[restart] = 0; refunded[restart] = False; since_pay[restart] = 0
        # fase-overgangen
        p1 = (phase == 1) & (eq >= 1.10) & (days_in >= 4) & ~restart
        phase[p1] = 2; eq[p1] = 1.0; days_in[p1] = 0
        p2 = (phase == 2) & (eq >= 1.05) & (days_in >= 4) & ~restart & ~p1
        phase[p2] = 3; eq[p2] = 1.0; days_in[p2] = 0; since_pay[p2] = 0
        newly = p2 & ~funded_ever
        funded_ever |= p2; funded_day[newly] = day
        # uitbetaling in funded (≥ 14 dagen, maandelijks)
        f = (phase == 3) & ~p2 & ~restart
        since_pay[f] += 1
        pay = f & (since_pay >= BLOCK) & (eq > 1.0)
        amount = (eq - 1.0) * S * SPLIT
        cash += np.where(pay, amount, 0.0)
        ref = pay & ~refunded
        cash += np.where(ref, FEE, 0.0); refunded |= ref
        first_pay[(first_pay < 0) & pay] = day
        eq[pay] = 1.0; since_pay[pay] = 0
    net = cash - fees
    fp = first_pay[first_pay >= 0]
    return {
        "funded": funded_ever.mean(),
        "breach12": breach_12m[funded_ever].mean() if funded_ever.any() else float("nan"),
        "net_month": net.mean() / 24,
        "net_month_med": np.median(net) / 24,
        "first_pay_months": np.median(fp) / 21 if len(fp) else float("nan"),
        "attempts": attempts.mean(),
        "p_loss": (net < 0).mean(),
    }


def main():
    series = {"A F3b (RSI(2)+ORB)": load("results/f/F3b_comb_daily.csv"),
              "B RSI(2) oorspr. (1/6)": load("results/f/F1_RSI2_swapcorr_daily.csv")}
    for name, (r, d) in series.items():
        m = r.mean()
        for vlabel, rv in (("historisch", r), ("−50% drift", r - 0.5 * m), ("nul-drift", r - m)):
            print(f"\n== {name} — {vlabel} (gem. dagrendement {rv.mean()*1e4:+.2f} bp, max dagverlies {d.max()*100:.2f}% bij t=1)")
            print(f"  {'t':>5}{'funded':>8}{'breuk12':>9}{'netto €/mnd':>12}{'mediaan':>9}{'1e uitb. mnd':>13}{'pogingen':>9}{'P(netto<0)':>11}")
            for t in SCALES:
                o = simulate(rv, d, t)
                print(f"  {t:>5.2f}{o['funded']*100:>7.1f}%{o['breach12']*100:>8.1f}%{o['net_month']:>12,.0f}{o['net_month_med']:>9,.0f}"
                      f"{o['first_pay_months']:>13.1f}{o['attempts']:>9.2f}{o['p_loss']*100:>10.1f}%")


if __name__ == "__main__":
    main()
