# VOORSTEL_PRESCREEN_N125 — DEFENSIVE_CYCLICAL → US500cash session-flat twin (NEW_FAMILY AT)

**Status:** **PASS → PREREG** — D-092.1 `n124_n125` train N=**478** mean bruto **+5,48** ≥ gate **2,34** (filed 2026-10-02 ~23:56 CEST). Live: `PREREG_FTMO_N125_DEFENSIVE_CYCLICAL.md`.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY AT** from S2 `13fe10c` cycle_2346.  
**Signal:** Yahoo/proxy **XLU/XLI** relative. **Trade:** `US500cash` (**US500 twin** per S2 FLAG — not US100 overnight).  
**Track 4 + D-100:** Defensive-vs-cyclical relative as risk-appetite timing; intradag-vlak (geen swap).

**Gate:** 3 × US500 RT = 3 × 0,78 = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: XLU/XLI relative ≠ SECTOR_DISP XL* dispersion (N93 DEAD). FTMO-M5 for costs. S2 FLAG → US500 twin.

**Onderscheid:**
- ≠ **N93 SECTOR_DISP** FAIL_COST_GATE (dispersion ≠ relative level)
- ≠ **N119 IWM** / **N81** pair RV / ORB / L60
- ≠ US100 overnight long (S2 FLAG swap-hostile) / sector CFD / N75–N123 clones

## Regel
**Signal (dag t):**
1. `ratio = XLU_adj / XLI_adj`; `z40` (min_periods=max(20,13)).
2. **defensive_high:** `z40 > +0,5` → **SHORT**; `z40 < −0,5` → **LONG**; else skip.

**Execution (dag t+1, US500cash) — D-100 session-flat:**
3. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
4. Exit: flat ≤ **21:00 CET** same day. **No overnight. No US100 rewrite.**
5. Non-overlapping (≤1/day).

## Pre-screen result
- Data: `XLU`/`XLI` + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- N=**478**, mean **+5,48**, med **+4,81**, years 2021 **+0,90** / 2022 **+8,84** / 2023 **+3,72** → **PASS_may_PREREG**.
- FAIL path (if U2 fails): STOP — geen thr-grid, geen US100 overnight rewrite, geen SECTOR_DISP clone, geen soft gate.
