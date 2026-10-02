# Volledige stand van de repo (CEO, 2 okt 2026)
Omvang: 2.197 bestanden op main (985 results, 588 data), 921 commits, 11 branches. Werk door: Grok-agents (Manager/Strateeg/CTO/Uitvoerder), Claude (CEO, Auditor, Uitvoerder-2, Faraday), Debian-agent (MT5-VM).
Getelde trials: 456 (main, catalogus/TRIALS.csv) + 14 CEO-trials (results/ceo/TRIALS_CEO.csv).

## MetaTrader (waar het echt is getest)
- Echte MT5 Strategy Tester-runs (Model=1, 1-min OHLC, €80k, 2021–2026, echte FTMO-spreads/swaps): MomentumRotation.mq5, TrendFollow_CrossAsset.mq5, RSI2Sleeve.mq5 (F1), ORBSleeve.mq5 (F2), combinatie F3/F3b; reconciliatie Python↔MT5 (o.a. 277=277 trades; F1/F2 geslaagd; K1 deels buiten tolerantie, MT5 zwakker). Bugs gevonden via MT5: swap-artefact, order-retry/market-closed, FTMO-dagverlies (Python zag die regel niet, MT5 wel).
- F3b: RSI(2)+ORB op dagverlies-gebonden schaal: SR 0,95 (CI 0,23–1,65), ≈ €225/mnd, FTMO-economie EV −€11/poging (challenge-kans fase 1 25%, funded 17,5%).
- Forward-paper (Debian cron 22:40) loopt sinds 30 sep; FTMO-demo verlopen (trade_allowed=False).
- Mijn (CEO) 15 nieuwe tests zijn Python-only (screening); MT5 voor kandidaat NIET gedaan want geen kandidaat overleefde.

## Wat er getest is (families)
Trend/mean-reversion/momentum-rotatie; RSI(2); ORB (B4a, plateau=PIEK); last-30, gap-reversal; FOMC/pre-FOMC; TSMOM FX/energie/index-short; open-fade; XAU pre-NY; VIX-term; carry/swap; basis/lang/qa-families; P1 ORB+BTC (reserve FAIL, AUDIT_4). CEO: ML (LightGBM shock/dag/COT/ORB-meta → reserve FAIL), NFP-proxy, ORB-regimes+tijdstop+extra indices, turn-of-month, pairs, aandelen-XS, crypto US-open (2 rondes), uur-van-de-dag scan (spread-artefact).
Uitkomst: geen enkele kandidaat haalt de eigen beslisregel (t≥3 train én test, DSR) na kosten.

## Geleerd
1. Kosten/swap zijn de muur (voorspelbare beweging < spread; swap long idx ≈ 7,5%/jr; crypto 30%/jr).
2. Gepubliceerde anomalieën (TOM, pairs, RSI2, SPX-effecten) zijn dood/gedecayd in 2016+.
3. In-sample t≈2–3 verdampt op de reserve (ORB-meta: t 1,76 → reserve −1,15).
4. FTMO-mechaniek: vereiste SR 3–4 voor ~€500–900/mnd bij mean-reversion-profiel; ~1 voor dagelijks-vlak positief-scheef. ORB's SR ~0,6–1 is te laag/onbevestigd.
5. Datafouten: bid-reeks spread-artefact rond rollover; 2021 data onvolledig; lookahead-bugs (zelf gevonden).

## Niveau-oordeel
Proces: boven beginner/retail — pre-registratie, trial-teller, gedeflateerde Sharpe, onafhankelijke audit en Python↔MT5-reconciliatie, FTMO-regels letterlijk, eerlijke negatieve resultaten. Dat is semi-professioneel.
Ideeën/inputs: junior-quant tot hobbyistisch — bijna alles = bekende publieke prijsanomalieën op één venue (FTMO-CFD's) met 5,7 jaar M5; geen unieke databron, geen structurele edge, geen microstructuur/orderflow/fundamentele data. Professionele shops verdienen via data/infrastructuur/execution, niet via zulke signalen. Uitkomst "niets overleeft" is dus verwacht en geen falen van proces.
