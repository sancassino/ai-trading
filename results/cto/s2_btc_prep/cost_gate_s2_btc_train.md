# S2-BTC kostenpoort TRAIN — PREREG_S2_BTC_USOPEN

- Train: 2021-01-01 … 2023-12-31 (geen 2024/2025 in poort)
- Data: `data/m5gz/BTCUSD.csv.gz` + `US100cash.csv.gz` (U-006 v41)
- Regel: pre-range 14:30–15:30 CET; entry close-break 15:30–16:00; stop=mid; flat 21:00; US100 |gap|≥0.15% same sign; width∈[0.20%,1.50%]
- N trades: **132** (power ≥150: False)
- Mean bruto: **+22.91 bp** | median bruto: -37.54 bp
- Mean cost (bar-spread+2×0.20 bp): **4.37 bp**
- Mean cost +50% spread: **6.35 bp**
- Fixed RT (COSTS_FTMO_alle): 1.25 bp → 2× = 2.50 bp
- Cost share: **19.1%** (poort <50%)
- Gates: 2×fixed=True cost_share=True stress_2x=True stress_share=True power=False
- **Verdict: FAIL**

Reserve 2025→: **onaangeraakt**.

