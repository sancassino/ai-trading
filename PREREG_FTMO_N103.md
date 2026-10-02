# PREREG_FTMO_N103 — GER40 Lon-AM → US30 NY industrial lead-lag, session-flat (NEW_FAMILY Z)

**Status:** **OPEN** — frozen for U2 cost-gate + formal trial (CTO **C-035** Lane-B DIAG_PASS 2026-10-02 ~22:05 CEST).  
**Auteur:** CTO (Grok) on `grok/cto-1`, from Strateeg `VOORSTEL_PRESCREEN_N103.md` (Faraday `edbd2ee`).  
**Signal:** `GER40cash` Lon-AM. **Trade:** `US30cash`. **NEW_FAMILY Z** (≠ N98 oil→tech / S2-GER_US_LEAD / N85 US500→US100 / N41 EU→US cont).

Diagnostic (train 2021–2023, CTO C-035, 0 trials): N=286, mean bruto **+1.749 bp** ≥ gate **1.35**, day_t≈0.38, h1 −1.92 / h2 +5.42 → **DIAG_PASS** (N≥150 ∧ mean≥gate). Formal t / test / stress still OPEN for U2. **Prior: weak day_t + h1/h2 flip → elevated FAIL_T risk; do not retune.**

## 1. Bevroren regel
- Data: `data/m5gz/GER40cash.csv.gz` + `data/m5gz/US30cash.csv.gz`. Dagen ma–vr. Tijden = brokerservertijd (CET-proxy).
- Lon-AM GER impulse: `ger_am_bp = 1e4 × (GER40_close@12:00 / GER40_close@08:00 − 1)` (first M5 in ±15 min windows).
- Trade only if `|ger_am_bp| ≥ 40`.
- Same-direction US30: ger_am ≥ +40 → **LONG** US30; ger_am ≤ −40 → **SHORT** US30.
- Entry: US30 close of first M5 in **[15:30, 15:45] CET**. If missing, skip day.
- Exit: flat at **21:00 CET** same day. **No overnight. No stop.** Max 1 trade/dag.
- Geen thr-grid, geen US100-substitute, geen GER→US-open rewrite, geen overnight, geen soft gate.

## 2. Kosten en poort
- RT **0,45 bp** (`COSTS_FTMO` US30cash); session-flat → swap = 0.
- Gate: mean bruto ≥ **3 × 0,45 = 1,35 bp**/trade op train 2021–2023, **N ≥ 150**.
- Stress: +50% roundtrip (gate equivalent mean ≥ 2,025 bp) vóór formal t.

## 3. Beslisregel
- Train 2021–2023 en test **2024** (≤2024-12-31): dag-geclusterd netto t ≥ 2,0 in elk venster, netto mean > 0 in elk; N_train ≥ 150.
- Reserve **2025+ onaangeroerd** (D-084 / D-094.1; alleen CEO-vrijgave).
- Bij cost-gate PASS + formal: append TRIALS + TRIAL_COUNT +1; daarna `engine/ftmo.py` met **intradag-DD** (M5 trough in hold window → `daily_drawdowns`) per D-101 lat-B + Auditor.
- Bij FAIL: 1 trial, **geen klonen** (geen thr-/US100-/GER-open-/overnight-variatie). Dead label `N103_GER40_LON_AM_US30_NY_INDUSTRIAL`.

## 4. Verwachting / faalmodi
- Prior zwak: diag day_t≈0.38 ≪ 2; h1 negatief → formal t waarschijnlijk FAIL_T ondanks cost-gate.
- Faalmodi: 2024 regime; EU/US industrial desync; correlatie met dode GER_US_LEAD / N98 (Auditor FDR: keep distinct — EU equity AM → US30 PM session-flat, not oil→tech and not GER→US cash-open).
- Script: `scripts/n103_ger40_us30_industrial_gate.py`.

## 5. Onderscheid (bindend)
- ≠ N98 USOIL→US100 DIAG_FAIL (olie→tech)
- ≠ S2-GER_US_LEAD STOP (GER Europe-AM → US open / US100)
- ≠ N85 US500→US100 DIAG_FAIL
- ≠ N41 / N35 EU→US continuation FAIL_T
- ≠ N93 SECTOR_DISP / VIX / ORB / L60 / UKOIL-OVN / CORN / NY-2h / N75–N102 restarts
