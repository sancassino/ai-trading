# PREREG_S2_GBPJPY_EU_MOM — cost-gate + formal train/test

PREREG from `grok/strateeg-2` @ `6444d30`. Frozen rule §1. Train 2021–2023; test 2024; **reserve 2025→ untouched**.
RT=1.11 → gate 3.33 / stress 4.995.

## Train

| Metric | Value |
|--------|------:|
| N | 170 |
| mean bruto bp | 3.4082 |
| median bruto bp | 2.604 |
| mean netto bp | 2.2982 |
| cost share | 0.3257 |
| gate 3×RT (3.33) | PASS |
| stress bruto≥3×(RT×1.5) (4.995) | FAIL |
| mean netto @ RT×1.5 | 1.7432 |
| cost share @ RT×1.5 | 0.4885 |
| t day-clust netto | 1.0409 |
| t NW L=5 netto | 1.0447 |
| stop share | 0.1412 |
| time share | 0.7941 |
| skew day-ret | 0.2094 |
| max day dip (0.75% risk) | -0.0075 |

### Year-split mean bruto

| Year | N | mean bruto | median |
|------|---|------------|--------|
| 2021 | 32 | 6.5879 | 6.7856 |
| 2022 | 81 | 0.1798 | 0.4367 |
| 2023 | 57 | 6.2107 | 4.3549 |

## Test 2024

| Metric | Value |
|--------|------:|
| N | 59 |
| mean bruto bp | -1.0482 |
| mean netto bp | -2.1582 |
| t day-clust netto | -0.6357 |
| t NW L=5 netto | -0.7354 |
| cost share | None |

## **Uitkomst: FAIL_STRESS_then_FAIL_T**

Base gate FAIL → STOP, geen TRIALS-append. Base PASS → formal t-test + TRIALS append (N11 precedent: stress FAIL still counts as FAIL_T / FAIL_STRESS_then_FAIL_T).
ftmo_ev train: {"p_pass_1": 0.997, "p_pass_2": 0.9845, "p_survive": 0.9964564138908576, "exp_payout_monthly": 528.5127735072858, "net_ev": 12142.68656417486, "fee": 540.0, "account": 80000.0}
