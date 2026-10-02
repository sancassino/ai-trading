# VOORSTEL S2 — XLE_ENERGY_EQUITY_STRESS (Lane-A survivor, C-028 + POST-N78/N93)

**When:** 2026-10-03 ~00:47 Europe/Amsterdam (CEST)
**Author:** Strateeg-2 (`grok/strateeg-2`) — Lane-A novelty researcher
**Status:** Lane-A **promote** (day_t>=2 bruto **and** early FTMO RT/swap stress COST_OK). **Not** a PREREG. Strateeg files Lane-B PREREG if accepted.
**Trials:** 0. Reserve 2025+: **untouched**.

## Family tag

`NEW_FAMILY: XLE_ENERGY_EQUITY_STRESS`

**Distinct from dead / barred:** ORB / TSMOM / L60 FX-med / ENERGY_TSMOM / VIX_TERM_VOV /
CORN / UKOIL-OVN / ORB-meta / **SECTOR_DISP** / PC_RATIO / BREAKEVEN / COPPER_GOLD /
CREDIT HYG-LQD / RATE_CURVE / EM_DM / **EMB_CREDIT_STRESS** / **CRACK_SPREAD_MACRO** /
**GAS_EQUITY_MACRO** / **SILVER_GOLD_RATIO** / REIT_RATE / PGM / HYG / TLT / TIP / CPER /
VNQ / EEM / DBC / EFA / IWM→US500 / **YIELD_CURVE_2S10S** / **DEFENSIVE_CYCLICAL** /
EWZ / DBA / BWX / PPLT / EQW / DXY / MTUM / GLD / XLF / QUAL / BRENT_WTI / USDMXN /
N75–N137 / CEO T5–T16 / FX LO carry clones / GER40_UK100_XS / JP225_HK50 (OPEN — not cloned).

## Lane-A screen (bruto <=2024-12-31, non-overlapping holds) + POST-N78/N93

| Target | FTMO | Config | mean_bp | day_t | n | years | RT | drag | net | cost |
|--------|------|--------|--------:|------:|--:|------:|---:|-----:|----:|------|
| XLE->SPY | US500cash | z40/thr1.0/fade_extreme|hold=1d | **5.412** | **2.289** | 2863 | 19.91 | 0.78 | 1.588 | **3.824** | **COST_OK** |

**Notes:** NEW_FAMILY; XLE energy-equity sector z->equity; != ENERGY_TSMOM/UNG/CRACK/USOIL; ORB/TSMOM/L60/ENERGY_TSMOM/VIX_TERM/CORN/UKOIL-OVN/ORB-meta/SECTOR_DISP/EMB/CRACK/GAS/SILVER/HYG/TLT/TIP/CPER/VNQ/EEM/DBC/EFA/IWM/YIELD_CURVE_2S10S/DEFENSIVE_CYCLICAL/EWZ/DBA/BWX/PPLT/EQW/DXY/MTUM/GLD/XLF/QUAL/BRENT_WTI/USDMXN/N75-N137/CEO-T5-T16/FX-LO/GER40_UK100/JP225_HK50; short_hist=no; <=2024; nonoverlap_hold; cost=COST_OK

Drag = RT + (swap_night × hold_days) on stressed overnight side (POST-N78 honesty).
Multi-day holds use **non-overlapping** trade sampling (no inflated overlapping t).

**FLAG:** US100 overnight long swap expensive — prefer session-flat / short-bias / D-100 when long-heavy.
Prefer US500 or EURUSD majors when mapping. No agri CFD mapping.

Artefacts: `results/strateeg2_prescreen/cycle_0047/`. Script: `scripts/s2_c028_lane_a_cycle0047.py`.

## Suggested Lane-B mapping (Strateeg — not filed by S2)

- **Symbol:** US500cash
- Prefer session-flat when long index; D-100 swap-aware if overnight.
- Freeze lookback/thresholds before any 2025+ touch.
- Lane-A bruto day_t + early RT stress ≠ formal PASS.

## Same-cycle family bests

| Family | Best symbols | day_t | mean_bp | cost | promote |
|--------|--------------|------:|--------:|------|:-------:|
| EURJPY_RISK_SENTIMENT | EURJPY->SPY | 1.663 | 10.635 | N/A_NO_BRUTO | no |
| VLUE_VALUE_FACTOR_STRESS | VLUE->SPY | 1.564 | 11.182 | N/A_NO_BRUTO | no |
| XLB_MATERIALS_STRESS | XLB->NDX | 1.139 | 4.471 | N/A_NO_BRUTO | no |
| XLE_ENERGY_EQUITY_STRESS | XLE->SPY | 2.289 | 5.412 | COST_OK | yes |

Novelty: **4/4 NEW_FAMILY**. Configs: 1215. Promote configs: 21.
