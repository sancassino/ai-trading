# PREREG_FTMO_FX_EUR_SHORT_TSMOM — EUR short-only TSMOM on D-100 cheap overnight sides (CTO C-025 / D-100)

**Status:** Pre-registratie 2026-10-01 ~11:35 Europe/Amsterdam, branch `grok/cto-1`.  
**Auteur:** Grok CTO (D-100 swap-bewust; U2 IDX_SHORT FAIL — CTO bevriest één family-B regel met positieve diagnostische bruto zodat cadans niet stilvalt).  
**Geen resultaat van deze exacte bevroren regel gezien als formele gate vóór deze commit.**  
C-025 family diag (`results/cto/c025_idx_short_fail_fx_prereg/`) is forking-path context (Auditor FDR); niet de formele toets.

**Waarom niet IDX_SHORT / ENERGY / AUD-long carry / N67:**  
- IDX_SHORT_TSMOM U2 `72f40d3` → FAIL_COST_GATE (bruto −66 bp; equity drift). **Geen klonen** (incl. **N68** GER40 short).  
- ENERGY / TSMOM_DIV → FAIL_COST_GATE (overnight swap wall).  
- C-025 diag: AUDCHF/AUDJPY/USDJPY/USDCHF **long** L20/H10 train means negative → geen PREREG; **N67 DIAG_FAIL**.  
- N58 SWAP_HOSTILE (wrong FX sides). Dit PREREG = EUR **short** sides die in `swap_side_map` goedkoop/earn zijn.

## 1. Bevroren regel

- **Universum (vast):** `EURUSD`, `EURAUD` alleen. Geen EURGBP/EURCHF/EURJPY in v1 (houd N klein; geen post-hoc add).  
- **Proxy mechanisme (D-094a b):**  
  - `EURUSD` → `data/daily/FX_EURUSD.csv`  
  - `EURAUD` → BIS-cross `FXBIS_AUD / FXBIS_EUR` per `data/PROXY_MAP_FTMO.csv` (≥10 jaar tot 2024).  
- **Signaal (dagelijkse slots, proxy):** \( s_t = \mathrm{sign}(P_t / P_{t-20} - 1) \). Alleen **short** als \( s_t < 0 \); flat als \( s_t \ge 0 \). Geen long-been.  
- **Entry / exit:** signaal op slot \( t \); entry slot \( t+1 \) close; **hold = 10 handelsdagen**; daarna flat tot nieuw short-signaal. Geen stops, geen trailing, geen lookback/hold-tuning na deze commit. Non-overlap per symbool.  
- **Positie:** gelijke risico-weging over actieve shorts; doelvol per been 10%/jr (σ = 20d realized t/m \( t \)); portefeuille-vol cap ≈10%/jr via diagonale schaal.  
- **Kosten (D-100):**
  - `EURUSD`: `COSTS_FTMO.csv` RT + `swap_short_bp_per_nacht`.  
  - `EURAUD`: RT = `COSTS_FTMO_alle.csv` `rondreis_bp`; overnight short uit `results/ceo/swap_side_map.csv` / C-024 copy (`short_pct_yr` → bp/nacht; earn = negatieve kosten).  
  - Cost-gate swap = max(swap_short_bp_night, 0) × nachten (credits → 0).  
  - **Alfa-maatstaf = bruto prijsrendement.** Rapporteer netto mét signed swap en +50% swap-stress. Geen swap-credit als PASS-drager.

## 2. Mechanisme

FX time-series momentum on the **carry-friendly short side** of EUR crosses (D-100): when 20d return is negative, short and hold 10d. FTMO `swap_side_map` marks EURUSD short ≈ +0,2 %/jr and EURAUD short ≈ +0,7 %/jr (nearly free / slight earn) vs expensive EUR-long. Hypothese = downside continuation in EUR crosses is large enough in **bruto prijs** to clear a low overnight gate. Bekend risico: 2011/2013 risk-off year skew; EURAUD test weakness in C-025 diag; carry≠alpha (credits zeroed in gate).

## 3. Data en toetsvenster

- Ontdekking / kostenpoort / toets: proxy dagdata **≤ 2024-12-31** (hard cut).  
- Train: **2010-01-01 → 2016-12-31**. Test: **2017-01-01 → 2024-12-31**.  
- Reserve **2025-01-01 → heden: onaangeroerd** tot CEO-vrijgave (D-084).  
- FTMO-M5: optioneel uitvoeringssanity; poort mag op proxy + FTMO-kostenconstanten.

## 4. Beslisregel (vóór reserve)

1. **Kostenpoort (geen trial bij FAIL):** mean **bruto prijs**-bp per completed trade ≥ 3× mean (RT + swap_gate) over train. Stress: swap_gate×1,5. Faalt → STOP.  
2. **Toets (1 trial bij door poort):** dag-geclusterd netto-t (mét echte signed swap) ≥ 2,0 in train **én** test; mean netto > 0 in beide helften van train en van test; mean bruto prijs > 0 in beide helften; N_trades ≥ 150 gepoold over EURUSD+EURAUD; beide symbolen mean bruto prijs ≥ 0 op test.  
3. **FTMO-EV:** bij PASS → CTO `engine/ftmo.py` `recommend_scale` op gecombineerde dagreeks; ook +50% swap; rapporteer p_pass, p_survive, net EV.  
4. Bij PASS: shortlist → CEO reserve-besluit + Auditor. Bij FAIL: 1 trial, **geen klonen** (geen L/H-grid, geen EURGBP-add, geen long-been, geen 5d-retune).

## 5. Verwachting

Prior: gematigd. C-025 diagnostic (niet-bindend) suggereerde pooled train mean bruto ≈ +18,6 bp (N=226; h1/h2 beide >0) vs gate ≈ 2–3 bp — zoekpad-context, geen bewijs. Falen kan: year skew, EURAUD test decay, of formal t < 2.

## 6. Dead-set afbakening

Niet herstarten / geen klonen van: IDX_SHORT_TSMOM, ENERGY_TSMOM, TSMOM_DIV, N35–N41, N58 (hostile), N59, N67 (diag FAIL), N68 (BARRED), B1 FX TSMOM-mix, A5 intradag ORB. Dit PREREG = **andere** hypothese (2-naam daily EUR short-only 20/10 op D-100 cheap sides).
