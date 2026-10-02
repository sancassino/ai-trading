# VOORSTEL_PRESCREEN_N94 — NZDJPY Long-Only 5d Carry+Momentum (D-100 family B; NEW_FAMILY S)

**Status:** **geen PREREG — D-092.1 FAIL** Strateeg `n94_n95_prescreen` (2026-10-02 ~21:05 CEST).  
N=**107**≪150, mean bruto **−0,97 bp < gate 6,00** (med −2,05; years 2021 +6,78 / 2022 +9,23 / 2023 −20,20). Artifact: `results/R2/n94_n95_prescreen/`.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY S** (NZDJPY NZD/JPY commodity-yen carry+momentum long-only).  
**Instrument:** `NZDJPY` (RT **2,00 bp** — geschat; swap_long earn → 0 in gate per D-100).  
**Gate:** 3 × 2,00 = **6,00 bp**.

**D-094a:** train 2021–2023. Reden **(b)**: FX carry + TSMOM op commodity-yen cross (Menkhoff et al. 2012; Burnside et al. 2011; Chen & Rogoff 2003 NZD commodity; FTMO-M5 = kosten).

**Onderscheid (historisch):** ≠ N90 GBPJPY UNDERPOWERED / N91 AUDUSD DIAG_FAIL / N62 GBPJPY FAIL / L60 FX-med BARRED / N88 / N58.

## Regel (bevroren; geen retune)
- `ret5 = close_t / close_{t−5} − 1` → LONG iff ret5 > 0; hold 5d non-overlapping; long-only.

## Pre-screen result
- FAIL (mean + N). **STOP** — geen ret10-switch, geen AUDJPY-add, geen soft gate. Dead screen S.
