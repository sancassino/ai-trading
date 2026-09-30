# VOORSTEL F1 — ORB-verval-heronderzoek (geen trial, FTMO-baseline Fase 3)

## Doel
Bepaal of de ORB-edge (B4a-regel, US500/US100/GER40/XAU) structureel is afgenomen na 2023, of tijdelijk afwezig is door een regime-shift. Dit is **geen nieuwe trial** (B4a is al getest en telde als trial); het is een diagnostische analyse die het startpunt bepaalt voor Fase 3.

## Aanleiding
- FTMO-M5-dataset 2021–26: ORB dag-geclusterde t = **1,81** (N7; eerder 2,93 voor cluster-correctie)
- Uitsplitsing 2021–23 vs 2024–26 was gepland maar nooit expliciet gerapporteerd
- S9-stap 1: vol-regime verklaart de edge **niet** direct (N = 100 vol-tercielen, ruisig)
- Nul-kalibratie (blok-bootstrap) is **niet** toegepast op de FTMO-M5-reeks (alleen op cross-market dagdata)

## Uitvoering (geen trial-teller)
1. **Jaar-voor-jaar rapportage:** bruto-edge per jaar 2021–2026 (bp/trade), trades/jaar, t per jaar (niet gepooled), grafisch
2. **Twee-helft-split:** 2021–23 vs 2024–26; gepoold t en SE per helft; verschil in gemiddelde bp/trade
3. **Nul-kalibratie op FTMO-M5:** stationaire blok-bootstrap (blok ≈ 21 handelsdagen = 1 maand; 1000 replica's); randomiseer dagvolgorde maar bewaar intradag-structuur; meet hoe vaak de gesimuleerde gepoold-t ≥ 1,81 → p-waarde; vergelijk met cross-market (p = 0,46 was voor DD-reductie, dit is voor SR)
4. **Vol-regime verfijnd:** week/maand-realized-vol (ATR14 of 21d-rolling-std) als regime; split in laag/hoog-vol en rapporteer t per kwartiel; aparte rapportage voor 2022 (hoog-vol-jaar) vs 2025–26 (lager vol)
5. **Instrumentvergelijking:** US100 (hoogste edge historisch) vs US500 vs GER40 vs XAU; welk instrument droeg de t van 1,81 het meest?

## Beslisregel (voor Strateeg/CEO, geen selectie-drempel voor trial)
| Uitkomst | Interpretatie | Actie |
|----------|--------------|-------|
| t 2021–23 ≥ 2,0 én t 2024–26 ≥ 1,0 | Edge aanwezig, mogelijk tijdelijk lager | S3 (2011–20) blijft hoogste prioriteit; verwacht FTMO-EV positief |
| t 2021–23 ≥ 2,0 én t 2024–26 < 0,5 | Structureel verval 2024+ | S3 bevestigt ooit-effect; maar FTMO-EV onzeker; herzie horizon |
| Nul-kalibratie p ≤ 0,10 | Reële alpha ook na seasonality-correctie | Versterkt S3-verwachting |
| Nul-kalibratie p ≥ 0,40 | Edge = regime-specifiek (2022-vol), niet structureel | S3 alleen bij vol-conditionering; VOORSTEL aanpassen |

## Instrumenten/data
- `data/m5/` FTMO-M5 2021–2026 (aanwezig)
- B4a-regel `b4_sim.run_orb` (bevroren; geen wijzigingen)
- Analyse-script: nieuw (`analyse/f1_orb_decay.py`), geen trial-telling

## Verwachting
Kans dat 2021–23 significant is én 2024–26 niet → ≈ 40–50% (consistent met S9-bevinding: vol verklaart het niet, maar de val na 2023 is reëel). De analyse geeft een prior voor de S3-beslissing (als S3 bevestigt: welk FTMO-EV is realistisch gegeven het verval?).
