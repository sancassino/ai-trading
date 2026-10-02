# VOORSTEL_PRESCREEN_N138 — GER40_UK100_XS session-flat (NEW_FAMILY BG)

**Status:** **geen PREREG — D-092.1 FAIL_CLONE** `n138_n139` (N=178, mean **−4,09 < 6,42**; med −5,85; years — / −3,22 / −4,74; L/S 67/111). **FAIL_CLONE** of EU50/UK z40 (sign-agree **1,00**, cover **0,78**; z-corr 0,89 < 0,90). Not N103 (agree 0,51, cover 0,41) and not N107 (agree 0,51, cover 0,38). No 2021 15:30 fill (GER40 15:30 starts 2021-12-28); N=178 is 2022–23, still ≥150. Screened 2026-10-03 ~00:46 CEST. NEW_FAMILY BG dead screen; no EU50/UK or GER/UK rewrite.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BG** (DAX–FTSE **geographic equity basis**, two index CFDs, session-flat — eurozone vs UK cash basis; **≠ N81** US100/US500 pair RV / **≠ N103** GER→US30 lead-lag / **≠ N107** UK→FRA continuation / **≠ N136** Brent–WTI / **≠ ETF→US500** stress).  
**Signal:** M5 day-close ratio **GER40cash / UK100cash**. **Trade:** both legs, equal bp.  
**Track 4 + D-100 + D-097 XS:** GER rich vs UK mean-reverts when the basis is stretched; intradag-vlak (no overnight, no swap-credit).

**Gate:** GER40 RT **0,72** (`COSTS_FTMO.csv`) + UK100 RT **est. 1,42** (not in COSTS).  
UK100 est. = all-hours M5 spread median **1,42 bp** over 2024-01-01…2026-09-30 (same method as the COSTS spread column; index commission **0**, as GER40/US500). Session 15:30–21:00 median **1,06 bp, not used**.  
RT sum **2,14** → gate 3 × 2,14 = **6,42** bp. Swap 0 (session-flat). No single-leg cherry-pick. Binding UK100 RT = max(est, U2) before any PREREG.

**D-094a:** train 2021–2023. Reden **(b)**: both cash CFDs have M5 from 2021-01. Mechanism is a geographic index basis, not a US pair RV and not a morning lead-lag.

**Onderscheid:**
- ≠ **N81** US100/US500 3d pair RV DIAG_FAIL (US mega-cap pair ≠ DAX/FTSE; this is session-flat, not a 3d hold)
- ≠ **N103** GER40→US30 industrial lead-lag FAIL_STRESS / **N107** UK100→FRA40 continuation FAIL
- ≠ **N136** Brent–WTI XS FAIL (crude location basis ≠ equity geographic basis)
- ≠ **N105/N108** Asia→London continuation / **N64** HK50 TSMOM
- ≠ N75–N137 ETF-level→US500 / oil XS / EM FX fade / thr-grid / overnight / PPLT CFD

## Regel
**Signal (dag t, last M5 ≤ 22:00 CET on each leg):**
1. `ratio_t = GER40_close_t / UK100_close_t`.
2. `z40 = (ratio_t − mean_40(ratio)) / stdev_40(ratio)` (ddof=0).
3. **basis fade:** `z40 > +1,5` → **SHORT GER40 + LONG UK100** (DAX rich); `z40 < −1,5` → **LONG GER40 + SHORT UK100**; else skip. Threshold frozen — no grid.

**Execution (dag t+1) — D-100 session-flat, both legs:**
4. Entry: first M5 ≥ **15:30 CET** (span ≤15 min) on **each** leg. Either missing → skip day.
5. Exit: flat ≤ **21:00 CET** same day on both. **No overnight.**
6. PnL bp = sum of the two signed leg returns (equal weight). Non-overlapping (≤1 basket/day).

**Future clone bar (precommitted):** FAIL_CLONE if |z corr| vs US100/US500 ratio z40 ≥ 0,90, or (sign agree ≥ 0,85 AND cover ≥ 0,70) vs that US pair or vs a single-leg GER/UK lead-lag. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/GER40cash.csv.gz` + `data/m5gz/UK100cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **6,42** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N138 only after UK100 RT is in COSTS (binding = max(1,42, measured)). FAIL → STOP (geen single-leg GER or UK rewrite, geen FRA40 twin, geen US100/US500 pair rewrite, geen thr-grid, geen overnight, geen soft gate).
