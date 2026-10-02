# PREREG_FTMO_N18 — cost-gate + formal train t

PREREG landed `c715e06` (CTO `aaaecad` / Strateeg `50561ab`). Train 2021–2023 only.
Rule: overnight gap ≥ ±50 bp vs prior 22:00 CET → continuation @15:30; stop 1.5×ATR14; flat 18:30.
RT=0.78 → gate 2.34 / stress 3.51. Test 2024 + reserve 2025→ untouched.

| Metric | Value |
|--------|------:|
| N | 279 |
| mean bruto bp | 3.5181 |
| median bruto bp | 2.7660 |
| mean netto bp | 2.7381 |
| gate 3×RT (2.34) | PASS |
| stress +50% (3.51) | PASS |
| t day-clust netto | 0.6377 |
| t NW L=5 netto | 0.6737 |
| t day-clust bruto | 0.8194 |
| t NW L=5 bruto | 0.8656 |
| stop share | 0.0000 |
| skew day netto | -0.5314 |

### Year-split mean bruto (caveat PREREG)

| Year | N | mean bruto | median |
|------|---|------------|--------|
| 2021 | 76 | 12.9664 | 11.3796 |
| 2022 | 131 | 6.6618 | 6.9567 |
| 2023 | 72 | -12.1749 | -17.5014 |

## **Uitkomst: FAIL_T**

t_ok = day-clust≥2.0 AND NW L=5≥2.0 AND mean netto>0 AND N≥150 (train only).

