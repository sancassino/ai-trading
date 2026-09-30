> ## ▶️ 2026-09-30 07:29 — STEADY-STATE OPGEHEVEN, ZOEKTOCHT GAAT DOOR (opdracht Sandro)
> Sandro wil door tot ≈ €800–900/mnd. De stopregel van 05:16 was mijn fout en is ingetrokken. Geen Free Trial/demo-account nodig zolang er geen strategie is die het waard is. Nieuwe backlog (NEXT_STEPS v11): **Q1** inkomens-frontier onder FTMO-regels (wat kan er bij welk risico?), **Q2** aandelen-earnings-events, **Q3** crypto-intraday, **Q4** machine-learning met grote steekproef en streng walk-forward, **Q5** portefeuille-plafond. De vorige eindstand (≈ €50–150/mnd) geldt voor wat tot nu toe getest is (indices, dagsignalen); hij is geen oordeel over alles wat nog niet geprobeerd is.

> ## ✅ 2026-09-30 07:17 — STAND NA ~394 TESTS (kort voor Sandro)
> **Eerlijke eindstand (PLAFOND_DEFINITIEF.md):** met FTMO €80k is realistisch **€50–150 per maand** haalbaar, ~1 op 4 kans op een verliesjaar; **€880/mnd niet haalbaar** met deze aanpak. De MT5-bevestiging van de kern (RSI(2), 1–2 nachten) faalde (Sharpe 0,47; 0,12). De code is onafhankelijk geaudit (geen lookahead) en 6/6 kernresultaten zijn reproduceerbaar (`reproduce.sh`). Een FTMO-challenge is economisch niet de moeite (verwacht ≈ −€10 per poging).
> **De agent staat in steady-state:** dagelijkse papieren forward-test (eerste dag 30-09) + weekverslag, geen nieuwe hypothesen (voorkomt data-mining). Hij bereidt nu alleen voor op jouw input.
> **Jouw keuze (kort):** (1) **stoppen**; (2) **data leveren** voor de ORB-toets (`DATA_REQUEST_SANDRO.md`, ~100 HistData-bestanden; kan hooguit naar ≈ €146/mnd) ; (3) **eigen tradingidee met regels aanleveren** dat we met dezelfde pijplijn kunnen testen; (4) doel bijstellen. Mijn advies: (3) of (1) — meer van hetzelfde levert bij onze data geen doorbraak op.
> Vraag: wil je dat ik de uurlijkse controle verlaag naar bv. 2×/dag zolang de agent in steady-state staat? (Nu: elk uur, zoals je vroeg.)

> ## 🔔 2026-09-30 05:16 — UPDATE + wat ik van je nodig heb
> Lange intraday-data (nodig om ORB en pre-FOMC te bevestigen) is **niet gratis/automatisch te krijgen** (Dukascopy: rate-limit + betaalde S3; HistData: geblokkeerd; Stooq: botcheck). De agent heeft de beperkingen correct **niet omzeild**. Resultaat: **pre-FOMC valt af** (effect tot 2011, daarna ≈ 0), **ORB blijft onbevestigd**. Enige statistisch verdedigbare kern: **RSI(2) met 1–2 nachten vasthouden (≈ €100–200/mnd)**.
> **Jouw opties (kies er minstens één of niets):** (A) 2 minuten op de VM in MT5 een gratis demo-account aanmaken bij MetaQuotes-Demo/andere broker met lange geschiedenis (agent test of die 10+ jaar heeft); (B) HistData-bestanden handmatig downloaden; (C) AWS-account voor Dukascopy (enkele dollars). De agent schrijft stap-voor-stap instructies in `DATA_REQUEST_SANDRO.md`. Daarnaast nog steeds: nieuwe FTMO Free Trial voor echte demo-forward, en beslissen of het doel ≈ €100–250/mnd wordt.
> Ik zet de agent na de huidige taken in 'steady-state' (alleen forward-test + weekverslag) om eindeloos data-minen te voorkomen (394 trials); nieuwe input van jou of nieuwe data start het weer.

> ## 🔔 2026-09-30 02:18 — ACTIE/BESLISSING VAN SANDRO (kort)
> **Stand:** de enige overlevende kandidaat (RSI(2)+opening-range-breakout, in MT5 bevestigd, FTMO-dagverlies-conform) haalt **≈ €225/mnd op €80k, bij realistische kosten ≈ €146–200/mnd** (Sharpe 0,95, CI 0,23–1,65; DD 4,4%, slechtste dag 3,8%). Kans op €880+/mnd **< 5%**. Een FTMO-challenge-poging heeft EV ≈ −€11 (slaagkans funded 17,5%, ~31 mnd) → **economisch nog niet de moeite**. ~385 varianten getest (gedeflateerde Sharpe ≈ 0,3).
> **Wat ik van jou nodig heb:** (1) **Nieuwe FTMO Free Trial (Swing, €80k) of andere demo-inlog op de VM** — het huidige demo-account (login 1514742872) staat `trade_allowed = False` (waarschijnlijk verlopen), dus de echte forward-test kan niet starten; ondertussen draait er een papieren forward-test zonder account. (2) Wil je het doel bijstellen naar ≈ €150–250/mnd, of zoeken we verder naar een ander type edge (nu: intraday-omkeer en event-drift)?

> ## 📊 2026-09-30 00:20 — PLAFOND BEREIKT: eerste kandidaat met kleine, mogelijk echte edge
> Na ~350 vooraf-vastgelegde, multiple-testing-getelde varianten (momentum, trend, carry, pairs, reversal, lead-lag, seizoen, crypto, vol-timing, risicopariteit) is er **één** kandidaat: **RSI(2)-mean-reversion op indices + opening-range-breakout**, op FTMO-data (2021-09..2026): Sharpe 0,98 ± 0,42, ≈ **€480/mnd op €80k (Swing-account)**, max DD 7,8%, slechtste dag −3,0%; Standard-account ≈ €230/mnd. **Gedeflateerde Sharpe 0,27** (dus nog niet bewezen). Verwachte live-uitkomst ≈ **€250–350/mnd**; kans op ≥ €880/mnd **< 10%**.
> Volgende fase (op jouw 'doorgaan'): MT5-bevestiging met echte fills/swaps (F1–F3), plateau-check, meer breedte met identieke regels (F5), en een **forward-test op de FTMO-demo zonder echt geld** (F6). Beslispunt voor jou blijft: accepteer je een doel van ≈ €250–500/mnd, of zoek je een andere bron van edge.

> ## ▶️ 2026-09-29 22:55 — Sandro kiest: DOORGAAN, met sneller werkritme
> Supervisor (Cloud) en uitvoerder (Debian) werken nu volgens `COORDINATION.md`: uurlijkse server-side controle door mij (`SUPERVISOR_LOG.md`), gevulde BACKLOG in `NEXT_STEPS.md` (hoge-breedte-strategieën, long/short-neutraal, gedeflateerde Sharpe), zodat de uitvoerder nooit hoeft te wachten. Onderstaande conclusies over momentum/trend/carry blijven gelden.

> ## ⛔ UPDATE 2026-09-29 (avond): RONDE 2 OOK AFGEWEZEN — WACHT OP JOUW BESLISSING
> Vooraf vastgelegde test (PREREG_ronde2.md) van 2 andere families over 2000–2026, 10% vol-target: **tijdreeks-trend** Sharpe 0,19, CAGR +1,5%, DD 39%; **FX-carry+trend** Sharpe −0,04, CAGR −1,0%, DD 68%. Beide ver onder de drempel (Sharpe ≥ 0,7). Ter vergelijking: SPY @10% vol Sharpe 0,41, +5,7%/jr. (Kanttekening: de agent meldde en herstelde een Sharpe-bug; zonder financiering-markup 0,58/0,42 — óók dan afgewezen.)
> **Conclusie: na 3 strategiefamilies (mean-reversion, trend/momentum-rotatie, multi-asset trend/carry) is er geen aantoonbare edge die het doel (€880–2.000/mnd op €80k, DD<10%) benadert.** De agent staat stil; ik start geen nieuw onderzoek zonder jouw keuze.
> **Jouw keuze:** (A) stoppen; (B) doel drastisch verlagen (bv. alleen kapitaalbehoud/kleine winst — een FTMO-challenge met kosten loont dan niet); (C) een écht andere bron van edge aanleveren (bv. eigen discretionaire/orderflow-strategie met regels die we kunnen backtesten). Mijn advies: A of C. Doorgaan met vergelijkbare systematische families is data-mining.

# EINDVERSLAG (bijgewerkt 2026-09-29 ~17:00) — voor Sandro

> ## ⚠️ BESLISSING VAN SANDRO NODIG
> **De momentum-rotatie-aanpak is duidelijk AFGEWEZEN.** De lange validatie (2000–2026, zonder hindsight en zonder survivorship-bias) laat **geen edge** zien: ensemble +0,04%/jr (26 ETF's) en +0,25%/jr (point-in-time top-10 aandelen) bij 30% exposure, na financiering; bruto ≈ +2%/jr, gelijk aan gewoon SPY kopen. De positieve 2021–2026-resultaten waren een regime-/hindsight-artefact. Willekeurige aandelenuniversums gaven gemiddeld €83/mnd (spreiding ≫ niveau).
> **Het doel €1.000–2.000/mnd op €80k (13–30%/jr bij max 10% DD, dus Sharpe ≳ 1,5) is met deze strategiefamilie niet haalbaar.**
> Keuze voor jou: (A) stoppen met deze richting en een compleet andere strategiefamilie proberen (kans klein, zie onder), (B) je doel verlagen (bv. FTMO-challenge niet loont bij edge van 0–3%/jr; overweeg of het onderzoek de moeite waard blijft), of (C) de agent laten doorgaan met één laatste, vooraf vastgelegde test van 2 andere families (zie NEXT_STEPS.md). Ik adviseer C met harde stopregel, daarna A/B beslissen.

## Update 2026-09-29 (uitkomst NEXT_STEPS ronde 1)
- Stap 2 Python↔MT5: per losse config corr 0,87–0,94 (criterium niet gehaald), ensemble van 9: corr 0,95 → Python bruikbaar op ensemble-niveau.
- Stap 1 lange validatie: NEGATIEF (zie boven). Beslisregel (≥65% jaren+, DD<20%) faalt voor beide universums; 2022 was in universum B −9,9%, 2000–02 −6–7%.
- Stap 3 rang-gevoeligheid: T10 €186/mnd; NVDA-varianten €242 en €406; 5 willekeurige trekkingen €96, €64, €333, €1, −€77 (gem. €83). Dus de 2021–26-uitkomst hangt aan welke aandelen erin zitten (NVDA/PLTR).
- EA-ensemble T10: €186/mnd @30%; @60% breekt dagverlies (8,1%), met guard stort het in (€38–42/mnd).
- Kans einddoel met deze aanpak: **<2%**. Kans op een kleine echte edge (€200+/mnd): **<15%** (was 35–45%).

---
(Onderstaand: eerdere tussenstand, voor context)

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
