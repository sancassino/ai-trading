# VOORSTEL_PRESCREEN_N136 — BRENT_WTI_XS session-flat (NEW_FAMILY BE)

**Status:** **OPEN** — D-094 refill after N134/N135 D-092.1 FAIL (filed 2026-10-03 ~00:29 CEST). Not screened this cycle.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BE** (Atlantic **Brent–WTI location/quality spread** → two oil CFDs, session-flat — crude-basis XS; **≠ N101 CRACK** product-crack→equity / **≠ N22** UKOIL London-AM fade / **≠ N80** UKOIL OVN-gap / **≠ ENERGY_TSMOM** / **≠ N98** USOIL→US100).  
**Signal:** M5 day-close ratio **UKOILcash / USOILcash**. **Trade:** both legs, equal bp.  
**Track 4 + D-100 + D-097 commodities XS:** Brent rich vs WTI mean-reverts when the basis is stretched; intradag-vlak (UKOIL short-swap is toxic — no overnight).

**Gate:** RT_UK **2,71** + RT_US **3,34** = **6,05** bp (both in `COSTS_FTMO.csv`; swap 0 session-flat) → 3 × 6,05 = **18,15** bp. No single-leg cherry-pick.

**D-094a:** train 2021–2023. Reden **(b)**: both cash CFDs have M5 from 2021-01; the ratio is a location spread, not a crack (gasoline/heat vs crude → equity) and not a single-name London impulse fade. Binding window is FTMO-M5 on **both** legs.

**Onderscheid:**
- ≠ **N101 CRACK_SPREAD_MACRO** FAIL_T (refined-product crack → US100 ≠ Brent/WTI basis → the two crude CFDs)
- ≠ **N22** UKOIL Lon→NY MR FAIL / **N76** inventory-window / **N80** OVN-gap FAIL_COST / **S2-USOIL** EIA
- ≠ **N98** USOIL→US100 lead-lag / **N112 GAS** / **N122 DBC** / **N126 DBA**
- ≠ N75–N135 ETF-level→US500 stress template / thr-grid / soft gate / overnight

## Regel
**Signal (dag t, last M5 ≤ 22:00 CET on each leg):**
1. `ratio_t = UKOIL_close_t / USOIL_close_t`.
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)`.
3. **basis fade:** `z40 > +1,5` → **SHORT UKOIL + LONG USOIL** (Brent rich); `z40 < −1,5` → **LONG UKOIL + SHORT USOIL**; else skip.

**Execution (dag t+1) — D-100 session-flat, both legs:**
4. Entry: first M5 ≥ **15:30 CET** (span ≤15 min) on **each** leg. Either missing → skip day.
5. Exit: flat ≤ **21:00 CET** same day on both. **No overnight.**
6. PnL bp = sum of the two signed leg returns (equal weight). Non-overlapping (≤1 basket/day).

## Pre-screen
- Data: `data/m5gz/UKOILcash.csv.gz` + `data/m5gz/USOILcash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **18,15** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N136. FAIL → STOP (geen single-leg UKOIL rewrite, geen crack→equity twin, geen thr-grid, geen overnight, geen soft gate).
