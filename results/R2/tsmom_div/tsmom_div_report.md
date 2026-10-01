# PREREG_FTMO_TSMOM_DIV — cost-gate + formal train/test

Universe freeze: `/workspace/ai-trading-u2/results/R2/tsmom_div/universe.csv` (n=56, loaded=56).
Train 2008–2016 / test 2017–2024-12. Reserve 2025→ **untouched**.
Rule: 12-1 TSMOM monthly, inv-vol 10%/yr equal-risk, port-vol cap 10% via 1/√N diagonal scale.

**Uitkomst: FAIL_COST_GATE** (counts_as_trial=False)

## Train

```json
{
  "label": "train",
  "ok": true,
  "N_days": 2561,
  "N_month": 107,
  "N_trades": 5962,
  "mean_bruto_bp_unit": -5.7334,
  "mean_cost_bp_unit": 45.1235,
  "mean_cost_stress_bp_unit": 66.6836,
  "gate_3x": false,
  "stress_3x_swap50": false,
  "mean_netto_daily": -0.00070373,
  "mean_bruto_daily": 0.00010048,
  "t_day_clust_netto": -2.0007,
  "t_nw_L5_netto": -1.8789,
  "mean_netto_h1": -0.0007321,
  "mean_netto_h2": -0.00067546,
  "class_mean_netto": {
    "indices": -0.0001685,
    "metalen": -7.264e-05,
    "energie_agri": -0.00028424,
    "fx": -0.00017834
  },
  "n_pos_class": 0,
  "n_class": 4,
  "class_rule_pass": false
}
```

## Test

```json
{
  "label": "test",
  "ok": true,
  "N_days": 2282,
  "N_month": 95,
  "N_trades": 5318,
  "mean_bruto_bp_unit": -2.6746,
  "mean_cost_bp_unit": 43.068,
  "mean_cost_stress_bp_unit": 63.5979,
  "gate_3x": false,
  "stress_3x_swap50": false,
  "mean_netto_daily": -0.00073428,
  "mean_bruto_daily": 0.00016925,
  "t_day_clust_netto": -2.3903,
  "t_nw_L5_netto": -2.1314,
  "mean_netto_h1": -0.00117007,
  "mean_netto_h2": -0.00029774,
  "class_mean_netto": {
    "indices": -0.0002635,
    "metalen": -9.679e-05,
    "energie_agri": -0.0001264,
    "fx": -0.00024759
  },
  "n_pos_class": 0,
  "n_class": 4,
  "class_rule_pass": false
}
```

