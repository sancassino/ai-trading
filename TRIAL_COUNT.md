# TRIAL_COUNT — aantal geteste varianten (voor multiple-testing-correctie)

Telling 2026-09-29 (eerlijke schatting; sterk gecorreleerde varianten tellen elk mee).

| Blok | Varianten | Bron |
|---|---|---|
| Overdrachtsdocument mean-reversion (edelmetalen), niet in repo | ~20 (schatting) | Bevindingen/trend-research |
| Python/Yahoo trend-grid (trend 100–250 × ATR 2–4) | ~20 (schatting) | trend-research.md |
| MT5-runs vorige sessies (root-CSV's: TrendFollow TP/ATR/Donchian/regime/buffer, MomRot, MR/TRAIN/TEST) | 89 | root-CSV's |
| Plateau USD (r0/r10/guard/exposure) | 45 | results/plateau |
| EUR-herberekening | 19 | results/eur |
| Breed universum, vol-gecorr., IDX, T10, dual momentum | 51 (+3 ongeldig) | results/wide |
| Ensemble-EA + stap-3-universums | 13 | results/ens |
| Lange validatie A/B (kostengevoeligheid niet apart geteld) | 18 | results/long |
| Ronde 2 (familie 1, 2) | 2 | results/ronde2 |
| **Totaal** | **≈ 300** | |

Gebruik in `stats_tools.py`: N = 300 (eerlijk) en N = 30 (grove schatting "effectief onafhankelijk",
omdat veel varianten buren van elkaar zijn). Bijwerken na elke nieuwe test.

## Log van nieuwe trials (vanaf B1)
| Datum | Taak | Nieuwe varianten | Lopend totaal |
|---|---|---|---|
| 2026-09-29 | B1 (alleen statistiek, geen nieuwe strategie) | 0 | 300 |
| 2026-09-29 | B2 dagfrequent (a IBS, b RSI2, c1 intraday, c2 overnight, d TOM), gepoold | 5 | 305 |
| 2026-09-29 | B3 dollar-neutrale L/S momentum (9 configs × universum A en B) | 18 | 323 |
| 2026-09-29 | B4 intraday FTMO-M5 (ORB, laatste-30-min, gap-reversal), gepoold over 7 symbolen | 3 | 326 |
| 2026-09-29 | C1 pairs/stat-arb (8 paren; ETF-versie = zelfde regel) | 8 | 334 |
| 2026-09-29 | C2 lead-lag (a,b) + vaste vensters (c1 XAU, c2 US100) | 4 | 338 |
| 2026-09-29 | C3 kortetermijn-omkeer markt-neutraal (FTMO-set + Yahoo-bovengrens) | 2 | 340 |
| 2026-09-29 | C4 sizing/combinatie bestaande sleeves (geen nieuwe signalen) | 0 | 340 |
| 2026-09-29 | C5 crypto-trend BTC+ETH | 1 | 341 |
| 2026-09-29 | C6 vol-timing SPX/NDX/DAX | 3 | 344 |
| 2026-09-29 | C7 alleen ontwerp (geen trial) | 0 | 344 |
| 2026-09-29 | D1 EURUSD-intradagseizoen (2 vaste vensters) | 2 | 346 |
| 2026-09-29 | D2 goud vs reële rente | 1 | 347 |
| 2026-09-29 | D3 niet uitvoerbaar (geen trial) | 0 | 347 |
| 2026-09-29 | D4 risicopariteit FTMO-klassen | 1 | 348 |
| 2026-09-30 | E1/E3/F1–F3 validatie (geen nieuwe signalen) | 0 | 348 |
| 2026-09-30 | F1b dagverlies-varianten RSI(2) (cap, guard, beide) | 3 | 351 |
| 2026-09-30 | F4 plateau-buren (niet selecteerbaar: 8 RSI + 5 ORB) | 13 | 364 |
| 2026-09-30 | F5 breedte (8 RSI + 8 ORB + 2 IBS) | 18 | 382 |
| 2026-09-30 | G3-H1 NR7-ORB | 1 | 383 |
| 2026-09-30 | G3-H2 Double 7s, G3-H3 RSI(2) hoog-vol | 2 | 385 |
| 2026-09-30 | I2 intraday mean-reversion H1 (IBS, RSI2) | 2 | 387 |
| 2026-09-30 | I3 event-drift (pre-FOMC, post-nieuws) | 2 | 389 |
| 2026-09-30 | K1 RSI(2) max 1 nacht / max 2 nachten | 2 | 391 |
| 2026-09-30 | J2 (US100 gap-continuatie, XAU ORB Londen, GER40 ORB + US-filter) | 3 | 394 |
| 2026-09-30 | Q2 earnings-gap continuatie / fade | 2 | 396 |
| 2026-09-30 | Q3 crypto intraday (H1-momentum, 3σ-omkeer) | 2 | 398 |
| 2026-09-30 | Q4 ML LightGBM walk-forward (3 horizons) | 3 | 401 |
| 2026-09-30 | VOORSTEL_H-H1 maandeinde-herbalancering | 1 | 402 |
| 2026-09-30 | VOORSTEL_H-H2 pre-feestdag, H3 RSI(2) bij VIX>20 | 2 | 404 |
| 2026-09-30 | R1 FX-ML (15 symbolen, 3 horizons) | 3 | 407 |
| 2026-09-30 | R2 aandelen-ML cross-sectioneel (2 targets) | 2 | 409 |
| 2026-09-30 | R4 Donchian 20/10 + ATR-trailing H4 (FX/goud) | 1 | 410 |
| 2026-09-30 | S1 noise-area intraday-momentum (4 varianten, alle door kostenpoort) | 4 | 414 |

**Noot N7 (2026-09-30):** dag-geclusterde t-waarden van kernresultaten staan in RESULTATEN_GECLUSTERD.md; ORB-B4a (7 symbolen) 2,93 → 1,81, S3-set 3,73 → 2,90; B2b (dagreeks) overleeft (NW 3,80).
| 2026-09-30 | CAT1 catalogusrun 1 (C01, C02, C03, C05, C07, C12, C17; D-037) | 7 | 421 |
| 2026-09-30 | R2/CAT2: C51 (1), C52 (2 varianten), C53 (1), C54 (basis + qa = 2; eerdere 2 rijen ongeldig door future-model-fout, tellen niet) | 6 | 427 |
| 2026-09-30 | R3/CAT3: C04, C16, C29, C33, C43, C44, C45, C55 (1 variant elk; vehikelrapporten cfd_retail zonder trial) | 8 | 435 |
| 2026-09-30 | R4/CAT4: C57, C58, C59, C60, C61 (v1.2-diversifiers; screen/frontier/decompositie zonder trial) | 5 | 440 |
| 2026-09-30 | R5/CAT5: S11 cross-market-replicatie C02 (één familie, 12 markten; regionale C52 informatief zonder trial) | 1 | 441 |
| 2026-09-30 | R7/CAT7: C67 landenrotatie (C66 VRP-proxy = evidentie zonder trial; C65/C68/PutWrite wachten op data) | 1 | 442 |
| 2026-09-30 | A4/PREREG_FTMO_C17 amend 5fc3fb9: C17 FOMC op FTMO-index-CFD (kostenpoort STOP, 1 variant) | 1 | 443 |
| 2026-09-30 | B1/PREREG_FTMO_B1: C05 TSMOM-mix FX6 (kostenpoort STOP, signed-mean poort, 1 variant) | 1 | 444 |
| 2026-09-30 | A2/PREREG_FTMO_A2: US41 SIP-ORB earnings (kostenpoort STOP, mean-poort; **geen** TRIAL_COUNT++ per PREREG §3) | 0 | 444 |
| 2026-10-01 | S2/PREREG_S2_LUNCH_OPEN: lunch open-anchor fade US30/US100 (cost-gate PASS + formal trial FAIL_T, 1 variant) | 1 | 445 |
| 2026-10-01 | N11/PREREG_FTMO_N11: GER40 XETRA ORB (cost-gate PASS + stress FAIL + formal FAIL_T, 1 variant) | 1 | 446 |
| 2026-10-01 | N18/PREREG_FTMO_N18: US500 OVN Gap Cont (cost-gate PASS + stress PASS + formal FAIL_T, 1 variant) | 1 | 447 |
| 2026-10-01 | P1/PREREG_FTMO_P1_ORB_BTC: ORB+BTC eqvol reserve one-shot (FAIL, D-096; 1 variant) | 1 | 448 |
| 2026-10-01 | S2/PREREG_S2_GBPJPY_EU_MOM: Europe-morning session mom (cost-gate PASS + stress FAIL + formal FAIL_T, 1 variant) | 1 | 449 |
| 2026-10-01 | N35/PREREG_FTMO_N35: US100 EU→US cont (cost-gate PASS + stress PASS + formal FAIL_T, 1 variant) | 1 | 450 |
| 2026-10-01 | N36/PREREG_FTMO_N36: XAU NY-open drive (cost-gate PASS + stress FAIL + formal FAIL_T, 1 variant) | 1 | 451 |
| 2026-10-01 | N40/PREREG_FTMO_N40: GER40 mid-morning mom cont (cost-gate PASS + stress FAIL + formal FAIL_T, 1 variant) | 1 | 452 |
| 2026-10-01 | N41/PREREG_FTMO_N41: US30 EU→US cont (cost-gate PASS + stress PASS + formal FAIL_T, 1 variant) | 1 | 453 |
| 2026-10-01 | FX_EUR_SHORT/PREREG_FTMO_FX_EUR_SHORT_TSMOM: EURUSD+EURAUD short-only L20/H10 (cost-gate PASS + stress PASS + formal FAIL_T, 1 variant) | 1 | 454 |
| 2026-10-01 | FX_USDJPY_MED/PREREG_FTMO_FX_USDJPY_MED_TSMOM: USDJPY long-only L60/H10 (cost-gate PASS + stress PASS + formal FAIL_T, 1 variant) | 1 | 455 |
| 2026-10-01 | FX_EURJPY_MED/PREREG_FTMO_FX_EURJPY_MED_TSMOM: EURJPY long-only L60/H10 (cost-gate PASS + stress PASS + formal FAIL_T, 1 variant) | 1 | 456 |
| 2026-10-01 | N78/PREREG_FTMO_N78_VIX_TERM_VOV: US100cash vov10/combo (kostenpoort STOP mean bruto 2.21 < 7.83; **ongeldig/telt niet** per NEXT_STEPS v78 / C-028 — FAIL_COST_GATE ≠ trial) | 0 | 456 |
| 2026-10-01 | N80/PREREG_FTMO_N80: UKOIL OVN-gap cont EOD-flat (kostenpoort STOP mean bruto 7.56 < 8.13; **ongeldig/telt niet** per NEXT_STEPS v81 / C-029 — FAIL_COST_GATE ≠ trial) | 0 | 456 |
| 2026-10-01 | N87/PREREG_FTMO_N87: US30cash opening-gap fade |gap|>30bp intradag-flat (cost-gate PASS + stress PASS train; formal FAIL_T: t_NW 1.63 <2.0 train; test N=27 mean -17.71 bp; 1 variant) | 1 | 457 |
| 2026-10-02 | N92/PREREG_FTMO_N92: US100cash NY-open 2h mom intradag-flat (cost-gate PASS + stress PASS train; formal FAIL_T: t_NW 1.56 <2.0 train; test t_NW 0.51; 1 variant) | 1 | 458 |
| 2026-10-02 | N93/PREREG_FTMO_N93: SECTOR_DISP_ROTATION US100 session-flat (kostenpoort STOP mean bruto 0.99 < 1.98; **ongeldig/telt niet** per NEXT_STEPS v86 / C-029 — FAIL_COST_GATE ≠ trial) | 0 | 458 |
| 2026-10-02 | N100/PREREG_FTMO_N100: EMB_CREDIT_STRESS US100 session-flat (cost-gate PASS + stress PASS train; formal FAIL_T: t_NW 0.38 <2.0 train; test N=154 mean -2.57 bp; 1 variant) | 1 | 459 |
| 2026-10-02 | N101/PREREG_FTMO_N101: CRACK_SPREAD_MACRO US100 session-flat (cost-gate PASS + stress PASS train; formal FAIL_T: t_NW 1.21 <2.0 train; test N=184 mean -5.00 bp; 1 variant) | 1 | 460 |
| 2026-10-02 | N112/PREREG_FTMO_N112: GAS_EQUITY_MACRO US500 session-flat (cost-gate PASS + stress PASS train; formal FAIL_T: t_NW 1.04 <2.0 train; test N=71 mean -4.34 bp; 1 variant) | 1 | 461 |
| 2026-10-02 | N113/PREREG_FTMO_N113: SILVER_GOLD_RATIO US500 session-flat (kostenpoort STOP mean bruto 1.60 < 2.34; **ongeldig/telt niet** — FAIL_COST_GATE ≠ trial) | 0 | 461 |
| 2026-10-02 | N114/PREREG_FTMO_N114: HYG_CREDIT_STRESS US500 session-flat (cost-gate PASS + stress PASS train; formal FAIL_T: t_NW 0.71 <2.0 train; test N=150 mean -2.16 bp; 1 variant) | 1 | 462 |
| 2026-10-02 | N116/PREREG_FTMO_N116: TLT_DURATION_STRESS US500 session-flat (cost-gate PASS + stress PASS train; formal FAIL_T: t_NW 1.17 <2.0 train; test N=124 mean +3.46 bp; 1 variant) | 1 | 463 |
| 2026-10-02 | N117/PREREG_FTMO_N117: CPER_COPPER_STRESS US500 session-flat (cost-gate PASS mean bruto 2.89 ≥ 2.34; stress STOP 2.89 < 3.51; **ongeldig/telt niet** — FAIL_STRESS ≠ trial) | 0 | 463 |
