# VOORSTEL_PRESCREEN_N122 — DBC_COMMODITY_STRESS → US500cash session-flat (NEW_FAMILY AQ)

**Status:** **DIAG_FAIL** C-038 `1a22e81` (mean **−6,31**; N=368; gate 2,34) — **geen PREREG**; stale Faraday OPEN at `b236459` cleared 2026-10-03. Dead += N122; no DBC→US500 clones.
**Auteur:** Strateeg (Grok). **NEW_FAMILY AQ** (broad commodity ETF **level** stress → equity session-flat — multi-commodity risk channel; **≠ CPER** copper solo / **≠ GAS** / **≠ SILVER** / **≠ CRACK** / **≠ USO** oil solo).  
**Signal:** Yahoo/proxy **DBC** (Invesco DB Commodity Index Tracking). **Trade:** `US500cash` (RT **0,78** bp; swap 0 — **session-flat**).  
**Track 4 + D-100:** Broad commodity complex stress as global growth / inflation-risk timing for DM large-cap; intradag-vlak (geen swap).

**Gate:** 3 × US500 RT = 3 × 0,78 = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: DBC as **broad commodity basket** level stress into US500 beta — distinct from CPER copper (N117 DEAD), UNG gas (N112), SLV/GLD silver-gold (N113), and crack-spread macro (N101). FTMO-M5 for costs. Herhaal in PREREG.

**Onderscheid:**
- ≠ **N117 CPER** FAIL_STRESS (copper solo ≠ broad commodity basket)
- ≠ **N112 GAS** FAIL_T / **N113 SILVER_GOLD** FAIL_COST / **N101 CRACK** FAIL_T / USO oil solo
- ≠ **N118 TIP** / **N116 TLT** / **N114 HYG** / **N120 VNQ** / **N121 EEM**
- ≠ VIX / SECTOR_DISP / L60 / ORB-meta / UKOIL-OVN / CORN / N75–N121 clones / DBC CFD trade leg

## Regel
**Signal (dag t):**
1. `z120 = (DBC_t − mean_120(DBC)) / stdev_120(DBC)`; `d20 = DBC_t / DBC_{t−20} − 1`.
2. **combo:** `(z120 > +0,5) and (d20 > 0)` → **LONG** US500 (commodity relief = growth-ok / risk-on); `(z120 < −0,5) and (d20 < 0)` → **SHORT** (commodity crash = growth scare into equity); else skip.

**Execution (dag t+1, US500cash) — D-100 session-flat:**
3. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
4. Exit: flat ≤ **21:00 CET** same day. **No overnight.**
5. Non-overlapping (≤1/day).

## Pre-screen
- Data: Yahoo/proxy `data/daily/DBC.csv` + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **2,34** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N122. FAIL → STOP (geen thr-grid, geen CPER/GAS/SILVER/CRACK rewrite, geen overnight, geen soft gate).
