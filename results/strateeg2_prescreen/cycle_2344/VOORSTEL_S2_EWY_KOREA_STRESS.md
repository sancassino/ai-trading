# VOORSTEL S2 — EWY_KOREA_STRESS (Lane-A survivor, C-028 + POST-N78/N93)

**When:** 2026-10-03 ~23:44 Europe/Amsterdam (CEST)
**Author:** Strateeg-2 (`grok/strateeg-2`) — Lane-A novelty researcher
**Status:** Lane-A **promote** (day_t>=2 bruto **and** early FTMO RT/swap stress COST_OK). **Not** a PREREG. Strateeg files Lane-B PREREG if accepted.
**Trials:** 0. Reserve 2025+: **untouched**.

## Family tag

`NEW_FAMILY: EWY_KOREA_STRESS`

**Distinct from dead / barred:** ORB / TSMOM / L60 FX-med / ENERGY_TSMOM / VIX_TERM_VOV /
CORN / UKOIL-OVN / ORB-meta / **SECTOR_DISP** / PC_RATIO / BREAKEVEN / COPPER_GOLD /
CREDIT HYG-LQD / RATE_CURVE / EM_DM / **EMB_CREDIT_STRESS** / **CRACK_SPREAD_MACRO** /
**GAS_EQUITY_MACRO** / **SILVER_GOLD_RATIO** / REIT_RATE / PGM / HYG / TLT / TIP / CPER /
VNQ / EEM / DBC / EFA / IWM→US500 / **YIELD_CURVE_2S10S** / **DEFENSIVE_CYCLICAL** /
EWZ / DBA / BWX / PPLT / EQW / DXY / MTUM / GLD / XLF / QUAL / BRENT_WTI / USDMXN /
**XLE_ENERGY_EQUITY_STRESS** / VLUE / XLB / EURJPY_RISK / SOFTS_RATIO /
**XLK_TECH_SECTOR_STRESS** / XLV / COCOA / AUDUSD_COMMODITY_FX /
N75–N165 / CEO T5–T16 / FX LO carry / AUD–XAU / GBP–UKOIL / BTC–ETH /
US2000 NY-impulse / EURCHF London-haven / US500 cash-close / AUD NY-fade /
Formal OPEN empty (not cloned).

## Lane-A screen (bruto <=2024-12-31, non-overlapping holds) + POST-N78/N93

| Target | FTMO | Config | mean_bp | day_t | n | years | RT | drag | net | cost |
|--------|------|--------|--------:|------:|--:|------:|---:|-----:|----:|------|
| EWY->EURUSD | EURUSD | z120/thr0.5/z_level|hold=3d | **7.485** | **2.597** | 1242 | 19.82 | 0.63 | 4.016 | **3.469** | **COST_OK** |

**Notes:** NEW_FAMILY; EWY Korea country z->equity/FX; != EWZ/EEM/JP225-HK50; ORB/TSMOM/L60/ENERGY_TSMOM/VIX_TERM/CORN/UKOIL-OVN/ORB-meta/SECTOR_DISP/EMB/CRACK/GAS/SILVER/HYG/TLT/TIP/CPER/VNQ/EEM/DBC/EFA/IWM/YIELD_CURVE_2S10S/DEFENSIVE_CYCLICAL/EWZ/DBA/BWX/PPLT/EQW/DXY/MTUM/GLD/XLF/QUAL/BRENT_WTI/USDMXN/XLE/VLUE/XLB/EURJPY_RISK/SOFTS_RATIO/XLK/XLV/COCOA/AUDUSD_COMMODITY_FX/N75-N165/CEO-T5-T16/FX-LO/GER40_UK100/JP225_HK50/XAU_UKOIL/US30_US500/BTC_ETH/AUD_XAU/GBP_UKOIL/USDJPY_US100/EUR_GER40/XAG_US30/EURJPY_USDCHF/GBP_NZD/EUR_CAD/US100_GER40/US30_UKOIL/XAU_GER40/XAU_US100/USOIL_NY/GER40_EU_CLOSE/XAG_NY/US500_CASH_CLOSE/AUD_NY/NZD_SAME/US2000_NY/EURCHF_LONDON/GBPCHF_USDCHF_AUDCHF_LONDON; OPEN empty — no clone; short_hist=no; <=2024; nonoverlap_hold; cost=COST_OK

Drag = RT + (swap_night × hold_days) on stressed overnight side (POST-N78 honesty).
Multi-day holds use **non-overlapping** trade sampling (no inflated overlapping t).

**FLAG:** US100 overnight long swap expensive — prefer session-flat / short-bias / D-100 when long-heavy.
Prefer US500 or EURUSD majors when mapping. No agri CFD mapping.
USDNOK RT 4.76 FLAG — prefer EURUSD/SPY targets if signal is USDNOK.

Artefacts: `results/strateeg2_prescreen/cycle_2344/`. Script: `scripts/s2_c028_lane_a_cycle2344.py`.

## Suggested Lane-B mapping (Strateeg — not filed by S2)

- **Symbol:** EURUSD
- Prefer session-flat when long index; D-100 swap-aware if overnight.
- Freeze lookback/thresholds before any 2025+ touch.
- Lane-A bruto day_t + early RT stress ≠ formal PASS.

## Same-cycle family bests

| Family | Best symbols | day_t | mean_bp | cost | promote |
|--------|--------------|------:|--------:|------|:-------:|
| EWY_KOREA_STRESS | EWY->EURUSD | 2.597 | 7.485 | COST_OK | yes |
| LQD_IG_CREDIT_STRESS | LQD->NDX | 4.218 | 27.454 | COST_OK | yes |
| USDNOK_OIL_FX | USDNOK->USDNOK | 2.1 | 5.648 | COST_HOSTILE | no |
| XLY_DISCRETIONARY_STRESS | XLY->NDX | 1.804 | 17.866 | N/A_NO_BRUTO | no |

Novelty: **4/4 NEW_FAMILY**. Configs: 1485. Promote configs: 119.
