# PREREG C4 — sizing en combinatie van bestaande sleeves (vastgelegd vóór berekening, 2026-09-29)

Geen nieuwe strategieparameters; alleen schaal en weging. Beide stappen gebruiken al bestaande netto-reeksen.

## (a) RSI(2) op SPX + NDX
- Sleeve-dagrendementen uit `b2_sim.sleeve("b", ...)` voor SPX en NDX (100% notional per instrument, netto:
  0,02%/kant + (DTB3+2%) per overnachting), gepoold 50/50, 1990–2026.
- Schaal k = grootste waarde (stap 0,05) waarvoor max dag-equity-DD < 8% **én** slechtste dagverlies < 3%.
  Dit is in-sample sizing (gemeld). Rapport: k, CAGR, Sharpe, €/mnd op €80k, DD, slechtste dag, per helft.

## (b) Combinatie van sleeves
- Selectie (vooraf, drempel supervisor): strategie-niveau (gepoold, primaire toets) met t ≥ 2,5 in B1–B4/C1–C3:
  **RSI(2) gepoold (B2b, t 3,65)** en **ORB gepoold (B4a, t 2,93)**. TOM (t 2,49) valt net af; niets uit C1–C3.
  Per-instrument-cijfers (secundair) worden niet gebruikt om te selecteren.
- ORB-dagreeks: gemiddelde netto trade-rendement per dag over de 7 symbolen (1/7 notional per symbool,
  0 op dagen zonder trade). Overlap met RSI(2): 2021-09..2026-09 (FTMO-M5-periode).
- Gelijk risico: gewichten ∝ 1/vol (over de overlap), daarna schaal k volgens dezelfde regel als (a)
  (dag-DD < 8%, dagverlies < 3%). Rapport: correlatie, gecombineerde Sharpe, t, DSR (N = 340), €/mnd op €80k,
  FTMO-dagverlies-check, en de afstand tot de benodigde Sharpe 1,41.
- Geen nieuwe trials (geen nieuwe signalen); TRIAL_COUNT blijft 340.
