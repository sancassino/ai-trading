# PREREG C5 — crypto-trend/momentum BTC + ETH (vastgelegd vóór berekening, 2026-09-29)

- Data: Yahoo BTC-USD (2014-09+), ETH-USD (2017-11+). Instrumenten stromen in zodra 252 + 200 dagen historie.
- Kosten (FTMO, opgevraagd 29-09-2026 via MT5): swap_mode 5 = **−30%/jr op de notional, zowel long als short**
  (per kalenderdag); spread 0,05% per kant (conservatief; FTMO-D1-mediaan BTC 0,001%, ETH 0,03%).
  Diagnostiek (geen beslisgrond): zonder financiering, en met DTB3 ± 2%.
- Regel: maandelijks herbalanceren op de eerste handelsdag (uitvoering op slot). Per asset:
  s = +1 als 12-1-momentum (rendement t−252 → t−21) > 0 **én** SMA50 > SMA200; s = −1 als beide negatief;
  anders 0. Gewicht = 0,5 × 0,20 / σ60 (jaarlijkse vol uit 60 dagrendementen), cap 1,0 per asset.
  Signalen op slot van de vorige dag.
- Rapport: CAGR, vol, Sharpe, t, max DD, jaren positief, per jaar, Sharpe excl. de 2 beste kalenderjaren, DSR (N = 341).
- **Beslisregel:** Sharpe ≥ 0,7 excl. beste 2 jaren, max DD < 25%, ≥ 5 kalenderjaren positief.
- Trials +1 → 341.
