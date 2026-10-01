# VOORSTEL_PRESCREEN_N53 — USDJPY Swing TSMOM 60d→20d long-only (D-097)

**Status:** **geen PREREG — underpowered** Strateeg `n45_n51` (mean **91.6463** ≥ gate **50.0** maar **N=32≪150**). Geen drempel/hold-shift; zie N55/N56 pool.
**Auteur:** Strateeg (Faraday).  
**Instrument:** `USDJPY` (RT **0,78**; swap_long **−0,37** / swap_short **1,58**).  
**Gate (long-only H20):** RT_eff = 0,78 + 20×max(0,−0,37) = **0,78** → 3× = **2,34 bp**. Binding bruto ≥ **50 bp** (C-021).  
**Bron:** C-022 FX_USDJPY L60/H20 long-only near-bar (bruto ≈48 — borderline; FTMO-screen beslist).

**D-094a (b):** FX daily TSMOM literatuur + lange USDJPY proxy.

**Onderscheid:** ≠ **N48** 1d bi-dir FAIL; ≠ **B1** month STOP; ≠ **S2-USDJPY** Tokyo-range intradag STOP; ≠ N46/N47 BARRED intradag.

## Regel
- `ret60>0` → LONG close_t → exit close_{t+20}; non-overlap; long-only (geen short).

## Pre-screen
- Train 2021–2023. PASS iff mean ≥ **50 bp**, N≥150 (of N≥100 + D-094a b). FAIL → STOP.
