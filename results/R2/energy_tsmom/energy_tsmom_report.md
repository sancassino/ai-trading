# PREREG_FTMO_ENERGY_TSMOM — cost-gate + formal train/test

PREREG: `PREREG_FTMO_ENERGY_TSMOM.md` (CTO C-023 / D-099).
Rule: L20/H10 long-only; UKOIL.cash + USOIL.cash via BRENT_F/WTI_F.
Train 2010–2016 / test 2017–2024. Reserve 2025→ **untouched**.

**Uitkomst: FAIL_COST_GATE** (counts_as_trial=False)

## Train 2010–2016

| Metric | Waarde |
|--------|-------:|
| N_trades | 209 |
| mean bruto bp | 29.0762 |
| mean RT bp | 7.3603 |
| mean swap bp (gate) | 83.3317 |
| mean cost bp | 90.6919 |
| gate 3× = 272.0758 | **FAIL** |
| mean netto bp | -61.6157 |
| t day-clust netto | -1.5324 |
| t NW L=5 netto | -1.3091 |
| h1 bruto / h2 bruto | 18.9195 / 40.147 |
| h1 netto / h2 netto | -71.9774 / -50.3214 |

Train_stress +50% swap gate_3x: FAIL

Symbol breakdown (train):

| Symbol | N | mean bruto | mean netto |
|--------|---|------------|------------|
| UKOIL.cash | 107 | 37.0922 | -57.8226 |
| USOIL.cash | 102 | 20.6674 | -65.5947 |
