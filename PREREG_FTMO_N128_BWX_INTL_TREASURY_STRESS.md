# PREREG_FTMO_N128 — BWX_INTL_TREASURY_STRESS (US500cash; session-flat; NEW_FAMILY AW)

**Status:** **OPEN** — frozen for U2 cost-gate + formal trial (Lane-B D-092.1 PASS).  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**VOORSTEL:** `VOORSTEL_PRESCREEN_N128.md`.  
**Signal:** Yahoo/proxy **BWX** (SPDR Bloomberg International Treasury Bond). **Trade:** `US500cash`.  
**NEW_FAMILY AW:** DM ex-US treasury ETF **level** stress → equity session-flat (**≠ TLT** US duration / **≠ TIP** real-rate / **≠ EMB** EM credit / **≠ YIELD_CURVE** 10Y−3M slope).  
**Hold:** **session-flat** entry ≈15:30 CET → flat ≈21:00 CET (D-100; US500 overnight swap avoided).  
**TRIAL_COUNT book:** **467** (deze PREREG telt nog niet).  
**Reserve 2025+:** **onaangeroerd.**  
**Geen retune** na freeze.

Pre-screen: `results/R2/n128_n129_prescreen/` — N128 **PASS** train N=**419** mean bruto **+6,63** ≥ gate **2,34** (stress informal ≥ **3,51**).

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

**TRIAL_COUNT at freeze:** **467**.
