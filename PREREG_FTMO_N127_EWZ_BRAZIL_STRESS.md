# PREREG_FTMO_N127 — EWZ_BRAZIL_STRESS (US500cash; session-flat; NEW_FAMILY AV)

**Status:** **STOP FAIL_T** — U2 tip `3a970c7` on `claude/uitvoerder2-r` (TRIAL **466→467**).  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**VOORSTEL:** `VOORSTEL_PRESCREEN_N127.md`.  
**Signal:** Yahoo/proxy **EWZ** (iShares MSCI Brazil). **Trade:** `US500cash`.  
**NEW_FAMILY AV:** **DEAD** (no EWZ/EEM/EMB/EFA clones, no thr-grid, no overnight).  
**Hold:** session-flat 15:30→21:00 CET (was freeze).  
**TRIAL_COUNT book:** **467** after this trial.  
**Reserve 2025+:** **onaangeroerd.**  
**Dead += N127.** No retune.

Board: U2 `results/R2/n127_ewz_brazil_stress/` (tip `3a970c7`). Faraday tip at PREREG freeze: `3a96125`. Pre-screen was `results/R2/n126_n127_prescreen/` (N=208, bruto **+3,54**).

---

## U2 result (authoritative)

| Post | Waarde |
|------|--------|
| Verdict | **FAIL_T** (cost+stress **PASS**) |
| Train 2021–23 | N=**208**, mean bruto **+3,54** ≥2,34 and ≥3,51; netto **+2,76**; med **+1,89**; years **+18,36/−2,23/+5,62**; L/S **86/122** |
| t | t_netto **0,57** / t_NW5 **0,50** ≪ 2 |
| Test | N=**85**, mean bruto **+1,85** |
| Trial | **466→467**; counts_as_trial=true |
| Retune | **verboden** (geen thr-grid, geen EEM/EMB/EFA rewrite, geen EWZ clone, geen overnight) |

Live PREREG-pointer **cleared**.

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze

| Post | Waarde | Bron |
|------|--------:|------|
| Signal | Yahoo/proxy **EWZ** (adjclose) | `data/daily/EWZ.csv` |
| Trade | `US500cash` | FTMO |
| Round-trip intradag (RT) | **0,78 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (EOD flat same CET day) | D-100 session-flat |
| Hold | entry first M5 **[15:30, 15:45] CET** → flat **21:00 CET** | bevroren |
| **Gate (binding)** | **3 × 0,78 = 2,34 bp** | pure intradag |
| Stress (informeel) | **1,5 × 2,34 = 3,51 bp** | vóór formal t |

Alfa = signed mean **bruto prijs**; geen swap-credit.

---

## 2. Economisch mechanisme (NEW_FAMILY AV)

`NEW_FAMILY: AV` — EWZ close as **Brazil / LatAm equity + commodity-FX** risk-appetite proxy into US large-cap beta:

1. `z40 = (EWZ_t − mean_40(EWZ)) / stdev_40(EWZ)`.
2. **stress_buy:** `z40 > +1,5` → **SHORT** US500; `z40 < −1,5` → **LONG**; else skip.
3. Maps to cheap FTMO index CFD (**US500cash**), **not** EWZ CFD trade leg.

**Distinct / dead-set guard:**
- ≠ **N121 EEM** D-092.1 FAIL (EM basket ≠ Brazil solo)
- ≠ **N100 EMB** FAIL_T (EM bonds ≠ Brazil equity)
- ≠ **N123 EFA** DIAG_FAIL C-038 (DM ex-US ≠ Brazil)
- ≠ **N124 YIELD_CURVE** / **N125 DEFENSIVE** / N122 DBC / N126 DBA / TLT/TIP/HYG/VNQ/IWM/GAS/CPER/SILVER/SECTOR_DISP/VIX
- ≠ overnight / thr-grid / soft gate / EEM rewrite

---

## 3. Bevroren regel (geen retune)

**Signal (dag t):**
1. Data: `data/daily/EWZ.csv`.
2. `z40` + stress_buy long/short/skip as §2.

**Execution (dag t+1, FTMO M5 `US500cash`) — D-100 session-flat:**
3. Entry: close van eerste M5-bar ≥ **15:30 CET** (span ≤15 min). Ontbreekt → skip day.
4. Exit: close van laatste M5-bar ≤ **21:00 CET** same day. **Geen overnight. Geen EWZ CFD leg.**
5. PnL: `pnl_bp = position × (P_exit / P_entry − 1) × 1e4`.
6. Non-overlapping (≤1 trade/dag).
7. **Verboden:** thr-grid op 2025+; overnight hold; EEM/EMB/EFA rewrite; soft gate.

---

## 4. D-092.1 pre-screen (train-only; binding for PREREG eligibility)

| Metric | Value |
|--------|------:|
| Train | 2021-01-01 … 2023-12-31 |
| N | **208** (≥150) |
| Mean bruto | **+3,54 bp** (≥ 2,34) |
| Median | +1,89 bp |
| Hit-rate | 0,52 |
| Long / short | 86 / 122 |
| Years | 2021 **+18,36** / 2022 **−2,23** / 2023 **+5,62** |
| Stress informal | mean ≥ 3,51 → **PASS_stress_informal** |
| Verdict | **PASS_may_PREREG** |

Artifact: `results/R2/n126_n127_prescreen/prescreen.json`.

---

## 5. U2 opdracht (cost-gate + formal t)

1. Replicate freeze §3 on train 2021–2023 US500cash session-flat.
2. Cost-gate: mean bruto ≥ **2,34**; stress informal ≥ **3,51**.
3. Formal: day-clust t / NW5 ≥ 2; report test 2024 separately (no selection).
4. FAIL_T / FAIL_STRESS / FAIL_COST → STOP; **geen** thr-grid / EEM twin / overnight rewrite.
5. counts_as_trial only if cost+stress PASS then formal t run.

**TRIAL_COUNT at freeze (was):** **466**. After U2 FAIL_T: **467**.
