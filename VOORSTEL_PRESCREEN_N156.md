# VOORSTEL_PRESCREEN_N156 — XAU_GER40_HAVEN_DAX_XS session-flat (NEW_FAMILY BY)

**Status:** **geen PREREG — D-092.1 FAIL** `n156_n157` (2026-10-03 ~01:47 CEST). N=146, mean **−2,46 < 4,65** (also N<150). Not a clone of N95 / N146 / N140 / N133 / N149 / N157 (cover 0,57). No XAU-only / GER-only / gold–index / FX / oil rewrite.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BY** (bullion vs cash DAX **haven–Europe basis**, one metal CFD and one index CFD, session-flat). Both round-trips are in `COSTS_FTMO.csv`. Not an FX book. Not a G10 cross. Not silver/index (gold, not silver; DAX, not a US500 factor). Not metal–oil. Not an equity-factor z→US500.  
**Signal:** M5 day-close ratio **XAUUSD / GER40cash**. **Trade:** both legs, equal bp.  
**Track 4 + D-100:** gold and the cash DAX dislocate when the bullion haven has outrun, or lagged, European equities. Flat inside 15:30→21:00 CET so neither overnight swap is the alpha.

**Gate (both in `COSTS_FTMO.csv`):** XAUUSD RT **0,83** + GER40cash RT **0,72** = **1,55** → gate 3 × 1,55 = **4,65** bp. Swap 0 (session-flat; overnight long-XAU is 2,15 and long-GER is 1,79 — a two-sided book cannot lock a receiving side). No single-leg cherry-pick.

**D-094a:** train 2021–2023. Reden **(b)**: both CFDs have M5 from 2021-01. Mechanism is bullion versus the cash DAX, not Nasdaq versus the DAX, not EUR versus the DAX, and not a one-way gold ETF into the S&P.

**Onderscheid:**
- ≠ **N154** US100/GER40 FAIL (first leg is XAU, not US100; no transatlantic index remap)
- ≠ **N149** EUR/GER40 (no FX leg)
- ≠ **N150** XAG/US30 silver/index / **N113** SLV/GLD→US500 (gold, not silver; both legs; not a one-way into US500)
- ≠ **N133** GLD→US500 (DAX, not US500; both legs traded)
- ≠ **N140** XAU/UKOIL / **N141** XAG/UKOIL / **N155** US30/UKOIL (no oil leg)
- ≠ **N146** AUD/XAU / **N75** XAU/XAG (no FX leg; second leg is an index, not silver)
- ≠ **N138** GER/UK / **N142** US30/US500 (not an index/index pair)
- ≠ **N157** XAU/US100 (other OPEN; do not pool)

## Regel
**Signal (dag t, last M5 ≤ 22:00 CET on each leg):**
1. `ratio_t = XAU_close_t / GER40_close_t`.
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)` (ddof=0).
3. **basis fade:** `z40 > +1,5` → **SHORT XAU + LONG GER40** (bullion rich vs DAX); `z40 < −1,5` → **LONG XAU + SHORT GER40**; else skip. Threshold frozen — no grid.

**Execution (dag t+1) — D-100 session-flat, both legs:**
4. Entry: first M5 ≥ **15:30 CET** (span ≤15 min) on **each** leg. Either missing → skip day.
5. Exit: flat ≤ **21:00 CET** same day on both. **No overnight.**
6. PnL bp = sum of the two signed leg returns (equal weight). Non-overlapping (≤1 basket/day).

**Future clone bar (precommitted):** FAIL_CLONE if |z corr| vs US100/GER40 z40 ≥ 0,90, or vs XAG/US30 z40 ≥ 0,90, or vs XAU/UKOIL z40 ≥ 0,90, or vs XAU/XAG z40 ≥ 0,90, or vs XAU/US100 z40 ≥ 0,90, or (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N154, vs N149, vs N150, vs N133's gold day-sign, vs N140, vs N75, vs N146, or vs N157. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/XAUUSD.csv.gz` + `data/m5gz/GER40cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **4,65** bp, **N ≥ 150**.
- PASS → PREREG. FAIL → STOP (geen XAU-only, geen GER-only, geen US100/GER remap, geen silver/index, geen metal–oil, geen FX leg, geen factor→US500, geen thr-grid, geen overnight, geen soft gate).
