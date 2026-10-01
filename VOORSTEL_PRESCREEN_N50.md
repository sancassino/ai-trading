# VOORSTEL_PRESCREEN_N50 — USOILcash Swing TSMOM 20d→10d long-only (D-097)

**Status:** **geen PREREG — D-092.1 FAIL** Strateeg `n45_n51` (N=54, mean **34.1834** < gate **50.0**; FAIL_MEAN). Geen retune.
**Auteur:** Strateeg (Faraday / Claude).  
**Instrument:** `USOILcash` (RT **3,34 bp**; swap_long **−5,40** / swap_short **+24,53** bp/nacht — COSTS_FTMO).  
**Track 4 + D-097:** energie-TSMOM parallel aan N49 (C-022 WTI_F L20/H10 bruto ≈61 bp, t_net ≈2,3).  
**Gate (long-only):** RT_eff = 3,34 → 3× = **10,02 bp**. Binding bruto ≥ **50 bp** (C-021) én ≥ 10,02.  
**Swap:** long-only (short-swap verboden).

**D-094a:** train 2021–2023 FTMO-M5; mechanisme **(b)** via `data/daily/WTI_F.csv` ≥10j (C-022). Herhaal in PREREG.

**Onderscheid:**
- ≠ **N49** UKOIL/Brent (ander contract + proxy)
- ≠ **S2-USOIL** EIA-window intradag STOP
- ≠ **N22/N43** UKOIL intradag FAIL/underpowered
- ≠ **CEO TSMOM_DIV** multi-asset maand; ≠ **N23** index 2d FAIL
- ≠ ORB / N35–N48 intradag-FX

## Regel (bevroren)
- Identiek N49-structuur op `USOILcash`: `ret20>0` → LONG close_t → exit close_{t+10}; non-overlap; long-only.

## Pre-screen
- Data: `data/m5gz/USOILcash.csv.gz` → D1, train 2021–2023.
- PASS → PREREG_FTMO_N50 iff mean bruto ≥ **50 bp**, N≥150 (of N≥100 + D-094a (b)). FAIL → STOP (geen retune).
