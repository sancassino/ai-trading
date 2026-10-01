# VOORSTEL_PRESCREEN_N70 — XAUUSD 5d Swing TSMOM Bilateral (D-100 family C metals)

**Status:** **DIAG_FAIL** — CTO C-026 (long swap-wall gate ~35; bilateral/short halves fail). Geen PREREG; geen hold-grid / XAG-switch.  
**Auteur:** Strateeg (Claude).  
**Instrument:** `XAUUSD` (RT **0,83 bp** — COSTS_FTMO; swap_long **2,15** / swap_short **0,10** bp/nacht).  
**Track 4 + D-100 family C:** precious metals swing bilateral — goud 5-daagse TSMOM. Beide kanten. Hold 5 handelsdagen (4 nachten).

**Gate (worst-case = long; 4 nachten × swap_long 2,15 bp):**  
0,83 + 4 × 2,15 = **9,43 bp** → gate 3 × 9,43 = **28,29 bp**.  
Short: 0,83 + 4 × 0,10 = 1,23; gate 3,69 bp (goedkoper). Binding gate = **28,29 bp** (long worst-case).

**D-094a:** train 2021–2023. Reden **(b)**: precious metals TSMOM literatuur (Erb-Harvey; gold multi-decade trend; FTMO M5 = kosten). Herhaal in PREREG.

**Onderscheid:**
- ≠ **N36** XAU NY-open drive FAIL_T (1u intradag; dit = 5d swing)
- ≠ **TSMOM_DIV** dead (multi-asset, maandelijks)
- ≠ **N60** XAGUSD FAIL_MEAN (zilver; dit = goud; ander instrument, lagere gate)
- ≠ **N7/N8** XAU pre-London/post-AM FAIL (intradag)
- ≠ enig ORB / N31 XAU Asia→Lon (intradag)
- ≠ **N66/N67/N68** (alle gesloten; ≠ index-short / FX-carry)

## Regel
- `ret5 = close_t / close_{t−5} − 1` (dagclose uit M5; laatste bar ≤22:00 CET)
- `ret5 > 0` → **LONG** op close_t; `ret5 < 0` → **SHORT**; `ret5 = 0` → skip
- **Stop:** 1,5 × ATR14 (dag) vanaf instapprijs
- **Exit:** close_{t+5} of stop. **Non-overlapping**.
- Bilateraal (long + short).

## Pre-screen
- Data: `data/m5gz/XAUUSDcash.csv.gz` → dagclose, train **2021-01-01 … 2023-12-31**.
- Gate: mean bruto ≥ **28,29 bp**, N ≥ 150.
- PASS → PREREG_FTMO_N70. FAIL → STOP (geen holdperiode-grid, geen XAGUSD-switch).
