# ALLOCATIE_V1 — implementeerbare allocatie-specificatie (Strateeg; D-078; v1 op 2026-09-30 19:40 Amsterdam)
**Dit is een specificatie en geen beleggingsadvies of aanbeveling.** Ze beschrijft wat het project heeft gebouwd en getest, wat het volgens de eigen vooraf vastgelegde regels waard lijkt, en wat er nog moet gebeuren vóór een echte stap. Een echte stap (rekening, geld, trades) is altijd een besluit van Sandro. **Status H1–H8 (S10b): H4 niet gehaald; geen go-advies.**

## 1. Wat de allocatie is (één alinea)
Een **risicogestuurde multi-asset-allocatie** (P-ETF-a): (i) een *all-weather-sleeve* (aandelen VS, 10-jaars Treasury, goud; gewicht ∝ 1/volatiliteit, totale vol-doel 8%, nooit hefboom) en (ii) een *aandelen-trendfilter* (Faber: 5 indices, 10-maands-gemiddelde, long of cash); beide sleeves gecombineerd met gewichten ∝ 1/σ(60 dagen), maandelijks herwogen, **ongehefeld**. Beloning = risicopremies + structuur (spreiding, vol-gewicht, DD-filter); **geen bewezen alfa** (run 5: nul-kalibratie p = 0,46; lange-historie-toets 1976–2024: risicopariteit SR 0,51 = 60/40 SR 0,51, maar halve maxDD 14% vs 29%).

## 2. Regels (exact in `PREREG_PORT.md`, `PREREG_CAT1/2.md`, `catalogus/C02_faber.py`, `C52_allweather.py`; hier samengevat)
| Onderdeel | Regel |
|---|---|
| **Sleeve A — all-weather (C52 'lang')** | activa: S&P 500, 10j-Treasury, goud; gewicht_i ∝ 1/σ_i(60 d); portefeuille geschaald met s = min(1; 8%/σ_P(60 d)); rest = cash; maandeinde |
| **Sleeve B — Faber (C02)** | voor elk van SPX, NDX, DJI, DAX, N225: long als maandslot > 10-maands-SMA, anders cash (kasrente); gelijk gewogen over de 5; maandeinde |
| **Combinatie (P-ETF-a)** | gewicht_sleeve ∝ 1/σ(60 d) van de sleeve-excessreeks, som = 1, **geen hefboom**; herweging **eerste handelsdag van de maand**, geen drempelregel |
| **Variant P-ETF-b (niet aanbevolen bij huidig excess)** | zelfde × k (vol-doel 10%, hefboom ≤ 2×, lening tegen rf + 1,5%) — onder premie-verwachting *lager* dan ongehefeld (VERWACHTING.md §3) |
| **Gemiddelde exposure (2001–24; 2021–24)** | aandelen 0,40 (0,45) · obligaties 0,29 (0,26) · goud 0,11 (0,13) · cash 0,20 (0,16) (QA D-075) |
| **DD-filter** | uitsluitend via Faber (sleeve B) en de vol-schaal (sleeve A); geen discretionaire ingrepen; backtest-maxDD 11,2% (2001–24), budget standaard ≤ 20% / p95 ≤ 25% (D-062) |

## 3. Uitvoering (UCITS/ETC; **alle TER/ISIN onbevestigd tot broker-check**; geen US-ETF's in EU-retail)
| Bouwsteen | UCITS-kandidaat (bron: web-claim) | TER |
|---|---|---|
| S&P 500 | iShares Core S&P 500 Acc (IE00B5BMR087) of Vanguard S&P 500 Acc (IE00BFMXXD54) ([JustETF](https://www.justetf.com/uk/asset-comparisons/etf-comparisons/IE00B5BMR087-ishares-core-sp500-acc-vs-IE00BFMXXD54-vanguard-sp500-acc)) | 0,07% |
| Nasdaq-100, Dow, DAX, Nikkei 225 | te identificeren (UCITS-trackers bestaan; ISIN/TER niet door mij geverifieerd) | ≈ 0,1–0,3%ᵉ |
| 10j-Treasury | UCITS Treasury 7–10j (USD of EUR-hedged) — te identificeren; TIPS-UCITS als variant: iShares $ TIPS EUR-H (IE00BDZVH966) 0,12%, Amundi US TIPS (LU1452600437) 0,13% ([extraETF](https://extraetf.com/etf-profile/LU1452600437)) | ≈ 0,07–0,13%ᵉ |
| Goud | fysiek goud-ETC (Invesco Physical Gold, TER 0,12%, [Invesco](https://invesco.com/ie/en/insights/why-invest-in-gold.html)); ISIN te identificeren | 0,12% |
| Cash | EUR-geldmarkt-UCITS (€STR-gerelateerd) of USD-variant (valuta-keuze!) | ≈ 0,10%ᵉ |
| Transactiekosten | NL-retail: vaste €3–3,75 per trade op Euronext ([Curvo](https://curvo.eu/nl/artikel/interactive-brokers-vs-degiro)); engine-gevoeligheid 13 bp rondreis | — |
**Niet nodig/uitgesloten:** futures, CFD's, hefboom, inverse-ETF's (C61 faalde), managed-futures-UCITS (geen historie), opties (VRP: alleen onderzoek).
**Jaarlijkse omloop/kosten:** nog niet uitgesplitst — *open aanvraag:* turnover en kosten per jaar uit `forward_portfolio.py`/`PORT_backtest` (Uitvoerder-1).

## 4. Verwachting (premie-gebaseerd; `VERWACHTING.md`, D-075, D-072)
| €80k, per maand | Laag | Midden | Hoog |
|---|---|---|---|
| **Alfa boven cash** (echte exposures) | −€34 | **€58** | €144 |
| + EUR-cash (€STR 2,44%) ≈ €163 = **totaal** | €128 | **€220** | €306 |
| (USD-cash 4,07%: valutakeuze, geen alfa) | €237 | €329 | €415 |
Kans op totaal ≥ €400: MC ≈ 0,4–13% afhankelijk van prior (5% gangbaar); na box 3 (≈ −€37, onbevestigd) lager. **Doel €400–500 niet in zicht** zonder hogere premies; stapeling van extra premies (PutWrite, factoren, regio) ≈ +€55/mnd (catalogus v2 §7), met extra staartrisico. **Backtest-cijfers (alfa €380/mnd; SR 0,94) zijn bull-premies (2001–24) en niet gebruiken als verwachting.**

## 5. Risico's en scenario's
- **2022-achtig** (rente ↑, aandelen én obligaties ↓): P-ETF-a −9,5% (C52 −13,6%, 60/40 −17,0%); RP 3-activa 1976–2024 −10,7% in 2022.
- **Regime-afhankelijkheid:** risicopariteit wint in rente-/inflatieschokken en aandelenbears (jaren 70, 2000s), verliest in aandelenbulls (jaren 80/90: SR 0,17/0,25 vs 60/40 0,39/0,94). Langere drawdownduur 1,8–2,5 jaar (rolling-3j-SR min ≈ 0).
- **Waardering:** CAPE ≈ 41; 10j-verwachtingen aandelen 3,9–5,9% nominaal (Vanguard) → lage aandelenpremie.
- **Goud:** ≈ 4.180 na sterke stijging; premie-verwachting ≈ 0 of negatief t.o.v. cash 4%.
- **Valuta:** USD-activa, EUR-rekening: onverdekt +6–8% FX-vol; verdekt kost renteverschil (≈ 1,6%/jr).
- **Uitvoering/model:** synthetische obligatie (D = 8), prijsindices zonder dividend voor sommige indices, 13 bp-gevoeligheid, niet-geverifieerde TER/ISIN, box 3 onbevestigd.
- **Overfitting-geschiedenis:** 441 trials in D2; sleeves na zien van ontdekkingsdata gekozen; reserve-OOS (1,75 jr, SR-SE ≈ 0,75) kan alleen grove tekenfouten vangen.

## 6. Bewijsstatus (S10b v2, D-070)
H1 structuur-robuustheid: cross-market DD-reductie 12/12 (filtermechanica, geen alfa); plateau ✔ (SMA 8/10/12, vol-venster 30/60/90); 1976–2024: SR = 60/40, DD ½ ✔ gedeeltelijk · H2 vs 60/40 én cash: DD beter, SR over 48 jr gelijk; vs cash: alfa ≈ €58/mnd midden → **afweging expliciet** · H3 reserve-run: morgen 12:00 (tekenfout-check) · **H4 premie-verwachting totaal ≥ €400: niet gehaald** · H5 uitvoerbaarheid: ETF-route ✔ (ISIN/TER te verifiëren) · H6 forward-papier: start 1-10 · H7 Auditor: nog niet gestart (pas bij kandidaat) · H8 gefaseerde start: advies aan Sandro.

## 7. Wat er moet gebeuren vóór een echte stap (Sandro beslist; niets hiervan is gedaan)
1. Sandro kiest **doel/tussendoel** en **DD-tolerantie** (nu standaard 20% / p95 25%) en of €80k eigen kapitaal dit doel dient (alternatief: cash/geldmarkt ≈ €163/mnd).
2. **Valuta- en cash-beleid** (EUR vs USD, verdekt/onverdekt).
3. **Broker-check** (kosten, toegang, TER/ISIN van elk ETF/ETC), **fiscalist** (box 3-effect, transactie-/werkelijk-rendement-regime).
4. Reserve-run-uitslag, ≥ 3 maanden forward-papier zonder alarm, **Auditor** (onafhankelijke herimplementatie), bij voorkeur ook de resultaten van run 7 (premies).
5. Vooraf vastgelegd **stop-/herzieningsregel voor de allocatie zelf** (alleen Sandro beslist), gefaseerde start (≤ 25% van kapitaal × 6 maanden).
## 8. Open (aan Uitvoerder-1/2)
Turnover/kosten per jaar; ISIN/TER-lijst na broker-check; EUR-perspectief van de hele specificatie (nu USD-backtest + ongehedged EUR-rij); reserve-uitslag; run 7 (C65–C68).
