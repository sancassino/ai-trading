# VOORSTEL_PRESCREEN_N83 — DXYcash overnight → US100 opposite intradag (NEW_FAMILY H; D-094a/D-100)

**Status:** **UNDERPOWERED** — C-030 (mean +15,36 ≥ 1,98 maar N=52≪150; DXY M5 short); **geen PREREG**; do not retune (2026-10-01 ~13:35 CEST).  
**Auteur:** Strateeg (Grok).  
**Signal:** `DXYcash` (dollar index CFD; signal-only). **Trade:** `US100cash` (RT **0,66** bp; swap 0 — **EOD flat**).  
**NEW_FAMILY H:** **macro DXY overnight → equity opposite**, same-day flat — ≠ N2 twin-index relative, ≠ N81 pair RV DIAG_FAIL, ≠ N78 VIX→US100 dead, ≠ IDX_SHORT overnight.

**Track 2 + D-100:** **intradag-vlak** on US100 (swap = 0). DXY not sized (signal).

**Gate:** 3 × US100 RT = 3 × 0,66 = **1,98** bp.

**D-094a:** train 2021–2023. Reden **(b)**: USD strength overnight as risk-off impulse into US equity open is a macro cross-asset session effect; DXY series long; FTMO-M5 for US100 uitvoering. Herhaal in PREREG. Pool note: single equity target (not ≥5 instruments) — mechanisme (b) + ≥3y FTMO + DXY proxy history.

**Onderscheid:**
- ≠ **N2** US100↔US500 relative morning FAIL (no DXY; twin equity)
- ≠ **N81** US100/US500 pair RV 3d DIAG_FAIL (overnight equity pair; not DXY)
- ≠ **N78** VIX_TERM→US100 FAIL_COST_GATE (vol structure; barred clones)
- ≠ **IDX_SHORT** L20 overnight FAIL_COST (no DXY; multi-night)
- ≠ N5/N18 index gap fade/cont (gap on equity itself, not DXY signal)
- ≠ L60 FX / ORB / classic TSMOM / CORN

## Regel
1. Prior DXY ref: close ≤ **22:00 CET** prior session (`D_ref`).
2. At **08:00 CET**: `dxy_gap_bp = 1e4 × (DXY_mid_0800 / D_ref − 1)`.
3. Trade only if `|dxy_gap_bp| ≥ 15`.
4. **Opposite US100:** dxy_gap ≥ +15 → **SHORT** US100; dxy_gap ≤ −15 → **LONG** US100.
5. Entry: US100 close of first M5 in [15:30, 15:45] CET (US cash open proxy). If missing, skip day.
6. Exit: flat at **17:30 CET** same day. **No overnight.**
7. Stop (formal): 1,0 × ATR14(D1 prior) US100. Non-overlapping (≤1/day).

## Pre-screen
- Data: `data/m5gz/DXYcash.csv.gz` + `data/m5gz/US100cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **1,98** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N83. FAIL → STOP (geen DXY-threshold grid, geen US500 twin, geen overnight hold, geen VIX substitute).
