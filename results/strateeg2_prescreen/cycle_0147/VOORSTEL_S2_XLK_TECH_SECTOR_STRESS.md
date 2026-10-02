# VOORSTEL S2 — XLK_TECH_SECTOR_STRESS (Lane-A survivor, C-028 + POST-N78/N93)

**When:** 2026-10-03 ~01:47 Europe/Amsterdam (CEST)
**Author:** Strateeg-2 (`grok/strateeg-2`) — Lane-A novelty researcher
**Status:** Lane-A **promote** (day_t>=2 bruto **and** early FTMO RT/swap stress COST_OK). **Not** a PREREG. Strateeg files Lane-B PREREG if accepted.
**Trials:** 0. Reserve 2025+: **untouched**.

## Family tag

`NEW_FAMILY: XLK_TECH_SECTOR_STRESS`

**Distinct from dead / barred:** ORB / TSMOM / L60 FX-med / ENERGY_TSMOM / VIX_TERM_VOV /
CORN / UKOIL-OVN / ORB-meta / **SECTOR_DISP** / PC_RATIO / BREAKEVEN / COPPER_GOLD /
CREDIT HYG-LQD / RATE_CURVE / EM_DM / **EMB_CREDIT_STRESS** / **CRACK_SPREAD_MACRO** /
**GAS_EQUITY_MACRO** / **SILVER_GOLD_RATIO** / REIT_RATE / PGM / HYG / TLT / TIP / CPER /
VNQ / EEM / DBC / EFA / IWM→US500 / **YIELD_CURVE_2S10S** / **DEFENSIVE_CYCLICAL** /
EWZ / DBA / BWX / PPLT / EQW / DXY / MTUM / GLD / XLF / QUAL / BRENT_WTI / USDMXN /
**XLE_ENERGY_EQUITY_STRESS** / VLUE / XLB / EURJPY_RISK / SOFTS_RATIO /
N75–N153 / CEO T5–T16 / FX LO carry / AUD–XAU / GBP–UKOIL / BTC–ETH /
OPEN N154 US100_GER40_XS / N155 US30_UKOIL_XS (not cloned).

## Lane-A screen (bruto <=2024-12-31, non-overlapping holds) + POST-N78/N93

| Target | FTMO | Config | mean_bp | day_t | n | years | RT | drag | net | cost |
|--------|------|--------|--------:|------:|--:|------:|---:|-----:|----:|------|
| XLK->NDX | US100cash | z120/thr0.5/mom_confirm|hold=3d | **12.228** | **2.046** | 1246 | 19.82 | 0.66 | 6.512 | **5.716** | **COST_OK** |

**Notes:** NEW_FAMILY; XLK tech-sector z->equity/FX; != XLE/XLB/XLF/QUAL/MTUM; ORB/TSMOM/L60/ENERGY_TSMOM/VIX_TERM/CORN/UKOIL-OVN/ORB-meta/SECTOR_DISP/EMB/CRACK/GAS/SILVER/HYG/TLT/TIP/CPER/VNQ/EEM/DBC/EFA/IWM/YIELD_CURVE_2S10S/DEFENSIVE_CYCLICAL/EWZ/DBA/BWX/PPLT/EQW/DXY/MTUM/GLD/XLF/QUAL/BRENT_WTI/USDMXN/XLE/VLUE/XLB/EURJPY_RISK/SOFTS_RATIO/N75-N153/CEO-T5-T16/FX-LO/GER40_UK100/JP225_HK50/XAU_UKOIL/US30_US500/BTC_ETH/AUD_XAU/GBP_UKOIL/USDJPY_US100/EUR_GER40/XAG_US30/EURJPY_USDCHF/GBP_NZD/EUR_CAD; OPEN N154/N155 not cloned; short_hist=no; <=2024; nonoverlap_hold; cost=COST_OK

Drag = RT + (swap_night × hold_days) on stressed overnight side (POST-N78 honesty).
Multi-day holds use **non-overlapping** trade sampling (no inflated overlapping t).

**FLAG:** Survivor maps to **US100cash** overnight hold=3d (drag 6.51 bp; long-swap hostile).
No SPY/US500 twin cleared day_t≥2 this cycle — Lane-B should prefer **session-flat** /
short-bias / D-100 swap-aware sizing, or reject if overnight long cannot clear cost gate.
Prefer remapping to US500 only after re-screen. No agri CFD mapping.

Artefacts: `results/strateeg2_prescreen/cycle_0147/`. Script: `scripts/s2_c028_lane_a_cycle0147.py`.

## Suggested Lane-B mapping (Strateeg — not filed by S2)

- **Symbol:** US100cash
- **FLAG** overnight long US100: prefer session-flat / D-100; no US500 twin this cycle.
- Freeze lookback/thresholds before any 2025+ touch.
- Lane-A bruto day_t + early RT stress ≠ formal PASS.

## Same-cycle family bests

| Family | Best symbols | day_t | mean_bp | cost | promote |
|--------|--------------|------:|--------:|------|:-------:|
| AUDUSD_COMMODITY_FX | AUDUSD->EURUSD | 1.29 | 5.344 | N/A_NO_BRUTO | no |
| COCOA_FOOD_SOFT_MACRO | COCOA->SPY | 1.827 | 3.54 | N/A_NO_BRUTO | no |
| XLK_TECH_SECTOR_STRESS | XLK->NDX | 2.046 | 12.228 | COST_OK | yes |
| XLV_HEALTHCARE_STRESS | XLV->NDX | 1.783 | 6.577 | N/A_NO_BRUTO | no |

Novelty: **4/4 NEW_FAMILY**. Configs: 1350. Promote configs: 1.
