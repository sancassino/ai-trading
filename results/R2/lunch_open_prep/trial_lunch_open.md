# S2 LUNCH_OPEN — formele trial (na cost-gate PASS)

Datum: 2026-10-01 ~02:55 CEST | PREREG_S2_LUNCH_OPEN | Reserve 2025→ onaangeraakt.

## Day-clustered netto (bp)

| Window | N trades | N days | mean netto/trade | t (day-clust) | skew day |
|--------|---------:|-------:|-----------------:|--------------:|---------:|
| train | 233 | 191 | 4.1761 | 1.1387 | 2.4325 |
| test | 100 | 80 | 0.1662 | 0.0515 | 0.4378 |

**t_ok (≥2.0 train&test, mean netto>0, N≥150):** False
**cost_ok (mean RT < 50% mean bruto):** True (frac=0.1144)
**skew_ok (day PnL > 0):** True

## ftmo_ev (train nonzero days, 0.75% risk, n_paths=5000)

```json
{
  "p95_daily_loss_frac": 0.015287,
  "p95_daily_loss_ok": true,
  "train_only": {
    "p_pass_1": 0.9948,
    "p_pass_2": 0.9606,
    "p_survive": 0.400977,
    "exp_payout_monthly": 615.546329,
    "net_ev": 13522.255886,
    "attempts_mean": 2.3164,
    "horizon_months": 24.0,
    "n_funded": 4803
  },
  "train_test_sens": {
    "p_pass_1": 0.9912,
    "p_pass_2": 0.938,
    "p_survive": 0.246218,
    "exp_payout_monthly": 521.316439,
    "net_ev": 10895.806524
  },
  "net_ev_monthly": 563.43,
  "net_ev_per_attempt": 5837.62,
  "ev_per_attempt_ok": true
}
```

## **Uitkomst: FAIL_T**

PASS_CANDIDATE → shortlist/Manager. FAIL_* → STOP (TRIAL_COUNT already +1 on cost-gate PASS).