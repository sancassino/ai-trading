# VOORSTEL_PRESCREEN_N164 — US2000_NY_IMPULSE_FADE session-flat (NEW_FAMILY CG)

**Status:** **OPEN** — D-094 refill after C-044 closed N162/N163 DIAG_FAIL_CLONE + N161 FAIL_T (filed 2026-10-03 ~23:21 CEST). Not cost-screened.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY CG** (Russell **2000 cash CFD** NY-hour impulse **fade**, one small-cap index leg, session-flat). Round-trip **not** in `COSTS_FTMO.csv` — honest M5 spread_med ≈ **3,14** bp (all-hours 2021–2026); U2 remeasure before any PREREG. Not an ETF→index stress book. Not US500/US100/US30. Not IWM→US500. Not a cash-close fade. Not AUD/oil/silver impulse.  
**Signal:** M5 impulse on **US2000cash** 15:30→17:00 CET. **Trade:** the same leg, flat by 21:00.  
**Track 2 + D-100 + family pivot:** after the XLK/sector→index FAIL_T streak, pivot to a **direct small-cap index CFD** (not a Yahoo ETF mapped into US500/US100). NY open overshoots Russell; fade inside the session. Flat before the roll.

**Gate (est.):** US2000cash RT_est **3,14** → gate 3 × 3,14 = **9,43** bp. Swap 0 (session-flat). Binding RT = max(est, U2) before PREREG. No US500/US100/US30 twin. No IWM remap.

**D-094a:** train 2021–2023. Reden **(b)**: US2000cash M5 from 2021-01 (true 5-min; n_train bars ≫150). Russell NY-hour |move| is larger than S&P (expect p50≳25 bp) — threshold **±35** frozen a priori on that scale (not chosen on PnL). Mechanism is a same-day fade of the Russell NY impulse, not IWM factor→US500, not the S&P cash-close window.

**Pre-file clone check (qualitative; not a cost screen):** not a filed clone by construction.  
≠ N119 IWM→US500 (other instrument; signal is Russell's own M5, not IWM z). ≠ N162 US500 cash-close (19:00→20:30; other window + other index). ≠ N92 US100 NY-2h mom (fade vs continuation; Russell ≠ Nasdaq). ≠ N87 US30 gap. ≠ N24 US500 lunch fade. ≠ N161 XLK→US100. ≠ N158/N160 oil/silver NY-fade.

**Same-family twins must not be filed after a clone hit:** US500/US100/US30 15:30→17:00 fade of the same window.

**Onderscheid:**
- ≠ **N161** XLK→US100 FAIL_T (no equity ETF signal; Russell CFD direct)
- ≠ **N119** IWM_SMALLCAP→US500 FAIL screen (trade leg is US2000cash, not US500)
- ≠ **N162** US500 cash-close DIAG_FAIL_CLONE / **N163** AUD NY-fade DIAG_FAIL_CLONE
- ≠ **N92** / **N24** / **N87** / large-cap NY books
- ≠ ETF→index stress family (kill-circuit pivot)

## Regel
**Signal (dag t, US2000cash):**
1. `P0` = first M5 ≥ **15:30 CET** (span ≤15 min). `P1` = first M5 ≥ **17:00 CET** (span ≤15 min). Either missing → skip.
2. `ny_bp = 1e4 × (P1 / P0 − 1)`.
3. **fade:** `ny_bp ≥ +35` → **SHORT** at P1; `ny_bp ≤ −35` → **LONG** at P1; else skip. Threshold frozen — no grid.

**Execution (same day) — D-100 session-flat:**
4. Entry = that 17:00 bar. Exit: last M5 ≤ **21:00 CET**. **No overnight.**
5. PnL bp = signed return of the one leg. Non-overlapping (≤1 trade/day).

**Future clone bar (precommitted):** FAIL_CLONE if (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N119's US500 side, vs N92, vs N24, vs N162's impulse sign, vs a US500/US100/US30 same-window fade. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/US2000cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **9,43** bp (or U2-remeasured 3×RT), **N ≥ 150**.
- PASS → PREREG. FAIL → STOP (geen US500/US100/US30 twin, geen IWM→US500 rewrite, geen thr-grid, geen overnight, geen soft gate).
