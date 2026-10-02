# VOORSTEL_PRESCREEN_N128 — BWX_INTL_TREASURY_STRESS → US500cash session-flat (NEW_FAMILY AW)

**Status:** **OPEN** — D-094 refill after N126 D-092.1 FAIL + N127 PASS→PREREG (filed 2026-10-03 ~00:10 CEST).  
**Auteur:** Strateeg (Grok). **NEW_FAMILY AW** (international / DM ex-US treasury ETF **level** stress → equity session-flat — global rates channel; **≠ TLT** US duration / **≠ TIP** real-rate / **≠ EMB** EM credit / **≠ YIELD_CURVE** 10Y−3M slope).  
**Signal:** Yahoo/proxy **BWX** (SPDR Bloomberg International Treasury Bond). **Trade:** `US500cash` (RT **0,78** bp; swap 0 — **session-flat**).  
**Track 4 + D-100 + D-097 rates:** Intl treasury stress as global rates / FX-reserve timing for DM large-cap; intradag-vlak.

**Gate:** 3 × US500 RT = 3 × 0,78 = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: BWX as **intl DM treasury basket** level ≠ TLT US long (N116), ≠ TIP (N118), ≠ EMB EM (N100), ≠ 10Y−3M slope (N124). FTMO-M5 for costs.

**Onderscheid:**
- ≠ **N116 TLT** / **N118 TIP** / **N100 EMB** / **N124 YIELD_CURVE** FAIL_T
- ≠ **N126 DBA** FAIL / **N127 EWZ** PREREG / N122 DBC / N123 EFA
- ≠ N75–N127 clones / BWX CFD trade leg / overnight / thr-grid / soft gate

## Regel
**Signal (dag t):**
1. `z120 = (BWX_t − mean_120(BWX)) / stdev_120(BWX)`; `d20 = BWX_t / BWX_{t−20} − 1`.
2. **combo:** `(z120 > +0,5) and (d20 > 0)` → **LONG** US500; `(z120 < −0,5) and (d20 < 0)` → **SHORT**; else skip.

**Execution (dag t+1, US500cash) — D-100 session-flat:**
3. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
4. Exit: flat ≤ **21:00 CET** same day. **No overnight.**
5. Non-overlapping (≤1/day).

## Pre-screen
- Data: `data/daily/BWX.csv` + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **2,34** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N128. FAIL → STOP (geen TLT/TIP/EMB/yield-curve rewrite, geen overnight, geen soft gate).
