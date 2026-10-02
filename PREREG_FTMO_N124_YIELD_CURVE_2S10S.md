# PREREG_FTMO_N124 — YIELD_CURVE_2S10S → US500cash session-flat (NEW_FAMILY AS)

**Status:** **OPEN** — frozen for U2 cost-gate + formal trial (CTO **C-039** Lane-B DIAG_PASS 2026-10-02 ~23:56 CEST).  
**Auteur:** CTO (Grok) on `grok/cto-1`, from S2 `VOORSTEL_S2_YIELD_CURVE_2S10S.md` (cycle_2346 `13fe10c`). Faraday tip still `47e0eab` (OPEN empty) — CTO refill under D-094.  
**Signal:** Yahoo/proxy **YLD_US10Y − YLD_US3M** slope. **Trade:** `US500cash`. **NEW_FAMILY AS** (≠ TLT_DURATION / TIP_REALRATE / REIT_RATE / RATE_CURVE / HYG/EMB credit).

Diagnostic (train 2021–2023, CTO C-039, 0 trials): N=**240**, mean bruto **+8.971 bp** ≥ gate **2.34**, day_t≈1.89, h1 +11.12 / h2 +6.83, years 2021 −2.31 / 2022 +8.57 / 2023 +12.41 → **DIAG_PASS** (N≥150 ∧ mean≥gate).  
Gate smoke (same script, not a trial): cost **PASS** / stress **PASS** (8.97≥3.51); t_nw≈1.82; test 2024 mean bruto +2.89 t_nw≈0.33 → **elevated FAIL_T risk**; do **not** retune.

## 1. Bevroren regel
- Data: `data/daily/YLD_US10Y.csv` + `data/daily/YLD_US3M.csv` (adjclose/close) + `data/m5gz/US500cash.csv.gz`. Dagen ma–vr. Tijden = brokerservertijd (CET-proxy).
- Signal dag t: `slope = YLD_US10Y − YLD_US3M`; `z60 = (slope_t − mean_60(slope)) / stdev_60(slope)` (rolling min_periods = max(20, 60//3)).
- **flatten_fade:** `z60 > +1,5` → **SHORT**; `z60 < −1,5` → **LONG**; else skip.
- Execution dag t+1 on US500cash — D-100 session-flat:
  - Entry: close of first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
  - Exit: flat ≤ **21:00 CET** same day. **No overnight. No stop.** Max 1 trade/dag.
- Geen thr-grid, geen 10Y-2Y twin, geen TLT/TIP rewrite, geen overnight, geen soft gate, geen US100 remap.

## 2. Kosten en poort
- RT **0,78 bp** (`COSTS_FTMO` US500cash); session-flat → swap = 0.
- Gate: mean bruto ≥ **3 × 0,78 = 2,34 bp**/trade op train 2021–2023, **N ≥ 150**.
- Stress: +50% roundtrip (mean ≥ **3,51 bp**) vóór formal t.

## 3. Beslisregel
- Train 2021–2023 en test **2024** (≤2024-12-31): dag-geclusterd netto t ≥ 2,0 in elk venster, netto mean > 0 in elk; N_train ≥ 150.
- Reserve **2025+ onaangeroerd** (D-084 / D-094.1; alleen CEO-vrijgave).
- Bij cost-gate PASS + formal: append TRIALS + TRIAL_COUNT +1; daarna `engine/ftmo.py` met **intradag-DD** (M5 trough in hold window → `daily_drawdowns`) per D-101 lat-B + Auditor.
- Bij FAIL: 1 trial (als cost-gate PASS), **geen klonen** (geen thr-/2s10s-/TLT-/overnight-variatie). Dead label `N124_YIELD_CURVE_2S10S`.

## 4. Verwachting / faalmodi
- Diag day_t≈1.89 < 2; 2021 year-split negatief → formal **FAIL_T** risk even if cost/stress PASS.
- Faalmodi: yield-curve / equity desync in 2024; correlatie met dode N116 TLT_DURATION (Auditor FDR: keep distinct — **Treasury slope level** ≠ TLT price ETF).
- Script: `scripts/n124_yield_curve_2s10s_gate.py`.

## 5. Onderscheid (bindend)
- ≠ **N116 TLT_DURATION_STRESS** FAIL_T (TLT price ≠ 10Y−3M slope)
- ≠ **N118 TIP_REALRATE_STRESS** FAIL_T / **N114 HYG** / **N100 EMB**
- ≠ RATE_CURVE / REIT_RATE / VNQ/TLT clones
- ≠ VIX / SECTOR_DISP / ORB / L60 / UKOIL-OVN / CORN / N75–N123 restarts

## 6. D-094a
Train 2021–2023. Reden **(b)**: US Treasury 10Y−3M slope z as risk-appetite / recession-timing into DM equity beta — literature curve–equity channel; distinct from TLT price stress. FTMO-M5 for costs. Herhaal in U2-runlog.
