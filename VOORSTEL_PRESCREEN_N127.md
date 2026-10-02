# VOORSTEL_PRESCREEN_N127 — EWZ_BRAZIL_STRESS → US500cash session-flat (NEW_FAMILY AV)

**Status:** **STOP FAIL_T** — U2 `3a970c7` (cost+stress PASS; t_netto/t_NW5 **0,57/0,50**; test N=85 bruto **+1,85**; TRIAL **466→467**). Dead += N127; no EWZ/EEM/EMB/EFA clones. Pre-screen was PASS (+3,54; N=208).
**Auteur:** Strateeg (Grok). **NEW_FAMILY AV** (Brazil single-country EM equity ETF **level** stress → US large-cap session-flat — LatAm / commodity-FX equity channel; **≠ EEM** EM basket / **≠ EMB** EM credit / **≠ EFA** DM ex-US).  
**Signal:** Yahoo/proxy **EWZ** (iShares MSCI Brazil). **Trade:** `US500cash` (RT **0,78** bp; swap 0 — **session-flat**).  
**Track 4 + D-100:** Brazil equity stress as EM/commodity-FX risk-appetite timing for US large-cap; intradag-vlak (geen swap).

**Gate:** 3 × US500 RT = 3 × 0,78 = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: EWZ as **single-country Brazil** equity level stress into US500 beta — distinct from EEM EM basket (N121 FAIL), EMB EM credit (N100 DEAD), EFA DM ex-US (N123 DIAG_FAIL C-038). FTMO-M5 for costs. Herhaal in PREREG.

**Onderscheid:**
- ≠ **N121 EEM** D-092.1 FAIL (EM basket ≠ Brazil solo)
- ≠ **N100 EMB** FAIL_T (EM bonds ≠ Brazil equity) / **N123 EFA** DIAG_FAIL (DM ex-US ≠ Brazil)
- ≠ **N124/N125** / TLT/TIP/HYG/VNQ/IWM/GAS/CPER/SILVER/SECTOR_DISP/VIX
- ≠ N75–N126 clones / EWZ CFD trade leg / overnight / thr-grid / soft gate

## Regel
**Signal (dag t):**
1. `z40 = (EWZ_t − mean_40(EWZ)) / stdev_40(EWZ)`.
2. **stress_buy:** `z40 > +1,5` → **SHORT** US500 (Brazil spike = crowded EM risk-on fade into US); `z40 < −1,5` → **LONG** (Brazil crash = EM scare bounce into US); else skip.

**Execution (dag t+1, US500cash) — D-100 session-flat:**
3. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
4. Exit: flat ≤ **21:00 CET** same day. **No overnight.**
5. Non-overlapping (≤1/day).

## Pre-screen
- Data: Yahoo/proxy `data/daily/EWZ.csv` + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **2,34** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N127. FAIL → STOP (geen thr-grid, geen EEM rewrite→N121 clone, geen EMB twin, geen overnight, geen soft gate).
