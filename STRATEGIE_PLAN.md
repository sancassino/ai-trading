# STRATEGIE_PLAN (Strateeg, bijgewerkt 2026-09-30 10:55 Amsterdam) — v1.1

**Update 10:55:** Manager heeft S0–S3 goedgekeurd (NEXT_STEPS v14). Nieuw op main: R1 (FX-ML) en R2 (aandelen-ML) afgewezen (bruto ≈ 0, zoals verwacht), **R4 (Donchian/ATR-trail H4 op FX+goud) afgewezen** (netto −3,1 bp, t −1,8/+0,2; alleen XAU positief) → mijn S4 is grotendeels afgedaan (alleen D1/lange FRED-historie blijft, prior nu laag). FX-kosten zijn nu **gemeten** (R1: spread 0,18–0,85 bp, per kant 0,28–0,86 incl. commissie) → FX-rijen in §2 zijn G i.p.v. A. Geen S1-regelbevestiging mogelijk: SSRN/concretum/sfi geven alleen de samenvatting; ik heb de bandformule uit geheugen → **niet als exact beschouwen**. Gevraagd aan Sandro (2 min, optioneel): paper-PDF handmatig van SSRN (abstract_id=4824172) in `docs/` zetten. Zo niet: S1 alleen met expliciet label 'regel uit samenvatting', en dan is een negatief resultaat geen bewijs tegen het paper.

Eerlijk vooraf: met 404 trials, kosten-muur en ~5,7 jr data is de kans dat hieruit €800–900/mnd via FTMO komt **klein (mijn schatting ≤ 10%)**. Dit plan maximaliseert de kans per uur Uitvoerder-tijd; het belooft niets. Details/bronnen: `STRATEGIE_BIJLAGE.md`.

## UPDATE 11:25 Amsterdam (v1.2) — uitslagen en koers
- **S1 afgewezen** (alle 4; train +2,2 bp t 2,2, test +0,7 t 0,9, OOS 2025–26 +0,3 bp; corr ORB 0,52). **S2 gestopt op kostenpoort** (alle 4; let op: Uitvoerder vond dat het paper alleen in de richting van de eerste kaars handelt — mijn voorstel noemde beide kanten; bron-check door Uitvoerder was hier dus nodig en juist). S0: kosten gemeten (indices 0,45–0,78 bp, FX-majors 0,63–1,22, XAU 0,83). Q7: ORB+RSI(2) verlaagt de FTMO-uitkomst → ORB alleen.
- **Patroon:** ORB en S1 zijn sterk in 2021–23 (vooral 2022), ≈ 0 in 2024–26. Twee lezingen: (a) vervallen/gearbitreerd, (b) volatiliteitsregime-effect. S3 (2011–20) scheidt dit **alleen** als het regime-label vooraf vastligt → S9. Trap 1 hangt aan S3.
- **Ik heb geen sterke nieuwe signaal-kandidaat** en verzin er geen bij (D-013). Geschrapt volgens D-009: S4, S5, S7; S6 alleen exploratief. Ik stel nu twee *niet-signaal*-voorstellen voor: **S8** (decay-bewuste FTMO-EV van ORB; gratis, geen trial) en **S9** (vol-regime-diagnose + één bevroren toets op S3-data, vóór de data wordt geopend in PREREG_S3 op te nemen).
- **Compliance-kanttekening bij D-013:** 'weinig trades/lage vol/alleen fase 1 halen en uitbetaling minimaliseren' of hoge schaal om optiewaarde te pakken is gokgedrag / misbruik van de fee-structuur (R3: nul-edge al +€216/mnd door vol alleen). Ik stel dat **niet** voor; S8 rapporteert zulke schalen alleen als bovengrens.
- Sandro: geen verzoeken meer (D-014). §4 hierboven (data-opties) blijft als passieve referentie; A-01/A-02 lopen via de CEO.

## 1. Gap-analyse (wat is níet onderzocht)
- **Instrumenten:** FX-majors/crosses zijn nauwelijks getest (alleen EURUSD: carry-seizoen/ORB/ML-idee; geen GBP/JPY/AUD/CHF/CAD-intraday; R1 ligt open). Energie (USOIL/UKOIL/NATGAS) alleen pairs + ORB-1; koper/platina/zilver ≈ niets. Indices buiten US/GER: RSI/ORB-breedte F5 negatief (AUS, HK, JP, EU, FRA, SPN, N25) — afgedaan. US2000 en DXY geen data.
- **Strategietypes:** (i) *intraday momentum met volatiliteitsbanden + trailing stop* (Noise-area) — niet getest, ORB is het enige aanverwante; (ii) *ORB op 'stocks in play'* (Q2 testte vaste 60-min-houdduur, geen stop/EOD-structuur); (iii) D1-breakout met trailing op FX/goud (positief scheef) — alleen als R4 gepland; (iv) flow-events (FX-fix, expiraties) — niets; (v) hedging-flow/laatste-30-min **voorwaardelijk** op dagbeweging — B4b was onvoorwaardelijk.
- **Data ontbreekt:** lange intraday (2008–2020) voor alles; **spread/commissie per instrument** staat niet in de repo (alleen E1-eind-van-dag-spreads, Q2/Q3-gemiddelden) → kosten-eerst is nu deels aanname; M5-export bevat **geen tick_volume** (nodig voor relatief-volume-filter); FX-M5 bestaat alleen voor EURUSD; swap-tarieven zijn één momentopname (tijdvariabel); FX-swaps ontbreken in `swap_specs_FTMO.csv` (alleen EURUSD).
- **Methodisch:** nagenoeg alle recent gepubliceerde regels testen we op 2021–26, dat grotendeels in hún steekproef ligt → echte out-of-sample is alleen 2025–26 of lange data. Dat maakt S3 (lange data) de hoogste-waardetaak.

## 2. Kosten-eerst (samenvatting; volledige tabel in bijlage)
Break-even = spread + 2×commissie (intraday) of + swap/nacht (overnight). Gemeten = uit repo; "a-priori" = niet gemeten, door S0 te verifiëren.
| Klasse | Rondreis-kosten intraday (bp) | Swap long / short (bp per nacht) | Bron |
|---|---|---|---|
| FX-majors (EURUSD, GBPUSD, USDJPY, USDCAD, USDCHF) | ≈ 0,6–0,8 rondreis (spread 0,18–0,33 + commissie 0,19–0,26/kant); AUD/NZD/crosses 1,0–1,7 | EURUSD −1,1 / +0,1; USDJPY long +0,4 / short −1,6 | gemeten (R1), swaps data/swap_specs_fx.csv |
| US-indices (US500/US100/US30) | ≈ 0,5–0,8 | −1,4…−2,3 / −0,8…+0,1 | gemeten (E1) |
| XAUUSD | ≈ 0,8 (comm 0,1) | −2,2 / −0,1 | gemeten |
| GER40 | ≈ 1,4 | −1,8 / 0 | gemeten |
| Aandelen-CFD (US) | ≈ 2,9 | −2,3 / −1,8 | gemeten (Q2) |
| UK100 | ≈ 7 (eind-van-dag) | −2,3 / +0,1 | gemeten (E1) — schrappen |
| Crypto | ≈ 8–9 | −8,2 / −8,2 | gemeten (Q3) — schrappen |
**Afleiding:** goedkoopst = FX-majors, US-indices, goud, dan GER40, dan aandelen. Swap is **asymmetrisch**: shorts houden op indices/goud/FX kost ≈ 0, longs 1,4–2,3 bp/nacht (5–8%/jr). Intraday-flat vermijdt dat helemaal. Positieve "swap" op EU50/FRA40/USOIL-long is dividend/roll-artefact — niet als bron gebruiken.

## 3. Portefeuille van 8 voorstellen (volgorde = prioriteit)
Toets voor elk: dagelijks-vlak, positief scheef, kosten laag, structurele oorzaak. Bruto ≥ 3× kosten is een **poort vóór formele trial** (S0 meet dit gratis).
0. **S0 Kostenmeting (geen trial):** spread per uur/instrument uit M5-`spread`-kolom voor alle relevante symbolen (+ tick_volume, FX-M5 export). Ontgrendelt 1–8.
1. **S3 ORB-bevestiging op lange data** (bevroren B4a-regel, SPX/NSX/GRX/XAU 2011–20). Hoogste waarde/kosten; vereist Sandro (§4). `VOORSTEL_S3.md`.
2. **S1 Noise-area intraday-momentum** (Zarattini–Aziz–Barbon 2024: volatiliteitsbanden, trailing, EOD-exit) op US500/US100/US30/GER40. Zelfde mechanisme als ORB maar vol-genormaliseerd; structurele oorzaak = gamma-/hedgingvraag + onder-reactie. `VOORSTEL_S1.md`.
3. **S2 Stocks-in-Play ORB** (earnings-dagen, 5-min ORB, stop, EOD) op 41 FTMO-aandelen; data grotendeels aanwezig (earnings.csv). Oorzaak: nieuws-gedreven order-onbalans. `VOORSTEL_S2.md`.
4. **S4 (AFGEWEZEN op H4 door R4; D1-variant laag)** D1-breakout met trailing op FX-majors + goud (Donchian 20/10 of ATR-trail, 1 regel; sluit aan op Manager-R4). Positief scheef, kosten ≈ 0 op D1; lange historie via FRED-FX (1971+, noon-fixings) en Yahoo-goud. Let op: houdt posities over nacht → dagverlies-dip (meegedragen float) telt.
5. **S5 Maandeinde-FX-fixing** (Melvin–Prins: rebalancing-flows rond WM/Reuters 16:00 Londen) EURUSD/GBPUSD/USDJPY/AUDUSD. Flow-oorzaak, kosten ≈ 0,5 bp, maar N klein (~70 maandeinden × 4) en effect waarschijnlijk afgenomen sinds 2015-fixing-hervorming → lage kans.
6. **S6 Olie-voorraadcijfers (woensdag 16:30 CET) onderreactie-drift** na eerste 15 min, alleen intraday. NB: FTMO-nieuwsregel ±2 min verifiëren (Manager). Geen straddle rond nieuws.
7. **S7 Kwartaal-expiratie/herbalancering slotveiling** (3e vrijdag mrt/jun/sep/dec): slotbewegingsdrift. N ≈ 22 dagen × 4 indices → ver onder N ≥ 500; alleen exploratief, waarschijnlijk niet bewijsbaar.
8. **R1 FX-ML-breedte: uitgevoerd en afgewezen (bruto ≈ 0) — bevestigt mijn prior.** Q4 toont: voorspelbare beweging < spread; FX is het meest efficiënte vlak; kosten laag maar signaal lager. Pas ná S1–S4; 15 paren × 3 horizons = 45 trials → multiple-testing-zwaar.

## 4. Data-strategie (gewone taal; Sandro beslist, niemand doet iets zonder hem)
Doel: dezelfde *bevroren* regels (ORB, straks noise-area) op 2011–2020 laten draaien. Eén bevestiging weegt zwaarder dan tien nieuwe ideeën.
| Optie | Wat | Kosten | Jouw werk | Kanttekening |
|---|---|---|---|---|
| **B. HistData** (in `DATA_REQUEST_SANDRO.md`) | 1-min SPX/NSX/GRX/XAU, 2010-11→ | gratis | ± 1 uur klikken, ~100 zips naar `data/long_m1/` | quotes van een broker-feed, geen US30; sessietijden controleren |
| **C. Dukascopy via AWS** | 1-min, ook US30, spreadinfo | naar schatting < $1–5 (opgave Manager/Uitvoerder, niet door mij geverifieerd) | AWS-account + creditcard, read-only sleutel | "Requester Pays" is hun officiële route |
| **D. Betaalde set (FirstRate Data)** | SPX-index en ES-futures 1-min, 2008→; 1 mnd updates gratis, daarna $99,95/jr (firstratedata.com); **aankoopprijs niet gevonden** | onbekend — Sandro checkt prijs | bestelling + download | schoon, exchange-gebaseerd (beste kwaliteit) |
| **A. Andere MT5-demo** (bv. MetaQuotes/IC-brokers) | kan lange M1-historie hebben | gratis | demo aanmaken op naam Sandro | niet geverifieerd; indices vaak kort |
Mijn advies: **B eerst** (gratis, genoeg voor SPX/NSX/GRX/XAU); D alleen als B tegenvalt of je US30/futures-kwaliteit wil. Geen scraping of omzeilen van limieten.

## 5. Venue/product-check (analyse, geen actie; bronnen in bijlage)
- FTMO 2-Step (statisch 5%/10%) past bij dagelijks-vlak + positief scheef; **1-Step is slechter** (3% dag, trailing, Best-Day-regel straft juist grote winstdagen van positief-scheve profielen; Q1b bevestigt vereiste SR > 4).
- **Fee-aanname mogelijk fout:** secundaire bronnen noemen FTMO-accountgroottes 10k–200k (geen 80k) en ≈ €540 voor 100k 2-Step. Onze sims gebruiken €540 voor €80k → kan te hoog/laag zijn; Manager/Sandro verifiëren op ftmo.com.
- Futures-props (Topstep: 90%, weekly payouts, trailing HWM-drawdown; Apex: 100% eerste $25k dan 90%, EOD-trailing; alleen CME-futures): zelfde index-intraday-strategie, exchange-data/geen CFD-swap, maar trailing drawdown is strenger dan statisch. Niet doorgerekend; voorstel: Q1b-simulatie met trailing-DD als gratis analyse-taak (S0b).
- **Eigen kapitaal:** zonder first-passage-regels is de lat ≈ SR 0,9 bij 15% vol voor ≈ €1.000/mnd op €80k (SR × vol × kapitaal), maar met DD 15–25% en zonder fee/split. FTMO's regels verhogen de vereiste SR voor negatief-scheef profiel naar 3–4 (R3) — voor positief-scheef ≈ 1. Dus: het profiel bepaalt of FTMO überhaupt zin heeft; bij SR < 0,7 is FTMO niet beter dan eigen geld. Of €80k eigen kapitaal bestaat/gewenst is: Sandro.

## 6. Nu bij Manager/Uitvoerder neerleggen
Actief bij Manager/Uitvoerder (v14): S0, S1, S2, S3 (S3 wacht op Sandro-data; M-001). Volgorde: S0 (gratis, nu) → S2 (data aanwezig, direct) → S1 (M5 aanwezig) → S3 zodra Sandro data kiest. S4–S8 in reserve (≥ 3 klaar: S1, S2, S3 + S0).
