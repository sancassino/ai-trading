# PREREG_FTMO_FX_USDJPY_MED_TSMOM — USDJPY medium-term long-only TSMOM (CTO C-026 / D-100 / D-097)

**Status:** **FORMEEL GESTOPT FAIL_T** (U2 `910d6ff`, TRIAL 455; 2026-10-01 ~12:26 CEST). Was: Pre-registratie 2026-10-01 ~12:05 Europe/Amsterdam, branch `grok/cto-1`.  
**Auteur:** Grok CTO (D-100 swap-bewust; U2 FX_EUR_SHORT FAIL_T — CTO bevriest één D-097 FX medium-term regel met positieve diagnostische bruto zodat cadans niet stilvalt).  
**Geen resultaat van deze exacte bevroren regel gezien als formele gate vóór deze commit.**  
C-026 family diag (`results/cto/c026_fx_eur_short_fail_next/`) is forking-path context (Auditor FDR); niet de formele toets.

**Waarom niet FX_EUR_SHORT / N67 / N69–N71 / COFFEE / family A:**  
- FX_EUR_SHORT_TSMOM U2 `0e04df6` → **FAIL_T** (TRIAL 454; cost-gate PASS; test bruto −3.4; EURAUD test −8). **Geen klonen** (geen L/H-grid, geen EURGBP-add, geen long-been).  
- **N67** USDJPY **L20/H10** long → C-025 DIAG_FAIL. Dit PREREG = **L60/H10** medium-term (C-022 D-097 FX path), niet L20 retune.  
- N69 NZDUSD long / N71 GBPUSD short / N70 XAU 5d → C-026 DIAG_FAIL.  
- COFFEE long: honest CEO `spread_bp`≈10.4 → gate ~31 > train bruto; S2 D-092.1 FAIL.  
- Family A overnight index-short closed (IDX_SHORT / N68).

## 1. Bevroren regel

- **Universum (vast):** `USDJPY` alleen. Geen USDCHF/USDCNH/EURJPY-add in v1.  
- **Proxy mechanisme (D-094a b):** `data/daily/FX_USDJPY.csv` (≥10 jaar tot 2024).  
- **Signaal (dagelijkse slots, proxy):** \( s_t = \mathrm{sign}(P_t / P_{t-60} - 1) \). Alleen **long** als \( s_t > 0 \); flat als \( s_t \le 0 \). Geen short-been.  
- **Entry / exit:** signaal op slot \( t \); entry slot \( t+1 \) close; **hold = 10 handelsdagen**; daarna flat tot nieuw long-signaal. Geen stops, geen trailing, geen lookback/hold-tuning na deze commit. Non-overlap.  
- **Positie:** doelvol 10%/jr (σ = 20d realized t/m \( t \)); cap ≈10%/jr.  
- **Kosten (D-100):**
  - `COSTS_FTMO.csv` USDJPY: RT + `swap_long_bp_per_nacht` (−0,37 = earn).  
  - Cost-gate swap = max(swap_long_bp_night, 0) × nachten (credits → 0).  
  - **Alfa-maatstaf = bruto prijsrendement.** Rapporteer netto mét signed swap en +50% swap-stress. Geen swap-credit als PASS-drager.

## 2. Mechanisme

FX time-series momentum on the **carry-friendly long side** of USDJPY (D-100 / D-097): when 60d return is positive, long and hold 10d. FTMO COSTS mark USDJPY long as slight overnight earn; gate zeros that credit. Hypothese = medium-term USDJPY upside continuation is large enough in **bruto prijs** to clear a low overnight gate (~2,3 bp). Bekend risico: test first-half bruto negatief in C-026 diag; N67 L20 path already failed; yen risk-off skew (2008/2022).

## 3. Data en toetsvenster

- Ontdekking / kostenpoort / toets: proxy dagdata **≤ 2024-12-31** (hard cut).  
- Train: **2000-01-01 → 2016-12-31** (D-094a b; ≥10j mechanism). Test: **2017-01-01 → 2024-12-31**.  
- Reserve **2025-01-01 → heden: onaangeroerd** tot CEO-vrijgave (D-084).  
- FTMO-M5: optioneel uitvoeringssanity; poort mag op proxy + FTMO-kostenconstanten.

## 4. Beslisregel (vóór reserve)

1. **Kostenpoort (geen trial bij FAIL):** mean **bruto prijs**-bp per completed trade ≥ 3× mean (RT + swap_gate) over train. Stress: swap_gate×1,5 (nog steeds 0 als credit). Faalt → STOP.  
2. **Toets (1 trial bij door poort):** dag-geclusterd netto-t (mét echte signed swap) ≥ 2,0 in train **én** test; mean netto > 0 in beide helften van train en van test; mean bruto prijs > 0 in beide helften; N_trades ≥ 150 in train (test ≥ 100 acceptabel solo FX); USDJPY mean bruto prijs ≥ 0 op test.  
3. **FTMO-EV:** bij PASS → CTO `engine/ftmo.py` `recommend_scale` op dagreeks; ook +50% swap; rapporteer p_pass, p_survive, net EV.  
4. Bij PASS: shortlist → CEO reserve-besluit + Auditor. Bij FAIL: 1 trial, **geen klonen** (geen L20/L120-grid, geen USDCNH-add, geen short-been, geen 5d-retune).

## 5. Verwachting

Prior: gematigd. C-026 diagnostic (niet-bindend): train N=237 mean bruto ≈ +11,0 bp (h1/h2 +4,0/+17,9) vs gate 2,34; test N=121 mean ≈ +17,3 maar h1 test <0. Falen kan: year skew, formal t < 2, of test-half bruto.

## 6. Dead-set afbakening

Niet herstarten / geen klonen van: FX_EUR_SHORT_TSMOM, IDX_SHORT_TSMOM, ENERGY_TSMOM, TSMOM_DIV, N35–N41, N58–N60, N67 (L20), N68, N69–N71 (diag FAIL), B1 FX TSMOM-mix, A5 intradag ORB. Dit PREREG = **andere** hypothese (solo USDJPY daily **medium-term** long-only 60/10 op D-100 cheap long side).
