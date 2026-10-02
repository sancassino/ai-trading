# VOORSTEL_PRESCREEN_N107 — UK100 Lon-AM → FRA40 afternoon continuation session-flat (NEW_FAMILY AD)

**Status:** **OPEN** — pipeline replace after U2 N103 FAIL_STRESS (filed 2026-10-02 ~22:15 CEST).  
**Auteur:** Strateeg (Grok). **NEW_FAMILY AD** (FTSE Lon-AM impulse → CAC40 EU-afternoon same-dir continuation, EOD flat — nooit deze setup).  
**Signal:** `UK100cash` (Lon-AM impulse). **Trade:** `FRA40cash` (RT **est. 1,98** bp — M5 spread_med≈1,98 bp 2024–26; indices commissie 0; **not in** `COSTS_FTMO.csv` — U2 remeasure before any PREREG; swap 0 — **EOD flat**).  
**Track 2 + D-100:** Intra-Europe equity lead–lag (UK morning risk → French equity afternoon); intradag-vlak (geen swap).

**Gate:** 3 × FRA40 RT_est = 3 × 1,98 = **5,94** bp.

**D-094a:** train 2021–2023. Reden **(b)**: UK cash-session morning impulse persists into continental EU afternoon liquidity (FTSE→CAC same-region equity handoff); microstructure lead within Europe, not Asia→Lon and not cross-Atlantic industrial. FTMO-M5. Herhaal in PREREG.

**Onderscheid:**
- ≠ **N105** JP225 Tokyo→Lon OPEN (Asia→Europe **same-index**; dit = **UK→FR cross-index** Lon-AM→EU-PM)
- ≠ **N103** GER40→US30 FAIL_STRESS (cross-Atlantic industrial; dit = **intra-Europe** UK→FRA40)
- ≠ **S2-GER_US_LEAD** / **N41/N35/N85** EU↔US FAIL
- ≠ **N98** USOIL→US100 / EMB / CRACK / SECTOR_DISP / VIX / ORB / L60 / UKOIL-OVN / CORN / N75–N105 restarts

## Regel
1. Lon-AM UK impulse: `uk_am_bp = 1e4 × (UK100cash_close@12:00 / UK100cash_close@08:00 − 1)` (first M5 in ±15 min windows; CET).
2. Trade only if `|uk_am_bp| ≥ 40`.
3. Same-direction FRA40: uk_am ≥ +40 → **LONG** FRA40; uk_am ≤ −40 → **SHORT** FRA40.
4. Entry: FRA40 close of first M5 in **[13:00, 13:15] CET**. If missing, skip day.
5. Exit: flat at **17:30 CET** same day (vóór US cash open). **No overnight.**
6. Non-overlapping (≤1/day).

## Pre-screen
- Data: `data/m5gz/UK100cash.csv.gz` + `data/m5gz/FRA40cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **5,94** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N107. FAIL → STOP (geen thr-grid, geen EU50 substitute → high-RT, geen GER→US rewrite, geen overnight).
