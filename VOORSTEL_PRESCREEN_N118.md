# VOORSTEL_PRESCREEN_N118 — TIP_REALRATE_STRESS → US500cash session-flat (NEW_FAMILY AM)

**Status:** **PASS → PREREG** D-092.1 `n118_n119` (N=359, mean **+5,38 ≥ 2,34**; years −7,40/+7,92/+5,27) → `PREREG_FTMO_N118_TIP_REALRATE_STRESS.md`. Screened 2026-10-02 ~23:16 CEST.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY AM** (US TIPS / real-rate ETF stress → equity session-flat — inflation-linked real rates channel, nooit als TLT nominal-duration twin).  
**Signal:** Yahoo/proxy **TIP** (TIPS ETF). **Trade:** `US500cash` (RT **0,78** bp; swap 0 — **session-flat**).  
**Track 4 + D-100:** Real-rate / inflation-expectations level+trend as risk-off timing for DM equity; intradag-vlak (geen swap).

**Gate:** 3 × US500 RT = 3 × 0,78 = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: TIP as real-rate / breakeven inflation proxy into equity beta — distinct from TLT nominal long-duration (N116) and from HYG/EMB credit. FTMO-M5 for costs. Herhaal in PREREG.

**Onderscheid:**
- ≠ **N116** TLT_DURATION_STRESS (nominal long-end duration ≠ TIPS real-rate)
- ≠ **N114 HYG** FAIL_T / **N100 EMB** FAIL_T / **N112 GAS** / **N113 SILVER_GOLD**
- ≠ REIT_RATE VNQ/TLT ratio / IEF twin rewrite of N116
- ≠ VIX / SECTOR_DISP / L60 / ORB-meta / UKOIL-OVN / CORN / N75–N117 clones

## Regel
**Signal (dag t):**
1. `z120 = (TIP_t − mean_120(TIP)) / stdev_120(TIP)`; `d20 = TIP_t / TIP_{t−20} − 1`.
2. **combo:** `(z120 > +0,5) and (d20 > 0)` → **LONG** US500 (real-rate relief / easier conditions); `(z120 < −0,5) and (d20 < 0)` → **SHORT** (real-rate spike / risk-off); else skip.

**Execution (dag t+1, US500cash) — D-100 session-flat:**
3. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
4. Exit: flat ≤ **21:00 CET** same day. **No overnight.**
5. Non-overlapping (≤1/day).

## Pre-screen
- Data: Yahoo/proxy `data/daily/TIP.csv` + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **2,34** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N118. FAIL → STOP (geen thr-grid, geen TLT rewrite → N116 clone, geen IEF twin, geen overnight, geen soft gate).
