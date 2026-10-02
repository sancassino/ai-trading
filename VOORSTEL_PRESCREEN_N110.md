# VOORSTEL_PRESCREEN_N110 — DXYcash Lon-AM → EU-afternoon continuation session-flat (NEW_FAMILY AG)

**Status:** **DIAG_FAIL** C-036 (`f3cf632`) — DATA_GAP: DXYcash M5 starts 2024-11-26; train 2021–23 empty (n=0). Geen PREREG; geen soft gate on 2024-only. Dead += N110; no DXY Lon→EU-PM clones. Filed OPEN 2026-10-02 ~22:25; closed ~22:57 CEST.
**Auteur:** Strateeg (Grok). **NEW_FAMILY AG** (DXY Lon-AM impulse → same-dir EU-afternoon continuation on dollar index CFD, session-flat — nooit deze setup).  
**Instrument:** `DXYcash` (RT **est. 2,62** bp — M5 spread_med≈2,62 bp 2024–26; **not in** `COSTS_FTMO.csv` — U2 remeasure before any PREREG; swap 0 — **session-flat**).  
**Track 2 + D-100:** USD trade-weighted impulse persists from Lon morning into EU afternoon; intradag-vlak (geen swap).

**Gate:** 3 × DXY RT_est = 3 × 2,62 = **7,86** bp.

**D-094a:** train 2021–2023. Reden **(b)**: dollar-index morning risk (DXY) continues into EU afternoon liquidity; macro USD beta, not single FX pair and not equity lead–lag. FTMO-M5. Herhaal in PREREG.

**Onderscheid:**
- ≠ **N108** AUS200 Asia→Lon FAIL / **N105** JP225 Tokyo→Lon FAIL (equity Asia→Lon ≠ DXY Lon→EU-PM)
- ≠ **N107** UK→FRA40 FAIL / **N103** GER→US30 FAIL_STRESS (equity lead–lag ≠ dollar index)
- ≠ FX LO 5d set (N90–N109) / EMB / CRACK / SECTOR_DISP / VIX / ORB / L60 / UKOIL-OVN / CORN / N75–N109 restarts

## Regel
1. Lon-AM DXY impulse: `dxy_am_bp = 1e4 × (DXYcash_close@12:00 / DXYcash_close@08:00 − 1)` (first M5 in ±15 min; CET).
2. Trade only if `|dxy_am_bp| ≥ 25` (DXY daily ranges smaller than equity; thr fixed a priori).
3. Same-direction: dxy_am ≥ +25 → **LONG** DXY; ≤ −25 → **SHORT** DXY.
4. Entry: close of first M5 in **[13:00, 13:15] CET**. If missing, skip day.
5. Exit: flat at **17:00 CET** same day (vóór US cash open). **No overnight.**
6. Non-overlapping (≤1/day).

## Pre-screen
- Data: `data/m5gz/DXYcash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **7,86** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N110. FAIL → STOP (geen thr-grid after freeze, geen EURUSD substitute, geen overnight, geen soft gate).
