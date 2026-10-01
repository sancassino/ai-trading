# PREREG_FTMO_FX_USDJPY_MED_TSMOM — cost-gate + formal train/test

PREREG: `PREREG_FTMO_FX_USDJPY_MED_TSMOM.md` (CTO C-026 / D-100).
Rule: L60/H10 **long-only**; USDJPY.
Costs: COSTS_FTMO RT + swap_long (credits→0 in gate). Alfa = bruto prijs.
Train 2000–2016 / test 2017–2024. Reserve 2025→ **untouched**.

**Uitkomst: FAIL_T** (counts_as_trial=True)

## Train 2000–2016

| Metric | Waarde |
|--------|-------:|
| N_trades | 237 |
| mean bruto bp | 10.9746 |
| mean cost bp | 0.78 |
| gate 3× | 2.34 | **PASS** |
| t day-clust netto | 1.1508 |
| t NW L=5 netto | 1.1616 |
| h1/h2 bruto | 3.9824 / 17.9081 |

Train_stress +50% swap gate_3x: PASS

## Test 2017–2024

| Metric | Waarde |
|--------|-------:|
| N_trades | 121 |
| mean bruto bp | 17.2497 |
| mean netto bp | 21.8637 |
| t day-clust netto | 1.3188 |
| h1/h2 bruto | -11.8837 / 45.9055 |

