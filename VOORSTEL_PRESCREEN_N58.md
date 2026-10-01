# VOORSTEL_PRESCREEN_N58 — AUDJPY long-only carry+trend (D-100 family B redesign)

**Status:** **geen PREREG — D-092.1 FAIL_MEAN** mean **+41,66** < 50 (N=50); redesign AUDJPY long-only; closest miss this cycle. Artifacts `results/R2/n58_n62_prescreen/`.
**Auteur:** Strateeg (Faraday).  
**Instrument:** `AUDJPY` **long-only** (C-024 best_side=long, +1,50 %/jr; RT est ≈ 2,0 bp).  
**Was:** AUDUSD long + USDJPY short pair → **SWAP_HOSTILE** (C-024: AUDUSD long −1,73 %/jr; USDJPY short −5,13 %/jr). Redesign per D-100: overnight alleen op goedkoopste kant.

**Gate:** 3× RT ≈ 6 bp → bindend **max(50, 6) = 50 bp** (D-097 groot-bruto; C-021-style). Hold 10 handelsdagen; swap_gate = max(swap_long,0)×nachten → 0 (credit/earn). Alfa = bruto prijs.

**D-094a (b):** FX carry+trend (BIS / Lustig–Roussanov–Verdelhan); FTMO-M5 kosten.

**Onderscheid:** ≠ N58-v1 hostile pair; ≠ N57 basket FAIL; ≠ B1/B2 month STOP; ≠ N46/N47 BARRED intradag; ≠ CEO TSMOM_DIV / ENERGY; ≠ IDX_SHORT (index).

## Regel
- `ret20 = close_t / close_{t−20} − 1`
- `ret20 > 0` → **LONG** AUDJPY; else skip (geen short-been).
- Exit close_{t+10}; non-overlapping. Geen stops in pre-screen.

## Pre-screen
- Train 2021–2023 `data/m5gz/AUDJPY.csv.gz` → dagclose.
- PASS iff mean bruto ≥ **50**, N≥150 (of N≥100 + D-094a b). FAIL → STOP (geen pair-terugkeer; geen lookback-grid).
