# R7 — premies: C66 VRP-proxy (evidentie, geen trial) en C67 landenrotatie (1 trial) — PREREG_CAT7; ontdekking ≤ 2024

## C66 — VRP-proxy (VIX − gerealiseerde SPX-vol vooruit 21 d; 1990-01-31→2024-11-29, 419 maanden)

- gemiddelde VIX 19.5, gemiddelde RV 15.5, **gemiddelde VRP +4.08 vol-punten**; VRP > 0 in **84%** van de maanden; mediaan +4.63
- **variantieswap-proxy** r = (VIX² − RV²)/VIX² per eenheid variantie-notional: gem. +0.313/mnd, **SR 1.66**, scheefheid -4.7, kurtosis 33, slechtste maand -5.7 (2008-08-29), beste +0.87; 5 slechtste maanden = **15% van de totale winst** (2008-08-29, 2020-02-28, 2015-07-31, 2008-09-30, 2018-01-31)
- corr met SPX-21d-rendement +0.53; met 5%-vaste notional: maxDD 42% (capitaal-verlies als RV ≫ VIX), met 1%: 9%

| periode | n | gem. VRP | % VRP > 0 | SR proxy | slechtste maand |
|---|---|---|---|---|---|
| 1990s | 120 | +5.46 | 92% | 5.19 | -1.0 |
| 2000s | 120 | +2.96 | 77% | 0.92 | -5.7 |
| 2010s | 120 | +3.90 | 84% | 1.44 | -3.8 |
| 2020–24 | 59 | +3.94 | 83% | 1.21 | -4.4 |

| VIX-regime | n | gem. VRP | % VRP > 0 | SR proxy | slechtste maand |
|---|---|---|---|---|---|
| VIX < 15 | 134 | +3.03 | 84% | 1.96 | -3.8 |
| 15–25 | 206 | +4.47 | 85% | 1.96 | -5.7 |
| > 25 | 79 | +4.86 | 81% | 0.81 | -4.4 |

Staarttest: 2008-09/10: proxy -3.4; 2008-10: proxy -0.5; 2011-07: proxy -2.6; 2018-01: proxy -2.6; 2020-02: proxy -4.4. Lezing: het VRP-patroon is robuust (positief in 84% van de maanden, in elk decennium en elk VIX-regime), maar het is een verzekeringspremie met zware linkerstaart: de slechtste maand (−5,7) wist ≈ 18 maanden gemiddelde winst uit; bij 5% vaste notional is de maxDD 42%. De proxy is optimistisch (geen spreads/marge/strike-selectie; VIX-methodiek vóór 2003 anders → SR 5,2 in de jaren 90 is niet serieus te nemen); geen optie-P&L-claim. PutWrite-substitutie wacht op ^PUT/^BXM (R2-007).

## C67 — landenrotatie (top-3 van 12 markten op 12-1m, USD; 2000-05-31→2024-12-31; ontdekking)

| | SR (excess) | CAGR totaal | maxDD |
|---|---|---|---|
| **top-3 rotatie** | +0.12 | 2.3% | 61% |
| gelijk gewogen 12 markten (benchmark) | +0.19 | 3.7% | 61% |

- ΔSR -0.07, ΔmaxDD +1 pp, **NW-t van het verschil -0.97** (eenzijdig p 0.834); TER 0,25%-gevoeligheid: SR +0.11 vs +0.18, t -0.97
- beslissing (vooraf: t ≥ 3 én ΔSR > 0 én ΔmaxDD ≤ 0): **afgewezen**
  - 2000s: top-3 SR +0.08 vs benchmark +0.14 (Δ -0.06)
  - 2010s: top-3 SR +0.19 vs benchmark +0.29 (Δ -0.10)
  - 2020–24: top-3 SR +0.10 vs benchmark +0.16 (Δ -0.07)
