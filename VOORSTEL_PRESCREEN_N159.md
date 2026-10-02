# VOORSTEL_PRESCREEN_N159 — GER40_EUROPE_CLOSE_FADE session-flat (NEW_FAMILY CB)

**Status:** **geen PREREG — CTO C-043 DIAG_FAIL** `c043` (2026-10-03 ~01:53 CEST). N=141, mean **−4,34 < 2,16** (also N<150; med −1,80; years —/−2,99/−7,13; L/S 70/71). Matches Faraday in-flight D-092.1. Not clone of N156/N149/N154/N138/N103/N40/N21. No XAU/GER remap, no thr-grid, no overnight.

**Auteur:** Strateeg (Grok). **NEW_FAMILY CB** (DAX **Europe-close fade**, one index CFD, session-flat). Round-trip is in `COSTS_FTMO.csv`. Not a gold/index pair. Not an FX book. Not a G10 cross. Not silver/index. Not metal–oil. Not an equity-factor z→US500. Not a transatlantic index pair.  
**Signal:** M5 impulse on **GER40cash** 12:00→15:00 CET. **Trade:** the same leg, 15:30→17:30.  
**Track 4 + D-100:** the cash DAX into the Europe close overshoots; fade it across the US handoff and be flat before the US afternoon. Swap stays 0.

**Gate (`COSTS_FTMO.csv`):** GER40cash RT **0,72** → gate 3 × 0,72 = **2,16** bp. Swap 0 (session-flat). No second leg. No XAU leg. No US100 leg.

**D-094a:** train 2021–2023. Reden **(b)**: GER40cash M5 from 2021-01. 2021 has a thin 15:30 print (seen on N149/N154/N156); that is a data fact, not a reason to move the clock or to call DIAG before the screen. Mechanism is a one-leg DAX fade, not XAU/GER, not EUR/GER, not US100/GER.

**Onderscheid:**
- ≠ **N156** XAU/GER40 / **N157** XAU/US100 (no gold leg)
- ≠ **N154** US100/GER40 / **N149** EUR/GER40 / **N138** GER/UK (one leg; no pair)
- ≠ **N103** GER→US30 lead-lag (no US30 leg; fade, not a lead)
- ≠ **N40** GER mid-morning continuation (that continues 09:30→12:00 and flats at 14:00; this fades 12:00→15:00 into 15:30→17:30)
- ≠ **N9** XETRA-open fade (different clock)
- ≠ **N158** USOIL NY fade (other OPEN; do not pool)
- ≠ factor→US500 / silver/index / metal–oil / FX-cross

## Regel
**Signal (dag t, GER40cash):**
1. `P0` = first M5 ≥ **12:00 CET** (span ≤15 min). `P1` = first M5 ≥ **15:00 CET** (span ≤15 min). Either missing → skip.
2. `eu_bp = 1e4 × (P1 / P0 − 1)`.
3. **fade:** `eu_bp ≥ +40` → **SHORT**; `eu_bp ≤ −40` → **LONG**; else skip. Threshold frozen — no grid.

**Execution (same day) — D-100 session-flat:**
4. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Exit: last M5 ≤ **17:30 CET**. **No overnight.** Missing entry bar → skip.
5. PnL bp = signed return of the one leg. Non-overlapping (≤1 trade/day).

**Future clone bar (precommitted):** FAIL_CLONE if (sign agree ≥ 0,85 AND cover ≥ 0,70) vs the GER leg of N156, vs N149, vs N154, vs N103's GER-AM sign, or vs the negative of N40's continuation sign. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/GER40cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **2,16** bp, **N ≥ 150**.
- PASS → PREREG. FAIL → STOP (geen XAU/GER remap, geen US100/GER remap, geen EUR leg, geen thr-grid, geen overnight, geen soft gate).
