# VOORSTEL_PRESCREEN_N126 — DBA_AG_STRESS → US500cash session-flat (NEW_FAMILY AU)

**Status:** **geen PREREG — D-092.1 FAIL** `n126_n127` (N=380, mean **−6,36 < 2,34**; years +9,26/−15,58/−1,35); screened 2026-10-03 ~00:05 CEST. NEW_FAMILY AU dead screen; ≠DBC.
**Auteur:** Strateeg (Grok). **NEW_FAMILY AU** (agriculture commodity ETF **level** stress → equity session-flat — soft-ag / food complex; **≠ DBC** broad commodity basket DIAG_FAIL / **≠ CPER** / **≠ GAS** / **≠ SILVER** / **≠ CRACK** / **≠ CORN** solo).  
**Signal:** Yahoo/proxy **DBA** (Invesco DB Agriculture). **Trade:** `US500cash` (RT **0,78** bp; swap 0 — **session-flat**).  
**Track 4 + D-100 + D-097 commodities:** Ag complex stress as food/inflation-growth timing for DM large-cap; intradag-vlak (geen swap).

**Gate:** 3 × US500 RT = 3 × 0,78 = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: DBA as **agriculture basket** level stress into US500 beta — distinct from DBC broad commodity (N122 DIAG_FAIL C-038), CPER copper (N117), UNG gas (N112), SLV/GLD (N113), crack (N101), CORN_F demoted. FTMO-M5 for costs. Herhaal in PREREG.

**Onderscheid:**
- ≠ **N122 DBC** DIAG_FAIL C-038 (broad commodity ≠ ag-only basket)
- ≠ **N117 CPER** / **N112 GAS** / **N113 SILVER_GOLD** / **N101 CRACK** / CORN_F demote
- ≠ **N124 YIELD_CURVE** / **N125 DEFENSIVE** / TLT/TIP/HYG/VNQ/EEM/EMB/IWM/SECTOR_DISP/VIX
- ≠ N75–N125 clones / DBA CFD trade leg / overnight / thr-grid / soft gate

## Regel
**Signal (dag t):**
1. `z120 = (DBA_t − mean_120(DBA)) / stdev_120(DBA)`; `d20 = DBA_t / DBA_{t−20} − 1`.
2. **combo:** `(z120 > +0,5) and (d20 > 0)` → **LONG** US500 (ag relief = growth-ok); `(z120 < −0,5) and (d20 < 0)` → **SHORT** (ag crash = growth scare); else skip.

**Execution (dag t+1, US500cash) — D-100 session-flat:**
3. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
4. Exit: flat ≤ **21:00 CET** same day. **No overnight.**
5. Non-overlapping (≤1/day).

## Pre-screen
- Data: Yahoo/proxy `data/daily/DBA.csv` + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **2,34** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N126. FAIL → STOP (geen thr-grid, geen DBC rewrite→N122 clone, geen overnight, geen soft gate).
