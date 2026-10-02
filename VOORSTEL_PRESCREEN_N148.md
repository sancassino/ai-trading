# VOORSTEL_PRESCREEN_N148 — USDJPY_US100_RISK_XS session-flat (NEW_FAMILY BQ)

**Status:** **geen PREREG — D-092.1 FAIL** `n148_n149` (N=217, mean **+3,31 < 4,32**; med +0,96; years +23,98 / +8,55 / −6,67; L/S 106/111; 262 signals, 45 missing bars). Not a clone: N142 agree 0,99 but cover **0,47**; N81 agree 0,97 cover 0,36; US100/US500 z **−0,70**; N92 agree 0,39 cover 0,83; USDJPY L60 agree 0,48 cover 0,79; US100 20d overnight agree **0,02** cover 1,00; N149 z 0,43 cover 0,30. Screened 2026-10-03 ~01:23 CEST. NEW_FAMILY BQ dead; no USDJPY-only, no US100-only, no FX/index twin.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BQ** (yen vs Nasdaq **risk basis**, two CFDs, session-flat). Both round-trips are in `COSTS_FTMO.csv`. Not an FX/metal twin of N146. Not an FX/oil twin of N147. Not an index–index pair. Not an equity-factor z→US500.  
**Signal:** M5 day-close ratio **USDJPY / US100cash**. **Trade:** both legs, equal bp.  
**Track 4 + D-100:** the funding currency and the cash Nasdaq dislocate when one has outrun the other. Flat inside 15:30→21:00 CET so neither overnight swap is the alpha.

**Gate (both in `COSTS_FTMO.csv`):** USDJPY RT **0,78** + US100cash RT **0,66** = **1,44** → gate 3 × 1,44 = **4,32** bp. Swap 0 (session-flat is the cheap side; overnight short-JPY is 1,58 and long-US100 is 1,95). No single-leg cherry-pick.

**D-094a:** train 2021–2023. Reden **(b)**: both CFDs have M5 from 2021-01. Mechanism is a yen/tech risk basis, not a G10 FX cross, not a US cash-index pair, and not a dollar-index signal into one equity leg.

**Onderscheid:**
- ≠ **N146** AUD/XAU FAIL (−1,56 < 6,15) / **N147** GBP/UKOIL FAIL_CLONE (z 0,92 vs N140)
- ≠ **N142** US30/US500 / **N81** US100/US500 3d RV / **N138** GER/UK — this book has a yen leg, not two indices
- ≠ **N131** DXY→US500 (one destination) / **N92** NY-2h / **IDX_SHORT** / L60 USDJPY
- ≠ inline **USDCHF/USDJPY** FX–FX FAIL_CLONE (do not rescreen) / D-098 single-name FX
- ≠ **N144** PGM / **N145** crypto / **N143** XLE–DBC / metal–oil
- ≠ **N149** EUR–GER40 (other OPEN; do not pool)

## Regel
**Signal (dag t, last M5 ≤ 22:00 CET on each leg):**
1. `ratio_t = USDJPY_close_t / US100_close_t`.
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)` (ddof=0).
3. **basis fade:** `z40 > +1,5` → **SHORT USDJPY + LONG US100** (yen cheap vs Nasdaq); `z40 < −1,5` → **LONG USDJPY + SHORT US100**; else skip. Threshold frozen — no grid.

**Execution (dag t+1) — D-100 session-flat, both legs:**
4. Entry: first M5 ≥ **15:30 CET** (span ≤15 min) on **each** leg. Either missing → skip day.
5. Exit: flat ≤ **21:00 CET** same day on both. **No overnight.**
6. PnL bp = sum of the two signed leg returns (equal weight). Non-overlapping (≤1 basket/day).

**Future clone bar (precommitted):** FAIL_CLONE if |z corr| vs US100/US500 z40 ≥ 0,90, or vs US30/US500 z40 ≥ 0,90, or vs EUR/GER40 z40 ≥ 0,90, or (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N81, vs N142, vs N131's US500 day-sign, vs N92, or vs N149. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/USDJPY.csv.gz` + `data/m5gz/US100cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **4,32** bp, **N ≥ 150**.
- PASS → PREREG. FAIL → STOP (geen USDJPY-only, geen US100-only, geen US30/US500 remap, geen DXY→US500, geen FX/metal, geen FX/oil, geen thr-grid, geen overnight, geen soft gate).
