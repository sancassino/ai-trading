"""Forward (PREREG_PORT §3): FRED-FX_*-reeksen (FRED geblokkeerd na 25-09-2026) aanvullen met Yahoo =X-slotkoersen van hetzelfde paar,
alleen voor datums ná de laatste FX_*-datum (append-only, snapshot). Tijdstip verschilt (FRED noon NY vs Yahoo-slot) — vermeld."""
from update_daily import snapshot
MAP = {"FX_EURUSD": "EURUSD", "FX_GBPUSD": "GBPUSD", "FX_USDJPY": "USDJPY", "FX_AUDUSD": "AUDUSD", "FX_USDCAD": "USDCAD",
       "FX_USDCHF": "USDCHF", "FX_NZDUSD": "NZDUSD"}
for fx, y in MAP.items():
    p = f"data/daily/{fx}.csv"
    last = max(l.split(";")[0] for l in open(p) if l[:1].isdigit())
    from datetime import date as _d
    new = [l.strip() for l in open(f"data/daily/{y}.csv") if l[:1].isdigit() and l.split(";")[0] > last and _d.fromisoformat(l.split(";")[0]).weekday() < 5]
    rows = [f"{r.split(';')[0]};;;;{r.split(';')[4]};{r.split(';')[4]};" for r in new if r.split(";")[4]]
    if rows:
        with open(p, "a") as f:
            f.write("\n".join(rows) + "\n")
        snapshot(fx, rows)
    print(fx, "+", len(rows))
