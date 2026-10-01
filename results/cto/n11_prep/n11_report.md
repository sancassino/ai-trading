# PREREG_FTMO_N11 — cost-gate + formal train t

PREREG landed `564ee5e` (Strateeg `e8f261f`). Train 2021–2023 only.
Rule: ORB 09:00–09:30, breakout entry before **10:30**, stop=ORB opposite, flat 13:00.
RT=0.72 → gate 2.16 / stress 3.24. Test 2024 + reserve 2025→ untouched.

| Metric | Value |
|--------|------:|
| N | 475 |
| mean bruto bp | 2.7365 |
| median bruto bp | -14.3176 |
| mean netto bp | 2.0165 |
| gate 3×RT (2.16) | PASS |
| stress +50% (3.24) | FAIL |
| t day-clust netto | 0.915 |
| t NW L=5 netto | 0.8545 |
| t day-clust bruto | 1.2417 |
| t NW L=5 bruto | 1.1596 |
| stop share | 0.5179 |
| skew day netto | 1.3411 |

## **Uitkomst: FAIL_STRESS_then_FAIL_T**

t_ok = day-clust≥2.0 AND NW L=5≥2.0 AND mean netto>0 AND N≥150 (train only).

