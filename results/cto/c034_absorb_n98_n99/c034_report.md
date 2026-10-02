# C-034 — absorb Faraday N98/N99 + Lane-B diag (0 trials)

**When:** 2026-10-02 ~21:32 Europe/Amsterdam. **TRIAL_COUNT:** 458. **FREEZE:** OFF.

## Absorb

- `origin/main` still `6775e28` (NEXT_STEPS **v87**; Manager not yet bumped for C-033).
- Faraday `4a5ec7c` N96 UNDERPOWERED + N97 FAIL D-092.1; filed **N98/N99** NEW_FAMILY W/X; **no** D-092.1 for N98/N99 → CTO Lane-B.
- U2 `83d6331` IDLE/HOLD after v87 absorb. Track-3 PAUSED. Reserve 2025+ untouched.

## Lane-B diagnostic (train 2021–2023; ≤2024; 0 trials)

| Idee | mean_bp | n | gate | day_t | h1 | h2 | Verdict |
|------|--------:|--:|-----:|------:|---:|---:|---------|
| N98_USOIL_LON_AM_US100_NY_RISKON | -3.786 | 356 | 1.98 | -0.615 | -8.589 | 1.018 | **DIAG_FAIL** |
| N99_CADCHF_LO_OIL_CHF_CARRY_MOM_5D | -3.997 | 103 | 6.81 | -0.393 | 8.128 | -15.888 | **DIAG_FAIL** |

### Notes

- N98: USOILcash 08→12 CET impulse |bp|≥40 → same-dir US100 @15:30 → flat 21:00; gate=3×RT 0.66=1.98.
- N99: CADCHF dayclose ≤22:00; ret5>0 → long; hold 5d non-overlap; swap earn not credited in gate (D-100); gate=3×RT 2.27=6.81.
- DIAG_PASS → CTO freezes PREREG for U2 (C-031 precedent); else drop / replace NEW_FAMILY (D-094).
- No thr-grid / no UKOIL twin / no overnight oil rewrite / no CADJPY twin / no soft gate.

**Promote candidates (DIAG_PASS):** none.

Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.
