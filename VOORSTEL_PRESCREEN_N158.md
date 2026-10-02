# VOORSTEL_PRESCREEN_N158 — USOIL_NY_IMPULSE_FADE session-flat (NEW_FAMILY CA)

**Status:** **OPEN** — D-092.1 refill after N156 FAIL / N157 FAIL (filed 2026-10-03 ~01:47 CEST). Not screened this cycle.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY CA** (WTI **NY-hour impulse fade**, one oil CFD, session-flat). Round-trip is in `COSTS_FTMO.csv`. Not a gold/index pair. Not an FX book. Not a G10 cross. Not silver/index. Not metal–oil (no bullion leg). Not an equity-factor z→US500. Not Brent–WTI. Not an index/oil pair.  
**Signal:** M5 impulse on **USOILcash** 15:30→17:00 CET. **Trade:** the same leg, flat by 21:00.  
**Track 2 + D-100:** the NY energy hour overshoots; fade it inside the same cash session. Flat before the roll so the short-side swap (~24,53 bp) is not the alpha.

**Gate (`COSTS_FTMO.csv`):** USOILcash RT **3,34** → gate 3 × 3,34 = **10,02** bp. Swap 0 (session-flat). No UKOIL substitute. No equity leg.

**D-094a:** train 2021–2023. Reden **(b)**: USOILcash M5 from 2021-01. Mechanism is a same-day WTI fade of the NY hour, not a London-AM Brent fade, not a Brent/WTI cross, and not oil→Nasdaq.

**Onderscheid:**
- ≠ **N156** XAU/GER40 / **N157** XAU/US100 (no gold leg; not a haven–index book)
- ≠ **N22** UKOIL Lon-AM fade (WTI, not Brent; impulse is 15:30→17:00, not 09:00→12:00)
- ≠ **N43** UKOIL NY-open continuation (opposite sign; Brent, not WTI)
- ≠ **N80** UKOIL overnight gap / **S2-USOIL** EIA breakout (no overnight; no event window; fade, not breakout)
- ≠ **N98** oil→US100 (the trade leg is WTI, not the Nasdaq)
- ≠ **N136** Brent/WTI XS / **N155** US30/UKOIL / **N140–N141** metal–oil (one leg; no second asset)
- ≠ **N159** GER40 Europe-close fade (other OPEN; do not pool)

## Regel
**Signal (dag t, USOILcash):**
1. `P0` = first M5 ≥ **15:30 CET** (span ≤15 min). `P1` = first M5 ≥ **17:00 CET** (span ≤15 min). Either missing → skip.
2. `ny_bp = 1e4 × (P1 / P0 − 1)`.
3. **fade:** `ny_bp ≥ +40` → **SHORT** at P1; `ny_bp ≤ −40` → **LONG** at P1; else skip. Threshold frozen — no grid.

**Execution (same day) — D-100 session-flat:**
4. Entry = that 17:00 bar. Exit: last M5 ≤ **21:00 CET**. **No overnight.**
5. PnL bp = signed return of the one leg. Non-overlapping (≤1 trade/day).

**Future clone bar (precommitted):** FAIL_CLONE if (sign agree ≥ 0,85 AND cover ≥ 0,70) vs N22's UKOIL day-sign, vs N43's UKOIL day-sign, vs N80's gap sign, vs N98's oil-morning sign, or vs the USOIL leg of N136. A clone is not a PASS.

## Pre-screen
- Data: `data/m5gz/USOILcash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **10,02** bp, **N ≥ 150**.
- PASS → PREREG. FAIL → STOP (geen Brent twin, geen index leg, geen gold leg, geen FX leg, geen thr-grid, geen overnight, geen soft gate).
