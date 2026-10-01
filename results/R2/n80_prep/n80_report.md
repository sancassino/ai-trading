# PREREG_FTMO_N80 — cost-gate + formal train/test

PREREG: `PREREG_FTMO_N80.md` (Strateeg Faraday `23c3741` / D-092.1 PASS).
Rule: UKOIL |gap|≥40 bp @08:00 vs prior ≤22:00 → continuation; stop 1.5×ATR14(H1); flat 17:00 CET; swap=0.
Gate: 3× RT 2.71 = **8.129999999999999 bp**. Stress = **12.19 bp**.
Train 2021–2023 / test 2024 (if gate PASS). Reserve 2025→ **untouched**. No retune.
D-092.1 pre-screen (no stop) mean +12.26 bp — **not** automatic PASS; re-measure with stop.

**Uitkomst: FAIL_COST_GATE** (counts_as_trial=False)

| Metric | Train | Test |
|--------|------:|-----:|
| N | 415 | None |
| mean bruto | 7.5625 | None |
| mean netto | 4.8525 | None |
| gate 8.129999999999999 | FAIL | — |
| stress 12.19 | FAIL | — |
| t day-clust netto | 0.6772 | None |
| t NW L=5 netto | 0.6862 | None |
| t day-clust bruto | 1.0554 | None |
| mean h1/h2 bruto | 19.0757/-3.8952 | — |
| stop share | 0.4482 | None |
| long/short n | 231/184 | — |

Year-split train mean bruto: 2021: n=144 +25.2600, 2022: n=153 -0.4648, 2023: n=118 -3.6260

C-029: FAIL_COST_GATE ≠ trial (N78 erratum). Append TRIALS / bump TRIAL_COUNT only if counts_as_trial.

