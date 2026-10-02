# VOORSTEL_PRESCREEN_N150 — XAGUSD_US30_METAL_INDUSTRIAL_XS session-flat (NEW_FAMILY BS)

**Status:** **geen PREREG — CTO C-042 DIAG_FAIL** (n=225, mean **+10.05 < 16.56**; med +3.59; years +13.15/−7.57/+29.22; L/S 131/94; day_t 1.26). Faraday filed OPEN ~01:23; CTO screened ~01:30 CEST. Dead screen; no thr-grid / no overnight / no soft gate.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BS** (silver vs Dow **metal–industrial basis**, two CFDs, session-flat). Both round-trips are in `COSTS_FTMO.csv`. Not an FX/index twin of N148 or N149. Not an FX/metal twin of N146. Not an FX/oil twin of N147. Not XAU/XAG and not XAG/UKOIL.  
**Signal:** M5 day-close ratio **XAGUSD / US30cash**. **Trade:** both legs, equal bp.  
**Track 4 + D-100:** silver and the cash Dow dislocate when the metal has outrun, or lagged, US industrial equity. Flat inside 15:30→21:00 CET so neither overnight swap is the alpha.

**Gate (both in `COSTS_FTMO.csv`):** XAGUSD RT **5,07** + US30cash RT **0,45** = **5,52** → gate 3 × 5,52 = **16,56** bp. Swap 0 (session-flat is the cheap side that does not depend on the sign; overnight long-XAG is 3,15 and long-US30 is 2,28; short-XAG receives 0,18 and short-US30 receives 0,12, so a two-sided book cannot lock the cheap overnight side). No single-leg cherry-pick.

**D-094a:** train 2021–2023. Reden **(b)**: both CFDs have M5 from 2021-01. Mechanism is a precious-metal vs US-industrial basis, not a currency vs an index and not a US cash-index pair.

**Onderscheid:**
- ≠ **N148** USDJPY/US100 FAIL (+3,31 < 4,32) / **N149** EUR/GER40 FAIL (+2,05 < 4,05) — no FX leg
- ≠ **N146** AUD/XAU / **N147** GBP/UKOIL (FX/commodity; do not rewrite)
- ≠ **N75** XAU/XAG / **N141** XAG/UKOIL / **N140** XAU/UKOIL / **N133** GLD→US500 (one destination)
- ≠ **N142** US30/US500 / **N81** US100/US500 / **N92** NY-2h / US100 overnight / IDX_SHORT
- ≠ **N151** EURJPY/USDCHF (other OPEN; do not pool)

## Regel
**Signal (dag t, last M5 ≤ 22:00 CET on each leg):**
1. `ratio_t = XAG_close_t / US30_close_t`.
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)` (ddof=0).
3. **basis fade:** `z40 > +1,5` → **SHORT XAG + LONG US30** (silver rich vs Dow); `z40 < −1,5` → **LONG XAG + SHORT US30**; else skip. Threshold frozen — no grid.

**Execution (dag t+1) — D-100 session-flat, both legs:**
4. Entry: first M5 ≥ **15:30 CET** (span ≤15 min) on **each** leg. Either missing → skip day.
5. Exit: flat ≤ **21:00 CET** same day on both. **No overnight.**
6. PnL bp = sum of the two signed leg returns (equal weight). Non-overlapping (≤1 basket/day).

**Future clone bar (precommitted):** FAIL_CLONE if |z corr| vs XAU/XAG z40 ≥ 0,90, or vs XAG/UKOIL z40 ≥ 0,90, or vs US30/US500 z40 ≥ 0,90, or vs USDJPY/US100 z40 ≥ 0,90, or (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N75, vs N141, vs N142, vs N133's US500 day-sign, or vs N151. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/XAGUSD.csv.gz` + `data/m5gz/US30cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **16,56** bp, **N ≥ 150**.
- PASS → PREREG. FAIL → STOP (geen XAG-only, geen US30-only, geen XAU/XAG remap, geen GLD→US500, geen FX/index, geen FX/metal, geen FX/oil, geen thr-grid, geen overnight, geen soft gate).
