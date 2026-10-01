"""Ververst de MT5-historiecache op de VM vóór de forward-exports (forward_paper 22:15, forward_p1): copy_rates_range dwingt een sync af,
copy_rates_from_pos (in mt5_export_recent.py, bevroren I1) doet dat na een herstart niet (gezien 2026-10-01). Gebruik: python mt5_warmup.py SYM1,SYM2,..."""
import sys
import time
from datetime import datetime, timedelta, timezone
import MetaTrader5 as mt5
if not mt5.initialize(path=r"C:\Program Files\MetaTrader 5\terminal64.exe", timeout=60000):
    sys.exit(f"initialize FAILED: {mt5.last_error()}")
end = datetime.now(timezone.utc) + timedelta(days=1)
for k in range(2):
    for s in sys.argv[1].split(","):
        mt5.symbol_select(s, True)
        for tf, days in ((mt5.TIMEFRAME_M5, 10), (mt5.TIMEFRAME_D1, 400)):
            r = mt5.copy_rates_range(s, tf, end - timedelta(days=days), end)
            if k == 1 and tf == mt5.TIMEFRAME_M5:
                print(s, "laatste M5", datetime.fromtimestamp(int(r[-1]["time"]), timezone.utc).strftime("%Y.%m.%d %H:%M") if r is not None and len(r) else "GEEN")
    time.sleep(5)
mt5.shutdown()
