# PREREG_FTMO_N128 — BWX_INTL_TREASURY_STRESS (US500cash; session-flat; NEW_FAMILY AW)

**Status:** **STOP FAIL_T** — U2 tip `62a7718` on `claude/uitvoerder2-r` (TRIAL **467→468**).  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**VOORSTEL:** `VOORSTEL_PRESCREEN_N128.md`.  
**Signal:** Yahoo/proxy **BWX** (SPDR Bloomberg International Treasury Bond). **Trade:** `US500cash`.  
**NEW_FAMILY AW:** **DEAD** (no BWX/TLT/TIP/EMB/yield clones, no thr-grid, no overnight).  
**Hold:** session-flat 15:30→21:00 CET (was freeze).  
**TRIAL_COUNT book:** **468** after this trial.  
**Reserve 2025+:** **onaangeroerd.**  
**Dead += N128.** No retune.

Board: U2 `results/R2/n128_bwx_intl_treasury_stress/` (tip `62a7718`). Faraday tip at PREREG freeze: `cb136e0`. Pre-screen was `results/R2/n128_n129_prescreen/` (N=419, bruto **+6,63**).

---

## U2 result (authoritative)

| Post | Waarde |
|------|--------|
| Verdict | **FAIL_T** (cost+stress **PASS**) |
| Train 2021–23 | N=**419**, mean bruto **+6,63** ≥2,34 and ≥3,51; netto **+5,85**; med **+8,58**; years **−8,07/+8,89/+9,55**; L/S **96/323** |
| t | t_netto **1,40** / t_NW5 **1,43** ≪ 2 |
| Test | N=**136**, mean bruto **−2,37** |
| Trial | **467→468**; counts_as_trial=true |
| Signal (locked) | `(z>+0,5)&(d20>0)`→LONG; `(z<−0,5)&(d20<0)`→SHORT |
| Retune | **verboden** (geen thr-grid, geen TLT/TIP/EMB/yield rewrite, geen BWX clone, geen overnight) |

Live PREREG-pointer **cleared**.

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze

| Post | Waarde | Bron |
|------|--------:|------|
| Signal | Yahoo/proxy **BWX** (adjclose) | `data/daily/BWX.csv` |
| Trade | `US500cash` | FTMO |
| Round-trip intradag (RT) | **0,78 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (EOD flat same CET day) | D-100 session-flat |
| Hold | entry first M5 **[15:30, 15:45] CET** → flat **21:00 CET** | bevroren |
| **Gate (binding)** | **3 × 0,78 = 2,34 bp** | pure intradag |
| Stress (informeel) | **1,5 × 2,34 = 3,51 bp** | vóór formal t |

Alfa = signed mean **bruto prijs**; geen swap-credit.

---

## 2. Economisch mechanisme (NEW_FAMILY AW)

`NEW_FAMILY: AW` — BWX close as **international DM treasury** (FX-hedged global rates / reserve-demand) timing into US large-cap beta:

1. `z120 = (BWX_t − mean_120(BWX)) / stdev_120(BWX)`; `d20 = BWX_t / BWX_{t−20} − 1`.
2. **combo:** `(z120 > +0,5) and (d20 > 0)` → **LONG** US500; `(z120 < −0,5) and (d20 < 0)` → **SHORT**; else skip.
3. Maps to cheap FTMO index CFD (**US500cash**), **not** a BWX CFD trade leg.

**Distinct / dead-set guard:**
- ≠ **N116 TLT** FAIL_T (US long duration ≠ DM ex-US treasury basket)
- ≠ **N118 TIP** FAIL_T (US real rate ≠ nominal intl treasury)
- ≠ **N100 EMB** FAIL_T (EM credit ≠ DM treasury)
- ≠ **N124 YIELD_CURVE** FAIL_T (10Y−3M slope ≠ ETF level)
- ≠ **N127 EWZ** FAIL_T / EEM / EFA / DBA / PPLT / HYG / VNQ / IWM / SECTOR_DISP / VIX
- ≠ overnight / thr-grid / soft gate / TLT-TIP-EMB-yield rewrite

---

## 3. Bevroren regel (geen retune)

**Signal (dag t):**
1. Data: `data/daily/BWX.csv`.
2. `z120` + `d20` combo long/short/skip as §2.

**Execution (dag t+1, FTMO M5 `US500cash`) — D-100 session-flat:**
3. Entry: close van eerste M5-bar ≥ **15:30 CET** (span ≤15 min). Ontbreekt → skip day.
4. Exit: close van laatste M5-bar ≤ **21:00 CET** same day. **Geen overnight. Geen BWX CFD leg.**
5. PnL: `pnl_bp = position × (P_exit / P_entry − 1) × 1e4`.
6. Non-overlapping (≤1 trade/dag).
7. **Verboden:** thr-grid op 2025+; overnight hold; TLT/TIP/IEF/EMB/yield-curve rewrite; soft gate.

---

## 4. D-092.1 pre-screen (train-only; binding for PREREG eligibility)

| Metric | Value |
|--------|------:|
| Train | 2021-01-01 … 2023-12-31 |
| N | **419** (≥150) |
| Mean bruto | **+6,63 bp** (≥ 2,34) |
| Median | +8,58 bp |
| Hit-rate | 0,55 |
| Long / short | 96 / 323 |
| Years | 2021 **−8,07** / 2022 **+8,89** / 2023 **+9,55** |
| Stress informal | mean ≥ 3,51 → **PASS_stress_informal** |
| Verdict | **PASS_may_PREREG** |

Artifact: `results/R2/n128_n129_prescreen/prescreen.json`.

---

## 5. U2 opdracht (cost-gate + formal t)

1. Replicate freeze §3 on train 2021–2023 US500cash session-flat.
2. Cost-gate: mean bruto ≥ **2,34**; stress informal ≥ **3,51**.
3. Formal: day-clust t / NW5 ≥ 2; report test 2024 separately (no selection).
4. FAIL_T / FAIL_STRESS / FAIL_COST → STOP; **geen** thr-grid / TLT twin / yield-curve rewrite / overnight.
5. counts_as_trial only if cost+stress PASS then formal t run.

**TRIAL_COUNT at freeze (was):** **467**. After U2 FAIL_T: **468**.
