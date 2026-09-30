# Standpunt — waar staan we met de FTMO-zoektocht? (voor Sandro, 30-09-2026)

*Opgesteld door de uitvoerende agent op verzoek van de supervisor (NEXT_STEPS v13, R5). Gewone taal, één pagina.*

**Wat is getest.** ± **410 strategie-varianten** in ± 25 families: trend en momentum (indices, ETF's, valuta's, crypto), carry,
paren-handel, kortetermijn-omkeer, seizoenspatronen, nieuws- en Fed-effecten, bedrijfscijfers (earnings), machine learning op
indices, valuta's en aandelen, en uitbraakstrategieën. Alles vooraf vastgelegd, met kosten van FTMO zelf, en de beste kandidaten
nagebouwd en gecontroleerd in MetaTrader 5.

**Wat de 'kosten-muur' betekent.** Bij FTMO betaal je per trade een spread (0,3 bp op de goedkoopste valuta's, ± 1 bp op indices,
± 3 bp op aandelen, ± 8 bp op crypto) en voor posities die over nacht blijven een financieringsvergoeding (± 5–8% per jaar op
indices en aandelen, 30% op crypto). Machine learning vond wel patronen, maar de voorspelde bewegingen waren **kleiner dan de spread**.
Gepubliceerde effecten (Fed-dagen, maandeinde, feestdagen) bestonden vroeger, maar zijn sinds ± 2012 grotendeels verdwenen.

**Welke 'kwaliteit' is nodig.** Met een simulatie van de echte FTMO-regels (fee, twee fasen, 5%-dagverlies, 10%-max-verlies,
herstarts, 80% winstdeling) blijkt: voor € 500 resp. € 900 per maand netto is een Sharpe van **± 3 resp. ± 4** nodig bij een
strategie die dagenlang verliesposities meedraagt. Bij een strategie die **elke dag vlak gaat, met strakke stops en af en toe grote
winnaars** (positief scheef) ligt die lat veel lager, rond **1** — maar dan betaal je deels voor 'loterij': met hoge inzet en een
begrensd verlies (de fee) levert zelfs een strategie zónder voordeel in de simulatie iets op; in werkelijkheid maken kosten dat negatief.

**Wat we hebben.** Eén kandidaat met dat gunstige profiel: de **uitbraak na het eerste half uur (ORB)** op US-indices/DAX
(Sharpe ± 0,9, positief scheef). Met FTMO-regels en historische kosten ± **€ 480–510 per maand**, met realistische extra kosten
± **€ 150–160**, en 1 op 4 à 2 kans op verlies. Maar: dit voordeel is alleen gezien in 2021–2026, in de tweede helft zwak
(t 1,1), en is **niet bevestigd op langere data**. Alle andere families zijn afgewezen.

**Gefundeerde beslisregel.** Geen enkele nieuwe familie (R1–R4) haalde Sharpe ≥ 1,5 los, en er is geen pad naar een
portefeuille met Sharpe ≈ 3. Daarom:
1. **Eerlijke aanbeveling:** stop de jacht op € 800–900 per maand via FTMO met publieke/systematische signalen, of stel het doel bij.
2. **Eén zinvolle uitzondering:** lever de lange minuutdata (zie `DATA_REQUEST_SANDRO.md`, ± 1 uur klikwerk). Houdt de ORB-uitbraak
   ook in 2011–2020 stand (vooraf vastgelegde regel, geen aanpassing), dan is ± € 150–500 per maand via één FTMO-challenge een
   verdedigbare, beperkte gok (inzet: de fee). Zo niet: stoppen.
3. De papieren test vooruit in de tijd loopt door (dagelijks, wekelijks rapport) en kost niets.

**Sandro beslist.**
