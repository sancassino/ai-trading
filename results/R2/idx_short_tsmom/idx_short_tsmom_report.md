# PREREG_FTMO_IDX_SHORT_TSMOM — cost-gate + formal train/test

PREREG: `PREREG_FTMO_IDX_SHORT_TSMOM.md` (CTO C-024 / D-100).
Rule: L20/H10 **short-only**; US100.cash + US30.cash via NDX/DJI.
Costs: `COSTS_FTMO.csv` RT + swap_short (credits→0 in gate). Alfa = bruto prijs.
Train 2010–2016 / test 2017–2024. Reserve 2025→ **untouched**.

**Uitkomst: FAIL_COST_GATE** (counts_as_trial=False)

## Train 2010–2016

| Metric | Waarde |
|--------|-------:|
| N_trades | 177 |
| mean bruto bp | -66.2182 |
| mean RT bp | 0.5532 |
| mean swap bp (gate) | 1.489 |
| mean cost bp | 2.0422 |
| gate 3× = 6.1266 | **FAIL** |
| mean netto bp | -67.3817 |
| t day-clust netto | -2.6869 |
| t NW L=5 netto | -2.8517 |
| h1 bruto / h2 bruto | -82.5412 / -48.5509 |
| h1 netto / h2 netto | -83.8123 / -49.5981 |

Train_stress +50% swap gate_3x: FAIL

Symbol breakdown (train):

| Symbol | N | mean bruto | mean netto |
|--------|---|------------|------------|
| US100.cash | 87 | -67.9122 | -71.6015 |
| US30.cash | 90 | -64.5806 | -63.3026 |
