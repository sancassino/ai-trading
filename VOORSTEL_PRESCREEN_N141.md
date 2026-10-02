# VOORSTEL_PRESCREEN_N141 — XAG_UKOIL_XS session-flat (NEW_FAMILY BJ)

**Status:** **OPEN** — D-097 refill after N138/N139 D-092.1 FAIL (filed 2026-10-03 ~00:46 CEST). Not screened this cycle.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BJ** (silver–Brent **industrial-precious vs crude basis**, two CFDs, session-flat). **≠ N140** gold–Brent (do not pool; silver’s industrial beta is the point) / **≠ N75** XAU/XAG pair / **≠ N82** XAG London fade / **≠ N113** SLV/GLD→US500 / **≠ N136** Brent–WTI / **≠ N129** PPLT→equity.  
**Signal:** M5 day-close ratio **XAGUSD / UKOILcash**. **Trade:** both legs, equal bp.  
**Track 4 + D-100 + D-097:** silver rich vs Brent mean-reverts on the stretch. Flat inside the US afternoon so the hold is not overnight and not a swap credit.

**Gate (both in `COSTS_FTMO.csv`):** XAG RT **5,07** + UKOIL RT **2,71** = **7,78** → gate 3 × 7,78 = **23,34** bp. Swap 0 (session-flat). No single-leg cherry-pick. The high RT is the gate — do not soft it.

**D-094a:** train 2021–2023. Reden **(b)**: both CFDs have M5 from 2021-01. Mechanism is silver vs crude, not gold vs silver and not an ETF level→US500.

**Onderscheid:**
- ≠ **N140** XAU/UKOIL (different metal; clone bar below is binding)
- ≠ **N75** XAU/XAG 3d MR DIAG_FAIL / **N82** XAG AM-fix fade / **N60** XAG TSMOM
- ≠ **N113** silver-gold ratio→US500 (this trades the two CFDs, not US500; still FAIL_CLONE if the z bar trips)
- ≠ **N136** Brent–WTI / **N101** crack / **N80** UKOIL OVN
- ≠ **N129** platinum→US500 / **N133** GLD haven
- ≠ N75–N140 thr-grid / soft gate / overnight / single-leg silver rewrite

## Regel
**Signal (dag t, last M5 ≤ 22:00 CET on each leg):**
1. `ratio_t = XAG_close_t / UKOIL_close_t`.
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)` (ddof=0).
3. **basis fade:** `z40 > +1,5` → **SHORT XAG + LONG UKOIL** (silver rich); `z40 < −1,5` → **LONG XAG + SHORT UKOIL**; else skip. Threshold frozen — no grid.

**Execution (dag t+1) — D-100 session-flat, both legs:**
4. Entry: first M5 ≥ **15:30 CET** (span ≤15 min) on **each** leg. Either missing → skip day.
5. Exit: flat ≤ **21:00 CET** same day on both. **No overnight.**
6. PnL bp = sum of the two signed leg returns (equal weight). Non-overlapping (≤1 basket/day).

**Future clone bar (precommitted):** FAIL_CLONE if |z corr| vs XAU/UKOIL ratio z40 ≥ 0,90, or vs XAU/XAG ratio z40 ≥ 0,90, or vs UKOIL/USOIL ratio z40 ≥ 0,90, or (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N140, N75, N136, or a single-leg XAG fade. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/XAGUSD.csv.gz` + `data/m5gz/UKOILcash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **23,34** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N141 (both RTs already in COSTS). FAIL → STOP (geen XAG/USOIL twin, geen XAU/XAG rewrite, geen XAU/UKOIL rewrite, geen single-leg XAG, geen thr-grid, geen overnight, geen soft gate).
