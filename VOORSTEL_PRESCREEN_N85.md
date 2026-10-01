# VOORSTEL_PRESCREEN_N85 — US500 AM lead → US100 same-dir PM lag (NEW_FAMILY J; D-094a/D-100)

**Status:** **OPEN** — awaiting D-092.1 (**D-094** + Lane-B replace after N80 FAIL_COST_GATE; filed 2026-10-01 ~13:25 CEST).  
**Auteur:** Strateeg (Grok).  
**Signal:** `US500cash` (lead). **Trade:** `US100cash` (RT **0,66** bp; swap 0 — **EOD flat**).  
**NEW_FAMILY J:** **index lead–lag non-ratio** — US500 morning impulse → US100 afternoon continuation, same-day flat — ≠ N2 twin relative morning, ≠ N81 3d pair RV DIAG_FAIL, ≠ N83 DXY→US100, ≠ IDX_SHORT.

**Track 2 + D-100:** **intradag-vlak** on US100 (swap = 0). Lead measured on US500; **no ratio / no pair hedge** (single US100 leg).

**Gate:** 3 × US100 RT = 3 × 0,66 = **1,98** bp.

**D-094a:** train 2021–2023. Reden **(b)**: large-cap cash index often leads tech/nasdaq beta into the US cash session; trading the **lagging** name on a delayed entry is a classic lead–lag microstructure effect, not relative-value ratio MR. FTMO-M5 both series. Herhaal in PREREG. Pool note: single trade leg (US100) — mechanisme (b) + ≥3y FTMO.

**Onderscheid:**
- ≠ **N2** US100↔US500 relative morning FAIL (simultaneous relative; both names)
- ≠ **N81** US100/US500 pair RV 3d overnight DIAG_FAIL (**ratio/pair**; multi-night)
- ≠ **N83** DXY overnight → US100 opposite (macro USD signal; not equity lead)
- ≠ **N14** US100 pre-market mom FAIL; ≠ **N18/N5** gap cont/fade on own index
- ≠ **IDX_SHORT** L20 overnight FAIL_COST; ≠ N78 VIX→US100 dead
- ≠ ORB / L60 FX / classic TSMOM / CORN

## Regel
1. At **15:35 CET** (US cash open proxy): `lead_bp = 1e4 × (US500_mid_1535 / US500_close_prior_2200 − 1)`.
2. Trade only if `|lead_bp| ≥ 25`.
3. **Same-direction US100 lag:** lead ≥ +25 → **LONG** US100; lead ≤ −25 → **SHORT** US100.
4. Entry: US100 close of first M5 in **[17:00, 17:15] CET** (afternoon lag window). If missing, skip day.
5. Exit: flat at **21:00 CET** same day. **No overnight.**
6. Stop (formal): 1,0 × ATR14(D1 prior) US100. Non-overlapping (≤1/day).

## Pre-screen
- Data: `data/m5gz/US500cash.csv.gz` + `data/m5gz/US100cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **1,98** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N85. FAIL → STOP (geen lead-threshold grid, geen US30 twin, geen overnight hold, geen ratio/pair rewrite → N81 clone).
