# VOORSTEL_PRESCREEN_N121 — EEM_EM_EQUITY_STRESS → US500cash session-flat (NEW_FAMILY AP)

**Status:** **FAIL** — Faraday D-092.1 2026-10-02 ~23:23 CEST (n=172 mean +0.08 < gate 2.34). Absorbed CTO C-038. Geen PREREG. Dead += N121_EEM_EM_EQUITY_STRESS (≠ EMB clones).
**Auteur:** Strateeg (Grok). **NEW_FAMILY AP** (EM equity ETF **level** stress → DM large-cap session-flat — EM risk-appetite / growth channel; **≠ EMB** EM hard-currency credit).  
**Signal:** Yahoo/proxy **EEM** (MSCI EM equity ETF). **Trade:** `US500cash` (RT **0,78** bp; swap 0 — **session-flat**).  
**Track 4 + D-100:** EM equity stress as global risk-appetite timing for US large-cap; intradag-vlak (geen swap).

**Gate:** 3 × US500 RT = 3 × 0,78 = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: EEM as EM **equity** level stress into US500 beta — distinct from EMB EM bond/credit (N100 DEAD) and from IWM small-cap (N119 FAIL). FTMO-M5 for costs. Herhaal in PREREG.

**Onderscheid:**
- ≠ **N100 EMB_CREDIT_STRESS** FAIL_T (EM **bonds/credit** ≠ EM **equity** level)
- ≠ **N119 IWM_SMALLCAP** D-092.1 FAIL (US small-cap ≠ EM equity)
- ≠ **N114 HYG** / **N116 TLT** / **N117 CPER** / **N118 TIP** / GAS / SILVER_GOLD
- ≠ VIX / SECTOR_DISP / L60 / ORB-meta / UKOIL-OVN / CORN / N75–N120 clones / EEM CFD trade leg

## Regel
**Signal (dag t):**
1. `z40 = (EEM_t − mean_40(EEM)) / stdev_40(EEM)`.
2. **stress_buy:** `z40 > +1,5` → **SHORT** US500 (EM equity spike = crowded risk-on fade into DM); `z40 < −1,5` → **LONG** (EM crash = growth-scare bounce / relief into DM); else skip.

**Execution (dag t+1, US500cash) — D-100 session-flat:**
3. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
4. Exit: flat ≤ **21:00 CET** same day. **No overnight.**
5. Non-overlapping (≤1/day).

## Pre-screen
- Data: Yahoo/proxy `data/daily/EEM.csv` + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **2,34** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N121. FAIL → STOP (geen thr-grid, geen EMB rewrite→N100 clone, geen IWM twin, geen overnight, geen soft gate).
