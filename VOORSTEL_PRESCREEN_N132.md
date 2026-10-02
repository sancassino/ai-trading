# VOORSTEL_PRESCREEN_N132 — MTUM_MOM_FACTOR_STRESS → US500cash session-flat (NEW_FAMILY BA)

**Status:** **geen PREREG — D-092.1 FAIL** — `n132_n133` train N=**185** mean bruto **+1,55** < gate **2,34** (med −0,52; years +11,52/−6,45/+4,90; L/S 106/79); screened 2026-10-03 ~00:23 CEST. Dead screen; no MTUM/momentum-factor clone.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BA** (US **cross-sectional momentum factor** ETF stress → equity session-flat — momentum-crash channel; **≠ EQW** breadth ratio / **≠ IWM** small-cap level / **≠ SECTOR_DISP** / **≠ XLU/XLI**).  
**Signal:** Yahoo/proxy **MTUM**. **Trade:** `US500cash` (RT **0,78** bp; swap 0 — **session-flat**).  
**Track 4 + D-100 + D-097:** Momentum-factor extremes as crowded trend participation timing the US cash session; intradag-vlak.

**Gate:** 3 × US500 RT = 3 × 0,78 = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: MTUM history from 2013 (≥5y) but the binding window is FTMO-M5 costs. Momentum-factor **level** is not the RSP/SPX breadth ratio (N130), not IWM, not sector rotation.

**Onderscheid:**
- ≠ **N130 EQW** FAIL_T (breadth ratio ≠ momentum ETF level)
- ≠ **N119 IWM** / **N93 SECTOR_DISP** / **N125 XLU-XLI**
- ≠ **N131 DXY** / GLD / TLT / TIP / HYG
- ≠ N75–N131 clones / thr-grid / soft gate / overnight US100

## Regel
**Signal (dag t):**
1. `z40 = (MTUM_t − mean_40(MTUM)) / stdev_40(MTUM)`.
2. **stress_buy:** `z40 > +1,5` → **SHORT** US500 (momentum blow-off); `z40 < −1,5` → **LONG** (momentum washout); else skip.

**Execution (dag t+1, US500cash) — D-100 session-flat:**
3. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
4. Exit: flat ≤ **21:00 CET** same day. **No overnight.**
5. Non-overlapping (≤1/day).

## Pre-screen
- Data: `data/daily/MTUM.csv` + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Result: `results/R2/n132_n133_prescreen/` — **FAIL** (N=185, +1,55 < 2,34).
- STOP (geen MTUM rewrite, geen EQW/IWM/sector twin, geen thr-grid, geen overnight, geen soft gate).
