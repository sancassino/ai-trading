# NEXT_STEPS v14 — Manager, 2026-09-30 10:36 Amsterdam — eerste goedgekeurde Strateeg-voorstellen

Bron: `STRATEGIE_PLAN.md` + `VOORSTEL_S1–S3.md` op branch `claude/trusting-faraday-34tsmg` (haal ze op met `git show origin/claude/trusting-faraday-34tsmg:<bestand>` of merge de branch). R1 (FX-ML) is klaar en afgewezen (bruto ≈ 0) — R2/R4 vervallen.

## Beoordeling Manager (kort)
- Strateeg-plan is sterk: eerlijke kansinschatting (≤ 10%), kosten-eerst, dagelijks-vlak/positief-scheef als criterium, juiste prioriteit (bevestig ORB vóór nieuwe ideeën). Twee vondsten opgepakt: (1) spread/commissie per instrument ontbreekt in de repo → **S0 meten**; (2) M5-export mist tick_volume.
- **FTMO-regels geverifieerd door Manager (ftmo.com, 30-09):** nieuwsregel — Standard-account: geen openen/sluiten (ook geen SL/TP) van 2 min vóór tot 2 min na geselecteerde nieuws, **alleen op FTMO Accounts (funded), niet tijdens de Evaluation**; **Swing: geen nieuwsbeperking**. Fee/accountgroottes: de FAQ-pagina's tonen ze niet leesbaar; **€540 voor €80k blijft onbevestigd** (Strateeg meldt: secundaire bronnen noemen 10k–200k, €540 bij 100k). Sandro moet op de bestelpagina kijken; tot dan is elke EV/frontier-uitkomst 'onder aanname fee'.
- Afgekeurd/aangepast: S3 mag met t ≥ 2,5 alleen als bevroren regel (zie hieronder, aangescherpt).

## WACHTRIJ (volgorde = prioriteit; PREREG vóór resultaat; TRIAL_COUNT)

**S0 — Kostenmeting per instrument (GEEN trial, ≈ 30 min, doe nu).** Uit M5-`spread`-kolom + `SymbolInfo`/specs: mediane en P90-spread per uur-van-de-dag en per instrument voor: US500, US100, US30, GER40, XAUUSD, XAGUSD, EURUSD, GBPUSD, USDJPY, AUDUSD, USDCAD, USDCHF, NZDUSD, EURGBP, EURJPY, USOIL, UKOIL + commissie (€/lot → bp) + swap long/short per nacht in bp (voeg de ontbrekende FX-swaps toe aan `swap_specs_FTMO.csv`). Breid de M5-export uit met **tick_volume** (en exporteer FX-M5 voor de paren hierboven, 2021–26). Lever `COSTS_FTMO.csv` + tabel: break-even-bp intraday en per overnachting per instrument. Dit is de kosten-poort voor alle voorstellen.

**S1 — Noise-area intraday-momentum (Strateeg VOORSTEL_S1).** (a) Probeer eerst de regel uit de volledige paper te verifiëren (Zarattini–Aziz–Barbon 2024, 'Beat the Market…', publiek op SSRN/ResearchGate); lukt dat niet (download geblokkeerd) → noteer dat de regel uit een samenvatting komt en vraag de Strateeg om bevestiging; NIET omzeilen. (b) PREREG (bevries regel, 4 varianten uit voorstel, **kosten-poort eerst**: bruto ≥ 3× rondreiskost anders stop zonder trial-telling). Instrumenten: US500, US100, US30, GER40. Train 2021–23 / test 2024–26; **eis t ≥ 3,5 in beide** (familie van 4), N ≥ 500, ≥ 4/6 jaar+, +50% spread robuust (t ≥ 2). **Extra (Manager):** het paper-venster loopt tot 2024 → rapporteer apart de echte out-of-sample **2025-01…2026-09** (moet positief zijn) en de correlatie met ORB (> 0,7 = geen nieuwe sleeve).

**S2 — Stocks-in-Play ORB op earnings-dagen (VOORSTEL_S2).** Kosten-poort (mediaan-bruto ≥ 8,7 bp op train). PREREG met exacte regel (a)–(d), 41 US-aandelen uit `universe_stocks49` (vast, geen herselectie), events uit `earnings.csv` (859). Beslisregel: t ≥ 3,5 per helft **bij N ≥ 100 events per helft**, ≥ 4/6 jaar+, +50% spread robuust; ≥ 40 trade-dagen/jaar om als sleeve te tellen. Let op: dit lijkt op Q2 (t 1,35/0,91) → rapporteer expliciet wat de stop/EOD-structuur toevoegt en tel ook variant (e) (relatief volume) pas na tick_volume-export als aparte familie.

**S3 — ORB-bevestiging op lange data (VOORSTEL_S3) — WACHT OP SANDRO-DATA.** Bereid alles voor: PREREG_S3 (bevroren B4a-regel, één test), HistData-parser (M1 → M5, EST→server/CET-DST, cash-open-afbakening), `run_s3.sh`, en test de parser op een synthetisch mini-bestand. Beslisregel (Manager-aangescherpt): **bevestigd** = gepoold netto t ≥ 2,5 én beide helften (2011–15, 2016–20) positief én gemiddeld ≥ 0,9 bp/trade (≥ 50% van 2021–26) én ≥ 2 van 3 (US500/US100/GER40) individueel positief; **verworpen** = t < 1 of gemiddelde ≤ 0,5 bp; anders 'onbeslist'. Check eerst of de HistData-index 24-uurs futures-afgeleid is en definieer OR op de cash-open. Draai zodra `data/long_m1/` gevuld is.

**Q6 — Forward-onderhoud** (papier): weekrapport, alarmen.

## Reserve (Strateeg S4–S7, alleen na S0–S2 of na nieuwe data): S4 D1-breakout+trail FX/goud, S5 maandeinde-FX-fix, S6 olie-voorraadcijfers (FTMO-nieuwsregel: Swing/evaluatie geen beperking — geverifieerd), S7 kwartaals-expiratie.

## Regels
Na elke taak RUNLOG + push; volgende taak direct. Bij lege wachtrij: vraag de Strateeg (STRATEGIE_LOG/voorstel) of schrijf zelf VOORSTEL met economische logica; geen nieuwe trials zonder kosten-poort.
