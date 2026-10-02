# C-041 — absorb main v102 + Faraday e1bf004 + Lane-B diag N142/N143 (0 CTO trials)

**When:** 2026-10-03 ~01:03 Europe/Amsterdam. **TRIAL_COUNT:** 470. **FREEZE:** OFF. **Track-3:** PAUSED. **Live PREREG:** N143 (frozen this cycle).

## Absorb

- `origin/main` tip `cb1b8d1` (NEXT_STEPS **v102** @ `b0b20ac` ~00:44): N134–N137 FAIL; OPEN **N138/N139** (stale vs Faraday); TRIAL **470**; FREEZE **OFF**; C-040 absorbed.
- Faraday `e1bf004` (~00:56): N140 FAIL / N141 FAIL_CLONE; prior N138 FAIL_CLONE / N139 FAIL; OPEN **N142 US30_US500_XS** / **N143 XLE→US500**; no PREREG.
- U2 `78775a2` IDLE/HOLD absorb v102; TRIAL **470**.
- S2 `5a21939` cycle_0047 XLE_ENERGY_EQUITY_STRESS — Lane-A feed for N143.
- Prior CTO C-040 `659d6c6`. Absorbed Faraday N132–N141 FAIL chain. Reserve 2025+ untouched.

## Lane-B diagnostic N142/N143 (train 2021–2023; ≤2024; 0 CTO trials)

| Idee | mean_bp | n | gate | day_t | h1 | h2 | L/S | years | Verdict |
|------|--------:|--:|-----:|------:|---:|---:|----:|-------|---------|
| N142_US30_US500_XS_SESSION | -1.681 | 187 | 3.69 | -0.709 | 2.284 | -5.604 | 101/86 | 2021:-0.452/2022:0.362/2023:-4.593 | **DIAG_FAIL** |
| N143_XLE_ENERGY_EQUITY_STRESS_US500_SESSION | 7.856 | 356 | 2.34 | 1.809 | 12.455 | 3.257 | 117/239 | 2021:-5.17/2022:14.148/2023:4.563 | **DIAG_PASS** |

### Notes

- N142: US30cash/US500cash ratio z40 thr1.5 basis fade (z>+1.5→SHORT US30+LONG US500; z<−1.5→LONG US30+SHORT US500) day t → both legs session-flat 15:30→21:00 CET day t+1; gate=3×(0.45+0.78)=3.69; ≠ N81/N138/N143/IDX_SHORT/N87.
- N143: XLE level z40 thr1.0 fade_extreme (z>+1→SHORT; z<−1→LONG) day t → US500 session-flat 15:30→21:00 CET day t+1; gate=3×RT 0.78=2.34; S2 5a21939 cycle_0047; ≠ GAS/CRACK/N98/N134/N140/N142.
- Also absorb Faraday N138 FAIL_CLONE / N139 FAIL / N140 FAIL / N141 FAIL_CLONE — no re-run.
- DIAG_PASS → CTO freezes PREREG for U2; else drop / replace NEW_FAMILY (D-094).
- No thr-grid / no overnight / no soft gate / no US100 remap / no XLE CFD / no GER/UK rewrite.
- Kill: bar N75–N141 + prior; N142/N143 novelty BK/BL.

**Promote candidates (DIAG_PASS):** N143 → PREREG_FTMO_N143 frozen; U2 unblocked. N142 DIAG_FAIL → no PREREG.

Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.

### PREREG

- Frozen `PREREG_FTMO_N143_XLE_ENERGY_EQUITY_STRESS.md` + `scripts/n143_xle_energy_equity_stress_gate.py`.
- Gate smoke: cost PASS / stress PASS; t_nw≈1.56; test 2024 mean +6.83 — elevated FAIL_T risk; no retune.
