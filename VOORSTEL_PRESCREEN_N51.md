# VOORSTEL_PRESCREEN_N51 — XAUUSD Swing TSMOM 20d→5d long-only + SMA200 regime (D-097.2)

**Status:** **geen PREREG — D-092.1 FAIL** Strateeg `n45_n51` (N=59, mean **8.4748** < gate **50.0**; FAIL_MEAN). Geen retune.
**Auteur:** Strateeg (Faraday / Claude).  
**Instrument:** `XAUUSD` (RT **0,83 bp**; swap_long **2,15** / swap_short **0,10** bp/nacht — COSTS_FTMO).  
**Track 4 + D-097.2:** lage omloop + **vooraf** regime-filter (close > SMA200); hold 5d beperkt swap-drag t.o.v. 10–20d.  
**Gate (long-only):** RT_eff = 0,83 + 5×2,15 = **11,58 bp** → 3× = **34,74 bp**. Binding bruto ≥ **50 bp** (C-021) én ≥ 34,74.

**D-094a:** train 2021–2023 FTMO-M5; mechanisme **(b)** goud-trend/TSMOM literatuur + lange proxy waar beschikbaar. Herhaal in PREREG.

**Onderscheid:**
- ≠ alle XAU **intradag** FAIL (N4/N7–N12/N19/N25/N31/N34/N36/AM_FADE watch)
- ≠ **N23/N48/N49/N50** (ander instrument / geen regime-filter / andere hold)
- ≠ **CEO TSMOM_DIV** (multi-asset maand 12-1, geen SMA200-filter)
- ≠ ORB / EU→US / FX intradag barred set

## Regel (bevroren)
- D1 close uit M5.
- Regime: `close_t > SMA200(close)` anders skip.
- `ret20 = close_t / close_{t-20} − 1`; `ret20 > 0` → LONG close_t; else skip.
- Exit close_{t+5}; non-overlapping; long-only.
- Geen intraday stop in bruto pre-screen.

## Pre-screen
- Data: `data/m5gz/XAUUSD.csv.gz` → D1, train 2021–2023.
- PASS → PREREG_FTMO_N51 iff mean ≥ **50 bp**, N≥150 (of N≥100 + D-094a (b)). FAIL → STOP (geen SMA/lookback/hold dunnen).
