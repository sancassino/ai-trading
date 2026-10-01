# C-021 — D-097 low-turnover FTMO target grid (CTO track 5)

- When: 2026-10-01 ~09:28 Europe/Amsterdam (CEST / UTC+2)
- Branch: `grok/cto-1`
- Reserve 2025+: **not used**
- Trials appended: **0** (diagnostic design table)
- Engine: `engine/ftmo.py` recommend_scale + ftmo_ev
- Synthetic calendar: 2020-01-02 … 2024-12-31; n_paths=2500

## Binding policy shifts (D-097)

1. **Intraday micro-edges deprioritized** — 0–15 bp bruto dies on costs (P1/N35–N41 pattern).
2. **Target sleeve class:** hold 3–20d, bruto 50–300 bp/trade, cost 1–10 bp + swap explicit.
3. **Track 3 combining PAUSED** until individual day-clust t ≥ 2.0 (no more C-018-style ceiling books as candidates).
4. Dead: P1, S2-BTC US-open, N35, N36, N40, N41, GBPJPY_EU_MOM. No clones.

## Tier minima (hold=5d core slice; mean **net** bp/trade after costs)

| trades/yr | tier | min net bp/trade | ann SR | t_NW5 | €/m EV | p1·p2 | note |
|---:|---|---:|---:|---:|---:|---:|---|
| 12 | ev300 | **60** | 1.56 | 4.30 | 626 | 0.94 | cleared |
| 12 | ev500 | **60** | 1.56 | 4.30 | 626 | 0.94 | cleared |
| 12 | ev800 | **150** | 1.58 | 4.25 | 914 | 0.95 | cleared |
| 24 | ev300 | **40** | 1.78 | 4.94 | 668 | 0.97 | cleared |
| 24 | ev500 | **40** | 1.78 | 4.94 | 668 | 0.97 | cleared |
| 24 | ev800 | **60** | 1.99 | 5.42 | 906 | 0.99 | cleared |
| 36 | ev300 | **20** | 1.57 | 4.38 | 523 | 0.93 | cleared |
| 36 | ev500 | **20** | 1.57 | 4.38 | 523 | 0.93 | cleared |
| 36 | ev800 | **40** | 2.17 | 5.71 | 1066 | 0.99 | cleared |
| 52 | ev300 | **20** | 1.91 | 5.34 | 933 | 0.99 | cleared |
| 52 | ev500 | **20** | 1.91 | 5.34 | 933 | 0.99 | cleared |
| 52 | ev800 | **20** | 1.91 | 5.34 | 933 | 0.99 | cleared |
| 78 | ev300 | **20** | 2.41 | 6.08 | 1138 | 1.00 | cleared |
| 78 | ev500 | **20** | 2.41 | 6.08 | 1138 | 1.00 | cleared |
| 78 | ev800 | **20** | 2.41 | 6.08 | 1138 | 1.00 | cleared |

## Practical operating points (for Strateeg PREREG design)

| label | trades/yr | hold | net bp | t_NW5 | SR | scale | €/m | p1·p2 | formal? |
|---|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| A_monthly_swing | 12 | 10 | 150 | 4.34 | 1.58 | 2.42 | 975 | 0.96 | Y |
| B_biweekly_swing | 24 | 5 | 100 | 5.97 | 2.18 | 2.32 | 1589 | 1.00 | Y |
| C_weekly_swing | 52 | 5 | 80 | 8.92 | 3.25 | 2.25 | 3017 | 1.00 | Y |

## Strateeg / S2 bars (actionable)

- **Pre-screen (free):** mean bruto ≥ 3× (RT + swap×nights); prefer ≥ **50 bp bruto/trade**.
- **Discovery:** ≥10y proxy for mechanism (D-094a b) when FTMO-M5 <5y; freeze rule before FTMO cost gate.
- **Formal:** day-clust t≥2.0 both halves + ann SR≥0.8; no threshold mining on 2021–22-only edges.
- **FTMO:** `recommend_scale` with max daily loss ≤4%; need p1·p2≥0.35 and net_EV>0; €300–500 ok if robust.
- **Combine (CTO track 3):** only after **solo** formal PASS — do not stack FAIL_T sleeves.
- **Families:** commodity/FX/index TSMOM; XS-momentum across 166; carry/RV dollar-neutral; regime filter (ATR%ile or 200d) pre-registered as one rule.

## CTO next

- Idle on track-3 blends until a D-097 sleeve clears formal t.
- When U2 lands a gate+stress+t PASS: run track-5 `recommend_scale` + optional solo `ftmo_ev` (still no 2025+ without BESLUITEN).
- Manager: absorb D-097 into NEXT_STEPS (v67 still ends at D-096).

Artefacts: `results/cto/c021_d097_low_turnover/target_grid.csv`, `tier_mins.json`, `c021_board.json`.

## Assumptions / ceiling (read this)

This grid **assumes** a stable mean net bp/trade exists over 2020–2024 and is then vol-scaled into FTMO. It answers: *if* Strateeg finds such an edge, what magnitude × frequency clears FTMO EV. It is **not** evidence that any live sleeve has that edge. Real series will have regime breaks (2021–22 vs 2023–24 pattern); formal t on both halves remains the gate. Overnight swap must be inside the net bp figure before claiming a row.
