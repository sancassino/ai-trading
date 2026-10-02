# C-040 — absorb main v100 + Faraday c19fd24 + Lane-B diag N134/N135 (0 CTO trials)

**When:** 2026-10-03 ~00:30 Europe/Amsterdam. **TRIAL_COUNT:** 470. **FREEZE:** OFF. **Track-3:** PAUSED. **Live PREREG:** none (pending diag).

## Absorb

- `origin/main` `b8a1450` NEXT_STEPS **v100** (Manager ~00:21): N130+N131 FAIL_T; TRIAL **470**; formal OPEN **empty** (Faraday tip listed as 0af85da — stale vs c19fd24).
- Faraday `c19fd24` (~00:24): N132/N133 D-092.1 FAIL; OPEN **N134 XLF** / **N135 QUAL**; no PREREG.
- U2 `a76b07a` IDLE/HOLD absorb v100; TRIAL **470** (material `03ad9da`).
- S2 `13fe10c` cycle_2346 — no newer Lane-A tip.
- Prior CTO C-039 `e34ae09`. N124/N125 FAIL_T @ U2 (TRIAL 465–466). Reserve 2025+ untouched.

## Lane-B diagnostic N134/N135 (train 2021–2023; ≤2024; 0 CTO trials)

| Idee | mean_bp | n | gate | day_t | h1 | h2 | years | Verdict |
|------|--------:|--:|-----:|------:|---:|---:|-------|---------|
| N134_XLF_FINANCIAL_STRESS_US500_SESSION | -1.457 | 184 | 2.34 | -0.239 | 2.507 | -5.421 | 2021:11.617/2022:0.266/2023:-5.657 | **DIAG_FAIL** |
| N135_QUAL_QUALITY_STRESS_US500_SESSION | -5.029 | 211 | 2.34 | -1.039 | -2.236 | -7.796 | 2021:10.498/2022:-4.314/2023:-9.578 | **DIAG_FAIL** |

### Notes

- N134: XLF level z40 thr1.5 stress_buy (z>+1.5→SHORT; z<−1.5→LONG) day t → US500 session-flat 15:30→21:00 CET day t+1; gate=3×RT 0.78=2.34; ≠ HYG/EMB/SECTOR_DISP/XLU-XLI/MTUM.
- N135: QUAL level z40 thr1.5 stress_buy → US500 session-flat; gate=3×RT 0.78=2.34; ≠ MTUM/EQW/XLU/USMV/IWM.
- Also absorb Faraday N132 MTUM FAIL (mean +1.55 n=185) / N133 GLD FAIL (mean +0.26 n=361) — no re-run.
- DIAG_PASS → CTO freezes PREREG for U2; else drop / replace NEW_FAMILY (D-094).
- No thr-grid / no overnight / no soft gate / no HYG rewrite / no SECTOR_DISP rewrite.
- Kill: bar N75–N133 + EQW/DXY_DOLLAR/BWX/EWZ/YIELD/DEFENSIVE + prior; N134/N135 novelty BC/BD.

**Promote candidates (DIAG_PASS):** none.

Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.
