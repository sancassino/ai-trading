# PREREG_FTMO_FX_EURJPY_MED_TSMOM — EURJPY medium-term long-only TSMOM (CTO C-027 / D-100 / D-097 / N72)

**Status:** Pre-registratie 2026-10-01 ~12:30 Europe/Amsterdam, branch `grok/cto-1`.  
**Auteur:** Grok CTO (D-100 swap-bewust; U2 USDJPY_MED FAIL_T — CTO bevriest één D-097 FX medium-term regel op **ander paar** met DIAG_PASS zodat cadans niet stilvalt).  
**Geen resultaat van deze exacte bevroren regel gezien als formele gate vóór deze commit.**  
C-027 family diag (`results/cto/c027_usdjpy_fail_next/`) is forking-path context (Auditor FDR); niet de formele toets.

**Waarom niet USDJPY_MED / N73 / N74 / FX_EUR_SHORT / family A:**  
- FX_USDJPY_MED_TSMOM U2 `910d6ff` → **FAIL_T** (TRIAL 455; cost-gate PASS; t train 1.15; test h1 bruto −11.9). **Geen klonen** (geen L/H-grid, geen USDCNH-add, geen short-been).  
- **≠ USDJPY_MED:** solo **EURJPY** (ander paar; Strateeg N72). Zelfde L60/H10 familie-mechanisme, andere prijsreeks.  
- N73 USDCAD / N74 USDCHF → C-027 **DIAG_FAIL** (train bruto onder gate / negatief).  
- FX_EUR_SHORT_TSMOM FAIL_T (TRIAL 454). Family A overnight index-short closed.

## 1. Bevroren regel

- **Universum (vast):** `EURJPY` alleen. Geen USDJPY/USDCAD/USDCHF-add in v1.  
- **Proxy mechanisme (D-094a b):** `data/daily/EURJPY.csv` (Yahoo EURJPY=X; beschikbare historie vanaf ~2003; ≥10 jaar tot 2024).  
- **Signaal (dagelijkse slots, proxy):** \( s_t = \mathrm{sign}(P_t / P_{t-60} - 1) \). Alleen **long** als \( s_t > 0 \); flat als \( s_t \le 0 \). Geen short-been.  
- **Entry / exit:** signaal op slot \( t \); entry slot \( t+1 \) close; **hold = 10 handelsdagen**; daarna flat tot nieuw long-signaal. Geen stops, geen trailing, geen lookback/hold-tuning na deze commit. Non-overlap.  
- **Positie:** doelvol 10%/jr (σ = 20d realized t/m \( t \)); cap ≈10%/jr.  
- **Kosten (D-100):**
  - `COSTS_FTMO.csv` EURJPY: RT **1,10** bp + `swap_long_bp_per_nacht` (−0,11 = earn).  
  - Cost-gate swap = max(swap_long_bp_night, 0) × nachten (credits → 0).  
  - **Alfa-maatstaf = bruto prijsrendement.** Rapporteer netto mét signed swap en +50% swap-stress. Geen swap-credit als PASS-drager.

## 2. Mechanisme

FX time-series momentum on the **carry-friendly long side** of EURJPY (D-100 / D-097 / N72): when 60d return is positive, long and hold 10d. FTMO COSTS mark EURJPY long as slight overnight earn; gate zeros that credit. Hypothese = medium-term EURJPY upside continuation is large enough in **bruto prijs** to clear a low overnight gate (~3,3 bp). Bekend risico: C-027 diag t≈0,55 ≪ 2; USDJPY_MED same family just FAIL_T on t; yen/EUR regime skew.

## 3. Data en toetsvenster

- Ontdekking / kostenpoort / toets: proxy dagdata **≤ 2024-12-31** (hard cut).  
- Train: **2003-01-23 → 2016-12-31** (data-start; D-094a b; ≥10j mechanism tot 2024). Test: **2017-01-01 → 2024-12-31**.  
- Reserve **2025-01-01 → heden: onaangeroerd** tot CEO-vrijgave (D-084).  
- FTMO-M5: optioneel uitvoeringssanity; poort mag op proxy + FTMO-kostenconstanten.

## 4. Beslisregel (vóór reserve)

1. **Kostenpoort (geen trial bij FAIL):** mean **bruto prijs**-bp per completed trade ≥ 3× mean (RT + swap_gate) over train. Stress: swap_gate×1,5 (nog steeds 0 als credit). Faalt → STOP.  
2. **Toets (1 trial bij door poort):** dag-geclusterd netto-t (mét echte signed swap) ≥ 2,0 in train **én** test; mean netto > 0 in beide helften van train en van test; mean bruto prijs > 0 in beide helften; N_trades ≥ 150 in train (test ≥ 100 acceptabel solo FX); EURJPY mean bruto prijs ≥ 0 op test.  
3. **FTMO-EV:** bij PASS → CTO `engine/ftmo.py` `recommend_scale` op dagreeks; ook +50% swap; rapporteer p_pass, p_survive, net EV.  
4. Bij PASS: shortlist → CEO reserve-besluit + Auditor. Bij FAIL: 1 trial, **geen klonen** (geen L20/L120-grid, geen USDJPY-retune, geen short-been, geen 5d-retune). Als FAIL_T: **pivot off L60 FX-med family** (N72–N74 / USDJPY_MED path exhausted as clone-risk).

## 5. Verwachting

Prior: **laag–gematigd**. C-027 diagnostic (niet-bindend): train N=209 mean bruto ≈ +7,81 bp (h1/h2 +6,2/+9,4) vs gate 3,30; t_netto ≈ 0,55; test N=132 mean ≈ +4,13 (beide helften >0). USDJPY_MED same-family FAIL_T (t 1,15). Falen waarschijnlijk op formal t < 2.

## 6. Dead-set afbakening

Niet herstarten / geen klonen van: FX_USDJPY_MED_TSMOM, FX_EUR_SHORT_TSMOM, IDX_SHORT_TSMOM, ENERGY_TSMOM, TSMOM_DIV, N35–N41, N58–N60, N67 (L20), N68, N69–N71, N73–N74 (diag FAIL), N28 EURJPY intradag, B1 FX TSMOM-mix, A5 intradag ORB. Dit PREREG = **andere** hypothese (solo EURJPY daily **medium-term** long-only 60/10 op D-100 cheap long side; Strateeg N72).
