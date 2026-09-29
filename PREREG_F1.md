# PREREG F1 — MT5-EA RSI(2) + reconciliatie met Python (vastgelegd vóór berekening, 2026-09-29)

- EA `RSI2Sleeve.mq5`: symbolen US500.cash, US100.cash, US30.cash, GER40.cash, UK100.cash, XAUUSD; long-only.
  Per symbool bij een nieuwe D1-bar (servertijd): RSI(2) (MT5 iRSI, Wilder) en SMA200 op de laatst afgesloten
  D1-bar. Geen positie en RSI(2) < 10 en slot > SMA200 → kopen; positie en RSI(2) > 70 → sluiten.
  Notional per positie = equity × 1/6 (= E1 gepoold: 6 sleeves à 1/6). Weekend toegestaan (Swing).
  Orders worden herhaald (max 1×/min) tot ze gevuld zijn (market-closed-retry). Dagelijkse equity-log + deals.
- Strategy Tester: Model=1 (1-min OHLC), Deposit 80000 EUR, 2021-01-01..2026-09-24, echte FTMO-swaps/spreads.
- Verschil met Python (e1_rsi2_ftmo.py) dat vooraf bekend is: Python vult op het dagslot, de EA op de eerste
  tick van de volgende serverdag (≈ open na de dagpauze); Python gebruikt constante huidige swap, MT5 de
  tester-swap (punten, bekend artefact — swap_correct.py toepassen voor vergelijking).
- Toleranties (supervisor): maandcorrelatie ≥ 0,9, totaalrendement binnen 25%, trade-aantal binnen 10%.
  Wijkt het meer af: oorzaak zoeken en rapporteren; model of EA corrigeren (gemeld, met vóór/na).
- Geen nieuwe trial (zelfde regel als E1/B2b).
