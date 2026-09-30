# PREREG S2 — Stocks-in-Play ORB op earnings-dagen (vastgelegd vóór berekening, 2026-09-30)

**Bron van de regel (geverifieerd):** volledige tekst SFI RP 24-98 / SSRN 4729284 ('A Profitable Day Trading Strategy For The U.S. Equity
Market', Zarattini–Barbon–Aziz), open-access kopie in de repository van de Universiteit St. Gallen (item ab50f49b-…). Regel: opening range =
eerste 5-min-kaars; **alleen in de richting van die kaars** (slot > open → buy-stop op OR-high; slot < open → sell-stop op OR-low; doji → niets);
stop-loss op 10% van ATR14 (dag) vanaf de instapprijs; anders uit op de sessie-sluiting; risico 1% per trade, hefboom ≤ 4×.
**Afwijking van VOORSTEL_S2:** het voorstel noemde breakouts naar beide kanten; het paper handelt alleen in de OR-richting → die regel geldt.
In plaats van 'top-20 relatief volume' (paper) selecteren we **earnings-dagen** (voorstel, objectieve catalyst uit het paper, §3).

**Data/universum (vast):** 41 US-aandelen (universe_us41.txt = universe_stocks49 zonder EU-namen), FTMO-M5 2021–26, sessie = alle bars van
de NY-datum (Q2-fix; eerste bar = OR, ook als FTMO pas om 09:35 opent). Events uit earnings.csv: tijd ≤ 09:30 ET → zelfde dag; anders de
volgende handelsdag. ATR14 uit dag-OHLC van dezelfde sessies (14 vorige dagen). Kosten: spread instapbar (long) / uitstapbar (short) +
0,002% commissie per kant; +50% spread als robuustheid.

**Varianten (4):** (a) stop aan de andere kant van de OR; (b) stop 10% ATR14 (paper); (c) = (b) alleen long; (d) = (b) met uitstap 12:00 NY.
**Kosten-poort (Manager, v14):** mediaan-bruto ≥ 8,7 bp per trade op train (2021–23); faalt → stop zonder trial. (Gemiddeld bruto wordt ook
gerapporteerd; bij een positief-scheve stop-strategie is de mediaan meestal negatief — zie vraag U-001 in VRAGEN_UITVOERDER.md.)
**Beslisregel:** netto t ≥ 3,5 in train (2021–23) én test (2024–26), N ≥ 100 events per helft, ≥ 4/6 jaar positief, +50% spread t ≥ 2 in test,
≥ 40 trade-dagen per jaar om als sleeve te tellen. Rapporteer dagreeks (1% risico/trade, ≤ 4×, max 5 gelijktijdig), SR, skew, dagdip, corr ORB.
TRIAL_COUNT +1 per variant die de poort haalt (basis 414).
