# VOORSTEL_PRESCREEN_N160 — XAG_NY_IMPULSE_FADE session-flat (NEW_FAMILY CC)

**Status:** **OPEN** — D-092.1 refill after N158 FAIL / N159 FAIL (filed 2026-10-03 ~01:53 CEST). Not screened this cycle.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY CC** (silver **NY-hour impulse fade**, one metal CFD, session-flat). Round-trip is in `COSTS_FTMO.csv`. Not a gold/index pair. Not an FX book. Not a G10 cross. Not metal–oil (no oil leg). Not silver/index (no index leg). Not an equity-factor z→US500. Not an oil sleeve. Not a GER40 session.  
**Signal:** M5 impulse on **XAGUSD** 15:30→17:00 CET. **Trade:** the same leg, flat by 21:00.  
**Track 2 + D-100:** the NY metals hour overshoots silver; fade it inside the same cash session. Flat before the roll so neither silver swap is the alpha.

**Gate (`COSTS_FTMO.csv`):** XAGUSD RT **5,07** → gate 3 × 5,07 = **15,21** bp. Swap 0 (session-flat). No XAU substitute. No US30 leg. No UKOIL leg.

**D-094a:** train 2021–2023. Reden **(b)**: XAGUSD M5 from 2021-01. Mechanism is a same-day silver fade of the NY hour, not the London AM-fix fade, not a silver/Dow basis, and not silver versus oil.

**Onderscheid:**
- ≠ **N161** XLK→US100 tech-stress (other OPEN; this is one silver leg, not a sector ETF into Nasdaq; do not pool)
- ≠ **N158** USOIL NY-fade / **N159** GER40 Europe-close (prior cycle; different instrument)
- ≠ **N82** XAG London AM-fix fade (impulse is 15:30→17:00, flat 21:00; not 08:00→10:30 flat 13:00)
- ≠ **N150** XAG/US30 / **N141** XAG/UKOIL / **N75** XAU/XAG / **N113** SLV→US500 (one leg; no index, no oil, no gold, no US500)
- ≠ **N25** XAU NY-afternoon fade (silver, not gold; signal is the NY hour itself, not the 18:00 deviation)
- ≠ **N156/N157** gold/index (dead; no gold leg, no index leg)
- ≠ oil-overnight / GER40-session / FX-cross / factor→US500

## Regel
**Signal (dag t, XAGUSD):**
1. `P0` = first M5 ≥ **15:30 CET** (span ≤15 min). `P1` = first M5 ≥ **17:00 CET** (span ≤15 min). Either missing → skip.
2. `ny_bp = 1e4 × (P1 / P0 − 1)`.
3. **fade:** `ny_bp ≥ +40` → **SHORT** at P1; `ny_bp ≤ −40` → **LONG** at P1; else skip. Threshold frozen — no grid.

**Execution (same day) — D-100 session-flat:**
4. Entry = that 17:00 bar. Exit: last M5 ≤ **21:00 CET**. **No overnight.**
5. PnL bp = signed return of the one leg. Non-overlapping (≤1 trade/day).

**Future clone bar (precommitted):** FAIL_CLONE if (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N82's London-fade day-sign, vs the XAG leg of N150, vs the XAG leg of N141, vs N75's silver side, or vs N113's silver day-sign. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/XAGUSD.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **15,21** bp, **N ≥ 150**.
- PASS → PREREG. FAIL → STOP (geen XAU twin, geen US30 leg, geen oil leg, geen US500 remap, geen thr-grid, geen overnight, geen soft gate).
