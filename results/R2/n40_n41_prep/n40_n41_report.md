# PREREG_FTMO_N40 + N41 — cost-gate + formal train/test

Source: `origin/claude/trusting-faraday-34tsmg` @ `6ef46a7`. Reserve 2025→ untouched. Frozen rules = n38_n40 / n41_n43 prescreen sims.

## N40 (GER40cash)

| Metric | Train | Test |
|--------|------:|-----:|
| N | 205 | 53 |
| mean bruto | 2.4282 | -0.0035 |
| mean netto | 1.7082 | -0.7235 |
| gate 2.16 | PASS | — |
| stress 3.24 | FAIL | — |
| t day-clust netto | 0.5532 | -0.2282 |
| t NW L=5 netto | 0.5622 | -0.2147 |
| stop share | 0.0 | 0.0 |

Year-split train mean bruto: 2022: n=136 +3.0814, 2023: n=69 +1.1406

**Uitkomst N40: FAIL_STRESS_then_FAIL_T**

## N41 (US30cash)

| Metric | Train | Test |
|--------|------:|-----:|
| N | 160 | 14 |
| mean bruto | 8.6507 | -4.3916 |
| mean netto | 8.2007 | -4.8416 |
| gate 1.35 | PASS | — |
| stress 2.025 | PASS | — |
| t day-clust netto | 2.0145 | -0.3855 |
| t NW L=5 netto | 1.8509 | -0.4884 |
| stop share | 0.0063 | 0.0 |

Year-split train mean bruto: 2021: n=34 +9.7146, 2022: n=98 +11.6716, 2023: n=28 +-3.2142

**Uitkomst N41: FAIL_T**

