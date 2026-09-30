# C61 — testspecificatie voor de compounding-/padafhankelijkheidstest (Strateeg, 2026-09-30 16:30; voor Uitvoerder-2, D-063; geen trial)
Doel: vóór C61 (long SPX boven 10-mnd-SMA, anders −1× via UCITS-inverse-ETF) als regel geteld wordt, vaststellen of een dagelijks-gereset −1×-product op houdperiodes van 1–10 maanden het gewenste short-profiel repliceert.
## 1. Constructie van de inverse-reeks (engine, per dag)
x_inv,t = −r_SPX,t + rf_t − TER/252 − s_swap/252   (r in dagrendement; 'rf' = collateral-rente; TER 0,50% (web-claim); s_swap = swap-spread, onbekend → gevoeligheid 0 / 0,5 / 1,0%/jr). Dagelijks compounden: V_T = Π(1 + x_inv,t). **Niet** −(SPX-periode-rendement). Gebruik SPX_TR (total return) voor r_SPX; rf uit engine.rf_on (USD) en €STR (EUR-variant).
## 2. Te rapporteren (één tabel, SPX 1928→2024)
(a) **Replicatiefout per houdperiode H ∈ {21, 63, 126, 210 handelsdagen}:** E_H = V_H − (1 − R_H + rf-carry) met R_H = SPX-periode-TR; toon mediaan, P5, P95, en uitsplitsing naar vol-regime (20d-vol-tercielen) en naar richting (markt +/− over H). Verwachte drift: ≈ −σ²·H/252 (variantie-verval), dus 20% vol ≈ −4%/jr, 35% vol ≈ −12%/jr.
(b) **Bearmarkt-episodes apart:** 1929–32, 1973–74, 2000–02, 2008, 2020-03, 2022: wat leverde −1× daadwerkelijk vs een ideale −1× (continu gehedged op maandbasis)? (De trend-regel schakelt pas na het signaal; meet dus óók *vanaf signaaldatum*.)
(c) **C61 zelf (na (a)/(b)):** twee uitvoeringen: (i) inverse-ETF als short-leg met bovenstaande dagelijkse compounding, (ii) cash als flat-leg (= C02 met cash). Rapporteer SR, maxDD, corr met C02/C52/SPX, en ΔSR/ΔDD op P-ETF-a/P-ETF+ (vehikelrapport; telt als 1 trial voor C61 totaal).
## 3. Beslisregel (vooraf)
- **Replicatie faalt** als de mediane |E_H| > 1,5%-punt voor H ≤ 126 in alle vol-tercielen, of als het gemiddelde verval in het hoogste vol-terciel > 8%/jr → C61 **niet** als UCITS-sleeve (alleen als CFD/future, dan retail-kosten); geen conclusie op SR.
- **Edge-toets** pas bij replicatie-OK: min(NW, bootstrap) t ≥ 3, BH-q ≤ 0,10 (436 trials), ΔSR op P-ETF-a ≥ +0,05 én corr met C02 ≤ 0,5 in de ontdekkingsset.
## 4. Waarschuwingen
(1) De inverse-ETF heeft ≈ 10–20 jr echte historie; de SPX-synthetische reeks is een model — valideer het model tegen een echte inverse-ETF-koers als er een reeks is (Yahoo: XSPS.L/XSPD.L e.d., licentie/voorwaarden Yahoo) voor de overlap. (2) De rf-collateral-aanname is gunstig bij hoge rente; toon resultaat ook met rf = 0 (conservatief). (3) Winnaarsvloek: C61 is bedacht ná het zien van C02-resultaten; behandel als exploratief.
