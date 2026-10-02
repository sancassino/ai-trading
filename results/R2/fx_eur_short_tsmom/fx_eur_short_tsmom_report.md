# PREREG_FTMO_FX_EUR_SHORT_TSMOM — cost-gate + formal train/test

PREREG: `PREREG_FTMO_FX_EUR_SHORT_TSMOM.md` (CTO C-025 / D-100).
Rule: L20/H10 **short-only**; EURUSD + EURAUD (FX_EURUSD + BIS cross).
Costs: EURUSD COSTS_FTMO; EURAUD alle RT + swap_side_map short (credits→0). Alfa = bruto prijs.
Train 2010–2016 / test 2017–2024. Reserve 2025→ **untouched**.

**Uitkomst: FAIL_T** (counts_as_trial=True)

## Train 2010–2016

| Metric | Waarde |
|--------|-------:|
| N_trades | 227 |
| mean bruto bp | 21.958 |
| mean RT bp | 0.8689 |
| mean swap bp (gate) | 0.0 |
| mean cost bp | 0.8689 |
| gate 3× = 2.6068 | **PASS** |
| mean netto bp | 24.1608 |
| t day-clust netto | 1.8961 |
| t NW L=5 netto | 1.8706 |
| h1 bruto / h2 bruto | 17.5052 / 26.2188 |
| h1 netto / h2 netto | 19.7361 / 28.3947 |

Train_stress +50% swap gate_3x: PASS

Symbol breakdown (train):

| Symbol | N | mean bruto | mean netto |
|--------|---|------------|------------|
| EURUSD | 114 | 24.3529 | 25.7566 |
| EURAUD | 113 | 19.5418 | 22.5508 |

## Test 2017–2024

| Metric | Waarde |
|--------|-------:|
| N_trades | 239 |
| mean bruto bp | -3.4206 |
| mean netto bp | -1.1898 |
| t day-clust netto | -0.1381 |
| t NW L=5 netto | -0.1317 |
| h1 bruto / h2 bruto | -18.0213 / 11.8041 |
| h1 netto / h2 netto | -15.7798 / 14.0236 |

Symbol breakdown (test):

| Symbol | N | mean bruto | mean netto |
|--------|---|------------|------------|
| EURUSD | 120 | 1.2136 | 2.6416 |
| EURAUD | 119 | -8.0937 | -5.0535 |
