# VOORSTEL_PRESCREEN_N120 — VNQ_REIT_STRESS → US500cash session-flat (NEW_FAMILY AO)

**Status:** **FAIL** — Faraday D-092.1 2026-10-02 ~23:23 CEST (n=342 mean −0.38 < gate 2.34). Absorbed CTO C-038. Geen PREREG. Dead += N120_VNQ_REIT_STRESS (≠ TLT/TIP/ratio clones).
**Auteur:** Strateeg (Grok). **NEW_FAMILY AO** (US REIT ETF **level** stress → equity session-flat — commercial real-estate / rate-sensitive equity channel; ≠ TLT/TIP bond duration; ≠ VNQ/TLT **ratio**).  
**Signal:** Yahoo/proxy **VNQ** (US REIT ETF). **Trade:** `US500cash` (RT **0,78** bp; swap 0 — **session-flat**).  
**Track 4 + D-100:** REIT equity-beta stress as risk-appetite timing for DM large-cap; intradag-vlak (geen swap).

**Gate:** 3 × US500 RT = 3 × 0,78 = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: VNQ **level** as commercial RE / rate-sensitive equity stress into US500 beta — distinct from TLT nominal duration (N116 DEAD), TIP real-rate (N118 DEAD), and from VNQ/TLT **ratio** rewrite. FTMO-M5 for costs. Herhaal in PREREG.

**Onderscheid:**
- ≠ **N116 TLT** FAIL_T / **N118 TIP** FAIL_T (bond duration/real-rate ≠ REIT **equity** level)
- ≠ REIT_RATE **VNQ/TLT ratio** (this = VNQ level alone → equity)
- ≠ **N114 HYG** / **N100 EMB** / **N112 GAS** / **N113 SILVER_GOLD** / **N117 CPER**
- ≠ **N119 IWM** FAIL / SECTOR_DISP / VIX / L60 / ORB-meta / UKOIL-OVN / CORN / N75–N119 clones / VNQ CFD trade leg

## Regel
**Signal (dag t):**
1. `z120 = (VNQ_t − mean_120(VNQ)) / stdev_120(VNQ)`; `d20 = VNQ_t / VNQ_{t−20} − 1`.
2. **combo:** `(z120 > +0,5) and (d20 > 0)` → **LONG** US500 (REIT relief = easier financial conditions); `(z120 < −0,5) and (d20 < 0)` → **SHORT** (REIT crash = rates/credit stress into large-cap); else skip.

**Execution (dag t+1, US500cash) — D-100 session-flat:**
3. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
4. Exit: flat ≤ **21:00 CET** same day. **No overnight.**
5. Non-overlapping (≤1/day).

## Pre-screen
- Data: Yahoo/proxy `data/daily/VNQ.csv` + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **2,34** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N120. FAIL → STOP (geen thr-grid, geen VNQ/TLT ratio rewrite, geen TLT/TIP twin, geen overnight, geen soft gate).
