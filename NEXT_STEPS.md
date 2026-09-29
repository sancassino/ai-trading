# NEXT_STEPS — opdracht van supervisor (2026-09-29)

## Beoordeling in het kort
- Goed werk: hindsight-universum ontmaskerd, swap-artefact gevonden, walk-forward gedaan. Dit is de juiste, kritische lijn.
- Eerlijke stand: zonder hindsight (T10) is de edge **~€200–330/mnd bij 30% exposure op €80k** (~3–5%/jaar). Doel is €880–2.000/mnd = 13–30%/jaar bij max 10% DD. Dat is een factor 3–5 te weinig; opschalen van exposure breekt de FTMO-dagregel (dagverlies was al 5,2% @30%).
- Resterende zwaktes:
  1. **Alles leunt op 5,7 jaar (2021–2026), 1 bear-episode (2022).** Eis is 5–10 jaar en meerdere regimes. De 26-jaars Yahoo-proxy is alleen op 4 indices gedaan, niet op het echte universum/de echte regels.
  2. Parameterkeuze heeft geen voorspellende waarde (rho −0,05…−0,28) → verder tunen = data-mining. **Stop met nieuwe parametervarianten op 2021–2026.**
  3. T10-marktkapitalisaties komen "uit eigen kennis" → risico op onbewuste bias (bv. NVDA ~#13 in 2020 net buiten de lijst). Rang-onzekerheid moet als gevoeligheidstest worden meegenomen.
  4. Winst is geconcentreerd (top-3 maanden = 50–100% van netto). Gedeeltelijk winnaars-bias van mega-caps 2021–26.
  5. Swap-correctie is een Python-nabewerking, geen MT5-resultaat. Reconcilieer (zie stap 2).

## Opdracht (in deze volgorde; geen nieuwe parametergrids)

### Stap 1 — Lange, onafhankelijke validatie zonder hindsight en zonder survivorship (Python, Yahoo/Stooq, geen MT5 nodig)
Hypothese: cross-sectionele momentum + SMA10-regimefilter (zelfde regels, dezelfde 9 configs TopN 2–4 × lb 1–3, **exact de bestaande regels, niets tunen**) heeft ook over 2000–2026 een positieve netto-expectancy in een universum dat **vooraf vaststaat en geen survivorship-bias heeft**.
- Universum A (asset-class rotatie): SPY, QQQ, DIA, IWM, EFA, EEM, EWJ, EWG, EWU, GLD (vanaf 2004; ervoor goud-spot), SLV, USO/oliefutures, TLT, IEF, HYG, de 11 SPDR-sector-ETF's (XLK, XLF, XLE, XLV, XLY, XLP, XLI, XLB, XLU, + XLRE/XLC vanaf lancering). Gebruik adjusted close.
- Universum B (single stocks, point-in-time): per 1 januari elk jaar de 10 grootste US-bedrijven op marktkap **voor dat jaar** (gebruik een gedocumenteerde bron; leg de lijst per jaar vast in `universe_pit_top10.csv` mét bronvermelding). Dit omvat ook namen die later zakten (GE, Cisco, Intel, Exxon, Citi, Pfizer, AT&T, Lucent, Nortel enz.); gebruik alleen namen waarvan data beschikbaar is en **rapporteer expliciet welke ontbreken** (survivorship-check). Als data van gedelistte namen niet te krijgen is: zeg dat, en behandel B als bovengrens.
- Rapporteer per jaar 2000–2026: rendement, DD, aantal trades; specifiek 2000–02, 2008, 2020-Q1, 2022. Kosten: 8%/jr financiering (constant %), spread 0,05% per zijde.
- Verwachting/beslisregel: als A én B over ≥15 jaar netto positief zijn in ≥65% van de jaren met portefeuille-DD < 20% bij 30% exposure → edge is niet slechts een 2021–26-artefact; ga naar stap 3. Als B negatief/vlak is en alleen A werkt → dan is de FTMO-uitvoerbare edge (aandelen/indices-CFD's) niet aangetoond; zeg dat glashelder.

### Stap 2 — Reconcilieer Python-simulatie met MT5 (methodologische controle)
Draai `momentum_rotation.py`/`momentum_rotation_daily.py` op precies het T10-universum, 2021-01→2026-09, config TopN=2/lb=3/SMA10/30%, en vergelijk maandrendementen met de MT5-run (`results/...` T10). Rapporteer correlatie en verschil in totaal-€. Verwachting: ≥0,95 correlatie, totaalverschil <15%. Zo niet: de lange Python-resultaten uit stap 1 zijn niet overdraagbaar en dat moet vermeld worden.

### Stap 3 — Rang-gevoeligheid T10 (hindsight-check op de check)
Draai T10-universum nog 2× met alternatieve, plausibele top-10-lijsten (bv. vervang META door NVDA; vervang BABA door TSM/NVDA) en 1× met een **willekeurig getrokken** universum van 10 aandelen uit de 65 wide-lijst (5 trekkingen, vaste seed). Verwachting bij echte edge: alle uitkomsten positief, spreiding ≪ het niveau. Rapporteer de 5 trekkingen in een tabel (geen cherry-pick).

### Stap 4 — Alleen als 1 én 2 slagen: het echte ensemble in de EA (één keer, vooraf vastgelegd)
9 sub-portefeuilles in één account op T10, SMA10, gewichten per symbool opgeteld, dag-guard 3%, **exposure vooraf gekozen op basis van dagverlies ≤ 4% in de MT5-run** (niet op winst kiezen). Eén run, één rapport: €/mnd, statische DD op dag-equity, max dagverlies, dag-Monte-Carlo funded% en live ≥ €880. Geen herhaling met andere exposure tot na rapportage.

### Stap 5 — Rapportage
Voeg RUNLOG-regel toe per stap. Bij een negatief resultaat: schrijf dat op, niet zoeken naar een variant die het toch redt.

## Verwacht beeld (mijn prior, zodat je kunt zien of iets afwijkt)
- Stap 1A: momentum op asset-class/sector werkt historisch matig, ~4–8%/jr bruto, DD-jaren 2000–02/2008 grotendeels gedempt door SMA10. Stap 1B: positief, maar duidelijk lager dan het 16-universum.
- Stap 2: Python en MT5 wijken enkele % af (swap, spread, gaps).
- Stap 3: spreiding van ±€100/mnd rond €200.
- Realistisch plafond bij FTMO-veilig risico: ~€200–450/mnd. €1.000+/mnd blijft alleen haalbaar als stap 1 een veel sterker signaal laat zien dan tot nu toe.
