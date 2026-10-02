# VOORSTEL_PRESCREEN_N146 — AUD_XAU_COMMODITY_XS session-flat (NEW_FAMILY BO)

**Status:** **OPEN** — D-092.1 refill after N144 FAIL / N145 FAIL (filed 2026-10-03 ~01:13 CEST). Not screened this cycle.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BO** (Aussie vs gold **commodity-complex basis**, two CFDs, session-flat). Both round-trips are in `COSTS_FTMO.csv`. Not an estimated-gate placeholder. Not an equity-factor z→US500. Not a metal–oil twin.  
**Signal:** M5 day-close ratio **AUDUSD / XAUUSD**. **Trade:** both legs, equal bp.  
**Track 4 + D-100:** the commodity-currency vs the monetary metal mean-reverts when the Aussie is rich or cheap versus gold. Flat inside 15:30→21:00 CET so neither overnight swap is the alpha. Not a single-name FX fade (D-098 barred those at ~3 bp).

**Gate (both in `COSTS_FTMO.csv`):** AUDUSD RT **1,22** + XAUUSD RT **0,83** = **2,05** → gate 3 × 2,05 = **6,15** bp. Swap 0. No single-leg cherry-pick.

**D-094a:** train 2021–2023. Reden **(b)**: both CFDs have M5 from 2021-01. Mechanism is a commodity-complex basis, not a PGM pair, not crypto, and not an ETF stress into US500.

**Onderscheid:**
- ≠ **N144** XPT/XPD FAIL (−0,69 < 205,06) / **N145** BTC/ETH FAIL (−9,65 < 64,31)
- ≠ **N140/N141** XAU/XAG–UKOIL (metal–oil dead) / **N75** XAU/XAG 3d one-side / **N133** GLD→US500
- ≠ **N91** AUDUSD 5d carry LO / **N95** XAU Lon→NY / **N147** GBP–UKOIL (other OPEN; do not pool)
- ≠ **N142** index basis / **N143** XLE / equity-factor z→US500 / thr-grid / overnight
- ≠ D-098 single-name FX (EURGBP/USDCHF). This book has a metal leg and a COSTS gate of 6,15

## Regel
**Signal (dag t, last M5 ≤ 22:00 CET on each leg):**
1. `ratio_t = AUD_close_t / XAU_close_t`.
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)` (ddof=0).
3. **basis fade:** `z40 > +1,5` → **SHORT AUD + LONG XAU** (Aussie rich); `z40 < −1,5` → **LONG AUD + SHORT XAU**; else skip. Threshold frozen — no grid.

**Execution (dag t+1) — D-100 session-flat, both legs:**
4. Entry: first M5 ≥ **15:30 CET** (span ≤15 min) on **each** leg. Either missing → skip day.
5. Exit: flat ≤ **21:00 CET** same day on both. **No overnight.**
6. PnL bp = sum of the two signed leg returns (equal weight). Non-overlapping (≤1 basket/day).

**Future clone bar (precommitted):** FAIL_CLONE if |z corr| vs XAU/XAG z40 ≥ 0,90, or vs XAU/UKOIL z40 ≥ 0,90, or vs GLD z40 ≥ 0,90, or vs GBP/UKOIL z40 ≥ 0,90, or (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N75, vs N140, vs N91's AUD day-sign, or vs N147. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/AUDUSD.csv.gz` + `data/m5gz/XAUUSD.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **6,15** bp, **N ≥ 150**.
- PASS → PREREG. FAIL → STOP (geen XAU-only, geen AUD-only, geen UKOIL leg, geen US500 remap, geen thr-grid, geen overnight, geen soft gate).
