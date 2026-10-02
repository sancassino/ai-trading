# VOORSTEL_PRESCREEN_N155 — US30_UKOIL_INDUSTRIAL_CRUDE_XS session-flat (NEW_FAMILY BX)

**Status:** **OPEN** — D-092.1 refill after N152 FAIL / N153 FAIL (filed 2026-10-03 ~01:35 CEST). Not screened this cycle.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BX** (Dow vs Brent **industrial–crude basis**, one cash index and one oil CFD, session-flat). Both round-trips are in `COSTS_FTMO.csv`. Not an FX book. Not a G10 cross. Not silver/index. Not metal–oil (no bullion leg). Not an equity-factor z→US500.  
**Signal:** M5 day-close ratio **US30cash / UKOILcash**. **Trade:** both legs, equal bp.  
**Track 4 + D-100:** the Dow and Brent dislocate when industrial equities have outrun, or lagged, the crude complex. Flat inside 15:30→21:00 CET. Overnight long-UKOIL receives and short-UKOIL pays ~27 bp; a two-sided book cannot lock the receiving side, so swap in the gate is 0.

**Gate (both in `COSTS_FTMO.csv`):** US30cash RT **0,45** + UKOILcash RT **2,71** = **3,16** → gate 3 × 3,16 = **9,48** bp. Swap 0. No single-leg cherry-pick. No UKOIL-only overnight.

**D-094a:** train 2021–2023. Reden **(b)**: both CFDs have M5 from 2021-01. Mechanism is cash industrials versus Brent, not WTI versus Brent, not gold versus Brent, and not a one-way oil impulse into the Nasdaq.

**Onderscheid:**
- ≠ **N152** GBP/NZD / **N153** EUR/CAD (no FX leg; G10 crosses exhausted this stretch)
- ≠ **N136** Brent–WTI (second leg is US30, not WTI)
- ≠ **N140** XAU/UKOIL / **N141** XAG/UKOIL / **N147** GBP/UKOIL (no metal, no sterling)
- ≠ **N98** USOIL→US100 one-way / **N22** UKOIL Lon-AM / **N80** UKOIL OVN-gap (two legs, Dow not Nasdaq, no overnight)
- ≠ **N142** US30/US500 / **N150** XAG/US30 (the second leg is crude, not another index and not silver)
- ≠ **N143** XLE→US500 / ENERGY_TSMOM / crack→equity
- ≠ **N154** US100/GER40 (other OPEN; do not pool)

## Regel
**Signal (dag t, last M5 ≤ 22:00 CET on each leg):**
1. `ratio_t = US30_close_t / UKOIL_close_t`.
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)` (ddof=0).
3. **basis fade:** `z40 > +1,5` → **SHORT US30 + LONG UKOIL** (Dow rich vs Brent); `z40 < −1,5` → **LONG US30 + SHORT UKOIL**; else skip. Threshold frozen — no grid.

**Execution (dag t+1) — D-100 session-flat, both legs:**
4. Entry: first M5 ≥ **15:30 CET** (span ≤15 min) on **each** leg. Either missing → skip day.
5. Exit: flat ≤ **21:00 CET** same day on both. **No overnight.**
6. PnL bp = sum of the two signed leg returns (equal weight). Non-overlapping (≤1 basket/day).

**Future clone bar (precommitted):** FAIL_CLONE if |z corr| vs UKOIL/USOIL z40 ≥ 0,90, or vs XAU/UKOIL z40 ≥ 0,90, or vs XAG/UKOIL z40 ≥ 0,90, or vs US30/US500 z40 ≥ 0,90, or vs XAG/US30 z40 ≥ 0,90, or (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N136, vs N140, vs N141, vs N147, vs N98's oil day-sign, vs N142, vs N150, or vs N154. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/US30cash.csv.gz` + `data/m5gz/UKOILcash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **9,48** bp, **N ≥ 150**.
- PASS → PREREG. FAIL → STOP (geen US30-only, geen UKOIL-only, geen Brent–WTI remap, geen metal–oil, geen FX leg, geen factor→US500, geen thr-grid, geen overnight, geen soft gate).
