# VOORSTEL_PRESCREEN_N60 — XAGUSD 5d Swing TSMOM (D-097 precious metals swing)

**Status:** **geen PREREG — D-092.1 FAIL_MEAN** mean **+37,01** < 53,01 (N=151). Artifacts `results/R2/n58_n62_prescreen/`.
**Auteur:** Strateeg (Claude).  
**Instrument:** `XAGUSD` (RT **5,07 bp** — COSTS_FTMO; spread med 4,92 bp).  
**Track 4 + D-097:** precious metals swing — 5-daagse close-to-close TSMOM op zilver (COMEX proxy). Hold 5 handelsdagen (4 nachten). Swap 0 (credit, short XAGUSD ontvangt). D-097: swing 3–20d, bruto-target ≥50 bp/trade.

**Gate (worst-case = long; 4 nachten × swap_long 3,15 bp):**  
5,07 + 4 × 3,15 = **17,67 bp** → gate 3 × 17,67 = **53,01 bp**.  
Short: RT 5,07 + 4 × (−0,18 ontvangen) = effectief 5,07 → 15,21 bp. Binding gate = **53,01 bp** (long worst-case; beide kanten ≥ gate vereist).

**D-094a:** train 2021–2023. Reden **(b)**: precious metals time-series momentum literatuur (Erb-Harvey, Gorton-Rouwenhorst; silver volgt gold + industriële vraag; COMEX-proxy BIS/FTMO-M5); FTMO-M5 kosten bindend. Herhaal in PREREG.

**Onderscheid (anti-kloon):**
- ≠ **TSMOM_DIV** dead (gediversifieerd multi-asset; dit = zilver solo)
- ≠ **ENERGY_TSMOM** CTO C-023 (energie; dit = precious metals)
- ≠ **N36** XAU NY-drive FAIL_T (intradag 1u XAU; dit = 5d swing XAGUSD)
- ≠ **B1** maand-TSMOM STOP (~20+ nachten FX; dit = 5d metaal)
- ≠ enig ORB / session-mom / intradag FX clone

## Regel
- `ret5 = close_t / close_{t−5} − 1` (dagclose uit M5-reeks; laatste M5-bar vóór 22:00 CET)
- `ret5 > 0` → **LONG** op close_t; `ret5 < 0` → **SHORT**; `ret5 = 0` → skip
- **Stop:** 1,5 × ATR14 (dag) vanaf instapprijs
- **Exit:** close_{t+5} (5 handelsdagen) of stop. **Non-overlapping** entries (wacht tot flat).
- Max 1 positie tegelijk.

## Pre-screen
- Data: `data/m5gz/XAGUSD.csv.gz` → dagclose (laatste M5 / 22:00 CET), train **2021-01-01 … 2023-12-31**.
- Maatstaf: signed mean bruto bp (beide kanten), N (non-overlap), median.
- Gate: mean bruto ≥ **53,01 bp**, N ≥ 150.
- PASS → PREREG_FTMO_N60. FAIL → STOP (geen lookback-dunnen; geen silver→gold-switch).
