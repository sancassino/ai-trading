# Eindstand FTMO-onderzoek (CEO, 2026-10-01)

**Conclusie:** er is nog geen sleeve met een gevalideerde edge na kosten. Evaluatie (€540) NIET kopen op basis van wat er nu ligt.

## Cijfers
- 447 geteste trials (TRIALS.csv), alle FTMO-sleeves dood: kostenpoort (A4, A5, B1, A2, S2-XAU/GER40/USDJPY/USOIL/BTC-ETH, N3–N17, IB_FADE, LUNCH_OPEN) of formele t-toets (N11 GER40-ORB, N18 US500-overnight-gap, LUNCH_OPEN).
- Intradag/overnight-edges zijn klein (0–5 bp bruto) tegenover kosten (0,7–3 bp + swap).
- Rekenkundig: €800/mnd vraagt Sharpe ≳ 1,0; bekende ORB-sleeve haalt ≈ €290–300/mnd en is statistisch zwak (t ≈ 1,8).
- Engine `engine/ftmo.py` onafhankelijk gevalideerd (Auditor). Grok- en Claude-PREREGs voldoen aan alle regels (AUDIT_2).
- Reserve 2025+ onaangeroerd.

## Wat kan heropenen
1. Lange M1-data via HistData (SANDRO_ACTIES / M-001): zonder deze data kan de enige sleeve met bruto-edge (ORB) niet langer dan 2021–26 getest worden. ±1 uur werk.
2. Andere markten of andere prop-regels (kleinere account, andere firm).
3. Definitief stoppen.

Alles staat bevroren tot Sandro kiest. Agents openen of kopen nooit iets.
