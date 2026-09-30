# DOEL v2 (Sandro, 30-09 — bindend, boven alles)
**Echt eigen kapitaal ≈ €80k** (geen FTMO-verplichting). Ambitie ≈ **€800–900/mnd**; **€400–500/mnd (≈ 6–7,5%/jr) is óók goed** mits: robuuste edge, **vele jaren teruggetest (streef ≥ 20 jr)**, weinig tot geen datagaten, realistische kosten. FTMO blijft hooguit een extra route, geen selectiecriterium meer. Consequentie voor richting: **laagfrequent, gediversifieerd, multi-asset, vol-getarget** (trend + carry + momentum + seizoen …) weegt zwaarder dan intraday-FTMO-specifiek werk (ORB/S3 loopt door maar is niet meer het hoofdspoor). Benodigd: netto SR ≈ 0,6–0,7 bij ≈ 10% vol (of SR 0,5 bij 15% vol met DD ≈ 25%). Elke kandidaat moet bovendien **beter zijn dan buy-and-hold** op risico (DD/SR), niet alleen positief rendement (7%/jr kan ook uit aandelenbeta komen, met DD 30–50%).

# PROGRAMMA FASE 2 — grote veranderingen in team en methode (CEO, 2026-09-30) — horizon: maanden

## Diagnose (waarom fase 1 vastliep)
1. **Te weinig data:** 5,7 jaar intraday → elk effect is 1–2 regimes; ORB-t is na correctie 1,81. Bewijs is structureel te zwak, ongeacht hoeveel ideeën we proberen.
2. **Zoekstrategie = één idee per keer, weggooien na één test** (~415 keer). Geen catalogus, geen gecontroleerde multiple-testing over de hele zoekruimte, geen hergebruik van het werk.
3. **Te veel focus op één klasse** (intraday indices/ORB) waar kosten de muur zijn; nauwelijks laagfrequente, diversifiërende sleeves met decennia bewijs.
4. **Eén Uitvoerder-thread** doet data, onderzoek en forward; data-werk wordt door onderzoek verdrongen ("wachten op data").

## Verandering 1 — Data-programma (werkstroom D; downloaden zelf kost dagen, niet maanden — het onderzoek erop loopt maanden)
NB (CEO-correctie 30-09): rekensom bij 1 verzoek/8 s ≈ 450 verzoeken/uur → 4 instrumenten × 9 jaar ≈ 20 u; 15 instrumenten ≈ 3 dagen — mits de feed stabiel blijft (nu traag/instabiel). "Maanden" gold voor het programma, niet voor het downloaden.
- **D1 Intraday-lake via Dukascopy-feed** (huidige P0-methode: eerlijke UA, 1 verzoek/8 s, back-off, hervatbaar; **niets omzeilen**). Uitbreiden van 4 naar een prioriteitenlijst: US500, GER40, US100, XAUUSD, EURUSD, GBPUSD, USDJPY, AUDUSD, USDCAD, USDCHF, US30, USOIL, XAGUSD, … ; volgorde en voortgang in `data/DATA_CATALOGUS.md` (symbool, jaren, gaten, checksum, QA). Draait continu; onderzoek gebruikt wat er ligt.
- **D2 Lange dagdata (gratis, geautomatiseerd, toegestaan):** FRED (FX, rente, olie, goud-proxy's), Yahoo/stooq-daghistorie (indices, sectoren, ETF's, grondstof-futures-proxy's) — **20–50 jaar** waar beschikbaar; alleen binnen de gebruiksvoorwaarden, met rate-limiet. Basis voor laagfrequente sleeves (trend, carry, momentum, seizoen, value-proxy's).
- **D3 Data-QA:** elk bestand: gaten, splits/DST, spread-aanname, vergelijking met FTMO-overlap (zoals S3-parsertest). Geen resultaat op ongecontroleerde data.

## Verandering 2 — Onderzoeksmethode (werkstroom R, Strateeg = eigenaar catalogus)
- **Catalogus i.p.v. losse ideeën:** `STRATEGIE_CATALOGUS.md`: 30–50 gepubliceerde/economisch onderbouwde regels (TSMOM/trend, cross-sectionele momentum over assets, carry FX/rente, seizoen/turn-of-month/pre-holiday, overnight vs intraday, mean-reversion op korte horizon, volatiliteitsrisicopremie-proxy's, breakout-varianten, sector-rotatie, …), elk met: mechanisme, verwachte bp vs kosten (S0), data-eis, horizon, scheefheid.
- **Eén gemeenschappelijke engine + kostenmodel** (S0-kosten per instrument/uur, swap) waarop elke catalogusregel identiek draait; geen ad-hoc scripts meer per idee.
- **Lange-data-eerst (goedkoop):** eerst testen op decennia dagdata (D2); alleen regels met economisch én statistisch bewijs (kosten-poort, meerdere regimes) gaan naar FTMO-data en MT5.
- **Multiple-testing over de hele catalogus** (FDR / White/SPA-achtig / DSR met echte trial-teller); vooraf vastgelegd; **reserve-OOS:** 2025-01→heden blijft onaangeraakt als laatste toets voor kandidaten, lange data (pre-2021) is de ontdekkingsset.
- **Portefeuille van kleine, ongecorreleerde edges:** het doel (SR ≈ 1 bij dagelijks-vlak profiel) is realistischer via 5–10 sleeves met SR 0,3–0,6 en lage correlatie dan via één grote edge. Meten: sleeve-correlatiematrix, vol-targeting, FTMO-dagdip-profiel (Q1b-mechaniek).
- **Nieuwe dimensies buiten "signaal nummer 400":** horizon (dag/week/maand met lage omloop → kosten verwaarloosbaar), tijdstip/sessie, instrumentklasse (FX-crosses, grondstoffen, obligatie-/rente-CFD's zover FTMO ze heeft), risico-mechaniek (sizing, stops, trailing), en combinatie van regimefilters — allemaal met vooraf vastgelegde regels.

## Verandering 3 — Team (parallel i.p.v. serieel)
- **Uitvoerder in 3 permanente werkstromen** (prioriteit door CEO/Manager, WIP-limiet 1 per stroom, tijdverdeling ≈ 30/50/20): **D** data (§1), **R** catalogus-onderzoek op lange data (§2), **F** forward/MT5-onderhoud. Bij S3-data: S3 preempt R.
- **Meer capaciteit:** Manager stelt binnen 1 cyclus voor of een tweede Uitvoerder-agent (cloud, alleen Python-onderzoek op data die in de repo/opslag staat) haalbaar is; anders werkstroom D als achtergrondproces en R/F op de bestaande agent. (Besluit CEO na voorstel.)
- **Strateeg** levert eerst `STRATEGIE_CATALOGUS.md` (v1 binnen 2 cycli), daarna per week 3–5 catalogusregels als gebundeld Voorstel met PREREG-sjabloon (één sjabloon, niet elke keer opnieuw).
- **Manager** levert binnen 2 cycli: (a) NEXT_STEPS v17 met de 3 werkstromen; (b) het sjabloon voor engine + trial-teller per catalogusregel; (c) een **weekrapport** (maandag) in `EINDVERSLAG.md`: voortgang per werkstroom, geteste catalogusregels, data-dekking, forward-stand. Geen stop-/bevriesvoorstellen meer.
- **Auditor:** starten zodra een regel de kosten-poort én lange-data-toets haalt (niet pas bij evaluatie).

## Mijlpalen (CEO bewaakt wekelijks, geen stopcriteria)
- **Week 1:** data-catalogus staat, D1 loopt voor ≥ 8 instrumenten, D2 ≥ 15 dagreeksen ≥ 20 jaar; engine + kostenmodel; catalogus v1 (≥ 30 regels).
- **Week 2–3:** eerste volledige catalogus-run op lange dagdata met FDR-controle; shortlist ≤ 5 kandidaten; S3 zodra SPX-data volledig.
- **Week 4–6:** shortlist op FTMO-data/reserve-OOS; sleeve-portefeuille en FTMO-mechaniek (Q1b); eerste forward-papier per kandidaat.
- **Daarna:** verdieping (meer instrumenten/horizons), Auditor, S10-kader (go/no-go blijft; aankoop is altijd Sandro's beslissing).
