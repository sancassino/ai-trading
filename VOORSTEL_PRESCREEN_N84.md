# VOORSTEL_PRESCREEN_N84 — AUDNZD rate-diff stretch fade, same-day flat (NEW_FAMILY I; D-097/D-100)

**Status:** **OPEN** — awaiting D-092.1 (**D-094** + Lane-B replace after N80 FAIL_COST_GATE; filed 2026-10-01 ~13:25 CEST).  
**Auteur:** Strateeg (Grok).  
**Instrument:** `AUDNZD` (RT **est. 1,06** bp = M5 spread_med **0,64** bp 2024–26 + 2×€2,25/lot/kant ≈ **0,21** bp; **not yet in** `COSTS_FTMO.csv` — U2 remeasure before any PREREG). Swap irrelevant — **EOD flat**.  
**NEW_FAMILY I:** **AUD–NZD rate-differential / cross stretch fade**, London session, same-day flat — ≠ L60 FX-med (C-028 barred), ≠ N69/N71 NZD/AUD USD-legs DIAG_FAIL, ≠ N77 FX6 XS, ≠ carry-TSMOM long-only.

**Track 2 + 4 (carry/RV) + D-100:** **intradag-vlak** (swap = 0). Rate-diff proxy = AUDNZD level vs 20d MA (RBA vs RBNZ cash-spread proxy without external rate feed).

**Gate:** 3 × RT_est = 3 × 1,06 = **3,18** bp. No D-097 50-floor on pure intradag. Binding RT = max(est, U2-remeasured) at PREREG time.

**D-094a:** train 2021–2023 (AUDNZD m5gz from 2021-01). Reden **(b)**: AUDNZD is the liquid FTMO cross that embeds the AU–NZ policy-rate differential; stretch fade is a known commodity-FX / rates relative effect, distinct from USD-pair TSMOM and from L60/H10 single-pair med trends. FTMO-M5 = uitvoering. Herhaal in PREREG.

**Onderscheid:**
- ≠ **N69** NZDUSD 10d carry+trend DIAG_FAIL (USD-leg; multi-night)
- ≠ **N71** GBPUSD SO / AUDUSD family B clones
- ≠ **N77** FX6 vol-timed XS rank-reversal DIAG_FAIL (basket XS; 5d overnight)
- ≠ **N72–N74 / USDJPY_MED** L60/H10 (C-028 BARRED — this is **intradag fade**, not L60 trend)
- ≠ **B1** month TSMOM; ≠ ORB / VIX_TERM / ENERGY / UKOIL OVN-gap (N80 dead)
- ≠ N46/N47 Lon-Asia fades BARRED (other pairs / C-021)

## Regel
1. Prior day close ≤ **22:00 CET**: `C_ref`, and `MA20` = mean of last 20 day-closes of AUDNZD.
2. At **08:00 CET**: `stretch_bp = 1e4 × (mid_0800 / MA20 − 1)`.
3. Trade only if `|stretch_bp| ≥ 40`.
4. **Fade:** stretch ≥ +40 → **SHORT**; stretch ≤ −40 → **LONG**. Entry = close of 08:00 signal bar (or first M5 in [08:00, 08:15]).
5. Exit: flat at **16:00 CET** same day. **No overnight.**
6. Stop (formal): 1,0 × ATR14(D1 prior). Non-overlapping (≤1/day).

## Pre-screen
- Data: `data/m5gz/AUDNZD.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **3,18** bp (or 3×U2-RT if higher), **N ≥ 150**.
- PASS → PREREG_FTMO_N84 (only after RT landed in COSTS). FAIL → STOP (geen stretch-threshold grid, geen AUDUSD twin, geen overnight hold, geen L60 fork).
