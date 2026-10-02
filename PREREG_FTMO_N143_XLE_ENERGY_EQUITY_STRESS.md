# PREREG_FTMO_N143 — XLE_ENERGY_EQUITY_STRESS → US500cash session-flat (NEW_FAMILY BL)

**Status:** **OPEN** — frozen for U2 cost-gate + formal trial (CTO **C-041** Lane-B DIAG_PASS 2026-10-03 ~01:03 CEST).  
**Auteur:** CTO (Grok) on `grok/cto-1`, from Faraday `VOORSTEL_S2_XLE_ENERGY_EQUITY_STRESS.md` (S2 `5a21939` cycle_0047; Faraday tip `e1bf004`).  
**Signal:** Yahoo/proxy **XLE** level. **Trade:** `US500cash` only. **NEW_FAMILY BL** (≠ ENERGY_TSMOM / N112 GAS / N101 CRACK / N98 USOIL→US100 / N134 XLF / N140 XAU–UKOIL / N142 US30/US500).

Diagnostic (train 2021–2023, CTO C-041, 0 trials): N=**356**, mean bruto **+7.856 bp** ≥ gate **2.34**, day_t≈1.81, med +5.92, h1 +12.46 / h2 +3.26, years 2021 −5.17 / 2022 +14.15 / 2023 +4.56, L/S 117/239 → **DIAG_PASS** (N≥150 ∧ mean≥gate).  
Gate smoke (same script, not a trial): cost **PASS** / stress **PASS** (7.86≥3.51); t_nw≈1.56; test 2024 mean bruto +6.83 t_nw≈1.25 → **elevated FAIL_T risk**; do **not** retune.

## 1. Bevroren regel
- Data: `data/daily/XLE.csv` (adjclose/close) + `data/m5gz/US500cash.csv.gz`. Dagen ma–vr. Tijden = brokerservertijd (CET-proxy).
- Signal dag t: `z40 = (XLE_t − mean_40(XLE)) / stdev_40(XLE)` (rolling min_periods = 40; ddof=0).
- **fade_extreme:** `z40 > +1,0` → **SHORT** US500; `z40 < −1,0` → **LONG** US500; else skip. Threshold frozen from S2 — **no thr-grid**.
- Execution dag t+1 on US500cash — D-100 session-flat:
  - Entry: close of first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
  - Exit: flat ≤ **21:00 CET** same day. **No overnight. No US100. No stop.** Max 1 trade/dag.
- Signal-only sector ETF — no XLE CFD leg, no oil CFD leg.
- Geen thr-grid, geen US100 overnight remap, geen UNG/CRACK/XLF rewrite, geen soft gate, geen overnight.

## 2. Kosten en poort
- RT **0,78 bp** (`COSTS_FTMO` US500cash); session-flat → swap = 0.
- Gate: mean bruto ≥ **3 × 0,78 = 2,34 bp**/trade op train 2021–2023, **N ≥ 150**.
- Stress: +50% roundtrip (mean ≥ **3,51 bp**) vóór formal t.

## 3. Beslisregel
- Train 2021–2023 en test **2024** (≤2024-12-31): dag-geclusterd netto t ≥ 2,0 in elk venster, netto mean > 0 in elk; N_train ≥ 150.
- Reserve **2025+ onaangeroerd** (D-084 / D-094.1; alleen CEO-vrijgave).
- Bij cost-gate PASS + formal: append TRIALS + TRIAL_COUNT +1; daarna `engine/ftmo.py` met **intradag-DD** (M5 trough in hold window → `daily_drawdowns`) per D-101 lat-B + Auditor.
- Bij FAIL: 1 trial (als cost-gate PASS), **geen klonen** (geen thr-/US100-/oil-CFD-/overnight-variatie). Dead label `N143_XLE_ENERGY_EQUITY_STRESS`.

## 4. Verwachting / faalmodi
- Diag day_t≈1.81 ≪ 2; 2021 year-split negative (−5.17) → formal **FAIL_T** risk even if cost/stress PASS.
- Lane-A day_t 2.29 / mean 5.41 was overnight hold=1d proxy — **not** this session-flat rule; do not soft-pass from Lane-A.
- Faalmodi: energy-equity stress desync with SPX session; correlatie met dode N112 GAS / N134 XLF / N98 USOIL (Auditor FDR: keep distinct — **XLE level fade** ≠ natgas / financials / crude→US100).
- Script: `scripts/n143_xle_energy_equity_stress_gate.py`.

## 5. Onderscheid (bindend)
- ≠ **ENERGY_TSMOM** (UKOIL+USOIL L20/H10 LO, FAIL_COST_GATE)
- ≠ **N112 GAS** / UNG→US500 / natgas CFD
- ≠ **N101 CRACK** (HO/BRENT → US100)
- ≠ **N98** USOIL Lon-AM → US100
- ≠ **N134** XLF_FINANCIAL_STRESS / **N122** DBC / **N140** XAU–UKOIL / **N141** XAG–UKOIL
- ≠ **N142** US30/US500 two-leg basis (DIAG_FAIL this cycle; do not pool)
- ≠ **N124** YIELD / **N125** DEFENSIVE / VIX / ORB / L60 / UKOIL-OVN / CORN / N75–N142 restarts

## 6. D-094a
Train 2021–2023. Reden **(b)**: energy-equity sector stress into broad cash index — literature sector-stress / risk-appetite channel; distinct from crude CFD and from financials (XLF). Binding window is FTMO-M5 on US500. Herhaal in U2-runlog.
