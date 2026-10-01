# VOORSTEL_PRESCREEN_N58 — FX Carry+Trend AUDUSD vs USDJPY relative (D-097 carry/RV)

**Status:** **OPEN** — awaiting D-092.1 (**D-094** track 4 + D-097 carry/RV; replace N55–N57 FAIL; filed 2026-10-01 ~10:25 CEST).  
**Auteur:** Strateeg (Faraday).  
**Instruments:** long `AUDUSD` / short `USDJPY` equal-risk when relative 20d momentum favors AUD (carry+trend proxy). Hold 10 handelsdagen; non-overlap.  
**Gate:** per-leg costs: AUDUSD RT_eff≈1,22+10×0,45=**5,72** (3×=17,16); USDJPY short RT_eff=0,78+10×1,58=**16,58** (3×=**49,74**). Binding pair ≥ **50 bp** pooled bruto (C-021).  
**D-094a (b):** FX carry+trend literatuur (BIS); FTMO-M5 kosten.

**Onderscheid:** ≠ N57 basket TSMOM FAIL; ≠ B1/B2 month; ≠ N46/N47 BARRED intradag; ≠ CEO TSMOM_DIV.

## Regel
- `rel = ret20(AUDUSD) − ret20(USDJPY)`
- `rel > 0` → LONG AUDUSD + SHORT USDJPY (equal notional risk 1/σ20); exit both t+10.
- `rel ≤ 0` → skip (no inverse sleeve in pre-screen).

## Pre-screen
- Train 2021–2023. Mean pair bruto (sum of leg bp) ≥ **50**, N≥150 (of N≥100 + D-094a b). FAIL → STOP.
