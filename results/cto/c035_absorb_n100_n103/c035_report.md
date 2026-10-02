# C-035 — absorb U2 N100/N101 FAIL_T + Faraday N102/N103 Lane-B diag (0 CTO trials)

**When:** 2026-10-02 ~22:05 Europe/Amsterdam. **TRIAL_COUNT:** 460. **FREEZE:** OFF.

## Absorb

- `origin/main` `1e06371` (NEXT_STEPS **v88**; Manager @21:42 still TRIAL 458 / U2 IDLE — stale vs U2).
- Faraday `edbd2ee` ~21:57: PREREG **N100/N101** from S2 `67a9be1` + OPEN **N102/N103** NEW_FAMILY Y/Z.
- U2 `2ffb9af` N100 EMB_CREDIT_STRESS **FAIL_T** (TRIAL **459**); `d09d00a` N101 CRACK_SPREAD_MACRO **FAIL_T** (TRIAL **460**).
- No live PREREG. Track-3 PAUSED. Reserve 2025+ untouched.

## U2 formal (already committed; CTO absorb only)

| Idee | Family | Trial | Verdict | Notes |
|------|--------|------:|---------|-------|
| N100 | EMB_CREDIT_STRESS | 459 | **FAIL_T** | cost PASS +2.97≥1.98; t 0.37; test −2.57 |
| N101 | CRACK_SPREAD_MACRO | 460 | **FAIL_T** | cost PASS +6.30≥1.98; t 1.05; test −5.00 |

## Lane-B diagnostic N102/N103 (train 2021–2023; ≤2024; 0 CTO trials)

| Idee | mean_bp | n | gate | day_t | h1 | h2 | Verdict |
|------|--------:|--:|-----:|------:|---:|---:|---------|
| N102_USDCHF_LO_USD_CHF_CARRY_MOM_5D | 2.94 | 104 | 3.03 | 0.273 | 19.12 | -13.241 | **DIAG_FAIL** |
| N103_GER40_LON_AM_US30_NY_INDUSTRIAL | 1.749 | 286 | 1.35 | 0.38 | -1.922 | 5.419 | **DIAG_PASS** |

### Notes

- N102: USDCHF dayclose ≤22:00; ret5>0 → long; hold 5d non-overlap; swap earn not credited (D-100); gate=3×RT 1.01=3.03.
- N103: GER40cash 08→12 CET impulse |bp|≥40 → same-dir US30 @15:30 → flat 21:00; gate=3×RT 0.45=1.35.
- DIAG_PASS → CTO freezes PREREG for U2 (C-031 precedent); else drop / replace NEW_FAMILY (D-094).
- No thr-grid / no CADCHF twin / no L60 rewrite / no GER→US-open rewrite / no US100 substitute / no soft gate.
- Kill: bar EMB_CREDIT_STRESS / CRACK_SPREAD_MACRO clones; skip N75–N101 + prior bars.

**Promote candidates (DIAG_PASS):** N103 → **PREREG_FTMO_N103 frozen** for U2.

- N102 DIAG_FAIL (mean 2.94 < gate 3.03; n=104) → drop; Strateeg file ≥1 NEW_FAMILY replace (D-094).
- N103 gate smoke: cost PASS (+1.75≥1.35) but **stress FAIL** (+1.75<2.025); day_t≈0.28 — elevated FAIL_T/FAIL_STRESS risk; no retune.

Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.
