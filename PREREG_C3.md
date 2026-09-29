# PREREG C3 — kortetermijn-omkeer, markt-neutraal (vastgelegd vóór berekening, 2026-09-29)

- Universum: de 49 aandelen uit `universe_wide.txt` (FTMO Equities, vooraf vastgelegd).
  - **Primair (beslisgrond): FTMO-D1-koersen** (`<SYM>_rates.csv`), 2021-01..2026-09. Hindsight in de
    keuze van 'welke aandelen' blijft (FTMO-lijst van nu).
  - **Bovengrens: Yahoo adjusted close** van dezelfde 49 namen (EU-namen via ADS.DE, AF.PA, ALV.DE, BAYN.DE,
    DBK.DE, IBE.MC, MC.PA, VOW3.DE; BRK.B → BRK-B), 2000-01..2026-09, namen stromen in zodra data er is.
    Sterke survivorship-bias (huidige samenstelling) → alleen bovengrens.
- Regel: elke 5 handelsdagen (vaste cyclus) op slot t: rangschik op 5-daags rendement (slot t−5 → t);
  long onderste 20% (gelijk gewogen, samen +0,5 van het kapitaal), short bovenste 20% (samen −0,5).
  **Uitvoering op slot t+1**, 5 handelsdagen houden (tot de volgende rebalans). Lokale valuta, geen FX.
- Kosten: 0,05% per kant per aandeel (FTMO-aandelen-CFD-spread + commissie, conservatief). Financiering
  **zoals FTMO nu** (swap_specs_FTMO.csv): long −8,4%/jr, short −6,7%/jr over de notional (constant).
  Diagnostiek (geen beslisgrond): financiering DTB3 ± 2%.
- Beslisregel (op FTMO-set): netto Sharpe ≥ 0,7, t ≥ 3, positief in beide helften (2021–2023, 2024–2026),
  DSR(N = 340) ≥ 0,5. Yahoo-bovengrens: zelfde maten, helften 2000–2012 / 2013–2026.
- Trials +2 → 340.
