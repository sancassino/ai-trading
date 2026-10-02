# PREREG_FTMO_N130 — EQW_BREADTH_STRESS (US500cash; session-flat; NEW_FAMILY AY)

**Status:** **OPEN** — frozen for U2 cost-gate + formal trial (Lane-B D-092.1 PASS).  
**Auteur:** Strateeg (Grok) Lane-B on `claude/trusting-faraday-34tsmg`.  
**VOORSTEL:** `VOORSTEL_PRESCREEN_N130.md`.  
**Signal:** Yahoo/proxy **SPX_EQW / SPX** (RSP/SPX breadth ratio). **Trade:** `US500cash`.  
**NEW_FAMILY AY:** US equal-weight vs cap-weight **breadth ratio** stress → equity session-flat (**≠ IWM** small-cap level / **≠ SECTOR_DISP** / **≠ DEFENSIVE_CYCLICAL** XLU/XLI / **≠ N81** pair RV overnight).  
**Hold:** **session-flat** entry ≈15:30 CET → flat ≈21:00 CET (D-100; US500 overnight swap avoided).  
**TRIAL_COUNT book:** **468** (deze PREREG telt nog niet).  
**Reserve 2025+:** **onaangeroerd.**  
**Geen retune** na freeze.

Pre-screen: `results/R2/n130_n131_prescreen/` — N130 **PASS** train N=**220** mean bruto **+6,68** ≥ gate **2,34** (stress informal ≥ **3,51**).

---

## 1. Instrument & kosten (D-100 / D-092.1) — freeze

| Post | Waarde | Bron |
|------|--------:|------|
| Signal | Yahoo/proxy **SPX_EQW / SPX** (adjclose ratio) | `data/daily/SPX_EQW.csv` + `data/daily/SPX.csv` |
| Trade | `US500cash` | FTMO |
| Round-trip intradag (RT) | **0,78 bp** | `COSTS_FTMO.csv` |
| Swap | **0** (EOD flat same CET day) | D-100 session-flat |
| Hold | entry first M5 **[15:30, 15:45] CET** → flat **21:00 CET** | bevroren |
| **Gate (binding)** | **3 × 0,78 = 2,34 bp** | pure intradag |
| Stress (informeel) | **1,5 × 2,34 = 3,51 bp** | vóór formal t |

Alfa = signed mean **bruto prijs**; geen swap-credit.

---

## 2. Economisch mechanisme (NEW_FAMILY AY)

`NEW_FAMILY: AY` — RSP/SPX ratio as **participation vs mega-cap concentration** timing into US large-cap beta:

1. `ratio_t = SPX_EQW_t / SPX_t`.
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)`.
3. **stress_buy:** `z40 > +1,5` → **SHORT** US500 (breadth blow-off); `z40 < −1,5` → **LONG** (breadth washout); else skip.
4. Maps to cheap FTMO index CFD (**US500cash**), **not** an RSP CFD trade leg.

**Distinct / dead-set guard:**
- ≠ **N119 IWM** D-092.1 FAIL (small-cap ETF level ≠ EQW/SPX ratio)
- ≠ **N93 SECTOR_DISP** / **N125 DEFENSIVE_CYCLICAL** FAIL_T (sector rotation / XLU-XLI ≠ breadth ratio)
- ≠ **N81** pair RV DIAG_FAIL (US100/US500 3d overnight ≠ session-flat breadth)
- ≠ **N128 BWX** FAIL_T / TLT / TIP / EMB / YIELD_CURVE / EWZ / EEM / EFA / HYG / VIX / PPLT
- ≠ overnight / thr-grid / soft gate / IWM or XLU-XLI rewrite

---

## 3. Bevroren regel (geen retune)

**Signal (dag t):**
1. Data: `data/daily/SPX_EQW.csv`, `data/daily/SPX.csv`.
2. `z40` stress_buy long/short/skip as §2. Thresholds **±1,5** and window **40** frozen.

**Execution (dag t+1, FTMO M5 `US500cash`) — D-100 session-flat:**
3. Entry: close van eerste M5-bar ≥ **15:30 CET** (span ≤15 min). Ontbreekt → skip day.
4. Exit: close van laatste M5-bar ≤ **21:00 CET** same day. **Geen overnight. Geen RSP/IWM CFD leg.**
5. PnL: `pnl_bp = position × (P_exit / P_entry − 1) × 1e4`.
6. Non-overlapping (≤1 trade/dag).
7. **Verboden:** thr-grid op 2025+; overnight hold; IWM/SECTOR_DISP/XLU-XLI rewrite; soft gate.

---

## 4. D-092.1 pre-screen (train-only; binding for PREREG eligibility)

| Metric | Value |
|--------|------:|
| Train | 2021-01-01 … 2023-12-31 |
| N | **220** (≥150) |
| Mean bruto | **+6,68 bp** (≥ 2,34) |
| Median | +1,66 bp |
| Hit-rate | 0,51 |
| Long / short | 99 / 121 |
| Years | 2021 **−0,41** / 2022 **+18,72** / 2023 **−1,71** |
| Stress informal | mean ≥ 3,51 → **PASS_stress_informal** |
| Verdict | **PASS_may_PREREG** |

Artifact: `results/R2/n130_n131_prescreen/prescreen.json`.

---

## 5. U2 opdracht (cost-gate + formal t)

1. Replicate freeze §3 on train 2021–2023 US500cash session-flat.
2. Cost-gate: mean bruto ≥ **2,34**; stress informal ≥ **3,51**.
3. Formal: day-clust t / NW5 ≥ 2; report test 2024 separately (no selection).
4. FAIL_T / FAIL_STRESS / FAIL_COST → STOP; **geen** thr-grid / IWM twin / sector rewrite / overnight.
5. counts_as_trial only if cost+stress PASS then formal t run.

**TRIAL_COUNT at freeze:** **468**.
