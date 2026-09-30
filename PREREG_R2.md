# PREREG R2 — machine learning cross-sectioneel op 41 aandelen (vastgelegd vóór berekening, 2026-09-30)
- Data: FTMO-M5 2021–2026, 41 US-aandelen (universe_us41.txt); sessie per NY-datum = eerste t/m laatste bar (Q2-bugfix).
  Modelrijen: elke 3e M5-bar (kwartier-raster) binnen de sessie (geheugen: 2 CPU / 3 GB).
- Features: Q4-set (r1/r3/r12/r48, range/ATR, afstand dag-hoog/laag, tijd sinds open sin/cos, dag-van-week, gap, RSI2/RSI14)
  + relatieve sterkte t.o.v. US500 (12-bar en dag-tot-nu-rendement min dat van US500) + cross-sectionele rang (0–1) van het
  12-bar-rendement over de 41 namen op hetzelfde tijdstip + earnings-nabijheid (handelsdagen sinds/tot het dichtstbijzijnde
  event uit earnings.csv, afgekapt op ±10) + symbool als categorie.
- Targets (2 varianten): (a) rendement over de volgende 12 bars (60 min) binnen de sessie; (b) rendement tot het sessieslot.
- LightGBM vaste Q4-parameters; walk-forward 6 → 1 mnd vanaf 2022-01 met purging; training op elke 2e modelrij.
- Handelen: long bij voorspelling ≥ p95, short bij ≤ p5 (van de trainingsvoorspellingen); geen overlap per symbool; kosten = spread
  instapbar (long) / uitstapbar (short) + 0,002% commissie per kant; geen swap (intraday).
- Beslisregel: gepoolde netto OOS-t ≥ 3, positief in ≥ 4/5 testjaren; permutatietest (100×) alleen als t ≥ 3.
  Rapport ook SR na kosten (dagreeks) en correlatie met de ORB-dagreeks. Trials +2 → 409.
