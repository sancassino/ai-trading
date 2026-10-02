# VOORSTEL_PRESCREEN_N157 — XAU_US100_HAVEN_NASDAQ_XS session-flat (NEW_FAMILY BZ)

**Status:** **geen PREREG — D-092.1 FAIL** `n156_n157` (2026-10-03 ~01:47 CEST). N=174, mean **−1,82 < 4,47**. Not a twin of N156 (z 0,68, agree 1,00, cover 0,55). Not N92 (agree 0,38) or N148 (cover 0,47). No XAU-only / US100-only / gold–index rewrite.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BZ** (bullion vs Nasdaq **haven–growth basis**, one metal CFD and one index CFD, session-flat). Both round-trips are in `COSTS_FTMO.csv`. Not an FX book. Not a G10 cross. Not silver/index (gold, not silver). Not metal–oil. Not an equity-factor z→US500 (both legs; Nasdaq, not a factor ETF into the S&P).  
**Signal:** M5 day-close ratio **XAUUSD / US100cash**. **Trade:** both legs, equal bp.  
**Track 4 + D-100:** gold and the Nasdaq dislocate when the haven has outrun, or lagged, US growth equities. Flat inside 15:30→21:00 CET. Overnight long-XAU is 2,15 and long-US100 is 1,95; a two-sided book cannot lock a receiving side, so swap in the gate is 0.

**Gate (both in `COSTS_FTMO.csv`):** XAUUSD RT **0,83** + US100cash RT **0,66** = **1,49** → gate 3 × 1,49 = **4,47** bp. Swap 0. No single-leg cherry-pick. No US100-only NY-2h.

**D-094a:** train 2021–2023. Reden **(b)**: both CFDs have M5 from 2021-01. Mechanism is bullion versus the Nasdaq cash index, not yen versus the Nasdaq, not Nasdaq versus the S&P, and not a one-way gold ETF into US500.

**Onderscheid:**
- ≠ **N156** XAU/GER40 (other OPEN; second leg is US100, not the DAX; do not pool)
- ≠ **N154** US100/GER40 (first leg is XAU, not another index)
- ≠ **N148** USDJPY/US100 (no FX leg)
- ≠ **N81** US100/US500 / **N92** US100 NY-2h / **N142** US30/US500 (not an index/index or a one-way Nasdaq momentum)
- ≠ **N150** XAG/US30 / **N113** SLV/GLD→US500 (gold, not silver; not a one-way into US500)
- ≠ **N133** GLD→US500 (Nasdaq, not US500; both legs)
- ≠ **N140–N141** metal–oil / **N155** US30/UKOIL (no oil leg)
- ≠ **N146** AUD/XAU / **N75** XAU/XAG (no FX; second leg is not silver)

## Regel
**Signal (dag t, last M5 ≤ 22:00 CET on each leg):**
1. `ratio_t = XAU_close_t / US100_close_t`.
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)` (ddof=0).
3. **basis fade:** `z40 > +1,5` → **SHORT XAU + LONG US100** (bullion rich vs Nasdaq); `z40 < −1,5` → **LONG XAU + SHORT US100**; else skip. Threshold frozen — no grid.

**Execution (dag t+1) — D-100 session-flat, both legs:**
4. Entry: first M5 ≥ **15:30 CET** (span ≤15 min) on **each** leg. Either missing → skip day.
5. Exit: flat ≤ **21:00 CET** same day on both. **No overnight.**
6. PnL bp = sum of the two signed leg returns (equal weight). Non-overlapping (≤1 basket/day).

**Future clone bar (precommitted):** FAIL_CLONE if |z corr| vs XAU/GER40 z40 ≥ 0,90, or vs USDJPY/US100 z40 ≥ 0,90, or vs US100/US500 z40 ≥ 0,90, or vs US100/GER40 z40 ≥ 0,90, or vs XAG/US30 z40 ≥ 0,90, or vs XAU/XAG z40 ≥ 0,90, or (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N156, vs N148, vs N81, vs N92's US100 day-sign, vs N154, vs N150, vs N133's gold day-sign, vs N75, or vs N146. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/XAUUSD.csv.gz` + `data/m5gz/US100cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **4,47** bp, **N ≥ 150**.
- PASS → PREREG. FAIL → STOP (geen XAU-only, geen US100-only, geen XAU/GER remap, geen FX leg, geen silver/index, geen metal–oil, geen factor→US500, geen thr-grid, geen overnight, geen soft gate).
