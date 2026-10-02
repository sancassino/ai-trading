# VOORSTEL_PRESCREEN_N116 — TLT_DURATION_STRESS → US500cash session-flat (NEW_FAMILY AK)

**Status:** **PASS → PREREG** D-092.1 `n116_n117` (N=386, mean **+6,01 ≥ 2,34**; years +3,39/+9,62/+1,92) → `PREREG_FTMO_N116_TLT_DURATION_STRESS.md`. Screened 2026-10-02 ~23:12 CEST.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY AK** (US long-duration Treasury ETF stress → equity session-flat — rates/duration channel, nooit als HYG/EMB credit twin).  
**Signal:** Yahoo/proxy **TLT** (20+y UST ETF). **Trade:** `US500cash` (RT **0,78** bp; swap 0 — **session-flat**).  
**Track 4 + D-100:** Duration/rates level+trend as risk-off timing for DM equity; intradag-vlak (geen swap).

**Gate:** 3 × US500 RT = 3 × 0,78 = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: TLT as long-end rates/duration stress proxy into equity beta (rates spike = risk-off); distinct from HYG domestic credit and EMB EM hard-currency. FTMO-M5 for costs. Herhaal in PREREG.

**Onderscheid:**
- ≠ **N114** HYG_CREDIT_STRESS OPEN/PREREG (HY credit ≠ duration/rates)
- ≠ **N100 EMB** FAIL_T / **N112 GAS** FAIL_T / **N113 SILVER_GOLD** FAIL_COST_GATE
- ≠ REIT_RATE VNQ/TLT ratio (prior Lane-A; this = **TLT level** alone → equity)
- ≠ VIX / SECTOR_DISP / L60 / ORB-meta / UKOIL-OVN / CORN / N75–N115 clones

## Regel
**Signal (dag t):**
1. `z120 = (TLT_t − mean_120(TLT)) / stdev_120(TLT)`; `d20 = TLT_t / TLT_{t−20} − 1`.
2. **combo:** `(z120 > +0,5) and (d20 > 0)` → **LONG** US500 (duration rally = risk-on / easier financial conditions); `(z120 < −0,5) and (d20 < 0)` → **SHORT** (duration crash = rates spike / risk-off); else skip.

**Execution (dag t+1, US500cash) — D-100 session-flat:**
3. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
4. Exit: flat ≤ **21:00 CET** same day. **No overnight.**
5. Non-overlapping (≤1/day).

## Pre-screen
- Data: Yahoo/proxy `data/daily/TLT.csv` + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **2,34** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N116. FAIL → STOP (geen thr-grid, geen IEF/LQD twin, geen HYG rewrite → N114 clone, geen overnight, geen soft gate).
