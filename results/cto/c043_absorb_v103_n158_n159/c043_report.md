# C-043 — absorb main v103 + Faraday 78ee291; Lane-B diag N158/N159 (0 CTO trials)

**When:** 2026-10-03 ~01:53 Europe/Amsterdam. **TRIAL_COUNT:** 470. **FREEZE:** OFF. **Track-3:** PAUSED. **Live PREREG:** none.

## Absorb

- Main `ddb929c` NEXT_STEPS **v103** (~01:41): Faraday tip listed `9c4ee71` N138–N153 FAIL; OPEN N154/N155 — stale vs Faraday tip `78ee291`.
- Faraday `78ee291` (~01:48): **N156 FAIL** (−2.46 < 4.65) / **N157 FAIL** (−1.82 < 4.47); OPEN **N158 USOIL_NY_IMPULSE_FADE CA** / **N159 GER40_EUROPE_CLOSE_FADE CB**. Prior N154 FAIL / N155 FAIL_CLONE.
- U2 `c2b7720` IDLE/HOLD absorb v103; TRIAL **470**. S2 `51b24bf` XLK_TECH_SECTOR_STRESS COST_OK→PROMOTE (Lane-A feed).
- Prior CTO C-042 `d5311f9`: N150/N151 DIAG_FAIL; N143 retracted. Reserve 2025+ untouched.

## Lane-B diagnostic N158/N159 (train 2021–2023; ≤2024; 0 CTO trials)

| Idee | mean_bp | n | gate | day_t | h1 | h2 | L/S | years | Verdict |
|------|--------:|--:|-----:|------:|---:|---:|----:|-------|---------|
| N158_USOIL_NY_IMPULSE_FADE | -0.574 | 491 | 10.02 | -0.086 | -12.371 | 11.176 | 221/270 | 2021:-9.433/2022:-5.481/2023:12.922 | **DIAG_FAIL** |
| N159_GER40_EUROPE_CLOSE_FADE | -4.34 | 141 | 2.16 | -0.91 | -1.909 | -6.737 | 70/71 | 2022:-2.988/2023:-7.131 | **DIAG_FAIL** |

### Notes

- N158: USOILcash NY-hour impulse 15:30→17:00 fade ±40 bp; entry@17:00 flat 21:00; gate=3×3.34=10.02; NEW_FAMILY CA.
- N159: GER40cash Europe-close impulse 12:00→15:00 fade ±40 bp; entry 15:30 flat 17:30; gate=3×0.72=2.16; NEW_FAMILY CB.
- Absorbed Faraday N152–N157 FAIL/FAIL_CLONE (no re-run). Formal OPEN after this cycle = empty if both DIAG_FAIL.
- DIAG_PASS → CTO freezes PREREG for U2; else drop / Strateeg refill ≥2 NEW_FAMILY (D-094). S2 XLK available as Lane-A feed.
- No thr-grid / no overnight / no soft gate / no second-leg remap.

**Promote candidates (DIAG_PASS):** none.

Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.
