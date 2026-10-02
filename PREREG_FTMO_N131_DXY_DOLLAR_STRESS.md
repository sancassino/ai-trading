# PREREG_FTMO_N131 — DXY_DOLLAR_STRESS (US500cash; session-flat; NEW_FAMILY AZ)

**Status:** **STOP FAIL_T** — U2 tip `03ad9da` on `claude/uitvoerder2-r` (TRIAL **469→470**).  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**VOORSTEL:** `VOORSTEL_PRESCREEN_N131.md`.  
**Signal:** Yahoo/proxy **DXY** (DX-Y.NYB daily level). **Trade:** `US500cash`.  
**NEW_FAMILY AZ:** **DEAD** (no DXY/dollar-index clones, no N110 Lon→EU-PM rewrite, no thr-grid, no overnight). **≠ N110** remains (session 15:30–21:00, not DXYcash 13:00–17:00).  
**Hold:** session-flat 15:30→21:00 CET (was freeze).  
**TRIAL_COUNT book:** **470** after this trial.  
**Reserve 2025+:** **onaangeroerd.**  
**Dead += N131.** No retune.

Board: U2 `results/R2/n131_dxy_dollar_stress/` (tip `03ad9da`). Faraday tip at PREREG freeze: `0af85da`. Pre-screen was `results/R2/n130_n131_prescreen/` (N=413, bruto **+5,08**).

---

## U2 result (authoritative)

| Post | Waarde |
|------|--------|
| Verdict | **FAIL_T** (cost+stress **PASS**) |
| Train 2021–23 | N=**413**, mean bruto **+5,08** ≥2,34 and ≥3,51; netto **+4,30**; med **+5,22**; years **−6,69/+5,44/+9,12**; L/S **131/282** |
| t | t_netto **1,01** / t_NW5 **1,05** ≪ 2 |
| Test | N=**146**, mean bruto **−1,10** |
| Trial | **469→470**; counts_as_trial=true |
| Signal (locked) | DXY `(z120>+0,5)&(d20>0)`→SHORT; `(z120<−0,5)&(d20<0)`→LONG; session **15:30–21:00** ≠ N110 |
| Retune | **verboden** (geen thr-grid, geen DXY clone, geen N110 rewrite, geen overnight) |

Live PREREG-pointer **cleared**.

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze

| Post | Waarde | Bron |
|------|--------:|------|
| Signal | Yahoo/proxy **DXY** (adjclose) | `data/daily/DXY.csv` |
| Trade | `US500cash` | FTMO |
| Round-trip intradag (RT) | **0,78 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (EOD flat same CET day) | D-100 session-flat |
| Hold | entry first M5 **[15:30, 15:45] CET** → flat **21:00 CET** | bevroren |
| **Gate (binding)** | **3 × 0,78 = 2,34 bp** | pure intradag |
| Stress (informeel) | **1,5 × 2,34 = 3,51 bp** | vóór formal t |

Alfa = signed mean **bruto prijs**; geen swap-credit.

---

## 2. Economisch mechanisme (NEW_FAMILY AZ) — not an N110 clone

`NEW_FAMILY: AZ` — DXY **daily level** as tighter/looser global financial conditions into the US cash session:

1. `z120 = (DXY_t − mean_120(DXY)) / stdev_120(DXY)`; `d20 = DXY_t / DXY_{t−20} − 1`.
2. **dollar_tightening (inverse combo):** `(z120 > +0,5) and (d20 > 0)` → **SHORT** US500; `(z120 < −0,5) and (d20 < 0)` → **LONG**; else skip.
3. Maps to cheap FTMO index CFD (**US500cash**), **not** a DXYcash trade leg.

**Not N110 (barred DXY Lon→EU-PM).** N110 was: DXYcash **M5** impulse 08:00→12:00 CET, `|am|≥25` bp, **same-direction** LONG/SHORT **DXYcash** itself, entry **13:00** flat **17:00** (before US cash), gate **7,86**. N131 uses a **daily Yahoo level** z120+d20, **inverse** map into **US500cash 15:30→21:00**, gate **2,34**. Different signal, clock, instrument, and direction. Do not rewrite N131 onto DXYcash or the 13:00–17:00 window.

**Distinct / dead-set guard:**
- ≠ **N110** DIAG_FAIL (Lon-AM→EU-PM DXYcash continuation)
- ≠ **N115** EURUSD→US500 FAIL (single-pair Lon-AM lead-lag ≠ dollar-index level)
- ≠ **N127 EWZ** / **N121 EEM** / **N123 EFA** (equity ETF ≠ dollar index)
- ≠ **N128 BWX** FAIL_T / **N116 TLT** / **N118 TIP** / **N124 YIELD_CURVE** (rates ≠ DXY)
- ≠ N84 AUDNZD stretch / L60 FX-med / 5d FX LO carry set
- ≠ overnight / thr-grid / soft gate / N110 session rewrite

---

## 3. Bevroren regel (geen retune)

**Signal (dag t):**
1. Data: `data/daily/DXY.csv` (not `DXYcash` M5).
2. `z120` + `d20` inverse combo long/short/skip as §2. Thresholds **±0,5** and windows **120 / 20** frozen.

**Execution (dag t+1, FTMO M5 `US500cash`) — D-100 session-flat:**
3. Entry: close van eerste M5-bar ≥ **15:30 CET** (span ≤15 min). Ontbreekt → skip day.
4. Exit: close van laatste M5-bar ≤ **21:00 CET** same day. **Geen overnight. Geen DXYcash leg. Geen 13:00–17:00 EU-PM window.**
5. PnL: `pnl_bp = position × (P_exit / P_entry − 1) × 1e4`.
6. Non-overlapping (≤1 trade/dag).
7. **Verboden:** thr-grid op 2025+; overnight hold; N110 Lon→EU-PM rewrite; EWZ/EEM/EFA clone; soft gate.

---

## 4. D-092.1 pre-screen (train-only; binding for PREREG eligibility)

| Metric | Value |
|--------|------:|
| Train | 2021-01-01 … 2023-12-31 |
| N | **413** (≥150) |
| Mean bruto | **+5,08 bp** (≥ 2,34) |
| Median | +5,22 bp |
| Hit-rate | 0,54 |
| Long / short | 131 / 282 |
| Years | 2021 **−6,69** / 2022 **+5,44** / 2023 **+9,12** |
| Stress informal | mean ≥ 3,51 → **PASS_stress_informal** |
| Verdict | **PASS_may_PREREG** |
| vs N110 | **DISTINCT** (not same session/map) |

Artifact: `results/R2/n130_n131_prescreen/prescreen.json`.

---

## 5. U2 opdracht (cost-gate + formal t)

1. Replicate freeze §3 on train 2021–2023 **US500cash** session-flat (do **not** trade DXYcash; do **not** use 13:00–17:00).
2. Cost-gate: mean bruto ≥ **2,34**; stress informal ≥ **3,51**.
3. Formal: day-clust t / NW5 ≥ 2; report test 2024 separately (no selection).
4. FAIL_T / FAIL_STRESS / FAIL_COST → STOP; **geen** thr-grid / N110 rewrite / EWZ clone / overnight.
5. counts_as_trial only if cost+stress PASS then formal t run.

**TRIAL_COUNT at freeze (was):** **468**. After U2 FAIL_T: **470**.
