# VOORSTEL_PRESCREEN_N153 — EURUSD_USDCAD_ATLANTIC_XS session-flat (NEW_FAMILY BV)

**Status:** **OPEN** — D-092.1 refill after N150 FAIL_CLONE / N151 FAIL (filed 2026-10-03 ~01:29 CEST). Not screened this cycle.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BV** (euro vs Canadian dollar **Atlantic basis**, two G10 CFDs, session-flat). Both round-trips are in `COSTS_FTMO.csv`. Not a silver/index book. Not an EURJPY/CHF book. Not AUDCAD, not CADCHF, not EURGBP, not EURNZD.  
**Signal:** M5 day-close ratio **EURUSD / USDCAD**. **Trade:** both legs, equal bp.  
**Track 4 + D-100:** the euro and the loonie dislocate when European rates have outrun, or lagged, the oil-linked dollar. Flat inside 15:30→21:00 CET so neither overnight swap is the alpha.

**Gate (both in `COSTS_FTMO.csv`):** EURUSD RT **0,63** + USDCAD RT **0,80** = **1,43** → gate 3 × 1,43 = **4,29** bp. Swap 0 (session-flat; overnight long-EUR costs 1,13 and short-CAD costs 0,98 — a two-sided book cannot lock a receiving side). No single-leg cherry-pick.

**D-094a:** train 2021–2023. Reden **(b)**: both CFDs have M5 from 2021-01. Mechanism is an euro/loonie basis, not silver versus a cash index and not a yen-cross versus the Swiss franc. EURCAD itself is not in `COSTS_FTMO.csv`; the gate uses the two listed legs.

**Onderscheid:**
- ≠ **N150** XAG/US30 FAIL_CLONE / **N151** EURJPY/USDCHF FAIL (do not rewrite either)
- ≠ **N97** AUDCAD LO / **N99** CADCHF LO / **N73** USDCAD L60 / **N106** EURNZD LO
- ≠ **N88** EURGBP SO / **N46** EURGBP fix fade / **N149** EUR/GER40 FX/index
- ≠ **N152** GBP/NZD (other OPEN; do not pool)
- ≠ **N136** Brent–WTI / **N147** GBP/UKOIL (oil books; this book has no crude leg)

## Regel
**Signal (dag t, last M5 ≤ 22:00 CET on each leg):**
1. `ratio_t = EUR_close_t / CAD_close_t`.
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)` (ddof=0).
3. **basis fade:** `z40 > +1,5` → **SHORT EUR + LONG CAD** (euro rich vs loonie); `z40 < −1,5` → **LONG EUR + SHORT CAD**; else skip. Threshold frozen — no grid.

**Execution (dag t+1) — D-100 session-flat, both legs:**
4. Entry: first M5 ≥ **15:30 CET** (span ≤15 min) on **each** leg. Either missing → skip day.
5. Exit: flat ≤ **21:00 CET** same day on both. **No overnight.**
6. PnL bp = sum of the two signed leg returns (equal weight). Non-overlapping (≤1 basket/day).

**Future clone bar (precommitted):** FAIL_CLONE if |z corr| vs AUD/CAD z40 ≥ 0,90, or vs EUR/GBP z40 ≥ 0,90, or vs CAD/CHF z40 ≥ 0,90, or vs EUR/GER40 z40 ≥ 0,90, or vs EURJPY/USDCHF z40 ≥ 0,90, or vs XAG/US30 z40 ≥ 0,90, or (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N97, vs N99, vs USDCAD L60, vs EURNZD-LO, vs N88, vs N149, or vs N152. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/EURUSD.csv.gz` + `data/m5gz/USDCAD.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **4,29** bp, **N ≥ 150**.
- PASS → PREREG. FAIL → STOP (geen EUR-only, geen CAD-only, geen AUDCAD remap, geen silver/index, geen EURJPY/CHF, geen thr-grid, geen overnight, geen soft gate).
