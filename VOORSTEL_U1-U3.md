# VOORSTELLEN Uitvoerder U1–U3 (2026-09-30, wachtrij leeg op S3-data) — ter toetsing door Manager/CEO; niets hiervan is uitgevoerd

Criteria D-009: dagelijks vlak/positief scheef, N ≥ 500, data die we hebben of gratis en geautomatiseerd kunnen krijgen (FTMO-MT5).

## U1 — ORB-bevestiging op indices die nooit in de selectie zaten (bevroren B4a-regel) — aanbevolen
- **Logica:** S3 test ORB in de tijd (2011–20) en wacht op Sandro. Dezelfde bevroren regel op **andere markten** (US2000, EU50, FRA40, N25,
  SPN35, JP225, AUS200, HK50; FTMO-M5 2021–26) is een onafhankelijke toets in de breedte: als het mechanisme (order-onbalans/gamma-hedging
  na de cash-open) echt is, moet het ook daar bestaan. Geen enkele parameter wordt aangepast; de instrumenten zijn nooit bekeken.
- **Kostenpoort eerst (geen trial):** M5-export + mediane spread in het OR-venster; alleen instrumenten met rondreis ≤ 1,0 bp (≈ ⅓ van de
  ORB-bruto 2,5–3 bp) gaan door. Verwachting: alleen US2000 en mogelijk JP225/AUS200 halen dit (EU50 nu 2,6 bp, UK100 3,9 bp).
- **Beslisregel (vast):** zoals S3 — dag-geclusterde t ≥ 2,5 én ≥ 0,9 bp/trade = bevestigd in de breedte; t < 1 of ≤ 0,5 bp = verworpen.
  1 trial. Kans ≈ 25% (weinig goedkope instrumenten → weinig power).
## U2 — Risico-sizing van ORB op OR-breedte (portefeuille-/sizing-mechaniek, D-009)
- **Logica:** ORB wordt nu met vaste notional (1/7) gehandeld; het verlies per trade = OR-breedte en varieert sterk. Met vast risico per trade
  (bijv. 0,5% equity / OR-breedte, hefboom ≤ 4×) wordt het dagverlies begrensd en het dip-profiel 'schoner' — R3/Q7 laten zien dat dit onder
  de FTMO-mechaniek zwaarder weegt dan SR. Zelfde trades (B4a), alleen andere grootte → frontier-vergelijking (Q1b) met 1 trial (sizing-keuze).
- **Beslisregel:** alleen informatief voor een eventuele challenge; geen nieuwe edge. Voorwaarde voor gebruik blijft S3 'bevestigd + blijvend'.
## U3 — London-open-ORB op FX-majors (EURUSD, GBPUSD; nieuwe familie)
- **Logica:** de Londense opening (08:00 UK) concentreert institutionele orderstroom in FX, analoog aan de cash-open in indices; rondreis
  0,63–0,70 bp (S0) is lager dan bij indices. Regel = B4a-structuur (OR 30 min vanaf 08:00 Londen, OCO, stop andere kant, uit 17:00 Londen).
- **Risico:** R1 vond op FX-M5 geen voorspelbaarheid (bruto ≈ 0); R4 trendvolgen op FX faalde. Kans ≈ 10%. Familie van 1 (t ≥ 3 in train én test).
