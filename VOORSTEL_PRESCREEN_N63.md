# VOORSTEL_PRESCREEN_N63 — EURCHF long-only carry+trend 20→10 (D-100 family B)

**Status:** **geen PREREG — D-092.1 FAIL_MEAN** mean **−43,08** < 50 (N=43).
**Instrument:** `EURCHF` long-only (C-024 best_side=long +0,46 %/jr). Gate **50 bp**. Hold 10d.  
**Onderscheid:** ≠ N58 AUDJPY FAIL; ≠ N62 GBPJPY FAIL; ≠ B1; ≠ intradag FX BARRED.
## Regel
- ret20 > 0 → LONG; exit t+10; non-overlap.
## Pre-screen
- Train 2021–2023. PASS iff mean ≥ 50, N≥150. FAIL → STOP.
