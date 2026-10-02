# VOORSTEL_PRESCREEN_N114 — HYG_CREDIT_STRESS → US500cash session-flat (NEW_FAMILY AI)

**Status:** **OPEN** — pipeline refill after C-036 closed N104–N111 (filed 2026-10-02 ~22:57 CEST).  
**Auteur:** Strateeg (Grok). **NEW_FAMILY AI** (US domestic HY credit stress → equity session-flat — nooit als EMB-twin).  
**Signal:** Yahoo/proxy **HYG** (US high-yield corporate bond ETF). **Trade:** `US500cash` (RT **0,78** bp; swap 0 — **session-flat**).  
**Track 4 + D-100:** Domestic HY credit level+trend as risk-appetite timing for DM equity; intradag-vlak (geen swap).

**Gate:** 3 × US500 RT = 3 × 0,78 = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: US HY credit spread/level (HYG) as domestic risk-appetite signal into equity beta — literature on credit–equity co-movement; **distinct from EMB** (EM hard-currency) which already reserved this as CREDIT_SPREAD_PROXY. FTMO-M5 for costs. Herhaal in PREREG.

**Onderscheid:**
- ≠ **N100 EMB_CREDIT_STRESS** FAIL_T (EM hard-currency bond ETF ≠ US domestic HY)
- ≠ **N93 SECTOR_DISP** / **N78 VIX_TERM** / **N112 GAS** / **N113 SILVER_GOLD**
- ≠ FX LO carry set / L60 / ORB-meta / UKOIL-OVN / CORN / GER→US30 / N75–N111 restarts

## Regel
**Signal (dag t):**
1. `z120 = (HYG_t − mean_120(HYG)) / stdev_120(HYG)`; `d20 = HYG_t / HYG_{t−20} − 1`.
2. **combo:** `(z120 > +0,5) and (d20 > 0)` → **LONG**; `(z120 < −0,5) and (d20 < 0)` → **SHORT**; else skip.

**Execution (dag t+1, US500cash) — D-100 session-flat:**
3. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
4. Exit: flat ≤ **21:00 CET** same day. **No overnight.**
5. Non-overlapping (≤1/day).

## Pre-screen
- Data: Yahoo/proxy `data/daily/HYG.csv` (or `data/yahoo/HYG.csv`) + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **2,34** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N114. FAIL → STOP (geen thr-grid, geen LQD twin, geen EMB rewrite, geen overnight, geen soft gate).
