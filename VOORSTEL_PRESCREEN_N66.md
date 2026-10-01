# VOORSTEL_PRESCREEN_N66 — EURAUD short-only carry+trend 20→10 (D-100 family B)

**Status:** **OPEN** — awaiting D-092.1 (filed 2026-10-01 ~11:30 CEST; replaces N58/N62/N63 FAIL).  
**Instrument:** `EURAUD` short-only when ret20 < 0 (C-024 best_side=short +0,74 %/jr). Gate **50 bp**. Hold 10d.  
**Onderscheid:** ≠ N63 EURCHF FAIL; ≠ N58/N62; ≠ A5 intradag; ≠ B1 month.
## Regel
- ret20 < 0 → SHORT; exit t+10; non-overlap.
## Pre-screen
- Train 2021–2023. PASS iff mean ≥ 50, N≥150. FAIL → STOP.
