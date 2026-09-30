"""Papieren forward-test van de F3b-kandidaat (RSI(2) + ORB), zonder handelsaccount (NEXT_STEPS v5, I1).

Dagelijks via cron (22:15 UTC, ma–vr): haalt recente FTMO-data op van de MT5-VM (mt5_export_recent.py), verwerkt elke
nieuwe, afgesloten serverdag D (vanaf START_DAY, geen terugwerkende kracht) met exact de F3b-regels en logt naar
forward/paper_daily.csv + forward/paper_trades.csv; commit + push (git-tijdstempel = bewijs dat het vooraf was).

Regels (ongewijzigd t.o.v. F3b): RSI(2) E1-regel op FTMO-D1-slot (drempel 10, SMA200, uitstap > 70), notional per positie
= equity × 0,62/6, eind-van-dag-spread per kant, FTMO-longswap per kalendernacht; ORB B4a (30 min, stop andere kant,
sessie-einde) op 7 symbolen, notional per trade = equity × 0,43/7, spread per bar + commissie.
Benaderingen: slot-tot-slot (geen intraday-dip voor RSI), geen EUR-conversie van USD-P&L.
"""
import csv
import json
import os
import subprocess
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import b4_sim
from b2_sim import rsi2
from e1_rsi2_ftmo import SWAP_LONG

START_DAY = date.fromisoformat(os.environ.get("FWD_TEST_START", "2026-09-30"))
EQUITY0 = 80000.0
RSI_FRAC, ORB_FRAC = 0.62 / 6, 0.43 / 7
RSI_SYMS = ["US500cash", "US100cash", "US30cash", "GER40cash", "UK100cash", "XAUUSD"]
ORB_SYMS = list(b4_sim.SYMS)          # 7 symbolen uit B4
VM, KEY = "sandro_cassino@34.69.153.107", os.path.expanduser("~/mt5_vm_key")
DIR = os.path.dirname(os.path.abspath(__file__))
FWD = os.environ.get("FWD_TEST_DIR", os.path.join(DIR, "forward"))
STATE = os.path.join(FWD, "state.json")
NY = ZoneInfo("America/New_York")


def mt5_name(s):
    return s.replace("cash", ".cash")


def fetch():
    cmd = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=30", "-i", KEY, VM,
           "python C:\\Users\\sandro_cassino\\mt5_export_recent.py "
           + ",".join(mt5_name(s) for s in ORB_SYMS) + " " + ",".join(mt5_name(s) for s in RSI_SYMS)]
    for attempt in range(3):
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=600).stdout
            if "D1;" in out:
                break
        except subprocess.TimeoutExpired:
            out = ""
        import time
        time.sleep(120)  # VM bezet (bv. tester-run) → later opnieuw
    m5, d1, point = defaultdict(list), defaultdict(list), {}
    for line in out.splitlines():
        p = line.strip().split(";")
        if p[0] == "M5" and len(p) == 8:
            m5[p[1].replace(".cash", "cash")].append((datetime.strptime(p[2], "%Y.%m.%d %H:%M"), *map(float, p[3:7]), int(p[7])))
        elif p[0] == "D1" and len(p) == 4:
            d1[p[1].replace(".cash", "cash")].append((datetime.strptime(p[2], "%Y.%m.%d").date(), float(p[3])))
    for s in ORB_SYMS:  # point uit de lokale M5-exportheader (vast per symbool)
        with open(os.path.join(DIR, "data", "m5", f"{s}.csv")) as f:
            point[s] = float(f.readline().split("point=")[1].split(";")[0])
    return m5, d1, point


def sessions_from_bars(sym, bars, point):
    tzname, (oh, om), (ch, cm), _ = b4_sim.SYMS[sym]
    tz = ZoneInfo(tzname)
    by_day = defaultdict(list)
    for t, o, h, l, c, sp in bars:
        local = (t - timedelta(hours=7)).replace(tzinfo=NY).astimezone(tz)
        by_day[local.date()].append((local, o, h, l, c, sp * point))
    out = {}
    for d, bs in by_day.items():
        op = datetime(d.year, d.month, d.day, oh, om, tzinfo=tz)
        cl = datetime(d.year, d.month, d.day, ch, cm, tzinfo=tz)
        s = sorted(b for b in bs if op <= b[0] < cl)
        if s and s[0][0] == op and s[-1][0] == cl - timedelta(minutes=5):
            out[d] = s
    return out


def eod_spread(bars, d, point):
    last = [b for b in bars if b[0].date() == d]
    return last[-1][5] * point / last[-1][4] if last else 0.0001


def main():
    os.makedirs(FWD, exist_ok=True)
    st = json.load(open(STATE)) if os.path.exists(STATE) else {"equity": EQUITY0, "last_day": None, "rsi_pos": {}}
    m5, d1, point = fetch()
    if not d1:
        print(f"{datetime.now(timezone.utc).replace(tzinfo=None):%Y-%m-%d %H:%M} GEEN DATA van de VM — niets verwerkt"); return
    server_now = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=3)  # benadering servertijd (NY+7)
    days = sorted(d for d, _ in d1["US500cash"] if d >= START_DAY and d < server_now.date()
                  and (st["last_day"] is None or d > date.fromisoformat(st["last_day"])))
    new_rows, new_trades = [], []
    for D in days:
        eq = st["equity"]
        rsi_pnl = orb_pnl = 0.0
        # --- RSI(2): P&L van aangehouden posities, dan signalen op het slot van D
        for s in RSI_SYMS:
            ser = [x for x in d1[s] if x[0] <= D]
            if len(ser) < 201 or ser[-1][0] != D:
                continue
            closes = [c for _, c in ser]
            pos = st["rsi_pos"].get(s)
            if pos:
                prev_d, prev_c = ser[-2]
                pnl = pos["units"] * (closes[-1] - prev_c) - pos["units"] * prev_c * SWAP_LONG[s] * (D - prev_d).days / 365
                rsi_pnl += pnl
            r = rsi2(closes)[-1]
            sma = sum(closes[-200:]) / 200
            spr = eod_spread(m5.get(s, []), D, point.get(s, 0.01)) if s in m5 else 0.0001
            if pos and r is not None and r > 70:
                rsi_pnl -= pos["units"] * closes[-1] * spr
                new_trades.append((D, "RSI2", s, "exit", f"RSI {r:.1f}", ""))
                del st["rsi_pos"][s]
            elif not pos and r is not None and r < 10 and closes[-1] > sma:
                units = eq * RSI_FRAC / closes[-1]
                rsi_pnl -= units * closes[-1] * spr
                st["rsi_pos"][s] = {"units": units, "entry": closes[-1], "entry_date": str(D)}
                new_trades.append((D, "RSI2", s, "entry", f"RSI {r:.1f} slot {closes[-1]}", ""))
        # --- ORB op de sessie van datum D
        n_orb = 0
        for s in ORB_SYMS:
            sess = sessions_from_bars(s, m5.get(s, []), point[s])
            if D not in sess:
                continue
            tr = b4_sim.run_orb([(D, sess[D])], b4_sim.SYMS[s][3])
            for d, net, R in tr:
                pnl = net * eq * ORB_FRAC
                orb_pnl += pnl; n_orb += 1
                new_trades.append((D, "ORB", s, "trade", f"{net*1e4:+.1f} bp ({R:+.2f} R)", f"{pnl:.2f}"))
        st["equity"] = eq + rsi_pnl + orb_pnl
        st["last_day"] = str(D)
        new_rows.append((D, eq, st["equity"], rsi_pnl, orb_pnl, len(st["rsi_pos"]), n_orb))
    if not new_rows:
        print(f"{datetime.now(timezone.utc).replace(tzinfo=None):%Y-%m-%d %H:%M} geen nieuwe afgesloten dag"); return
    daily = os.path.join(FWD, "paper_daily.csv")
    new_file = not os.path.exists(daily)
    with open(daily, "a") as f:
        if new_file:
            f.write("date;start_balance;start_equity;min_equity;end_equity;rsi_pnl;orb_pnl;rsi_open;orb_trades\n")
        for D, e0, e1, rp, op, no, nt in new_rows:
            f.write(f"{D:%Y.%m.%d};{e0:.2f};{e0:.2f};{min(e0, e1):.2f};{e1:.2f};{rp:.2f};{op:.2f};{no};{nt}\n")
    trades = os.path.join(FWD, "paper_trades.csv")
    new_file = not os.path.exists(trades)
    with open(trades, "a") as f:
        if new_file:
            f.write("date;leg;symbol;action;detail;pnl_eur\n")
        for row in new_trades:
            f.write(";".join(str(x) for x in row) + "\n")
    json.dump(st, open(STATE, "w"), indent=1)
    msg = f"forward: papieren dag(en) {', '.join(str(r[0]) for r in new_rows)} — equity €{st['equity']:,.2f}"
    print(msg)
    if "--no-push" not in sys.argv:
        subprocess.run(["git", "-C", DIR, "add", "forward/paper_daily.csv", "forward/paper_trades.csv", "forward/state.json"], check=False)
        subprocess.run(["git", "-C", DIR, "commit", "-q", "-m", msg, "-m", "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"], check=False)
        subprocess.run(["git", "-C", DIR, "push", "-q", "origin", "HEAD:main"], check=False)


if __name__ == "__main__":
    main()
