# C-033 — absorb main v87 + Lane-B diag N96/N97 (0 trials)

**When:** 2026-10-02 ~21:15 Europe/Amsterdam. **TRIAL_COUNT:** 458. **FREEZE:** OFF.

## Absorb

- Merged `origin/main` @ `6775e28` (NEXT_STEPS **v87** — C-032 + N94/N95 DIAG_FAIL; N96/N97 OPEN; TRIAL **458**).
- Faraday `b2ab614` VOORSTEL N96/N97 OPEN; **no** prior D-092.1 results for N96/N97 → CTO Lane-B diag.
- U2 `b382307` IDLE/HOLD after N93 FAIL_COST_GATE. Track-3 PAUSED. Reserve 2025+ untouched.

## Lane-B diagnostic (train 2021–2023; ≤2024; 0 trials)

| Idee | mean_bp | n | gate | day_t | h1 | h2 | Verdict |
|------|--------:|--:|-----:|------:|---:|---:|---------|
| N96_CADJPY_LO_CARRY_MOM_5D | 16.453 | 112 | 4.8 | 1.28 | 27.566 | 5.339 | **UNDERPOWERED** |
| N97_AUDCAD_LO_COMMODITY_XS_MOM_5D | -8.873 | 101 | 4.5 | -0.879 | -5.124 | -12.548 | **DIAG_FAIL** |

### Notes

- N96: CADJPY dayclose ≤22:00; ret5>0 → long; hold 5d non-overlap; swap earn not credited in gate (D-100).
- N97: AUDCAD dayclose ≤22:00; ret5>0 → long; hold 5d non-overlap; swap earn/neutral → 0 in gate.
- DIAG_PASS → CTO freezes PREREG for U2 (C-031 precedent); else drop / replace NEW_FAMILY (D-094).
- No retune lookback / no NZDJPY twin / no fade rewrite.

**Promote candidates (DIAG_PASS):** none.

Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.
