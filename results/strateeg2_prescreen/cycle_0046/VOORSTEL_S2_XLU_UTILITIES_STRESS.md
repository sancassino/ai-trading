# VOORSTEL S2 — XLU_UTILITIES_STRESS (Lane-A survivor, C-028 + POST-N78/N93)

**When:** 2026-10-04 ~00:46 Europe/Amsterdam (CEST)
**Author:** Strateeg-2 (`grok/strateeg-2`) — Lane-A novelty researcher
**Status:** Lane-A **promote** (day_t>=2 bruto **and** early FTMO RT/swap stress COST_OK). **Not** a PREREG. Strateeg Lane-B = **HOLD** per NEXT_STEPS v113 until CTO adds authorized COSTS_FTMO.csv symbol — pack for later.
**Trials:** 0. Reserve 2025+: **untouched**.

## Family tag

`NEW_FAMILY: XLU_UTILITIES_STRESS`

**Distinct from dead / barred:** ORB / TSMOM / L60 FX-med / ENERGY_TSMOM / VIX_TERM_VOV /
CORN / UKOIL-OVN / ORB-meta / **SECTOR_DISP** / PC_RATIO / BREAKEVEN / COPPER_GOLD /
CREDIT HYG-LQD / RATE_CURVE / EM_DM / **EMB_CREDIT_STRESS** / **CRACK_SPREAD_MACRO** /
**GAS_EQUITY_MACRO** / **SILVER_GOLD_RATIO** / REIT_RATE / PGM / HYG / TLT / TIP / CPER /
VNQ / EEM / DBC / EFA / IWM→US500 / **YIELD_CURVE_2S10S** / **DEFENSIVE_CYCLICAL** /
EWZ / DBA / BWX / PPLT / EQW / DXY / MTUM / GLD / XLF / QUAL / BRENT_WTI / USDMXN /
**XLE_ENERGY_EQUITY_STRESS** / VLUE / XLB / EURJPY_RISK / SOFTS_RATIO /
**XLK_TECH_SECTOR_STRESS** / XLV / COCOA / AUDUSD_COMMODITY_FX /
**LQD_IG_CREDIT_STRESS** / **EWY_KOREA_STRESS** / XLY_DISCRETIONARY /
N75–N175 / CEO T5–T16 / FX LO carry / AUD–XAU / GBP–UKOIL / BTC–ETH /
US2000 NY-impulse / EURCHF London-haven / US500 cash-close / AUD NY-fade /
USDCAD continuation / EUR-CAD XS / coffee/cocoa / USOIL swing / London-fix /
Europe inventory / Formal OPEN empty (not cloned).

## Lane-A screen (bruto <=2024-12-31, non-overlapping holds) + POST-N78/N93

| Target | FTMO | Config | mean_bp | day_t | n | years | RT | drag | net | cost |
|--------|------|--------|--------:|------:|--:|------:|---:|-----:|----:|------|
| XLU->SPY | US500cash | z40/thr1.5/stress_buy|hold=3d | **17.053** | **2.291** | 708 | 19.9 | 0.78 | 4.848 | **12.205** | **COST_OK** |

**Notes:** NEW_FAMILY; XLU utilities alone z->SPY; != DEFENSIVE XLU/XLI ratio; ORB/TSMOM/L60/ENERGY_TSMOM/VIX_TERM/CORN/UKOIL-OVN/ORB-meta/SECTOR_DISP/EMB/CRACK/GAS/SILVER/HYG/TLT/TIP/CPER/VNQ/EEM/DBC/EFA/IWM/YIELD_CURVE_2S10S/DEFENSIVE_CYCLICAL/EWZ/DBA/BWX/PPLT/EQW/DXY/MTUM/GLD/XLF/QUAL/BRENT_WTI/USDMXN/XLE/VLUE/XLB/EURJPY_RISK/SOFTS_RATIO/XLK/XLV/COCOA/AUDUSD_COMMODITY_FX/LQD/EWY/XLY/N75-N175/CEO-T5-T16/FX-LO/GER40_UK100/JP225_HK50/XAU_UKOIL/US30_US500/BTC_ETH/AUD_XAU/GBP_UKOIL/USDJPY_US100/EUR_GER40/XAG_US30/EURJPY_USDCHF/GBP_NZD/EUR_CAD/US100_GER40/US30_UKOIL/XAU_GER40/XAU_US100/USOIL_NY/GER40_EU_CLOSE/XAG_NY/US500_CASH_CLOSE/AUD_NY/NZD_SAME/US2000_NY/EURCHF_LONDON/GBPCHF_USDCHF_AUDCHF_LONDON/US30_EU_INV/GBP_LONDON_FIX/FRA40_US_OPEN/BTC_EU_MORNING/USOIL_SWING/USDCAD_CONT/COFFEE/COCOA_OH; OPEN empty — no clone; short_hist=no; <=2024; nonoverlap_hold; cost=COST_OK

Drag = RT + (swap_night × hold_days) on stressed overnight side (POST-N78 honesty).
Multi-day holds use **non-overlapping** trade sampling (no inflated overlapping t).

**FLAG:** US100 overnight long swap expensive — prefer session-flat / short-bias / D-100 when long-heavy.
Prefer US500 or EURUSD majors when mapping. No agri CFD mapping. No unauthorized alle-only symbols.

Artefacts: `results/strateeg2_prescreen/cycle_0046/`. Script: `scripts/s2_c028_lane_a_cycle0046.py`.

## Suggested Lane-B mapping (Strateeg — not filed by S2; HOLD per v113)

- **Symbol:** US500cash
- Prefer session-flat when long index; D-100 swap-aware if overnight.
- Freeze lookback/thresholds before any 2025+ touch.
- Lane-A bruto day_t + early RT stress ≠ formal PASS.
- Pack only — do not ask PREREG while Strateeg Lane-B HOLD.

## Same-cycle family bests

| Family | Best symbols | day_t | mean_bp | cost | promote |
|--------|--------------|------:|--------:|------|:-------:|
| EWA_AUSTRALIA_STRESS | EWA->EURUSD | 1.585 | 2.272 | N/A_NO_BRUTO | no |
| EWC_CANADA_STRESS | EWC->EURUSD | 2.779 | 14.215 | COST_OK | yes |
| XLI_INDUSTRIALS_STRESS | XLI->NDX | 1.265 | 7.343 | N/A_NO_BRUTO | no |
| XLP_STAPLES_STRESS | XLP->NDX | 1.698 | 6.038 | N/A_NO_BRUTO | no |
| XLU_UTILITIES_STRESS | XLU->SPY | 2.291 | 17.053 | COST_OK | yes |

Novelty: **5/5 NEW_FAMILY**. Configs: 1215. Promote configs: 9.
