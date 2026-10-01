# VOORSTEL_PRESCREEN_N67 — USDJPY long-only carry+trend 20→10 (D-100 family B)

**Status:** **DIAG_FAIL** — CTO C-025/C-026 (L20/H10 long). Geen PREREG. Live medium-term pad = CTO `PREREG_FTMO_FX_USDJPY_MED_TSMOM` (L60/H10; ≠ this L20).  
**Instrument:** `USDJPY` long-only (C-024 best_side=long +0,98 %/jr). Gate **50 bp**. Hold 10d.  
**Onderscheid:** ≠ N48 1d FAIL; ≠ N53 underpowered 60→20; ≠ S2-USDJPY intradag STOP; ≠ B1.
## Regel
- ret20 > 0 → LONG; exit t+10; non-overlap.
## Pre-screen
- Train 2021–2023. PASS iff mean ≥ 50, N≥150. FAIL → STOP.
