# v31 QA-2/3 — kosten/omloop P-ETF-a per jaar (€ op €80k) en EUR-backtest (ontdekking ≤ 2024)

Transactie = wijziging van de doelpositie van een instrument (maandherweging zonder drempel volgens PREREG_PORT + signaalwissels C02/C52).
Model A = engine (6,5 bp per eenheid omloop = 0,05% commissie + 1,5 bp halve spread); model B = NL-retail vast €3,50/transactie (web-claim €3–3,75) + 1,5 bp.
TER (web-claims): aandelen-ETF 0,07%, obligatie-ETF 0,10%, goud-ETC 0,12%.

| jaar | omloop (× kapitaal) | transacties | kosten A € | kosten B € | TER € | totaal A+TER € | totaal B+TER € |
|---|---|---|---|---|---|---|---|
| 2002 | 3.44 | 78 | 179 | 314 | 24 | 203 | 338 |
| 2003 | 2.01 | 107 | 105 | 399 | 51 | 155 | 449 |
| 2004 | 3.29 | 120 | 171 | 460 | 58 | 229 | 517 |
| 2005 | 3.20 | 113 | 167 | 434 | 62 | 228 | 496 |
| 2006 | 1.92 | 108 | 100 | 401 | 64 | 163 | 465 |
| 2007 | 1.70 | 120 | 88 | 440 | 69 | 157 | 509 |
| 2008 | 2.15 | 78 | 112 | 299 | 22 | 134 | 321 |
| 2009 | 2.61 | 108 | 136 | 409 | 37 | 173 | 447 |
| 2010 | 2.60 | 128 | 135 | 479 | 65 | 200 | 544 |
| 2011 | 2.50 | 116 | 130 | 436 | 60 | 190 | 496 |
| 2012 | 2.46 | 127 | 128 | 474 | 62 | 190 | 536 |
| 2013 | 1.17 | 132 | 61 | 476 | 68 | 129 | 544 |
| 2014 | 1.21 | 130 | 63 | 470 | 69 | 132 | 538 |
| 2015 | 2.71 | 132 | 141 | 495 | 66 | 207 | 561 |
| 2016 | 3.18 | 110 | 166 | 423 | 59 | 224 | 482 |
| 2017 | 0.85 | 127 | 44 | 455 | 69 | 113 | 523 |
| 2018 | 2.72 | 123 | 142 | 463 | 66 | 208 | 529 |
| 2019 | 2.79 | 128 | 145 | 482 | 66 | 211 | 547 |
| 2020 | 3.25 | 128 | 169 | 487 | 61 | 230 | 548 |
| 2021 | 1.58 | 134 | 82 | 488 | 69 | 151 | 557 |
| 2022 | 2.96 | 103 | 154 | 396 | 36 | 190 | 432 |
| 2023 | 2.11 | 127 | 110 | 470 | 61 | 171 | 531 |
| 2024 | 1.75 | 131 | 91 | 479 | 67 | 158 | 547 |

**Gemiddeld per jaar (2002–2024):** omloop 2.36× kapitaal, 118 transacties; kosten A €122 (≈ 0.15%), B €440 (≈ 0.55%), TER €58 (≈ 0.07%) → totaal A+TER ≈ €15/mnd, B+TER ≈ €42/mnd.
In de backtest/forward zitten al: model A + TER 0,07% overal (engine). Extra t.o.v. de engine bij model B: ≈ €26/mnd; bij TER-verschillen ≈ €5/mnd (zie TER-kolom).
Een drempelregel (bv. geen transactie < 1% gewichtsverschil) zou het aantal transacties sterk verlagen — dat is een **andere regel** (niet in PREREG_PORT) en alleen als gevoeligheid te toetsen.

## EUR-backtest van de hele P-ETF-a (ontdekking)

| periode | variant | CAGR EUR | vol | maxDD | boven EUR-cash/jr | €/mnd totaal | €/mnd boven cash |
|---|---|---|---|---|---|---|---|
| 2004–24 | ongehedged | 8.4% | 12.3% | 16.6% | 7.1% | €558 | €472 |
| 2004–24 | gehedged | 6.7% | 6.3% | 11.8% | 5.4% | €446 | €361 |
| 2011–24 | ongehedged | 8.4% | 9.8% | 14.1% | 7.9% | €560 | €525 |
| 2011–24 | gehedged | 5.5% | 6.3% | 11.8% | 5.0% | €370 | €335 |
| 2021–24 | ongehedged | 11.1% | 9.3% | 10.9% | 9.4% | €740 | €624 |
| 2021–24 | gehedged | 5.0% | 6.7% | 11.8% | 3.4% | €335 | €226 |

Backtest-getallen = gerealiseerde premies (regime-afhankelijk, D-070/D-073); vóór live-haircut en box 3. Verwachting: zie VERWACHTING.md / QA_exposures_MC.md.
