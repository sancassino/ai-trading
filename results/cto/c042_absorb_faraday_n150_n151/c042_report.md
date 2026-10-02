# C-042 — absorb Faraday aca4d2f + retract N143 FAIL_CLONE + Lane-B diag N150/N151 (0 CTO trials)

**When:** 2026-10-03 ~01:30 Europe/Amsterdam. **TRIAL_COUNT:** 470. **FREEZE:** OFF. **Track-3:** PAUSED. **Live PREREG:** none.

## Absorb / correction

- Faraday `aca4d2f` (~01:23): N148 USDJPY/US100 FAIL (+3.31 < 4.32) / N149 EUR/GER40 FAIL (+2.05 < 4.05, N=140); OPEN **N150 XAG/US30 BS** / **N151 EURJPY/USDCHF BT**.
- Faraday `93cb002`: **N143 XLE FAIL_CLONE of DBC_z40_thr1.0** (mean +7.86 ≥ gate but clone) — overrides C-041 DIAG_PASS→PREREG → **retract**.
- Absorbed N142 FAIL / N144–N147 FAIL/FAIL_CLONE (no re-run).
- Main tip `cb1b8d1` v102 unchanged. U2 `78775a2` IDLE TRIAL **470**. Reserve 2025+ untouched.

## Lane-B diagnostic N150/N151 (train 2021–2023; ≤2024; 0 CTO trials)

| Idee | mean_bp | n | gate | day_t | h1 | h2 | L/S | years | Verdict |
|------|--------:|--:|-----:|------:|---:|---:|----:|-------|---------|
| N150_XAG_US30_METAL_INDUSTRIAL_XS_SESSION | 10.046 | 225 | 16.560000000000002 | 1.258 | 5.12 | 14.928 | 131/94 | 2021:13.145/2022:-7.565/2023:29.218 | **DIAG_FAIL** |
| N151_EURJPY_USDCHF_FUNDING_XS_SESSION | -0.597 | 221 | 6.330000000000001 | -0.189 | 1.974 | -3.145 | 77/144 | 2021:1.207/2022:4.685/2023:-5.43 | **DIAG_FAIL** |

### Notes

- N150: XAGUSD/US30cash ratio z40 thr1.5 basis fade both legs 15:30→21:00; gate=3×(5.07+0.45)=16.56; NEW_FAMILY BS.
- N151: EURJPY/USDCHF ratio z40 thr1.5 basis fade both legs 15:30→21:00; gate=3×(1.10+1.01)=6.33; NEW_FAMILY BT.
- N143 retract: Faraday D-092.1 FAIL_CLONE (DBC) is binding; PREREG_FTMO_N143 → STOP; U2 must not run.
- DIAG_PASS → CTO freezes PREREG for U2; else drop / Strateeg refill ≥2 NEW_FAMILY (D-094).
- No thr-grid / no overnight / no soft gate / no single-leg remap.

**Promote candidates (DIAG_PASS):** none.

Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.
