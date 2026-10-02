# VOORSTEL_PRESCREEN_N131 — DXY_DOLLAR_STRESS → US500cash session-flat (NEW_FAMILY AZ)

**Status:** **STOP FAIL_T** — U2 `03ad9da` (TRIAL **469→470**; t/NW **1,01/1,05**; test N=146 bruto **−1,10**). Cost+stress PASS. Session 15:30–21:00 **≠ N110**. Dead += N131; no DXY clone. Was D-092.1 PASS (N=413, +5,08).  
**Auteur:** Strateeg (Grok). **NEW_FAMILY AZ** (broad **US dollar index level** stress → equity session-flat — financial-conditions / dollar-smile channel; **≠ N110** DXY Lon-AM→EU-afternoon lead-lag / **≠ EWZ** country equity / **≠ BWX** intl treasury level / **≠ FX 5d LO** carry).  
**Signal:** Yahoo/proxy **DXY** (DX-Y.NYB). **Trade:** `US500cash` (RT **0,78** bp; swap 0 — **session-flat**).  
**Track 4 + D-100 + D-097:** Dollar uptrend as tighter global conditions into the US cash session; intradag-vlak (geen swap).

**Gate:** 3 × US500 RT = 3 × 0,78 = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: DXY **level combo** into US500 cash is not the N110 session lead-lag (DATA_GAP, different clocks and EU index leg), not a single-country equity ETF (EWZ/EEM/EFA dead), and not a bond-ETF level (TLT/TIP/BWX). FTMO-M5 for costs.

**Onderscheid:**
- ≠ **N110** DXYcash Lon-AM → EU-afternoon DIAG_FAIL (lead-lag ≠ dollar-level → US500 cash)
- ≠ **N127 EWZ** FAIL_T / **N121 EEM** / **N123 EFA** (equity ETF ≠ dollar index)
- ≠ **N128 BWX** / **N116 TLT** / **N118 TIP** / **N124 YIELD_CURVE** (rates ≠ DXY)
- ≠ N84 AUDNZD stretch / L60 FX-med / 5d FX LO carry set
- ≠ N75–N130 clones / thr-grid / soft gate / overnight US100 / DXY Lon→EU-PM rewrite

## Regel
**Signal (dag t):**
1. `z120 = (DXY_t − mean_120(DXY)) / stdev_120(DXY)`; `d20 = DXY_t / DXY_{t−20} − 1`.
2. **dollar_tightening (inverse combo):** `(z120 > +0,5) and (d20 > 0)` → **SHORT** US500; `(z120 < −0,5) and (d20 < 0)` → **LONG**; else skip.

**Execution (dag t+1, US500cash) — D-100 session-flat:**
3. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
4. Exit: flat ≤ **21:00 CET** same day. **No overnight.**
5. Non-overlapping (≤1/day).

## Pre-screen
- Data: `data/daily/DXY.csv` + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **2,34** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N131. FAIL → STOP (geen N110 rewrite, geen EWZ/EEM/EFA clone, geen thr-grid, geen overnight, geen soft gate).
