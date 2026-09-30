# A2 kostenpoort TRAIN — PREREG_FTMO_A2

- Variant: **b** (OR-richting, stop 10% ATR14, EOD; enige bindende)
- Train: 2021-01-01 … 2023-12-31 (geen 2024/2025 in poort)
- Data: `data/m5gz/` US41 + `earnings.csv` + `COSTS_FTMO_alle.csv`
- N trades: **365**
- Mean bruto: **+3.77 bp** | median bruto: **-23.78 bp**
- Trade-gewogen mean rondreis (tabel): **8.91 bp** → 3× = **26.74 bp**
- Mean bar-spread+comm (informatief): 1.55 bp
- Mean bruto zonder top-5% winnaars (D-012 staart, informatief): -25.88 bp
- +50% spread-poort (gevoeligheid): FAIL
- **Verdict (mean bruto ≥ 3× mean RT): FAIL**

## Per jaar (train)

| Jaar | N | mean bruto bp | median bruto bp |
|-----:|--:|--------------:|----------------:|
| 2021 | 89 | +38.83 | -19.65 |
| 2022 | 138 | +0.68 | -29.02 |
| 2023 | 138 | -15.75 | -20.74 |

Reserve 2025→: **onaangeraakt**. Bij FAIL: STOP, TRIALS append `stop:kostenpoort`, geen TRIAL_COUNT++, geen ftmo_ev().
