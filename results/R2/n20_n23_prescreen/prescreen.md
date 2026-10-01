# D-092.1 U2 pre-screen — N20–N23 (train 2021–2023)

Source: Strateeg `VOORSTEL_PRESCREEN_N20..N23` @ `f54ad28` (D-094).
Reserve 2025+ untouched. No TRIALS. No PREREG written by U2 (Strateeg on PASS).
PASS = mean bruto ≥ gate **and** N≥150 → `PASS_may_PREREG`.

| Idee | Instrument | N | mean bruto | gate | Uitkomst | decision |
|------|------------|---|------------|------|----------|----------|
| N20 AM→PM cont | US30cash | 384 | -2.2603 bp | 1.35 bp | **FAIL** | `NO_PREREG_screen_fail` |
| N21 afternoon fade | GER40cash | 234 | -2.4515 bp | 2.16 bp | **FAIL** | `NO_PREREG_screen_fail` |
| N22 London-AM fade | UKOILcash | 345 | -1.6697 bp | 8.13 bp | **FAIL** | `NO_PREREG_screen_fail` |
| N23 2d TSMOM | US100cash | 377 | 4.457 bp | 13.68 bp | **FAIL** | `NO_PREREG_screen_fail` |

### Side split (esp. N23)
- N20 long/short mean: -2.7513 / -1.7153 (n=202/182)
- N21 long/short mean: -3.6608 / -1.3222 (n=113/121)
- N22 long/short mean: 2.1276 / -5.2739 (n=168/177)
- N23 long/short mean: 10.8275 / -4.7678 (n=223/154)

### Notes
- N20–N22: stop = 1.0×ATR14 (prior day); swap=0 (intraday flat).
- N23: pure close-to-close 2d; non-overlapping; gate RT_eff = 0.66+2×1.95 = 4.56 → 13.68 bp; bruto unadjusted.
- D-094a: train 2021–23 as specified by Strateeg; reason (b) deferred to PREREG if PASS.

