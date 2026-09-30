# Papieren forward-test (NEXT_STEPS v5, I1) — vastgelegd vóór de eerste dag (2026-09-30)

- Script: `forward_paper.py`, dagelijks via cron op de Debian-machine om **22:15 UTC, ma–vr** (na de US-slot).
- Start: **handelsdag 2026-09-30**, vlak (geen posities), €80.000. Geen terugwerkende kracht.
- Regels: exact F3b — RSI(2) (drempel 10, SMA200, uitstap > 70) op US500/US100/US30/GER40/UK100/XAUUSD,
  notional per positie = equity × 0,62/6; ORB (30 min, stop andere kant, sessie-einde) op US500/US100/US30/XAUUSD/GER40/
  UK100/EURUSD, notional per trade = equity × 0,43/7. Kosten: FTMO-spread uit de laatste bar, FTMO-longswap, commissie.
- Data: FTMO-marktdata via MT5 (Python) op de VM; het account hoeft daarvoor niet te mogen handelen.
- Uitvoer: `paper_daily.csv`, `paper_trades.csv`, `state.json`; elke dag commit + push (git-tijdstempel = bewijs).
- Beperkingen: slot-tot-slot (geen intraday-dip voor RSI), geen EUR-conversie, geen slippage.
- Verwachting (supervisor): na ≥ 60 handelsdagen een eerste, nog ruisige indicatie.
- Controle vóór start: droogtest 2026-09-21..29 in een aparte map; ORB-trades per symbool identiek aan backtest B4a.

## Vooraf vastgelegde beslisregel (K2, 2026-09-30 — vóór de eerste forward-dag)
Power (zie results/k1/K2_power.txt): bij ware SR 0,66 duurt 80% kans op t ≥ 2 ≈ 18 jaar; de kans dat de geschatte SR na
6 / 12 maanden < 0 is ondanks een echte edge is ≈ 32% / 25%. De forward-test kan de edge dus niet snel bewijzen; hij
dient om fouten, kostenverrassingen en regimebreuken te vangen. Regels:
1. **Harde review (direct):** papieren dagverlies ≥ 4% of drawdown ≥ 8% → code/kosten/regime controleren vóór doorgaan.
2. **Na 6 maanden (≈ 2027-03-31):** stoppen als de geschatte jaarlijkse SR < −0,29 (25e percentiel bij ware SR 0,66).
3. **Na 12 maanden (≈ 2027-09-30):** stoppen als de geschatte SR < 0; doorgaan en MT5-demo/challenge heroverwegen als SR ≥ 0,66.
4. **ORB-kostencontrole na 6 maanden:** gemiddeld < −1,0 bp/trade (≈ 900 trades) → kosten/slippage onderzoeken (backtest +1,7 bp).
5. Elk forward-verslag vermeldt: slot-tot-slot (geen intraday-dip), geen slippage → papieren resultaat is optimistisch.
