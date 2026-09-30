# PREREG_PORT3 — gevoeligheidsvariant omloop/kosten van P-ETF-a (Manager v32 QA-1) — vastgelegd 2026-09-30 ≈ 18:00Z, vóór forward-start (22:25 UTC) en reserve-run

PREREG_PORT.md en PREREG_PORT2.md blijven onveranderd. Dit is **geen trial en geen selectie**: een extra backtest-rij en een extra forward-portefeuille om het
effect van een drempelregel op omloop en kosten te meten. Na commit niet meer wijzigen (SHA in RUNLOG).

## Simulator op instrumentniveau (nieuw, `port3.py`)
- Instrumenten van P-ETF-a: SPY, BOND10_SYN, GOLD_F (C52 lang) en SPX, NDX, DJI, DAX, N225 (C02); rendementen per instrument volgens het etf-vehikel
  (SPX_TR voor SPX; overige prijsindex/adjclose zoals de engine), cash = rf (engine.rf_on).
- **Doel-exposure** per instrument = P-ETF-a-sleevegewicht (PREREG_PORT: 1/σ, maandelijks, 60 d vertraagd) × sleeve-positie (C52 lang-gewichten; C02 long/cash
  per index / 5), laatste bekende positie op niet-handelsdagen. Posities **drijven mee** met de koersen tussen transacties.
- Twee rijen, zelfde code:
  - **P-ETF-a-inst (drempel 0):** elke wijziging van de doel-exposure wordt uitgevoerd (≈ PREREG_PORT-gedrag op instrumentniveau; referentie).
  - **P-ETF-a-D1 (drempel 1%):** op elke dag met een gewijzigde doel-exposure wordt instrument i alleen verhandeld als |doel_i − huidig_i| ≥ 1,0% van de
    portefeuillewaarde; dan volledig naar doel. Verschil gaat naar/van cash. Geen andere wijzigingen.
- **Kosten:** hoofdrapport **model B** (NL-retail: €3,50 vast per transactie op €80k-schaal + 1,5 bp halve spread; web-claim €3–3,75); model A (6,5 bp per
  eenheid omloop) als gevoeligheid. TER per instrument: aandelen-ETF 0,07%, obligatie-ETF 0,10%, goud-ETC 0,12% (web-claims).
- **Rapport (ontdekking ≤ 2024; reserve niet apart):** omloop/jr, transacties/jr, kosten €/jr, SR (excess), CAGR, maxDD, alfa boven USD-cash, en Δ t.o.v. drempel 0.

## Forward
`forward/portfolio3_daily.csv` (datum; P-ETF-a-inst en P-ETF-a-D1: dagrendement USD, EUR ongehedged, EUR gehedged, aantal transacties die dag), start 2026-10-01,
append-only, zelfde cron (22:25 UTC).

## Vooraf vastgelegde verwachting
D1 halveert grofweg het aantal transacties (≈ 118 → ≈ 40–60/jr) en daarmee de vaste kosten; het effect op SR/alfa vóór kosten is klein (± 0,05 SR). Geen
conclusie over 'beter' zonder de kosten mee te nemen; geen van beide vervangt P-ETF-a (PREREG_PORT) als adviesbasis zonder CEO-besluit.
