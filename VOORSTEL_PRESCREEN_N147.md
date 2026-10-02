# VOORSTEL_PRESCREEN_N147 — GBP_UKOIL_PETRO_XS session-flat (NEW_FAMILY BP)

**Status:** **geen PREREG — D-092.1 FAIL_CLONE** `n146_n147` (N=188, mean **−3,22 < 10,23**; med +0,71; years −45,72 / +15,82 / −8,60; L/S 107/81; 231 signals, 43 skipped missing bar). Gate **10,23** = 3×(GBPUSD RT 0,70 + UKOIL RT 2,71), both in COSTS; swap 0. Clone of **N140 XAU/UKOIL** (z **0,92**, agree **1,00**, cover **0,81**). Not N136 (z 0,51, agree 0,96, cover 0,48), not N146 (z 0,04), not N22 UKOIL day-sign (agree 0,52, cover 0,51). Screened 2026-10-03 ~01:18 CEST. NEW_FAMILY BP dead; no GBP-only, no UKOIL-only, no FX/oil twin.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BP** (sterling vs Brent **petrocurrency basis**, two CFDs, session-flat). Both round-trips are in `COSTS_FTMO.csv`. Not an estimated-gate placeholder. Not an equity-factor z→US500. Not a metal–oil twin and not Brent–WTI.  
**Signal:** M5 day-close ratio **GBPUSD / UKOILcash**. **Trade:** both legs, equal bp.  
**Track 4 + D-100:** cable vs Brent mean-reverts when sterling is rich or cheap versus the oil leg the UK still prices. Flat inside 15:30→21:00 CET so the UKOIL overnight swap is not the alpha.

**Gate (both in `COSTS_FTMO.csv`):** GBPUSD RT **0,70** + UKOILcash RT **2,71** = **3,41** → gate 3 × 3,41 = **10,23** bp. Swap 0. No single-leg cherry-pick.

**D-094a:** train 2021–2023. Reden **(b)**: both CFDs have M5 from 2021-01. Mechanism is a petrocurrency basis, not a crack spread, not WTI vs Brent, and not an ETF.

**Onderscheid:**
- ≠ **N136** Brent–WTI FAIL (oil–oil) / **N22** UKOIL Lon→NY single-leg MR / **N80** UKOIL OVN-gap / **ENERGY_TSMOM**
- ≠ **N140/N141** metal–oil / **N146** AUD–XAU (other OPEN; do not pool)
- ≠ **N144** PGM / **N145** crypto / **N98** USOIL→US100 lead-lag / **N143** XLE→US500
- ≠ **N137** USDMXN / D-098 single-name FX / equity-factor z→US500 / thr-grid / overnight
- ≠ N50/N49 oil TSMOM (overnight swing, one leg)

## Regel
**Signal (dag t, last M5 ≤ 22:00 CET on each leg):**
1. `ratio_t = GBP_close_t / UKOIL_close_t`.
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)` (ddof=0).
3. **basis fade:** `z40 > +1,5` → **SHORT GBP + LONG UKOIL** (sterling rich); `z40 < −1,5` → **LONG GBP + SHORT UKOIL**; else skip. Threshold frozen — no grid.

**Execution (dag t+1) — D-100 session-flat, both legs:**
4. Entry: first M5 ≥ **15:30 CET** (span ≤15 min) on **each** leg. Either missing → skip day.
5. Exit: flat ≤ **21:00 CET** same day on both. **No overnight.**
6. PnL bp = sum of the two signed leg returns (equal weight). Non-overlapping (≤1 basket/day).

**Future clone bar (precommitted):** FAIL_CLONE if |z corr| vs UKOIL/USOIL z40 ≥ 0,90, or vs XAU/UKOIL z40 ≥ 0,90, or vs AUD/XAU z40 ≥ 0,90, or (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N136, vs N140, vs N22's UKOIL day-sign, or vs N146. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/GBPUSD.csv.gz` + `data/m5gz/UKOILcash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **10,23** bp, **N ≥ 150**.
- PASS → PREREG. FAIL → STOP (geen UKOIL-only, geen GBP-only, geen USOIL twin, geen XAU leg, geen US500 remap, geen thr-grid, geen overnight, geen soft gate).
