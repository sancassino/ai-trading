# VOORSTEL_PRESCREEN_N109 — CHFJPY Long-Only 5d CHF-JPY Carry+Momentum (NEW_FAMILY AF)

**Status:** **UNDERPOWERED** D-092.1 `n108_n109` (mean **+19,69 ≥ 4,23** maar **N=122≪150**); geen PREREG; screened 2026-10-02 ~22:20 CEST.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY AF** (CHFJPY CHF-vs-JPY safe-haven cross carry+momentum long-only — nooit als deze setup).  
**Instrument:** `CHFJPY` (RT **est. 1,41** bp — M5 spread_med≈0,81 bp 2024–26 + FX commissie≈0,30×2; **not in** `COSTS_FTMO.csv` — U2 remeasure before any PREREG; swap_long CHF vs JPY = typically earn vs funding JPY → 0 in gate per D-100).  
**Track 4 + D-100 family B:** CHFJPY long-only 5d swing. Long = CHF vs JPY (SNB vs BoJ funding / safe-haven cross) + positief 5d momentum.

**Gate (long-only; 4 nachten; swap earn → 0 in gate per D-100):**  
1,41 → gate 3 × 1,41 = **4,23** bp.  
(Swap-credit telt NIET als alfa; bruto = signed prijsrendement.)

**D-094a:** train 2021–2023. Reden **(b)**: FX carry + TSMOM on CHF/JPY (Menkhoff et al. 2012; JPY funding vs CHF; FTMO-M5 = kosten). Herhaal in PREREG. ≥5y proxy + FTMO-M5 train.

**Onderscheid:**
- ≠ **N96** CADJPY LO UNDERPOWERED / **N94** NZDJPY FAIL / **N90** GBPJPY UNDERPOWERED (CAD/NZD/GBP ≠ CHF)
- ≠ **USDJPY_MED / EURJPY_MED** L60 BARRED/FAIL_T (L60 medium ≠ 5d LO; USD/EUR ≠ CHF)
- ≠ **N102** USDCHF / **N104** GBPCHF UNDERPOWERED / **N99** CADCHF DIAG (JPY≠CHF quote)
- ≠ **N106** EURNZD FAIL / EMB / CRACK / SECTOR_DISP / VIX / ORB / L60 / UKOIL-OVN / CORN / N75–N108 restarts

## Regel
- `ret5 = close_t / close_{t−5} − 1` (dagclose uit M5; laatste bar ≤22:00 CET)
- `ret5 > 0` → **LONG** op close_t
- `ret5 ≤ 0` → skip (geen short-been; short CHFJPY swap structureel duurder vs long earn)
- Hold: exit close_{t+5}. **Non-overlapping**. Alleen LONG.

## Pre-screen
- Data: `data/m5gz/CHFJPY.csv.gz` → dagclose, train **2021-01-01 … 2023-12-31**.
- Gate: mean bruto ≥ **4,23** bp, N ≥ 150.
- PASS → PREREG_FTMO_N109. FAIL → STOP (geen ret10-switch, geen CADJPY/NZDJPY twin, geen L60 rewrite, geen soft gate).
