# S2-BTC kostenpoort TRAIN — PREREG_S2_BTC_USOPEN

- Train/discovery: 2021-01-01 … 2024-12-31 (D-095 stap 1; 2025→ onaangeraakt)
- Data: `data/m5gz/BTCUSD.csv.gz` + `US100cash.csv.gz` (U-006 v41)
- Regel: pre-range 14:30–15:30 CET; entry close-break 15:30–16:00; stop=mid; flat 21:00; US100 |gap|≥0.15% same sign; width∈[0.20%,1.50%]
- N trades: **197** (power ≥150: True)
- Mean bruto: **+15.76 bp** | median bruto: -38.94 bp
- Mean cost (bar-spread+2×0.20 bp): **3.50 bp**
- Mean cost +50% spread: **5.05 bp**
- Fixed RT (COSTS_FTMO_alle): 1.25 bp → 2× = 2.50 bp
- Cost share: **22.2%** (poort <50%)
- Gates: 2×fixed=True cost_share=True stress_2x=True stress_share=True power=True
- **Verdict: PASS**

Reserve 2025→: **onaangeraakt**.

## Informatief (geen formal trial / geen TRIALS)
- Day-clustered NW-L5 t bruto: **1.49**; netto: **1.17**
- Skew bruto: +2.725
- Half 2021–22 mean netto: +36.13 bp (N=81)
- Half 2023–24 mean netto: -4.41 bp (N=116)
- Year means bruto bp: 2021 +53.3 (N=23), 2022 +35.3 (N=58), 2023 -4.9 (N=51), 2024 +1.2 (N=65)
- Geen reserve 2025+; geen TRIAL_COUNT-bump (stap 1 = poort, geen formal).
