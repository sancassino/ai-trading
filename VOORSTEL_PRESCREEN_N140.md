# VOORSTEL_PRESCREEN_N140 — XAU_UKOIL_XS session-flat (NEW_FAMILY BI)

**Status:** **OPEN** — D-097 refill after N138/N139 D-092.1 FAIL (filed 2026-10-03 ~00:46 CEST). Not screened this cycle.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BI** (gold–Brent **real-asset basis**, two CFDs, session-flat — bullion vs crude, not an equity index and not a single-leg metal fade). **≠ N136** Brent–WTI (second leg is XAU, not WTI) / **≠ N101** crack→equity / **≠ N75** XAU/XAG 3d / **≠ N113** SLV/GLD→US500 / **≠ N95** XAU Lon→NY single leg / **≠ N80** UKOIL OVN-gap / **≠ N138** DAX/FTSE / **≠ N139** Nikkei/Hang Seng.  
**Signal:** M5 day-close ratio **XAUUSD / UKOILcash**. **Trade:** both legs, equal bp.  
**Track 4 + D-100 + D-097:** gold rich vs Brent mean-reverts when the real basis is stretched. Intraday-flat so the UKOIL long-swap credit is not the alpha.

**Gate (both in `COSTS_FTMO.csv`):** XAU RT **0,83** + UKOIL RT **2,71** = **3,54** → gate 3 × 3,54 = **10,62** bp. Swap 0 (session-flat). No single-leg cherry-pick. No swap-credit.

**D-094a:** train 2021–2023. Reden **(b)**: both CFDs have M5 from 2021-01. Mechanism is a bullion–crude basis, not an EU/Asia index session and not an ETF→US500 stress.

**Onderscheid:**
- ≠ **N136** Brent/WTI XS FAIL (location spread of two crudes ≠ gold vs one crude)
- ≠ **N101** CRACK→US500 / **N80** UKOIL overnight gap / ENERGY_TSMOM
- ≠ **N75** XAU/XAG ratio / **N113** silver-gold→equity / **N133** GLD haven / **N129** PPLT→US500
- ≠ **N95/N25/N36** single-leg XAU session fades
- ≠ **N138** GER/UK (FAIL_CLONE of EU50/UK) / **N139** JP/HK / N103 / N107 / N108
- ≠ N75–N139 thr-grid / soft gate / overnight

## Regel
**Signal (dag t, last M5 ≤ 22:00 CET on each leg):**
1. `ratio_t = XAU_close_t / UKOIL_close_t`.
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)` (ddof=0).
3. **basis fade:** `z40 > +1,5` → **SHORT XAU + LONG UKOIL** (gold rich); `z40 < −1,5` → **LONG XAU + SHORT UKOIL**; else skip. Threshold frozen — no grid.

**Execution (dag t+1) — D-100 session-flat, both legs:**
4. Entry: first M5 ≥ **15:30 CET** (span ≤15 min) on **each** leg. Either missing → skip day.
5. Exit: flat ≤ **21:00 CET** same day on both. **No overnight.**
6. PnL bp = sum of the two signed leg returns (equal weight). Non-overlapping (≤1 basket/day).

**Future clone bar (precommitted):** FAIL_CLONE if |z corr| vs UKOIL/USOIL ratio z40 ≥ 0,90, or vs XAU/XAG ratio z40 ≥ 0,90, or (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N136, vs N75, or vs a single-leg XAU fade / UKOIL-OVN sign. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/XAUUSD.csv.gz` + `data/m5gz/UKOILcash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **10,62** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N140 (both RTs already in COSTS). FAIL → STOP (geen XAU/USOIL twin, geen XAU/XAG rewrite, geen single-leg XAU or UKOIL, geen thr-grid, geen overnight, geen soft gate).
