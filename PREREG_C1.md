# PREREG C1 — pairs / stat-arb (vastgelegd vóór berekening, 2026-09-29)

## Paren
- ETF, Yahoo adjusted close (lange data): SPY/DIA, SPY/QQQ, GLD/SLV (vanaf 2006-04), EWG/EWU. Periode 2004-01..2026-09
  (GLD/SLV vanaf start SLV). Wordt gekoppeld aan FTMO-paar: SPY/DIA→US500/US30, SPY/QQQ→US500/US100,
  GLD/SLV→XAUUSD/XAGUSD, EWG/EWU→GER40/UK100.
- FTMO D1 (`*_rates.csv`): US500/US30, US500/US100, GER40/EU50, GER40/FRA40, UK100/EU50, XAUUSD/XAGUSD,
  UKOIL/USOIL, GER40/UK100. Test = 2021-01..2026-09 (eerder beschikbare data alleen als opwarming).
  GER40/EU50, GER40/FRA40, UK100/EU50 en UKOIL/USOIL hebben geen ETF-tegenhanger → kunnen de 15-jaar-eis
  niet halen; alleen gerapporteerd.

## Regel (vast, geen varianten)
- log-prijzen a, b. Op elk slot t: OLS van log a op log b (met constante) over de 60 dagen t−60..t−1 →
  β, α, residu-gemiddelde en -sd; z_t = (log a_t − α − β log b_t − mean) / sd.
- Entry als |z| > 2 (z > 2: short a / long b; z < −2: long a / short b). Exit als |z| < 0,5, stop als
  |z| > 4, of na 20 handelsdagen. Beslissing op slot t, **uitvoering op slot t+1** (geen lookahead).
- Gewichten (log-rendement-ruimte): w_a = ±1/(1+|β|), w_b = ∓β/(1+|β|) → bruto 100% van het kapitaal
  per paar; β vastgezet bij instap.
- Kosten per kant per been: 0,02% (indices/goud; gemeten FTMO-mediaan 0,005–0,013%), 0,05% (zilver, olie,
  EU50/FRA40). Financiering tijdens positie: long betaalt DTB3 + 2%/jr, short ontvangt DTB3 − 2%/jr.
  (FTMO-olie-swap weerspiegelt contango en is niet gemodelleerd — gemeld.)

## Evaluatie en beslisregel (per paar)
- Dagrendementen van de paarportefeuille (0 als flat). t-stat, Sharpe, N trades, max DD, DSR(N = 334).
- **Geslaagd** als: ETF-versie netto t ≥ 3 over ≥ 15 jaar, N ≥ 300 trades, DSR ≥ 0,5, **én** de
  bijbehorende FTMO-versie netto positief in 2021–2026.
- Trials: +8 (8 FTMO-paren; ETF-versie = zelfde regel) → TRIAL_COUNT 334.
