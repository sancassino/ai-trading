# PREREG Q3 — crypto intraday BTC/ETH, geen overnight (vastgelegd vóór berekening, 2026-09-30)
- Data: FTMO-M5 BTCUSD en ETHUSD 2021–2026 → H1 per serveruur. Spread per bar uit de export (gemeten en gerapporteerd);
  commissie onbekend → conservatief 0,01% per kant. **Geen positie over servermiddernacht** (FTMO-crypto-swap −30%/jr wordt bij
  de rollover berekend): elke positie wordt uiterlijk op het slot van de 23:55-M5-bar gesloten; geen instap na 22:00 server.
- (a) H1-tijdreeksmomentum (long-only): instap op H1-slot als rendement laatste 24 uur > 0 én slot > SMA48(H1); uitstap na
  6 H1-bars of zodra een van beide voorwaarden vervalt (op H1-slot), of de middernachtregel.
- (b) Omkeer na extreme uurbeweging: σ = sd van de laatste 480 H1-rendementen; H1-rendement < −3σ → long, > +3σ → short;
  uitstap na 4 H1-bars of middernachtregel.
- Kosten: spread instapbar (long) / uitstapbar (short) + 2 × 0,01%. Train 2021–2023, test 2024–2026.
- Beslisregel (als Q2): netto t ≥ 3 in train én test, N ≥ 500, ≥ 4/6 jaar positief, DSR(N = 398) > 0,5, bruto ≥ 3× kosten.
- Trials +2 → 398.
