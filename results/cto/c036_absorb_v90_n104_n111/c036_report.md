# C-036 — absorb main v90 + Faraday N104–N109 + Lane-B diag N110/N111 (0 CTO trials)

**When:** 2026-10-02 ~22:35 Europe/Amsterdam. **TRIAL_COUNT:** 460. **FREEZE:** OFF. **Track-3:** PAUSED.

## Absorb

- `origin/main` `b7b8004` NEXT_STEPS **v90** (Manager ~22:10): C-035; N102 DIAG_FAIL / N103 FAIL_STRESS; formal OPEN N104/N105; TRIAL **460**.
- U2 `b9af560` N103 FAIL_STRESS (geen trial); `a70dc8b` IDLE absorb v90; hold N110/N111.
- Faraday `7d2d48a`: N104 UNDERPOWERED (N=98) / N105 FAIL → OPEN N106/N107.
- Faraday `107e502`: N106–N108 FAIL / N109 UNDERPOWERED → OPEN **N110/N111** NEW_FAMILY AG/AH. **No PREREG.**
- Prior CTO C-035 `f7af392` (N103 PREREG → U2 FAIL_STRESS). Reserve 2025+ untouched.

## Faraday D-092.1 (already committed; CTO absorb only — 0 CTO trials)

| Idee | mean_bp | n | gate | Verdict |
|------|--------:|--:|-----:|---------|
| N104 GBPCHF LO 5d | +10.62 | 98 | 4.53 | **UNDERPOWERED** |
| N105 JP225 Tokyo→Lon | −2.77 | 392 | 4.53 | **FAIL** |
| N106 EURNZD LO | +3.45 | 103 | 4.11 | **FAIL** |
| N107 UK→FRA40 | +3.94 | 255 | 5.94 | **FAIL** |
| N108 AUS Asia→Lon | −4.86 | 242 | 4.38 | **FAIL** |
| N109 CHFJPY LO 5d | +19.69 | 122 | 4.23 | **UNDERPOWERED** |

## Lane-B diagnostic N110/N111 (train 2021–2023; ≤2024; 0 CTO trials)

| Idee | mean_bp | n | gate | day_t | h1 | h2 | Verdict |
|------|--------:|--:|-----:|------:|---:|---:|---------|
| N110_DXY_LON_AM_EU_PM_CONT | None | 0 | 7.86 | None | None | None | **DIAG_FAIL** |
| N111_GBPAUD_LO_GBP_AUD_CARRY_MOM_5D | 3.244 | 104 | 4.38 | 0.351 | -4.152 | 10.639 | **DIAG_FAIL** |

### Notes

- N110: DXYcash 08→12 CET impulse |bp|≥25 → same-dir entry 13:00 → flat 17:00; gate=3×RT 2.62=7.86.
- N111: GBPAUD dayclose ≤22:00; ret5>0 → long; hold 5d non-overlap; swap earn not credited (D-100); gate=3×RT 1.46=4.38.
- DIAG_PASS → CTO freezes PREREG for U2 (C-031/C-035 precedent); else drop / replace NEW_FAMILY (D-094).
- No thr-grid / no EURUSD twin / no GBPCHF twin / no Asia→Lon rewrite / no soft gate / no n-inflate on UNDERPOWERED.
- Kill: bar N104–N109 families + EURNZD-LO / UK→FRA40 / AUS Asia→Lon / GBPCHF-LO / JP225 Tokyo→Lon / CHFJPY-LO + prior N75–N103 / EMB / CRACK / …

**Promote candidates (DIAG_PASS):** none.


### N110 data gap

- `data/m5gz/DXYcash.csv.gz` coverage starts **2024-11-26** (ends ~2026-10-01). Train 2021–2023 → **0 bars** → n=0 DIAG_FAIL.
- Not UNDERPOWERED (no positive mean with thin n); not soft-pass on 2024-only (violates D-094a ≥5y / train window).
- No 2025+ reserve open. No Yahoo DX-Y rewrite / thr retune this cycle. Drop N110 PREREG path; Strateeg file ≥2 NEW_FAMILY replace (D-094) for N110+N111 deaths.

Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.
