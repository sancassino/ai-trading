# PREREG L3(a) — pre-FOMC op lange Yahoo-dagproxy (vastgelegd vóór berekening, 2026-09-30)
- FOMC-besluitdagen 1994–2026: federalreserve.gov/monetarypolicy/fomchistorical{YYYY}.htm (koppen '… Meeting - YYYY',
  laatste dag van de vergadering; conference calls uitgesloten) voor 1994–2020, en fomccalendars.htm voor 2021–2026 (events.csv).
- Proxy (dagdata, 14:00-ET-slot niet beschikbaar): SPY adjusted, rendement slot(dag−1) → slot(FOMC-dag); dat bevat ook de
  reactie op het besluit (gemeld). Secundair: open → slot van de FOMC-dag. Baseline: zelfde maat op alle niet-FOMC-dagen.
- Beslisregel (NEXT_STEPS v7): event-t ≥ 2,5 over ≥ 120 events (1994–2026), en effect 2010–2020 ≥ 50% van 2021–2026.
  Rapport ook per subperiode 1994–2011 / 2012–2026. Geen nieuwe trial (regel bestond al).
