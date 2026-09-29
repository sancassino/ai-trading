# PREREG D1 — FX-intradagseizoen met vaste vensters (vastgelegd vóór berekening, 2026-09-29)

Hypothese uit de literatuur (Breedon & Ranaldo 2013, "Intraday patterns in FX returns and order flow"): een valuta
depreciëert gemiddeld tijdens de handelsuren van zijn eigen regio. Toegepast op EURUSD (enige FX in de M5-export):
- (i) **short EURUSD 08:00 → 12:00 Londen** (Europese ochtend; instap open bar 08:00, uitstap slot bar 11:55);
- (ii) **long EURUSD 14:00 → 18:00 Londen** (= 09:00–13:00 New York, US-uren; instap open bar 14:00, uitstap slot bar 17:55).
Elke handelsdag; tijden in Europe/London (zoneinfo), servertijd = NY + 7 u. Kosten: spread van de bar
(long: instapbar, short: uitstapbar) + commissie 0,00225% per kant. Data: FTMO-M5 2021–2026.
Beslisregel per venster (als C2): t ≥ 3 in train 2021–23 én test 2024–26, N ≥ 1.000, expectancy > 0 in ≥ 4/6 jaren.
Trials +2 → 346.
