# VEHICLE_ANALYSE v1 (Strateeg, werkstroom V, 2026-09-30 13:15 Amsterdam) — eigen kapitaal €80k, NL/EU
Status: **eerste versie (cyclus 1 van ≤ 3)**. Alles met bron is web-claim (D-034), niet geverifieerd bij broker/belastingdienst; kosten die ik uit eigen kennis noem zijn gemarkeerd (ᵉ = eigen kennis, onbevestigd). Geen fiscaal of beleggingsadvies; rekening openen en trades blijven bij Sandro.

## 1. Vehikels
| Vehikel | Wat | Kosten (bron) | Beperking |
|---|---|---|---|
| **UCITS-ETF's / ETC's** | aandelen-, goud-, obligatie-indices, volledig deelbaar | TER: S&P 500 (CSPX/VUAA) 0,07% ([JustETF-vergelijking](https://www.justetf.com/uk/asset-comparisons/etf-comparisons/IE00B5BMR087-ishares-core-sp500-acc-vs-IE00BFMXXD54-vanguard-sp500-acc)); fysiek goud ETC (Invesco) 0,12% ([Invesco](https://invesco.com/ie/en/insights/why-invest-in-gold.html)); EUR/USD-ultrashort-obligatie 0,09% ([iShares/Stuttgart](https://www.boerse-stuttgart.de/en/products/etps/etfs/stuttgart-fxplus/a1w375-ishares-euro-ultrashort-duration-bond-ucits-etf/)). Commissie IBKR Xetra 0,05%, min €1,25, max €29 ([IBKR Europe-overzicht](https://www.eupersonalfinance.eu/articles/interactive-brokers-review-europe)); spread ETF ≈ 1–5 bpᵉ | **US-ETF's zijn voor EU-retail niet beschikbaar (PRIIPs/KID)** ([JustETF](https://www.justetf.com/en/news/etf/us-domiciled-etfs.html)); geen short, geen hefboom; **beperkt universum** (geen FX, weinig grondstoffen behalve goud/ETC's, geen carry) |
| **Futures (micro)** | MES/MNQ/MGCᵉ via IBKR | MES ≈ $1,14 rondreis per contract volgens gebruikers ([forum](https://forums.aeromir.com/threads/interactive-brokers-micro-s-p-e-mini-futures-mes-commissions.2188/post-9839)), initiële margin ≈ 5% van notional ([NinjaTrader FAQ](https://ninjatrader.com/futures/futures-contracts/micro-emini/micro-e-mini-futures-faqs/)); roll per kwartaalᵉ; **financiering zit in de future-prijs** (basis/cost of carry) i.p.v. swap | **Granulariteit:** notional per contract uit onze prijzen (swap_specs): US500 ≈ 7.689 × $5ᵉ ≈ $38k, US100 ≈ 30.383 × $2ᵉ ≈ $61k, goud ≈ 4.156 × 10 ozᵉ ≈ $42k → bij €80k is 1 contract ≈ 40–75% van het kapitaal; een gediversifieerd 20-instrumenten-Carver-portfolio is **niet uitvoerbaar** (Carver lost dit op met dynamische optimalisatie/weinig instrumenten — zie WEB_LEERLOG). Toegang tot CME-futures voor NL-retail via IBKR: niet door mij geverifieerd |
| **CFD's** | elke index/FX/metaal, deelbaar, long én short | spread/commissie zoals S0 (FTMO-niveau; retail-CFD-spreads van een EU-broker kunnen hoger zijn, niet gemeten); **financiering ≈ benchmark ± 1,5%, min. 20% margin** (CEO-log, IBKR-documentatie) — dus long ≈ benchmark + 1,5%, short ontvangt ≈ benchmark − 1,5%; hefboomlimiet retail (ESMA 1:20 indices, 1:30 FX majors)ᵉ | financiering bij long hoog t.o.v. ETF-TER (≈ 3–6%/jrᵉ vs 0,07%); negatieve saldi beschermd; geen dividend-ontvangst maar aanpassing |

## 2. Wat dit betekent voor de catalogus (engine-parameters per vehikel)
| Parameter | UCITS-ETF | Micro-future | CFD |
|---|---|---|---|
| rondreis (bp) | 0,05% comm (min €1,25) + spread 1–5ᵉ | ≈ 0,3–1ᵉ (vast $1,14 op ≈ $40k notional ≈ 0,3 bp + spread 1 tick) | S0 (indices 0,45–0,78; FX 0,6–1,2; XAU 0,83) of hoger bij retail |
| lopende kost | TER 0,07–0,12%/jr | roll + impliciete financiering (≈ benchmark) | benchmark ± 1,5% op notional |
| short mogelijk | nee | ja | ja |
| deelbaarheid | volledig | grof (1 contract ≈ 40–75% kapitaal) | volledig |
| valuta | USD-expositie tenzij hedged-klasse | USD | per instrument, EUR-rekening → conversie 0,03–0,1%ᵉ |
**Consequentie (nieuw ten opzichte van FTMO-kostenmodel):** de swap-asymmetrie (long 5–8%/jr, short ≈ 0–3%) geldt voor FTMO-CFD's, **niet** voor ETF's. Voor eigen kapitaal is de *long-only* trend/dual-momentum-klasse dus veel goedkoper via UCITS-ETF's (TER 0,07–0,12%) dan via CFD's — maar beperkt tot wat UCITS heeft (aandelenregio's, sectoren, goud, obligaties, geldmarkt). FX-carry/trend, olie, koper en shorts vragen CFD's of futures. **De engine krijgt daarom een `vehicle`-parameter; elke catalogusregel wordt per vehikel gerapporteerd.**

## 3. Data-gaten per vehikel
- ETF's: UCITS-historie begint ≈ 2009–2012 (CSPX 2010ᵉ) → voor 20+ jr valt men terug op de onderliggende indexreeksen/US-ETF-proxy's (SPY/GLD/TLT in `data/daily`) plus TER/kosten → **rapporteer proxy + kostenmodel, geen echte ETF-historie**. Prijsindex vs total return: ETF (acc) heeft dividend herbelegd; Yahoo-`adjclose` gebruiken voor ETF-vehikel, `close` voor CFD/future.
- Futures: doorlopende reeksen (GC=F e.d.) hebben rolgaten (`D2`-QA: rolsprongen); echte roll-kosten niet meetbaar uit Yahoo.
- CFD: alleen 5,7 jr echte spreads (S0).

## 4. Box 3 (alleen benoemen; onzeker; geen advies)
- 2026: forfaitair rendement **overige bezittingen 6,00%** (definitief), tarief **36%**, heffingsvrij vermogen **€59.357 per persoon** ([SRA](https://www.sra.nl/nieuws/259001/2026/01/box-3-percentages-vrijstellingen-en-bedragen-2026), [rendement.nl](https://www.rendement.nl/inkomen-uit-sparen-en-beleggen/nieuws/box-3-tarief-blijft-36-in-2026.html)).
- Indicatieve rekenregel (aanname: €80k volledig 'overige bezittingen', geen schulden, geen fiscaal partner, geen tegenbewijs): (80.000 − 59.357) × 6% × 36% ≈ **€446/jaar ≈ €37/mnd**, onafhankelijk van het werkelijke rendement. Met fiscaal partner verdubbelt de vrijstelling (→ ≈ €0). **Gevolg voor het doel:** het netto-doel €400–500/mnd is grotendeels bruto-doel; box-3-drag is hier klein (≈ 0,56% van het kapitaal) maar **vast** — ook in verliesjaren.
- **Niet geverifieerd:** hoe een overgang naar belasting op werkelijk rendement (wetgeving in voorbereiding, ingangsdatum niet door mij bevestigd), tegenbewijsregeling, schulden/margin-effect en of actief handelen als 'resultaat uit overige werkzaamheden' wordt gezien. Dit moet Sandro met een fiscalist/Belastingdienst nagaan vóór echt geld.

## 5. Open punten (volgende cycli ≤ 2)
(1) Retail-CFD-spread/financiering van een EU-broker echt opzoeken (IBKR/anderen) i.p.v. FTMO-S0; (2) CME-toegang en micro-contractspecs bij IBKR verifiëren (multiplier, margin, commissie); (3) UCITS-universumlijst (aandelen regio's, sectoren, goud, obligatie-duur, geldmarkt) met TER + ISIN → `engine/vehicles.csv`; (4) valuta-hedge-kosten; (5) `engine`-parameters formeel aan Uitvoerder/Manager doorgeven.
