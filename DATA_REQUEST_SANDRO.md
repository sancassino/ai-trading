> **UPDATE 2026-09-30 10:54 (CEO-besluit D-001): VERKLEIND.** Alleen **2011 t/m 2020** downloaden (niet 2010, niet 2021+; die hebben we al via FTMO): ≈ **40 zips** i.p.v. ≈ 100. Volgorde: **SPX/USD → NSX/USD → GRX/EUR → XAU/USD**; lever **SPX eerst** (dan krijgen we al een voorlopige uitslag). Zips niet uitpakken, in `ai-trading/data/long_m1/` op de Debian/VM-machine (of een Drive-link). Inspanning ± 30–45 min. Optie C/D (AWS/betaald) niet nu.

# Dataverzoek aan Sandro — lange minuutdata (2010–2026) om de strategie buiten 2021–2026 te testen

**Waarom:** alle intraday-resultaten rusten nu op FTMO-data van 5,7 jaar. Met 10+ jaar extra data kunnen we de
"uitbraak na het eerste half uur" (ORB) en het effect rond Fed-besluiten echt bevestigen of verwerpen. Ik heb geen gratis bron
gevonden die geautomatiseerd downloaden toestaat (en omzeil geen blokkades). Kies één optie:

## Optie B — HistData handmatig downloaden (gratis, ± 1 uur klikwerk) — aanbevolen
1. Ga naar https://www.histdata.com/download-free-forex-data/?/ascii/1-minute-bar-quotes
2. Kies per instrument: **SPX/USD** (S&P 500), **NSX/USD** (Nasdaq-100), **GRX/EUR** (DAX), **XAU/USD** (goud).
3. Download per jaar **2011 t/m 2025** (klik op het jaar, dan op de link "HISTDATA_COM_ASCII_…_M1….zip"); voor **2026** per maand
   (januari–augustus). Voor SPX/NSX/GRX begint de data in november 2010 (die maand mag ook).
4. Zet alle .zip-bestanden (niet uitpakken) in een map en upload die naar de VM of Debian-machine in `ai-trading/data/long_m1/`
   (of zet ze in Google Drive en deel de link).
5. Totaal ± 4 × 24 ≈ 100 bestanden, samen naar schatting enkele honderden MB.
Wat het oplevert: ORB en pre-FOMC-intraday op 2011–2020 (≈ 10 jaar extra, onafhankelijk van FTMO). Geen US30 beschikbaar.

## Optie C — Dukascopy via Amazon (AWS), vrijwel gratis maar technisch
1. Maak een AWS-account (creditcard vereist).
2. Dukascopy stelt historische data beschikbaar in een 'Requester Pays'-bucket: je betaalt het ophalen zelf.
3. Kosten voor minuutdata van 6 instrumenten 2010–2026: naar schatting **minder dan $1–5** (± $0,0004 per 1.000 bestanden + $0,02/GB).
4. Deel een AWS-toegangssleutel met alleen leesrechten (ik zet het downloadscript klaar).
Wat het oplevert: alles van optie B plus US30 en betere spreadinformatie.

## Optie A — demo-account bij een andere MT5-server (onzeker)
1. Op de VM in MetaTrader 5: File → Open an Account → bijvoorbeeld **MetaQuotes-Demo** → demo-account aanmaken (vraagt naam/e-mail).
2. Laat de terminal ingelogd; ik controleer met Python of die server ≥ 10 jaar minuutdata voor S&P 500/Nasdaq/DAX/goud heeft.
3. **Niet door mij geverifieerd** (ik kan geen account aanmaken namens jou); veel demo-servers hebben voor indices maar enkele jaren.
Wat het oplevert: alleen iets als de server lange indexhistorie heeft.

**Mijn advies:** optie B (gratis, betrouwbaar genoeg, geen accounts). Laat weten welke optie je kiest; zodra de data er staat
voer ik L2/L3b (ORB en pre-FOMC op 2011–2020) direct uit met de vooraf vastgelegde regels.
