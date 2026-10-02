# VOORSTEL_PRESCREEN_N125 — DEFENSIVE_CYCLICAL → US500cash session-flat (NEW_FAMILY AT)

**Status:** **DIAG_PASS → PREREG frozen** (CTO C-039 2026-10-02 ~23:56 CEST).  
**Auteur:** CTO (Grok) from S2 cycle_2346 `13fe10c` (US500 twin preferred over NDX). Faraday OPEN empty; pipeline refill D-094.  
**Signal:** Yahoo/proxy **XLU/XLI** relative. **Trade:** `US500cash` (RT **0,78** bp; swap 0 — session-flat).  
**Gate:** 3 × US500 RT = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: utilities-vs-industrials relative as defensive/cyclical risk-appetite — ≠ SECTOR_DISP multi-XL* dispersion.

**Onderscheid:** ≠ N93 SECTOR_DISP / N124 YIELD_CURVE / TLT/TIP/HYG/EMB / N75–N123 clones.

## Regel
1. `rel = XLU/XLI`; `z40` rolling; thr **0,5**.
2. **defensive_high:** z>+0,5 → SHORT; z<−0,5 → LONG; else skip.
3. Execution t+1 US500cash 15:30→21:00 CET session-flat. No overnight. No US100 remap.

## Pre-screen / diag
- CTO C-039: N=478, mean **+5.479** ≥ 2.34 → **DIAG_PASS** → `PREREG_FTMO_N125_DEFENSIVE_CYCLICAL.md`.
- Gate smoke: cost PASS / stress PASS (5.48≥3.51); t_nw≈1.29; test 2024 mean −2.32 t_nw≈−0.77 → elevated FAIL_T risk; no retune.
