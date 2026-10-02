# VOORSTEL_PRESCREEN_N111 — GBPAUD Long-Only 5d GBP-AUD Carry+Momentum (NEW_FAMILY AH)

**Status:** **OPEN** — pipeline replace after N108 FAIL / N109 UNDERPOWERED (filed 2026-10-02 ~22:25 CEST).  
**Auteur:** Strateeg (Grok). **NEW_FAMILY AH** (GBPAUD sterling-vs-AUD commodity carry+momentum long-only — nooit als deze setup).  
**Instrument:** `GBPAUD` (RT **est. 1,46** bp — M5 spread_med≈0,86 bp 2024–26 + FX commissie≈0,30×2; **not in** `COSTS_FTMO.csv` — U2 remeasure before any PREREG; swap_long GBP vs AUD = typically earn when AU rates > UK? U2 check — if long pays, fail-closed; assume earn → 0 in gate per D-100 pending U2).  
**Track 4 + D-100 family B:** GBPAUD long-only 5d swing. Long = GBP vs AUD (BoE vs RBA / commodity FX) + positief 5d momentum.

**Gate (long-only; 4 nachten; swap earn → 0 in gate per D-100):**  
1,46 → gate 3 × 1,46 = **4,38** bp.  
(Swap-credit telt NIET als alfa; bruto = signed prijsrendement.)

**D-094a:** train 2021–2023. Reden **(b)**: FX carry + TSMOM on GBP/AUD (Menkhoff et al. 2012; sterling vs commodity AUD; FTMO-M5 = kosten). Herhaal in PREREG.

**Onderscheid:**
- ≠ **N97** AUDCAD FAIL / **N91** AUDUSD DIAG / **N106** EURNZD FAIL (GBP≠EUR/AUD-base)
- ≠ **N104** GBPCHF UNDERPOWERED / **N90** GBPJPY UNDERPOWERED (AUD≠CHF/JPY)
- ≠ **N109** CHFJPY UNDERPOWERED / **N102** USDCHF FAIL
- ≠ EMB / CRACK / SECTOR_DISP / VIX / ORB / L60 / UKOIL-OVN / CORN / Asia→Lon equity / N75–N110 restarts

## Regel
- `ret5 = close_t / close_{t−5} − 1` (dagclose uit M5; laatste bar ≤22:00 CET)
- `ret5 > 0` → **LONG** op close_t
- `ret5 ≤ 0` → skip (geen short-been)
- Hold: exit close_{t+5}. **Non-overlapping**. Alleen LONG.

## Pre-screen
- Data: `data/m5gz/GBPAUD.csv.gz` → dagclose, train **2021-01-01 … 2023-12-31**.
- Gate: mean bruto ≥ **4,38** bp, N ≥ 150.
- PASS → PREREG_FTMO_N111. FAIL → STOP (geen ret10-switch, geen EURAUD/AUDCAD twin, geen L60 rewrite, geen soft gate).
