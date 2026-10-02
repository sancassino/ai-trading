# VOORSTEL_PRESCREEN_N134 — XLF_FINANCIAL_STRESS → US500cash session-flat (NEW_FAMILY BC)

**Status:** **OPEN** — D-094 refill after N132/N133 D-092.1 FAIL + N130/N131 FAIL_T (filed 2026-10-03 ~00:24 CEST). Not screened this cycle.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BC** (US **financial-sector equity level** stress → equity session-flat — bank/broker balance-sheet channel; **≠ HYG** credit ETF / **≠ EMB** / **≠ SECTOR_DISP** XL* dispersion / **≠ XLU/XLI** ratio / **≠ MTUM** momentum factor).  
**Signal:** Yahoo/proxy **XLF**. **Trade:** `US500cash` (RT **0,78** bp; swap 0 — **session-flat**).  
**Track 4 + D-100 + D-097:** Financials lead the cash session when bank equity is stretched or washed out; intradag-vlak.

**Gate:** 3 × US500 RT = 3 × 0,78 = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: XLF history from 1998 (≥5y); binding window is FTMO-M5 costs. A single financials **level** is not a credit-bond ETF, not cross-sectional sector dispersion, and not the utilities/industrials ratio.

**Onderscheid:**
- ≠ **N114 HYG** / **N100 EMB** / LQD (bond credit ≠ bank equity)
- ≠ **N93 SECTOR_DISP** (XL* dispersion → US100 ≠ XLF level → US500)
- ≠ **N125 DEFENSIVE_CYCLICAL** XLU/XLI ratio
- ≠ **N132 MTUM** FAIL / **N130 EQW** FAIL_T
- ≠ N75–N133 clones / thr-grid / soft gate / overnight US100

## Regel
**Signal (dag t):**
1. `z40 = (XLF_t − mean_40(XLF)) / stdev_40(XLF)`.
2. **stress_buy:** `z40 > +1,5` → **SHORT** US500 (financials blow-off); `z40 < −1,5` → **LONG** (financials washout); else skip.

**Execution (dag t+1, US500cash) — D-100 session-flat:**
3. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
4. Exit: flat ≤ **21:00 CET** same day. **No overnight.**
5. Non-overlapping (≤1/day).

## Pre-screen
- Data: `data/daily/XLF.csv` + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **2,34** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N134. FAIL → STOP (geen HYG/EMB rewrite, geen SECTOR_DISP/XLU-XLI twin, geen thr-grid, geen overnight, geen soft gate).
