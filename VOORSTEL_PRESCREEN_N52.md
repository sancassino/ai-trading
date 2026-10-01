# VOORSTEL_PRESCREEN_N52 — US100cash Swing TSMOM 120d→20d long-only (D-097)

**Status:** **geen PREREG — underpowered** Strateeg `n45_n51` (mean **131.0173** ≥ gate **118.98** maar **N=21≪150**). Geen drempel/hold-shift; zie N55/N56 pool.
**Auteur:** Strateeg (Faraday).  
**Instrument:** `US100cash` (RT **0,66**; swap_long **1,95** / swap_short **0,21**).  
**Gate (long-only H20):** RT_eff = 0,66 + 20×1,95 = **39,66** → 3× = **118,98 bp**. Binding ≥ **118,98** (also ≥50 C-021).  
**Bron:** C-022 proxy NDX L120/H20 long-only bruto ≈124 bp (2015–2024).

**D-094a (b):** ≥10j NDX/proxy mechanisme; FTMO-M5 train 2021–2023 kosten.

**Onderscheid:** ≠ **N23** US100 2d bi-dir FAIL; ≠ **N49/N50** energy; ≠ **CEO TSMOM_DIV** multi-asset maand; ≠ ORB/N35.

## Regel
- `ret120 = close_t/close_{t-120}−1`; `ret120>0` → LONG close_t → exit close_{t+20}; non-overlap; long-only.

## Pre-screen
- `data/m5gz/US100cash.csv.gz` D1, train 2021–2023. PASS iff mean ≥ **118,98** bp, N≥150 (of N≥100 + D-094a b). FAIL → STOP.
