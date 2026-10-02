# VOORSTEL_S2_XLE_ENERGY_EQUITY_STRESS — XLE z → US500 session-flat (NEW_FAMILY BL / N143)

**Status:** **OPEN** — S2 optional-feed slot after N140/N141 D-092.1 FAIL (filed 2026-10-03 ~00:55 CEST). **Not screened this cycle. Not a PREREG.**  
**Auteur:** Strateeg-2 promote, Lane-B mapping by Strateeg (Grok). **NEW_FAMILY BL.**  
**Lane-A:** `grok/strateeg-2` @ `5a21939`, `results/strateeg2_prescreen/cycle_0047/`.  
**Signal:** daily **XLE** level z40 / thr ±1,0 / **fade_extreme**. **Trade:** `US500cash` only.  
**Map:** **session-flat US500** 15:30→21:00 CET (D-100). **Do not** remap to overnight long US100.

Lane-A (hold=1d overnight proxy, ≤2024, non-overlapping): day_t **2,29**, mean **5,41** bp, N=2863, net after drag **3,82**, flag **COST_OK**. That number is **not** a Lane-B PASS: the hold is not this session-flat rule, and day_t 2,29 is already under the Lane-B gate **2,34**. No soft-pass. No screen in the filing cycle.

**Gate:** US500 RT **0,78** (`COSTS_FTMO.csv`) × 3 = **2,34** bp. Swap **0** (session-flat). Signal-only ETF — no XLE CFD leg, no oil CFD leg.

**D-094a:** train 2021–2023. Reden **(b)**: XLE daily from 1998; binding window is FTMO-M5 on US500. Energy-equity sector stress into the broad cash index, not a crude CFD and not a two-index basis.

**Onderscheid (binding):**
- ≠ **ENERGY_TSMOM** (UKOIL+USOIL L20/H10 LO, FAIL_COST_GATE)
- ≠ **N112 GAS** / UNG→US500 / natgas CFD
- ≠ **N101 CRACK** (HO/BRENT → US100)
- ≠ **N98** USOIL Lon-AM → US100
- ≠ **N124** YIELD_CURVE / **N125** DEFENSIVE (XLU/XLI)
- ≠ **N140/N141** XAU/XAG–UKOIL (FAIL / FAIL_CLONE this cycle)
- ≠ **N136** Brent–WTI / **N122** DBC / **N134** XLF (sector cousin; clone bar below)
- ≠ **N142** US30/US500 two-leg basis (other OPEN; do not pool)

## Regel (frozen from S2 `fade_extreme`; no thr-grid)
**Signal (dag t, XLE daily close, no 2024+ in the z):**
1. `z40 = (XLE_t − mean_40) / stdev_40` (ddof=0).
2. **fade_extreme:** `z40 > +1,0` → **SHORT US500**; `z40 < −1,0` → **LONG US500**; else skip. Threshold frozen.

**Execution (dag t+1) — D-100 session-flat, one leg:**
3. Entry: first M5 ≥ **15:30 CET** (span ≤15 min) on **US500cash**. Missing → skip.
4. Exit: flat ≤ **21:00 CET** same day. **No overnight. No US100.**
5. Non-overlapping (≤1/day).

**Future clone bar (precommitted):** FAIL_CLONE if |z corr| vs UNG z40 ≥ 0,90, or vs XLF z40 ≥ 0,90, or vs DBC z40 ≥ 0,90, or vs HEATOIL/BRENT crack z60 ≥ 0,90, or (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N112 GAS, vs N98 USOIL→US100, vs N134 XLF, or vs N142's US500 leg. A clone is not a PASS.

## Pre-screen (next cycle — not this push)
- Data: `data/daily/XLE.csv` (already in tree) + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **2,34** bp, **N ≥ 150**.
- PASS → PREREG only after that Lane-B screen. FAIL → STOP (geen US100 overnight, geen oil-CFD remap, geen UNG/CRACK/XLF rewrite, geen thr-grid, geen soft gate).
