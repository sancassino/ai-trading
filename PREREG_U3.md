# PREREG U3 — London-open ORB op EURUSD en GBPUSD (D-015 GO; vastgelegd vóór berekening, 2026-09-30)
- **Regel (B4a-structuur, niets getuned):** sessie 08:00–17:00 Londen (Europe/London, DST-bewust); OR = eerste 30 min (6 M5-bars);
  buy-stop op OR-high / sell-stop op OR-low (OCO, eerste doorbraak telt); stop aan de andere kant van de OR; uit op 17:00 Londen;
  1 trade per dag per symbool. Implementatie = `b4_sim.run_orb` ongewijzigd (conservatief: beide kanten in één bar = verlies).
- **Data/kosten:** FTMO-M5 2021–26; spread instapbar (long) / uitstapbar (short) + 2× commissie (€2,25/lot/kant → EURUSD 0,23 bp,
  GBPUSD 0,19 bp per kant; S0/R1).
- **Kostenpoort (eerst, train 2021–23):** gemiddeld bruto ≥ 3× gemiddelde kosten per trade; faalt → stop zonder trial.
- **Beslisregel (familie van 1):** dag-geclusterde netto t ≥ 3 in train (2021–23) én test (2024–26); N ≥ 500; +50% spread: dag-geclusterde
  test-t ≥ 2. Rapporteer per symbool, per jaar, per-trade-t, dagreeks-SR/skew en correlatie met ORB (F2). TRIAL_COUNT +1 (als de poort gehaald wordt).
