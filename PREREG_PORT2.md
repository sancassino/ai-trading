# PREREG_PORT2 — tweede-generatie-portefeuilles (CEO D-061/D-057) — vastgelegd 2026-09-30 vóór de reserve-run (01-10 12:00) en vóór forward

PREREG_PORT.md blijft onveranderd en bevroren (SHA 9f17d335…). Dit bestand voegt twee portefeuilles toe; na commit niet meer wijzigen (SHA in RUNLOG).
Methoden, kosten, vehikelset, rf, valuta en herweging: **identiek aan PREREG_PORT §2–§3** (verwijzing, geen herdefinitie).

## Portefeuilles
- **P-ETF+** = S_C52L (C52 lang, etf) + S_C02 (C02 basis, etf) + **S_C55 (C55_daa basis, etf)**; methode = **P-ETF-a** (gewichten ∝ 1/σ_60d vertraagd,
  som 1, ongehefeld, maandelijkse herweging op de eerste handelsdag, herwegingskosten 6,5 bp per eenheid). Doet mee in de reserve-run als extra rij
  (zonder selectie erop) en start als extra forward-portefeuille op 2026-10-01.
- **P-breed-2 (informatief)** = alle catalogus-rijen die op 30-09 G-ontdekking haalden en niet expliciet 'geen kandidaat' zijn: S_C02, S_C52B, S_C52L,
  S_C54B, S_C54Q (future), S_C55 (etf), **S_C16 (C16_halloween basis, etf; decay-label), S_C44 (C44_krediet basis, etf; kleine-N-label),
  S_C33 (C33_trend_lowvol basis, future; label: voegt weinig toe aan C05)**; methode = **P-breed** (sleeves 10% vol, gelijk gewogen, portefeuille 10%
  vol, ≤ 3×; opslag rf + 1,5% op geleend etf-deel). C45 niet (haalt G-benchmark niet), C17 niet (haalde G-ontdekking niet).

## Forward
`forward/portfolio2_daily.csv` (zelfde kolommen/regels als forward/portfolio_daily.csv, append-only, tracking-band 1 bp), start 2026-10-01, cron 22:25 UTC
via forward_portfolio.py (tweede sectie, zelfde code-paden als PREREG_PORT).

## Vooraf vastgelegde verwachting
P-ETF+ ≈ P-ETF-a ± diversificatie van C55 (corr met C02 ≈ 0,5–0,7 verwacht); geen verwachting van een structureel hogere alfa boven cash;
oordeelsgetal = alfa boven cash in €/mnd na 30–50% haircut op excess (D-055/D-060), EUR ongehedged én gehedged.
