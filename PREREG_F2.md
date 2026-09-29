# PREREG F2 — MT5-EA ORB + reconciliatie met Python B4a (vastgelegd vóór berekening, 2026-09-29)

- EA `ORBSleeve.mq5`, symbolen US500.cash, US100.cash, US30.cash, XAUUSD (NY 09:30–16:00 = server 16:30–23:00),
  GER40.cash (Frankfurt 09:00–17:30), UK100.cash en EURUSD (Londen 08:00–16:30). Europese sessies in servertijd
  10:00 (of 11:00 in de DST-afwijkingsweken: tussen US- en EU-zomertijdstart in maart en tussen EU- en US-einde
  eind okt/begin nov); servertijd = NY + 7 u.
- Regel = B4a: opening range = high/low van de eerste 30 min (M5-bars). Daarna buy-stop op OR-high en sell-stop op
  OR-low (OCO); bij vulling SL = andere kant; staat de prijs al voorbij een kant → direct marktorder. Eén trade per
  dag. Openstaande positie en orders gesloten/verwijderd op het sessie-einde. Notional per trade = equity × 1/7.
- Strategy Tester Model=1, €80k EUR, 2021-01-01..2026-09-24.
- Reconciliatie (supervisor): N trades binnen 10% van B4a (9.249), gemiddelde bp/trade binnen 0,7 bp,
  teken per jaar gelijk. Bp/trade uit fill-prijzen (spread zit in de fills) + commissie.
- Als MT5 bp/trade ≤ 0 → ORB-poot afgewezen; combinatie zonder ORB herberekenen (expliciet melden).
- Geen nieuwe trial.
