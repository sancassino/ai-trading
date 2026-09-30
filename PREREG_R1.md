# PREREG R1 — machine learning op FX-breedte (vastgelegd vóór berekening, 2026-09-30)
- Symbolen (15): EURUSD, GBPUSD, USDJPY, AUDUSD, USDCAD, USDCHF, NZDUSD, EURGBP, EURJPY, GBPJPY, AUDJPY, EURCHF, EURAUD,
  GBPAUD, XAUUSD (referentie). FTMO-M5 2021–2026.
- **Stap 1 — kosten per paar:** mediane spread (bp) in de modeluren + commissie €2,25/lot/kant (XAU €2,00) omgerekend naar bp
  (basisvaluta → EUR met vaste koersen 30-09-2026: USD 0,88, GBP 1,17, AUD 0,58, NZD 0,52, CHF 1,07, CAD 0,64, JPY 0,0059);
  rapport welke paren < 0,8 bp round-trip-halve kosten per kant.
- **Stap 2 — model (Q4-methode):** alleen bars 07:00–17:00 Londen, ma–vr. Features: r1/r3/r12/r48, range/ATR48, afstand tot
  dag-hoog/laag (vanaf 07:00), tijd-van-de-dag sin/cos, dag-van-week, RSI2/RSI14, plus cross-paar: (i) USD-index-proxy = gemiddeld
  12-bar-rendement van de USD tegen EUR/GBP/JPY/AUD/CAD/CHF/NZD (teken zo dat + = USD sterker), (ii) driehoeksafwijking
  log(EURUSD·USDJPY/EURJPY), (iii) 12-bar-rendement van EURUSD (voor EURUSD: GBPUSD); symbool als categorie.
  Targets 3/6/12 bars; LightGBM vaste parameters (Q4); walk-forward 6 mnd → 1 mnd (vanaf 2022-01) met purging;
  **training op elke 4e rij** (geheugen/CPU; test op alle rijen); handelen bij ≥ p95 / ≤ p5 van de trainingsvoorspellingen,
  geen overlap per symbool; kosten = spread instapbar (long) / uitstapbar (short) + commissie × 2.
- Rapport per horizon: gepoolde netto OOS-t, bp/trade, N, effectieve N (unieke tijdstippen), SR na kosten (dagreeks), per-symbool-t.
- **Beslisregel:** gepoolde netto OOS-t ≥ 3 én positief in ≥ 4/5 testjaren; plus per-symbool-t gerapporteerd. Permutatietest
  (100×) alleen als t ≥ 3. Trials +3 → 407.
