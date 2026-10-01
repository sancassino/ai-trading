# VOORSTEL_PRESCREEN_N62 — GBPJPY long-only carry+trend 20→10 (D-100 family B)

**Status:** **geen PREREG — D-092.1 FAIL_MEAN** mean **+9,75** < 50 (N=55).
**Auteur:** Strateeg (Faraday).  
**Instrument:** `GBPJPY` **long-only** (C-024 best_side=long, +0,71 %/jr).  
**Gate:** **50 bp** (D-097); 3×RT≈6. Hold 10d. Swap_gate long earn → 0.

**D-094a (b):** FX carry+trend; ≠ S2-GBPJPY_EU_MOM intradag FAIL_T (andere horizon/regel).

**Onderscheid:** ≠ S2-GBPJPY session mom STOP; ≠ N58 AUDJPY (ander pair); ≠ B1 month; ≠ N48 USDJPY 1d FAIL.

## Regel
- `ret20 > 0` → **LONG**; else skip. Exit t+10. Non-overlap.

## Pre-screen
- Train 2021–2023. PASS iff mean ≥ **50**, N≥150. FAIL → STOP.
