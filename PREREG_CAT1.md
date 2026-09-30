# PREREG CAT1 — catalogusrun 1 (STRATEGIE_CATALOGUS v1, prio 1–2: C01, C02, C03, C05, C07, C12, C17) — vastgelegd vóór berekening, 2026-09-30

**Engine/kosten/gates:** `engine/run_rule.py` (R0; ENGINE_TEMPLATE.md). Data D2 (`data/daily`, QA in DATA_CATALOGUS.md). Ontdekkingsset = alles t/m
**2024-12-31**; reserve-OOS 2025-01→ **onaangeraakt** (alleen voor de shortlist, één keer, met `--reserve`).
Kosten: FTMO-rondreis (COSTS_FTMO.csv) per eenheid positiewijziging (halve rondreis per kant) + financiering per kalendernacht:
FX = historisch 3m-renteverschil (FRED IR3TIB, 1 maand publicatievertraging) − FTMO-opslag geijkt op de huidige swap-specs; indices/goud/zilver =
huidige FTMO-swap in bp/nacht, constant (sjabloon-aanname; dividenden genegeerd). +50%-spreadvariant wordt gerapporteerd.
Instrumenten doen mee vanaf de datum waarop koers én (bij FX) beide rentes bestaan.

**Gates (vast, sjabloon §4 + catalogus §3):** kostenpoort (bruto ≥ 3× (spread + financiering), anders 'stop, geen trial') → dag-t:
min(Newey-West lag 5, blok-bootstrap 21 d) ≥ 3 **én** H1, H2 > 0 **én** netto SR ≥ 0,3 **én** ≥ 60% van de niet-overlappende 5-jaarsvensters
positief **én** N ≥ 500 positie-wijzigingen (maandregels: 'lage omloop' vrijgesteld) → **Benjamini–Hochberg q ≤ 0,10 over alle rijen in
catalogus/TRIALS.csv** → shortlist ≤ 5 → reserve-OOS. Portefeuille = gelijk gewogen gemiddelde over de instrumenten die die dag meedoen.
Trials: +7 (één variant per regel; geen extra varianten) → TRIAL_COUNT 421.

**Universa (vooraf vast, op kostenrang/beschikbaarheid, niet op resultaat):**
- U12 (C01, C05, C07): FX_EURUSD, FX_GBPUSD, FX_USDJPY, FX_AUDUSD, FX_USDCAD, FX_USDCHF (FRED; NZDUSD weg op kosten 1,85 bp), GOLD_F, SILVER_F,
  SPX (→US500), NDX (→US100), DAX (→GER40), N225 (→JP225) = 12.
- Indices (C02, C17): SPX, NDX, DJI, DAX, N225.
- C03: 6 FX van U12 + GOLD_F (7; catalogus noemde '8 FX + goud', maar NZDUSD valt af op kosten → vermeld).
- C12: de 6 FX-paren van U12 (valuta's EUR, GBP, JPY, AUD, CAD, CHF tegen USD).

**Regels (exact, 0 vrije parameters; beslissing op slot van de laatste handelsdag van de maand = 'maandeinde', positie vanaf dat slot):**
- **C01 TSMOM 12m:** per instrument teken van het 252-daagse rendement (slot/slot); gewicht = 0,10 / σ60 (σ60 = jaarvolatiliteit uit 60
  dagrendementen), afgekapt op 3; maandelijks herzien; lang bij > 0, kort bij < 0.
- **C02 Faber SMA-10m:** lang (gewicht 1) als het maandeindslot > gemiddelde van de laatste 10 maandeindsloten, anders geen positie.
- **C03 Donchian 55/20 D1:** lang als slot > hoogste slot van de 55 vorige dagen, kort als < laagste; uit bij slot < laagste slot 20 d (lang)
  / > hoogste slot 20 d (kort) óf bij een 2×ATR-stop (ATR = gemiddelde |Δslot| over 20 d, gemeten vanaf de instapkoers; slotbasis omdat FRED-FX
  geen high/low heeft); dagelijks; gewicht 1.
- **C05 TSMOM-mix 1/3/12m:** positie = gemiddelde van de tekens van het 21-, 63- en 252-daagse rendement × 0,10 / σ60 (afgekapt op 3); maandelijks.
- **C07 cross-asset-momentum 12-1:** maandeinde; rangschik U12 op rendement van dag −252 t/m −21; lang top-3, kort bottom-3 (gewicht ±1 elk;
  andere 6 nul); alleen instrumenten met volledige historie tellen mee (bij < 6 beschikbare: geen positie).
- **C12 carry + trendfilter (FX):** maandeinde; carry van valuta X = i_X − i_USD (3m, FRED); rangschik de 6 valuta's; top-3 → lang X/USD
  (bij USDJPY/USDCAD/USDCHF: kort het paar) **alleen** als het 63-daagse rendement van X tegen USD > 0; bottom-3 → kort X/USD alleen als dat
  rendement < 0; anders geen positie. Gewicht 1.
- **C17 FOMC-cyclus (Cieslak–Morse–Vissing-Jorgensen):** FOMC-datums uit fomc_dates_1994_2020.txt + events.csv (2021→); dag 0 = besluitdag;
  lang indices (gewicht 1) op handelsdagen −1 t/m +4, +9 t/m +14, +19 t/m +24, +29 t/m +34 (weken 0, 2, 4, 6 in FOMC-tijd; telling in
  handelsdagen van SPX sinds dag 0, begin bij de laatste FOMC vóór de datum); anders geen positie; periode 1994→.

**Verwachting (Strateeg):** 0–2 overleven de lange dagdata. Swap-drag van lange index-posities (5–8%/jr) weegt zwaar bij C02/C17.
