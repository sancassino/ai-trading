# VOORSTEL_PRESCREEN_N124 — YIELD_CURVE_2S10S → US500cash session-flat (NEW_FAMILY AS)

**Status:** **DIAG_PASS → PREREG frozen** (CTO C-039 2026-10-02 ~23:56 CEST).  
**Auteur:** CTO (Grok) from S2 cycle_2346 `13fe10c` (Faraday OPEN empty; pipeline refill D-094).  
**Signal:** Yahoo/proxy **YLD_US10Y − YLD_US3M**. **Trade:** `US500cash` (RT **0,78** bp; swap 0 — session-flat).  
**Gate:** 3 × US500 RT = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: Treasury 10Y−3M slope z as risk-appetite / recession-timing into DM equity — ≠ TLT price / TIP / REIT_RATE / RATE_CURVE.

**Onderscheid:** ≠ N116 TLT / N118 TIP / N114 HYG / N100 EMB / RATE_CURVE / REIT_RATE / N75–N123 clones.

## Regel
1. `slope = YLD_US10Y − YLD_US3M`; `z60` rolling; thr **1,5**.
2. **flatten_fade:** z>+1,5 → SHORT; z<−1,5 → LONG; else skip.
3. Execution t+1 US500cash 15:30→21:00 CET session-flat. No overnight.

## Pre-screen / diag
- CTO C-039: N=240, mean **+8.971** ≥ 2.34 → **DIAG_PASS** → `PREREG_FTMO_N124_YIELD_CURVE_2S10S.md`.
- Gate smoke: cost PASS / stress PASS (8.97≥3.51); t_nw≈1.82; test 2024 mean +2.89 t_nw≈0.33 → elevated FAIL_T risk; no retune.
