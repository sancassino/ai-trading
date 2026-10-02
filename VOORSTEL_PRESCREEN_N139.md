# VOORSTEL_PRESCREEN_N139 — JP225_HK50_ASIA_XS Asia-morning session-flat (NEW_FAMILY BH)

**Status:** **geen PREREG — D-092.1 FAIL** `n138_n139` (N=240, mean **−1,97 < 12,42**; med −4,27; years −4,95 / +1,44 / −3,97; L/S 59/181). Not a clone of N108 (agree 0,55, cover 0,32), N105 (agree 0,51, cover 0,46), JP/AUS z-corr 0,34, or N64 (agree 0,06, cover 0,76). Screened 2026-10-03 ~00:46 CEST. NEW_FAMILY BH dead screen; no JP/HK or AUS-morning rewrite.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BH** (Nikkei–Hang Seng **Asia geographic basis**, two index CFDs, **Asia-morning** flat — Japan vs HK/China beta; **≠ N138** DAX/FTSE / **≠ N105** JP225 Tokyo→London continuation / **≠ N108** AUS200→London / **≠ N64** HK50 short TSMOM / **≠ N81** US pair RV).  
**Signal:** M5 day-close ratio **JP225cash / HK50cash**. **Trade:** both legs, equal bp.  
**Track 4 + D-100 + D-097 XS:** Nikkei rich vs Hang Seng mean-reverts when the basis is stretched. Flat inside the Asia cash morning so the hold is not the NY 15:30–21:00 template and not overnight.

**Gate (both est., not in `COSTS_FTMO.csv`):** all-hours M5 spread median 2024-01-01…2026-09-30, index commission **0**.  
JP225 **1,51** bp + HK50 **2,63** bp = **4,14** → gate 3 × 4,14 = **12,42** bp.  
(Session 03:00–08:00 medians not used.) Swap 0 (flat before the CET rollover). Binding RT = max(est, U2) on **each** leg before any PREREG.

**D-094a:** train 2021–2023. Reden **(b)**: both cash CFDs have M5 from 2021-01. Mechanism is an Asia cash basis during the local morning, not a London continuation and not a US-afternoon equity stress.

**Onderscheid:**
- ≠ **N138** GER40/UK100 XS (different region and clock — do not pool)
- ≠ **N105** JP225 Tokyo-AM → London continuation FAIL / **N108** AUS200 Asia-AM → London FAIL / **N64** HK50 TSMOM underpowered
- ≠ **N81** US100/US500 pair RV / **N103** GER→US30 / **N107** UK→FRA
- ≠ **N136** Brent–WTI / **N137** USDMXN / oil / PPLT / copper CFD / ETF→US500
- ≠ N75–N137 thr-grid / soft gate / overnight / NY-session rewrite of this rule

## Regel
**Signal (dag t, last M5 ≤ 22:00 CET on each leg):**
1. `ratio_t = JP225_close_t / HK50_close_t`.
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)` (ddof=0).
3. **basis fade:** `z40 > +1,5` → **SHORT JP225 + LONG HK50** (Nikkei rich); `z40 < −1,5` → **LONG JP225 + SHORT HK50**; else skip. Threshold frozen — no grid.

**Execution (dag t+1) — D-100 Asia-morning flat, both legs:**
4. Entry: first M5 ≥ **03:00 CET** (span ≤15 min) on **each** leg. Either missing → skip day.
5. Exit: flat ≤ **08:00 CET** same day on both. **No overnight. No 15:30 NY hold.**
6. PnL bp = sum of the two signed leg returns (equal weight). Non-overlapping (≤1 basket/day).

**Future clone bar (precommitted):** FAIL_CLONE if |z corr| vs GER40/UK100 ratio z40 ≥ 0,90, or (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N138 or vs a single-leg JP/HK lead-lag. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/JP225cash.csv.gz` + `data/m5gz/HK50cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **12,42** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N139 only after both RTs are in COSTS. FAIL → STOP (geen single-leg JP or HK rewrite, geen AUS200/N138 twin, geen NY 15:30 rewrite, geen thr-grid, geen overnight, geen soft gate).
