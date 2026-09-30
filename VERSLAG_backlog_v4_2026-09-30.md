# Verslag BACKLOG v3/v4 (F1–F6, G1–G3) — 2026-09-30

| Taak | Uitkomst |
|---|---|
| F1 MT5-EA RSI(2) | Reconciliatie geslaagd (277 = 277 trades, maandcorr 0,989, totaal 25% verschil = tolerantiegrens). **FTMO-dagverlies 6,1% al bij 100% notional.** |
| F1c dagverliesdefinitie | Geverifieerd op ftmo.com: balance om 00:00 CE(S)T − 5%; floating telt mee. Strengste lezing toegevoegd aan analyze_daily. |
| F1b dagverlies-varianten | Cap / guard / beide: alle afgewezen (SR ≤ 0,44 bij dagverlies < 4%). |
| F2 MT5-EA ORB | Reconciliatie geslaagd (N 9.414 vs 9.249, +1,76 vs +1,73 bp/trade, corr per trade 0,99). |
| F3 (E3-schaal) | Faalt: dagverlies 8,56%, dag-DD 9,6%. |
| **F3b (schaal door dagverliesregel)** | **Kandidaat leeft**: SR 0,95 (CI 0,23–1,65), dag-DD 4,4%, slechtste dag 3,8%, 5/6 jaar+, maar **≈ €225/mnd**; FTMO-EV −€11/poging (funded 17,5%, ~31 mnd tot fase 1). |
| F4 plateau/decay | RSI(2): plateau (t 3,3–3,7 over 9 cellen), maar SPX-edge na 2010 gehalveerd. ORB: piek (sessie-einde nodig; 30 min het sterkst). |
| F5 breedte | 0/18 sleeves opgenomen: edge generaliseert niet buiten US-indices/GER40. |
| F6 demo-forward | **Geblokkeerd**: account '€80k FTMO Free Trial Swing 2-Step' heeft trade_allowed = False (trial verlopen?). Niets gestart. |
| G1 kosten | +50% spread → €200/mnd; + 1 punt slippage/ORB-trade → SR 0,66, **€146/mnd**. |
| G2 beta | corr US500 0,39, beta 0,07; stress 2025-03/04 corr 0,63. |
| G3 (H1–H3) | NR7-ORB, Double 7s, RSI(2)-hoog-vol: alle afgewezen. |

**Stand:** één FTMO-conforme kandidaat (RSI(2) + ORB, Swing) met een kleine edge: ≈ €150–225/mnd op €80k bij realistische kosten,
DSR ruim onder 0,5. Doel €880+ niet haalbaar met deze familie (kans < 5%). TRIAL_COUNT 385.

**Nodig van Sandro:** (1) beslissing over doel/aanpak (zie PLAFOND_RAPPORT.md); (2) voor F6: een nieuwe FTMO Free Trial (Swing, €80k)
of andere demo-inloggegevens in de terminal op de VM.
