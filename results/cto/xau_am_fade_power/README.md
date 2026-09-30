# XAU_AM_FADE power-pad — DIAGNOSTIC ONLY

**Not a trial. Frozen thresholds unchanged (0.60× ATR, 11:30 entry, 14:00 flat).**
**Reserve 2025+ not used for any gate/decision.**

## Finding
STRUCTURAL underpower: m5gz/XAUUSD.csv.gz starts 2021-01-01 — no 2018–2020. Train 2021–2023 N=12 under frozen 0.60× (≪120). Eligible=760; hit_rate=0.015789473684210527. Not a TZ/filter bug (windows present). Watch-only; new PREREG if N≥120 needed. Do NOT loosen 0.60×.

## N breakdown
| Window | N signals | Eligible days | Note |
|--------|-----------|---------------|------|
| 2018–2020 | 0 | 0 | NO_DATA |
| 2021–2023 train | 12 | 760 | matches U2 gate N=12 |
| 2024 test | 2 | 259 | report only |

Report-only threshold sensitivity N(train): {'0.45': 24, '0.6': 12, '0.75': 2}
ext/ATR distribution (eligible train): {'p50': 0.1071328289375525, 'p75': 0.20564088086980298, 'p90': 0.3207457657136327, 'p95': 0.3954129076515316, 'p99': 0.6154743282097472, 'max': 0.8302929113382834, 'frac_ge_0.60': 0.015789473684210527, 'frac_ge_0.45': 0.031578947368421054, 'frac_ge_0.30': 0.11447368421052631, 'n_eligible': 760}

## Recommendation
Keep sleeve **watch-only**. Ask Strateeg for a *new* PREREG with different mechanism if N cannot reach 120 without post-hoc threshold change. **Do not loosen 0.60×.** No formal `ftmo_ev`.

Reproduce: `/workspace/venv-u2/bin/python scripts/xau_am_fade_power_diag.py`
