# VOORSTEL_PRESCREEN_N130 — EQW_BREADTH_STRESS → US500cash session-flat (NEW_FAMILY AY)

**Status:** **PASS → PREREG** — D-092.1 `n130_n131` train N=**220** mean bruto **+6,68** ≥ gate **2,34** (stress informal ≥3,51; med +1,66; years −0,41/+18,72/−1,71; L/S 99/121); screened 2026-10-03 ~00:17 CEST. Live: `PREREG_FTMO_N130_EQW_BREADTH_STRESS.md`.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY AY** (US **equal-weight vs cap-weight breadth ratio** stress → equity session-flat — participation/concentration channel; **≠ IWM** small-cap level / **≠ SECTOR_DISP** / **≠ DEFENSIVE_CYCLICAL** XLU/XLI / **≠ N81** US100/US500 pair RV overnight).  
**Signal:** Yahoo/proxy **SPX_EQW** (RSP) / **SPX**. **Trade:** `US500cash` (RT **0,78** bp; swap 0 — **session-flat**).  
**Track 4 + D-100 + D-097 XS:** Breadth extremes as crowded participation vs mega-cap concentration timing for the US cash session; intradag-vlak.

**Gate:** 3 × US500 RT = 3 × 0,78 = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: the **ratio** RSP/SPX is a breadth factor, not an equity-ETF level (IWM N119), not sector rotation (N93/N125), not a 3-day index-pair RV with overnight swap (N81). FTMO-M5 for costs.

**Onderscheid:**
- ≠ **N119 IWM** D-092.1 FAIL (small-cap ETF level ≠ EQW/SPX ratio)
- ≠ **N93 SECTOR_DISP** / **N125 DEFENSIVE_CYCLICAL** FAIL_T (sector rotation / XLU-XLI ≠ breadth ratio)
- ≠ **N81** pair RV DIAG_FAIL (US100/US500 3d overnight ≠ session-flat breadth)
- ≠ **N127 EWZ** / EEM / EFA / BWX / TLT / TIP / HYG / VIX
- ≠ N75–N129 clones / thr-grid / soft gate / overnight US100

## Regel
**Signal (dag t):**
1. `ratio_t = SPX_EQW_t / SPX_t` (adjclose).
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)`.
3. **stress_buy:** `z40 > +1,5` → **SHORT** US500 (breadth blow-off); `z40 < −1,5` → **LONG** (breadth washout); else skip.

**Execution (dag t+1, US500cash) — D-100 session-flat:**
4. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
5. Exit: flat ≤ **21:00 CET** same day. **No overnight.**
6. Non-overlapping (≤1/day).

## Pre-screen
- Data: `data/daily/SPX_EQW.csv` + `data/daily/SPX.csv` + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **2,34** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N130. FAIL → STOP (geen IWM rewrite, geen SECTOR_DISP/XLU-XLI twin, geen thr-grid, geen overnight, geen soft gate).
