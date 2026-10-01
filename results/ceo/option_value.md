# Optiewaarde van de FTMO-structuur (CEO, 2026-10-01 18:10)
Synthetische dagreeksen, **zero-edge** (mu = 0, kostenlek 0/1/3 bp per dag), `ftmo_ev()`, fee €540, split 80%, herstart na breach (p1/p2 zijn dus "uiteindelijk" over meerdere pogingen, niet per poging). Script `option_value.py`.

| Kosten | Vol/jr | p1 | p2 | overleef 12m | Net EV €/mnd |
|---|---:|---:|---:|---:|---:|
| 0 | 8% | 0,33 | 0,12 | 0,53 | −26 |
| 0 | 15% | 0,82 | 0,56 | 0,15 | +42 |
| 0 | 25% | 1,00 | 0,95 | 0,04 | +382 |
| 0 | 40% | 1,00 | 0,99 | 0,00 | −127 |
| 1 bp/dag | 25% | 0,99 | 0,92 | 0,03 | +268 |
| 3 bp/dag | 25% | 0,99 | 0,90 | 0,01 | +113 |

Lezing: de structuur (verlies = fee, winst = 80%) werkt als een call-optie. Variantie levert positieve EV zonder edge, maar alleen in een middenbereik (~20–30%/jr vol) en niet bij extreme vol; overleving funded is dan laag. Aannames die NIET geverifieerd zijn: fee €540, refund bij eerste payout, payout-ritme, geen "gokregel"-clausule, intradag-drawdown (close-only onderschat breach).
