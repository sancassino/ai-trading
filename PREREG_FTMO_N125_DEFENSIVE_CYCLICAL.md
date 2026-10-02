# PREREG_FTMO_N125 — DEFENSIVE_CYCLICAL → US500cash session-flat (NEW_FAMILY AT)

**Status:** **OPEN** — frozen for U2 cost-gate + formal trial (CTO **C-039** Lane-B DIAG_PASS 2026-10-02 ~23:56 CEST).  
**Auteur:** CTO (Grok) on `grok/cto-1`, from S2 `VOORSTEL_S2_DEFENSIVE_CYCLICAL.md` (cycle_2346 `13fe10c`; US500 twin preferred over NDX short-bias). Faraday tip still `47e0eab`.  
**Signal:** Yahoo/proxy **XLU/XLI** relative. **Trade:** `US500cash`. **NEW_FAMILY AT** (≠ SECTOR_DISP multi-XL* dispersion / N93 SECTOR_DISP_ROTATION).

Diagnostic (train 2021–2023, CTO C-039, 0 trials): N=**478**, mean bruto **+5.479 bp** ≥ gate **2.34**, day_t≈1.43, h1 +6.31 / h2 +4.65, years 2021 +0.90 / 2022 +8.84 / 2023 +3.72 → **DIAG_PASS** (N≥150 ∧ mean≥gate).  
Gate smoke (same script, not a trial): cost **PASS** / stress **PASS** (5.48≥3.51); t_nw≈1.29; test 2024 mean bruto −2.32 t_nw≈−0.77 → **elevated FAIL_T risk**; do **not** retune.

## 1. Bevroren regel
- Data: `data/daily/XLU.csv` + `data/daily/XLI.csv` (adjclose/close) + `data/m5gz/US500cash.csv.gz`. Dagen ma–vr. Tijden = brokerservertijd (CET-proxy).
- Signal dag t: `rel = XLU/XLI`; `z40 = (rel_t − mean_40(rel)) / stdev_40(rel)` (rolling min_periods = max(20, 40//3)).
- **defensive_high:** `z40 > +0,5` → **SHORT** (defensive outperformance = risk-off); `z40 < −0,5` → **LONG**; else skip.
- Execution dag t+1 on US500cash — D-100 session-flat:
  - Entry: close of first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
  - Exit: flat ≤ **21:00 CET** same day. **No overnight. No stop.** Max 1 trade/dag.
- Geen thr-grid, geen XLP/XLY twin, geen NDX/US100 remap, geen overnight, geen soft gate, geen SECTOR_DISP rewrite.

## 2. Kosten en poort
- RT **0,78 bp** (`COSTS_FTMO` US500cash); session-flat → swap = 0.
- Gate: mean bruto ≥ **3 × 0,78 = 2,34 bp**/trade op train 2021–2023, **N ≥ 150**.
- Stress: +50% roundtrip (mean ≥ **3,51 bp**) vóór formal t.

## 3. Beslisregel
- Train 2021–2023 en test **2024** (≤2024-12-31): dag-geclusterd netto t ≥ 2,0 in elk venster, netto mean > 0 in elk; N_train ≥ 150.
- Reserve **2025+ onaangeroerd** (D-084 / D-094.1; alleen CEO-vrijgave).
- Bij cost-gate PASS + formal: append TRIALS + TRIAL_COUNT +1; daarna `engine/ftmo.py` met **intradag-DD** (M5 trough in hold window → `daily_drawdowns`) per D-101 lat-B + Auditor.
- Bij FAIL: 1 trial (als cost-gate PASS), **geen klonen** (geen thr-/XLPXLY-/US100-/overnight-variatie). Dead label `N125_DEFENSIVE_CYCLICAL`.

## 4. Verwachting / faalmodi
- Diag day_t≈1.43 ≪ 2; 2021 year-split weak → formal **FAIL_T** risk even if cost/stress PASS.
- Faalmodi: defensive/cyclical rotation desync with SPX session; correlatie met dode N93 SECTOR_DISP (Auditor FDR: keep distinct — **single pair relative** ≠ multi-sector dispersion).
- Script: `scripts/n125_defensive_cyclical_gate.py`.

## 5. Onderscheid (bindend)
- ≠ **N93 SECTOR_DISP_ROTATION** FAIL_COST_GATE (multi-XL* dispersion ≠ XLU/XLI pair relative)
- ≠ **N124 YIELD_CURVE** (this cycle) / TLT / TIP / HYG / EMB / VNQ / EEM / DBC / EFA
- ≠ VIX / ORB / L60 / UKOIL-OVN / CORN / N75–N123 restarts / GAS / SILVER

## 6. D-094a
Train 2021–2023. Reden **(b)**: utilities-vs-industrials relative as defensive/cyclical risk-appetite timing into DM equity beta — literature sector-rotation channel; distinct from SECTOR_DISP. Prefer US500 twin (POST-N78) over NDX short-bias. FTMO-M5 for costs. Herhaal in U2-runlog.
