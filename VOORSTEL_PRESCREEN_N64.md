# VOORSTEL_PRESCREEN_N64 — HK50 short-only TSMOM 20→10 (D-100 family A)

**Status:** **geen PREREG — underpowered** mean **+89,62** ≥ 50 maar **N=55≪150**. No threshold shift; proxy/pool later only with D-094a.
**Instrument:** `HK50cash` short-only when ret20 < 0 (C-024 best_side=short +0,15 %/jr). Gate **50 bp**.  
**Onderscheid:** ≠ IDX_SHORT (US100/US30); ≠ N61 AUS200 FAIL; ≠ N35/N41 intradag.
## Regel
- ret20 < 0 → SHORT; exit t+10; non-overlap.
## Pre-screen
- Train 2021–2023. PASS iff mean ≥ 50, N≥150. FAIL → STOP.
