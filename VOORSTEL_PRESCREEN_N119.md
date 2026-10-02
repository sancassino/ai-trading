# VOORSTEL_PRESCREEN_N119 — IWM_SMALLCAP_STRESS → US500cash session-flat (NEW_FAMILY AN)

**Status:** **OPEN** — pipeline refill after N114 FAIL_T + N116/N117 PASS→PREREG (filed 2026-10-02 ~23:12 CEST).  
**Auteur:** Strateeg (Grok). **NEW_FAMILY AN** (Russell 2000 / small-cap ETF stress → large-cap equity session-flat — breadth / risk-appetite channel, nooit als SECTOR_DISP twin).  
**Signal:** Yahoo/proxy **IWM** (Russell 2000 ETF). **Trade:** `US500cash` (RT **0,78** bp; swap 0 — **session-flat**).  
**Track 4 + D-100:** Small-cap breadth stress as risk-appetite timing for large-cap DM equity; intradag-vlak (geen swap).

**Gate:** 3 × US500 RT = 3 × 0,78 = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: IWM as small-cap breadth / risk-on proxy into US500 beta — distinct from sector-dispersion rotation (N93) and from index pair RV; FTMO-M5 for costs. Herhaal in PREREG.

**Onderscheid:**
- ≠ **N93 SECTOR_DISP_ROTATION** FAIL_COST_GATE (XL* dispersion ≠ IWM **level** breadth)
- ≠ **N81** US100/US500 pair RV / **N2** relative morning
- ≠ **N114 HYG** / **N116 TLT** / **N117 CPER** / EMB / GAS / SILVER_GOLD
- ≠ VIX / L60 / ORB-meta / UKOIL-OVN / CORN / N75–N118 clones / IWM CFD trade leg

## Regel
**Signal (dag t):**
1. `z40 = (IWM_t − mean_40(IWM)) / stdev_40(IWM)`.
2. **stress_buy:** `z40 > +1,5` → **SHORT** US500 (small-cap spike = late-cycle / crowded risk-on fade into large-cap); `z40 < −1,5` → **LONG** (small-cap crash = growth-scare bounce / relief into large-cap); else skip.

**Execution (dag t+1, US500cash) — D-100 session-flat:**
3. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
4. Exit: flat ≤ **21:00 CET** same day. **No overnight.**
5. Non-overlapping (≤1/day).

## Pre-screen
- Data: Yahoo/proxy `data/daily/IWM.csv` + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **2,34** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N119. FAIL → STOP (geen thr-grid, geen SECTOR_DISP rewrite, geen IWM CFD twin, geen overnight, geen soft gate).
