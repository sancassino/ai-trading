# NEXT_STEPS / BACKLOG v8 — supervisor, 2026-09-30 05:16 Amsterdam

## Beoordeling
- L1 correct afgebroken: rate-limit/paywall **niet** omzeild — goed. Gevolg: ORB (2010–2020) en pre-FOMC-intraday (L2/L3b) kunnen **zonder nieuwe data niet bevestigd worden**. Status daarom: ORB = 'onbevestigd, 5,7 jr, piek', pre-FOMC = 'klassiek effect tot 2011, sindsdien ≈ 0 (2012–26 t 0,88; 2021–26 t 0,07)' → **geen sleeve**. Alleen RSI(2)-overnight overleeft (Yahoo 30 jr t 3,0–3,6; FTMO te weinig power).
- Werkende kern nu: **RSI(2), max 1–2 nachten** (Yahoo t 3,05/3,59; FTMO t 1,79/1,53; dagverlies 2,8–3,6% bij €150/mnd). Dat is klein (≈ €100–200/mnd) maar het is de enige statistisch verdedigbare sleeve.
- Ik stel een **stopregel tegen eindeloos mijnen** in (394 trials): zie 'Steady-state' onderaan.

## BACKLOG (prioriteit 1 = eerst; geen afhankelijkheid van Sandro)

**N1 — MT5-bevestiging van de kern: RSI(2) met max 2 nachten (en aparte run max 1 nacht).** Pas RSI2Sleeve.mq5 aan (input MaxNights = 1|2, exit op de open van nacht MaxNights); regels/symbolen/swap identiek aan F1. Reconcilieer met k1_nights.py (trades ± 10%, maandcorrelatie ≥ 0,9, totaal binnen 25%). Daarna dag-equity-analyse (officieel + streng) en schaal = grootste t met slechtste FTMO-dagverlies < 4% → rapporteer SR (CI), €/mnd op €80k (met G1-kosten), DD. Beslisregel kern: MT5-SR ≥ 0,5 én dagverlies < 4% bij ≥ €100/mnd. Verwacht: SR 0,5–0,8, €100–180/mnd.

**N2 — Datastop netjes opleveren: `DATA_REQUEST_SANDRO.md`.** Beschrijf voor een niet-technisch persoon in ≤ 10 regels per optie de goedkoopste route om lange intraday-data te krijgen: (A) op de VM in MT5 'File → Open an Account' → server MetaQuotes-Demo (of een ander broker-demo met lange indexhistorie) aanmaken en de inlog delen — test zelf eerst met Python of zo'n server ≥ 10 jaar M1 voor US500/US100/GER40/XAU heeft (kijk welke publieke demo-servers dat bieden; noteer bron/voorwaarden; geen omzeiling van beperkingen); (B) HistData handmatig downloaden (exacte URL's/bestandsnamen SPXUSD/NSXUSD/GRXEUR/XAUUSD, maanden) en in data/long_m1/ zetten; (C) Dukascopy-S3 met AWS-account (kostenraming). Geef aan wat je per optie kunt bevestigen en wat het oplevert (ORB 2010–2020; pre-FOMC intraday).

**N3 — Definitieve PLAFOND- en SCENARIO-update.** Herbereken met de kern (RSI2 max 2 nachten) zonder ORB en zonder pre-FOMC; toon apart: 'kern' vs 'kern + ORB (onbevestigd)'. Tabel: SR (CI), €/mnd @80k, realistische kosten, verliesskans 12 mnd, FTMO-dagverlies, challenge-EV, benodigd eigen kapitaal voor €880/mnd. Eén pagina, gewone taal, bovenaan de kernconclusie.

**N4 — Forward-test onderhoud (L5).** Maandagverslag `forward/weekrapport.md`; controleer cron-gaten en dat de eerste echte dag (2026-09-30) is verwerkt (`forward/paper_daily.csv` bestond bij mijn check nog niet — bevestig en meld).

## Steady-state (stopregel tegen data-mining)
Zijn N1–N4 klaar en is de kern-SR ≥ 0,5 óf < 0,5: **stop met nieuwe hypothesen.** Alleen (a) forward-test dagelijks, (b) wekelijks verslag, (c) opnieuw werken zodra Sandro nieuwe data levert (L2/L3b) of zelf een nieuw idee met regels aanlevert. Schrijf dat in RUNLOG als 'steady-state'. Dit voorkomt dat nog 100 trials het DSR nul maken; ik vul de backlog dan alleen aan bij nieuwe data of nieuwe input van Sandro.
