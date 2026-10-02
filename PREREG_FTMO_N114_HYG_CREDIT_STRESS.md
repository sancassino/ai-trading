# PREREG_FTMO_N114 — HYG_CREDIT_STRESS → US500cash session-flat (NEW_FAMILY AI)

**Status:** **OPEN** — frozen for U2 cost-gate + formal trial (CTO **C-037** Lane-B DIAG_PASS 2026-10-02 ~23:05 CEST).  
**Auteur:** CTO (Grok) on `grok/cto-1`, from Strateeg `VOORSTEL_PRESCREEN_N114.md` (Faraday `791a17c`).  
**Signal:** Yahoo/proxy **HYG** (US domestic high-yield). **Trade:** `US500cash`. **NEW_FAMILY AI** (≠ N100 EMB_CREDIT_STRESS / N113 SILVER_GOLD / N112 GAS).

Diagnostic (train 2021–2023, CTO C-037, 0 trials): N=**371**, mean bruto **+3.812 bp** ≥ gate **2.34**, day_t≈0.85, h1 +2.50 / h2 +5.12 → **DIAG_PASS** (N≥150 ∧ mean≥gate).  
Gate smoke (same script, not a trial): cost **PASS** / stress **PASS** (3.81≥3.51); formal t_nw≈0.71 ≪2; test 2024 mean bruto −2.16 → **elevated FAIL_T risk**; do **not** retune.

## 1. Bevroren regel
- Data: `data/daily/HYG.csv` (close) + `data/m5gz/US500cash.csv.gz`. Dagen ma–vr. Tijden = brokerservertijd (CET-proxy).
- Signal dag t: `z120 = (HYG_t − mean_120(HYG)) / stdev_120(HYG)`; `d20 = HYG_t / HYG_{t−20} − 1`.
- **combo:** `(z120 > +0,5) ∧ (d20 > 0)` → **LONG**; `(z120 < −0,5) ∧ (d20 < 0)` → **SHORT**; else skip.
- Execution dag t+1 on US500cash — D-100 session-flat:
  - Entry: close of first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
  - Exit: flat ≤ **21:00 CET** same day. **No overnight. No stop.** Max 1 trade/dag.
- Geen thr-grid, geen LQD twin, geen EMB rewrite, geen overnight, geen soft gate, geen US100 remap.

## 2. Kosten en poort
- RT **0,78 bp** (`COSTS_FTMO` US500cash); session-flat → swap = 0.
- Gate: mean bruto ≥ **3 × 0,78 = 2,34 bp**/trade op train 2021–2023, **N ≥ 150**.
- Stress: +50% roundtrip (mean ≥ **3,51 bp**) vóór formal t.

## 3. Beslisregel
- Train 2021–2023 en test **2024** (≤2024-12-31): dag-geclusterd netto t ≥ 2,0 in elk venster, netto mean > 0 in elk; N_train ≥ 150.
- Reserve **2025+ onaangeroerd** (D-084 / D-094.1; alleen CEO-vrijgave).
- Bij cost-gate PASS + formal: append TRIALS + TRIAL_COUNT +1; daarna `engine/ftmo.py` met **intradag-DD** (M5 trough in hold window → `daily_drawdowns`) per D-101 lat-B + Auditor.
- Bij FAIL: 1 trial (als cost-gate PASS), **geen klonen** (geen thr-/LQD-/EMB-/overnight-variatie). Dead label `N114_HYG_CREDIT_STRESS`.

## 4. Verwachting / faalmodi
- Prior zwak: diag day_t≈0.85 ≪ 2; smoke formal t_nw≈0.71; test 2024 negatief → formal **FAIL_T** waarschijnlijk ondanks cost/stress PASS.
- Faalmodi: 2024 HY–equity desync; correlatie met dode N100 EMB (Auditor FDR: keep distinct — **US domestic HY** ≠ EM hard-currency EMB).
- Script: `scripts/n114_hyg_credit_stress_gate.py`.

## 5. Onderscheid (bindend)
- ≠ **N100 EMB_CREDIT_STRESS** FAIL_T (EM hard-currency bond ETF ≠ US domestic HY)
- ≠ **N112 GAS_EQUITY_MACRO** FAIL_T / **N113 SILVER_GOLD_RATIO** FAIL_COST_GATE
- ≠ **N93 SECTOR_DISP** / **N78 VIX_TERM** / ORB / L60 / UKOIL-OVN / CORN / N75–N113 restarts
- ≠ FX LO carry / DXY Lon→EU / EURUSD→US500 (N115)

## 6. D-094a
Train 2021–2023. Reden **(b)**: US HY credit level+trend (HYG) as domestic risk-appetite timing into DM equity beta — literature credit–equity co-movement; distinct from EMB. FTMO-M5 for costs. Herhaal in U2-runlog.
