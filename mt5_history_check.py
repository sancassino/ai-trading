"""Eerste beschikbare D1-bar per FTMO-symbool (draait op de VM)."""
import csv, sys
from datetime import datetime
import MetaTrader5 as mt5

if not mt5.initialize(path=r"C:\Program Files\MetaTrader 5\terminal64.exe", timeout=60000):
    sys.exit(f"initialize FAILED: {mt5.last_error()}")
out = []
GROUPS = ("Agriculture", "Cash", "Commodities", "Equities", "Metals")
for s in mt5.symbols_get():
    if not s.path.startswith(GROUPS) or s.name.startswith(("XAG", "XAU")) and not s.name.endswith("USD"):
        continue
    mt5.symbol_select(s.name, True)
    r = mt5.copy_rates_range(s.name, mt5.TIMEFRAME_D1, datetime(2019, 1, 1), datetime(2026, 9, 25))
    first = datetime.utcfromtimestamp(r[0]["time"]).strftime("%Y-%m-%d") if r is not None and len(r) else "-"
    out.append((s.name, s.path.split("\\")[0], first, len(r) if r is not None else 0))
    print(*out[-1], sep=";", file=sys.stderr, flush=True)
mt5.shutdown()
w = csv.writer(sys.stdout, delimiter=";")
w.writerow(["symbol", "group", "first_d1", "bars"])
w.writerows(sorted(out, key=lambda x: (x[1], x[0])))
