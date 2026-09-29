# EINDVERSLAG (tussenstand 2026-09-29) — voor Sandro

> **Stand van zaken: doel (€1.000–2.000/mnd op €80k FTMO, 5+ jaar aantoonbaar) is NIET gehaald.**
> Beste eerlijke schatting zonder hindsight: **≈ €200–330/mnd** bij FTMO-veilig risico. Geen beslissing van jou nodig op dit moment; wel een terugkerend punt: als de lange validatie (NEXT_STEPS stap 1) ook tegenvalt, is de vraag of je een lager inkomensdoel accepteert of de aanpak stopt.

## Wat is geprobeerd
1. Mean-reversion → geen edge.
2. Trendvolgen (SMA-cross, Donchian, wekelijkse regime-exit, hysterese) → geen aantoonbare edge.
3. **Cross-sectionele momentum-rotatie** (elke maand top-N van het universum op 1–3 maanden rendement, gelijk gewogen) + regimefilter (alleen als US500 boven 10-maands gemiddelde) → enige aanpak met een positief teken.

## Wat werkt (concrete cijfers, €80k EUR, MT5 Strategy Tester, 2021-01 t/m 2026-09)
- Teken robuust: 36/36 testruns positief in de blinde testperiode; alle 9 parameterconfigs positief.
- In-sample beste config: €1.069/mnd, maar train €1.321 → test €648 (en parameterkeuze op historie voorspelt niets: rangcorrelatie −0,05 tot −0,28). Dit is dus **geen verwachting**.
- Plateau-ensemble op het oorspronkelijke 16-instrumenten-universum: ~€470/mnd (swap-gecorrigeerd).

## Wat niet werkt / ontmaskerd
- **Hindsight-universum**: het 16-universum bevat NVDA/META/TSLA, de winnaars van juist 2021–26. Zonder hindsight (top-10 marktkap. per eind 2020): **€200/mnd**; alleen indices/grondstoffen: **€130/mnd**; breed universum van 65: verliest geld.
- **Swap-artefact** in de tester (tot 62% van bruto winst) is gecorrigeerd; dat maakte de resultaten beter, maar niet het hindsight-probleem kleiner.
- Dual-momentum-filter: geen verbetering. Equity-guard: helpt alleen bij één config, niet robuust.
- Opschalen naar €880+/mnd vergt 3–4× de exposure → breekt de FTMO-dagverlies- en drawdownregels (dagverlies al 5,2% @30%).
- Winst is geconcentreerd: 2–3 maanden leveren 50–100% van het netto.

## Kans op succes (huidige inschatting)
- Kans dat de strategie een FTMO-fase 1+2 haalt: redelijk voor de meest agressieve in-sample configs (44–62% funded in Monte Carlo), maar die zijn overfit; voor de eerlijke versie veel lager.
- Kans op ≥ €880/mnd live, 12 maanden: in-sample bovengrens 19–22%; realistisch **< 5%**.
- Kans dat er een echte, kleine edge is (€200–450/mnd): **matig (~35–45%)**, in afwachting van validatie over 15+ jaar.
- Kans dat het einddoel €1.000–2.000/mnd binnen de regels wordt gehaald met deze aanpak: **laag (~5%)**.

## Volgende stappen
Zie `NEXT_STEPS.md`: 15–25 jaar onafhankelijke validatie zonder survivorship/hindsight, reconciliatie Python↔MT5, gevoeligheid van universumkeuze, en dan één vooraf vastgelegde ensemble-run.
