# C-030 — N80 absorb + Lane-B diag N82–N86 (0 trials)

**When:** 2026-10-01 ~13:35 Europe/Amsterdam. **TRIAL_COUNT:** 456. **FREEZE:** OFF.

## Absorb

- U2 `454628f` **N80** UKOIL OVN-gap cont → **FAIL_COST_GATE** (mean +7.56 < 8.13 with stop; geen trial).
- Dead += N80. **Bar** UKOIL overnight-gap continuation / softer-gate / USOIL twin clones.
- Faraday `6c9c1e5` filed NEW_FAMILY **N84–N86**; N82/N83 remain OPEN on main v81.

## Lane-B diagnostic (train 2021–2023; ≤2024; 0 trials)

| Idee | mean_bp | n | gate | day_t | Verdict |
|------|--------:|--:|-----:|------:|---------|
| N82_XAG_AM_FIX_FADE | -2.907 | 311 | 15.21 | -0.987 | **DIAG_FAIL** |
| N83_DXY_OVN_US100_OPP | 15.358 | 52 | 1.98 | 1.163 | **UNDERPOWERED** |
| N84_AUDNZD_STRETCH_FADE | 0.478 | 460 | 3.18 | 0.521 | **DIAG_FAIL** |
| N85_US500_LEAD_US100_LAG | -7.114 | 370 | 1.98 | -1.47 | **DIAG_FAIL** |
| N86_XAU_OWN_VOV_MR_3D | -9.273 | 96 | 15.39 | -0.712 | **DIAG_FAIL** |

### Notes

- N83: DXYcash M5 only from 2024-11 → Yahoo `data/daily/DXY.csv` open/prior-close used as overnight gap proxy (diagnostic honesty).
- N84: AUDNZD RT est (not in COSTS_FTMO) — any DIAG_PASS still needs U2 RT land before PREREG.
- N86: own-asset XAU VoV ≠ VIX_TERM (C-029 bar still holds for VIX→equity).

**Promote / freeze PREREG:** none.

Reserve 2025+ untouched. No purchases / no FTMO signup.
