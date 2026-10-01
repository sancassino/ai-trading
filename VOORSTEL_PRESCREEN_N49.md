# VOORSTEL_PRESCREEN_N49 — UKOILcash Swing TSMOM 20d→10d long-only (D-097)

**Status:** **geen PREREG — D-092.1 FAIL** Strateeg `n45_n51` (N=55, mean **36.4032** < gate **50.0**; FAIL_MEAN). Geen retune.
**Auteur:** Strateeg (Faraday / Claude).  
**Instrument:** `UKOILcash` (RT **2,71 bp**; swap_long **−5,98** / swap_short **+27,03** bp/nacht — COSTS_FTMO).  
**Track 4 + D-097:** lage omloop, groot bruto per trade (C-022 proxy: L20/H10 bruto ≈117 bp, t_net ≈3,6 op 2015–2024 BRENT_F).  
**Gate (long-only):** RT_eff = RT + 10×max(0, swap_long) = **2,71** bp → 3× = **8,13 bp**. Binding bruto ≥ **50 bp** (C-021/D-098 floor) én ≥ 8,13.  
**Swap note:** long ontvangt swap (−5,98); short verboden in deze regel (short-swap 27 bp/nacht doodt edge).

**D-094a:** train 2021–2023 op FTMO-M5; mechanisme **(b)** op ≥10j proxy `data/daily/BRENT_F.csv` (C-022). Herhaal in PREREG.

**Onderscheid (anti-kloon):**
- ≠ **N22** UKOIL Lon→NY session **MR** FAIL (intradag fade)
- ≠ **N43** UKOIL NY-open drive underpowered (intradag)
- ≠ **B1** FX month TSMOM STOP; ≠ **N23** US100 2d bi-dir FAIL
- ≠ **CEO TSMOM_DIV** (D-098 multi-asset maand 12-1) — dit = single-name energy, 10d hold
- ≠ **S2-USOIL** EIA intradag STOP; ≠ ORB / N35–N47 intradag

## Regel (bevroren)
- D1 close uit M5 (laatste bar / 22:00 CET).
- `ret20 = close_t / close_{t-20} − 1`
- Als `ret20 > 0` → **LONG** op close_t; anders skip (long-only).
- Hold: exit close_{t+10} (**10** handelsdagen). Non-overlapping.
- Geen intraday stop in bruto pre-screen.

## Pre-screen
- Data: `data/m5gz/UKOILcash.csv.gz` → D1, train **2021-01-01 … 2023-12-31** only (geen test/reserve).
- Maatstaf: mean bruto bp, N non-overlap.
- PASS → PREREG_FTMO_N49 iff mean ≥ **50 bp** én N≥150 (of N≥100 met D-094a (b) proxy-cite + forward). FAIL → STOP (geen hold/lookback dunnen).
