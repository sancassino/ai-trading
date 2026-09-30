"""Dagelijkse FTMO-symbool-snapshot (draait op de VM): swap (ruw + %/jr bij swap_mode 1), actuele spread, contractspecs, voor alle symbolen in de lijst.
Uitvoer: CSV naar stdout. Gebruik: python mt5_symbol_snapshot.py SYM1,SYM2,..."""
import sys
import time
from datetime import datetime, timezone
import MetaTrader5 as mt5
if not mt5.initialize(path=r"C:\Program Files\MetaTrader 5\terminal64.exe", timeout=60000):
    sys.exit(f"initialize FAILED: {mt5.last_error()}")
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
print("snapshot_utc;symbol;swap_mode;swap_long;swap_short;swap_3day;bid;ask;spread_pts;point;contract;tick_value;currency_profit;currency_margin;"
      "spread_bp;long_pct_yr;short_pct_yr")
syms = sys.argv[1].split(",")
ok = {s: mt5.symbol_select(s, True) for s in syms}
time.sleep(5)                     # ticks laten binnenkomen na selectie
for s in syms:
    if not ok[s]:
        print(f"{ts};{s};NA;;;;;;;;;;;;;;"); continue
    i = mt5.symbol_info(s); t = mt5.symbol_info_tick(s)
    bid, ask = (t.bid, t.ask) if t else (0.0, 0.0)
    px = (bid + ask) / 2 if bid and ask else 0.0
    if not px:
        r0 = mt5.copy_rates_from_pos(s, mt5.TIMEFRAME_D1, 0, 1)
        px = float(r0[0]["close"]) if r0 is not None and len(r0) else 0.0
    spread_bp = (ask - bid) / px * 1e4 if px and bid and ask else float("nan")
    # swap_mode 1 = punten per lot per nacht → %/jr van notional; swap_mode 5 = rente %/jr (huidige prijs) → direct
    pct = lambda sw: (sw * i.point * i.trade_contract_size * 365 / (px * i.trade_contract_size) * 100 if px else float("nan")) if i.swap_mode == 1 else (float(sw) if i.swap_mode == 5 else float("nan"))
    print(f"{ts};{s};{i.swap_mode};{i.swap_long};{i.swap_short};{i.swap_rollover3days};{bid};{ask};{i.spread};{i.point};{i.trade_contract_size};"
          f"{i.trade_tick_value};{i.currency_profit};{i.currency_margin};{spread_bp:.3f};{pct(i.swap_long):.3f};{pct(i.swap_short):.3f}")
mt5.shutdown()
