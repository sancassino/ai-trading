# VOORSTEL S2 — DEFENSIVE_CYCLICAL (Lane-A survivor, C-028 + POST-N78/N93)

**When:** 2026-10-02 ~23:46 Europe/Amsterdam (CEST)
**Author:** Strateeg-2 (`grok/strateeg-2`) — Lane-A novelty researcher
**Status:** Lane-A **promote** (day_t>=2 bruto **and** early FTMO RT/swap stress COST_OK). **Not** a PREREG. Strateeg files Lane-B PREREG if accepted.
**Trials:** 0. Reserve 2025+: **untouched**.

## Family tag

`NEW_FAMILY: DEFENSIVE_CYCLICAL`

**Distinct from dead / barred:** ORB / TSMOM / L60 FX-med / ENERGY_TSMOM / VIX_TERM_VOV /
CORN / UKOIL-OVN / ORB-meta / **SECTOR_DISP** / PC_RATIO / BREAKEVEN / COPPER_GOLD /
CREDIT HYG-LQD / RATE_CURVE / EM_DM / **EMB_CREDIT_STRESS** / **CRACK_SPREAD_MACRO** /
**GAS_EQUITY_MACRO** / **SILVER_GOLD_RATIO** / REIT_RATE / PGM / HYG / TLT / TIP / CPER /
VNQ / EEM / DBC / EFA / IWM→US500 / N75–N123 / CEO T5–T16 / FX LO carry clones.

## Lane-A screen (bruto <=2024-12-31, non-overlapping holds) + POST-N78/N93

| Target | FTMO | Config | mean_bp | day_t | n | years | RT | drag | net | cost |
|--------|------|--------|--------:|------:|--:|------:|---:|-----:|----:|------|
| XLU/XLI->NDX | US100cash | z40/thr0.5/defensive_high|hold=5d | **19.754** | **2.077** | 911 | 19.89 | 0.66 | 1.687 | **18.067** | **COST_OK** |

**Notes:** NEW_FAMILY; XLP/XLY or XLU/XLI defensive-vs-cyclical relative->equity; != SECTOR_DISP XL*disp; short_hist=no; <=2024; nonoverlap_hold; cost=COST_OK

Drag = RT + (swap_night × hold_days) on stressed overnight side (POST-N78 honesty).
Multi-day holds use **non-overlapping** trade sampling (no inflated overlapping t).

**FLAG:** US100 overnight long swap expensive — prefer session-flat / short-bias / D-100 when long-heavy.
Prefer US500 or EURUSD majors when mapping.

Artefacts: `results/strateeg2_prescreen/cycle_2346/`. Script: `scripts/s2_c028_lane_a_cycle2346.py`.

## Suggested Lane-B mapping (Strateeg — not filed by S2)

- **Symbol:** US100cash
- Prefer session-flat when long index; D-100 swap-aware if overnight.
- Freeze lookback/thresholds before any 2025+ touch.
- Lane-A bruto day_t + early RT stress ≠ formal PASS.

## Same-cycle family bests

| Family | Best symbols | day_t | mean_bp | cost | promote |
|--------|--------------|------:|--------:|------|:-------:|
| DEFENSIVE_CYCLICAL | XLU/XLI->NDX | 2.077 | 19.754 | COST_OK | yes |
| EQW_CAP_BREADTH | EQW/SPY->SPY | 1.989 | 6.81 | N/A_NO_BRUTO | no |
| SOFTS_RATIO_MACRO | SUGAR/COFFEE->NDX | 1.871 | 16.386 | N/A_NO_BRUTO | no |
| YIELD_CURVE_2S10S | 10Y-3M->SPY | 2.525 | 28.933 | COST_OK | yes |

Novelty: **4/4 NEW_FAMILY**. Configs: 1377. Promote configs: 17.

## Preferred Lane-B remap (POST-N78)

Best day_t lands on NDX/US100 with **short_bias** (defensive_high) — US100 short swap cheap (drag 1.69).
**Prefer US500 twin** also COST_OK: `XLU/XLI→SPY` same config day_t=**2.020**, mean=16.48 bp, drag=4.82, net=11.66.
CSV twin: `DEFENSIVE_CYCLICAL_XLU_XLI-_SPY_z40_thr0_5_defensive_high_hold_5d_daily.csv`.
If overnight US100 long appears in Lane-B retune → **FLAG** swap-hostile; keep short-bias / session-flat.

