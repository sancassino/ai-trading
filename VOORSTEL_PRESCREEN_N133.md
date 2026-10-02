# VOORSTEL_PRESCREEN_N133 — GLD_GOLD_HAVEN_STRESS → US500cash session-flat (NEW_FAMILY BB)

**Status:** **geen PREREG — D-092.1 FAIL** — `n132_n133` train N=**361** mean bruto **+0,26** < gate **2,34** (med −0,68; years −4,00/+12,60/−12,07; L/S 146/215); screened 2026-10-03 ~00:23 CEST. Dead screen; no GLD/GOLD haven clone.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BB** (gold ETF **haven bid** → equity session-flat — monetary-metal channel; **≠ SILVER_GOLD** ratio / **≠ PPLT** / **≠ CPER** / **≠ DBC** / **≠ TIP** / **≠ DXY**).  
**Signal:** Yahoo/proxy **GLD**. **Trade:** `US500cash` (RT **0,78** bp; swap 0 — **session-flat**).  
**Track 4 + D-100 + D-097:** Gold uptrend as haven demand into the US cash session; intradag-vlak (geen swap). Not an XAU CFD own-leg.

**Gate:** 3 × US500 RT = 3 × 0,78 = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: GLD history from 2004 (≥5y); binding window is FTMO-M5 costs. Gold **level** inverse into US500 is not the silver/gold ratio, not platinum, not TIPS.

**Onderscheid:**
- ≠ **N113 SILVER_GOLD** FAIL_COST (ratio ≠ gold level)
- ≠ **N129 PPLT** / **N117 CPER** / **N122 DBC** (other metals/basket)
- ≠ **N118 TIP** FAIL_T (TIPS ETF ≠ gold ETF)
- ≠ **N131 DXY** FAIL_T / XAU CFD intradag set
- ≠ N75–N132 clones / thr-grid / soft gate / overnight

## Regel
**Signal (dag t):**
1. `z120 = (GLD_t − mean_120(GLD)) / stdev_120(GLD)`; `d20 = GLD_t / GLD_{t−20} − 1`.
2. **haven (inverse):** `(z120 > +0,5) and (d20 > 0)` → **SHORT** US500; `(z120 < −0,5) and (d20 < 0)` → **LONG**; else skip.

**Execution (dag t+1, US500cash) — D-100 session-flat:**
3. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
4. Exit: flat ≤ **21:00 CET** same day. **No overnight.**
5. Non-overlapping (≤1/day).

## Pre-screen
- Data: `data/daily/GLD.csv` + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Result: `results/R2/n132_n133_prescreen/` — **FAIL** (N=361, +0,26 < 2,34).
- STOP (geen GLD/GOLD rewrite, geen SILVER_GOLD/PPLT/CPER/DBC/TIP twin, geen thr-grid, geen overnight, geen soft gate).
