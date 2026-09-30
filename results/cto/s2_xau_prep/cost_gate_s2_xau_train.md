# S2-XAU kostenpoort TRAIN — PREREG_S2_XAU_OVERLAP

- Train: 2021-01-01 … 2023-12-31 (geen 2024/2025 in poort)
- Data: `data/m5gz/XAUUSD.csv.gz` (U-006 A)
- Regel: overlap 14:00–17:00 CET; range 14:00–14:30; stop 0.35×ATR(14); Asia-compressiefilter
- N trades: **351**
- Mean bruto: **-1.89 bp** | median bruto: -2.95 bp
- Mean cost (bar-spread+2×€2/lot): **0.55 bp** → 2× = **1.11 bp**
- Mean cost +50% spread: **0.72 bp** → 2× = **1.44 bp**
- Fixed RT (COSTS_FTMO): 0.83 bp → 2× = 1.66 bp (info)
- Cost share: **-29.4%** (poort <50%)
- Gates: 2×realized=False cost_share=False stress_2x=False stress_share=False
- **Verdict: FAIL**

Reserve 2025→: **onaangeraakt**.

