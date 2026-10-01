"""Forward-papier P1 ORB+BTC (PREREG_FTMO_P1_ORB_BTC.md stap 3; D-095). Bevroren regels, geen wijziging:
- Been A (ORB): b4_sim.run_orb (F2/B4a) op US500cash, US100cash, GER40cash; kosten zoals b4_sim (spread instap/uitstap + commissie).
- Been B (BTC): PREREG_S2_BTC_USOPEN, logica regel-voor-regel overgenomen uit scripts/s2_btc_cost_gate_train.py (CTO, grok/cto-1).
Per dag (≥ FORWARD_START): netto rendement per ORB-symbool (fractie, 1× notional), ORB-been = gemiddelde over de 3 indices (gelijke notional),
BTC-been netto (fractie, 1× notional). Gecombineerde reeks = sA·A + sB·B zodra de CTO de train-bevroren schaalconstanten vastlegt in
results/cto/p1_scales.json ({"sA":…, "sB":…}); tot dan 'n.v.t.'. Append-only naar forward/p1_daily.csv; data = data/m5 (dagelijks aangevuld)."""
import json
import os
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import b4_sim

FORWARD_START = date(2026, 10, 1)
OUT = "forward/p1_daily.csv"
NY = ZoneInfo("America/New_York"); CET = ZoneInfo("Europe/Amsterdam")
ORB_SYMS = ["US500cash", "US100cash", "GER40cash"]                     # PREREG-tekst been A
ORB7 = ["US500cash", "US100cash", "US30cash", "XAUUSD", "GER40cash", "UK100cash", "EURUSD"]   # F2-equivalent (CTO orb_unit = F2, 7 symbolen × 1/7)
RANGE_MIN, RANGE_MAX, GAP_MIN, COMM_BP_SIDE = 0.0020, 0.0150, 0.0015, 0.20


def orb_leg(syms=None):
    out = defaultdict(dict)
    for s in (syms or ORB_SYMS):
        for d, net, _ in b4_sim.run_orb(b4_sim.sessions(s), b4_sim.SYMS[s][3]):
            if d >= FORWARD_START:
                out[d][s] = net
    return out


def load_cet(sym):
    bars = []
    for t, o, h, l, c, sp in b4_sim.load(sym):
        loc = (t - timedelta(hours=7)).replace(tzinfo=NY).astimezone(CET)
        bars.append({"local": loc, "o": o, "h": h, "l": l, "c": c, "spread": sp})
    return bars


def us100_cash_gap(by_us, d):
    priors = sorted(x for x in by_us if x < d)
    if not priors:
        return None
    prev_bars = sorted(by_us[priors[-1]], key=lambda b: b["local"])
    cc = [b for b in prev_bars if b["local"].hour < 22]
    if not cc:
        return None
    prev_close = cc[-1]["c"]
    ob = [b for b in sorted(by_us[d], key=lambda b: b["local"]) if (b["local"].hour == 15 and b["local"].minute >= 30) or b["local"].hour > 15]
    if not ob or prev_close <= 0:
        return None
    return ob[0]["o"] / prev_close - 1.0


def btc_leg():
    by_btc, by_us = defaultdict(list), defaultdict(list)
    for b in load_cet("BTCUSD"):
        by_btc[b["local"].date()].append(b)
    for b in load_cet("US100cash"):
        by_us[b["local"].date()].append(b)
    res = {}
    for d in sorted(by_btc):
        if d < FORWARD_START or d not in by_us:
            continue
        gap = us100_cash_gap(by_us, d)
        if gap is None or abs(gap) < GAP_MIN:
            res[d] = None; continue
        day = sorted(by_btc[d], key=lambda x: x["local"])
        pre = [b for b in day if (b["local"].hour == 14 and b["local"].minute >= 30) or (b["local"].hour == 15 and b["local"].minute < 30)]
        entry_win = [b for b in day if b["local"].hour == 15 and b["local"].minute >= 30]
        post = [b for b in day if (b["local"].hour > 15 or (b["local"].hour == 15 and b["local"].minute >= 30))
                and (b["local"].hour < 21 or (b["local"].hour == 21 and b["local"].minute == 0))]
        if len(pre) < 10 or not entry_win:
            res[d] = None; continue
        rh, rl = max(b["h"] for b in pre), min(b["l"] for b in pre); mid = 0.5 * (rh + rl)
        if mid <= 0 or rh <= rl or not (RANGE_MIN <= (rh - rl) / mid <= RANGE_MAX):
            res[d] = None; continue
        trade = None; up_hit = dn_hit = False
        for b in entry_win:
            up, dn = b["c"] >= rh, b["c"] <= rl
            up_hit |= up; dn_hit |= dn
            if up_hit and dn_hit:
                trade = None; break
            if not (up or dn):
                continue
            side = 1 if up else -1
            if side * gap <= 0:
                break
            entry, stop = b["c"], mid
            seq = [x for x in post if x["local"] >= b["local"]]
            if not seq:
                break
            exit_p = None
            for i, eb in enumerate(seq):
                if i == 0:
                    continue
                if (side > 0 and eb["l"] <= stop) or (side < 0 and eb["h"] >= stop):
                    exit_p = stop; break
            if exit_p is None:
                fl = [x for x in seq if x["local"].hour == 21 and x["local"].minute == 0]
                exit_p = (fl[0] if fl else seq[-1])["c"]
            gross = side * (exit_p - entry) / entry
            trade = gross - (b["spread"] / entry + 2 * COMM_BP_SIDE * 1e-4)
            break
        res[d] = trade
    return res


def main():
    scales = json.load(open("results/cto/p1_scales.json")) if os.path.exists("results/cto/p1_scales.json") else None
    A, B, A7 = orb_leg(), btc_leg(), orb_leg(ORB7)
    days = sorted(set(A) | set(B) | set(A7))
    logged = set()
    if os.path.exists(OUT):
        logged = {l.split(";")[0] for l in open(OUT) if l[:1].isdigit()}
    else:
        with open(OUT, "w") as f:
            f.write("date;orb_US500;orb_US100;orb_GER40;orb_leg;btc_leg;orb7_unit;combined_cto;berekend_utc\n")
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    today = datetime.now(timezone.utc).date()
    new = []
    for d in days:
        if d.isoformat() in logged or d >= today:          # lopende dag niet loggen
            continue
        o = A.get(d, {}); orb = sum(o.values()) / len(ORB_SYMS)
        b = B.get(d); bnet = b if b is not None else 0.0
        orb7 = sum(A7.get(d, {}).values()) / len(ORB7)                    # F2-proxy (B4a-simulator, 7 symbolen × 1/7)
        comb = f"{scales['sA'] * orb7 + scales['sB'] * bnet:.8f}" if scales else "n.v.t."   # sA/sB zijn geijkt op orb_unit = F2
        fmt = lambda x: f"{x:.8f}" if x is not None else ""
        new.append(f"{d};{fmt(o.get('US500cash'))};{fmt(o.get('US100cash'))};{fmt(o.get('GER40cash'))};{orb:.8f};{fmt(b)};{orb7:.8f};{comb};{ts}")
    if new:
        with open(OUT, "a") as f:
            f.write("\n".join(new) + "\n")
    print(f"forward_p1: {len(new)} nieuwe dag(en); schaalconstanten {'aanwezig' if scales else 'nog niet (CTO)'}")


if __name__ == "__main__":
    main()
