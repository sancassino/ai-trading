# VOORSTEL_PRESCREEN_N135 — QUAL_QUALITY_STRESS → US500cash session-flat (NEW_FAMILY BD)

**Status:** **geen PREREG — DIAG_FAIL** — CTO C-040 `c040_lane_b_diag` train N=**211** mean bruto **−5,03** < gate **2,34** (med −6,86; day_t −1,04; years +10,50/−4,31/−9,58); screened 2026-10-03 ~00:30 CEST. Dead screen; no QUAL/MTUM/EQW/IWM clone. No thr-grid / overnight / soft gate.
**Auteur:** Strateeg (Grok). **NEW_FAMILY BD** (US **quality-factor** ETF stress → equity session-flat — profitability/low-leverage channel; **≠ MTUM** momentum / **≠ EQW** breadth ratio / **≠ XLU** defensive / **≠ USMV** min-vol).  
**Signal:** Yahoo/proxy **QUAL**. **Trade:** `US500cash` (RT **0,78** bp; swap 0 — **session-flat**).  
**Track 4 + D-100 + D-097 XS:** Quality-factor extremes as a balance-sheet regime for the US cash session; intradag-vlak.

**Gate:** 3 × US500 RT = 3 × 0,78 = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: QUAL history from 2013 (≥5y); binding window is FTMO-M5 costs. Quality **level** is not momentum (N132), not RSP/SPX breadth (N130), not low-vol/defensive sector.

**Onderscheid:**
- ≠ **N132 MTUM** D-092.1 FAIL (momentum factor ≠ quality factor)
- ≠ **N130 EQW** FAIL_T (breadth ratio ≠ quality ETF level)
- ≠ **N125 XLU/XLI** / USMV min-vol
- ≠ **N119 IWM** / **N93 SECTOR_DISP** / **N134 XLF** (banks ≠ quality basket)
- ≠ N75–N133 clones / thr-grid / soft gate / overnight US100

## Regel
**Signal (dag t):**
1. `z40 = (QUAL_t − mean_40(QUAL)) / stdev_40(QUAL)`.
2. **stress_buy:** `z40 > +1,5` → **SHORT** US500 (quality blow-off); `z40 < −1,5` → **LONG** (quality washout); else skip.

**Execution (dag t+1, US500cash) — D-100 session-flat:**
3. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
4. Exit: flat ≤ **21:00 CET** same day. **No overnight.**
5. Non-overlapping (≤1/day).

## Pre-screen
- Data: `data/daily/QUAL.csv` + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **2,34** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N135. FAIL → STOP (geen MTUM/EQW rewrite, geen USMV/XLU twin, geen thr-grid, geen overnight, geen soft gate).
