# Verslag BACKLOG B1–B5 (2026-09-29)

Alle taken met pre-registratie vóór berekening (PREREG_B1..B4.md), RUNLOG per taak, TRIAL_COUNT bijgewerkt (326).

| Taak | Uitkomst |
|---|---|
| B1 stats_tools + TRIAL_COUNT | Benodigde Sharpe: €880/mnd → 1,41; €2.000/mnd → 2,12; €400/mnd → 0,95. DSR (N=300): 16-ensemble 0,20, beste config 0,38, T10 0,04, lang A/B 0,00, familie 1/2 0,03/0,00. Niets significant na correctie. |
| B2 dagfrequent, indices 1990–2026 | Alle 5 afgewezen. Dichtst bij: RSI(2) (t 3,65, beide helften +, maar DD 15,9% > 15%; na 2010 ~2%/jr). IBS t 1,93; TOM t 2,49; intraday/overnight door kosten sterk negatief. |
| B3 dollar-neutrale L/S momentum | Beide universums negatief (Sharpe −0,29 / −0,65; bruto 0,02 / −0,30). Momentum-familie definitief dood. |
| B4 intraday FTMO-M5 2021–26 | Alle 3 afgewezen. ORB +0,037 R/trade, t train 2,90 / test 1,14; laatste-30-min en gap-reversal negatief. |
| B5 FTMO-economie | Tool gebouwd. Challenge = optie: EV per poging kan zelfs zonder edge positief zijn bij voldoende vol (loterij, live-breuk 36–96%), geen stabiel inkomen. |

**Stand:** na ~326 geteste varianten in 6 families is er geen edge die de benodigde Sharpe (≥1,4) benadert.
Niets haalde een beslisregel. Data-/tool-verbeteringen: MT5 MaxBars 5M (M5-historie vanaf 2021 beschikbaar),
FTMO-commissie en -spreads per symbool bekend, Python-simulators gevalideerd tegen MT5 op ensemble-niveau.

## VOORSTEL (uitvoerder, COORDINATION regel 1 — backlog leeg)
**"FTMO-EV met MT5-realisme"** — i.p.v. verder zoeken naar een edge (data-mining-risico, zie DSR), de
economisch relevante vraag toetsen: is er een eenvoudige, vooraf vastgelegde positie (US500.cash long met
vol-target en dagverlies-guard; de enige bron met positieve drift over 27 jaar, SPY Sharpe 0,41) die in
**MT5 met echte swap (−5%/jr long) en intraday-dips** een positieve EV per challenge-poging heeft, en hoe
verhoudt die zich tot de nul-edge-controle? Output: EV/poging, P(funded), live-breuk, €/mnd|funded bij
3 vooraf gekozen schalen; beslisregel: EV/poging > 0 én > nul-edge-controle + 2 SE. Eerlijk kader: dit
levert hooguit een positieve-verwachting-gok per €540-fee op, geen stabiel inkomen van €880+/mnd.
Alternatief: stoppen (advies supervisor: A of C in EINDVERSLAG).
