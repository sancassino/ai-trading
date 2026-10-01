# D-092.1 Strateeg pre-screen — N24–N27 (train 2021–2023)

Source: `VOORSTEL_PRESCREEN_N24..N27` @ `b6e8c1e` (D-094).
Runner: Strateeg faraday (U2 tip still `a1756a7` idle on N20–N23). Reserve 2025+ untouched.
PASS = mean bruto ≥ gate **and** N≥150 → `PASS_may_PREREG`.

| Idee | Instrument | N | mean bruto | gate | Uitkomst | decision |
|------|------------|---|------------|------|----------|----------|
| N24 lunch fade | US500cash | 271 | 0.3499 bp | 2.34 bp | **FAIL** | `NO_PREREG_screen_fail` |
| N25 NY-PM fade | XAUUSD | 334 | 1.1423 bp | 2.49 bp | **FAIL** | `NO_PREREG_screen_fail` |
| N26 XS 1d reversal | 5-asset basket | 581 | 0.7679 bp | 4.83 bp | **FAIL** | `NO_PREREG_screen_fail` |
| N27 H4 MR | AUDUSD | 429 | 1.4935 bp | 3.66 bp | **FAIL** | `NO_PREREG_screen_fail` |

### Side split
- N24 long/short mean: -1.2162 / 1.9046 (n=135/136)
- N25 long/short mean: 1.241 / 1.0437 (n=167/167)
- N26 combined mean (side field=1 dummy): 0.7679
- N27 long/short mean: -0.5138 / 3.7919 (n=229/200)

### Notes
- N24/N25: stop = 1.0×ATR14 (prior day); swap=0.
- N26: equal-weight combined bp; no stop in bruto screen; D-094a (c).
- N27: H4 resample 4h left-closed; pure hold 12:00→16:00; D-094a (b).

