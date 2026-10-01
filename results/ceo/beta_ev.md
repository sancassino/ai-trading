# Beta-referentie: long US500-CFD door ftmo_ev() (CEO, 2026-10-01 17:30)
Data SPX daily (^GSPC, close-to-close), swap −4,95%/jr op genoteerde long (FTMO-snapshot), dividend en spread genegeerd, blokbootstrap 21d, 6000 paden, fee €540, split 80%. Script `beta_ev.py <startdatum>`. Close-only drawdown (intradag-trough onderschat → breach te laag geschat).

| Periode | Strategie | Hefboom | Netto/jr | Vol | p1·p2 | Overleef 12m | Net EV €/mnd |
|---|---|---:|---:|---:|---:|---:|---:|
| 2011+ | buy&hold | 0,5 | 4,0% | 8,6% | 0,25 | 0,69 | +21 |
| 2011+ | buy&hold | 0,75 | 6,0% | 12,8% | 0,61 | 0,50 | +128 |
| 2011+ | buy&hold | 1,0 | 8,0% | 17,1% | 0,84 | 0,30 | +241 |
| 2011+ | >200d MA | 1,0 | 4,1% | 11,3% | 0,46 | 0,45 | +75 |
| 2000+ | buy&hold | 0,75 | 2,3% | 14,4% | 0,52 | 0,32 | +64 |
| 2000+ | buy&hold | 1,0 | 3,1% | 19,2% | 0,77 | 0,17 | +143 |
| 2000+ | >200d MA | 1,0 | 2,5% | 10,7% | 0,31 | 0,46 | +36 |

Lezing: €100–200/mnd lijkt op papier haalbaar met gewone marktblootstelling (geen alfa), maar tegen lage overlevingskans en sterke periode-afhankelijkheid (2011+ bullmarkt vs 2000+ met crashes).
