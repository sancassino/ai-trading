# PREREG_FTMO_FX_EURJPY_MED_TSMOM — cost-gate + formal train/test

PREREG: `PREREG_FTMO_FX_EURJPY_MED_TSMOM.md` (CTO C-027 / D-100).
Rule: L60/H10 **long-only**; EURJPY.
Costs: COSTS_FTMO RT + swap_long (credits→0 in gate). Alfa = bruto prijs.
Train 2000–2016 / test 2017–2024. Reserve 2025→ **untouched**.

**Uitkomst: FAIL_T** (counts_as_trial=True)

## Train 2000–2016

| Metric | Waarde |
|--------|-------:|
| N_trades | 209 |
| mean bruto bp | 7.8117 |
| mean cost bp | 1.1 |
| gate 3× | 3.3 | **PASS** |
| t day-clust netto | 0.5525 |
| t NW L=5 netto | 0.5882 |
| h1/h2 bruto | 6.1832 / 9.4247 |

Train_stress +50% swap gate_3x: PASS

## Test 2017–2024

| Metric | Waarde |
|--------|-------:|
| N_trades | 132 |
| mean bruto bp | 4.1301 |
| mean netto bp | 4.5735 |
| t day-clust netto | 0.3316 |
| h1/h2 bruto | 6.3184 / 1.9419 |

