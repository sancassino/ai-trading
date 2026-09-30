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

### 9b. Herindeling catalogus (v3)

| Tier | Regels | Reden FTMO-uitvoerbaar? | Actiestatus |
|------|--------|------------------------|-------------|
| **A — HEROPENEN (hoge prioriteit)** | | | |
| A1 | **ORB/B4a (S3)** — intraday-vlak, US500/US100/GER40/XAU | Swap 0, instrumenten aanwezig, bevroren regel; bevestiging 2011–20 ontbreekt nog | Data-acquisitie (Sandro-actie), dan S3 |
| A2 | **Stocks-in-Play ORB earnings (S2)** — intraday-vlak, FTMO-aandelen-CFD | Eerder mediaan-poort FAIL; heropening D-012 gemiddelde-poort + cluster-t + FTMO-EV | **PREREG BEVROREN**; **wacht US41-M5gz** (NEXT_STEPS v41; enige actieve A/B-spoor) |
| A3 | **Noise-area intradag-momentum (S1)** — trailing EOD-exit, US-indices | Eerder afgewezen (na 2023); heroverwegen met nul-kalibratie en vol-regime; intraday-vlak | F1-heronderzoek, geen extra trial tenzij hypothese nieuw |
| A4 | **FOMC-cyclus (C17)** — even FOMC-weken, D1, index-CFD | Swap-drag hoger dan verwacht (mean nights ≈ 8,6) | **GESTOPT** kostenpoort TRAIN FAIL (`43b6ba2`); geen herstart zonder CEO |
| A5 | **FX-intradag-breakout** — London-open ORB majors | Swap 0; U3-precedent + m5gz-poort FAIL | **GESTOPT** kostenpoort TRAIN FAIL (`ce5abdc`); geen herstart (v41/C-003) |
| **B — ONDERZOEKEN (middel)** | | | |
| B1 | **TSMOM-mix FX (C05 op FX)** | Overnight maand-omloop + swap-drag | **GESTOPT** kostenpoort TRAIN FAIL (`18c7996`); geen nieuwe overnight maand-sleeves |
| B2 | **FX-carry + trendfilter (C12)** | Carry-risicopremie; C12 CAT1 ≈ 0 na kosten → herevalueer alleen met D1-reeksen + FTMO-FX-swaps | Lage prioriteit |
| B3 | **Donchian D1 FX/XAU (C03)** | R4 H4 negatief maar op short reeks; FX D1 = 1 nacht swap; positief scheef | Herevalueer met lange FX-dagreeksen (FRED 1971+) |
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

## 10. Coördinatie Strateeg-1 / Strateeg-2 (D-090, bijgehouden door Strateeg `claude/trusting-faraday-34tsmg`)

*Bijgewerkt: 2026-09-30 23:15 Amsterdam — post A5/S2 STOP (NEXT_STEPS v41)*

### 10a. Overzicht PREREGs (Faraday + Grok Strateeg-1 + Strateeg-2)

| Code | Naam | Branch | Status | Distinct / overlap |
|------|------|--------|--------|--------------------|
| C17 / A4 | FOMC-cyclus index-CFD | faraday | **STOP** poort FAIL `43b6ba2` | overnight swap-drag |
| FX_INTRADAG / A5 | London-open ORB FX | faraday | **STOP** poort FAIL `ce5abdc` | ≠ GS02 fade; U3-familie bevestigd dood |
| B1 | TSMOM-mix FX (C05) | faraday | **STOP** poort FAIL `18c7996` | ≠ B2/C12; geen nieuwe overnight maand-sleeves |
| A2 | Stocks-in-Play ORB earnings | faraday | **PREREG bevroren**; **wacht US41-M5gz** | ≠ A1/GS01 indices; D-012 vs oude S2-mediaan |
| GS01 | Gap-aligned long-only ORB indices | grok/strateeg-1 | PREREG (geen poort-run) | ≠ A1 bidirectioneel; long+gap; index-M5 aanwezig |
| GS02 | Asian-range fade FX | grok/strateeg-1 | PREREG (geen poort-run) | ≠ A5 breakout; fade/decay-risico |
| S2-XAU | XAUUSD London–NY overlap breakout | grok/strateeg-2 | **STOP** cost-gate `7bac598` | ≠ A1 cash-open |
| S2-GER40 | GER40 Frankfurt open-drive | grok/strateeg-2 | **STOP** cost-gate `7bac598` | A1-overlap was risico |
| S2-USDJPY | USDJPY Tokyo-range London-handoff | grok/strateeg-2 | **STOP** cost-gate `7bac598` | ≠ A5/GS02 |
| S2-USOIL | USOIL EIA-window breakout | grok/strateeg-2 | PREREG; **wacht M5** | hoog RT ≈ 3,34 bp; event-N ≈ wekelijks |
| S2-BTC | BTCUSD US-open + US100-gap | grok/strateeg-2 | PREREG; **wacht M5** | ≠ Q3; intraday-flat verplicht (crypto-swap) |

### 10b. FDR-teller impact (max, na poorten)

- A4/C17, B1, A5: poort FAIL — TRIALS append stop:kostenpoort waar gedaan; formele trial-count per PREREG-regel (A5: TRIAL_COUNT ongewijzigd).  
- S2-XAU/GER40/USDJPY: cost-gate FAIL (`7bac598`) — geen TRIALS-append (CTO).  
- A2: +1 indien poort PASS na US41-M5gz.  
- GS01, GS02: +2 indien poorten.  
- S2-USOIL/BTC: +2 indien M5 + poorten.  
- Manager herbereken BH na elke TRIALS-merge.

### 10c. Welke hypothese is sterker? (evidence uit docs/kosten — geen verzonnen backtests)

**Korte conclusie (v41):** het **enige actieve Faraday A/B-spoor** is **A2** (geblokkeerd op US41 equity M5gz). Onder *nog open* sleeves met bestaande index/FX-M5 scoort **GS01 (gap-aligned long-only ORB)** het sterkst op research-fit + dataklaarheid; Strateeg-2-overlevers zijn **S2-BTC / S2-USOIL** (wacht M5). Dood na poort: A4, B1, A5, S2-XAU, S2-GER40, S2-USDJPY.

| Rang (kwalitatief) | Hypothese | Waarom (alleen bestaande docs/kosten/research) |
|--------------------|-----------|-----------------------------------------------|
| 1 (programma-prio) | **A2 SIP earnings** | NEXT_STEPS v41 prio-1; swap=0; D-012 gemiddelde-poort; PREREG dicht — **blokker = US41-M5gz** (niet hypothese) |
| 2 (research-fit, data klaar) | **GS01 gap long-only ORB** | Publieke research: residual ORB-edge geconcentreerd long+gap post-popularization; index RT laag; US500/US100/GER40 al in `data/m5gz/` |
| 3 | **S2-BTC US-open** | Distinct cross-asset impulse; intraday-flat verplicht (crypto-swap); wacht BTC-M5 |
| 4 | **S2-USOIL EIA** | Event-microstructuur, swap=0; RT ≈ 3,34 bp → poort streng; wacht olie-M5 |
| Zwakker / dood | A5 / GS02 / S2-XAU / GER40 / USDJPY / B1 / A4 | A5+U3 poort FAIL op m5gz; S2-XAU/GER40/USDJPY cost-gate FAIL; GS02 fade/decay; B1/A4 overnight dood |

**Faraday vs Strateeg-2 (programma-fit):** Faraday A/B grotendeels dood behalve A2. Strateeg-2 leverde vijf intradag-PREREGs; drie faalden op cost-gate na m5gz — rest (BTC/USOIL) is FDR-diversificatie, niet vervanging van A2. CTO C-003: geen ORB/breakout-clones heropenen zonder mechanisch distinct ontwerp.

### 10d. Actiepunten Strateeg (deze branch)

1. ✅ PREREG_FTMO_C17 — bevroren; **STOP** na poort (U2 `43b6ba2`).  
2. ✅ PREREG_FTMO_FX_INTRADAG — bevroren; **STOP** na poort (U2 `ce5abdc`).  
3. ✅ PREREG_FTMO_B1 — bevroren; **STOP** na poort (U2 `18c7996`).  
4. ✅ PREREG_FTMO_A2 — **bevroren**; run wacht **US41-M5gz** (Uitvoerder-1/Debian).  
5. ✅ Catalogus §9/§10 bijgewerkt post-v41 (deze commit).  
6. Open (niet Strateeg): US41 equity M5gz landings; daarna A2 cost-gate (U2). Geen nieuwe overnight maand-sleeves. Geen A5/S2-XAU/GER40/USDJPY-herstart.
