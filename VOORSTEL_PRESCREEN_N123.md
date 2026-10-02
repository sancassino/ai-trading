# VOORSTEL_PRESCREEN_N123 — EFA_DM_EXUS_STRESS → US500cash session-flat (NEW_FAMILY AR)

**Status:** **DIAG_FAIL** C-038 `1a22e81` (mean **−2,66**; N=201; gate 2,34) — **geen PREREG**; stale Faraday OPEN at `b236459` cleared 2026-10-03. Dead += N123; no EFA→US500 clones.
**Auteur:** Strateeg (Grok). **NEW_FAMILY AR** (DM ex-US equity ETF **level** stress → US large-cap session-flat — EAFE / developed international risk-appetite channel; **≠ EEM** EM equity / **≠ EMB** EM credit).  
**Signal:** Yahoo/proxy **EFA** (iShares MSCI EAFE). **Trade:** `US500cash` (RT **0,78** bp; swap 0 — **session-flat**).  
**Track 4 + D-100:** DM international equity stress as global risk-appetite timing for US large-cap; intradag-vlak (geen swap).

**Gate:** 3 × US500 RT = 3 × 0,78 = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: EFA as **DM ex-US equity** level stress into US500 beta — distinct from EEM EM equity (N121 FAIL) and EMB EM credit (N100 DEAD). FTMO-M5 for costs. Herhaal in PREREG.

**Onderscheid:**
- ≠ **N121 EEM_EM_EQUITY** D-092.1 FAIL (EM equity ≠ DM ex-US / EAFE)
- ≠ **N100 EMB** FAIL_T (EM bonds ≠ DM equity) / **N119 IWM** (US small-cap ≠ EAFE)
- ≠ **N118 TIP** / **N116 TLT** / **N114 HYG** / **N120 VNQ** / GAS / CPER / SILVER
- ≠ VIX / SECTOR_DISP / L60 / ORB-meta / UKOIL-OVN / CORN / N75–N122 clones / EFA CFD trade leg

## Regel
**Signal (dag t):**
1. `z40 = (EFA_t − mean_40(EFA)) / stdev_40(EFA)`.
2. **stress_buy:** `z40 > +1,5` → **SHORT** US500 (DM-intl spike = crowded risk-on fade into US); `z40 < −1,5` → **LONG** (DM-intl crash = global growth scare bounce into US); else skip.

**Execution (dag t+1, US500cash) — D-100 session-flat:**
3. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
4. Exit: flat ≤ **21:00 CET** same day. **No overnight.**
5. Non-overlapping (≤1/day).

## Pre-screen
- Data: Yahoo/proxy `data/daily/EFA.csv` + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **2,34** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N123. FAIL → STOP (geen thr-grid, geen EEM rewrite→N121 clone, geen EMB twin, geen overnight, geen soft gate).
