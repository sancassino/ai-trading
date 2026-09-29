# PREREG F3 — MT5-combinatie RSI(2) + ORB op €80k (vastgelegd vóór berekening, 2026-09-29)

- Gewichten/schaal uit E3 (Swing), niet opnieuw gefit: RSI 0,59 / ORB 0,41, schaal 2,35 →
  RSI2Sleeve LegFrac = 0,59 × 2,35 / 6 = 0,2311 per positie; ORBSleeve LegFrac = 0,41 × 2,35 / 7 = 0,1376 per trade.
- **Afwijking (gemeld):** de Strategy Tester draait één EA per test. Beide EA's draaien daarom apart op €80k EUR
  (2021-01..2026-09, Model=1); de combinatie per dag: balance = 80.000 + Σ(balance_i − 80.000), equity idem,
  laagste equity = 80.000 + Σ(min_equity_i − 80.000) (ondergrens, conservatief: de minima vallen niet noodzakelijk
  samen). Compounding per EA apart (klein verschil).
- FTMO-regels op deze dagreeks: dagverlies = balance 00:00 (server) − laagste equity, als % van 80.000; totaal = 80.000 − laagste equity.
- **Beslisregel 'kandidaat blijft leven':** MT5-SR ≥ 0,6 (op dagrendementen, 2021-09..2026 = ORB-periode), max
  dag-equity-DD < 8%, slechtste dagverlies < 4%, ≥ 4/6 jaar positief. Rapport: €/mnd op €80k, funded-kans
  (ftmo_economics op deze dagreeks), bootstrap-CI van de Sharpe. Swap-correctie (swap_correct.py) toegepast op de RSI-poot.
