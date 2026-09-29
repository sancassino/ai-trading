# PREREG C6 — volatiliteits-timing van index-exposure (vastgelegd vóór berekening, 2026-09-29)

- Data: Yahoo ^GSPC (SPX), ^NDX, ^GDAXI (DAX, vanaf 1994) slotkoersen (prijsindex, zonder dividend),
  1990-01..2026-09 (opwarmen vanaf 1988).
- Vol-getimed: maandelijks op de eerste handelsdag (uitvoering op slot), gewicht w = min(1,5; 0,08 / σ21),
  σ21 = jaarlijkse vol van de laatste 21 dagrendementen t/m vorige slot (Moreira & Muir 2017, vol-versie).
- Referentie buy & hold op gelijke vol: constant gewicht = 0,08 / gerealiseerde vol van de index over de hele
  periode (ex-post schaal — alleen voor een eerlijke Sharpe/DD-vergelijking).
- Kosten beide: CFD-financiering (DTB3 + 2%)/365 per kalenderdag over de notional; spread 0,02% per kant
  over gewichtswijzigingen (b&h: alleen instap).
- Rapport per index: CAGR, vol, Sharpe, max DD, per helft; combinatie (gelijk gewogen 3 sleeves) informatief.
- **Beslisregel per index:** Sharpe(vol-getimed) − Sharpe(b&h) ≥ 0,15 **én** max DD < 15% bij 8% vol-target.
- Trials +3 → 344.
