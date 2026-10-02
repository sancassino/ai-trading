# VOORSTEL_PRESCREEN_N142 — US30_US500_XS session-flat (NEW_FAMILY BK)

**Status:** **DIAG_FAIL** (CTO **C-041** 2026-10-03 ~01:03 CEST). N=187 mean bruto **−1.681** < gate **3.69**; day_t≈−0.71; years −0.45/+0.36/−4.59; L/S 101/86. No PREREG. Original OPEN filed 2026-10-03 ~00:55 CEST.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BK** (Dow vs S&P **cash-index basis**, two index CFDs, session-flat). **≠ N140/N141** metal–oil (dead this cycle) / **≠ N143** XLE→US500 (signal is a sector ETF level, trade is one leg) / **≠ N81** US100/US500 3d RV / **≠ N138** GER/UK / **≠ IDX_SHORT** same-direction TSMOM / **≠ N87** US30 gap-fade.  
**Signal:** M5 day-close ratio **US30cash / US500cash**. **Trade:** both legs, equal bp.  
**Track 4 + D-100:** the industrial-vs-broad basis mean-reverts when the Dow is rich or cheap versus the S&P. Flat inside the US cash session so neither overnight swap is the alpha.

**Gate (both in `COSTS_FTMO.csv`):** US30 RT **0,45** + US500 RT **0,78** = **1,23** → gate 3 × 1,23 = **3,69** bp. Swap 0 (session-flat). No single-leg cherry-pick.

**D-094a:** train 2021–2023. Reden **(b)**: both index CFDs have M5 from 2021-01. Mechanism is a US cash-index basis, not a precious-vs-oil spread and not an energy-equity stress into one index.

**Onderscheid:**
- ≠ **N140** XAU/UKOIL FAIL (+4,72 < 10,62) / **N141** XAG/UKOIL FAIL_CLONE (agree 1,00 cover 0,73)
- ≠ inline **USDCHF/USDJPY** substitute FAIL_CLONE (do not rescreen; D-098 intradag FX)
- ≠ **N81** US100/US500 pair RV DIAG_FAIL (clone bar below is binding)
- ≠ **N138** GER/UK FAIL_CLONE / **EU50/UK** / **N139** JP/HK
- ≠ **N143** XLE_ENERGY_EQUITY_STRESS (S2 slot; different signal and one trade leg)
- ≠ **IDX_SHORT** / **N87** gap-fade / **N32** IB breakout / N75–N141 thr-grid / overnight

## Regel
**Signal (dag t, last M5 ≤ 22:00 CET on each leg):**
1. `ratio_t = US30_close_t / US500_close_t`.
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)` (ddof=0).
3. **basis fade:** `z40 > +1,5` → **SHORT US30 + LONG US500** (Dow rich); `z40 < −1,5` → **LONG US30 + SHORT US500**; else skip. Threshold frozen — no grid.

**Execution (dag t+1) — D-100 session-flat, both legs:**
4. Entry: first M5 ≥ **15:30 CET** (span ≤15 min) on **each** leg. Either missing → skip day.
5. Exit: flat ≤ **21:00 CET** same day on both. **No overnight.**
6. PnL bp = sum of the two signed leg returns (equal weight). Non-overlapping (≤1 basket/day).

**Future clone bar (precommitted):** FAIL_CLONE if |z corr| vs US100/US500 ratio z40 ≥ 0,90, or vs GER40/UK100 ratio z40 ≥ 0,90, or vs XLE z40 ≥ 0,90, or (sign agree ≥ 0,85 AND cover ≥ 0,70) vs the US100/US500 z40 position, vs N138, or vs a same-sign US30+US500 TSMOM (IDX_SHORT). A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/US30cash.csv.gz` + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **3,69** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N142 (both RTs already in COSTS). FAIL → STOP (geen US100/US500 rewrite, geen GER/UK rewrite, geen XLE remap, geen single-leg US30, geen thr-grid, geen overnight, geen soft gate).
