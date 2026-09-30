# STRATEGIE_CATALOGUS v1 (Strateeg, 2026-09-30 12:45 Amsterdam) — Fase 2, werkstroom R

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
