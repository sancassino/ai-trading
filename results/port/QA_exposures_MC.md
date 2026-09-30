# D-075 — werkelijke exposures P-ETF-a, gerealiseerde excess per klasse, Monte-Carlo (geen trial; ontdekking ≤ 2024)

## 1. Gemiddelde exposure (fractie van het kapitaal)

| periode | aandelen | obligaties | goud | cash |
|---|---|---|---|---|
| 2001–24 | 0.40 | 0.29 | 0.11 | 0.20 |
| 2011–24 | 0.43 | 0.33 | 0.13 | 0.11 |
| 2021–24 | 0.45 | 0.26 | 0.13 | 0.16 |

Strateeg-aanname (VERWACHTING §2): aandelen 0,45 · obligaties 0,31 · goud 0,12 · cash 0,12.

## 2. Gerealiseerde excess t.o.v. USD-cash (%/jr, meetkundig) per decennium

| klasse (reeks) | 1990–99 | 2000–09 | 2010–19 | 2020–24 | forward laag/midden/hoog |
|---|---|---|---|---|---|
| aandelen (SPX_TR) | +12.4 | -3.5 | +12.8 | +11.5 | +0.00 / +2.00 / +4.30 |
| obligaties (BOND10_SYN) | +3.1 | +4.1 | +3.5 | -4.0 | -0.50 / +1.00 / +1.80 |
| goud (GOLD_F, future = al excess) | n.v.t. | +16.1 | +3.1 | +11.6 | -1.50 / -0.25 / +1.00 |

## 3. Premie-verwachting met echte exposures (ongehefeld; kosten −0,20%/jr aangenomen)

| exposures | scenario | excess/jr | alfa €/mnd | + EUR-cash (€STR 2.44%) | + USD-cash (4.07%) |
|---|---|---|---|---|---|
| 2001–24 | laag | -0.51% | €-34 | €128 | €237 |
| 2001–24 | midden | +0.86% | €58 | €220 | €329 |
| 2001–24 | hoog | +2.16% | €144 | €306 | €415 |
| 2021–24 | laag | -0.53% | €-35 | €128 | €236 |
| 2021–24 | midden | +0.92% | €61 | €224 | €333 |
| 2021–24 | hoog | +2.32% | €154 | €317 | €426 |

## 4. Monte-Carlo — prior-afhankelijk (v30 QA-1): p(≥ €400) onder twee priors naast elkaar; EUR-cash vast op €STR

| prior | exposures | variant | p(totaal ≥ €400) | p(alfa ≥ €287) | mediaan totaal €/mnd | 5–95% totaal |
|---|---|---|---|---|---|---|
| VERWACHTING-midden (waardering, CAPE ≈ 41) | 2001–24 | parameter, SE 2% | 0.4% | 0.0% | €220 | €109–332 |
| VERWACHTING-midden (waardering, CAPE ≈ 41) | 2001–24 | parameter, SE 3% | 3.8% | 1.2% | €220 | €53–387 |
| VERWACHTING-midden (waardering, CAPE ≈ 41) | 2001–24 | SE 2,5%, corr 0,3 | 3.9% | 1.2% | €221 | €53–388 |
| VERWACHTING-midden (waardering, CAPE ≈ 41) | 2001–24 | SE 2,5% + 10-jr-toeval (vol 6,1%) | 12.0% | 6.7% | €220 | €-33–472 |
| VERWACHTING-midden (waardering, CAPE ≈ 41) | 2021–24 | parameter, SE 2% | 0.7% | 0.1% | €224 | €107–341 |
| VERWACHTING-midden (waardering, CAPE ≈ 41) | 2021–24 | parameter, SE 3% | 4.9% | 1.7% | €224 | €48–399 |
| VERWACHTING-midden (waardering, CAPE ≈ 41) | 2021–24 | SE 2,5%, corr 0,3 | 5.0% | 1.7% | €224 | €48–400 |
| VERWACHTING-midden (waardering, CAPE ≈ 41) | 2021–24 | SE 2,5% + 10-jr-toeval (vol 6,1%) | 13.0% | 7.5% | €224 | €-34–481 |
| historisch lange termijn (geen waarderingscorrectie) | 2001–24 | parameter, SE 2% | 6.2% | 1.1% | €296 | €185–407 |
| historisch lange termijn (geen waarderingscorrectie) | 2001–24 | parameter, SE 3% | 15.4% | 6.5% | €297 | €129–464 |
| historisch lange termijn (geen waarderingscorrectie) | 2001–24 | SE 2,5%, corr 0,3 | 15.4% | 6.6% | €297 | €129–464 |
| historisch lange termijn (geen waarderingscorrectie) | 2001–24 | SE 2,5% + 10-jr-toeval (vol 6,1%) | 25.0% | 15.9% | €296 | €43–550 |
| historisch lange termijn (geen waarderingscorrectie) | 2021–24 | parameter, SE 2% | 9.8% | 2.3% | €308 | €191–425 |
| historisch lange termijn (geen waarderingscorrectie) | 2021–24 | parameter, SE 3% | 19.3% | 9.2% | €308 | €133–483 |
| historisch lange termijn (geen waarderingscorrectie) | 2021–24 | SE 2,5%, corr 0,3 | 19.5% | 9.3% | €308 | €133–483 |
| historisch lange termijn (geen waarderingscorrectie) | 2021–24 | SE 2,5% + 10-jr-toeval (vol 6,1%) | 27.7% | 18.3% | €308 | €50–566 |

**Label: prior-afhankelijk** — geen enkel getal is 'de' kans. Lezing: exposures en premies zijn de enige invoer; het resultaat is zo goed als de premie-aannames (web-claims, VERWACHTING.md). Geen haircut toegepast (premies zijn al forward-verwachtingen, geen backtest).
