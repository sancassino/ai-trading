# PREREG_FTMO_TSMOM_DIV — gediversifieerde time-series momentum, maandelijkse rebalance (CEO, D-097 spoor 1)

**Status:** Pre-registratie 2026-10-01 ~10:00 Europe/Amsterdam, branch `claude/ftmo-trading-strategy-98mplz`. Geen resultaat van deze regel gezien vóór deze commit. Anders dan B1 (6 FX-paren, dood): 40+ instrumenten over 6 klassen, ≥ 10 jaar proxy-historie, vol-targeting.

## 1. Bevroren regel
- **Universum (vooraf):** alle FTMO-symbolen met `10j_plus = ja` in `data/PROXY_MAP_FTMO.csv`, uit de klassen indices, metalen, energie/commodities, agri, FX-majors/crosses. **Geen** aandelen-CFD, geen crypto (<10j), geen exotics. Lijst wordt bevroren in `results/R2/tsmom_div/universe.csv` vóór de run (Uitvoerder-2 commit).
- **Signaal (eind van elke maand, daggegevens proxy):** s = teken van het rendement van maand t−12 t/m t−1 (12-1 momentum). Long als s > 0, short als s < 0.
- **Positie:** inverse-vol gewicht, doelvol per instrument 10%/jr (σ = 60d realized t/m dag t); gelijk risico per instrument; totale bruto-hefboom capped zodat portefeuille-vol ≈ 10%/jr. Houd tot volgende maandeinde, geen stops, geen tuning van lookbacks.
- **Uitvoering:** dag t+1 slot; ontbrekende data = geen positie die maand.
- **Kosten (kostenpoort, per instrument):** rondreis uit `COSTS_FTMO.csv` per rebalance-flip, plus overnight swap per nacht uit `swap_specs_FTMO.csv` volgens richting (long/short apart), swap-tijdvariabiliteit: conservatief +50%-gevoeligheid.

## 2. Mechanisme
Persistente trends door trage informatieverwerking en risico-overdracht (Moskowitz–Ooi–Pedersen 2012, Hurst–Ooi–Pedersen 2017, ≥ 100 jaar bewijs). Bruto per trade (maandhold) is orde 50–300 bp vs kosten 1–10 bp. Bekend risico: trendvolgers verloren in 2023–24; het is een bekende, geen ontdekte, premie.

## 3. Data en toetsvenster
- Ontdekking en kostenpoort: proxy daggegevens 2008-01 → 2024-12 (≥ 10 jaar; indices/metalen/FX volledig, agri/energie waar beschikbaar); swap/kosten uit FTMO-snapshots toegepast als constanten (geen terugwerkende variabiliteit).
- Train/test: 2008–2016 / 2017–2024-12. Reserve 2025-01 → heden: **onaangeroerd** tot CEO-vrijgave.

## 4. Beslisregel (vóór reserve)
1. **Kostenpoort:** mean bruto per maand-trade ≥ 3× mean RT + swap-kosten over train; faalt → STOP, geen trial.
2. **Toets (1 trial):** dag-geclusterd netto t ≥ 2,0 in train én test; netto gemiddelde > 0 in beide helften; ≥ 2/3 van de klassen positief (indices, metalen, energie/agri, FX); N_maand-observaties ≥ 150 pooled.
3. **FTMO-EV:** `engine/ftmo.py` op de gecombineerde dagreeks, `recommend_scale`; rapporteer p_pass, p_survive, net EV, ook met +50% swap.
4. Bij PASS: shortlist → CEO beoordeelt reserve-vrijgave (D-084), Auditor herrekent onafhankelijk. Bij FAIL: telt als 1 trial, geen klonen (geen lookback-variatie, geen universum-selectie achteraf).

## 5. Verwachting
Prior: SR 0,3–0,6 gediversifieerd; EV per maand beperkt (FTMO-schaal), maar structureel. Falen kan: trendvolgers 2011–2019 zwak, hoge swap op carry-nadelige richting, FTMO-index/FX-kosten.

## Erratum (CEO, 2026-10-01 10:35) — openbaarmaking forking paths
CTO's diagnostic screen C-022 (09:53, 1908 solo-TSMOM- en 6 XS-rijen op proxies ≤ 2024-12-31, 0 trials) draaide **vóór** dit PREREG (10:05) op dezelfde ontdekkingsdata. Dit PREREG is een andere, bredere configuratie (12-1 maandelijks, hele universum, geen selectie) en gebruikt de C-022-uitkomsten niet voor selectie, maar het zoekpad is niet schoon. Daarom: (1) universe-keuze blijft de bevroren klassen-lijst, niet de C-022-shortlist; (2) de C-022-familie (1908+6 rijen) telt als extra multiplicity-context in de FDR-rapportage van Auditor; (3) de reserve-toets (2025+) blijft het eigenlijke bewijs; (4) swap-credit-caveat uit C-022 (UKOIL/USOIL long-swap ≈ −5,4…−6,0 bp/nacht) geldt ook hier: rapporteer netto zonder en met swap-subsidie, alfa wordt alleen op bruto-prijsrendement beoordeeld.
