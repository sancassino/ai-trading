# PREREG_FTMO_N78_VIX_TERM_VOV — cost-gate + formal train/test

PREREG: `PREREG_FTMO_N78_VIX_TERM_VOV.md` (Lane-B Faraday `6c9cdca` / S2 `b765613c`; C-028).
Rule: **vov10 / combo**; US100cash; hold 1d / 1 overnight long.
Gate D-100: 3×(0.66+1×1.95) = **7.83 bp**. Stress = **11.75 bp**.
Train 2021–2023 / test 2024. Reserve 2025→ **untouched**. No retune.
Signal: Yahoo VIX9D/VIX3M/VIX (`data/daily/`). PnL: FTMO US100cash D1.
D-094a (b): proxy history OK for novelty; FTMO re-measure for cost/formal.

**Uitkomst: FAIL_COST_GATE** (counts_as_trial=True)

## Train 2021–2023

| Metric | Waarde |
|--------|-------:|
| N (nonzero pos) | 492 |
| mean bruto bp | 2.2095 |
| mean netto bp | 0.5836 |
| mean cost bp | 1.6259 |
| gate 7.83 | **FAIL** |
| stress 11.75 | **FAIL** |
| t day-clust bruto / NW | 0.4483 / 0.5372 |
| t day-clust netto / NW | 0.1184 / 0.1418 |
| h1/h2 bruto | -1.2096 / 5.6287 |
| frac full/half | 0.2459 / 0.7541 |
| by year bruto | {'2021': 3.4327, '2022': -8.2505, '2023': 9.2076} |

## Test 2024

| Metric | Waarde |
|--------|-------:|
| N | 150 |
| mean bruto bp | 8.0079 |
| mean netto bp | 6.3027 |
| t day-clust netto / NW | 0.8127 / 0.7972 |
| h1/h2 bruto | 7.2145 / 8.8012 |

