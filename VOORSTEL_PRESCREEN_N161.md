# VOORSTEL_PRESCREEN_N161 — XLK_TECH_SECTOR_STRESS session-flat (NEW_FAMILY CD)

**Status:** **PREREG** — D-092.1 **PASS** `n160_n161` (2026-10-03 ~02:05 CEST). Train N=**383**, mean **+5,42 ≥ 1,98** (med +9,77; stress informal +5,42 ≥ 2,97; years −10,68/+6,84/+9,26; L/S 242/141; 137 signals skipped for a missing 15:30 bar — not DIAG). Not a clone. Actual trade vs DEFENSIVE XLU/XLI agree **0,73** cover **0,84** (cover high, agree under 0,85). vs N92 US100 NY-2h mom agree **0,49** cover **1,00**. Signal-day: SECTOR_DISP z −0,14 agree 0,67 cover 0,59; XLE z −0,16 agree 0,49 cover 0,56; DBC z −0,07 agree 0,43 cover 0,55; XLF z 0,45 agree 0,07 cover 0,33; XLU/XLI z −0,24 agree 0,64 cover 0,81; UNG z −0,03 agree 0,41 cover 0,38. Lane-A day_t **2,05 is not this PASS**. Session-flat, not hold=3d, not overnight long.  
**Auteur:** Strateeg (Grok), from Strateeg-2 `grok/strateeg-2` @ `51b24bf`, `results/strateeg2_prescreen/cycle_0147/`. **NEW_FAMILY CD** (XLK tech-sector stress → **US100cash** only, session-flat). US100 round-trip is in `COSTS_FTMO.csv`. Not a gold/index pair. Not an FX book. Not a G10 cross. Not metal–oil. Not silver/index. Not an oil sleeve. Not a GER40 session.  
**Signal:** daily **XLK** `z120` / thr **0,5** / **mom_confirm** (20d return same sign). **Trade:** US100cash the next cash session, flat the same day.  
**Track 4 + D-100:** S2 hold=3d on NDX is **not** the book. **Do not hold overnight long US100** (S2 FLAG; long-swap 1,95 is hostile). One session, swap 0.

**Gate (`COSTS_FTMO.csv`):** US100cash RT **0,66** → gate 3 × 0,66 = **1,98** bp. Swap 0 (session-flat). No US500 twin (S2 did not clear one). No XLK CFD leg.

**D-094a:** train 2021–2023. Reden **(b)**: XLK daily is long; US100cash M5 from 2021-01. Mechanism is tech-sector level plus momentum into the Nasdaq cash session, not energy-equity (XLE/DBC), not financials (XLF), not utilities-vs-industrials, not gas, not cross-sector dispersion.

**Pre-file clone check (train 2021–2023 sign/z only; not a cost screen):** not a clone (|z|≥0,90 or agree≥0,85 and cover≥0,70).  
SECTOR_DISP z **−0,14**, agree **0,67**, cover **0,59**. XLE z40 fade z **−0,16**, agree **0,49**, cover **0,56**. DBC z40 fade z **−0,07**, agree **0,43**, cover **0,55**. XLF z40 fade z **0,45**, agree **0,07**, cover **0,33**. XLU/XLI z40 thr 0,5 z **−0,24**, agree **0,64**, cover **0,81** (cover high, agree under the bar). UNG z40 stress z **−0,03**, agree **0,41**, cover **0,38**.

**Onderscheid:**
- ≠ **N160** XAG NY-fade (other OPEN; no silver leg; do not pool)
- ≠ **N93** SECTOR_DISP (dispersion of many XL*, not the XLK level)
- ≠ **N143** XLE / **DBC** (energy and broad commodity; this is tech)
- ≠ **N134** XLF (financials)
- ≠ **N125** DEFENSIVE XLU/XLI
- ≠ **N112** GAS / UNG
- ≠ **N158** oil NY-fade / **N159** GER40 Europe-close
- ≠ gold/index / FX-cross / metal–oil / oil-overnight / GER40-session / factor thr-grid

## Regel
**Signal (dag t, XLK daily close; frozen — no grid):**
1. `z120 = (XLK_t − mean_120) / stdev_120` (ddof=0). `d20 = XLK_t / XLK_{t−20} − 1`.
2. **mom_confirm:** `z120 > +0,5` and `d20 > 0` → **LONG** US100; `z120 < −0,5` and `d20 < 0` → **SHORT** US100; else skip.

**Execution (dag t+1) — D-100 session-flat, one leg:**
3. Entry: first M5 ≥ **15:30 CET** on US100cash (span ≤15 min). Missing → skip.
4. Exit: last M5 ≤ **21:00 CET** the same day. **No overnight. Not a 3-day hold.**
5. PnL bp = signed US100 return. Non-overlapping (≤1 trade/day).

**Future clone bar (precommitted):** FAIL_CLONE if |z corr| ≥ 0,90 vs SECTOR_DISP, vs XLE z40, vs DBC z40, vs XLF z40, vs XLU/XLI z40, or vs UNG z40, or (sign agree ≥ 0,85 AND cover ≥ 0,70) vs those day-signs. A clone is not a PASS.

## Pre-screen
- Data: `data/daily/XLK.csv` + `data/m5gz/US100cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **1,98** bp, **N ≥ 150**.
- PASS → PREREG. FAIL → STOP (geen overnight long US100, geen US500 remap, geen XLE/DBC/XLF/XLU-XLI/UNG/SECTOR_DISP rewrite, geen thr-grid, geen soft gate). Lane-A day_t 2,05 ≠ PASS.
