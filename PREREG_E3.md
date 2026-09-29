# PREREG E3 — C4-combinatie onder de FTMO-weekendregel (vastgelegd vóór berekening, 2026-09-29)

- RSI(2)-poot = FTMO-versie uit E1 (6 symbolen, gepoold). Twee varianten:
  - **Swing**: ongewijzigd (posities mogen over weekend).
  - **Standard**: dezelfde toestandsmachine, maar een positie die op de laatste handelsdag van de week openstaat
    wordt op dat slot gesloten (spread) en op het slot van de eerste handelsdag erna heropend als de oorspronkelijke
    regel nog 'in positie' zegt (spread); het rendement vrijdagslot → maandagslot en de weekend-swap vervallen.
- ORB-poot: B4a ongewijzigd (intraday, geen weekendposities).
- Combinatie zoals C4-controle: 1/vol-gewichten en schaal (dag-DD < 8%, dagverlies < 3%) vastgezet op
  2021-09..2023-12, ongewijzigd toegepast op 2024..2026.
- Rapport per variant: SR, t, CAGR, €/mnd op €80k, DD, slechtste dag, DSR(348), train/test, en
  `ftmo_economics.py` (schaal 1) incl. nul-drift-controle.
- Geen nieuwe trial (geen nieuwe signaalregel; uitvoeringsbeperking).
