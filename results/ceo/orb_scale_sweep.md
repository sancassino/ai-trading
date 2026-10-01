# F2-ORB: schaalsweep met intradag-trough (CEO, D-102, 2026-10-01 19:00)
Bron `results/f/F2_ORB_daily.csv` (kolom `min_equity` = echte intradag-trough → correcte daily-loss/DD-toets), `engine/ftmo.py`, 6000 paden, fee €540, split 80%. Schaal = hefboom t.o.v. de F2-baseline. Script `orb_scale_sweep.py`.

| Schaal | p1 | p2 | Overleef 12m | P(netto verlies) | Pogingen | Net EV €/mnd |
|---:|---:|---:|---:|---:|---:|---:|
| 1,5 | 0,69 | 0,45 | 0,97 | 0,60 | 1,0 | 55 |
| 2,8 | 0,92 | 0,79 | 0,67 | 0,31 | 1,5 | 285 |
| 4,0 | 0,98 | 0,88 | 0,29 | 0,27 | 2,7 | 357 |
| 5,0 | 0,99 | 0,94 | 0,18 | 0,20 | 3,7 | 505 |
| 6,0 | 1,00 | 0,96 | 0,04 | 0,30 | 6,7 | 405 |
| 8,0 | 1,00 | 0,98 | 0,00 | 0,48 | 14,1 | 183 |
| 10,0 | 1,00 | 0,99 | 0,00 | 0,70 | 26,4 | −150 |

Alleen t/m 2024: schaal 2,8 → €264/mnd (overleef 0,72); schaal 4,0 → €489 (0,44); schaal 6,0 → €602 (0,07).

Lezing: EV piekt rond schaal 4–5 (≈ €360–500/mnd) maar met overleving 0,2–0,3 en 3–4 pogingen; schaal 2,8 geeft ≈ €285/mnd met overleving 0,67. Voorbehoud: ORB-edge zelf is zwak bewezen (t ≈ 1,8); 2025+ valt in deze file (descriptief, niet als test gebruikt); aannames over FTMO-regels onbevestigd.
