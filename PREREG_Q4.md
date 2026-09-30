# PREREG Q4 — machine learning op M5 met walk-forward (vastgelegd vóór berekening, 2026-09-30)

- Data: FTMO-M5 2021–2026, US500, US100, GER40, XAUUSD; alleen bars binnen de eigen cash-sessie (sessies B4).
  Tick-volume zit niet in de export → feature vervalt (gemeld).
- Features per bar (alleen informatie t/m het slot van de bar): rendementen laatste 1/3/12/48 bars; (high−low)/ATR(48);
  afstand tot dag-hoog en dag-laag (in ATR); tijd-van-de-dag sin/cos (minuten sinds sessie-open); dag-van-de-week;
  gap van de dag (open / vorige sessieslot − 1); RSI(2) en RSI(14) op M5; cross-index: rendement laatste 12 bars van US500
  (voor niet-US500) resp. GER40 (voor US500); symbool als categorie.
- Targets (3 vaste horizons = 3 modelvarianten): rendement over de volgende 3, 6 en 12 bars (15/30/60 min), binnen dezelfde sessie.
- Model: LightGBM-regressor, één vaste set (n_estimators 200, learning_rate 0,05, num_leaves 31, min_child_samples 200,
  subsample 0,8 (bagging_freq 1), colsample_bytree 0,8, seed 7). Geen hyperparameter-zoektocht.
- Walk-forward: train 6 maanden → test 1 maand, maandelijks rollend (eerste test 2022-01 i.v.m. opwarming/data 2021);
  **purging/embargo**: trainingsrijen waarvan het target-venster in de testmaand valt, worden verwijderd.
- Handelsregel in de testmaand: drempels = 95e/5e percentiel van de voorspellingen op de trainingsset; long als voorspelling ≥ p95,
  short als ≤ p5; houden = horizon; geen overlap per symbool; kosten = spread instapbar (long) / uitstapbar (short) + commissie
  (indices 0; XAU 0,0006%/kant).
- Rapport per horizon: OOS netto t, bp/trade, N, jaren+, feature-importances (gain).
- **Beslisregel:** OOS netto t ≥ 3, positief in ≥ 4 van de getoetste kalenderjaren, én permutatie-p < 0,01. De permutatietest
  (target geschud binnen elke trainingsperiode, 100 herhalingen) wordt **alleen uitgevoerd als de OOS-t ≥ 3** (anders faalt de regel al).
- Trials +3 (3 horizons) → 401.
