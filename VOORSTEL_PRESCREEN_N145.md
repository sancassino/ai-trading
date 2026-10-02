# VOORSTEL_PRESCREEN_N145 — BTC_ETH_CRYPTO_XS session-flat (NEW_FAMILY BN)

**Status:** **OPEN** — D-092.1 refill after N142 FAIL / N143 FAIL_CLONE (filed 2026-10-03 ~01:03 CEST). Not screened this cycle.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BN** (bitcoin vs ether **crypto basis**, two crypto CFDs, session-flat). **D-097** high-vol book that is **not** an equity-factor z→US500 and **not** a metal–oil twin.  
**Signal:** M5 day-close ratio **BTCUSD / ETHUSD**. **Trade:** both legs, equal bp.  
**Track 4 + D-100:** the BTC/ETH basis mean-reverts when bitcoin is rich or cheap versus ether. Flat inside 15:30→21:00 CET so funding/overnight swap is not the alpha. The clock is the swap-flat window, not an Asia→EU continuation and not an ORB.

**Gate (both NOT in `COSTS_FTMO.csv`; estimator checked on US500 → 0,78 bp):** all-hours M5 spread median 2024-01-01…2026-09-30, `bp = spread_points × point / close × 1e4`, commission **not** in COSTS (spread-only est.; the old N45 **18 bp** crypto placeholder is **not** this measurement).  
BTC **0,17** + ETH **7,58** = **7,75** → gate 3 × 7,75 = **23,25** bp.  
(Session 15:30–21:00 medians not used.) Swap 0. Binding RT = max(est, U2) on **each** leg before any PREREG. If U2's book cost is higher, the gate rises before any PREREG. No single-leg cherry-pick.

**D-094a:** train 2021–2023. Reden **(b)**: both crypto CFDs have M5 from 2021-01-01. Mechanism is a crypto cross-sectional basis, not ETH session continuation and not a cash-index or commodity ETF.

**Onderscheid:**
- ≠ **N45** ETHUSD Asia→EU continuation FAIL (single leg, other clock)
- ≠ **S2-BTC** / **P1 ORB+BTC** (ORB / reserve sleeve, not a ratio fade)
- ≠ **N144** XPT/XPD PGM basis (other OPEN; do not pool)
- ≠ **N142** index basis FAIL / **N143** XLE FAIL_CLONE of DBC
- ≠ **N140/N141** metal–oil / USDCHF/USDJPY twin / **N75** XAU/XAG / **N136** Brent–WTI
- ≠ equity-factor z→US500 / GER/UK / JP/HK / USDMXN / DXY / thr-grid / overnight

## Regel
**Signal (dag t, last M5 ≤ 22:00 CET on each leg):**
1. `ratio_t = BTC_close_t / ETH_close_t`.
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)` (ddof=0).
3. **basis fade:** `z40 > +1,5` → **SHORT BTC + LONG ETH** (bitcoin rich); `z40 < −1,5` → **LONG BTC + SHORT ETH**; else skip. Threshold frozen — no grid.

**Execution (dag t+1) — D-100 session-flat, both legs:**
4. Entry: first M5 ≥ **15:30 CET** (span ≤15 min) on **each** leg. Either missing → skip day.
5. Exit: flat ≤ **21:00 CET** same day on both. **No overnight.**
6. PnL bp = sum of the two signed leg returns (equal weight). Non-overlapping (≤1 basket/day).

**Future clone bar (precommitted):** FAIL_CLONE if |z corr| vs XPT/XPD z40 ≥ 0,90, or vs XAU/XAG z40 ≥ 0,90, or (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N45's ETH continuation, vs a BTC-only ORB day-sign, or vs N144. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/BTCUSD.csv.gz` + `data/m5gz/ETHUSD.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **23,25** bp, **N ≥ 150**.
- PASS → PREREG only after U2 confirms each RT (binding = max(est, U2)). FAIL → STOP (geen ETH-only rewrite, geen BTC ORB, geen US500 remap, geen thr-grid, geen overnight, geen soft gate).
