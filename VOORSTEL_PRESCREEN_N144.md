# VOORSTEL_PRESCREEN_N144 — XPT_XPD_PGM_XS session-flat (NEW_FAMILY BM)

**Status:** **geen PREREG — D-092.1 FAIL** `n144_n145` (N=228, mean **−0,69 < 205,06**; med +14,57; years −10,45 / −21,07 / +27,30; L/S 71/157). Honest gate **205,06** = 3×(XPT RT 24,02 + XPD RT 44,33): all-hours spread medians 23,63 / 43,94 (the stated 202,71) plus €2/lot/side. Mean also **< stated 202,71**. Not a clone of XAU/XAG (z −0,06, agree 0,55, cover 0,32), XAU/UKOIL (z 0,12, agree 0,62, cover 0,43), PPLT (z 0,10), GLD (z 0,05), N75 (agree 0,29, cover 0,20), N113 (agree 0,47, cover 0,58), or N145 (z 0,04). M5 train days 773/773 (symbol_history D1 for XPT is 0 bars — not used; not DIAG). Screened 2026-10-03 ~01:13 CEST. NEW_FAMILY BM dead; no PPLT→US500, no XAU/XAG, no metal–oil.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BM** (platinum vs palladium **PGM cash basis**, two metal CFDs, session-flat). **D-097** metals book that is **not** an equity-factor z→US500 and **not** a metal–oil twin.  
**Signal:** M5 day-close ratio **XPTUSD / XPDUSD**. **Trade:** both legs, equal bp.  
**Track 4 + D-100:** the platinum/palladium basis mean-reverts when autocatalyst palladium is rich or cheap versus platinum. Flat inside 15:30→21:00 CET so neither overnight swap is the alpha. The clock is the swap-flat window, not a US-cash lead-lag.

**Gate (both NOT in `COSTS_FTMO.csv`; estimator checked on US500 → 0,78 bp):** all-hours M5 spread median 2024-01-01…2026-09-30, `bp = spread_points × point / close × 1e4`, commission **not** in COSTS (spread-only est.).  
XPT **23,63** + XPD **43,94** = **67,57** → gate 3 × 67,57 = **202,71** bp.  
(Session 15:30–21:00 medians not used.) Swap 0. Binding RT = max(est, U2) on **each** leg before any PREREG. No single-leg cherry-pick.

**D-094a:** train 2021–2023. Reden **(b)**: both PGM CFDs have M5 from 2021-01-04. Mechanism is an industrial precious-metal basis, not gold/silver, not crude, and not an ETF stress into US500.

**Onderscheid:**
- ≠ **N142** US30/US500 FAIL (−1,68 < 3,69; not an index clone) / **N143** XLE FAIL_CLONE of DBC (no commodity-ETF→US500 rewrite)
- ≠ **N75** XAU/XAG ratio / **N113** SLV/GLD→US500 / **N133** GLD haven / **N129** PPLT→US500
- ≠ **N140/N141** XAU/XAG–UKOIL (metal–oil dead) / inline USDCHF/USDJPY twin (do not rescreen)
- ≠ **N145** BTC/ETH crypto basis (other OPEN; do not pool)
- ≠ **N136** Brent–WTI / **N138** GER/UK / **N139** JP/HK / **N137** USDMXN
- ≠ equity-factor z→US500 (EQW, DXY, BWX, EWZ, MTUM, XLF, QUAL, XLE, DBC) / thr-grid / overnight

## Regel
**Signal (dag t, last M5 ≤ 22:00 CET on each leg):**
1. `ratio_t = XPT_close_t / XPD_close_t`.
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)` (ddof=0).
3. **basis fade:** `z40 > +1,5` → **SHORT XPT + LONG XPD** (platinum rich); `z40 < −1,5` → **LONG XPT + SHORT XPD**; else skip. Threshold frozen — no grid.

**Execution (dag t+1) — D-100 session-flat, both legs:**
4. Entry: first M5 ≥ **15:30 CET** (span ≤15 min) on **each** leg. Either missing → skip day.
5. Exit: flat ≤ **21:00 CET** same day on both. **No overnight.**
6. PnL bp = sum of the two signed leg returns (equal weight). Non-overlapping (≤1 basket/day).

**Future clone bar (precommitted):** FAIL_CLONE if |z corr| vs XAU/XAG z40 ≥ 0,90, or vs XAU/UKOIL z40 ≥ 0,90, or vs PPLT z40 ≥ 0,90, or vs GLD z40 ≥ 0,90, or (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N75, vs N140, vs N113, or vs N145. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/XPTUSD.csv.gz` + `data/m5gz/XPDUSD.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **202,71** bp, **N ≥ 150**.
- PASS → PREREG only after U2 confirms each RT (binding = max(est, U2)). FAIL → STOP (geen XAU/XAG rewrite, geen PPLT→US500, geen oil leg, geen single-leg XPD, geen thr-grid, geen overnight, geen soft gate).
