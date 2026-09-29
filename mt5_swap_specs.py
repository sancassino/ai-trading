"""Huidige swap per symbool omgerekend naar % van notional per jaar (draait op de VM)."""
import sys
import MetaTrader5 as mt5
if not mt5.initialize(path=r"C:\Program Files\MetaTrader 5\terminal64.exe", timeout=60000):
    sys.exit(f"initialize FAILED: {mt5.last_error()}")
print("symbol;swap_mode;swap_long;swap_short;price;contract;long_pct_yr;short_pct_yr")
for s in sys.argv[1].split(","):
    mt5.symbol_select(s, True)
    i = mt5.symbol_info(s)
    r0 = mt5.copy_rates_from_pos(s, mt5.TIMEFRAME_D1, 0, 1)
    px = float(r0[0]["close"]) if r0 is not None and len(r0) else 0.0
    # waarde van 1 punt voor 1 lot in winstvaluta = point * contract_size
    per_day = lambda sw: sw * i.point * i.trade_contract_size if i.swap_mode == 1 else float("nan")
    yr = lambda sw: per_day(sw) * 365 / (px * i.trade_contract_size) * 100 if px else float("nan")
    print(f"{s};{i.swap_mode};{i.swap_long};{i.swap_short};{px};{i.trade_contract_size};{yr(i.swap_long):.2f};{yr(i.swap_short):.2f}")
mt5.shutdown()
