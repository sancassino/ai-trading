# PREREG C2 — lead-lag en tijd-van-de-dag op FTMO-M5 (vastgelegd vóór berekening, 2026-09-29)

Data, sessies, tijdzones en kosten exact als PREREG_B4 (spread van instapbar bij long / uitstapbar bij short,
commissie per kant; servertijd = NY + 7u; CET = Europe/Berlin). Geen scan van uren: alleen onderstaande vensters.

- (a) US → Europa: s = teken(US500-rendement van de laatste volledige NY-sessie vóór de Europese datum,
  open 09:30 → slot 16:00 NY = 15:30–22:00 CET). Handel GER40 en UK100 in richting s van hun sessie-open
  (open eerste bar) tot slot van de bar die eindigt op open+60 min. Gepoold over beide.
- (b) Europa → US: s = teken(GER40-rendement open → slot van bar eindigend op open+30 min, zelfde datum).
  Handel US500 in richting s van NY-open (09:30) tot open+60 min.
- (c1) XAUUSD long in vast venster 13:30–14:30 CET (instap open bar 13:30, uitstap slot bar 14:25), elke dag.
- (c2) US100 long in vast venster 15:30–16:00 CET (instap open bar 15:30, uitstap slot bar 15:55), elke dag.
  (Richting long vooraf gekozen: drift-hypothese; vaste CET-vensters letterlijk, ook in DST-afwijkingsweken.)

Beslisregel per test: t-stat (per-trade netto) ≥ 3 in train (2021–2023) én test (2024–2026), N ≥ 1.000,
netto expectancy > 0 in ≥ 4/6 kalenderjaren. DSR met N = 338. Trials +4 → 338.
