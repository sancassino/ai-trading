# VOORSTEL_PRESCREEN_N165 — EURCHF_LONDON_HAVEN_FADE session-flat (NEW_FAMILY CH)

**Status:** **DIAG_FAIL** (C-045 — n=259 mean −2.233 < gate 3.45; day_t −1.868; no clone hit — GBPCHF agree 0.92 cover 0.66 / USDCHF 0.82/0.54 / AUDCHF 0.88/0.66) — D-094 refill after C-044 closed N162/N163 DIAG_FAIL_CLONE + N161 FAIL_T (filed 2026-10-03 ~23:21 CEST). Not cost-screened.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY CH** (EURCHF **London-AM haven impulse fade**, one FX haven leg, Europe session-flat). Round-trip **not** in `COSTS_FTMO.csv` — honest M5 spread_med ≈ **0,63** bp + commission ≈ **0,26**/side (EURUSD-like €2,25/lot) → RT_est **1,15** bp; U2 remeasure before any PREREG. Not GBPCHF/CADCHF LO carry. Not AUD NY-fade. Not G10 cross XS. Not ETF→index.  
**Signal:** M5 impulse on **EURCHF** 08:00→11:30 CET. **Trade:** the same leg, flat by **15:00 CET** (before US cash open).  
**Track 2 + D-100 + family pivot:** CHF haven flow in the London morning overshoots; fade it and be flat before NY so the book is pure Europe-session, swap 0, and orthogonal to the NY-impulse / sector-stress dead set.

**Gate (est.):** EURCHF RT_est **1,15** → gate 3 × 1,15 = **3,45** bp. Swap 0 (flat 15:00). Binding RT = max(est, U2) before PREREG. No GBPCHF/USDCHF/AUDCHF twin. No NZD/AUD NY remap.

**D-094a:** train 2021–2023. Reden **(b)**: EURCHF M5 from 2021-01 (n_train ≈ 222k bars). London-AM |move| on EURCHF is modest (expect p50≈10–15 bp) — threshold **±15** frozen a priori (not chosen on PnL). Mechanism is a same-day fade of EUR/CHF haven impulse in London, not LO carry, not NY commodity-FX fade, not a cross basket.

**Pre-file clone check (qualitative; not a cost screen):** not a filed clone by construction.  
≠ N104 GBPCHF LO UNDERPOWERED (intradag fade ≠ month LO carry; EURCHF ≠ GBPCHF). ≠ CADCHF LO barred. ≠ N163 AUD NY-fade (London window; haven CHF ≠ commodity AUD; flat 15:00 ≠ 21:00). ≠ N151 EURJPY/USDCHF funding XS (one EURCHF leg). ≠ inline USDCHF/USDJPY. ≠ L60 FX-med. ≠ FX_INTRADAG London ORB (fade of 3,5h impulse, not OR-break).

**Same-family twins must not be filed after a clone hit:** GBPCHF / USDCHF / AUDCHF / NZDCHF same London-AM fade window.

**Onderscheid:**
- ≠ **N104** GBPCHF LO / **CADCHF-LO** barred / **AUDCHF** stretch
- ≠ **N163** AUDUSD NY-fade DIAG_FAIL_CLONE (other session + other pair)
- ≠ **N151** EURJPY–USDCHF XS / **N047** USDCHF Asia→Lon
- ≠ **FX_INTRADAG** / **A5** London ORB STOP
- ≠ **N161** XLK→US100 / ETF→index stress family
- ≠ G10 FX-cross stretch (N152–N153 closed)

## Regel
**Signal (dag t, EURCHF):**
1. `P0` = first M5 ≥ **08:00 CET** (span ≤15 min). `P1` = first M5 ≥ **11:30 CET** (span ≤15 min). Either missing → skip.
2. `lon_bp = 1e4 × (P1 / P0 − 1)`.
3. **fade:** `lon_bp ≥ +15` → **SHORT** at P1; `lon_bp ≤ −15` → **LONG** at P1; else skip. Threshold frozen — no grid.

**Execution (same day) — D-100 Europe session-flat:**
4. Entry = that 11:30 bar. Exit: last M5 ≤ **15:00 CET**. **No overnight. No US-session hold.**
5. PnL bp = signed return of the one leg. Non-overlapping (≤1 trade/day).

**Future clone bar (precommitted):** FAIL_CLONE if (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N104 GBPCHF sign, vs CADCHF LO sign, vs N163 AUD NY-fade sign, vs N47 USDCHF Asia→Lon, vs a GBPCHF/USDCHF/AUDCHF same-window London fade. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/EURCHF.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **3,45** bp (or U2-remeasured 3×RT), **N ≥ 150**.
- PASS → PREREG. FAIL → STOP (geen GBPCHF/USDCHF/AUDCHF twin, geen NY remap, geen LO carry rewrite, geen thr-grid, geen overnight, geen soft gate).
