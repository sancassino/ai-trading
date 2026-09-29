# PREREG F4 — plateau- en decay-check (vastgelegd vóór berekening, 2026-09-30)

Geen selectie op P&L: de buren worden alleen als kaart gerapporteerd; de kandidaat blijft RSI(2) < 10 / SMA200 en ORB 30 min / sessie-einde.

- (a) Decay: RSI(2) (B2b-regel, Yahoo 1990–2026) per index (SPX, NDX, DAX, FTSE, N225, GLD) — rollende 5-jaars-Sharpe
  (jaarlijks geëvalueerd), en gemiddelde Sharpe 1990–2009 vs 2010–2026.
- (b) Plateaukaart RSI(2): instapdrempel {5, 10, 15} × SMA {150, 200, 250}, uitstap RSI(2) > 70 ongewijzigd; gepoold
  zoals B2b (1/N sleeves, kosten B2), 1990–2026. Rapport: netto t-stat en CAGR per cel.
- (c) Plateaukaart ORB (FTMO-M5 2021–2026, kosten B4): opening range {15, 30, 60} min × uitstap {12:00 lokaal, sessie-einde};
  gepoold over 7 symbolen én per symbool. Rapport: bp/trade en t-stat per cel.
- **Eis (plateau vs piek):** ≥ 2/3 van de buren (alle cellen ≠ kandidaat) hetzelfde teken als de kandidaat én ≥ 50% van
  het niveau (t-stat resp. bp/trade) van de kandidaat. Conclusie alleen 'plateau' of 'piek'.
- Trials: buren zijn niet selecteerbaar; geteld als 'plateau-buren' (8 RSI + 5 ORB = 13) in TRIAL_COUNT voor transparantie.
