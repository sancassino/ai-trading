# C-022 — D-097 proxy TSMOM / XS-mom diagnostic (CTO track 4/5 assist)

- When: 2026-10-01 ~09:53 Europe/Amsterdam (CEST / UTC+2)
- Branch: `grok/cto-1`
- Reserve 2025+: **not used** (hard cut ≤2024-12-31)
- Trials appended: **0**
- Proxies loaded (10j+, daily file, no compound FXBIS): **53** (fx14 / index14 / commodity16 / stock7 / crypto2)
- Inputs: `data/PROXY_MAP_FTMO.csv` (spoor 6) + `data/daily/*` + `COSTS_FTMO.csv`
- Script: `scripts/c022_d097_proxy_tsmom_screen.py`

## Binding

- Diagnostic / mechanism screen only — **not** a formal gate, **not** a PREREG.
- Strateeg/S2 must freeze a rule in PREREG before U2 FTMO-M5 cost-gate.
- D-094a (b): ≥10y proxy can underwrite mechanism; FTMO-M5 still needed for costs/execution.
- Track-3 combine still **paused** until solo day-clust t≥2.0 on a formal PASS.
- Classic **XS-mom L3/S3** on commodities/indices/FX majors is **negative** on 2015–2024 — do not PREREG that family as-is.

## Headline (actionable)

1. **Energy TSMOM (best non-crypto D-097 family):** UKOIL / USOIL / HEATOIL — lookback **20d**, hold **10–20d**, long-only. Several rows clear ≥50 bp bruto with t_net>1 and both-half t>0. UKOIL L20/H10: bruto≈117, t_net≈3.6, t_h1/h2≈2.14/2.92 (costs from FTMO UKOILcash; net>bruto because swap_long is a credit in `COSTS_FTMO` — verify overnight before PREREG).
2. **Index TSMOM (secondary):** HK50 long_short L20/H20; US100/US500 long-only L120/H20. Half-splits weaker than oil — use only with a frozen 200d regime filter or drop.
3. **FX:** USDCNH / USDJPY long-only L20–60 / H10–20 near bars; USDCNH uses fallback costs — confirm FTMO CNH book before PREREG.
4. **Crypto daily TSMOM** (BTC/LTC) tops the raw shortlist on bruto/t — but treat as **separate, high-risk** family (S2-BTC US-open already dead; high RT/swap; regime 2021–22). Not the default D-097 path; only if Strateeg writes an explicit non-clone PREREG with D-094a (a)/(b).
5. **XS-mom cross-section:** FAIL diagnostically (negative mean) on all three universes — kill for now.

## Non-crypto shortlist (top)

| family | symbol | cat | mode | L/H | N | bruto bp | net bp | t_net | t_h1/h2 | tr/yr | cost |
|---|---|---|---|---|---:|---:|---:|---:|---|---:|---|
| TSMOM | HEATOIL.c | commodity/metal | long_only | L20/H20 | 65 | 249.7 | 206.7 | 1.64 | 0.76/1.46 | 6.7 | fallback:commodity/metal |
| TSMOM | HEATOIL.c | commodity/metal | long_short | L20/H20 | 124 | 195.4 | 152.4 | 1.70 | 0.63/1.64 | 12.6 | fallback:commodity/metal |
| TSMOM | HK50.cash | index | long_short | L20/H20 | 121 | 135.9 | 111.0 | 2.04 | 1.41/1.48 | 12.3 | fallback:index |
| TSMOM | MCD | stock | long_only | L20/H20 | 77 | 134.2 | 110.2 | 2.32 | 1.88/1.38 | 7.9 | fallback:stock |
| TSMOM | UKOIL.cash | commodity/metal | long_only | L20/H20 | 74 | 128.3 | 245.1 | 2.41 | 2.10/1.32 | 7.6 | UKOILcash |
| TSMOM | HK50.cash | index | long_only | L20/H20 | 64 | 128.9 | 97.4 | 1.22 | 1.11/0.70 | 6.6 | fallback:index |
| TSMOM | US100.cash | index | long_only | L120/H20 | 94 | 124.3 | 84.7 | 1.50 | 0.54/1.50 | 9.9 | US100cash |
| TSMOM | SIEGn | stock | long_only | L20/H20 | 75 | 123.8 | 99.8 | 1.34 | 1.51/0.65 | 7.6 | fallback:stock |
| TSMOM | HEATOIL.c | commodity/metal | long_only | L20/H10 | 134 | 119.7 | 96.7 | 1.56 | 0.81/1.33 | 13.7 | fallback:commodity/metal |
| TSMOM | UKOIL.cash | commodity/metal | long_only | L20/H10 | 144 | 116.9 | 174.0 | 3.60 | 2.14/2.92 | 14.6 | UKOILcash |
| TSMOM | MCD | stock | long_only | L60/H20 | 86 | 118.1 | 94.1 | 1.90 | 2.54/0.36 | 8.9 | fallback:stock |
| TSMOM | US500.cash | index | long_only | L120/H20 | 92 | 95.3 | 67.3 | 1.55 | 0.70/1.43 | 9.7 | US500cash |
| TSMOM | HEATOIL.c | commodity/metal | long_short | L20/H10 | 249 | 92.4 | 69.4 | 1.44 | 0.65/1.31 | 25.2 | fallback:commodity/metal |
| TSMOM | USOIL.cash | commodity/metal | long_only | L20/H20 | 68 | 86.4 | 191.1 | 1.79 | 1.04/1.48 | 7.2 | USOILcash |
| TSMOM | US500.cash | index | long_only | L20/H20 | 84 | 69.5 | 41.5 | 1.04 | 0.69/0.79 | 8.6 | US500cash |

## Crypto-only note (not default)

| family | symbol | cat | mode | L/H | N | bruto bp | net bp | t_net | t_h1/h2 | tr/yr | cost |
|---|---|---|---|---|---:|---:|---:|---:|---|---:|---|
| TSMOM | LTCUSD | crypto | long_only | L60/H20 | 87 | 907.9 | 799.9 | 1.79 | 1.80/0.41 | 8.9 | fallback:crypto |
| TSMOM | LTCUSD | crypto | long_only | L20/H20 | 93 | 835.9 | 727.9 | 1.78 | 1.93/0.02 | 9.4 | fallback:crypto |
| TSMOM | LTCUSD | crypto | long_only | L120/H20 | 95 | 806.9 | 698.9 | 1.76 | 1.38/1.21 | 9.9 | fallback:crypto |
| TSMOM | BTCUSD | crypto | long_only | L120/H20 | 115 | 681.5 | 573.5 | 2.98 | 2.13/2.10 | 12.0 | fallback:crypto |
| TSMOM | BTCUSD | crypto | long_only | L60/H20 | 109 | 574.5 | 466.5 | 2.33 | 2.67/0.53 | 11.2 | fallback:crypto |
| TSMOM | BTCUSD | crypto | long_only | L20/H20 | 107 | 536.4 | 428.4 | 2.23 | 1.99/1.08 | 10.9 | fallback:crypto |

## XS-mom (2015–2024) — all FAIL

| family | universe | mode | bruto bp | net bp | t_net |
|---|---|---|---:|---:|---:|
| XS_MOM | indices | L3/S3 L60/H20 | -1.6 | -27.6 | -2.20 |
| XS_MOM | fx_majors | L3/S3 L60/H20 | -33.5 | -48.3 | -3.66 |
| XS_MOM | commodities | L3/S3 L60/H20 | -89.0 | -135.0 | -3.14 |

## Strateeg / S2 — concrete next PREREGs (suggested)

Priority order (non-clones of N35–N44 / P1 / GBPJPY):

1. **PREREG energy TSMOM** — `UKOIL.cash` and/or `USOIL.cash`, signal = sign(close/close[20]-1), enter next day, hold 10d (and sensitivity 20d as secondary, not tuned), long-only, train on proxy ≤2024, D-094a (b) cite `BRENT_F`/`WTI_F` years; overnight swap from FTMO specs mandatory in net.
2. **Optional HEATOIL.c** same rule (fallback costs → must measure FTMO RT/swap before formal).
3. **Skip** raw XS-mom L/S. Consider **carry/RV** or **vol-targeted CTA** next if energy fails stress/t.
4. N45–N48 intradag queue may continue but is **lower EV** vs D-097 bars (C-021).

## CTO next

- Track-3 blends: still idle until formal solo t≥2 PASS.
- On first U2 D-097 PASS: track-5 `recommend_scale` / `ftmo_ev` (no 2025+ without BESLUITEN).
- Manager: no ask (v69 already absorbed D-097/C-021); point Strateeg at `shortlist_noncrypto.csv`.

Artefacts: `screen_all.csv`, `screen_2015_2024_ranked.csv`, `shortlist.csv` (incl. crypto), `shortlist_noncrypto.csv`, `c022_board.json`.
