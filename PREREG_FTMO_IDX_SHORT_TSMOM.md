# PREREG_FTMO_IDX_SHORT_TSMOM — short-only index TSMOM on cheap overnight side (CTO C-024 / D-100)

**Status:** Pre-registratie 2026-10-01 ~11:05 Europe/Amsterdam, branch `grok/cto-1`.  
**Auteur:** Grok CTO (D-100 swap-bewust; U2 idle na ENERGY FAIL — CTO bevriest één D-100-regel zodat cadans niet stilvalt).  
**Geen resultaat van deze exacte bevroren regel gezien als formele gate vóór deze commit.**  
C-022 (diagnostic, 0 trials) en C-024 shortlist zijn forking-path context (Auditor FDR); niet de formele toets.

**Waarom niet ENERGY / TSMOM_DIV / N35–N41:**  
- ENERGY_TSMOM U2 `c1499ce` → FAIL_COST_GATE (bruto 29 bp vs gate 272; oil overnight). **Geen klonen.**  
- TSMOM_DIV → FAIL_COST_GATE (monthly L/S + swap).  
- N35/N41 = intradag EU→US sessie-edges (FAIL_T) — andere hypothese dan dagelijkse short-only TSMOM.

## 1. Bevroren regel

- **Universum (vast):** `US100.cash`, `US30.cash` alleen. Geen US500/GER40/HK50 in v1 (houd N klein; geen post-hoc add).  
- **Proxy mechanisme (D-094a b):** `NDX` → US100, `DJI` → US30 uit `data/PROXY_MAP_FTMO.csv` / `data/daily/` (≥10 jaar tot 2024).  
- **Signaal (dagelijkse slots, proxy):** \( s_t = \mathrm{sign}(P_t / P_{t-20} - 1) \). Alleen **short** als \( s_t < 0 \); flat als \( s_t \ge 0 \). Geen long-been.  
- **Entry / exit:** signaal op slot \( t \); entry slot \( t+1 \) close; **hold = 10 handelsdagen**; daarna flat tot nieuw short-signaal. Geen stops, geen trailing, geen lookback/hold-tuning na deze commit. Non-overlap per symbool.  
- **Positie:** gelijke risico-weging over actieve shorts; doelvol per been 10%/jr (σ = 20d realized t/m \( t \)); portefeuille-vol cap ≈10%/jr via diagonale schaal.  
- **Kosten (D-100):**
  - Rondreis uit `COSTS_FTMO.csv` voor US100cash / US30cash.  
  - Overnight: **short-kant** uit kostenbron / `results/ceo/swap_side_map.csv` (short ≈ +0,4 %/jr ≈ vrijwel gratis).  
  - Cost-gate swap = max(swap_short_bp_night, 0) × nachten (credits → 0).  
  - **Alfa-maatstaf = bruto prijsrendement.** Rapporteer netto mét signed swap en +50% swap-stress. Geen swap-credit als PASS-drager.

## 2. Mechanisme

Equity index time-series momentum (Moskowitz–Ooi–Pedersen): persistence in trend; **short leg only** when 20d return negative. D-100 motiveert de short-kant: FTMO index-long betaalt ≈ 8 %/jr swap; index-short ≈ 0…+0,4 %/jr. Hypothese = trendpremie op de downside is groot genoeg in bruto-prijs om een lage overnight-last te dragen. Bekend risico: structurele opwaartse drift (shorts underperform longs); 2020 crash bounce; 2023–24 eenzijdige bull.

## 3. Data en toetsvenster

- Ontdekking / kostenpoort / toets: proxy dagdata **≤ 2024-12-31** (hard cut).  
- Train: **2010-01-01 → 2016-12-31**. Test: **2017-01-01 → 2024-12-31**.  
- Reserve **2025-01-01 → heden: onaangeroerd** tot CEO-vrijgave (D-084).  
- FTMO-M5: optioneel uitvoeringssanity; poort mag op proxy + FTMO-kostenconstanten.

## 4. Beslisregel (vóór reserve)

1. **Kostenpoort (geen trial bij FAIL):** mean **bruto prijs**-bp per completed trade ≥ 3× mean (RT + swap_gate) over train. Stress: swap_gate×1,5. Faalt → STOP.  
2. **Toets (1 trial bij door poort):** dag-geclusterd netto-t (mét echte signed swap) ≥ 2,0 in train **én** test; mean netto > 0 in beide helften van train en van test; mean bruto prijs > 0 in beide helften; N_trades ≥ 150 gepoold over US100+US30; beide symbolen mean bruto prijs ≥ 0 op test.  
3. **FTMO-EV:** bij PASS → CTO `engine/ftmo.py` `recommend_scale` op gecombineerde dagreeks; ook +50% swap; rapporteer p_pass, p_survive, net EV.  
4. Bij PASS: shortlist → CEO reserve-besluit + Auditor. Bij FAIL: 1 trial, **geen klonen** (geen L/H-grid, geen US500/GER40-add, geen long-been, geen 5d-retune).

## 5. Verwachting

Prior: gematigd-laag. Index short-only TSMOM is swap-vriendelijk (D-100) maar vecht tegen drift. C-022 diagnostic had US100 **long_only** L120/H20 rows — andere regel; geen bewijs voor deze short-only 20/10. Falen kan: bruto te klein vs drift, of 2017–24 bull vernietigt short-helften.

## 6. Dead-set afbakening

Niet herstarten / geen klonen van: ENERGY_TSMOM, TSMOM_DIV, N35, N40, N41, P1, classic XS-mom L3/S3, intradag index clones. Dit PREREG = **andere** hypothese (2-naam daily short-only 20/10 op D-100 cheap side).
