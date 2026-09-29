# PREREG ronde 2 — vastgelegd vóór het draaien (2026-09-29)

Opdracht: NEXT_STEPS ronde 2. Alleen Python, 2000-01 t/m 2026-09. **Eén vaste parameterset per
familie, geen grid, niets aanpassen na het zien van resultaten.** Alleen bugfixes (bijv.
lookahead) zijn toegestaan en worden dan expliciet gemeld met vóór/na-cijfers.

## Gemeenschappelijk
- Periode: eerste rebalans 2000-01-03 (of zodra 12 maanden + 60 dagen historie per instrument
  beschikbaar is; instrumenten stromen in zodra dat zo is), einde 2026-09-21.
- Rebalans: eerste handelsdag van elke maand, signalen op het slot van de vorige handelsdag,
  uitvoering op het slot van de rebalansdag (1 dag vertraging).
- Volatiliteit: standaarddeviatie van de laatste 60 dagrendementen × √252.
- **Vol-targeting portefeuille:** per instrument ruw gewicht w_i = s_i × (0,10 / σ_i) / N
  (s_i = +1/−1, N = aantal actieve instrumenten). Daarna portefeuille-schaalfactor
  k = 0,10 / σ_p, met σ_p = ex-ante vol van de ruwe portefeuille (huidige gewichten × de laatste
  60 dagrendementen). Bruto hefboom Σ|w| begrensd op 4.
- Kosten:
  - Spread 0,05% per kant over de verhandelde notional (|Δw| × equity) bij elke rebalans.
  - Financiering (CFD-stijl) over de notional per kalenderdag, met de historische korte rente:
    - ETF's/grondstoffen: long betaalt r_USD + 2%/jr, short ontvangt r_USD − 2%/jr.
      r_USD = FRED DTB3 (3-mnd T-bill), voorwaarts gevuld.
    - FX-paren: P&L = spotrendement + renteverschil (basis − quote) × dt − 1,5%/jr × |notional|.
      Buitenlandse rentes: FRED IR3TIB01xxM156N (3-mnd interbancair, maandelijks), met **1 maand
      vertraging** gebruikt (publicatievertraging, geen lookahead), voorwaarts gevuld.
  - Markups gebaseerd op huidige FTMO-swaps (swap_specs_FTMO.csv): index/goud ≈ r + 1–4%, FX ≈ 1,5–2%.
- Rendementen: adjusted close (dividenden inbegrepen) voor ETF's.
- Output: dag-equityreeks (start 100k, geschaald naar €80k voor €/mnd), per-jaar-tabel,
  netto CAGR, vol, Sharpe (excess t.o.v. DTB3), max maand-DD, % jaren positief, episodes
  2000–02, 2008, 2020, 2022, max dagverlies. Referentie: SPY buy & hold op dezelfde 10% vol
  (vaste schaal = 0,10 / gerealiseerde vol SPY over de hele periode).

## Familie 1 — Tijdreeks-trend multi-asset (Moskowitz/Ooi/Pedersen-stijl)
- Universum (12): SPY, EFA, EEM, TLT, IEF, GLD (vóór 2004-11 gespliced met GC=F), USO (vóór
  2006-04 met CL=F), DBC (vóór 2006-02 met ^SPGSCI), EURUSD, USDJPY, GBPUSD, AUDUSD (FX via
  FRED H.10: DEXUSEU, DEXJPUS, DEXUSUK, DEXUSAL).
- Signaal: 12-maands (252 handelsdagen) rendement tot en met vorige slot: > 0 → long (s=+1),
  ≤ 0 → short (s=−1). Voor FX-paren het spot-rendement van het paar.
- Geen varianten (geen 1/3/6-maands, geen flat-optie).

## Familie 2 — G10 FX carry + trend
- Valuta's (10): USD, EUR, JPY, GBP, CHF, AUD, NZD, CAD, NOK, SEK; FX vs USD via FRED H.10
  (DEXUSEU, DEXJPUS, DEXUSUK, DEXSZUS, DEXUSAL, DEXUSNZ, DEXCAUS, DEXNOUS, DEXSDUS).
- Rente: IR3TIB01{US,EZ,JP,GB,CH,AU,NZ,CA,NO,SE}M156N, 1 maand vertraagd. **JPY-rente pas vanaf
  2002-04 beschikbaar → JPY doet vóór 2002-05 niet mee aan de carry-rangschikking** (gemeld).
- Carry-poot: elke maand de 10 valuta's rangschikken op rente; long top-3, short bottom-3
  (USD kan in beide groepen vallen; USD-positie = geen FX-risico, alleen rente). Uitgedrukt als
  posities in de 9 paren vs USD (netto per valuta), gelijk gewogen vóór vol-scaling
  (per poot som |gewicht| = 1, daarna w_i/σ_i-schaling zoals hierboven).
- Trend-poot: 12-maands-tijdreekstrend op de 9 paren vs USD (zelfde regel als familie 1).
- Combinatie: 50% carry-gewichten + 50% trend-gewichten (elk eerst vol-geschaald), daarna de
  hele portefeuille geschaald naar 10% vol (hefboomcap 4).

## Beslisregel (hard, per familie)
Doorgaan naar MT5 alleen als **alle** gelden over ≥ 20 jaar:
1. Sharpe netto ≥ 0,7
2. ≥ 65% van de kalenderjaren positief
3. max DD (maand, en ook dag-equity) < 15% bij 10% vol-target
4. max dagverlies (t.o.v. equity vorige slot) < 5% in de dagreeks

Anders: "afgewezen", RUNLOG bijwerken, stoppen en wachten op beslissing van Sandro.
Een uitkomst veel beter dan de prior (Sharpe > 1) wordt eerst gecontroleerd op lookahead/bugs
vóór rapportage.
