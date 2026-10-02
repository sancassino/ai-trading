# PREREG_FTMO_N35 + N36 — cost-gate + formal train/test

Source: `origin/claude/trusting-faraday-34tsmg` @ `1d5bdb2`. Reserve 2025→ untouched. Frozen rules = n35_n37_prescreen sims.

## N35 (US100cash)

| Metric | Train | Test |
|--------|------:|-----:|
| N | 214 | 42 |
| mean bruto | 6.5995 | 3.6342 |
| mean netto | 5.9395 | 2.9742 |
| gate 1.98 | PASS | — |
| stress 2.97 | PASS | — |
| t day-clust netto | 1.2232 | 0.2882 |
| t NW L=5 netto | 1.1649 | 0.3364 |
| stop share | 0.0 | 0.0 |

Year-split train mean bruto: 2021: n=21 +-9.3916, 2022: n=129 +16.3163, 2023: n=64 +-7.7387

**Uitkomst N35: FAIL_T**

## N36 (XAUUSD)

| Metric | Train | Test |
|--------|------:|-----:|
| N | 150 | 42 |
| mean bruto | 2.801 | 5.1776 |
| mean netto | 1.971 | 4.3476 |
| gate 2.49 | PASS | — |
| stress 3.74 | FAIL | — |
| t day-clust netto | 0.643 | 0.6791 |
| t NW L=5 netto | 0.7244 | 0.6678 |
| stop share | 0.0067 | 0.0 |

Year-split train mean bruto: 2021: n=55 +0.1166, 2022: n=53 +1.7758, 2023: n=42 +7.61

**Uitkomst N36: FAIL_STRESS_then_FAIL_T**

