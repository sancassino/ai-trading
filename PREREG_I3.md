# PREREG I3 — event-drift FOMC / CPI / NFP (vastgelegd vóór berekening, 2026-09-30)

## Datalijst (`events.csv`)
- FOMC: besluitdagen 2021-01..2026-09 van federalreserve.gov/monetarypolicy/fomccalendars.htm (46 datums).
- NFP (Employment Situation) en CPI: releasedatums uit bls.gov/bls/news-release/empsit.htm en cpi.htm, automatisch
  uitgelezen (fouten zichtbaar, bv. 2024-01-15 = feestdag). **Verificatie op data, vooraf vastgelegd:** een datum geldt als
  bevestigd als de US500-M5-bar van 08:30–08:35 ET een range heeft ≥ 2× de mediaan van die bar op de 20 voorgaande
  niet-eventdagen. Niet bevestigd → zoek binnen ±2 handelsdagen; precies één bevestigde buur → gecorrigeerde datum.
  Maanden zonder datum in de bron: NFP zoeken in handelsdag 1–10, CPI in handelsdag 8–16 van de maand (idem ≥ 2×).
  Alle correcties worden in events.csv gemarkeerd. (Mogelijke bias: bevestiging selecteert op grootte van de reactie, niet
  op richting; gemeld.)
## Hypothesen (één parameterset)
- (a) Pre-FOMC-drift (Lucca & Moench 2015): long US500 en US100 van het slot van de laatste sessiebar (15:55–16:00 ET)
  op de handelsdag vóór FOMC tot het slot van de bar 13:55–14:00 ET op de FOMC-dag. Kosten: spread instapbar + FTMO-longswap 1 nacht.
- (b) Post-nieuws-momentum: op NFP- en CPI-dagen richting = teken van de M5-bar 08:30–08:35 ET; instap op het slot van die
  bar in die richting, uitstap op het slot van de bar 09:00–09:05 ET (30 min). Kosten: **2× spread** (slippage-aanname).
- Symbolen US500, US100 (FTMO-M5), 2021–2026.
## Beslisregel per hypothese (gepoold over 2 symbolen)
t ≥ 2,5, zelfde teken in beide helften (2021–2023 / 2024–2026), netto > 0 na de genoemde kosten. Trials +2 → 389.
