# VOORSTEL_PRESCREEN_N152 — GBPUSD_NZDUSD_CABLE_KIWI_XS session-flat (NEW_FAMILY BU)

**Status:** **OPEN** — D-092.1 refill after N150 FAIL_CLONE / N151 FAIL (filed 2026-10-03 ~01:29 CEST). Not screened this cycle.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BU** (sterling vs kiwi **cable–commodity basis**, two G10 CFDs, session-flat). Both round-trips are in `COSTS_FTMO.csv`. Not a silver/index book. Not an EURJPY/CHF book. Not GBPAUD, not AUDNZD, not EURNZD, not GBPJPY.  
**Signal:** M5 day-close ratio **GBPUSD / NZDUSD**. **Trade:** both legs, equal bp.  
**Track 4 + D-100:** cable and the kiwi dislocate when UK rates have outrun, or lagged, the commodity dollar. Flat inside 15:30→21:00 CET so neither overnight swap is the alpha.

**Gate (both in `COSTS_FTMO.csv`):** GBPUSD RT **0,70** + NZDUSD RT **1,85** = **2,55** → gate 3 × 2,55 = **7,65** bp. Swap 0 (session-flat; overnight long-GBP receives nothing material versus short-NZD, and a two-sided book cannot lock one receiving side). No single-leg cherry-pick.

**D-094a:** train 2021–2023. Reden **(b)**: both CFDs have M5 from 2021-01. Mechanism is a sterling/kiwi basis, not silver versus a cash index and not a yen-cross versus the Swiss franc.

**Onderscheid:**
- ≠ **N150** XAG/US30 FAIL_CLONE (silver/index; do not rewrite) / **N151** EURJPY/USDCHF FAIL (funding twin; do not rewrite)
- ≠ **N111** GBPAUD LO / **N84** AUDNZD / **N106** EURNZD LO / **N90** GBPJPY LO / **N94** NZDJPY LO
- ≠ **N146** AUD/XAU / **N147** GBP/UKOIL / **N148** USDJPY/US100 / **N149** EUR/GER40
- ≠ **N153** EUR/CAD (other OPEN; do not pool)

## Regel
**Signal (dag t, last M5 ≤ 22:00 CET on each leg):**
1. `ratio_t = GBP_close_t / NZD_close_t`.
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)` (ddof=0).
3. **basis fade:** `z40 > +1,5` → **SHORT GBP + LONG NZD** (cable rich vs kiwi); `z40 < −1,5` → **LONG GBP + SHORT NZD**; else skip. Threshold frozen — no grid.

**Execution (dag t+1) — D-100 session-flat, both legs:**
4. Entry: first M5 ≥ **15:30 CET** (span ≤15 min) on **each** leg. Either missing → skip day.
5. Exit: flat ≤ **21:00 CET** same day on both. **No overnight.**
6. PnL bp = sum of the two signed leg returns (equal weight). Non-overlapping (≤1 basket/day).

**Future clone bar (precommitted):** FAIL_CLONE if |z corr| vs GBP/AUD z40 ≥ 0,90, or vs AUD/NZD z40 ≥ 0,90, or vs EUR/NZD z40 ≥ 0,90, or vs XAG/US30 z40 ≥ 0,90, or vs EURJPY/USDCHF z40 ≥ 0,90, or (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N111's GBP day-sign, vs N84, vs N106, vs N90's GBP day-sign, vs N94, or vs N153. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/GBPUSD.csv.gz` + `data/m5gz/NZDUSD.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **7,65** bp, **N ≥ 150**.
- PASS → PREREG. FAIL → STOP (geen GBP-only, geen NZD-only, geen GBPAUD remap, geen silver/index, geen EURJPY/CHF, geen thr-grid, geen overnight, geen soft gate).
