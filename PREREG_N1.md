# PREREG N1 — MT5-bevestiging kern: RSI(2) max 1 / max 2 nachten (vastgelegd vóór berekening, 2026-09-30)
- RSI2Sleeve.mq5 + input `MaxNights` (0 = uit = F1-gedrag). Positie sluit op de eerste tick ná de n-de cash-sessie-open na
  instap (n = MaxNights): US500/US100/US30/XAUUSD 16:30 server (= 09:30 NY), GER40/UK100 10:00 server (11:00 in de
  US/EU-DST-afwijkingsweken). Oorspronkelijke uitstap RSI(2) > 70 blijft gelden (wat eerst komt). Overige regels/symbolen
  identiek aan F1 (1/6 equity per positie), Model=1, €80k EUR, 2021-01..2026-09, swap_correct.py.
- Reconciliatie met k1_nights.py (FTMO-deel): trades ± 10%, maandcorrelatie ≥ 0,9, totaal binnen 25%.
- Daarna: dag-equity (officieel + streng), schaal t = grootste waarde met slechtste FTMO-dagverlies < 4% → SR (bootstrap-CI),
  €/mnd op €80k met G1-kosten (+50% spread), DD.
- **Beslisregel kern:** MT5-SR ≥ 0,5 én dagverlies < 4% bij een schaal die ≥ €100/mnd geeft. Geen nieuwe trial (K1-varianten).
