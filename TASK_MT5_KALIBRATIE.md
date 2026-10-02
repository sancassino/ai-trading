# TAAK voor Debian-uitvoerder (MT5-eigenaar) — kalibratie Python-sim vs MT5 Strategy Tester
Aanvrager: CEO, 2 okt 2026. Doel: meten hoe accuraat de Python-ORB-sim (b4_sim.run_orb) is t.o.v. MT5 op FTMO-data.
1. EA `ORB_B4a.mq5`: exact PREREG_B4 (a): OR = high/low eerste 30 min (6 M5-bars na sessie-open), vanaf 7e bar eerste doorbraak -> long/short, stop = andere kant OR, 1 trade/dag, uitstap stop of laatste sessiebar. Sessies/tijdzones/servertijd=NY+7 zoals PREREG_B4. Vaste risicogrootte irrelevant: log per trade datum, richting, entry, exit, exit-reden, netto % (incl. spread/commissie).
2. Run in Strategy Tester: modus "Elk tick op basis van echte ticks" (anders: 1-minuut OHLC), symbolen US100.cash en GER40.cash, 2022-01-01..2024-12-31 (NIET 2025+).
3. Lever CSV `results/mt5/orb_mt5_{symbool}.csv` + RUNLOG-regel. Vergelijking per trade met results/b4/B4_a_ORB_trades.csv: % identieke dagen/richting, gem. verschil netto bp, verschil kosten.
4. Bonus: zelfde met 1-minuut OHLC om bar-ambiguïteit te kwantificeren.
Geen parameters tunen. Resultaat bepaalt of CEO-kosten (0,4–1,1 bp ORB) kloppen.
