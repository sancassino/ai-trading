# VOORSTEL_PRESCREEN_N117 — CPER_COPPER_STRESS → US500cash session-flat (NEW_FAMILY AL)

**Status:** **OPEN** — pipeline refill after N112 FAIL_T + N113 FAIL_COST_GATE + N115 D-092.1 FAIL (filed 2026-10-02 ~23:05 CEST).  
**Auteur:** Strateeg (Grok). **NEW_FAMILY AL** (copper ETF level stress → equity session-flat — industrial-metal growth proxy, nooit als Ag/Au ratio twin).  
**Signal:** Yahoo/proxy **CPER** (copper ETF). **Trade:** `US500cash` (RT **0,78** bp; swap 0 — **session-flat**).  
**Track 4 + D-100:** Copper level as global growth / industrial risk-appetite timing for DM equity; intradag-vlak (geen swap).

**Gate:** 3 × US500 RT = 3 × 0,78 = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: copper price stress as growth-cycle / risk-appetite signal for DM equity beta — distinct from silver/gold ratio fade and from copper/gold ratio; FTMO-M5 for costs. Herhaal in PREREG.

**Onderscheid:**
- ≠ **N113 SILVER_GOLD_RATIO** FAIL_COST_GATE (Ag/Au ratio ≠ copper **level**)
- ≠ **COPPER_GOLD_MACRO** prior Lane-A (Cu/Au **ratio** ≠ CPER level alone)
- ≠ **N112 GAS** FAIL_T / **N101 CRACK** / **N98 USOIL→US100** / copper CFD trade leg
- ≠ HYG/EMB/VIX/SECTOR_DISP / L60 / ORB-meta / UKOIL-OVN / CORN / N75–N116 clones

## Regel
**Signal (dag t):**
1. `z40 = (CPER_t − mean_40(CPER)) / stdev_40(CPER)`.
2. **stress_buy:** `z40 > +1,5` → **SHORT** US500 (copper spike = late-cycle / cost-push risk-off into equity); `z40 < −1,5` → **LONG** (copper crash = growth-scare bounce / relief into equity); else skip.

**Execution (dag t+1, US500cash) — D-100 session-flat:**
3. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
4. Exit: flat ≤ **21:00 CET** same day. **No overnight.**
5. Non-overlapping (≤1/day).

## Pre-screen
- Data: Yahoo/proxy `data/daily/CPER.csv` + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **2,34** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N117. FAIL → STOP (geen thr-grid, geen copper CFD twin, geen Cu/Au ratio rewrite, geen overnight, geen soft gate).
