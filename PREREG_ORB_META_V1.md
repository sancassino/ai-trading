# PREREG_ORB_META_V1 — ML-filter op de ORB (CEO, 2026-10-02 04:10; D-102/D-103)

**Status:** bevroren vóór enige blik op 2025+. Basis: `results/ceo/orb_meta_stability.py` (trial 7). Trades: `results/b4/B4_a_ORB_trades.csv` (B4a, 7 symbolen).

## Model (bevroren)
- LightGBM-regressie op `net_frac×1e4` (netto bp per trade), clip op 2e/98e percentiel van train.
- Parameters: n_estimators=80, learning_rate=0.02, num_leaves=7, min_child_samples=150, subsample=0.8 (freq 1), colsample_bytree=0.8, reg_lambda=10; gemiddelde van 5 seeds (0–4).
- Features (alleen informatie van vóór de handeldag, uit M5-dagaggregaties): prev_ret, prev_rng, atr20, rng_ratio, r5, r20, gap, gap_atr, dist_hi20, vol5_20, dow, month, symbool (zoals in het script).
- **Training:** alle ORB-trades 2021-01 → 2024-12. Geen hertraining op 2025+.

## Handelsregel (bevroren)
Handel de ORB-trade alleen als de voorspelling ≥ **mediaan van de voorspellingen over 2022–2024 (out-of-sample)**; de drempel wordt vastgelegd in `results/ceo/orb_meta_threshold.json` vóór de reserve-run. Anders overslaan.

## Beslisregel (reserve 2025-01 → 2026-09, éénmalig)
PASS alleen als alle gelden:
1. gefilterd gemiddeld netto bp/trade > 0 én ≥ ongefilterd + 1,0 bp (geselecteerd − niet-geselecteerd, dag-geclusterd t ≥ 1,5);
2. gefilterd SR (dagreeks) ≥ ongefilterd SR;
3. `ftmo_ev` op de gefilterde reeks bij vooraf bepaalde schaal (overleving ≥ 0,85) geeft net EV ≥ ongefilterd bij gelijke overleving;
4. **Auditor** reproduceert de reserve-uitkomst onafhankelijk.
FAIL → filter dood (klonen verboden: geen andere drempel/feature na de reserve-blik); telt als 1 trial.

## Opmerking forking
Trial 7 van het programma; features en drempel zijn vóór de reserve vastgelegd; ORB zelf is eerder al "afgewezen" (B4: t test 1,14, DSR 0,54) — dit PREREG toetst alleen of het filter waarde toevoegt. Reserve is dan verbruikt voor deze hypothese.
