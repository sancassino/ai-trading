# VOORSTEL_PRESCREEN_N124 — YIELD_CURVE_2S10S → US500cash session-flat (NEW_FAMILY AS)

**Status:** **STOP FAIL_T** U2 `9f00f24` (TRIAL **464→465**; cost+stress PASS; t/NW **1,72/1,82** <2; test +2,89). Dead += N124; no yield-curve / thr-grid / US100 overnight / TLT-TIP-SECTOR_DISP clones.
**Auteur:** Strateeg (Grok). **NEW_FAMILY AS** from S2 `13fe10c` cycle_2346.  
**Signal:** US Treasury **10Y−3M** slope. **Trade:** `US500cash` (RT **0,78** bp; swap 0 — **session-flat**).  
**Track 4 + D-100:** Curve-shape / growth-expectations timing for DM large-cap; intradag-vlak (geen swap).

**Gate:** 3 × US500 RT = 3 × 0,78 = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: 10Y−3M slope ≠ TLT duration level (N116) ≠ TIP real-rate (N118) ≠ REIT_RATE. FTMO-M5 for costs.

**Onderscheid:**
- ≠ **N116 TLT** FAIL_T / **N118 TIP** FAIL_T / **N120 VNQ** / RATE_CURVE→UKOIL N79
- ≠ **N114 HYG** / **N100 EMB** / **N93 SECTOR_DISP** / **N78 VIX**
- ≠ VIX / L60 / ORB-meta / UKOIL-OVN / CORN / N75–N123 clones / bond CFD trade leg

## Regel
**Signal (dag t):**
1. `slope = YLD_US10Y − YLD_US3M`; `z60` (min_periods=max(20,20)).
2. **flatten_fade:** `z60 > +1,5` → **SHORT**; `z60 < −1,5` → **LONG**; else skip.

**Execution (dag t+1, US500cash) — D-100 session-flat:**
3. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
4. Exit: flat ≤ **21:00 CET** same day. **No overnight.**
5. Non-overlapping (≤1/day).

## Pre-screen result
- Data: `YLD_US10Y`/`YLD_US3M` + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- N=**240**, mean **+8,97**, med **+9,89**, years 2021 **−2,31** / 2022 **+8,57** / 2023 **+12,41** → **PASS_may_PREREG**.
- FAIL path (if U2 fails): STOP — geen thr-grid, geen TLT/TIP rewrite, geen overnight, geen soft gate.
