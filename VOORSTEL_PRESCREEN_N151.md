# VOORSTEL_PRESCREEN_N151 — EURJPY_USDCHF_FUNDING_XS session-flat (NEW_FAMILY BT)

**Status:** **geen PREREG — D-092.1 FAIL** `n150_n151` (N=221, mean **−0,60 < 6,33**; med −1,49; years +1,21 / +4,69 / −5,43; L/S 77/144; 0 missing bars). Not the inline USDCHF/USDJPY book (z **−0,66**, agree **0,02**, cover 0,55). Not L60 (EURJPY agree 0,22 cover 0,78; USDCHF agree 0,53 cover 0,48), not EURNZD-LO (agree 0,31 cover 0,53), not AUDCAD-LO (agree 0,23 cover 0,41), not N28 (agree 0,36 cover 0,25). Screened 2026-10-03 ~01:29 CEST. NEW_FAMILY BT dead; no EURJPY-only, no USDCHF-only, no EURJPY/CHF twin.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BT** (yen-cross vs Swiss **funding basis**, two G10 CFDs, session-flat). Both round-trips are in `COSTS_FTMO.csv`. Not an FX/index twin of N148 or N149. Not the dead inline USDCHF/USDJPY pair. Not L60 FX-med. Not a single-name EURJPY or USDCHF fade.  
**Signal:** M5 day-close ratio **EURJPY / USDCHF**. **Trade:** both legs, equal bp.  
**Track 4 + D-100:** the euro-yen cross and the dollar-swiss dislocate when one funding pair has outrun the other. Flat inside 15:30→21:00 CET so neither overnight swap is the alpha.

**Gate (both in `COSTS_FTMO.csv`):** EURJPY RT **1,10** + USDCHF RT **1,01** = **2,11** → gate 3 × 2,11 = **6,33** bp. Swap 0 (session-flat; overnight long-EURJPY receives 0,11 but short-EURJPY costs 0,69; long-USDCHF receives 0,39 but short-USDCHF costs 2,17 — a two-sided book cannot lock the receiving side). No single-leg cherry-pick.

**D-094a:** train 2021–2023. Reden **(b)**: both CFDs have M5 from 2021-01. Mechanism is a funding-pair basis, not a currency vs an equity index and not a long-only 60-day FX hold.

**Onderscheid:**
- ≠ **N148** USDJPY/US100 / **N149** EUR/GER40 (FX/index; do not rewrite)
- ≠ inline **USDCHF/USDJPY** FAIL_CLONE (do not rescreen; this book has EURJPY, not USDJPY)
- ≠ **USDJPY_MED / EURJPY_MED / N72–N74** L60 FX-med (closed)
- ≠ **N28** EURJPY Lon→NY continuation / **N47** USDCHF Asia→Lon (single-name impulse, not a two-leg basis)
- ≠ **N77** FX6 rank-reversal / **N84** AUDNZD / **N150** XAG/US30 (other OPEN; do not pool)
- ≠ **N146** FX/metal / **N147** FX/oil

## Regel
**Signal (dag t, last M5 ≤ 22:00 CET on each leg):**
1. `ratio_t = EURJPY_close_t / USDCHF_close_t`.
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)` (ddof=0).
3. **basis fade:** `z40 > +1,5` → **SHORT EURJPY + LONG USDCHF** (yen-cross rich vs Swiss); `z40 < −1,5` → **LONG EURJPY + SHORT USDCHF**; else skip. Threshold frozen — no grid.

**Execution (dag t+1) — D-100 session-flat, both legs:**
4. Entry: first M5 ≥ **15:30 CET** (span ≤15 min) on **each** leg. Either missing → skip day.
5. Exit: flat ≤ **21:00 CET** same day on both. **No overnight.**
6. PnL bp = sum of the two signed leg returns (equal weight). Non-overlapping (≤1 basket/day).

**Future clone bar (precommitted):** FAIL_CLONE if |z corr| vs USDCHF/USDJPY z40 ≥ 0,90, or vs USDJPY/US100 z40 ≥ 0,90, or vs EUR/GER40 z40 ≥ 0,90, or (sign agree ≥ 0,85 AND cover ≥ 0,70) vs the inline USDCHF/USDJPY book, vs N28's EURJPY day-sign, vs USDJPY L60, vs N148, or vs N150. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/EURJPY.csv.gz` + `data/m5gz/USDCHF.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **6,33** bp, **N ≥ 150**.
- PASS → PREREG. FAIL → STOP (geen EURJPY-only, geen USDCHF-only, geen USDJPY remap, geen L60, geen FX/index, geen thr-grid, geen overnight, geen soft gate).
