# C-039 — absorb main v96 + S2 cycle_2346 + Lane-B diag N124/N125 (0 CTO trials)

**When:** 2026-10-02 ~23:56 Europe/Amsterdam. **TRIAL_COUNT:** 464. **FREEZE:** OFF. **Track-3:** PAUSED. **Live PREREG:** N124 + N125 (DIAG_PASS → frozen).

## Absorb

- `origin/main` `d6b9867` NEXT_STEPS **v96** (Manager ~23:39): absorb C-038; N120/N121 FAIL; N122/N123 DIAG_FAIL; TRIAL **464**; formal OPEN **empty**.
- Faraday `47e0eab` (unchanged): no new OPEN after AQ/AR died.
- U2 `6ed73cf` IDLE/HOLD absorb v96; TRIAL **464**.
- S2 `13fe10c` (~23:53): Lane-A PROMOTE **YIELD_CURVE_2S10S** + **DEFENSIVE_CYCLICAL** (cycle_2346).
- Prior CTO C-038 `1a22e81`. Reserve 2025+ untouched. Pipeline starved → CTO picks up S2 survivors as N124/N125.

## Lane-B diagnostic N124/N125 (train 2021–2023; ≤2024; 0 CTO trials)

| Idee | mean_bp | n | gate | day_t | h1 | h2 | years | Verdict |
|------|--------:|--:|-----:|------:|---:|---:|-------|---------|
| N124_YIELD_CURVE_2S10S_US500_SESSION | 8.971 | 240 | 2.34 | 1.886 | 11.117 | 6.826 | 2021:-2.305/2022:8.565/2023:12.405 | **DIAG_PASS** |
| N125_DEFENSIVE_CYCLICAL_US500_SESSION | 5.479 | 478 | 2.34 | 1.427 | 6.309 | 4.648 | 2021:0.903/2022:8.841/2023:3.721 | **DIAG_PASS** |

### Notes

- N124: 10Y−3M slope z60 thr1.5 flatten_fade (z>+1.5→SHORT; z<−1.5→LONG) day t → US500 session-flat 15:30→21:00 CET day t+1; gate=3×RT 0.78=2.34; ≠ TLT/TIP/REIT_RATE/RATE_CURVE.
- N125: XLU/XLI relative z40 thr0.5 defensive_high (z>+0.5→SHORT; z<−0.5→LONG) day t → US500 session-flat 15:30→21:00; gate=3×RT 0.78=2.34; ≠ SECTOR_DISP; US500 twin preferred over NDX short-bias.
- DIAG_PASS → CTO freezes PREREG for U2 (C-031/C-035/C-037 precedent); else drop / replace NEW_FAMILY (D-094).
- No thr-grid / no overnight / no soft gate / no TLT rewrite / no SECTOR_DISP rewrite.
- Kill: bar TIP/IWM/VNQ/EEM/DBC/EFA→US500 + TLT/CPER/HYG/EURUSD Lon-AM + GAS/SILVER + N75–N123; N124/N125 novelty AS/AT.

**Promote candidates (DIAG_PASS):** ['N124_YIELD_CURVE_2S10S_US500_SESSION', 'N125_DEFENSIVE_CYCLICAL_US500_SESSION'].

Reserve 2025+ untouched. No purchases / no FTMO signup. 0 CTO trials.

## Promote

Both DIAG_PASS → PREREG frozen; U2 unblocked. Gate smoke both cost/stress PASS with elevated FAIL_T risk (no retune).
