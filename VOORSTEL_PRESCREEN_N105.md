# VOORSTEL_PRESCREEN_N105 — JP225 Tokyo-AM → Lon continuation session-flat (NEW_FAMILY AB)

**Status:** **geen PREREG — D-092.1 FAIL** `n104_n105` (N=392, mean **−2,77 < 4,53**); Asia-open fallback [00:00,01:15] CET (filed 2026-10-02 ~22:15 CEST).  
**Auteur:** Strateeg (Grok). **NEW_FAMILY AB** (Nikkei Tokyo-AM impulse → London-hours same-dir continuation, EOD flat — nooit deze setup).  
**Instrument:** `JP225cash` (RT **est. 1,51** bp — M5 spread_med≈1,51 bp 2024–26; indices commissie 0; **not in** `COSTS_FTMO.csv` — U2 remeasure before any PREREG; swap 0 — **EOD flat**).  
**Track 2 + D-100:** Asia equity open risk impulse → Europe-hours continuation on same index; intradag-vlak (geen swap).

**Gate:** 3 × JP225 RT_est = 3 × 1,51 = **4,53** bp.

**D-094a:** train 2021–2023. Reden **(b)**: Tokyo cash-session impulse persists into London liquidity window (Asia→Europe equity handoff on Nikkei); classic microstructure lead within one index, not cross-Atlantic equity lag. FTMO-M5. Herhaal in PREREG.

**Onderscheid:**
- ≠ **N103** GER40→US30 industrial lag (EU→US cross-index; dit = **JP225→JP225** Asia→Lon same-index)
- ≠ **N45** ETH Asia→EU DIAG_FAIL (crypto; dit = equity index)
- ≠ **N64** HK50 short-only TSMOM UNDERPOWERED (HK≠JP; multi-day SO ≠ intradag cont)
- ≠ **N41 / N35 / N85** EU/US lead-lag FAIL / DIAG
- ≠ **N98** USOIL→US100 / EMB / CRACK / SECTOR_DISP / VIX / ORB / L60 / UKOIL-OVN / CORN / NY-2h / N75–N103 restarts

## Regel
1. Tokyo-AM JP impulse: `jp_am_bp = 1e4 × (JP225cash_close@06:00 / JP225cash_close@AsiaOpen − 1)` — AsiaOpen = first M5 in [00:00, 00:15] CET, else first in [00:00, 01:15] (FTMO JP225 often starts ~01:00).
2. Trade only if `|jp_am_bp| ≥ 40`.
3. Same-direction: jp_am ≥ +40 → **LONG** JP225; jp_am ≤ −40 → **SHORT** JP225.
4. Entry: JP225 close of first M5 in **[08:00, 08:15] CET**. If missing, skip day.
5. Exit: flat at **14:00 CET** same day (vóór US cash open). **No overnight.**
6. Non-overlapping (≤1/day).

## Pre-screen
- Data: `data/m5gz/JP225cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **4,53** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N105. FAIL → STOP (geen thr-grid, geen HK50 substitute → N64-adjacent, geen US-open extension, geen overnight).
