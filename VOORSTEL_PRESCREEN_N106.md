# VOORSTEL_PRESCREEN_N106 — EURNZD Long-Only 5d EUR-NZD Carry+Momentum (NEW_FAMILY AC)

**Status:** **geen PREREG — D-092.1 FAIL** `n106_n107` (N=103, mean **+3,45 < 4,11**; years −7,60/+18,64/−0,76); filed 2026-10-02 ~22:15, screened ~22:20 CEST.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY AC** (EURNZD EUR-vs-NZD dairy/commodity carry+momentum long-only — nooit als deze setup).  
**Instrument:** `EURNZD` (RT **est. 1,37** bp — M5 spread_med≈0,77 bp 2024–26 + FX commissie≈0,30×2; **not in** `COSTS_FTMO.csv` — U2 remeasure before any PREREG; swap_long EUR vs NZD = typically earn when NZ rates > EUR → 0 in gate per D-100).  
**Track 4 + D-100 family B:** EURNZD long-only 5d swing. Long = EUR vs NZD (Euro funding vs NZ dairy/commodity FX) + positief 5d momentum.

**Gate (long-only; 4 nachten; swap earn → 0 in gate per D-100):**  
1,37 → gate 3 × 1,37 = **4,11** bp.  
(Swap-credit telt NIET als alfa; bruto = signed prijsrendement.)

**D-094a:** train 2021–2023. Reden **(b)**: FX carry + TSMOM on EUR/NZD (Menkhoff et al. 2012; NZ as commodity/dairy currency vs EUR funding; FTMO-M5 = kosten). Herhaal in PREREG. ≥5y proxy + FTMO-M5 train.

**Onderscheid:**
- ≠ **N104** GBPCHF LO OPEN (GBP≠EUR; CHF≠NZD; sterling-funding vs EUR-NZ dairy)
- ≠ **N94** NZDJPY FAIL / **N97** AUDCAD FAIL / **N99** CADCHF DIAG / **N102** USDCHF FAIL
- ≠ **N90** GBPJPY / **N91** AUDUSD / **N96** CADJPY UNDERPOWERED
- ≠ EMB / CRACK / SECTOR_DISP / VIX / ORB-meta / UKOIL-OVN / CORN / L60 / GER40→US30 / N75–N105 restarts

## Regel
- `ret5 = close_t / close_{t−5} − 1` (dagclose uit M5; laatste bar ≤22:00 CET)
- `ret5 > 0` → **LONG** op close_t
- `ret5 ≤ 0` → skip (geen short-been; short EURNZD swap structureel duurder vs long)
- Hold: exit close_{t+5}. **Non-overlapping**. Alleen LONG.

## Pre-screen
- Data: `data/m5gz/EURNZD.csv.gz` → dagclose, train **2021-01-01 … 2023-12-31**.
- Gate: mean bruto ≥ **4,11** bp, N ≥ 150.
- PASS → PREREG_FTMO_N106. FAIL → STOP (geen ret10-switch, geen NZDJPY/AUDNZD twin, geen L60 rewrite, geen soft gate).
