# D-092.1 U2 pre-screen — N11 / N12 (train 2021–2023)

Source: Strateeg `VOORSTEL_PRESCREEN_N11.md` / `N12.md` @ `b374f0a`.
Data: `data/m5gz/GER40cash.csv.gz`, `data/m5gz/XAUUSD.csv.gz`.
Reserve 2025+ untouched. No TRIALS. No PREREG claimed by this screen.
PREREG requires gate PASS **and** N≥150.

| Idee | N | mean bruto | gate | Uitkomst |
|------|---|------------|------|----------|
| N11 GER40 XETRA ORB (VOORSTEL gate) | 496 | 3.3269 bp | 4.199999999999999 bp | **FAIL** |
| N11 GER40 (COSTS RT sens.) | 496 | 3.3269 bp | 2.16 bp | **PASS** (sens.) |
| N12 XAU NY-Open Continuation | 303 | 0.5947 bp | 2.4899999999999998 bp | **FAIL** |

- N11 binding decision (VOORSTEL gate 4.20, N≥150): `NO_PREREG_screen_fail`
- N11 COSTS sensitivity (gate 2.16): `PASS_may_PREREG`
- N12 decision: `NO_PREREG_screen_fail`

