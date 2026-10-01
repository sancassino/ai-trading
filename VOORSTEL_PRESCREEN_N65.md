# VOORSTEL_PRESCREEN_N65 — XAGUSD short-only 5d TSMOM (D-100 family C)

**Status:** **geen PREREG — D-092.1 FAIL_MEAN** mean **+39,23** < 50 (N=98).
**Instrument:** `XAGUSD` **short-only** when ret5 < 0 (C-024 best_side=short +0,41 %/jr; long is SWAP_HOSTILE −11 %/jr). Gate: RT 5,07 → 3×=15,21 → bindend **50 bp** (D-097). Hold 5d; optional 1,5×ATR stop.  
**Onderscheid:** ≠ N60 bi-dir FAIL (long worst-case); ≠ N36 XAU intradag; ≠ ENERGY.
## Regel
- ret5 < 0 → SHORT; exit t+5 or 1,5×ATR stop; non-overlap. Geen long-been.
## Pre-screen
- Train 2021–2023. PASS iff mean ≥ 50, N≥150. FAIL → STOP.
