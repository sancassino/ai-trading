# VOORSTEL_PRESCREEN_N108 — AUS200 Asia-AM → Lon continuation session-flat (NEW_FAMILY AE)

**Status:** **geen PREREG — D-092.1 FAIL** `n108_n109` (N=242, mean **−4,86 < 4,38**; years −5,63/−5,08/−3,49); screened 2026-10-02 ~22:20 CEST.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY AE** (ASX Asia-session impulse → London morning same-dir continuation, EOD-session flat — nooit deze setup).  
**Instrument:** `AUS200cash` (RT **est. 1,46** bp — M5 spread_med≈1,46 bp 2024–26 00–12h CET; indices commissie 0; **not in** `COSTS_FTMO.csv` — U2 remeasure before any PREREG; swap 0 — **session-flat**).  
**Track 2 + D-100:** AU equity Asia risk handoff into Lon cash; intradag-vlak (geen swap).

**Gate:** 3 × AUS200 RT_est = 3 × 1,46 = **4,38** bp.

**D-094a:** train 2021–2023. Reden **(b)**: Asia overnight AU equity impulse persists into London morning liquidity (ASX→Lon same-index handoff); microstructure Asia→Europe on AU beta, not JP225 and not cross-Atlantic. FTMO-M5. Herhaal in PREREG.

**Onderscheid:**
- ≠ **N105** JP225 Tokyo→Lon FAIL (JP≠AU; Nikkei≠ASX)
- ≠ **N61** AUS200 short-only TSMOM overnight FAIL (dit = **intradag session-flat cont**, geen overnight SO)
- ≠ **N103** GER→US30 FAIL_STRESS / **N107** UK→FRA40 FAIL (intra-EU / cross-Atlantic)
- ≠ EMB / CRACK / SECTOR_DISP / VIX / ORB / L60 / UKOIL-OVN / CORN / N75–N107 restarts

## Regel
1. Asia-AM AUS impulse: `aus_asia_bp = 1e4 × (AUS200cash_close@07:00 / AUS200cash_close@01:00 − 1)` (first M5 in ±15 min; CET). Fallback open window [01:00, 01:30] if exact miss.
2. Trade only if `|aus_asia_bp| ≥ 40`.
3. Same-direction: aus_asia ≥ +40 → **LONG**; ≤ −40 → **SHORT**.
4. Entry: close of first M5 in **[08:00, 08:15] CET**. If missing, skip day.
5. Exit: flat at **12:00 CET** same day (vóór EU afternoon / US prep). **No overnight.**
6. Non-overlapping (≤1/day).

## Pre-screen
- Data: `data/m5gz/AUS200cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **4,38** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N108. FAIL → STOP (geen thr-grid, geen HK50/JP225 substitute, geen overnight TSMOM rewrite, geen soft gate).
