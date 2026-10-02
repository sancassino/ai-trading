# VOORSTEL_PRESCREEN_N149 — EURUSD_GER40_EUROPE_XS session-flat (NEW_FAMILY BR)

**Status:** **OPEN** — D-092.1 refill after N146 FAIL / N147 FAIL_CLONE (filed 2026-10-03 ~01:18 CEST). Not screened this cycle.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BR** (euro vs DAX **Europe-local basis**, two CFDs, session-flat). Both round-trips are in `COSTS_FTMO.csv`. Not an FX/metal twin of N146. Not an FX/oil twin of N147. Not a GER/UK index pair and not GER→US30 lead-lag.  
**Signal:** M5 day-close ratio **EURUSD / GER40cash**. **Trade:** both legs, equal bp.  
**Track 4 + D-100:** the euro and the cash DAX dislocate when Europe's currency has outrun, or lagged, its own equity. Flat inside 15:30→21:00 CET so neither overnight swap is the alpha.

**Gate (both in `COSTS_FTMO.csv`):** EURUSD RT **0,63** + GER40cash RT **0,72** = **1,35** → gate 3 × 1,35 = **4,05** bp. Swap 0 (session-flat; overnight long-GER is 1,79 and long-EUR is 1,13). No single-leg cherry-pick.

**D-094a:** train 2021–2023. Reden **(b)**: both CFDs have M5 from 2021-01. Mechanism is a same-region currency/equity basis, not an index–index RV and not a single-name FX fade.

**Onderscheid:**
- ≠ **N146** AUD/XAU / **N147** GBP/UKOIL (FX/commodity twins; do not rewrite)
- ≠ **N138** GER40/UK100 FAIL_CLONE / **N142** US30/US500 / **N81** US pair — one leg here is EURUSD, not a second index
- ≠ **N103** GER Lon-AM→US30 (one US destination, lead-lag) / **N21** GER afternoon fade / **N40** GER mid-morning
- ≠ **N148** USDJPY/US100 (other OPEN; do not pool) / D-098 single-name EUR / L60 FX-med
- ≠ **N144** PGM / **N145** crypto / **N143** XLE–DBC / metal–oil / XAU Lon→NY

## Regel
**Signal (dag t, last M5 ≤ 22:00 CET on each leg):**
1. `ratio_t = EUR_close_t / GER40_close_t`.
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)` (ddof=0).
3. **basis fade:** `z40 > +1,5` → **SHORT EUR + LONG GER40** (euro rich vs DAX); `z40 < −1,5` → **LONG EUR + SHORT GER40**; else skip. Threshold frozen — no grid.

**Execution (dag t+1) — D-100 session-flat, both legs:**
4. Entry: first M5 ≥ **15:30 CET** (span ≤15 min) on **each** leg. Either missing → skip day.
5. Exit: flat ≤ **21:00 CET** same day on both. **No overnight.**
6. PnL bp = sum of the two signed leg returns (equal weight). Non-overlapping (≤1 basket/day).

**Future clone bar (precommitted):** FAIL_CLONE if |z corr| vs GER40/UK100 z40 ≥ 0,90, or vs USDJPY/US100 z40 ≥ 0,90, or vs US30/US500 z40 ≥ 0,90, or (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N138, vs N103's GER day-sign, vs N142, or vs N148. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/EURUSD.csv.gz` + `data/m5gz/GER40cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **4,05** bp, **N ≥ 150**.
- PASS → PREREG. FAIL → STOP (geen EUR-only, geen GER-only, geen UK100 twin, geen US30 remap, geen FX/metal, geen FX/oil, geen thr-grid, geen overnight, geen soft gate).
