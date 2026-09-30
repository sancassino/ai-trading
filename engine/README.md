# engine/ — gemeenschappelijke dagelijkse backtest-engine (R0, ENGINE_TEMPLATE.md)

- Regel: `catalogus/<id>.py` met `RULE` (id, naam, familie, mechanisme, bron, instrumenten, varianten, optioneel field/start_jaar/max_pos/
  laag_omloop/events/vehicle) en `positions(df, params)` (positie ná slot t, per instrument) of `positions_all(data, params)` (cross-sectioneel).
- Draaien: `python -m engine.run_rule <id> [--vehicle=cfd|etf|future] [--reserve]`. Reserve-OOS (2025-01→) alleen na CEO-vrijgave (D-038).
- Kosten (één plek): cfd = COSTS_FTMO.csv (rondreis per eenheid wijziging) + financiering (FX: historisch 3m-renteverschil − FTMO-opslag;
  overige: huidige FTMO-swap bp/nacht, constant); etf = long-only, TER, spread, cash-rente (DTB3) op niet-belegd; future = overschotrendement
  + rf op kapitaal + rolkosten. Parameters: `VEHICLE_DEFAULT` in run_rule.py, overschreven door `engine/vehicles.csv` (Strateeg).
- Output: results/R/<id>/<fase>_<vehikel>.md; `catalogus/TRIALS.csv` (primaire run = trial met p; vehikelrapporten zonder p), BH-q over alle p-rijen.
- Gates (ENGINE_TEMPLATE §4 + D-037/D-038): kostenpoort bruto ≥ 3× spread/commissie → min(t_NW, t_bootstrap) ≥ 3, H1/H2 > 0, SR ≥ 0,3,
  ≥ 60% 5j-vensters + → BH q ≤ 0,10 → G-benchmark (SR én maxDD beter dan buy-and-hold, zelfde vehikel).
- Regressietest na elke engine-wijziging: `python -m engine.test_b2b` (verwacht t_NW 3,21, SR 0,52).
