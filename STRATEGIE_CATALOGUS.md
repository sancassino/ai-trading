# STRATEGIE_CATALOGUS v2 — premies (Strateeg, 2026-09-30 19:00 Amsterdam; v1.2 16:05; v1.1 13:20; v1 12:45) — Fase 2, werkstroom R

Doel: 50 economisch onderbouwde regels op **één** engine/kostenmodel, getest op **lange dagdata eerst** (ontdekkingsset ≤ 2024-12), met FDR over de hele catalogus en reserve-OOS 2025-01→heden (alleen voor shortlist, één keer). Elke regel = 1 trial (+ ≤ 2 vooraf genoemde varianten). Mijn verwachtingen zijn **literatuur-ordegroottes uit geheugen, niet geverifieerd**; alleen de kostenkolom is uit de repo (S0, swap-specs).

## 0. Wat de kosten voor de catalogus betekenen (nieuw inzicht)
- **Financiering is de dominante kost voor meerdaagse posities, en asymmetrisch:** long index/aandeel/goud kost 1,4–2,4 bp/nacht (**5–8% per jaar**), short 0–0,8 bp/nacht (≈ 0–3%/jr; US30/UK100-short ontvangt zelfs). FX-swap is het renteverschil: long hoge-rente-valuta ontvangt, USDJPY long +0,4, USDCHF short −2,2 bp/nacht. Olie-specs onbetrouwbaar (niet gebruiken).
- Gevolg (*swap-gecorrigeerde netto verwachting* = bruto − swap × dagen-lang): **long-only index-beta-sleeves verliezen 5–8%/jr aan swap** — alleen regels met een edge ≫ 5%/jr of met korte houdduur overleven. **Kort/long-short, FX (swap = carry), en intraday-vlak** zijn structureel goedkoper. Catalogusprioriteit volgt dit.
- Omloop-kosten: rondreis 0,45–0,8 bp (indices), 0,6–1,2 (FX-majors), 0,83 (XAU), 2,9 (aandelen). Bij maandelijkse omloop ≈ 0,1–0,2%/jr → verwaarloosbaar; bij dagelijkse omloop 1–2%/jr.
- **Yahoo/ETF-dagdata heeft geen CFD-kosten**: de engine moet S0-spread + FTMO-swap per nacht los toepassen (en dividenden negeren: cash-CFD's zijn prijsindex; GER40 is performance-index).

## 1. Catalogus (status: N = nieuw, T = al getest in de 414 trials — dan **niet opnieuw**, alleen hergebruik als referentie; prio 1 = eerst)
Kolommen: ID · regel (exact, één keer vast) · mechanisme (wie betaalt ons) · horizon/omloop · data (lange bron) · bruto-verwachting (literatuur, grof) vs kosten · scheef/dagelijks-vlak · status/prio.

### A. Trend / tijdreeksmomentum (positief scheef, lage omloop)
| ID | Regel | Mechanisme | Horizon | Data | Bruto vs kosten | Scheef/vlak | Status |
|---|---|---|---|---|---|---|---|
| C01 | TSMOM 12m: lang als 12m-rendement > 0, kort anders; gewicht 10%/σ60; maandelijks; ≤ 12 assets (FX-majors, goud, zilver, US500, US100, GER40, JP225) | onder-reactie + hedgers betalen risicopremie (Moskowitz–Ooi–Pedersen 2012) | maand | Yahoo/FRED 1970–; FX FRED noon | SR 0,3–0,6 multi-asset; kosten ≈ 0,2%/jr + swap (long index 5–8%!) | + / nee | **N, prio 1** (eerder alleen op FTMO-set/5,7 jr en Yahoo-trendgrid, niet als vaste multi-asset-regel op decennia) |
| C02 | SMA-10-maanden (Faber) long/cash op indices; cash = geen positie | zelfde; DD-beperking | maand | Yahoo 1990– | lage SR-winst maar DD ↓ | + | N, prio 2 (swap-drag long!) |
| C03 | Donchian 55/20 D1, ATR-stop 2×, 8 FX+goud | breakout-trend, Turtle | dagen–weken | FRED FX 1971–, Yahoo goud | R4 (H4) negatief; D1 lange reeks ontbreekt | + / nee | N, prio 2 |
| C04 | EMA 50/200 cross (FX, goud) | trend | weken | idem | SR ≈ 0,2–0,4 | + | N, prio 3 |
| C05 | Mix TSMOM 1/3/12m gelijk gewogen (Hurst–Ooi–Pedersen) | idem, diversificatie in tijd | maand | idem | iets beter dan C01 | + | N, prio 2 (vervangt varianten van C01) |
| C06 | Trend-sterkte-gewicht (t-stat van 60d-regressie) i.p.v. teken | idem | maand | idem | ≈ C01 | + | N, prio 4 |

### B. Cross-sectioneel (markt-neutraal waar financiering het toelaat)
| ID | Regel | Mechanisme | Horizon | Data | Bruto vs kosten | Status |
|---|---|---|---|---|---|---|
| C07 | Asset-class momentum: lang top-3 / kort bottom-3 van 12 markten op 12-1m | relatieve trend (Asness–Moskowitz–Pedersen) | maand | als C01 | SR 0,3–0,5 | N, prio 2 |
| C08 | Industry/sector-ETF momentum 12-1, lang top-3 (Yahoo sector-ETF's) | industrie-lead-lag (Moskowitz–Grinblatt) | maand | Yahoo 1998– | long-only → swap-drag | N, prio 4 (FTMO heeft geen sector-ETF's → bewijsreeks, niet verhandelbaar) |
| C09 | Kortetermijn-omkeer weekly (1w) op 12 markten, lang/kort | liquiditeitsverschaffing | week | Yahoo | verdwijnt na kosten (C3 dood) | T (dood) |
| C10 | Long-momentum rotatie top-N (16, T10) | — | maand | — | T (dood, B3/ronde 1) | T |

### C. Carry / value (FX is hier goedkoop: swap = carry)
| ID | Regel | Mechanisme | Horizon | Data | Bruto vs kosten | Status |
|---|---|---|---|---|---|---|
| C11 | FX-carry G10: lang top-3 rente / kort bottom-3 (3m-rentes uit FRED IR3TIB…), maand | compensatie voor crash-risico (Lustig–Roussanov–Verdelhan) | maand | FRED 1990– (FX + rentes aanwezig in data/fred) | SR 0,3–0,5 voor 2008; negatieve scheefheid! | **T ("FX-carry" dood in samenvatting), niet herhalen**; wel *staart-gecorrigeerde* C12 |
| C12 | Carry + trend-filter: alleen carry-positie als 3m-momentum dezelfde kant op | filtert crash-dagen | maand | idem | verbetert skew | N, prio 2 |
| C13 | FX-value: 5j reële wisselkoers (FRED CPI + koers) lang ondergewaardeerd | PPP-mean-reversion | kwartaal | FRED | laag SR ≈ 0,2–0,3; ≈ 0 kosten | N, prio 3 |
| C14 | Index-waardering: long US500 als earnings-yield − 10j-rente > mediaan | risicopremie-timing | kwartaal | FRED 10y, Shiller (licentie controleren) | laag, swap-drag | N, prio 4 |
| C15 | Goud vs reële rente | — | maand | FRED | T (dood D2) | T |

### D. Seizoen / kalender (lage omloop, bekend gepubliceerd → verval waarschijnlijk)
| ID | Regel | Status |
|---|---|---|
| C16 | Halloween: long indices nov–apr, anders flat (Bouman–Jacobsen) | N, prio 3 (swap-drag 6 mnd ≈ 3%) |
| C17 | FOMC-cyclus: long index in even weken (Cieslak–Morse–Vissing-Jorgensen), `fomc_dates_1994_2020.txt` aanwezig | N, prio 2 (mechanisme: Fed-informatiestroom; gepubliceerd 2019) |
| C18 | Turn-of-month | T (dood B2d) |
| C19 | Pre-holiday | T (dood H2) |
| C20 | Maandeinde-herbalancering | T (dood H1) |
| C21 | Pre-FOMC drift | T (verdwenen sinds 2012) |
| C22 | Dag-van-de-week / overnight-intraday-splitsing | T (overnight −3,49) |
| C23 | Optie-expiratieweek | N, prio 4, N te klein per jaar |
| C24 | Earnings-announcement-premium: long aandeel 5 dagen vóór earnings (Frazzini–Lamont / Savor–Wilson) | N, prio 3 — `earnings.csv` alleen 2020–26; lange data via Yahoo onbetrouwbaar; swap 2,3 bp × 5 nachten + 2,9 bp |

### E. Mean-reversion op korte horizon
| ID | Regel | Status |
|---|---|---|
| C25 | RSI(2) < 10 boven SMA200 (index, meerdaags) | T (kern, SR 0,5; neg. scheef) |
| C26 | IBS < 0,2 | T (dood) |
| C27 | Double 7s | T (dood) |
| C28 | 3-daagse lage-koers-omkeer (Connors) | N, prio 4 (zelfde familie, lage toegevoegde waarde) |
| C29 | Z-score 20d Bollinger-omkeer op FX-crosses, 5 d hold | N, prio 3 (FX-kosten laag; FX mean-reverteert in range-regimes) |
| C30 | Pairs/stat-arb | T (dood) |
| C31 | VIX-spike-omkeer (koop index bij VIX-sluit > 30 en > 2σ) | N, prio 4 (H3 RSI(2)+VIX zegt: geen meerwaarde) |

### F. Volatiliteit / risico
| ID | Regel | Status |
|---|---|---|
| C32 | Vol-targeting (Moreira–Muir) | T (dood C6) |
| C33 | Trend alleen in laag-vol-regime (vol < eigen mediaan) | N, prio 3 (regime-filter op C01/C03) |
| C34 | Korte vol-risicopremie (short-vol proxies) | **niet verhandelbaar bij FTMO; negatief scheef — uitgesloten** |

### G. Intraday (alle reeds gedaan; ter referentie voor FDR)
C35 ORB (T, dag-t 1,81), C36 noise-area (T), C37 laatste-30-min (T dood), C38 gap-reversal/-continuatie (T dood), C39 London-open ORB (T dood, kostenpoort), C40 intraday-omkeer H1 (T dood), C41 stocks-in-play (T stop), C42 ML LightGBM (T dood).

### H. Cross-asset signalen (verhandeld via indices/goud/FX die FTMO wel heeft)
| ID | Regel | Mechanisme | Data | Status |
|---|---|---|---|---|
| C43 | Rente-signaal: 10j-rente-verandering 3m → aandelen-index long/short | discontovoet | FRED DGS10 | N, prio 3 |
| C44 | Credit-signaal: HYG/IEF-ratio 3m-trend → index long/flat | kredietspread leidt aandelen | Yahoo HYG/IEF (2007–) | N, prio 3 |
| C45 | Yield-curve-regime (T10Y2Y > 0) als filter voor indexbeta | recessierisico | FRED 1976– | N, prio 3 |
| C46 | Koper/goud-ratio-trend → index | groeiverwachting | Yahoo HG=F/GC=F | N, prio 4 |
| C47 | USD-trend → goud/FX-positionering | dollarcyclus | FRED DTWEXBGS | N, prio 4 |
| C48 | Risicopariteit | T (dood D4) |

### I. Sizing/portefeuille-mechaniek (geen signalen; hoort bij de sleeve-portefeuille)
C49 equal-risk over sleeves met rollende 60d-correlatie; C50 drawdown-gedreven schaal (−0,5× na −3% sleeve-DD, FTMO-dagdip-bewust) — **alleen als portefeuille-laag, geteld niet als trial per sleeve**.

## 2. Totaal en prioriteit
**Nieuw te testen (N): 24 signalen + 2 portefeuille-regels (C49–50); al getest/dood (T): 24** — niet herhalen; tellen mee in het FDR-universum. **Prio 1–2 (7): C01, C02, C03, C05, C07, C12, C17**; prio 3: C04, C13, C16, C24, C29, C33, C43, C44, C45; prio 4: rest.
**Bewust klein:** ≤ 7 regels in run 1 (prio 1–2), anders vreet FDR het vermogen op. Verwacht eerlijk: 0–2 overleven de lange dagdata; dan pas FTMO-data + reserve-OOS.

## 3. Eén PREREG-sjabloon (voor Manager/Uitvoerder, elke catalogusregel)
1. ID + regel (exact, inclusief aantal vrije parameters = 0; maximaal 2 vooraf genoemde varianten).
2. Universum vooraf (niet op resultaat); bron + periode; ontdekkingsset ≤ 2024-12, reserve-OOS 2025-01→ **pas na shortlist, één blik**.
3. Kosten: S0-spread per uur/instrument + FTMO-swap per nacht long/short (bp), geen dividend; rapporteer bruto én netto.
4. Poort vóór trial: gemiddelde bruto ≥ 3× kosten **op maandbasis netto-omloop**; anders stop zonder trial-telling.
5. Statistiek: dag-/maandgeclusterde t (Newey–West 5/12), blok-bootstrap-SR, per regime (vol-tercielen, pre-/post-2010, pre-/post-2020), halveringen; DSR met TRIAL_COUNT.
6. Beslisregel: FDR (Benjamini–Hochberg, q = 10%) over de catalogusrun; shortlist ≤ 5; per regel SR_netto ≥ 0,3, ≥ 60% van de 5-jaars-vensters > 0, beide helften > 0.
7. Uitvoer: SR, scheefheid, max dagdip (FTMO-definitie), sleeve-correlatie, swap-aandeel in de kosten.
8. Verwachte uitkomst en falen (1 alinea).

## 4. Toevoeging v1.1 (D-032, Doel v2 = eigen kapitaal) — klassen die bij eigen kapitaal passen; benchmark-eis vs buy-and-hold (SR **en** maxDD)
| ID | Regel (vast) | Mechanisme | Horizon | Data + licentie | Bruto vs kosten | Status |
|---|---|---|---|---|---|---|
| C51 | Vol-managed index: gewicht = min(1; 10%/σ21) op SPX/NDX/DAX (geen hefboom boven 1) | lage vol → hoger rendement per risico (Moreira–Muir); **C06/C32 was dood onder FTMO-kosten, niet onder ETF-kosten** | maand | Yahoo dagdata (D2, eerlijke UA; voorwaarden Yahoo: persoonlijk gebruik — controle door Manager) | ETF-TER 0,07%/jr; ΔSR +0,0–0,15 verwacht; vooral DD ↓ | **N, prio 1 (eigen kapitaal)** — heropent C32 met ETF-kostenmodel, geen nieuwe data-trial op FTMO |
| C52 | All-weather/risicopariteit: aandelen, obligaties (TLT/IEF), goud, grondstoffen; gewicht ∝ 1/σ60, vol-target 8% | diversificatie over groeiregimes | maand | D2 (TLT 2002–, TNX/IRX rente → obligatieproxy langer), FRED | UCITS-implementeerbaar; D4 dood zonder obligaties → herdoen mét obligaties | N, prio 2 (let op: 2022 = gelijktijdig aandelen+obligaties ↓) |
| C53 | Dual momentum (Antonacci GEM): elke maand: als US-aandelen 12m > geldmarkt → beste van US/wereld-aandelen, anders obligaties | absolute + relatieve momentum | maand | SPX/EFA-proxy (EWJ/EFA 2001–), IRX voor cash | TER; weinig trades (≈ 1–2/jr) | N, prio 2 |
| C54 | Carver-stijl forecast-combinatie: EWMAC(8,32),(16,64),(32,128),(64,256) + carry-forecast (FX/rente) per instrument, forecast-cap ±20, vol-target 10%, ≥ 20 instrumenten (indices, FX, goud, zilver, olie, koper, rentes) | trend + carry over veel markten; diversificatie is de hefboom (WEB_LEERLOG) | dag–week | D2 + FRED (licentie: FRED vrij, Yahoo voorwaarden) | futures/CFD-implementatie; granulariteit (VEHICLE §1) | N, prio 1–2 (vervangt losse C01/C03/C05 in portefeuillevorm; C01/C05 blijven als enkelvoudige referentie) |
| C55 | Defensive asset allocation (Keller): canary-assets (EEM, AGG-proxy) momentum → risico-aan/uit-verdeling | breadth-momentum als crash-filter | maand | D2 (EEM/ETF's) | TER | N, prio 3 |
| C56 | Seizoen-gecorrigeerde 'cash-parkeerrente': ongebruikt kapitaal in geldmarkt (IRX-proxy) | rentebaten op reserve | — | IRX/FRED | −TER | portefeuille-mechaniek, geen trial |
**Data-licenties (D-030.6):** FRED — vrij gebruik met bronvermelding (algemene FRED-voorwaarden; per serie kan een derde partij copyright hebben, bv. sommige OECD/ICE-reeksen → controleren per serie); Yahoo — chart-API zonder officiële licentie, voorwaarden beperken tot persoonlijk gebruik, geen herdistributie → **niet in publieke repo herpubliceren**, nu wel in privé-repo (Manager beoordeelt); Shiller (C14) — vrij beschikbaar op Yale-site voor onderzoek (ik heb de licentietekst niet gelezen) → C14 alleen na controle; Dukascopy-feed — geen robots-verbod maar voorwaarden onbekend (Uitvoerder-analyse D-018). **Niets wordt gescrapet buiten wat een voorwaarde toestaat.**
**Herprioritering run 1 (eigen kapitaal, 8 regels):** C01, C05, C07, C12, C51, C53, C54 (+ C03 als vergelijking; C02 en C17 schuiven naar run 2). Elke regel gerapporteerd per vehikel (ETF/future/CFD, zie `VEHICLE_ANALYSE.md`) en vs buy-and-hold (SPX/60-40) op SR en maxDD.

## 5. Toevoeging v1.2 (D-058) — DIVERSIFIERENDE sleeves (doel: correlatie < 0,3 met C02/C52/aandelenbeta) + uitvoerbaarheid bij €80k
**Screen (vooraf, geldt voor alle v1.2-sleeves):** (i) corr met C02, C52 lang en SPX-excess ≤ 0,3 op de ontdekkingsset; (ii) marginale bijdrage aan P-ETF-a: ΔSR en ΔmaxDD bij gelijk risicobudget (geen nieuwe trial, vehikelrapport); (iii) uitvoerbaar als UCITS/ETC (of micro-FX-future) met verifieerbare kosten; (iv) ≥ 20 jr data of expliciet 'korte reeks'-label. **Verwachting (eerlijk):** echte diversifiers zijn schaars en hebben SR 0,3–0,5; ze verbeteren P-ETF-a hooguit ΔSR +0,05–0,15.
| ID | Regel (vast) | Waarom diversifiërend | Vehikel + kosten (web-claim/aanname) | Data | Prior |
|---|---|---|---|---|---|
| C57 | **Faber-GTAA:** 10-mnd-SMA long/cash op 5 klassen: aandelen VS, aandelen wereld ex-VS, obligatie 10j, grondstoffen, goud (REIT alleen als proxy ≥ 20 jr) | obligatie-/grondstof-/goudpoot met eigen trend; beta naar aandelen alleen in 1/5 | UCITS: Invesco Bloomberg Commodity TER 0,19% ([extraETF](https://extraetf.com/etf-profile/IE00BD6FTQ80)), goud ETC 0,12%, aandelen 0,07–0,20%; 13 bp rondreis | D2: SPX, EFA-proxy (EWJ/EWG/EWU + N225/FTSE/DAX), TNX/TLT, DBC (2006→; commodity-proxy langer: COPPER/WTI/GOLD_F 2000→), GOLD_F | corr met C02 ≈ 0,5–0,6 (deels dezelfde Faber-logica), SR 0,4–0,6 |
| C58 | **Goud-trend:** long goud-ETC als koers > 10-mnd-SMA, anders cash | goud ≈ 0–0,2 corr met aandelen | ETC TER 0,12%; geen swap | GOLD_F 2000→ (24 jr, **regime: 2001–11-bull**), langere goudreeks ontbreekt (data-gat; bron/licentie zoeken, niet scrapen) | SR 0,3–0,5; regime-risico hoog |
| C59 | **Grondstoffen-trend:** Bloomberg-Commodity-UCITS long/cash op 10-mnd-SMA | corr 0,3–0,5 met aandelen, lage met obligaties | TER 0,19% (hedged 0,24%); contango zit in index | DBC (2006→), GSG; CRB-proxy langer (geen bron) | SR 0,2–0,4 |
| C60 | **Obligatie-duurtiming:** lange Treasury (UCITS EUR-hedged of USD) long als 10-mnd-SMA > 0, anders korte geldmarkt | corr ≈ −0,2…+0,3 met aandelen | TIPS/treasury-UCITS TER ≈ 0,12–0,13% ([extraETF](https://extraetf.com/etf-profile/LU1452600437)) | TNX_10Y 1962→ (synthetisch, D≈8) — **test expliciet op 1970–2000 (stijgende rente)** | SR 0,2–0,4; 2022 pijnlijk |
| C61 | **Long/short-trend op aandelen via UCITS-inverse-ETF:** long SPX boven SMA-10m, anders (a) cash of (b) −1× inverse-ETF | (b) verdient in bearmarkten (2000–02, 2008) → lagere corr met C02 in DD's | Xtrackers S&P 500 Inverse Daily Swap UCITS TER **0,50%** ([etfstream/finanzen](https://www.finanzen.net/etf/xtrackers-sp-500-inverse-daily-swap-etf-1c-lu0322251520)); **dagelijkse reset ⇒ engine moet −r_dag dagelijks compounden (volatiliteitsverval)**; 2× long TER 0,60% ([extraETF](https://extraetf.com/etf-profile/LU0411078552)) | SPX 1928→ | SR 0,3–0,5 (a)/(b); risico: fout in compounding ⇒ schijn-edge |
| C62 | **Regio-rotatie (C07, beperkt):** top-3 van 8 landen/regio 12-1 | ≈ aandelenbeta (corr 0,8+) | UCITS landenETF's TER 0,2–0,5% | EWJ/EWG/EWU/EEM 1996–2001→ | **geen diversifier**, alleen voor compleetheid; laag |
| C63 | **Factor-ETF's** (momentum/quality/low-vol) | long-only factoren zijn beta ≈ 1, geen diversifier; evidentie (Ken French-bibliotheek, vrij, citeren) geldt voor long-short | UCITS-factor-ETF's ≤ 12 jr historie | FF-factoren 1926/1963→ (licentie: onderzoek/citeren; niet geverifieerd) | **schrappen als sleeve**; alleen evidentie |
| C64 | **Managed-futures als gekocht fonds (watch-list):** iMGP DBi Managed Futures UCITS ETF (gelanceerd 13-05-2026, ≈ €480 mln) en BNP Paribas Easy Managed Futures UCITS (TER 0,60%, 29-05-2026) ([extraETF](https://extraetf.com/fr/etf-profile/LU3307218399)) | replicatie van CTA-index (SG CTA-achtig), corr met aandelen ≈ 0–0,3 | uitvoerbaar als ETF; **geen live-historie (< 5 mnd)** ⇒ niet toetsbaar | als *evidentie*: US-tegenhanger DBMF (Yahoo, 2019→) corr/SR opmeten (geen trial) | nu niets kopen/testen; forward-watch 12–24 mnd |
| C12 | FX-carry + trendfilter | — | **niet UCITS-uitvoerbaar**; micro-FX-futures alleen; CAT1 ≈ 0, cfd_retail dood | — | **schrappen** |
**Run 4 (mijn voorstel, prio):** C57, C60, C61, C58, C59 (vehikel-gerapporteerd; C61 met dagelijks-compounding-test) + C64-evidentie (DBMF-correlatie, geen trial) + het screen (i)–(iv). Verwachte uitkomst: 1–2 van de 5 passeren het diversifier-screen; C57/C60 het meest waarschijnlijk.

## 6. v2 — Premies verder dan de klassieke drie (D-074). Per premie: mechanisme · lange evidentie · verwachte *netto* excess na decay · capaciteit · uitvoerbaarheid €80k NL/EU · staart/DD
**Kader:** verwachtingen zijn *forward-looking na decay-haircut* (factorpremies verliezen ≈ 30% out-of-sample, [AQR 'Century of Evidence'-samenvatting](https://alphaarchitect.com/factor-investing-research-on-steroids/)), kosten meegerekend; cijfers zijn mijn schattingen op web-claims, geen bewijs. **Geen premie is hier een diversifier in de zin van corr < 0,3 met aandelen, behalve carry/roll in obligaties (die al in P-ETF-a zit).**
| # | Premie | Mechanisme | Lange evidentie (bron) | Verwachte netto excess, forward | Uitvoerbaar €80k NL/EU | Staart / DD |
|---|---|---|---|---|---|---|
| 1 | **Volatiliteitsrisicopremie** (implied − realized) | verzekeringsvraag naar puts; wie verkoopt krijgt premie | VIX/SPX 1990→ (D2): gem. implied 19,3% vs realized 15,1% (1990–2018, +4,2 pp); CBOE PUT-index juli 1986–2015: 10,1% vs 9,8% (S&P TR), vol 10,1 vs 15,3%, Sharpe 0,67 vs 0,47 (**bruto**); maxDD −33% vs −51% (2006–15) ([Cboe](https://www.cboe.com/insights/posts/white-paper-shows-volatility-risk-premium-facilitated-higher-risk-adjusted-returns-for-put-index/)) | PutWrite/covered-call = **aandelenbeta × 0,6–0,7 + VRP ≈ 1–2%/jr** na kosten; bij 1 beta-eenheid vervangen ΔSR ≈ +0,05…+0,15 (geen alfa-wonder) | UCITS covered call: JPM Nasdaq Equity Premium Income TER 0,35%, Global X S&P 500 Covered Call 0,45%, Infrastructure Capital 0,80% ([extraETF/InvestingInTheWeb](https://extraetf.com/ch/etf-profile/IE000SKTEI24)); WisdomTree CBOE S&P 500 PutWrite UCITS bestaat ([WisdomTree](https://wisdomtree.eu/en-gb/press-room/tabs/latest-news/wisdomtree-launches-cboe-s,-a-,p-500-putwrite-ucits-etf)) — TER/historie niet geverifieerd; eigen opties (XSP/Eurex) alleen na broker-check | **negatief scheef**: corr met aandelen in crises ≈ 1; DD-budget bindend; covered call kapt upside (yield 9–10% is deels teruggave van kapitaal); geen naakte short-vol-ETP's |
| 2 | **Factorpremies** (value, momentum, quality, min-vol, size) | gedrags-/risicopremies; long-short factoren niet belegbaar | Ken French-bibliotheek: VS-factoren maandelijks 1926→ (3-factor), momentum 1927→, 5-factor 1963→, dagelijks, internationaal ([datapagina](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html); **licentie: alleen 'Copyright Eugene F. Fama and Kenneth R. French' zichtbaar, geen gebruiksbeperking vermeld → citeren; gebruik als evidentie, geen herdistributie**); value-DD 2007–2020 ≈ −51% (diepste ooit) | long-only factortilt ≈ **+0,5…+1,5%/jr t.o.v. markt** na decay+TER, tracking error 3–5% ⇒ op 45% aandelen ≈ +0,2…+0,7% portefeuille (**≈ €13–45/mnd**) | UCITS: iShares Edge MSCI World Value/Momentum TER 0,25%, Quality 0,26% ([extraETF](https://extraetf.com/etf-profile/IE00BP3QZ825)); historie ≈ 10 jr → evidentie via FF-portefeuilles | factor-crashes (momentum 2009, value 2017–20); corr met markt ≈ 0,95 → **geen diversifier** |
| 3 | **Carry** (FX, obligatie roll-down/curve) | compensatie voor crash-/renterisico | FX: FRED/BIS/rentes (CAT1 ≈ 0 na kosten); curve: TNX vs IRX (10j 5,26% vs 3m 4,07% ⇒ +1,2%) | FX-carry long-only **niet UCITS-uitvoerbaar**; obligatiecarry zit al in de obligatiepoot; extra duration = meer renterisico (2022) | FX-micro-futures (M6E ≈ €12,5k) alleen als dynamisch carry+trend (C12 CAT1 ≈ 0) → **schrappen** (FX); obligatie: P-ETF-a bevat het al | FX-carry negatief scheef; rentestijging |
| 4 | **Grondstoffen-carry/-trend** | roll-rendement (backwardation) + trend | Pink Sheet = **spotprijzen**, géén termijncurve ⇒ **carry niet meetbaar**; trend C58/C59 faalden (SR 0,40/0,18) | UCITS Bloomberg Commodity TER 0,19% (roll zit in index) | **schrappen** (D-074 zelf: alleen bij termijncurves) | grondstof-DD hoog |
| 5 | **Landen-/regio-rotatie** (C07 op 15 D2b-markten) | relatieve momentum/waardering tussen markten | D2b (Yahoo-prijsindices, 1979→ afhankelijk van markt); Asness/Moskowitz/Pedersen-type evidentie | ≈ **0…+1%/jr** op aandelendeel (≈ €0–15/mnd); hoge omloop ⇒ kosten | UCITS landen-/regio-ETF's (TER 0,2–0,5%) | aandelenbeta (corr 0,8+) |
| 6 | **Waarderings-timing (CAPE)** | lage verwachting bij hoge waardering (mean reversion over 10 jr) | Shiller-data 1881→ (licentie nog te checken: Yale-site, citeren); **CAPE nu ≈ 41 (top 1%)** | als *allocatieregel* ≈ 0 alfa in 1–3 jr (timing-fout 1996–2000); **waarde = verwachting bijstellen (al gedaan in VERWACHTING.md)** | alleen als vooraf vastgelegde, traag bewegende aandelen-gewicht-multiplier (bv. 0,75–1,0) | vroeg-fout-risico; 14 onafhankelijke decennia ⇒ geen power |
| 7 | *(mijn toevoeging)* **Cash-/valuta-keuze** | rente-verschil USD (4,07%) vs EUR (2,44%) = 1,6%/jr ≈ **€108/mnd** op €80k | data/daily IRX_3M, €STR | **geen alfa maar FX-risico:** onverdekt USD-cash heeft EUR/USD-vol ≈ 7–8%; verwachting onder UIP ≈ 0 na valutaverlies → *geen* gratis €108 | USD-geldmarkt-UCITS bestaat (niet geverifieerd) | FX-staart; hedgen kost het renteverschil |
## 7. Stapelen van alles (mijn rekensom, netto, €80k, midden-scenario)
PutWrite i.p.v. 25% aandelenbeta ≈ **+€25/mnd** · factortilt op de aandelen ≈ **+€21** · regio-rotatie ≈ **+€9** · CAPE-regel ≈ **€0** · (FX-carry/commodity: geschrapt) ⇒ **≈ +€55/mnd** ⇒ midden-totaal ≈ €240 → **≈ €295** (EUR-cash), nog steeds < €400 en met extra staartrisico (VRP, factor-crashes). Hefboom helpt pas bij excess/eenheid > 1,5% (opslag). **Conclusie:** met de klassieke drie + deze zes komt het doel (€400–500) niet in zicht zonder hefboom/staartrisico buiten het DD-budget; de extra premies zijn elk ≈ €10–30/mnd.
## 8. Wat ik wél zou draaien (volgorde, één PREREG per premie, dezelfde gates + staarttest)
(a) **C65 Factor-evidentie (geen trial):** FF-factoren 1963→ en industry-portfolio's: decay per decennium, corr met markt, crisis-gedrag, premie na 30%-haircut. (b) **C66 VRP-proxy:** VIX vs realized vol 1990→ (D2: VIX, SPX): VRP-verdeling per regime/jaar, *geen* optie-P&L-claim uit VIX alleen; optie-indexreeksen (^PUT/^BXM via Yahoo, privé-repo) alleen met licentie-notitie; staarttest: worst-month, DD-duur, corr in crises; **vervolgens één regel:** 25% van aandelenbeta vervangen door PutWrite-proxy in P-ETF-a en ΔSR/ΔDD/ΔmaxDD rapporteren. (c) **C67 Landenrotatie C07** op 12 primaire D2b-markten (één trial). (d) **C68 CAPE-multiplier** pre-geregistreerd, decennia-test, verwacht ≈ 0. Verwachte uitkomst: 0–1 van 4 voegt iets toe buiten ruis.

## 9. FTMO-uitvoerbaarheidsherordening (v3, 2026-09-30 21:15 Amsterdam — D-086 FTMO-pivot)

**Koerscorrectie D-083:** maatstaf = FTMO-EV (niet SR of €/mnd boven cash); vehikel = `cfd` (FTMO-spread + commissie + swap, geen UCITS/ETF). Catalogus hieronder ingedeeld op uitvoerbaarheid binnen een FTMO-prop-account van €80k.

### 9a. FTMO-poortcriterium (geldt voor elke catalogusregel)
1. **Instrument aanwezig op FTMO** (SymbolList_FTMO.csv: indices, FX, goud/zilver/olie, aandelen-CFD, crypto)
2. **Kostenprofiel:** dagelijks-vlak (intraday-exit, swap = 0) **OF** bruto-carry > swap-kosten per nacht cfd (indices long 5–8%/jr → nauwelijks haalbaar, FX long hoge-rentecurrency = meevaller)
3. **Poort:** gemiddelde bruto ≥ 3× (spread+commissie intraday) of ≥ 3× (spread+commissie+swap overnight); anders stop zonder trial
4. **FTMO-mechanica:** 5%-dagverliesregel op floating equity; positief-scheef profiel overschrijdt grens zelden; negatief-scheef (VRP-achtig) risico op dagruin is hoog
5. **D-092.1 (bindend):** kost-pre-screen op train 2021–2023 (mean bruto ≥ 3× RT) **vóór** elke nieuwe PREREG. Faalt → nooit PREREG. Geen overnight maand-sleeves. Dead set niet heropenen.

### 9b. Herindeling catalogus (v3)

| Tier | Regels | Reden FTMO-uitvoerbaar? | Actiestatus |
|------|--------|------------------------|-------------|
| **A — HEROPENEN (hoge prioriteit)** | | | |
| A1 | **ORB/B4a (S3)** — intraday-vlak, US500/US100/GER40/XAU | Swap 0, instrumenten aanwezig, bevroren regel; bevestiging 2011–20 ontbreekt nog | Data-acquisitie (Sandro-actie), dan S3 |
| A2 | **Stocks-in-Play ORB earnings (S2)** — intraday-vlak, FTMO-aandelen-CFD | D-012 gemiddelde-poort; mean bruto te laag vs RT | **GESTOPT** kostenpoort TRAIN FAIL (`bba5c0c`; +3,77 < 26,74 bp) |
| A3 | **Noise-area intradag-momentum (S1)** — trailing EOD-exit, US-indices | Eerder afgewezen (na 2023); heroverwegen met nul-kalibratie en vol-regime; intraday-vlak | F1-heronderzoek, geen extra trial tenzij hypothese nieuw |
| A4 | **FOMC-cyclus (C17)** — even FOMC-weken, D1, index-CFD | Swap-drag hoger dan verwacht (mean nights ≈ 8,6) | **GESTOPT** kostenpoort TRAIN FAIL (`43b6ba2`); geen herstart zonder CEO |
| A5 | **FX-intradag-breakout** — London-open ORB majors | Swap 0; U3-precedent + m5gz-poort FAIL | **GESTOPT** kostenpoort TRAIN FAIL (`ce5abdc`); geen herstart (v41/C-003) |
| **B — ONDERZOEKEN (middel)** | | | |
| B1 | **TSMOM-mix FX (C05 op FX)** | Overnight maand-omloop + swap-drag | **GESTOPT** kostenpoort TRAIN FAIL (`18c7996`); geen nieuwe overnight maand-sleeves |
| B2 | **FX-carry + trendfilter (C12)** | Carry-risicopremie; C12 CAT1 ≈ 0 na kosten → herevalueer alleen met D1-reeksen + FTMO-FX-swaps | Lage prioriteit |
| B3 | **Donchian D1 FX/XAU (C03)** | R4 H4 negatief maar op short reeks; FX D1 = 1 nacht swap; positief scheef | Herevalueer met lange FX-dagreeksen (FRED 1971+) |
| **N — D-091 niet-kloon (nacht + cyclus 2–3)** | | | |
| N1 | **Opening-drive exhaustion FADE** — US100/US30/US500, T+30 ATR-filter, target→open, EOD flat | ≠ ORB (tegen drive, geen OR-break) | **GESTOPT** poort n=0 (`8c7a8e1`; 1,5× D1-ATR nooit geraakt) |
| N2 | **US100↔US500 relative morning** — z-score diff T+60, equal-risk, EOD flat | ≠ ORB/richting; twin-index | **GESTOPT** kostenpoort FAIL (`8c7a8e1`; −0,84 < 4,32 bp) |
| N3 | **US100 Close-Drive** — 14:30–15:55 ET, trend-filter 0,30%, EOD flat | ≠ ORB/A1/GS01 (close-sessie, geen OR-break) | **GESTOPT** gate PASS + t FAIL (`328284c`; NW t=0,853) |
| N4 | **XAU Pre-NY range breakout** — 13:00–15:00 CET range → NY open | ≠ XAU_AM_FADE (andere richting/tijd) | **GESTOPT** kostenpoort FAIL (`328284c`; +1,16 < 2,49 bp) |
| N5 | **US500/US100 Opening Gap Fill** — fade |gap|≥0,30%, 90-min flat | ≠ GS01 (fade vs continuation) | **GESTOPT** kostenpoort FAIL (CTO `69d15cc`; −3,84 < 1,95 bp) |
| N6 | **GER40 Pre-Close conditioneel** — 2u-trend 0,20%, 17:30–17:55 CET | ≠ B4b onvoorwaardelijk; ≠ N3 US close | **GESTOPT** kostenpoort FAIL (U2 `741639e` / CTO C-008); C-007 drained |
| N7 | **XAU Pre-London Range BO** (VOORSTEL_PRESCREEN_N7) | ≠ XAU_AM_FADE / N4 | **geen PREREG** — D-092.1 FAIL (C-010 `fc974de`; −1,18 bp) |
| N8 | **XAU Post-AM-Fix Continuation** (VOORSTEL_PRESCREEN_N8) | ≠ XAU_AM_FADE / N4 / N7 | **geen PREREG** — D-092.1 FAIL (C-010 `fc974de`; −1,47 bp) |
| N9 | **GER40 Ochtend-Fade → XETRA-open** (VOORSTEL_PRESCREEN_N9) | ≠ N6 / GER_US / LUNCH_OPEN US | **geen PREREG** — mean-PASS (+4,32≥4,20) maar **N=61≪150** underpowered (C-011 `01d93b7`) |
| N10 | **XAU Mid-London Fade → AM-Fix** (VOORSTEL_PRESCREEN_N10) | ≠ XAU_AM_FADE / N4 / N7 / N8 | **geen PREREG** — D-092.1 FAIL (C-011 `01d93b7`; −0,82 < 2,49 bp) |
| N11 | **GER40 XETRA ORB** — 09:00–09:30 ORB breakout, flat 13:00 | ≠ N9 fade / N6 close / S2-GER40-open | **GESTOPT FAIL_T** U2 `e6b2395` (gate PASS +2,74; stress FAIL; t≈0,92); TRIAL_COUNT **446** |
| N12 | **XAU NY-Open Continuation** (VOORSTEL_PRESCREEN_N12) | ≠ N4/N7/N8/N10/AM_FADE | **geen PREREG** — D-092.1 FAIL (C-012 `cdabfe8`; +0,59 < 2,49 bp) |
| N13 | **GER40 US-Open Sync** (VOORSTEL_PRESCREEN_N13) | ≠ N11 ochtend / GER_US_LEAD | **geen PREREG** — D-092.1 FAIL (U2 `d4cefff`; −3,34 bp; N=92) |
| N14 | **US100 NY-Open Pre-Market Mom** (VOORSTEL_PRESCREEN_N14) | ≠ LUNCH_OPEN fade / N3 close | **geen PREREG** — D-092.1 FAIL (U2 `d4cefff`; −5,05 bp) |
| N15–N17 | **Venue-ORB exploratie** (CTO C-013: UK100/JP225/US30+US100+US500) | single-symbol ORB clones | **geen PREREG** — alle FAIL (C-013 `64723ff`); simple ORB-family barred |
| N18 | **US500 Overnight Gap Continuation** — gap ≥±50 bp vs 22:00 CET, entry 15:30, flat 18:30 | ≠ N5 fade / ≠ ORB-familie | **GESTOPT FAIL_T** U2 `d1984ed` (gate+stress PASS; t≈0,64); TRIAL_COUNT **447**; D-093 freeze |
| N19 | **XAU Overnight Gap Fill** (VOORSTEL_PRESCREEN_N19) | ≠ N5 / XAU_AM_FADE / N7–N12 | **geen PREREG** — C-014 FAIL (+2,03 < 2,49); D-093 barred |
| N20 | **US30 PM Continuation** (VOORSTEL_PRESCREEN_N20) — AM-trend ≥±30 bp → entry 18:00 CET, flat 21:00 | ≠ LUNCH_OPEN / N3 / N14 / ORB | **geen PREREG — U2 D-092.1 FAIL** `a1756a7` (N=384, mean **−2,26** < 1,35); TRIAL_COUNT **447** |
| N21 | **GER40 Afternoon Deviation Fade** (VOORSTEL_PRESCREEN_N21) — dev vs XETRA-open ≥±50 bp → fade 16:30, flat 17:30 | ≠ N9 / N11 / N6 / N13 | **geen PREREG — U2 D-092.1 FAIL** `a1756a7` (N=234, mean **−2,45** < 2,16); TRIAL_COUNT **447** |
| N22 | **UKOILcash London→NY Session MR** (VOORSTEL_PRESCREEN_N22) — lon_bp ≥±40 bp → fade 15:30, flat 18:30 | ≠ S2-USOIL EIA / ORB; swap 0 | **geen PREREG — U2 D-092.1 FAIL** `a1756a7` (N=345, mean **−1,67** < 8,13); geen Lon-AM-fade kloon |
| N23 | **US100cash Swing 2d TSMOM** (VOORSTEL_PRESCREEN_N23) — ret20-sign, hold 2d, swap in gate | ≠ B1 FX month / ORB / N3 | **geen PREREG — U2 D-092.1 FAIL** `a1756a7` (N=377, mean **+4,46** < 13,68; long +10,83); geen 2d-TSMOM-dunnen |
| N24 | **US500cash Mid-Session Lunch Fade** (VOORSTEL_PRESCREEN_N24) — am_bp ≥±40 bp → fade 18:00, flat 20:30 | ≠ N20 cont / LUNCH_OPEN / IB_FADE / N18 | **geen PREREG — D-092.1 FAIL** Strateeg `n24_n27` (N=271, mean **+0,35** < 2,34); TRIAL_COUNT **447** |
| N25 | **XAUUSD NY Afternoon Fade** (VOORSTEL_PRESCREEN_N25) — dev vs NY-open ≥±35 bp → fade 18:00, flat 20:30 | ≠ AM_FADE / N4/N7–12/N19 | **geen PREREG — D-092.1 FAIL** Strateeg `n24_n27` (N=334, mean **+1,14** < 2,49) |
| N26 | **XS 1d Reversal Basket** (VOORSTEL_PRESCREEN_N26) — long bottom-1 / short top-1 of {US100,US30,US500,GER40,XAU}, 15:30→17:25 | ≠ N23 TSMOM / N2 / B1 | **geen PREREG — D-092.1 FAIL** Strateeg `n24_n27` (N=581, mean **+0,77** < 4,83) |
| N27 | **AUDUSD H4 MR** (VOORSTEL_PRESCREEN_N27) — |dev| vs SMA20(H4) ≥40 bp @12:00 → fade, exit 16:00 | ≠ A5/GS02/B1/N23 | **geen PREREG — D-092.1 FAIL** Strateeg `n24_n27` (N=429, mean **+1,49** < 3,66) |
| N28 | **EURJPY London→NY Session Mom** (VOORSTEL_PRESCREEN_N28) — lon_bp ≥±35 → continue 15:30, flat 18:30 | ≠ A5/GS02/S2-USDJPY/B1/N27 | **geen PREREG — D-092.1 FAIL** Strateeg `n28_n31` (N=189, mean **+2,91** < 3,30; closest miss) |
| N29 | **GBPUSD London Midday Fade** (VOORSTEL_PRESCREEN_N29) — |dev| vs 09:00 ≥30 @12:00 → fade, flat 15:00 | ≠ A5 ORB / GS02 / N27 | **geen PREREG — D-092.1 FAIL** Strateeg `n28_n31` (N=122, mean **−1,20** < 2,10) |
| N30 | **XS 5d Momentum Basket** (VOORSTEL_PRESCREEN_N30) — long top-1 / short bottom-1, 15:30→21:00 | ≠ N26 reversal / N23 / B1 | **geen PREREG — D-092.1 FAIL** Strateeg `n28_n31` (N=553, mean **+0,44** < 4,83) |
| N31 | **XAUUSD Asia→London Handoff Cont.** (VOORSTEL_PRESCREEN_N31) — |asia|≥40 00:00–08:00 → continue, flat 12:00 | ≠ AM_FADE / N25 / N4–12 | **geen PREREG — D-092.1 FAIL** Strateeg `n28_n31` (N=21, mean **−0,01** < 2,49) |
| N32 | **US30cash IB Breakout Continuation** (VOORSTEL_PRESCREEN_N32) — IB 15:30–16:30 break → flat 18:30 | ≠ IB_FADE / ORB / N20 | **geen PREREG — D-092.1 FAIL** Strateeg `n32_n34` (N=754, mean **+0,43** < 1,35) |
| N33 | **USDCAD London→NY Session Mom** (VOORSTEL_PRESCREEN_N33) — lon_bp ≥±35 → continue 15:30, flat 18:30 | ≠ N28 EURJPY / A5 / B1 | **geen PREREG — D-092.1 FAIL** Strateeg `n32_n34` (N=94, mean **+1,04** < 2,40) |
| N34 | **XAUUSD Post-AM-Fix MR to Lon-open** (VOORSTEL_PRESCREEN_N34) — |dev|≥40 @13:00 → fade, flat 15:00 | ≠ N8 cont / AM_FADE / N25 | **geen PREREG — D-092.1 FAIL** Strateeg `n32_n34` (N=148, mean **−2,71** < 2,49) |
| N35 | **US100cash Europe→US Open Cont.** — eu_bp 09:00–15:00 ≥±40 → entry 15:30, flat 17:00 | ≠ ORB / N3 / N14 / N20 | **GESTOPT FAIL_T** U2 `a498a69` (gate+stress PASS; t≈1,22/0,29); TRIAL **450**/451-set; geen herstart zonder CEO |
| N36 | **XAUUSD NY-Open Drive Cont.** — drive 15:30–16:00 ≥±25 → entry 16:00, flat 17:00 | ≠ N12 / N25 fade / AM_FADE | **GESTOPT FAIL_T** U2 `a498a69` (gate PASS; stress FAIL); TRIAL **451**; geen herstart zonder CEO |
| N37 | **EURUSD H4 Trend-Follow SMA20** — close vs SMA20+slope @12:00 → hold to 16:00 | ≠ N27 MR / A5 / B1 | **geen PREREG — D-092.1 FAIL** U2 `43c395e` (N=627, mean **−0,17** < 1,89) |
| N38 | **GBPUSD London Morning Mom Cont.** (VOORSTEL_PRESCREEN_N38) — 08:00→11:30 ≥±30 → flat 14:30 | ≠ N29 fade / S2-GBPJPY / N28 | **geen PREREG — D-092.1 FAIL** Strateeg `n38_n40` (N=102, **−1,35** < 2,10) |
| N39 | **BTCUSD Asia→Europe Handoff Cont.** (VOORSTEL_PRESCREEN_N39) — asia ≥±80 → flat 12:00 | ≠ S2-BTC US-open / S2b | **geen PREREG — D-092.1 FAIL** Strateeg `n38_n40` (N=132, **−3,43** < 3,75) |
| N40 | **GER40cash Mid-Morning Mom Cont.** — 09:30→12:00 ≥±40 → flat 14:00 | ≠ N9/N11/N13/N21/S2-GER* | **GESTOPT FAIL_T** U2 `5b3db74` (gate PASS; stress FAIL; trial **452**); TRIAL_COUNT **453**; geen retune |
| N41 | **US30cash Europe→US Open Cont.** — eu_bp ≥±40 → entry 15:30, flat 17:00 | ≠ N35 FAIL_T / N20 / N32 | **GESTOPT FAIL_T** U2 `5b3db74` (NW 1,85<2; test −4,39; trial **453**); geen herstart |
| N42 | **NZDUSD London Morning Mom Cont.** (VOORSTEL_PRESCREEN_N42) | ≠ N38 / S2-GBPJPY | **geen PREREG — D-092.1 FAIL** Strateeg `n41_n43` (N=132, +0,31 < 5,55) |
| N43 | **UKOILcash NY-Open Drive Cont.** (VOORSTEL_PRESCREEN_N43) | ≠ N22 MR / S2-USOIL | **geen PREREG — underpowered** Strateeg `n41_n43` (mean +12,74≥8,13 maar **N=139≪150**) |
| N44 | **US500cash Europe→US Open Cont.** (VOORSTEL_PRESCREEN_N44) — parallel N35/N41 | ≠ N18/N24/ORB | **BARRED clone-of-dead** N35/N41 FAIL_T — geen screen |
| N45 | **ETHUSD Asia→Europe Handoff Cont.** (VOORSTEL_PRESCREEN_N45) | ≠ N39 BTC / S2b / S2-BTC | **geen PREREG — D-092.1 FAIL** Strateeg `n45_n51` (N=61, mean **−81,8** < 54) |
| N46 | **EURGBP London Fix Extension Fade** (VOORSTEL_PRESCREEN_N46) | ≠ S2-GBPJPY/N29/N38 | **BARRED** D-098/C-021 intradag FX gate 3,12≪50 — geen screen |
| N47 | **USDCHF Asia→London Handoff Cont.** (VOORSTEL_PRESCREEN_N47) | ≠ S2-USDJPY/N31/N39 | **BARRED** D-098/C-021 intradag FX gate 3,03≪50 — geen screen |
| N48 | **USDJPY Swing 1d TSMOM** (VOORSTEL_PRESCREEN_N48) | ≠ B1/N23/S2-USDJPY | **geen PREREG — D-092.1 FAIL** Strateeg `n45_n51` (N=767, mean **+3,23** < 7,08) |
| N49 | **UKOILcash Swing TSMOM 20d→10d LO** (VOORSTEL_PRESCREEN_N49) | ≠ N22/N43/B1/N23/CEO TSMOM_DIV | **geen PREREG — D-092.1 FAIL** Strateeg `n45_n51` (N=55, mean **+36,4** < 50) |
| N50 | **USOILcash Swing TSMOM 20d→10d LO** (VOORSTEL_PRESCREEN_N50) | ≠ N49/S2-USOIL/N22 | **geen PREREG — D-092.1 FAIL** Strateeg `n45_n51` (N=54, mean **+34,2** < 50) |
| N51 | **XAUUSD TSMOM 20d→5d LO + SMA200** (VOORSTEL_PRESCREEN_N51) | ≠ XAU intradag FAIL set / N49 | **geen PREREG — D-092.1 FAIL** Strateeg `n45_n51` (N=59, mean **+8,5** < 50) |
| N52 | **US100cash TSMOM 120d→20d LO** (VOORSTEL_PRESCREEN_N52) | ≠ N23 2d / N49 energy | **geen PREREG — underpowered** mean **+131** ≥ 118,98 maar **N=21≪150** |
| N53 | **USDJPY TSMOM 60d→20d LO** (VOORSTEL_PRESCREEN_N53) | ≠ N48 1d / B1 / S2-USDJPY | **geen PREREG — underpowered** mean **+91,6** ≥ 50 maar **N=32≪150** |
| N54 | **UKOILcash Winter-Season Long** (VOORSTEL_PRESCREEN_N54) | ≠ N49 TSMOM / N22 intradag | **geen PREREG — underpowered** mean **+101,8** ≥ 50 maar **N=33≪150** |
| N55 | **Index basket TSMOM 120d→20d LO pooled** (N55) | ≠ N52 solo / CEO TSMOM_DIV | **geen PREREG — D-092.1 FAIL** pooled mean **+72,2** < 138,15 (N=70) |
| N56 | **Energy basket TSMOM 20d→10d LO pooled** (N56) | ≠ N49/N50 solo | **geen PREREG — D-092.1 FAIL** pooled mean **+35,3** < 50 (N=109) |
| N57 | **FX majors basket TSMOM 60d→20d LO pooled** (N57) | ≠ N48/N53 / B1 | **geen PREREG — D-092.1 FAIL** pooled mean **+40,7** < 50 (N=78; AUDUSD−) |
| N58 | **AUDJPY long-only carry+trend 20→10** (VOORSTEL_PRESCREEN_N58 redesign) | ≠ N58-v1 hostile pair / B1 / N62 | **geen PREREG — D-092.1 FAIL** mean **+41,66** < 50 (N=50); closest miss |
| N59 | **UKOILcash TSMOM + high-vol ATR** (VOORSTEL_PRESCREEN_N59) | ≠ N49/N54/N56 / ENERGY | **BARRED** ENERGY clone (C-024 / D-100) |
| N60 | **XAGUSD 5d swing TSMOM bi-dir** (VOORSTEL_PRESCREEN_N60) | ≠ N36/ENERGY/TSMOM_DIV | **geen PREREG — D-092.1 FAIL** mean **+37,01** < 53,01 (N=151) |
| N61 | **AUS200 short-only TSMOM 20→10** (VOORSTEL_PRESCREEN_N61) | ≠ IDX_SHORT US / N35 | **geen PREREG — D-092.1 FAIL** mean **−26,05** < 50 (N=45) |
| N62 | **GBPJPY long-only carry+trend 20→10** (VOORSTEL_PRESCREEN_N62) | ≠ S2-GBPJPY intradag / N58 | **geen PREREG — D-092.1 FAIL** mean **+9,75** < 50 (N=55) |
| N63 | **EURCHF long-only carry+trend 20→10** (VOORSTEL_PRESCREEN_N63) | ≠ N58/N62 | **geen PREREG — D-092.1 FAIL** mean **−43,08** < 50 (N=43) |
| N64 | **HK50 short-only TSMOM 20→10** (VOORSTEL_PRESCREEN_N64) | ≠ IDX_SHORT / N61 | **geen PREREG — underpowered** mean **+89,62** ≥ 50 maar **N=55≪150** |
| N65 | **XAGUSD short-only 5d TSMOM** (VOORSTEL_PRESCREEN_N65) | ≠ N60 bi-dir / N36 | **geen PREREG — D-092.1 FAIL** mean **+39,23** < 50 (N=98) |
| N66 | **EURAUD short-only carry+trend 20→10** (VOORSTEL_PRESCREEN_N66) | ≠ N63 / A5 / B1 | **SUBSUMED/dead** in FX_EUR_SHORT (FAIL_T TRIAL **454**) |
| N67 | **USDJPY long-only carry+trend 20→10** (VOORSTEL_PRESCREEN_N67) | ≠ N48/N53 / S2-USDJPY | **DIAG_FAIL** C-025/C-026 (L20); MED-pad closed under C-028 |
| N68 | **GER40 short-only TSMOM 20→10** (VOORSTEL_PRESCREEN_N68) | ≠ IDX_SHORT / N64 / N35 | **BARRED** family-A index-short closed (C-025) |
| N69 | **NZDUSD 10d carry+trend LO** (VOORSTEL_PRESCREEN_N69) | ≠ N66/N67 / B1 | **DIAG_FAIL** CTO C-026 (train −29 < ~33) |
| N70 | **XAUUSD 5d swing TSMOM bi-dir** (VOORSTEL_PRESCREEN_N70) | ≠ N36/N60 / ENERGY | **DIAG_FAIL** CTO C-026 (swap-wall / halves) |
| N71 | **GBPUSD 10d TSMOM SO** (VOORSTEL_PRESCREEN_N71) | ≠ N29 / GBPJPY | **DIAG_FAIL** CTO C-026 (+3,8 < ~11) |
| N72 | **EURJPY_MED** — long-only L60/H10 (VOORSTEL_PRESCREEN_N72) | ≠ N28 intradag / USDJPY_MED | **BARRED/STOP** — C-028; EURJPY_MED FAIL_T U2 `65a9b23`; TRIAL 455→456 |
| N73 | **USDCAD long-only L60/H10** (VOORSTEL_PRESCREEN_N73) | ≠ S2 USDCAD L20 FAIL / N33 | **BARRED/STOP** — C-028 L60 FX-med family closed after USDJPY_MED/EURJPY_MED FAIL_T; TRIAL_COUNT **456** |
| N74 | **USDCHF long-only L60/H10** (VOORSTEL_PRESCREEN_N74) | ≠ S2 USDCHF L20 FAIL / N47 | **BARRED/STOP** — C-028 L60 FX-med family closed after USDJPY_MED/EURJPY_MED FAIL_T; TRIAL_COUNT **456** |
| N75 | **XAU/XAG ratio MR 3d LO-gold/SO-silver** (VOORSTEL_PRESCREEN_N75) | ≠ N60/N65/N70 / ENERGY / L60-FX | **DIAG_FAIL** C-029 (mean 10,86 ≪ 30,60; N=71); geen PREREG |
| N76 | **UKOIL Mon→Thu inventory-window LO** (VOORSTEL_PRESCREEN_N76) | ≠ ENERGY/N49/N54/N59 | **DIAG_FAIL** C-029 (mean −14,90 ≪ 50,00; N=153); geen PREREG |
| N77 | **FX6 vol-timed XS rank-reversal 5d** (VOORSTEL_PRESCREEN_N77) | ≠ TSMOM_DIV/N26/N30/N57/L60 | **DIAG_FAIL** C-029 (mean −2,57 ≪ 46,29; N=107); geen PREREG |
| N78 | **VIX_TERM_VOV** — VIX9D/VIX3M + VoV10 combo → US100 1d LO (`PREREG_FTMO_N78_VIX_TERM_VOV`) | ≠ XASSET_VOL_TIMING / TSMOM / ORB / L60 / N75–N77 | **STOP FAIL_COST_GATE** U2 `b998253` (mean **+2,21** ≪ 7,83); **geen trial** (C-029/U2 `40d770a`); TRIAL_COUNT **456**; no VIX_TERM clones |
| N79 | **RATE_CURVE→UKOIL LO 5d** (VOORSTEL_PRESCREEN_N79) | ≠ C45 equity / ENERGY / N76 / N78 | **UNDERPOWERED** C-029 (mean 126,71 ≥ 50; N=46≪150); geen PREREG |
| N80 | **UKOIL OVN-gap cont, same-day flat** (`PREREG_FTMO_N80`) | ≠ N18/N19/N22/N76 / ENERGY | **STOP FAIL_COST_GATE** U2 `454628f` (mean **+7,56** < 8,13 with stop; stress 12,20 FAIL; years +25,26/−0,46/−3,63); **geen trial**; TRIAL_COUNT **456**; dead += N80; no OVN-gap clones |
| N81 | **US100/US500 pair RV 3d** (VOORSTEL_PRESCREEN_N81) | ≠ N2/N26/N30 / N78 / N75 | **DIAG_FAIL** C-029 (mean −7,77 ≪ 13,74; N=86); skip |
| N82 | **XAGUSD London AM-Fix Fade** (VOORSTEL_PRESCREEN_N82) | ≠ XAU_AM_FADE / N25 / N10 / N75 | **DIAG_FAIL** C-030 (mean −2,91 ≪ 15,21; N=311); geen PREREG |
| N83 | **DXY overnight → US100 opposite intradag** (VOORSTEL_PRESCREEN_N83) | ≠ N2 / N81 / N78 / IDX_SHORT | **UNDERPOWERED** C-030 (mean +15,36 ≥ 1,98; N=52≪150); geen PREREG |
| N84 | **AUDNZD rate-diff stretch fade EOD-flat** (VOORSTEL_PRESCREEN_N84) | ≠ L60-FX / N69/N71/N77 / N80 | **DIAG_FAIL** C-030 (mean +0,48 ≪ 3,18; N=460); geen PREREG |
| N85 | **US500 AM → US100 PM lead-lag** (VOORSTEL_PRESCREEN_N85) | ≠ N2 / N81 / N83 / IDX_SHORT | **DIAG_FAIL** C-030 (mean −7,11 ≪ 1,98; N=370); geen PREREG |
| N86 | **XAU own RV-VoV → 3d MR** (VOORSTEL_PRESCREEN_N86) | ≠ N78 VIX_TERM / N70 / N75 / AM_FADE | **DIAG_FAIL** C-030 (mean −9,27 ≪ 15,39; N=96); geen PREREG |
| N87 | **US30cash opening-gap fade** (VOORSTEL / CEO PREREG) | ≠ N5/N18 / ORB / N80 | **STOP FAIL_T** U2 `3a9108e` (t_NW=1,63; test −17,7); TRIAL **457**; no gap-fade clones |
| N88 | **EURGBP 5d short-only TSMOM** (VOORSTEL_PRESCREEN_N88) | ≠ FX_EUR_SHORT / N46 / N71 | **geen PREREG — D-092.1 pre-FAIL** U2 `d17573c` (N=107; −5,76 < 3,12) |
| N89 | **GER40cash EU 2h open momentum** (VOORSTEL_PRESCREEN_N89) | ≠ N40 / ORB / N35 | **geen PREREG — D-092.1 pre-FAIL** U2 `d17573c` (+1,06 ≪ 2,16) |
| N90 | **GBPJPY LO 5d carry+momentum** (VOORSTEL_PRESCREEN_N90) | ≠ N88 / N28 / L60 / N71 | **UNDERPOWERED** C-031 (mean +10,15; N=113≪150); geen PREREG |
| N91 | **AUDUSD LO 5d carry+momentum** (VOORSTEL_PRESCREEN_N91) | ≠ FX_EUR_SHORT / N88 / N90 / L60 | **DIAG_FAIL** C-031 (mean −18,59 ≪ 1,35; N=101); geen PREREG |
| N92 | **US100cash NY-open 2h momentum** (PREREG_FTMO_N92 / C-031) | ≠ N89 / N87 / ORB / N40 | **STOP FAIL_T** U2 `b5b59e0` (t_NW 1,56; test 0,51); TRIAL **458**; no NY-2h mom clones |
| N93 | **SECTOR_DISP_ROTATION → US100cash session-flat** (PREREG; S2 `fde4a15`) | ≠ N78 VIX / N92 / ORB / TSMOM | **STOP FAIL_COST_GATE** U2 `b382307` (N=309, mean **+0,99 < 1,98**; stress FAIL; test −10,99); **geen trial**; TRIAL_COUNT **458**; dead += N93; no SECTOR_DISP clones |
| N94 | **NZDJPY LO 5d carry+momentum** (VOORSTEL_PRESCREEN_N94) | ≠ N90 / N91 / L60 / N62 | **geen PREREG — D-092.1 FAIL** Strateeg `n94_n95` (N=107≪150, mean **−0,97 < 6,00**) |
| N95 | **XAUUSD Lon-AM → NY cont session-flat** (VOORSTEL_PRESCREEN_N95) | ≠ XAU_AM_FADE / N36 / N82 / N86 | **geen PREREG — D-092.1 FAIL** Strateeg `n94_n95` (N=226, mean **+1,40 < 2,49**) |
| N96 | **CADJPY LO 5d carry+momentum** (VOORSTEL_PRESCREEN_N96) | ≠ N94 / N90 / N58 / L60 | **UNDERPOWERED** Strateeg `n96_n97` (mean **+16,45 ≥ 4,80**; **N=112≪150**); geen PREREG |
| N97 | **AUDCAD LO 5d commodity-XS mom** (VOORSTEL_PRESCREEN_N97) | ≠ N84 / N91 / N96 / N77 | **geen PREREG — D-092.1 FAIL** Strateeg `n96_n97` (N=101, mean **−8,87 < 4,50**) |
| N98 | **USOILcash Lon-AM → US100 NY risk-on lead-lag** (VOORSTEL_PRESCREEN_N98) | ≠ N85 / N83 / UKOIL-OVN / ENERGY | **DIAG_FAIL** C-034 (mean **−3,79 ≪ 1,98**; N=356); geen PREREG |
| N99 | **CADCHF LO 5d oil-CHF carry+momentum** (VOORSTEL_PRESCREEN_N99) | ≠ N96 / N94 / N90 / L60 | **DIAG_FAIL** C-034 (mean **−4,00 ≪ 6,81**; N=103); geen PREREG |
| N100 | **EMB_CREDIT_STRESS → US100cash session-flat** (PREREG; S2 `67a9be1`) | ≠ HYG/LQD / EM_DM / SECTOR_DISP / VIX / N98 | **STOP FAIL_T** U2 `d09d00a` (cost+stress PASS; t/NW 0,37/0,38; test −2,57); TRIAL **458→459**; no EMB clones |
| N101 | **CRACK_SPREAD_MACRO → US100cash session-flat** (PREREG; S2 `67a9be1`) | ≠ ENERGY/UKOIL-OVN / N98 / oil CFD | **STOP FAIL_T** U2 `d09d00a` (cost+stress PASS; t/NW 1,05/1,21; test −5,00); TRIAL **459→460**; no crack clones |
| N102 | **USDCHF LO 5d USD-CHF carry+momentum** (VOORSTEL_PRESCREEN_N102) | ≠ N99 CADCHF / N74 L60 / NZDJPY / AUDCAD | **geen PREREG — D-092.1 FAIL** `n102_n103` (N=104, mean **+2,94 < 3,03**) |
| N103 | **GER40 Lon-AM → US30 NY industrial lead-lag** (PREREG_FTMO_N103) | ≠ N98 / S2-GER_US / N85 / N41 | **STOP FAIL_STRESS** U2 `b9af560` (cost PASS +1,75; stress FAIL vs 2,025; years +2,29/+10,53/**−14,08**; test +1,32); **geen trial**; TRIAL_COUNT **460**; dead += N103; no GER→US30 / US100 / GER→US-open clones |
| N104 | **GBPCHF LO 5d GBP-CHF carry+momentum** (VOORSTEL_PRESCREEN_N104) | ≠ N102 USDCHF / N99 CADCHF / N63 EURCHF | **UNDERPOWERED** D-092.1 `n104_n105` (mean **+10,62 ≥ 4,53**; **N=98≪150**); geen PREREG |
| N105 | **JP225 Tokyo-AM → Lon continuation session-flat** (VOORSTEL_PRESCREEN_N105) | ≠ N103 / N45 / N64 / N85 | **geen PREREG — D-092.1 FAIL** `n104_n105` (N=392, mean **−2,77 < 4,53**) |
| N106 | **EURNZD LO 5d EUR-NZD carry+momentum** (VOORSTEL_PRESCREEN_N106) | ≠ N104 GBPCHF / N94 NZDJPY / N97 AUDCAD | **geen PREREG — D-092.1 FAIL** `n106_n107` (N=103, mean **+3,45 < 4,11**) |
| N107 | **UK100 Lon-AM → FRA40 afternoon cont session-flat** (VOORSTEL_PRESCREEN_N107) | ≠ N105 JP225 / N103 GER→US30 / N85 | **geen PREREG — D-092.1 FAIL** `n106_n107` (N=255, mean **+3,94 < 5,94**) |
| N108 | **AUS200 Asia-AM → Lon continuation session-flat** (VOORSTEL_PRESCREEN_N108) | ≠ N105 JP225 / N61 AUS SO / N107 | **geen PREREG — D-092.1 FAIL** `n108_n109` (N=242, mean **−4,86 < 4,38**) |
| N109 | **CHFJPY LO 5d CHF-JPY carry+momentum** (VOORSTEL_PRESCREEN_N109) | ≠ N96 CADJPY / N94 NZDJPY / N90 GBPJPY / L60 | **UNDERPOWERED** D-092.1 `n108_n109` (mean **+19,69 ≥ 4,23**; **N=122≪150**); geen PREREG |
| N110 | **DXYcash Lon-AM → EU-afternoon cont session-flat** (VOORSTEL_PRESCREEN_N110) | ≠ N108 Asia→Lon / N107 UK→FRA / N103 | **DIAG_FAIL** C-036 (DATA_GAP; n=0 train); geen PREREG; no DXY Lon→EU-PM clones |
| N111 | **GBPAUD LO 5d GBP-AUD carry+momentum** (VOORSTEL_PRESCREEN_N111) | ≠ N97 AUDCAD / N104 GBPCHF / N106 EURNZD | **DIAG_FAIL** C-036 (mean +3,24 < 4,38; N=104); geen PREREG; no GBPAUD-LO clones |
| N112 | **GAS_EQUITY_MACRO → US500cash session-flat** (PREREG; S2 `35e38ac`) | ≠ ENERGY/UKOIL-OVN / N101 CRACK / N98 / gas CFD | **STOP FAIL_T** U2 `d1dd863`/`954680a` (cost+stress PASS; t/NW 1,07/1,04; test −4,34); TRIAL **460→461**; dead += N112; no UNG→US500 / gas CFD clones |
| N113 | **SILVER_GOLD_RATIO → US500cash session-flat** (PREREG; S2 `35e38ac`) | ≠ N75 XAU/XAG / N95 / N82 / silver CFD | **STOP FAIL_COST_GATE** U2 `954680a` (N=305, +1,60 < 2,34; **geen trial**); TRIAL **461**; dead += N113; no SLV/GLD→US500 / silver CFD clones |
| N114 | **HYG_CREDIT_STRESS → US500cash session-flat** (PREREG_FTMO_N114) | ≠ N100 EMB / N93 / N78 / N112 / N113 | **STOP FAIL_T** U2 `527e46e` (cost+stress PASS; t/NW 0,68/0,71; test −2,16; years −10,03/+7,69/+4,82); TRIAL **461→462**; dead += N114; no HYG/LQD/EMB clones |
| N115 | **EURUSD Lon-AM → US500 NY macro-beta session-flat** (VOORSTEL_PRESCREEN_N115) | ≠ N110 DXY / N83 opposite / N103 / N85 | **geen PREREG — D-092.1 FAIL** `n114_n115` (N=126, mean **−3,43 < 2,34**); NEW_FAMILY AJ dead screen |
| N116 | **TLT_DURATION_STRESS → US500cash session-flat** (PREREG_FTMO_N116) | ≠ N114 HYG / N100 EMB / REIT_RATE / N112 | **STOP FAIL_T** U2 `d0aa317` (cost+stress PASS; t/NW 1,16/1,17; test +3,46; years +3,39/+9,62/+1,92); TRIAL **462→463**; dead += N116; no TLT→US500 / IEF twin / TIP rewrite (TIP≠TLT) |
| N117 | **CPER_COPPER_STRESS → US500cash session-flat** (PREREG_FTMO_N117) | ≠ N113 Ag/Au / COPPER_GOLD ratio / N112 gas / copper CFD | **STOP FAIL_STRESS** U2 `d8b97d0` (cost PASS +2,89≥2,34; stress FAIL +2,89<3,51; med −2,21; years +0,52/+11,84/−5,56; **geen trial**; TRIAL **463**); dead += N117; no CPER→US500 / CuAu / copper CFD |
| N118 | **TIP_REALRATE_STRESS → US500cash session-flat** (PREREG_FTMO_N118) | ≠ N116 TLT / N114 HYG / N100 EMB / IEF twin | **STOP FAIL_T** U2 `9e928af`/`9a00524` (cost+stress PASS; t/NW 0,99/0,99; test −4,20; years −7,40/+7,92/+5,27); TRIAL **463→464**; dead += N118; no TIP→US500 / IEF twin / TLT rewrite; TIP≠TLT |
| N119 | **IWM_SMALLCAP_STRESS → US500cash session-flat** (VOORSTEL_PRESCREEN_N119) | ≠ N93 SECTOR_DISP / N81 pair RV / IWM CFD | **geen PREREG — D-092.1 FAIL** `n118_n119` (N=186, mean **−0,48 < 2,34**; med −3,47); NEW_FAMILY AN dead screen; IWM level≠SECTOR_DISP |
| N120 | **VNQ_REIT_STRESS → US500cash session-flat** (VOORSTEL_PRESCREEN_N120) | ≠ N116 TLT / N118 TIP / VNQ/TLT ratio / N119 IWM | **geen PREREG — D-092.1 FAIL** `n120_n121` (N=342, mean **−0,38 < 2,34**; years +0,48/−0,00/−1,12); NEW_FAMILY AO dead screen; VNQ level≠TLT/TIP/VNQ-TLT ratio |
| N121 | **EEM_EM_EQUITY_STRESS → US500cash session-flat** (VOORSTEL_PRESCREEN_N121) | ≠ N100 EMB credit / N119 IWM / HYG / TLT | **geen PREREG — D-092.1 FAIL** `n120_n121` (N=172, mean **+0,08 < 2,34**; med −8,98; years +15,33/+4,76/−8,05); NEW_FAMILY AP dead screen; EEM≠EMB |
| N122 | **DBC_COMMODITY_STRESS → US500cash session-flat** (VOORSTEL_PRESCREEN_N122) | ≠ N117 CPER / N112 GAS / N113 SILVER / N101 CRACK | **DIAG_FAIL** C-038 `1a22e81` (N=368, mean **−6,31 < 2,34**); geen PREREG; NEW_FAMILY AQ dead; no DBC→US500 clones |
| N123 | **EFA_DM_EXUS_STRESS → US500cash session-flat** (VOORSTEL_PRESCREEN_N123) | ≠ N121 EEM / N100 EMB / N119 IWM | **DIAG_FAIL** C-038 `1a22e81` (N=201, mean **−2,66 < 2,34**); geen PREREG; NEW_FAMILY AR dead; no EFA→US500 clones |
| N124 | **YIELD_CURVE_2S10S → US500cash session-flat** (PREREG; S2 `13fe10c`) | ≠ N116 TLT / N118 TIP / N120 VNQ / RATE_CURVE | **STOP FAIL_T** U2 `9f00f24` (cost+stress PASS; t/NW **1,72/1,82** <2; test +2,89; N=240/+8,97 train); TRIAL **464→465**; dead += N124; no yield-curve / thr-grid / US100 overnight / TLT-TIP-SECTOR_DISP clones |
| N125 | **DEFENSIVE_CYCLICAL → US500cash session-flat twin** (PREREG; S2 `13fe10c`) | ≠ N93 SECTOR_DISP / N119 IWM / US100 overnight | **STOP FAIL_T** U2 `9f00f24` (cost+stress PASS; t/NW **1,22/1,29** <2; test −2,32; N=478/+5,48 train); TRIAL **465→466**; dead += N125; no XLU/XLI twin / US100 overnight / SECTOR_DISP clones |
| N126 | **DBA_AG_STRESS → US500cash session-flat** (VOORSTEL_PRESCREEN_N126) | ≠ N122 DBC / N117 CPER / N112 GAS / N113 SILVER / N101 CRACK | **geen PREREG — D-092.1 FAIL** `n126_n127` (N=380, mean **−6,36 < 2,34**); NEW_FAMILY AU dead screen; ≠DBC |
| N127 | **EWZ_BRAZIL_STRESS → US500cash session-flat** (PREREG_FTMO_N127) | ≠ N121 EEM / N100 EMB / N123 EFA | **STOP FAIL_T** U2 `3a970c7` (cost+stress PASS; t/NW **0,57/0,50**; test N=85 **+1,85**; train +3,54); TRIAL **466→467**; dead += N127; no EWZ/EEM/EMB/EFA clones |
| N128 | **BWX_INTL_TREASURY_STRESS → US500cash session-flat** (PREREG_FTMO_N128) | ≠ N116 TLT / N118 TIP / N100 EMB / N124 YIELD_CURVE | **STOP FAIL_T** U2 `62a7718` (cost+stress PASS; t/NW **1,40/1,43**; test N=136 **−2,37**; train +6,63); TRIAL **467→468**; dead += N128; no BWX/TLT/TIP/EMB/yield clones |
| N129 | **PPLT_PLATINUM_STRESS → US500cash session-flat** (VOORSTEL_PRESCREEN_N129) | ≠ N113 SILVER_GOLD / N117 CPER / N126 DBA / XAU | **geen PREREG — D-092.1 FAIL** `n128_n129` (N=185, mean **−2,51 < 2,34**; years −14,58/−2,22/+1,70); NEW_FAMILY AX dead screen; no PPLT/PALL clones |
| N130 | **EQW_BREADTH_STRESS → US500cash session-flat** (PREREG_FTMO_N130) | ≠ N119 IWM / N93 SECTOR_DISP / N125 XLU-XLI / N81 pair RV | **STOP FAIL_T** U2 `03ad9da` (cost+stress PASS; t/NW **1,05/1,20**; test N=91 **−3,85**); TRIAL **468→469**; dead += N130; no EQW/breadth clones |
| N131 | **DXY_DOLLAR_STRESS → US500cash session-flat** (PREREG_FTMO_N131) | ≠ N110 DXY Lon→EU-PM / N127 EWZ / N128 BWX / FX 5d LO | **STOP FAIL_T** U2 `03ad9da` (cost+stress PASS; t/NW **1,01/1,05**; test N=146 **−1,10**); TRIAL **469→470**; dead += N131; **≠ N110** session kept; no DXY clones |
| N132 | **MTUM_MOM_FACTOR_STRESS → US500cash session-flat** (VOORSTEL_PRESCREEN_N132) | ≠ N130 EQW / N119 IWM / N93 SECTOR_DISP / N125 XLU-XLI | **geen PREREG — D-092.1 FAIL** `n132_n133` (N=185, mean **+1,55 < 2,34**; med −0,52; years +11,52/−6,45/+4,90; L/S 106/79); NEW_FAMILY BA dead screen; no MTUM/momentum-factor clones |
| N133 | **GLD_GOLD_HAVEN_STRESS → US500cash session-flat** (VOORSTEL_PRESCREEN_N133) | ≠ N113 SILVER_GOLD / N129 PPLT / N117 CPER / N122 DBC / N118 TIP / N131 DXY | **geen PREREG — D-092.1 FAIL** `n132_n133` (N=361, mean **+0,26 < 2,34**; med −0,68; years −4,00/+12,60/−12,07; L/S 146/215); NEW_FAMILY BB dead screen; no GLD/GOLD haven clones |
| N134 | **XLF_FINANCIAL_STRESS → US500cash session-flat** (VOORSTEL_PRESCREEN_N134) | ≠ N114 HYG / N100 EMB / N93 SECTOR_DISP / N125 XLU-XLI / N132 MTUM | **geen PREREG — D-092.1 FAIL** `n134_n135` (N=184, mean **−1,46 < 2,34**; med −6,04; years +11,62/+0,27/−5,66; L/S 82/102); not a SECTOR_DISP clone (agree 0,38); NEW_FAMILY BC dead screen; no XLF clones |
| N135 | **QUAL_QUALITY_STRESS → US500cash session-flat** (VOORSTEL_PRESCREEN_N135) | ≠ N132 MTUM / N130 EQW / N119 IWM / N125 XLU / USMV | **geen PREREG — D-092.1 FAIL** `n134_n135` (N=211, mean **−5,03 < 2,34**; med −6,86; years +10,50/−4,31/−9,58; L/S 86/125); not an EQW/IWM clone (IWM z-corr 0,72, cover 0,52); NEW_FAMILY BD dead screen; no QUAL clones |
| N136 | **BRENT_WTI_XS → UKOIL+USOIL session-flat** (VOORSTEL_PRESCREEN_N136) | ≠ N101 crack→equity / N22 UKOIL Lon-AM / N80 OVN-gap / ENERGY_TSMOM | **geen PREREG — D-092.1 FAIL** `n136_n137` (N=200, mean **−0,51 < 18,15**; med +0,19; years −8,38/+1,26/−0,03; L/S 98/102); not a CRACK clone (z-corr −0,11; agree 0,39); not UKOIL-OVN (agree 0,50; cover 0,47); NEW_FAMILY BE dead screen; no Brent–WTI / crack rewrite |
| N137 | **USDMXN_EM_CARRY_FADE session-flat** (VOORSTEL_PRESCREEN_N137) | ≠ G10 5d LO carry / N84 AUDNZD / N77 FX6 / N110 DXY | **geen PREREG — D-092.1 FAIL** `n136_n137` (N=**105≪150**, mean **+7,34 < 8,88**; med +5,39; years +5,36/+7,79/+9,49; all short); not a G10/DXY clone (DXY ret5 corr 0,46); NEW_FAMILY BF dead screen; no USDMXN/USDZAR twin |
| N138 | **GER40_UK100_XS → both legs session-flat** (VOORSTEL_PRESCREEN_N138) | ≠ N81 US pair RV / N103 GER→US30 / N107 UK→FRA / N136 Brent–WTI | **geen PREREG — D-092.1 FAIL_CLONE** `n138_n139` (N=178, mean **−4,09 < 6,42**; med −5,85; years —/−3,22/−4,74; L/S 67/111); EU50/UK z40 sign-agree **1,00** cover **0,78** (z-corr 0,89); not N103 (agree 0,51, cover 0,41) / not N107 (agree 0,51, cover 0,38); NEW_FAMILY BG dead screen; no GER/UK or EU50/UK rewrite |
| N139 | **JP225_HK50_ASIA_XS Asia-morning flat** (VOORSTEL_PRESCREEN_N139) | ≠ N138 DAX/FTSE / N105 JP→Lon / N108 AUS→Lon / N64 HK50 TSMOM | **geen PREREG — D-092.1 FAIL** `n138_n139` (N=240, mean **−1,97 < 12,42**; med −4,27; years −4,95/+1,44/−3,97; L/S 59/181); not N108 (agree 0,55, cover 0,32) / not N105 (agree 0,51, cover 0,46) / JP–AUS z-corr 0,34 / N64 agree 0,06; NEW_FAMILY BH dead screen; no JP/HK or AUS-morning rewrite |
| N140 | **XAU_UKOIL_XS → both legs session-flat** (VOORSTEL_PRESCREEN_N140) | ≠ N136 Brent–WTI / N75 XAU/XAG / N113 SLV→US500 / N95 XAU single-leg / N80 OVN | **OPEN** screen — **NEW_FAMILY BI** D-097; gate **10,62** bp (XAU 0,83 + UKOIL 2,71, both in COSTS); not screened this cycle |
| N141 | **XAG_UKOIL_XS → both legs session-flat** (VOORSTEL_PRESCREEN_N141) | ≠ N140 XAU/UKOIL / N75 XAU/XAG / N82 XAG fade / N136 Brent–WTI / N113 | **OPEN** screen — **NEW_FAMILY BJ** D-097; gate **23,34** bp (XAG 5,07 + UKOIL 2,71, both in COSTS); not screened this cycle |
| TSMOM_DIV | **Gediversifieerde 12-1 TSMOM** (CEO `PREREG_FTMO_TSMOM_DIV`) | D-098; ≠ B1/N49–N57 | **STOP FAIL_COST_GATE** U2 `e5d23c5` (geen trial) |
| ENERGY_TSMOM | **UKOIL+USOIL L20/H10 LO** (CTO C-023 / D-099) | ≠ N49/N59 | **STOP FAIL_COST_GATE** U2 `c1499ce` (geen trial) |
| IDX_SHORT | **US100+US30 short-only L20/H10** (CTO C-024 / D-100) | ≠ N35/N41/N61/N64 | **STOP FAIL_COST_GATE** U2 `72f40d3` (geen trial; family A closed) |
| FX_EUR_SHORT | **EURUSD+EURAUD short L20/H10** (CTO C-025) | ≠ N66 subsumed / B1 | **STOP FAIL_T** U2 `0e04df6` (TRIAL **454**; t train 1,90) |
| USDJPY_MED | **USDJPY long-only L60/H10** (CTO C-026 / D-100) | ≠ N67 L20 DIAG_FAIL | **BARRED/STOP FAIL_T** U2 `910d6ff` (TRIAL 454→455); C-028 closes L60 FX-med family |

| P1 | **ORB + BTC portfolio** (PREREG_FTMO_P1_ORB_BTC) | CEO D-095/D-096 | **GESTOPT FAIL** CTO C-020 `0a97602` (reserve t=0,24 / SR=0,20 / BTC-leg <0); TRIAL_COUNT **448** |
| **C — HERBEOORDELEN met FTMO-EV** | | | |
| C1 | **C02 Faber (D1 DD-filter, 1 nacht swap)** | Als overlay (long/flat), swap ≈ 1–2,3 bp/nacht → 5–8%/jr drag op long; nuttig als risicobeheer maar geen FTMO-trial | Geen trial; als portefeuille-overlay in FTMO-context herbeoordelen |
| C2 | **C55 DAA** | Weinig trades; swap-drag als in positie | Na engine/ftmo.py eventueel herbeoordelen |
| C3 | **C17 uitstellen van D1 naar intradag** | Maak er intraday-vlak van (ORB-achtig) | Exploratief; geen trial zonder PREREG |
| **D — SCHRAPPEN (FTMO-onuitvoerbaar)** | | | |
| D1 | C52 all-weather / C51 vol-managed / C53 dual-momentum / C54 Carver | UCITS-only; obligatiefutures niet op FTMO; long-index-swap 5–8%/jr doodt het | Geparkeerd in archief/eigen_kapitaal |
| D2 | C58 goud-trend / C59 grondstoffen-trend / C60 obligatie-duurtiming / C61 inverse-ETF | UCITS-only | Idem |
| D3 | Factorpremies C63 / CAPE C68 / landenrotatie C67 | UCITS-only; niet FTMO-verhandelbaar | Literatuurevidentie blijft; geen FTMO-run |
| D4 | C64 managed-futures UCITS | Geen FTMO-instrument | Watch-list eigen kapitaal later |

### 9c. FTMO-EV-baseline (na engine/ftmo.py gereed)
Per heropende regel de volgende metriek berekenen:
- `P(fase1_pass)`: kans op +10% vóór −10% (monte-carlo op dagreeks)
- `P(fase2_pass | fase1_pass)`: idem +5% vóór −5%
- `P(account_survive_12m | funded)`: overleven zonder dagverliesregel of statisch verlies
- `E[uitbetaling/mnd]`: over de overlevende jaren, na winstsplit 80%
- `FTMO_EV_netto`: voorgaande min fee/pogingen

**Doel: FTMO-EV ≥ €400/mnd bij realistisch risico (≤ 2% dagverlies als het fout gaat).** Schaal > 4% dagverlies-risico wordt alleen als bovengrens gerapporteerd (D-016/D-085).

## 10. Coördinatie Strateeg-1 / Strateeg-2 (D-090…D-100, bijgehouden door Strateeg `claude/trusting-faraday-34tsmg`)

*Bijgewerkt: 2026-10-03 00:38 Amsterdam — D-092.1 `n136_n137`: **N136 FAIL** (−0,51 < 18,15; N=200; not a CRACK/UKOIL-OVN clone) + **N137 FAIL** (+7,34 < 8,88; N=105; not a G10/DXY clone). No PREREG. Dead += N136/N137 (no Brent–WTI / USDMXN/USDZAR twins / thr-grid / overnight). Filed OPEN **N138–N139** NEW_FAMILY BG/BH (GER40–UK100 XS / JP225–HK50 Asia-morning XS). Freeze OFF. TRIAL **470**. **Geen** U2 wake; Quiet to Sandro*

### 10a. Overzicht PREREGs (Faraday + Grok Strateeg-1 + Strateeg-2)

| Code | Naam | Branch | Status | Distinct / overlap |
|------|------|--------|--------|--------------------|
| C17 / A4 | FOMC-cyclus index-CFD | faraday | **STOP** poort FAIL `43b6ba2` | overnight swap-drag |
| FX_INTRADAG / A5 | London-open ORB FX | faraday | **STOP** poort FAIL `ce5abdc` | ≠ GS02 fade; U3-familie bevestigd dood |
| B1 | TSMOM-mix FX (C05) | faraday | **STOP** poort FAIL `18c7996` | ≠ B2/C12; geen nieuwe overnight maand-sleeves |
| A2 | Stocks-in-Play ORB earnings | faraday | **STOP** poort FAIL `bba5c0c` | ≠ A1/GS01 indices; D-012 vs oude S2-mediaan |
| N1 | Opening-drive exhaustion FADE | faraday | **STOP** n=0 `8c7a8e1` | ≠ ORB; ATR-drempel te streng (geen post-hoc retune) |
| N2 | US100↔US500 relative morning | faraday | **STOP** poort FAIL `8c7a8e1` | ≠ ORB/richting; twin-index |
| N3 | US100 Close-Drive | faraday | **STOP** gate PASS + t FAIL `328284c` | ≠ ORB; SE te hoog (t=0,85) |
| N4 | XAU Pre-NY breakout | faraday | **STOP** poort FAIL `328284c` | ≠ XAU_AM_FADE |
| N5 | Opening Gap Fill US500/US100 | faraday | **STOP** poort FAIL CTO `69d15cc` (−3,84 bp) | ≠ GS01 continuation |
| N6 | GER40 Pre-Close conditioneel | faraday | **STOP** poort FAIL U2 `741639e` (C-007) | ≠ B4b / ≠ N3 |
| N7 / N8 (XAU) | Pre-London BO / Post-AM-Fix cont. | faraday VOORSTEL | **geen PREREG** — C-010 FAIL (`fc974de`) | ≠ XAU_AM_FADE / N4 |
| N9 | GER40 Ochtend-Fade → XETRA-open | faraday VOORSTEL | **geen PREREG** — mean-PASS N=61≪150 (C-011) | ≠ N6 / GER_US / LUNCH_OPEN |
| N10 | XAU Mid-London Fade → AM-Fix | faraday VOORSTEL | **geen PREREG** — C-011 FAIL (−0,82 bp) | ≠ XAU_AM_FADE / N7 / N8 |
| N11 | GER40 XETRA ORB | faraday | **STOP FAIL_T** U2 `e6b2395` (gate PASS +2,74; stress FAIL; t≈0,92); TRIAL_COUNT **446** | ≠ N9/N6/S2-GER40-open; skew-fragile |
| N12 | XAU NY-Open Continuation | faraday VOORSTEL | **geen PREREG** — C-012 FAIL (+0,59 bp) | ≠ N4/N7/N8/N10/AM_FADE |
| N13 | GER40 US-Open Sync | faraday VOORSTEL | **geen PREREG** — U2 FAIL (−3,34 bp; N=92) | ≠ N11 / GER_US_LEAD |
| N14 | US100 NY-Open Pre-Market Mom | faraday VOORSTEL | **geen PREREG** — U2 FAIL (−5,05 bp) | ≠ LUNCH_OPEN / N3 |
| N15–N17 | Venue-ORB UK100/JP225/US* | CTO C-013 | **geen PREREG** — alle FAIL (`64723ff`) | simple ORB-family barred |
| N18 | US500 Overnight Gap Continuation | faraday / CTO C-014 | **STOP FAIL_T** U2 `d1984ed` (gate+stress PASS; t≈0,64); TRIAL_COUNT **447** | ≠ N5 fade; ≠ ORB; year-skew 2023 −12,17 |
| N19 | XAU Overnight Gap Fill | faraday VOORSTEL | **geen PREREG** — C-014 FAIL (+2,03 bp) | ≠ N5 / AM_FADE / N7–N12 |
| N20 | US30 PM Continuation | faraday VOORSTEL | **geen PREREG** U2 FAIL `a1756a7` (−2,26 < 1,35; N=384) | ≠ LUNCH_OPEN; dead candidate |
| N21 | GER40 Afternoon Deviation Fade | faraday VOORSTEL | **geen PREREG** U2 FAIL `a1756a7` (−2,45 < 2,16; N=234) | ≠ N9/N11; dead candidate |
| N22 | UKOILcash London→NY Session MR | faraday VOORSTEL | **geen PREREG** U2 FAIL `a1756a7` (−1,67 < 8,13; N=345) | ≠ S2-USOIL EIA; geen Lon-AM kloon |
| N23 | US100cash Swing 2d TSMOM | faraday VOORSTEL | **geen PREREG** U2 FAIL `a1756a7` (+4,46 < 13,68; N=377; long +10,83) | ≠ B1; geen 2d-TSMOM dunnen |
| N24 | US500cash Mid-Session Lunch Fade | faraday VOORSTEL | **geen PREREG** FAIL +0,35 < 2,34 (N=271) | ≠ N20/LUNCH_OPEN |
| N25 | XAUUSD NY Afternoon Fade | faraday VOORSTEL | **geen PREREG** FAIL +1,14 < 2,49 (N=334) | ≠ AM_FADE/N4–12/N19 |
| N26 | XS 1d Reversal Basket (5) | faraday VOORSTEL | **geen PREREG** FAIL +0,77 < 4,83 (N=581) | D-094a (c); ≠ N23/N2/B1 |
| N27 | AUDUSD H4 MR | faraday VOORSTEL | **geen PREREG** FAIL +1,49 < 3,66 (N=429) | ≠ A5/GS02/B1 |
| N28 | EURJPY Lon→NY mom | faraday VOORSTEL | **geen PREREG** FAIL +2,91 < 3,30 (N=189) | closest miss this cycle |
| N29 | GBPUSD midday fade | faraday VOORSTEL | **geen PREREG** FAIL −1,20 < 2,10 (N=122) | ≠ A5/GS02 |
| N30 | XS 5d momentum basket | faraday VOORSTEL | **geen PREREG** FAIL +0,44 < 4,83 (N=553) | ≠ N26 reversal |
| N31 | XAU Asia→Lon cont | faraday VOORSTEL | **geen PREREG** FAIL −0,01 < 2,49 (N=21) | underpowered |
| N32 | US30 IB breakout cont | faraday VOORSTEL | **geen PREREG** FAIL +0,43 < 1,35 (N=754) | ≠ IB_FADE |
| N33 | USDCAD Lon→NY mom | faraday VOORSTEL | **geen PREREG** FAIL +1,04 < 2,40 (N=94) | ≠ N28 |
| N34 | XAU post-AM-fix MR | faraday VOORSTEL | **geen PREREG** FAIL −2,71 < 2,49 (N=148) | ≠ N8/AM_FADE |
| N35 | US100 Europe→US open cont | faraday | **STOP FAIL_T** U2 `a498a69` (t≈1,22); TRIAL **450** | dead; geen herstart zonder CEO |
| N36 | XAU NY-open drive cont | faraday | **STOP FAIL_T** U2 `a498a69` (stress FAIL); TRIAL **451** | dead; geen herstart zonder CEO |
| N37 | EURUSD H4 trend SMA20 | faraday VOORSTEL | **geen PREREG** U2 FAIL (−0,17 < 1,89; N=627) | ≠ N27 MR/A5/B1 |
| N38 | GBPUSD Lon morning mom | faraday VOORSTEL | **geen PREREG** FAIL −1,35 < 2,10 (N=102) | ≠ N29/S2-GBPJPY |
| N39 | BTC Asia→EU handoff | faraday VOORSTEL | **geen PREREG** FAIL −3,43 < 3,75 (N=132) | ≠ S2-BTC US-open |
| N40 | GER40 mid-morning mom | faraday | **STOP FAIL_T** U2 `5b3db74` (stress FAIL; trial **452**); TRIAL **453** | dead; geen retune |
| N41 | US30 Europe→US open cont | faraday | **STOP FAIL_T** U2 `5b3db74` (NW 1,85; trial **453**) | dead; ≠ N44 clone |
| N42 | NZDUSD Lon morning mom | faraday VOORSTEL | **geen PREREG** FAIL +0,31 < 5,55 (N=132) | ≠ N38 |
| N43 | UKOIL NY-open drive | faraday VOORSTEL | **geen PREREG** underpowered N=139≪150 (mean +12,74≥8,13) | ≠ N22; no threshold shift |
| N44 | US500 Europe→US open cont | faraday VOORSTEL | **BARRED** clone-of-dead N35/N41 | geen screen |
| N45 | ETH Asia→EU handoff | faraday VOORSTEL | **geen PREREG** FAIL −81,8 < 54 (N=61) | ≠ N39/S2b |
| N46 | EURGBP Lon fix ext fade | faraday VOORSTEL | **BARRED** D-098/C-021 | intradag FX ≪50 bp |
| N47 | USDCHF Asia→Lon cont | faraday VOORSTEL | **BARRED** D-098/C-021 | intradag FX ≪50 bp |
| N48 | USDJPY 1d TSMOM | faraday VOORSTEL | **geen PREREG** FAIL +3,23 < 7,08 (N=767) | track 4; dead candidate |
| N49 | UKOILcash TSMOM 20→10 LO | faraday VOORSTEL | **geen PREREG** FAIL +36,4 < 50 (N=55) | D-097 energy |
| N50 | USOILcash TSMOM 20→10 LO | faraday VOORSTEL | **geen PREREG** FAIL +34,2 < 50 (N=54) | D-097 energy |
| N51 | XAU TSMOM 20→5 + SMA200 | faraday VOORSTEL | **geen PREREG** FAIL +8,5 < 50 (N=59) | D-097.2 regime |
| N52 | US100 TSMOM 120→20 LO | faraday VOORSTEL | **underpowered** mean +131 N=21≪150 | C-022 index |
| N53 | USDJPY TSMOM 60→20 LO | faraday VOORSTEL | **underpowered** mean +91,6 N=32≪150 | ≠ N48 |
| N54 | UKOIL winter season LO | faraday VOORSTEL | **underpowered** mean +101,8 N=33≪150 | D-097 seizoen |
| N55 | Index basket TSMOM pooled | faraday VOORSTEL | **geen PREREG** FAIL +72,2 < 138 (N=70) | D-094a c |
| N56 | Energy basket TSMOM pooled | faraday VOORSTEL | **geen PREREG** FAIL +35,3 < 50 (N=109) | D-094a c |
| N57 | FX basket TSMOM pooled | faraday VOORSTEL | **geen PREREG** FAIL +40,7 < 50 (N=78) | D-094a c |
| N58 | AUDJPY LO carry+trend 20→10 | faraday VOORSTEL | **geen PREREG** FAIL +41,66 < 50 (N=50) | D-100 redesign |
| N59 | UKOIL TSMOM high-vol ATR | faraday VOORSTEL | **BARRED** ENERGY clone | C-024/D-100 |
| N60 | XAGUSD 5d bi-dir TSMOM | faraday VOORSTEL | **geen PREREG** FAIL +37,01 < 53 (N=151) | D-097 metals |
| N61 | AUS200 short-only 20→10 | faraday VOORSTEL | **geen PREREG** FAIL −26,05 < 50 (N=45) | D-100 A |
| N62 | GBPJPY LO carry+trend 20→10 | faraday VOORSTEL | **geen PREREG** FAIL +9,75 < 50 (N=55) | D-100 B |
| N63 | EURCHF LO carry+trend 20→10 | faraday VOORSTEL | **geen PREREG** FAIL −43,08 < 50 (N=43) | D-100 B |
| N64 | HK50 short-only 20→10 | faraday VOORSTEL | **underpowered** mean +89,62 N=55≪150 | D-100 A |
| N65 | XAGUSD short-only 5d | faraday VOORSTEL | **geen PREREG** FAIL +39,23 < 50 (N=98) | D-100 C |
| N66 | EURAUD short-only 20→10 | faraday VOORSTEL | **SUBSUMED/dead** (FX_EUR_SHORT FAIL_T) | D-100 B |
| N67 | USDJPY LO L20/H10 | faraday VOORSTEL | **DIAG_FAIL** C-025/C-026 | D-100 B; ≠ MED L60 |
| N68 | GER40 short-only 20→10 | faraday VOORSTEL | **BARRED** family A | C-025 |
| N69 | NZDUSD 10d LO | faraday VOORSTEL | **DIAG_FAIL** C-026 | D-100 B |
| N70 | XAUUSD 5d bi-dir | faraday VOORSTEL | **DIAG_FAIL** C-026 | D-100 C |
| N71 | GBPUSD 10d SO | faraday VOORSTEL | **DIAG_FAIL** C-026 | D-100 B |
| N72 | EURJPY_MED LO L60/H10 | faraday VOORSTEL | **BARRED/STOP** FAIL_T U2 `65a9b23` (TRIAL 455→456) | C-028 L60 FX-med closed |
| N73 | USDCAD LO L60/H10 | faraday VOORSTEL | **BARRED/STOP** C-028 after USDJPY_MED/EURJPY_MED FAIL_T | L60 FX-med closed |
| N74 | USDCHF LO L60/H10 | faraday VOORSTEL | **BARRED/STOP** C-028 after USDJPY_MED/EURJPY_MED FAIL_T | L60 FX-med closed |
| N75 | XAU/XAG ratio MR 3d | faraday VOORSTEL | **DIAG_FAIL** C-029 (10,86≪30,60; N=71) | drop PREREG path |
| N76 | UKOIL Mon→Thu inv-window | faraday VOORSTEL | **DIAG_FAIL** C-029 (−14,90≪50; N=153) | drop PREREG path |
| N77 | FX6 vol-timed XS rev 5d | faraday VOORSTEL | **DIAG_FAIL** C-029 (−2,57≪46,29; N=107) | drop PREREG path |
| N78 | VIX_TERM_VOV US100 1d LO | Lane-B from S2 `b765613c` | **STOP FAIL_COST_GATE** U2 `b998253` (geen trial); TRIAL **456** | dead; C-029 bar VIX_TERM clones |
| N79 | RATE_CURVE→UKOIL LO 5d | faraday VOORSTEL | **UNDERPOWERED** C-029 (126≥50; N=46) | geen PREREG |
| N80 | UKOIL OVN-gap same-day flat | `PREREG_FTMO_N80` | **STOP FAIL_COST_GATE** U2 `454628f` (+7,56 < 8,13; geen trial) | dead; TRIAL **456**; no OVN-gap clones |
| N81 | US100/US500 pair RV 3d | faraday VOORSTEL | **DIAG_FAIL** C-029 (−7,77≪13,74; N=86) | skip |
| N82 | XAGUSD London AM-Fix Fade | faraday VOORSTEL | **DIAG_FAIL** C-030 (−2,91≪15,21; N=311) | drop PREREG path |
| N83 | DXY→US100 opposite intradag | faraday VOORSTEL | **UNDERPOWERED** C-030 (+15,36≥1,98; N=52) | geen PREREG |
| N84 | AUDNZD rate-diff stretch fade | faraday VOORSTEL | **DIAG_FAIL** C-030 (+0,48≪3,18; N=460) | drop PREREG path |
| N85 | US500→US100 lead-lag PM | faraday VOORSTEL | **DIAG_FAIL** C-030 (−7,11≪1,98; N=370) | drop PREREG path |
| N86 | XAU own RV-VoV → 3d MR | faraday VOORSTEL | **DIAG_FAIL** C-030 (−9,27≪15,39; N=96) | drop PREREG path |
| N87 | US30cash opening-gap fade | faraday / CEO PREREG | **STOP FAIL_T** U2 `3a9108e`; TRIAL **457** | dead; no gap-fade clones |
| N88 | EURGBP 5d SO TSMOM | faraday VOORSTEL | **geen PREREG** pre-FAIL `d17573c` | NEW_FAMILY M dead screen |
| N89 | GER40 EU 2h open mom | faraday VOORSTEL | **geen PREREG** pre-FAIL `d17573c` | NEW_FAMILY N dead screen |
| N90 | GBPJPY LO 5d carry+mom | faraday VOORSTEL | **UNDERPOWERED** C-031 (N=113) | no inflate-N |
| N91 | AUDUSD LO 5d carry+mom | faraday VOORSTEL | **DIAG_FAIL** C-031 (−18,59) | drop PREREG path |
| N92 | US100 NY-open 2h mom | faraday / CTO PREREG | **STOP FAIL_T** U2 `b5b59e0`; TRIAL **458** | dead; no NY-2h mom clones |
| N93 | SECTOR_DISP_ROTATION US100 session-flat | faraday PREREG / S2 `fde4a15` | **STOP FAIL_COST_GATE** U2 `b382307` (geen trial); TRIAL **458** | dead; no SECTOR_DISP / XL*→US100 clones |
| N94 | NZDJPY LO 5d carry+mom | faraday VOORSTEL | **geen PREREG** D-092.1 FAIL `n94_n95` (−0,97 < 6,00; N=107) | NEW_FAMILY S dead screen |
| N95 | XAU Lon-AM → NY cont flat | faraday VOORSTEL | **geen PREREG** D-092.1 FAIL `n94_n95` (+1,40 < 2,49; N=226) | NEW_FAMILY T dead screen |
| N96 | CADJPY LO 5d carry+mom | faraday VOORSTEL | **UNDERPOWERED** `n96_n97` (+16,45; N=112≪150) | no inflate-N |
| N97 | AUDCAD LO 5d commodity-XS mom | faraday VOORSTEL | **geen PREREG** D-092.1 FAIL `n96_n97` (−8,87 < 4,50; N=101) | NEW_FAMILY V dead screen |
| N98 | USOIL Lon-AM → US100 NY risk-on lag | faraday VOORSTEL | **DIAG_FAIL** C-034 (−3,79 ≪ 1,98; N=356) | NEW_FAMILY W dead screen; no USOIL→US100 clones |
| N99 | CADCHF LO 5d oil-CHF carry+mom | faraday VOORSTEL | **DIAG_FAIL** C-034 (−4,00 ≪ 6,81; N=103) | NEW_FAMILY X dead screen; no CADCHF-LO clones |
| N100 | EMB_CREDIT_STRESS US100 session-flat | faraday PREREG / S2 `67a9be1` | **STOP FAIL_T** U2 `d09d00a` (TRIAL **458→459**) | dead; no EMB→NDX clones |
| N101 | CRACK_SPREAD_MACRO US100 session-flat | faraday PREREG / S2 `67a9be1` | **STOP FAIL_T** U2 `d09d00a` (TRIAL **459→460**) | dead; no crack/oil-CFD clones |
| N102 | USDCHF LO 5d USD-CHF carry+mom | faraday VOORSTEL | **geen PREREG** D-092.1 FAIL `n102_n103` (+2,94 < 3,03; N=104) | NEW_FAMILY Y dead screen |
| N103 | GER40 Lon-AM → US30 NY industrial lag | faraday PREREG | **STOP FAIL_STRESS** U2 `b9af560` (geen trial); TRIAL **460** | dead; no GER→US30 clones |
| N104 | GBPCHF LO 5d GBP-CHF carry+mom | faraday VOORSTEL | **UNDERPOWERED** D-092.1 `n104_n105` (+10,62; N=98≪150) | NEW_FAMILY AA; geen PREREG |
| N105 | JP225 Tokyo-AM → Lon cont session-flat | faraday VOORSTEL | **geen PREREG** D-092.1 FAIL `n104_n105` (−2,77 < 4,53; N=392) | NEW_FAMILY AB dead screen |
| N106 | EURNZD LO 5d EUR-NZD carry+mom | faraday VOORSTEL | **geen PREREG** D-092.1 FAIL `n106_n107` (+3,45 < 4,11; N=103) | NEW_FAMILY AC dead screen |
| N107 | UK100 Lon-AM → FRA40 afternoon cont | faraday VOORSTEL | **geen PREREG** D-092.1 FAIL `n106_n107` (+3,94 < 5,94; N=255) | NEW_FAMILY AD dead screen |
| N108 | AUS200 Asia-AM → Lon cont session-flat | faraday VOORSTEL | **geen PREREG** D-092.1 FAIL `n108_n109` (−4,86 < 4,38; N=242) | NEW_FAMILY AE dead screen |
| N109 | CHFJPY LO 5d CHF-JPY carry+mom | faraday VOORSTEL | **UNDERPOWERED** D-092.1 `n108_n109` (+19,69; N=122≪150) | NEW_FAMILY AF; geen PREREG |
| N110 | DXYcash Lon-AM → EU-afternoon cont | faraday VOORSTEL | **DIAG_FAIL** C-036 DATA_GAP | no DXY Lon→EU-PM clones |
| N111 | GBPAUD LO 5d GBP-AUD carry+mom | faraday VOORSTEL | **DIAG_FAIL** C-036 (+3,24<4,38; N=104) | no GBPAUD-LO clones |
| N112 | GAS_EQUITY_MACRO → US500 session-flat | S2 `35e38ac` | **STOP FAIL_T** U2 `d1dd863` (TRIAL **460→461**) | dead; no UNG→US500 / gas CFD clones |
| N113 | SILVER_GOLD_RATIO → US500 session-flat | S2 `35e38ac` | **STOP FAIL_COST_GATE** U2 `954680a` (geen trial); TRIAL **461** | dead; no SLV/GLD→US500 clones |
| N114 | HYG_CREDIT_STRESS → US500 session-flat | faraday PREREG | **STOP FAIL_T** U2 `527e46e` (TRIAL **461→462**) | dead; no HYG/LQD/EMB clones |
| N115 | EURUSD Lon-AM → US500 NY macro-beta | faraday VOORSTEL | **geen PREREG** D-092.1 FAIL (−3,43<2,34; N=126) | NEW_FAMILY AJ dead screen |
| N116 | TLT_DURATION_STRESS → US500 session-flat | faraday PREREG | **STOP FAIL_T** U2 `d0aa317` (TRIAL **462→463**) | dead; no TLT→US500 / IEF twin / TIP rewrite |
| N117 | CPER_COPPER_STRESS → US500 session-flat | faraday PREREG | **STOP FAIL_STRESS** U2 `d8b97d0` (geen trial); TRIAL **463** | dead; no CPER/CuAu/copper CFD clones |
| N118 | TIP_REALRATE_STRESS → US500 session-flat | faraday PREREG | **STOP FAIL_T** U2 `9e928af` (t/NW 0,99/0,99; test −4,20); TRIAL **463→464** | NEW_FAMILY AM DEAD; TIP≠TLT |
| N119 | IWM_SMALLCAP_STRESS → US500 session-flat | faraday VOORSTEL | **geen PREREG** D-092.1 FAIL (−0,48<2,34; N=186) | NEW_FAMILY AN dead screen |
| N120 | VNQ_REIT_STRESS → US500 session-flat | faraday VOORSTEL | **geen PREREG — D-092.1 FAIL** (−0,38; N=342) | NEW_FAMILY AO dead; VNQ≠TLT/TIP/ratio |
| N121 | EEM_EM_EQUITY_STRESS → US500 session-flat | faraday VOORSTEL | **geen PREREG — D-092.1 FAIL** (+0,08; N=172) | NEW_FAMILY AP dead; EEM≠EMB |
| N122 | DBC_COMMODITY_STRESS → US500 session-flat | faraday VOORSTEL / CTO C-038 | **DIAG_FAIL** C-038 `1a22e81` (−6,31; N=368) | NEW_FAMILY AQ dead; no DBC→US500 clones |
| N123 | EFA_DM_EXUS_STRESS → US500 session-flat | faraday VOORSTEL / CTO C-038 | **DIAG_FAIL** C-038 `1a22e81` (−2,66; N=201) | NEW_FAMILY AR dead; no EFA→US500 clones |
| N124 | YIELD_CURVE_2S10S → US500 session-flat | S2 `13fe10c` / faraday PREREG | **STOP FAIL_T** U2 `9f00f24` (t/NW 1,72/1,82; test +2,89); TRIAL **464→465** | NEW_FAMILY AS DEAD; no yield-curve twins |
| N125 | DEFENSIVE_CYCLICAL → US500 session-flat twin | S2 `13fe10c` / faraday PREREG | **STOP FAIL_T** U2 `9f00f24` (t/NW 1,22/1,29; test −2,32); TRIAL **465→466** | NEW_FAMILY AT DEAD; no XLU/XLI twins |
| N126 | DBA_AG_STRESS → US500 session-flat | faraday VOORSTEL | **geen PREREG — D-092.1 FAIL** (−6,36; N=380) | NEW_FAMILY AU dead; ≠DBC |
| N127 | EWZ_BRAZIL_STRESS → US500 session-flat | faraday PREREG | **STOP FAIL_T** U2 `3a970c7` (t/NW 0,57/0,50; test +1,85); TRIAL **466→467** | NEW_FAMILY AV DEAD; no EWZ/EEM/EMB/EFA clones |
| N128 | BWX_INTL_TREASURY_STRESS → US500 session-flat | faraday PREREG | **STOP FAIL_T** U2 `62a7718` (t/NW 1,40/1,43; test −2,37); TRIAL **467→468** | NEW_FAMILY AW DEAD; no BWX/TLT/TIP/EMB/yield clones |
| N129 | PPLT_PLATINUM_STRESS → US500 session-flat | faraday VOORSTEL | **geen PREREG — D-092.1 FAIL** (−2,51; N=185) | NEW_FAMILY AX dead; no PPLT/PALL clones |
| N130 | EQW_BREADTH_STRESS → US500 session-flat | faraday PREREG | **STOP FAIL_T** U2 `03ad9da` (t/NW 1,05/1,20; test −3,85); TRIAL **468→469** | NEW_FAMILY AY DEAD; no EQW/breadth clones |
| N131 | DXY_DOLLAR_STRESS → US500 session-flat | faraday PREREG | **STOP FAIL_T** U2 `03ad9da` (t/NW 1,01/1,05; test −1,10); TRIAL **469→470**; **≠ N110** | NEW_FAMILY AZ DEAD; no DXY clones |
| N132 | MTUM_MOM_FACTOR_STRESS → US500 session-flat | faraday VOORSTEL | **geen PREREG — D-092.1 FAIL** (+1,55; N=185) | NEW_FAMILY BA dead; no MTUM clones |
| N133 | GLD_GOLD_HAVEN_STRESS → US500 session-flat | faraday VOORSTEL | **geen PREREG — D-092.1 FAIL** (+0,26; N=361) | NEW_FAMILY BB dead; no GLD/GOLD clones |
| N134 | XLF_FINANCIAL_STRESS → US500 session-flat | faraday VOORSTEL | **geen PREREG — D-092.1 FAIL** (−1,46; N=184; not SECTOR_DISP clone) | NEW_FAMILY BC dead; no XLF clones |
| N135 | QUAL_QUALITY_STRESS → US500 session-flat | faraday VOORSTEL | **geen PREREG — D-092.1 FAIL** (−5,03; N=211; not EQW/IWM clone) | NEW_FAMILY BD dead; no QUAL clones |
| N136 | BRENT_WTI_XS → UKOIL+USOIL session-flat | faraday VOORSTEL | **geen PREREG — D-092.1 FAIL** (−0,51; N=200; not CRACK/OVN clone) | NEW_FAMILY BE dead; no Brent–WTI clones |
| N137 | USDMXN_EM_CARRY_FADE session-flat | faraday VOORSTEL | **geen PREREG — D-092.1 FAIL** (+7,34; N=105; not G10/DXY clone) | NEW_FAMILY BF dead; no USDMXN/USDZAR twins |
| N138 | GER40_UK100_XS session-flat | faraday VOORSTEL | **geen PREREG — D-092.1 FAIL_CLONE** (−4,09; N=178; EU50/UK agree 1,00 cover 0,78) | NEW_FAMILY BG dead; no GER/UK or EU50/UK rewrite |
| N139 | JP225_HK50_ASIA_XS Asia-morning flat | faraday VOORSTEL | **geen PREREG — D-092.1 FAIL** (−1,97; N=240; not N108/N105) | NEW_FAMILY BH dead; no JP/HK Asia XS |
| N140 | XAU_UKOIL_XS session-flat | faraday VOORSTEL | **OPEN** NEW_FAMILY BI gate 10,62 | ≠ N136/N75/N113/N95; D-097 |
| N141 | XAG_UKOIL_XS session-flat | faraday VOORSTEL | **OPEN** NEW_FAMILY BJ gate 23,34 | ≠ N140/N75/N82/N136; D-097 |
| TSMOM_DIV | CEO 12-1 multi-asset TSMOM | ftmo-strategy CEO | **STOP FAIL_COST_GATE** U2 `e5d23c5` | geen trial |
| ENERGY_TSMOM | UKOIL+USOIL L20/H10 LO | CTO C-023 | **STOP FAIL_COST_GATE** U2 `c1499ce` | geen trial |
| IDX_SHORT | US100+US30 short-only L20/H10 | CTO C-024 / D-100 | **STOP FAIL_COST_GATE** U2 `72f40d3` | family A closed |
| FX_EUR_SHORT | EURUSD+EURAUD SO L20/H10 | CTO C-025 | **STOP FAIL_T** U2 `0e04df6` (TRIAL **454**) | geen klonen |
| USDJPY_MED | USDJPY LO L60/H10 | CTO C-026 / D-100 | **BARRED/STOP FAIL_T** U2 `910d6ff` (TRIAL 454→455) | C-028 L60 FX-med family closed |

| P1 | ORB+BTC portfolio | CEO/CTO | **STOP FAIL** C-020 / D-096 (t=0,24; SR=0,20; BTC-leg <0); TRIAL **448** | reserve P1 verbruikt |
| S2-GBPJPY | GBPJPY EU morning mom | grok/strateeg-2 | **STOP FAIL_T** U2 `a498a69` (stress FAIL; TRIAL **449**) | catalog only; geen S2-PREREG rewrite |
| GS01 | Gap-aligned long-only ORB indices | grok/strateeg-1 | PREREG + erratum; **Faraday D-092.1 diagnostic pooled FAIL** (−0,38 < 1,92 bp) | ≠ A1 bidirectioneel; GER40-leg solo +6,21 — geen cherry-pick |
| GS02 | Asian-range fade FX | grok/strateeg-1 | PREREG (geen poort-run) | ≠ A5 breakout; fade/decay-risico |
| S2-XAU | XAUUSD London–NY overlap breakout | grok/strateeg-2 | **STOP** cost-gate `7bac598` | ≠ A1 cash-open |
| S2-GER40 | GER40 Frankfurt open-drive | grok/strateeg-2 | **STOP** cost-gate `7bac598` | A1-overlap was risico |
| S2-USDJPY | USDJPY Tokyo-range London-handoff | grok/strateeg-2 | **STOP** cost-gate `7bac598` | ≠ A5/GS02 |
| S2-USOIL | USOIL EIA-window breakout | grok/strateeg-2 | **STOP** cost-gate (CTO C-004) | hoog RT ≈ 3,34 bp |
| S2-BTC | BTCUSD US-open + US100-gap | grok/strateeg-2 | U2 D-095 stap1 **PASS** N=197 (+15,76 bp); was in P1 (FAIL reserve); solo still power-limited historically | ≠ Q3; P1 dead |
| S2b | BTC+ETH gepoold US-open | grok/strateeg-2 | **STOP** ETH leg FAIL (CTO C-005) | D-091.1; geen parent-wijziging |
| S2-MIDDAY_VWAP | Midday VWAP fade US100/US30 | grok/strateeg-2 | **STOP** poort FAIL `8c7a8e1` (n=3) | ≠ N1/ORB |
| S2-XAU_AM_FADE | XAU London-AM extensie-fade, flat 14:00 | grok/strateeg-2 | **gate PASS** +18,70 bp; **N=12 ≪ 120** watch-only; **S2c closed** | ≠ dode XAU_OVERLAP |
| S2-GER_US_LEAD | GER40 Europe-AM → US open | grok/strateeg-2 | **STOP** poort FAIL U2 `741639e` (C-007) | ≠ N2; ≠ S2-GER40_OPEN |
| S2-VWAP_PB | Morning-trend VWAP pullback | grok/strateeg-2 | **STOP** poort FAIL U2 `741639e` (C-007) | ≠ MIDDAY fade; ≠ N1 |
| S2-IB_FADE | US IB extreme fade | grok/strateeg-2 | **STOP** poort FAIL U2 `b8cf28a` (C-009; −3,54 bp) | ≠ N1/ORB/VWAP |
| S2-LUNCH_OPEN | US lunch open-anchor fade US30/US100 | grok/strateeg-2 | **STOP FAIL_T** U2 `2a4f28e` (gate PASS +4,72; train t=1,14 / test t=0,05) | ≠ MIDDAY/N1/IB_FADE/VWAP_PB; dead set |
| S2c | XAU_AM_FADE + XAG pool | — | **GESLOTEN** CTO D-092.1 pre-screen FAIL (XAG −21,6; pooled −2,24) | geen PREREG |
| index PLM / NR7 / Failed-OR | Faraday D-092.1 candidates | faraday | **geen PREREG** — pre-screen FAIL (`STRATEEG_PRESCREEN_D092.md`) | non-clones geprobeerd |

### 10b. FDR-teller impact (max, na poorten)

- A4/C17, B1, A5, A2: poort FAIL — TRIALS append stop:kostenpoort waar gedaan.  
- **S2-LUNCH_OPEN:** cost-gate PASS → formal trial FAIL_T → TRIALS append; TRIAL_COUNT 445 (U2 `2a4f28e`).  
- **N11 GER40 XETRA ORB:** cost-gate PASS → stress FAIL → formal FAIL_T → TRIALS append; TRIAL_COUNT 446 (U2 `e6b2395` / CTO C-013).  
- **N18 US500 OVN Gap Cont.:** cost-gate PASS → stress PASS → formal FAIL_T → TRIALS append; **TRIAL_COUNT = 447** (U2 `d1984ed` / CTO C-015 / D-093).  
- S2-* overig / N1–N10 / N12–N17 / N19–N34 / N37–N39 / N42–N43 / MIDDAY / GER_US / VWAP_PB / IB_FADE / S2b / S2c: cost-gate, t, pre-screen FAIL of underpowered — geen extra formele trial. **N20–N34 FAIL**; **N37/N38/N39/N42 FAIL**; **N43 underpowered**.  
- **P1 ORB+BTC:** reserve one-shot FAIL → TRIALS append; **TRIAL_COUNT = 448** (CTO C-020 / D-096).  
- **N35/N36/S2-GBPJPY FAIL_T:** U2 `a498a69` → trials 449–451.  
- **N40 FAIL_STRESS_then_FAIL_T** (trial **452**) + **N41 FAIL_T** (trial **453**): U2 `5b3db74` → **TRIAL_COUNT = 453**. Dead-set += N40·N41.  
- **N44 BARRED** (clone EU→US dood). **N46/N47 BARRED** D-098/C-021. **N59 BARRED** ENERGY clone. **N68 BARRED** family A. N45/N48–N58/N60–N65 screened **0 PASS** (N52–N54/N64 underpowered). N66 subsumed; N67/N69–N71 **DIAG_FAIL**. **USDJPY_MED FAIL_T** U2 `910d6ff` (TRIAL 454→455) + **EURJPY_MED FAIL_T** U2 `65a9b23` (TRIAL 455→456): **N72–N74 BARRED/STOP**, L60 FX-med family closed. **C-029:** N75–N77/N81 **DIAG_FAIL**; N79 **UNDERPOWERED**; N78 FAIL_COST_GATE **geen trial**. **N80 STOP FAIL_COST_GATE** U2 `454628f` (**geen trial**). **C-030:** N82/N84–N86 **DIAG_FAIL**; N83 **UNDERPOWERED**. **N87 FAIL_T** U2 `3a9108e` → **TRIAL_COUNT = 457**. N88/N89 D-092.1 pre-FAIL (geen trial). **C-031:** N90 **UNDERPOWERED**; N91 **DIAG_FAIL**; N92 PREREG→**FAIL_T** U2 `b5b59e0` → **TRIAL_COUNT = 458**. Dead += N92 (no NY-2h mom clones). **N93 FAIL_COST_GATE** U2 `b382307` (**geen trial**; TRIAL blijft **458**). Dead += N93 (no SECTOR_DISP clones). **N94/N95 D-092.1 FAIL** (`n94_n95_prescreen`). **N96 UNDERPOWERED** + **N97 FAIL** (`n96_n97_prescreen`). **C-034:** N98/N99 **DIAG_FAIL**. **N100 FAIL_T** (TRIAL **458→459**) + **N101 FAIL_T** (TRIAL **459→460**) U2 `d09d00a` — **TRIAL_COUNT = 460**. Dead += N100/N101 (no EMB/crack clones). D-092.1 **N102 FAIL** + **N103 PASS**→PREREG then **N103 FAIL_STRESS** U2 `b9af560` (**geen trial**; TRIAL blijft **460**). D-092.1 **N104 UNDERPOWERED** + **N105 FAIL**; **N106/N107 FAIL** (`n106_n107`); **N108 FAIL** + **N109 UNDERPOWERED** (`n108_n109`); OPEN screens **N110–N111** (AG/AH) → **C-036 DIAG_FAIL**. Land **PREREG N112/N113** then **N112 FAIL_T** (TRIAL **460→461**) + **N113 FAIL_COST_GATE** (geen trial; TRIAL **461**) U2 `954680a`. D-092.1 **N114 PASS**→PREREG then **N114 FAIL_T** U2 `527e46e` (TRIAL **461→462**); clear N114. D-092.1 **N116 PASS**→PREREG then **N116 FAIL_T** U2 `d0aa317` (TRIAL **462→463**); **N117 PASS**→PREREG then **N117 FAIL_STRESS** U2 `d8b97d0` (geen trial; TRIAL **463**); clear N116/N117. D-092.1 **N118 PASS**→PREREG then **N118 FAIL_T** U2 `9e928af` (TRIAL **463→464**); clear N118. D-092.1 **N120 FAIL** + **N121 FAIL** (`n120_n121`); OPEN **N122–N123** AQ/AR. Absorb S2 `13fe10c`: D-092.1 **N124 PASS**→PREREG + **N125 PASS**→PREREG then **N124 FAIL_T** (TRIAL **464→465**) + **N125 FAIL_T** (TRIAL **465→466**) U2 `9f00f24` — **TRIAL_COUNT = 466**. Clear N124/N125. C-038 **N122/N123 DIAG_FAIL** (stale OPEN cleared). D-092.1 **N126 FAIL** + **N127 PASS**→PREREG (`n126_n127`) then **N127 FAIL_T** U2 `3a970c7` (TRIAL **466→467**); clear N127. D-092.1 **N128 PASS**→PREREG + **N129 FAIL** (`n128_n129`); OPEN **N130–N131** AY/AZ then **N128 FAIL_T** U2 `62a7718` (TRIAL **467→468**); clear N128. D-092.1 **N130 PASS**→PREREG + **N131 PASS**→PREREG (`n130_n131`; N131 ≠ N110). **TSMOM_DIV+ENERGY+IDX_SHORT FAIL_COST_GATE** (geen trial). **D-104** ORB-meta reserve FAIL (CEO). **FX_EUR_SHORT FAIL_T** was TRIAL 454; MED → 456; N87 → 457; N92 → 458; N100/N101 → 460; N112 → 461; N114 → 462; N116 → 463; N118 → 464; N124 → 465; N125 → 466; N127 → **467**; N128 → **468**. Sync U2 `03ad9da` **N130 FAIL_T** (TRIAL **468→469**) + **N131 FAIL_T** (TRIAL **469→470**) — **TRIAL_COUNT = 470**. Clear N130/N131. D-092.1 **N132 FAIL** + **N133 FAIL** (`n132_n133`); OPEN **N134–N135** BC/BD. D-092.1 **N134 FAIL** (−1,46; N=184; not SECTOR_DISP clone) + **N135 FAIL** (−5,03; N=211; not EQW/IWM clone) (`n134_n135`); OPEN **N136–N137** BE/BF. **TRIAL_COUNT stays 470** (no PASS→trial). D-092.1 **N136 FAIL** (−0,51 < 18,15; N=200; not CRACK/UKOIL-OVN clone) + **N137 FAIL** (+7,34 < 8,88; N=105; not G10/DXY clone) (`n136_n137`); OPEN **N138–N139** BG/BH. **TRIAL_COUNT stays 470** (no PASS→trial). D-092.1 **N138 FAIL_CLONE** (−4,09 < 6,42; N=178; EU50/UK agree 1,00 cover 0,78; not N103/N107) + **N139 FAIL** (−1,97 < 12,42; N=240; not N108/N105) (`n138_n139`); OPEN **N140–N141** BI/BJ. **TRIAL_COUNT stays 470** (no PASS→trial).
- N3: gate PASS maar t FAIL — geen TRIALS-append.  
- N9: mean-PASS maar N≪150 — **geen PREREG/trial** (D-092.1 N-eis).  
- S2-XAU_AM_FADE: gate PASS maar power onvoldoende — **geen trial-claim** (watch-only).  
- GS01/GS02: +1 indien formele poort ooit PASS (GS01-test alleen 2024; D-091.5); Faraday diagnostic suggereert FAIL.  
- Manager herbereken BH na elke TRIALS-merge.

### 10c. Welke hypothese is sterker? (evidence uit docs/kosten — geen verzonnen backtests)

**Korte conclusie (2026-10-03 00:46):** **Freeze OFF**. D-092.1 **N138 FAIL_CLONE** (N=178, −4,09<6,42; EU50/UK sign-agree 1,00 cover 0,78; not N103/N107) + **N139 FAIL** (N=240, −1,97<12,42; not N108/N105/N64). No soft-pass. Dead += N138/N139. Filed OPEN **N140–N141** NEW_FAMILY BI/BJ D-097 (XAU–UKOIL XS gate 10,62 / XAG–UKOIL XS gate 23,34; both RTs in COSTS). TRIAL **470**. Ranking: **N140–N141** OPEN > **F2-ORB/A1** ref. Live PREREG **none**. **Geen** U2 wake; Quiet to Sandro.

| Rang (kwalitatief) | Hypothese | Waarom (alleen bestaande docs/kosten/research) |
|--------------------|-----------|-----------------------------------------------|
| 1 (live OPEN screens) | **N140–N141** | NEW_FAMILY BI/BJ D-097; XAU–UKOIL XS / XAG–UKOIL XS session-flat; gates 10,62 / 23,34 (RTs in COSTS); not screened |
| 1 (referentie-EV) | **F2-ORB / A1** | Gerepliceerde bruto-edge; reopen = lange M1 |
| 3 (watch-only) | **S2-XAU_AM_FADE** | +18,70 bp; N=12 |
| 4 (watch / P1-leg) | **S2-BTC** | stap1 PASS N=197; P1 reserve FAIL |
| 5 (verzwakt) | **GS01** | Faraday pooled pre-screen FAIL |
| Dood | A2/A4/A5/B1/N1–N65/**N78**/**N80**/**N87**/**N92**/**N93**/**N100**/**N101**/**N103**/**N106**/**N107**/**N108**/**N110**/**N111**/**N112**/**N113**/**N114**/**N115**/**N116**/**N117**/**N118**/**N119**/**N120**/**N121**/**N122**/**N123**/**N124**/**N125**/**N126**/**N127**/**N128**/**N129**/**N130**/**N131**/**N132**/**N133**/**N134**/**N135**/**N136**/**N137**/**N138**/**N139**/FX_EUR_SHORT/IDX_SHORT/ENERGY/TSMOM_DIV/P1/ORB_META/… | Poort, t, FAIL_T, FAIL_STRESS, FAIL_COST_GATE, DIAG_FAIL |
| Underpowered | **N43**; **N52–N54/N64**; **N79**; **N83**; **N90**; **N96**; **N104**; **N109** | mean PASS N≪150 — geen PREREG |
| Barred | **N44/N46/N47/N59/N68/N72–N74** + VIX_TERM/UKOIL-OVN/ORB-meta/SECTOR_DISP/GER40→US30/AUS Asia→Lon/UK→FRA40 / HYG→US500 / TLT→US500 / CPER→US500 / TIP→US500 / YIELD_CURVE / DEFENSIVE / DBC→US500 / EFA→US500 / EWZ→US500 / BWX→US500 / PPLT→US500 / EQW→US500 / DXY→US500 / MTUM→US500 / GLD→US500 / XLF→US500 / QUAL→US500 / BRENT_WTI / USDMXN / GER40–UK100 / EU50–UK / JP225–HK50 clones | clones / C-021 / ENERGY / family A / L60 / D-104 / N114–N139 |
| Open PREREG / Live PREREG | — | none (N130/N131 cleared FAIL_T) |
| Open screen | **N140–N141** | BI/BJ D-097 (XAU–UKOIL XS / XAG–UKOIL XS) |
| DIAG_FAIL | **N67/N69–N71 / N75–N77 / N81 / N82 / N84–N86 / N91 / N98 / N99 / N110 / N111 / N122 / N123** | C-025…C-038 — geen PREREG |
| Dead cost-gate | **TSMOM_DIV / ENERGY / IDX_SHORT / N78 VIX_TERM / N80 UKOIL OVN-gap / N93 SECTOR_DISP / N113 SILVER_GOLD** | FAIL_COST_GATE; geen trial |
| Dead FAIL_T / FAIL_STRESS | **USDJPY_MED + EURJPY_MED + N87 + N92 + N100 + N101 + N103 + N112 + N114 + N116 + N117 + N118 + N124 + N125 + N127 + N128 + N130 + N131** | U2 `910d6ff` / `65a9b23` / `3a9108e` / `b5b59e0` / `d09d00a` / `b9af560` / `d1dd863` / `527e46e` / `d0aa317` / `d8b97d0` / `9e928af` / `9f00f24` / `3a970c7` / `62a7718` / `03ad9da`; TRIAL **470** |
| Pre-FAIL / screen-FAIL | **N88 / N89 / N94 / N95 / N97 / N102 / N105 / N106 / N107 / N108 / N115 / N119 / N120 / N121 / N126 / N129 / N132 / N133 / N134 / N135 / N136 / N137 / N138 / N139** | D-092.1 FAIL; N138 FAIL_CLONE; geen trial |

**Faraday vs Strateeg-2:** D-092.1 **N136 FAIL** + **N137 FAIL** (not clones). Filed OPEN **N138–N139** BG/BH. Live PREREG **none**. TRIAL **470**. **Geen** U2 wake; Quiet to Sandro.


### 10d. Actiepunten Strateeg (deze branch)

1. ✅ PREREG_FTMO_C17 — bevroren; **STOP** (`43b6ba2`).  
2. ✅ PREREG_FTMO_FX_INTRADAG — bevroren; **STOP** (`ce5abdc`).  
3. ✅ PREREG_FTMO_B1 — bevroren; **STOP** (`18c7996`).  
4. ✅ PREREG_FTMO_A2 — bevroren; **STOP** (`bba5c0c`).  
5. ✅ PREREG_FTMO_N1–N5 — alle **STOP**.  
6. ✅ PREREG_FTMO_N6 — bevroren; **STOP** C-007 (`741639e`).  
7. ✅ VOORSTEL_PRESCREEN_N7/N8 — C-010 FAIL; N9 underpowered / N10 FAIL (C-011).  
8. ✅ PREREG_FTMO_N11 — **STOP FAIL_T** (`e6b2395`); TRIAL_COUNT 446.  
9. ✅ VOORSTEL_PRESCREEN_N12/N13/N14 — D-092.1 FAIL (C-012 / U2 `d4cefff`).  
10. ✅ PREREG_FTMO_N18 — **STOP FAIL_T** (`d1984ed`); TRIAL_COUNT **447**; C-015 / D-093.  
11. ✅ VOORSTEL N19 FAIL (C-014); N20/N21 waren BARRED D-093.2 → **heropend D-094**.  
12. ✅ Catalogus §9/§10 sync post D-093 / N18 FAIL_T / EINDSTAND; nu **D-094 sync**.  
13. ✅ D-092.1 index pre-screens (PLM/NR7/Failed-OR/GS01) — FAIL.  
14. ~~D-093 onderhoud~~ → **D-094 FREEZE OFF** (CEO 08:10 + D-094a 08:25).  
15. ✅ **2026-10-01 08:05:** VOORSTEL N20/N21 status→OPEN; N22 UKOIL track 2; N23 US100 2d TSMOM track 4; geen PREREG (geen cost PASS).  
16. ✅ **2026-10-01 08:12:** N20–N23 → **geen PREREG — U2 D-092.1 FAIL** (`a1756a7`; means −2,26/−2,45/−1,67/+4,46); VOORSTEL N24–N27 OPEN (US500 lunch-fade / XAU NY-PM fade / XS basket / AUDUSD H4 MR); TRIAL_COUNT **447**; geen PREREG.
17. ✅ **2026-10-01 08:28:** Strateeg advanced D-094: screened **N24–N34** (11× D-092.1 FAIL; artifacts `results/R2/n24_n27_prescreen/`, `n28_n31_prescreen/`, `n32_n34_prescreen/`); closest miss N28 EURJPY +2,91 vs 3,30; filed OPEN **N35–N37**; TRIAL_COUNT **447**; geen PREREG; geen U2 ping (CTO: only on PASS→PREREG).
18. ✅ **2026-10-01 09:28:** Sync D-096 P1 FAIL (TRIAL **448**). Land **PREREG N35/N36** (U2 PASS) + **N40/N41** (Strateeg PASS); N37/N38/N39/N42 FAIL; N43 underpowered; OPEN **N44–N45**. C17/FX/B1/A2 remain STOP. §10 vs S2 `6444d30` GBPJPY. U2 ping warranted (PASS→PREREG ×4 + GBPJPY already filed).
19. ✅ **2026-10-01 09:30:** U2 `a498a69`+`5b3db74` TRIAL **453**: **N35/N36/N40/N41/S2-GBPJPY STOP FAIL_T**; N44 BARRED clone; OPEN **N46–N48** (+N45). Geen PREREG; geen U2/Sandro ping (Quiet).
20. ✅ **2026-10-01 11:30:** Sync **D-100** (`615bca0`) + C-024. **BAR N59**; redesign+screen N58/N60–N65 (0 PASS; N64 underpowered); OPEN **N66–N68**; note TSMOM_DIV+ENERGY FAIL_COST + **IDX_SHORT** PREREG. C17/FX/B1/A2 remain STOP. §10 vs S2 `365f704`. Geen PREREG; Quiet / geen U2 ping.
21. ✅ **2026-10-01 12:15:** Sync C-025/C-026 + Manager v74 + CEO 12:15. **FX_EUR_SHORT FAIL_T** (TRIAL **454**); IDX_SHORT FAIL_COST; N66 subsumed; N67 DIAG_FAIL; N68 BARRED; N69–N71 DIAG_FAIL; OPEN **N72–N74**; live PREREG **USDJPY_MED**. C17/FX/B1/A2 remain STOP. §10 vs S2 `4575a4f`. Geen Faraday PREREG; U2 = USDJPY_MED gate (CTO); Quiet.
22. ✅ **2026-10-01 12:40:** **C-028 Lane-B**. No PREREG (no Lane-A survivor). Filed OPEN **N75–N77** NEW_FAMILY (XAU/XAG ratio / UKOIL Mon→Thu inv-window / FX6 vol-timed XS); N72–N74 remain OPEN + freeze further L60 FX forks. TRIAL_COUNT **454**. Quiet / geen U2 ping (no PASS→PREREG).
23. ✅ **2026-10-01 12:42:** C-028 closure after USDJPY_MED **FAIL_T** U2 `910d6ff` (TRIAL 454→455) and EURJPY_MED **FAIL_T** U2 `65a9b23` (TRIAL 455→456). N72–N74 **BARRED/STOP**; USDJPY_MED + EURJPY_MED dead; L60 FX-med family closed. Live OPEN = **N75–N77**; **TRIAL_COUNT 456**; no new VOORSTEL, no PREREG, no agent message.
24. ✅ **2026-10-01 12:47:** **PREREG_FTMO_N78_VIX_TERM_VOV** from S2 `b765613c` (vov10/combo freeze; US100cash; gate **7,83** bp). Ranking: N78 above watches; N75–N77 OPEN; N72–N74 BARRED; TRIAL_COUNT **456**. Source pointer `results/lane_b/VIX_TERM_VOV_SOURCE.md`. Quiet / parent U2 ping.
25. ✅ **2026-10-01 12:55:** U2 `b998253` → **N78 STOP FAIL_COST_GATE** (mean +2,21 ≪ 7,83; **geen trial** — C-029/U2 erratum TRIAL **456** not 457). Filed N79–N81. Quiet.
26. ✅ **2026-10-01 13:20:** Absorb **C-029** (`19dfe4c`): N75–N77/N81 **DIAG_FAIL**; N79 **UNDERPOWERED**; CORN demote; TRIAL **456**. D-092.1 **N80 PASS** → **PREREG_FTMO_N80** OPEN for U2. Filed NEW_FAMILY **N82–N83**. C17/FX/B1/A2 remain STOP. §10 vs S2 `b765613` (VIX promote dead). Parent: **U2 ping** for N80; Quiet to Sandro.
27. ✅ **2026-10-01 13:25:** U2 `454628f` → **N80 STOP FAIL_COST_GATE** (mean +7,56 < 8,13; stress FAIL; years +25,26/−0,46/−3,63; **counts_as_trial=false**; TRIAL **456**). Dead += N80; no UKOIL OVN-gap clones. Filed NEW_FAMILY **N84–N86** (AUDNZD stretch / US500→US100 lead-lag / XAU own VoV MR). OPEN = **N82–N86**. Geen PREREG; Quiet / geen U2 wake.
28. ✅ **2026-10-02 20:19:** Catch-up ff `6c9c1e5`→`45403f1` (+21). Absorb **D-101…D-104** @`8e25e3c` + Manager v83 + **C-030** + **N87 FAIL_T** (TRIAL **457**). Catalog §9/§10: N82/N84–N86 DIAG_FAIL; N83 UNDERPOWERED; N88/N89 pre-FAIL; OPEN **N90–N92**; VOORSTEL status sync. C17/FX/B1/A2 remain STOP. §10 vs S2 `b765613` STALE. Geen PREREG; Quiet / geen U2 wake.
29. ✅ **2026-10-02 20:56:** Sync **N92 FAIL_T** U2 `b5b59e0` (TRIAL **458**) + C-031 N90 UNDERPOWERED / N91 DIAG_FAIL. Land **PREREG_FTMO_N93_SECTOR_DISP_ROTATION** (S2 `fde4a15` cycle_2046; D-100 session-flat; gate **1,98**). Filed OPEN **N94–N95** NEW_FAMILY S/T. Source `results/lane_b/SECTOR_DISP_ROTATION_SOURCE.md`. Dead += N92. Parent: **U2 wake** for N93; Quiet to Sandro.
30. ✅ **2026-10-02 21:05:** Sync **N93 FAIL_COST_GATE** U2 `b382307` (N=309, +0,99 < 1,98; stress FAIL; test −10,99; **geen trial**; TRIAL **458**). Clear live PREREG. D-092.1 **N94 FAIL** + **N95 FAIL** (`results/R2/n94_n95_prescreen/`). Dead += N93 (no SECTOR_DISP clones). Filed OPEN **N96–N97** NEW_FAMILY U/V (CADJPY / AUDCAD). C17/FX/B1/A2 remain STOP. **Geen** U2/Sandro ping (Quiet; no PASS→PREREG).
31. ✅ **2026-10-02 21:22:** Hourly FTMO: D-092.1 **N96 UNDERPOWERED** + **N97 FAIL** (`results/R2/n96_n97_prescreen/`); TRIAL **458**. Filed OPEN **N98–N99** NEW_FAMILY W/X (USOIL→US100 risk-on / CADCHF). BESLUITEN tip still D-104 @`8e25e3c` (upbeat-dirac file tip D-086). C17/FX/B1/A2 remain STOP. §10 vs S2 `fde4a15` STALE. Geen PREREG; Quiet / geen U2 wake.
32. ✅ **2026-10-02 21:56:** Absorb **C-034** N98/N99 **DIAG_FAIL** (0 trials). Land **PREREG_FTMO_N100_EMB_CREDIT_STRESS** + **PREREG_FTMO_N101_CRACK_SPREAD_MACRO** from S2 `67a9be1` cycle_2140 (D-100 session-flat 15:30→21:00 CET; gate **1,98**; both COST_OK). Source pointers `results/lane_b/EMB_CREDIT_STRESS_SOURCE.md` + `CRACK_SPREAD_MACRO_SOURCE.md`. Filed OPEN **N102–N103** NEW_FAMILY Y/Z (USDCHF LO / GER40→US30). TRIAL **458**. Parent: **U2 wake** ×2; Quiet to Sandro.
33. ✅ **2026-10-02 22:05:** Sync U2 `d09d00a` **N100/N101 STOP FAIL_T** (TRIAL **458→460**). Clear live PREREG N100/N101. D-092.1 **N102 FAIL** + **N103 PASS** (`results/R2/n102_n103_prescreen/`) → **PREREG_FTMO_N103_GER40_US30_INDUSTRIAL**. Filed OPEN **N104–N105** NEW_FAMILY AA/AB (GBPCHF LO / JP225 Tokyo→Lon). Dead += N100/N101/N102. Parent: **U2 wake** ×1 (N103); Quiet to Sandro.
34. ✅ **2026-10-02 22:15:** Sync U2 `b9af560` **N103 STOP FAIL_STRESS** (cost PASS; stress FAIL vs 2,025; years +2,29/+10,53/−14,08; **geen trial**; TRIAL **460**). Clear live PREREG. D-092.1 **N104 UNDERPOWERED** + **N105 FAIL** (`results/R2/n104_n105_prescreen/`). Filed OPEN **N106–N107** NEW_FAMILY AC/AD (EURNZD LO / UK100→FRA40). Dead += N103/N105. **Geen** U2/Sandro ping (Quiet; no PASS→PREREG).
35. ✅ **2026-10-02 22:25:** Hourly FTMO: D-092.1 **N106 FAIL** + **N107 FAIL** (`n106_n107`); **N108 FAIL** + **N109 UNDERPOWERED** (`n108_n109`); TRIAL **460**. Filed OPEN **N110–N111** NEW_FAMILY AG/AH (DXY Lon→EU-PM / GBPAUD LO). Dead += N106/N107/N108. BESLUITEN tip D-104 @`8e25e3c`. C17/FX/B1/A2 remain STOP. §10 Faraday > S2 `67a9be1` STALE. **Geen** U2/Sandro ping (Quiet; no PASS→PREREG).
36. ✅ **2026-10-02 22:57:** Absorb **C-036** (`f3cf632`) N110/N111 **DIAG_FAIL** (DATA_GAP / mean<gate). Land **PREREG_FTMO_N112_GAS_EQUITY_MACRO** + **PREREG_FTMO_N113_SILVER_GOLD_RATIO** from S2 `35e38ac` cycle_2240 (D-100 session-flat US500 15:30→21:00 CET; gate **2,34**; both COST_OK; signal-only). Source pointers `results/lane_b/GAS_EQUITY_MACRO_SOURCE.md` + `SILVER_GOLD_RATIO_SOURCE.md`. Filed OPEN **N114–N115** NEW_FAMILY AI/AJ (HYG→US500 / EURUSD→US500). TRIAL **460**. Parent: **U2 wake** ×2; Quiet to Sandro.
37. ✅ **2026-10-02 23:05:** Sync U2 `954680a` **N112 STOP FAIL_T** (TRIAL **460→461**; t/NW 1,07/1,04; test −4,34) + **N113 STOP FAIL_COST_GATE** (+1,60 < 2,34; **geen trial**; TRIAL **461**). Clear live PREREGs. D-092.1 `n114_n115`: **N114 PASS** (+3,81≥2,34; N=371) → **PREREG_FTMO_N114_HYG_CREDIT_STRESS**; **N115 FAIL** (−3,43; N=126). Filed OPEN **N116–N117** NEW_FAMILY AK/AL (TLT_DURATION / CPER_COPPER → US500). Dead += N112/N113/N115. Parent: **U2 wake** ×1 (N114); Quiet to Sandro.
38. ✅ **2026-10-02 23:12:** Sync U2 `527e46e` **N114 STOP FAIL_T** (TRIAL **461→462**; t/NW 0,68/0,71; test −2,16; years −10,03/+7,69/+4,82). Clear N114 live PREREG. Dead += N114 (no HYG/LQD/EMB clones). D-092.1 `n116_n117`: **N116 PASS** (+6,01≥2,34; N=386) → **PREREG_FTMO_N116_TLT_DURATION_STRESS**; **N117 PASS** (+2,89≥2,34; N=152; med −2,21) → **PREREG_FTMO_N117_CPER_COPPER_STRESS**. Filed OPEN **N118–N119** NEW_FAMILY AM/AN (TIP_REALRATE / IWM_SMALLCAP → US500). Parent: **U2 wake** ×2 (N116+N117); Quiet to Sandro.
39. ✅ **2026-10-02 23:16:** Sync U2 `d0aa317` **N116 STOP FAIL_T** (TRIAL **462→463**; t/NW 1,16/1,17; test +3,46) + U2 `d8b97d0` **N117 STOP FAIL_STRESS** (geen trial; TRIAL **463**). Clear N116/N117 live PREREGs. Dead += N116/N117 (no TLT/CPER→US500 / IEF / CuAu). D-092.1 `n118_n119`: **N118 PASS** (+5,38≥2,34; N=359) → **PREREG_FTMO_N118_TIP_REALRATE_STRESS**; **N119 FAIL** (−0,48; N=186). Filed OPEN **N120–N121** NEW_FAMILY AO/AP (VNQ_REIT / EEM_EM_EQUITY → US500). Parent: **U2 wake** ×1 (N118); Quiet to Sandro.
40. ✅ **2026-10-02 23:25:** Sync U2 `9e928af`/`9a00524` **N118 STOP FAIL_T** (TRIAL **463→464**; t/NW 0,99/0,99; test −4,20). Clear N118 live PREREG. Dead += N118 (no TIP→US500 / IEF / TLT rewrite; TIP≠TLT). D-092.1 `n120_n121`: **N120 FAIL** (−0,38; N=342) + **N121 FAIL** (+0,08; N=172). Filed OPEN **N122–N123** NEW_FAMILY AQ/AR (DBC_COMMODITY / EFA_DM_EXUS → US500). **Geen** U2 wake (no PASS→PREREG); Quiet to Sandro.
41. ✅ **2026-10-02 23:56:** Absorb S2 `13fe10c` cycle_2346 (YIELD_CURVE_2S10S + DEFENSIVE_CYCLICAL). D-092.1 `n124_n125`: **N124 PASS** (+8,97≥2,34; N=240) → **PREREG_FTMO_N124_YIELD_CURVE_2S10S**; **N125 PASS** (+5,48≥2,34; N=478) → **PREREG_FTMO_N125_DEFENSIVE_CYCLICAL** (US500 twin per S2 FLAG — not US100 overnight). Source pointers `results/lane_b/YIELD_CURVE_2S10S_SOURCE.md` + `DEFENSIVE_CYCLICAL_SOURCE.md`. Keep OPEN **N122–N123** AQ/AR. TRIAL **464**. Parent: **U2 wake** ×2; Quiet to Sandro.
42. ✅ **2026-10-03 00:10:** Sync U2 `9f00f24` **N124 STOP FAIL_T** (TRIAL **464→465**; t/NW 1,72/1,82; test +2,89) + **N125 STOP FAIL_T** (TRIAL **465→466**; t/NW 1,22/1,29; test −2,32). Clear N124/N125 live PREREGs. Dead += N124/N125 (no yield-curve / XLU-XLI / thr-grid / US100 overnight / TLT-TIP-SECTOR_DISP clones). Absorb C-038 `1a22e81`: **N122/N123 DIAG_FAIL** (stale OPEN at `b236459` cleared; **geen** D-092.1). D-092.1 `n126_n127`: **N126 FAIL** (−6,36; N=380) + **N127 PASS** (+3,54≥2,34; N=208) → **PREREG_FTMO_N127_EWZ_BRAZIL_STRESS**. Filed OPEN **N128–N129** NEW_FAMILY AW/AX (BWX_INTL_TREASURY / PPLT_PLATINUM → US500). Parent: **U2 wake** ×1 (N127); Quiet to Sandro.
43. ✅ **2026-10-03 00:13:** Sync U2 `3a970c7` **N127 STOP FAIL_T** (TRIAL **466→467**; t/NW 0,57/0,50; test N=85 +1,85; netto +2,76). Clear N127 live PREREG. Dead += N127 (no EWZ/EEM/EMB/EFA clones / thr-grid / overnight). D-092.1 `n128_n129`: **N128 PASS** (+6,63≥2,34; N=419; stress informal PASS) → **PREREG_FTMO_N128_BWX_INTL_TREASURY_STRESS**; **N129 FAIL** (−2,51; N=185). Filed OPEN **N130–N131** NEW_FAMILY AY/AZ (EQW_BREADTH / DXY_DOLLAR → US500). Parent: **U2 wake** ×1 (N128); Quiet to Sandro.
44. ✅ **2026-10-03 00:17:** Sync U2 `62a7718` **N128 STOP FAIL_T** (TRIAL **467→468**; t/NW 1,40/1,43; test N=136 −2,37; netto +5,85). Clear N128 live PREREG. Dead += N128 (no BWX/TLT/TIP/EMB/yield clones / thr-grid / overnight). D-092.1 `n130_n131`: **N130 PASS** (+6,68≥2,34; N=220) → **PREREG_FTMO_N130_EQW_BREADTH_STRESS**; **N131 PASS** (+5,08≥2,34; N=413) → **PREREG_FTMO_N131_DXY_DOLLAR_STRESS** (**≠ N110** DXYcash Lon→EU-PM). Parent: **U2 wake** ×2 (N130, N131); Quiet to Sandro.
45. ✅ **2026-10-03 00:24:** Sync U2 `03ad9da` **N130 STOP FAIL_T** (TRIAL **468→469**; t/NW 1,05/1,20; test N=91 −3,85) + **N131 STOP FAIL_T** (TRIAL **469→470**; t/NW 1,01/1,05; test N=146 −1,10; session 15:30–21:00 **≠ N110**). Clear N130/N131 live PREREG. Dead += N130/N131 (no EQW/DXY clones / thr-grid / overnight). D-092.1 `n132_n133`: **N132 FAIL** (+1,55; N=185) + **N133 FAIL** (+0,26; N=361). Filed OPEN **N134–N135** NEW_FAMILY BC/BD (XLF_FINANCIAL / QUAL_QUALITY → US500). **Geen** U2 wake (no PASS→PREREG); Quiet to Sandro.
46. ✅ **2026-10-03 00:29:** D-092.1 `n134_n135`: **N134 FAIL** (−1,46; N=184; not SECTOR_DISP clone) + **N135 FAIL** (−5,03; N=211; not EQW/IWM clone). No PREREG. Dead += N134/N135 (no XLF/QUAL clones / thr-grid / overnight). Filed OPEN **N136–N137** NEW_FAMILY BE/BF (BRENT_WTI_XS gate 18,15 / USDMXN_EM_CARRY_FADE gate 8,88 est.). TRIAL **470**. **Geen** U2 wake; Quiet to Sandro.
47. ✅ **2026-10-03 00:38:** D-092.1 `n136_n137`: **N136 FAIL** (−0,51 < 18,15; N=200; not CRACK/UKOIL-OVN clone) + **N137 FAIL** (+7,34 < 8,88; N=105; not G10/DXY clone). No PREREG. Dead += N136/N137 (no Brent–WTI / USDMXN/USDZAR twins / thr-grid / overnight). Filed OPEN **N138–N139** NEW_FAMILY BG/BH (GER40_UK100_XS gate 6,42 / JP225_HK50_ASIA_XS gate 12,42 est., Asia-morning 03:00–08:00). TRIAL **470**. **Geen** U2 wake; Quiet to Sandro.
48. ✅ **2026-10-03 00:46:** D-092.1 `n138_n139`: **N138 FAIL_CLONE** (−4,09 < 6,42; N=178; EU50/UK agree 1,00 cover 0,78; not N103/N107) + **N139 FAIL** (−1,97 < 12,42; N=240; not N108/N105). No PREREG. Dead += N138/N139 (no GER/UK, EU50/UK, JP/HK Asia XS / thr-grid / overnight). Filed OPEN **N140–N141** NEW_FAMILY BI/BJ D-097 (XAU_UKOIL_XS gate 10,62 / XAG_UKOIL_XS gate 23,34). TRIAL **470**. **Geen** U2 wake; Quiet to Sandro.
