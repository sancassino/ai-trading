# PREREG_FTMO_N92 — US100cash NY-Open 2h Momentum, intradag-flat (NEW_FAMILY Q)

**Status:** **OPEN** — frozen for U2 cost-gate + formal trial (CTO **C-031** Lane-B DIAG_PASS 2026-10-02 ~20:31 CEST).  
**Auteur:** CTO (Grok) on `grok/cto-1`, from Strateeg `VOORSTEL_PRESCREEN_N92.md` (Faraday).  
**Instrument:** `US100cash`. **NEW_FAMILY Q** (≠ ORB / N87 gap-fade / N89 GER40 2h-open).

Diagnostic (train 2021–2023, CTO C-031, 0 trials): N=592, mean bruto **+5.904 bp** ≥ gate **1.98**, day_t≈1.56, h1/h2 both >0 → **DIAG_PASS**. Formal t / test / stress still OPEN for U2.

## 1. Bevroren regel
- Data: `data/m5gz/US100cash.csv.gz`. Dagen ma–vr. Tijden = **brokerservertijd** (CET-proxy zoals VOORSTEL).
- `P_1530` = close van eerste M5-bar ≥ 15:30 (span ≤15 min).
- `P_1730` = close van eerste M5-bar ≥ 17:30 (span ≤15 min).
- `ret2h = (P_1730 − P_1530) / P_1530`.
- `ret2h > 0` → **LONG** op `P_1730`; `ret2h < 0` → **SHORT** op `P_1730`; `ret2h = 0` → skip.
- Exit: close van laatste M5-bar ≤ 22:00. **Intradag-flat** (geen overnight, geen swap). Geen stop. Max 1 trade/dag.
- Geen tijdvenster-grid, geen US500-switch, geen ORB-range, geen drempel op |ret2h|.

## 2. Kosten en poort
- RT **0,66 bp** (`COSTS_FTMO_alle` US100cash); intradag-flat → swap = 0.
- Gate: mean bruto ≥ **3 × 0,66 = 1,98 bp**/trade op train 2021–2023, **N ≥ 150**.
- Stress: +50% roundtrip (gate equivalent mean ≥ 2,97 bp) vóór formal t.

## 3. Beslisregel
- Train 2021–2023 en test **2024** (≤2024-12-31): dag-geclusterd netto t ≥ 2,0 in elk venster, netto mean > 0 in elk; N_train ≥ 150.
- Reserve **2025+ onaangeroerd** (D-084 / D-094.1; alleen CEO-vrijgave).
- Bij cost-gate PASS + formal: append TRIALS + TRIAL_COUNT +1; daarna `engine/ftmo.py` met **intradag-DD** (M5 trough in hold window → `daily_drawdowns`) per D-101 lat-B + Auditor.
- Bij FAIL: 1 trial, **geen klonen** (geen venster-/drempel-/US500-variatie). Dead label `N92_US100_NY_2H_MOM`.

## 4. Verwachting / faalmodi
- Prior matig: diag day_t≈1.56 < 2 → formal t kan FAIL_T ondanks cost-gate.
- Faalmodi: 2024 regime shift; open-auction noise; correlatie met dode ORB-familie (Auditor FDR-context: ORB closed as robust edge, but this is session-direction continuation not range breakout — keep distinct).
- Script: `scripts/n92_us100_ny_2h_mom_gate.py`.

## 5. Onderscheid (bindend)
- ≠ ORB / ORB-meta (D-104 FAIL) / ORB-index-ext
- ≠ N87 US30 gap-fade FAIL_T
- ≠ N89 GER40 EU 2h-open pre-FAIL
- ≠ N35/N41 EU→US continuation overnight
