# VOORSTEL_PRESCREEN_N33 — USDCAD London→NY Session Momentum

**Status:** **geen PREREG — D-092.1 FAIL** (Strateeg screen 2026-10-01 08:26; N=94≪150, mean **+1,04** < 2,40 bp). Artifacts `results/R2/n32_n34_prescreen/`.  
**Auteur:** Strateeg (Grok).  
**Instrument:** `USDCAD` (RT **0,80 bp** → gate **2,40 bp**).  
**Track 2:** FX — commodity-dollar (olie-correlatie); **≠ N28 EURJPY** (ander paar/mechanisme-regio: CAD oil-beta vs EURJPY risk).  
**Grond:** London USDCAD-impuls (olie + NA prep) 09:00–15:30 CET vervolgt vaak in early NY. Continuation, flat 18:30. Swap 0.

**D-094a:** train 2021–2023. Reden **(b)**: FX session-momentum multi-decade; CAD oil-link structureel.

**Onderscheid:** ≠ A5 majors ORB; ≠ GS02 Asian fade; ≠ N28 EURJPY; ≠ B1 month TSMOM; ≠ N27/N29 MR/fade.

## Regel
- lon_bp = 1e4×(C_1530−C_0900)/C_0900; |lon|≥35 → side=sign; entry 15:30; stop 1×ATR14; flat 18:30.

## Pre-screen
- Data: `USDCAD` m5gz train 2021–2023. Gate ≥ **2,40 bp**, N≥150. PASS → PREREG_FTMO_N33.
