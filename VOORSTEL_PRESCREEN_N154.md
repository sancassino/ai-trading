# VOORSTEL_PRESCREEN_N154 — US100_GER40_TRANSATLANTIC_XS session-flat (NEW_FAMILY BW)

**Status:** **geen PREREG — D-092.1 FAIL** `n154_n155` (2026-10-03 ~01:41 CEST). N=177, mean **−2,79 < 4,14**. Not a clone. No US100-only / GER-only / US–US / GER–UK / FX rewrite.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BW** (Nasdaq vs DAX **transatlantic cash-index basis**, two index CFDs, session-flat). Both round-trips are in `COSTS_FTMO.csv`. Not an FX book. Not a G10 cross. Not silver/index. Not metal–oil. Not an equity-factor z→US500.  
**Signal:** M5 day-close ratio **US100cash / GER40cash**. **Trade:** both legs, equal bp.  
**Track 4 + D-100:** US tech and the cash DAX dislocate when the New York growth complex has outrun, or lagged, European industrials. Flat inside 15:30→21:00 CET so neither overnight swap is the alpha.

**Gate (both in `COSTS_FTMO.csv`):** US100cash RT **0,66** + GER40cash RT **0,72** = **1,38** → gate 3 × 1,38 = **4,14** bp. Swap 0 (session-flat; overnight long-US100 is 1,95 and long-GER is 1,79 — a two-sided book cannot lock a receiving side). No single-leg cherry-pick.

**D-094a:** train 2021–2023. Reden **(b)**: both CFDs have M5 from 2021-01. Mechanism is a same-session index/index basis across the Atlantic, not a US cash pair, not GER/UK, and not a one-way Europe-morning lead into the US open. 2021 GER40 afternoon bars may be thin; that is a fill fact for the screen, not a reason to change the clock.

**Onderscheid:**
- ≠ **N152** GBP/NZD FAIL / **N153** EUR/CAD FAIL (G10 crosses exhausted this stretch; no FX leg)
- ≠ **N142** US30/US500 / **N81** US100/US500 (both legs here are not a US–US pair)
- ≠ **N138** GER/UK / EU50/UK (second leg is US100, not FTSE or EU50)
- ≠ **N103** GER Lon-AM→US30 lead-lag / **N149** EUR/GER40 (no FX leg; both legs are indices)
- ≠ **N150** silver/index / **N140–N141** metal–oil / **N143** XLE→US500 / any equity-factor z→US500
- ≠ **N155** US30/UKOIL (other OPEN; do not pool)

## Regel
**Signal (dag t, last M5 ≤ 22:00 CET on each leg):**
1. `ratio_t = US100_close_t / GER40_close_t`.
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)` (ddof=0).
3. **basis fade:** `z40 > +1,5` → **SHORT US100 + LONG GER40** (Nasdaq rich vs DAX); `z40 < −1,5` → **LONG US100 + SHORT GER40**; else skip. Threshold frozen — no grid.

**Execution (dag t+1) — D-100 session-flat, both legs:**
4. Entry: first M5 ≥ **15:30 CET** (span ≤15 min) on **each** leg. Either missing → skip day.
5. Exit: flat ≤ **21:00 CET** same day on both. **No overnight.**
6. PnL bp = sum of the two signed leg returns (equal weight). Non-overlapping (≤1 basket/day).

**Future clone bar (precommitted):** FAIL_CLONE if |z corr| vs US30/US500 z40 ≥ 0,90, or vs US100/US500 z40 ≥ 0,90, or vs GER40/UK100 z40 ≥ 0,90, or vs EUR/GER40 z40 ≥ 0,90, or (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N142, vs N81, vs N138, vs N103's GER day-sign, vs N149, or vs N155. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/US100cash.csv.gz` + `data/m5gz/GER40cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **4,14** bp, **N ≥ 150**.
- PASS → PREREG. FAIL → STOP (geen US100-only, geen GER-only, geen US–US remap, geen GER/UK remap, geen FX leg, geen factor→US500, geen thr-grid, geen overnight, geen soft gate).
