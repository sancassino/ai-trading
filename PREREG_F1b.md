# PREREG F1b — dagverlies-beheersing RSI(2), 3 vaste varianten (vastgelegd vóór berekening, 2026-09-29)

EA RSI2Sleeve met twee nieuwe inputs (standaard uit = gedrag F1):
- `MaxIndexPositions` (0 = onbeperkt): max. gelijktijdige index-posities (US500, US100, US30, GER40, UK100); XAUUSD telt
  apart. Kandidaten die in dezelfde evaluatie-ronde binnenkomen worden op laagste RSI(2) eerst toegelaten.
- `DayGuardPct` (0 = uit): als equity < balance(servermiddernacht) − pct% × startkapitaal → alle RSI-posities sluiten,
  geen nieuwe instappen tot de volgende serverdag. (Servermiddernacht = 23:00 CE(S)T; de 3%-guard laat marge t.o.v. 5%.)

Varianten: (i) MaxIndexPositions = 2; (ii) DayGuardPct = 3; (iii) beide.
Schalen (sizing, geen signaalparameter): LegFrac = s × 1/6 met s ∈ {0,8; 1,0; 1,5; 2,0}. MT5, Model=1, €80k EUR, 2021–2026,
swap_correct.py toegepast.

Rapport per variant: slechtste FTMO-dagverlies (officieel + streng), SR, trades/jaar, en €/mnd op €80k bij de grootste
geteste schaal met slechtste dag < 4%.
**Beslisregel:** een variant blijft alleen als SR ≥ 0,5 én slechtste dag < 4% bij schaal ≥ 0,8.
Trials +3 → 351.
