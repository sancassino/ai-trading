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
