# VOORSTEL_PRESCREEN_N69 — NZDUSD 10d Carry+Trend Long-Only (D-100 family B)

**Status:** **OPEN** — awaiting D-092.1 (**D-094** track 4 + **D-100 family B** carry+; replace N66–N68 closed; filed 2026-10-01 ~11:50 CEST).  
**Auteur:** Strateeg (Claude).  
**Instrument:** `NZDUSD` (RT **1,85 bp** — COSTS_FTMO; swap_long **+0,92** bp/nacht).  
**Track 4 + D-100 family B:** FX carry+ long-only — NZDUSD is positieve carry bij long (NZD hogere rente); TSMOM-signaal L20 filter, H10 entry. Hold 10 handelsdagen (9 nachten). Overnight goedkoopste kant = **long**.

**Gate (long-only; worst-case = long-pays; 9 nachten × 0,92 bp):**  
1,85 + 9 × 0,92 = **10,13 bp** → gate 3 × 10,13 = **30,39 bp**.  
(Swap-credit telt NIET als alfa per D-100; swap-kost WEL in poort.)

**D-094a:** train 2021–2023. Reden **(b)**: FX carry+trend literatuur (Koijen e.a.; NZD hogere rentevaluta; BIS-volumes aantoonbaar; FTMO-M5 kosten). Herhaal in PREREG.

**Onderscheid:**
- ≠ **TSMOM_DIV** dead (multi-asset maandelijks; dit = 10d FX solo)
- ≠ **B1** FX maand-TSMOM STOP (~20+ nachten)
- ≠ **N66** EURAUD SO (andere paar + short-kant; N66 subsumed in FX_EUR_SHORT)
- ≠ **N67** USDJPY DIAG_FAIL (andere paar + andere carry-logica)
- ≠ **N48** USDJPY 1d TSMOM FAIL (ander paar + 1d vs 10d)
- ≠ **N58** AUDUSD/USDJPY relative FAIL_MEAN
- ≠ enig ORB / intradag / energie

## Regel
- `ret20 = close_t / close_{t−20} − 1` (dagclose uit M5; laatste bar ≤22:00 CET)
- `ret20 > 0` → **LONG** op close_t (trendfilter: momentum positief)
- `ret10 > 0` (dagclose_{t} vs _{t−10}) → bevestig; anders skip
- Hold: exit close_{t+10} (10 handelsdagen). **Non-overlapping**.
- Alleen LONG (carry+); geen short-been.

## Pre-screen
- Data: `data/m5gz/NZDUSD.csv.gz` → dagclose, train **2021-01-01 … 2023-12-31**.
- Gate: mean bruto ≥ **30,39 bp**, N ≥ 150.
- PASS → PREREG_FTMO_N69. FAIL → STOP (geen lookback-grid, geen AUDUSD-switch).
