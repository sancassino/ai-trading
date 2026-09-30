# ENGINE_TEMPLATE — sjabloon per catalogusregel (Manager, 2026-09-30 12:37) — bindend voor R-werkstroom

## 1. Eén engine, één kostenmodel
- Alle catalogusregels lopen door **dezelfde** code (`engine/run_rule.py`) met een regel-definitie (YAML/dict), nooit ad-hoc scripts. Input = data uit `data/` (D2 daily / D1 intraday) volgens `data/DATA_CATALOGUS.md`; output in `results/R/<regel-id>/`.
- Kostenmodel: rondreis-bp per instrument/uur uit `COSTS_FTMO.csv` (S0) + swap per nacht (`swap_specs_*.csv`); voor pre-FTMO-jaren dezelfde bp-aanname (vermeld) + variant +50%. Financiering DTB3+markup waar van toepassing. Eén plek in code, geen per-regel afwijkingen.
- Data-QA (D3) vooraf: gaten, splits, DST/sessies, overlap-check met FTMO; geen run op ongecontroleerde data.

## 2. Regel-definitie (vooraf, in `catalogus/<id>.yaml` + korte PREREG-tekst)
`id, naam, familie, mechanisme (economisch, 2 zinnen), bron (paper), instrumenten (vast, kostenrang, niet op resultaat gekozen), horizon, regel (exact; ≤ 4 varianten; geen grids), verwachte bruto bp vs kosten, verwachte scheefheid/dagelijks-vlak ja/nee, data-eis, ontdekkingsperiode (pre-2025-01), reserve-OOS (2025-01→heden, alleen voor shortlist), beslisregel (gate-lijst §4)`.

## 3. Standaard-output per regel (identiek)
Netto SR (+CI), **dag-geclusterde t** (of blok-bootstrap 21 d), t per helft en per jaar, N trades/dagen, skew, dagdip (max/P99), max drawdown, +50% spread-variant, correlatie met bestaande sleeves (ORB, RSI(2), overig), rendement per regime (vol-tercielen, bull/bear), FTMO-dagverlies-check (Q1b-mechaniek) alleen voor shortlist.

## 4. Gates (vooraf, vast; CEO kan wijzigen, Manager niet)
G-kosten (bruto ≥ 3× rondreiskosten) → G-ontdekking (dag-geclusterd netto t ≥ 3 over pre-2025 én in beide helften positief; N ≥ 500 trades of ≥ 100 events) → **FDR over de hele catalogus (BH, q = 0,10) + DSR** → shortlist ≤ 5 → G-reserve (2025-01→heden: teken positief, effect ≥ 50%; één keer kijken) → G-portefeuille (corr < 0,5 met bestaande sleeves; SR-bijdrage) → FTMO-mechaniek (Q1b) → Auditor (D-005).

## 5. Trial-teller (`TRIAL_COUNT.md` + `catalogus/TRIALS.csv`)
Kolommen: `datum, regel-id, variant, dataset, ontdekking/reserve, netto SR, t_geclusterd, p, FDR-q, beslissing`. Elke gedraaide variant = 1 rij (ook afgewezen). Reserve-OOS wordt per regel maximaal één keer geopend en gelogd. FDR-berekening wordt bij elke run over **alle** rijen herberekend.

## 6. Werkwijze
Strateeg levert per week 3–5 catalogusregels als bundel (één PREREG-sjabloon); Uitvoerder draait ze in één batch met dezelfde engine; Manager toetst QA (lookahead, kosten, clustering) en meldt blokkades schriftelijk; CEO beslist over prioriteit/gates.


## Wijziging 2026-09-30 (D-038/D-045, Manager)
- G-benchmark: netto SR én maxDD/Calmar beter dan buy-and-hold/60-40 van dezelfde reeks per vehikel; FTMO-dagverlies niet meer verplicht.
- Vehikel `future`: FX = spot + renteverschil, doorlopende futures zonder rf-aftrek, index/obligatie r − rf. SR/t voor etf/future op overschotrendement (x − rf).
- Reserve-OOS: één gezamenlijke run na bevroren shortlist en vooraf gecommitte portefeuilleregel, vrijgave CEO. Ongeldige TRIALS-rijen ('telt niet') blijven buiten BH.
