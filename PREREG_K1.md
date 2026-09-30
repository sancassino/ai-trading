# PREREG K1 — RSI(2)-edge per houdnacht (vastgelegd vóór berekening, 2026-09-30)

Signalen ongewijzigd: RSI(2) < 10 én slot > SMA200 (instap op het dagslot), oorspronkelijke uitstap RSI(2) > 70.
## Data
- Yahoo 1990–2026 (echte opens nodig): SPY (1993+), QQQ (1999+), GLD (2004+) — dividend-gecorrigeerde OHLC — en de
  indices ^GDAXI (1994+) en ^N225 (open-kwaliteit OK volgens B2-check). Signalen op de eigen slotkoersen van elke reeks.
- FTMO 2021–2026: 6 E1-symbolen; signalen op FTMO-D1-slot; 'open' = eerste M5-bar van de cash-sessie (sessietijden B4:
  US500/US100/US30/XAUUSD NY 09:30, GER40 Frankfurt 09:00, UK100 Londen 08:00).
## Ontleding
Per oorspronkelijke trade het rendement per segment: nacht k (slot dag k−1 → open dag k) en dag k (open → slot), k = 1, 2,
3, 4+, tot de oorspronkelijke uitstap. Gemiddelde en t per segment, gepoold per bron.
## Varianten (precies 2)
- (a) uitstap op de **eerstvolgende open** (max 1 nacht); (b) uitstap op de **tweede open** (max 2 nachten; eerder als de
  oorspronkelijke RSI>70-uitstap eerder komt, dan op dat slot).
- Kosten: instapspread (Yahoo 0,02%; FTMO eind-van-dag-spread) + uitstapspread (Yahoo 0,02%; FTMO mediaanspread van de
  eerste sessiebar) + financiering per kalendernacht (Yahoo DTB3 + 2%; FTMO huidige longswap).
## Beslisregel per variant
t ≥ 2,5 op Yahoo (gepoold) **én** op FTMO (gepoold), én FTMO-dagverlies < 4% bij de schaal die ≥ €150/mnd op €80k geeft
(dagverlies = som van de verliezen van alle posities die dezelfde nacht open staan, op die schaal).
Blijkt de edge pas na nacht 3+ te zitten → PLAFOND_RAPPORT: RSI(2) onder FTMO niet schaalbaar. Trials +2 → 391.
