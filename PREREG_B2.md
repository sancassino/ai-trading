# PREREG B2 — dagfrequente edges op lange data (vastgelegd vóór berekening, 2026-09-29)

Vaste literatuurparameters, geen grid, niets aanpassen na resultaten (bugfixes gemeld met vóór/na).

## Data (keuzes op basis van datakwaliteit, vóór resultaten; zie RUNLOG)
- Yahoo-indices ^GSPC (SPX), ^NDX, ^GDAXI (DAX), ^FTSE, ^N225: prijsindex (zonder dividend —
  conservatief voor longs). DAX pas vanaf 1994 (H/L vóór 1994 onbetrouwbaar).
- Goud: GLD (dividend-/kosten-gecorrigeerde OHLC), vanaf 2004-11 (GC=F-OHLC onbruikbaar, Stooq
  niet bereikbaar). Goud haalt dus zelf geen 25 jaar.
- (c) vereist echte openingskoersen: SPX → SPY (1993+), NDX → QQQ (1999+), DAX (1994+), N225, GLD.
  **FTSE valt af voor (c)** (open = vorige slot in vrijwel elk jaar). Voor (a)(b)(d) de indices zelf.
- Periode 1990-01-01 t/m 2026-09-21 (indicatoren mogen vanaf 1988 opwarmen).

## Strategieën (long-only, per instrument maximaal 1 positie)
- (a) IBS-reversal: IBS = (C−L)/(H−L). Instap op slot als IBS < 0,2. Uitstap op slot zodra
  C > H van de vorige dag, of op het slot van de 5e dag na instap.
- (b) RSI(2) (Wilder): instap op slot als RSI(2) < 10 én C > SMA(200); uitstap op slot als RSI(2) > 70.
- (c1) intraday: elke dag long open→slot. (c2) overnight: elke dag long slot→volgende open.
- (d) turn-of-month: long vanaf slot van de handelsdag vóór de laatste handelsdag van de maand
  t/m slot van de 3e handelsdag van de nieuwe maand (houdt laatste 1 + eerste 3 handelsdagen).

## Kosten
- Spread 0,02% per kant op elke in- en uitstap (c1/c2: elke dag een round-trip).
- Financiering alleen voor posities die over nacht staan: (DTB3 + 2%)/365 per kalendernacht
  (weekend = 3 nachten). Voor niet-US-instrumenten ook DTB3 (vereenvoudiging).

## Evaluatie
- **Primair per strategie (5: a, b, c1, c2, d):** gepoolde portefeuille, per instrument een sleeve
  van 1/N_beschikbaar van het kapitaal (100% notional totaal als alle sleeves positie hebben);
  dagrendement = gemiddelde van de sleeves.
- Secundair (informatief, geen beslisgrond): per instrument op 100% notional.
- **Beslisregel (per strategie, gepoold):** netto t-stat (dagrendementen) ≥ 3 over 1990–2026,
  netto positief in beide helften (1995–2010 en 2011–2026), ≥ 300 trades, max DD < 15%.
- Plus Sharpe, gedeflateerde Sharpe (stats_tools.py, N = 305 en 35), per-jaar-tabel.
- Trials: +5 (primaire strategieën) in TRIAL_COUNT.md.
