# PREREG I2 — intraday mean-reversion op H1 (vastgelegd vóór berekening, 2026-09-30)

- Data: FTMO-M5 2021–2026 → H1-bars per serveruur (open eerste, high/low, slot laatste M5-bar; spread = spread van de
  laatste M5-bar). Indicatoren over alle H1-bars (ook buiten de sessie). Symbolen: US500, US100, GER40 (.cash).
- Handelen alleen binnen de eigen cash-sessie (sessietijden als B4): instap op het slot van een H1-bar die binnen de
  sessie eindigt; uiterlijk sluiten op het slot van de laatste M5-bar van de sessie (geen overnight). Eén positie per symbool.
- (a) IBS-intraday: long als IBS(H1) = (C−L)/(H−L) < 0,2 én C > SMA200(H1); uitstap na 4 H1-bars (slot) of sessie-einde.
- (b) RSI(2)-H1 (Wilder, zoals b2_sim): long als RSI(2) < 10 én C > SMA200(H1); uitstap als RSI(2) > 65 (op H1-slot)
  of sessie-einde.
- Kosten: spread instap-bar (long) + commissie 0 (indices); geen financiering (intraday).
- Evaluatie per regel, trades gepoold over 3 symbolen; train 2021–2023, test 2024–2026.
- Beslisregel: N ≥ 1.500, t ≥ 3 in train én test, netto > 0 in ≥ 4/6 jaren, én FTMO-dagverlies < 4% bij de schaal die
  ≥ €150/mnd op €80k geeft. Dagverlies benaderd als som van de verliezende trades van die dag (conservatief; geen
  overnight-stapeling mogelijk).
- Trials +2 → 387.
