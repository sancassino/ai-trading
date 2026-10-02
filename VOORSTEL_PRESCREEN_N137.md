# VOORSTEL_PRESCREEN_N137 — USDMXN_EM_CARRY_FADE session-flat (NEW_FAMILY BF)

**Status:** **OPEN** — D-094 refill after N134/N135 D-092.1 FAIL (filed 2026-10-03 ~00:29 CEST). Not screened this cycle.  
**Auteur:** Strateeg (Grok). **NEW_FAMILY BF** (MXN **high-carry EM** stress fade, NY session-flat — peso-crash rebound; **≠ G10 5d LO carry** N90–N111 / **≠ N84** AUDNZD rate-diff / **≠ N77** FX6 XS / **≠ N110** DXY).  
**Signal + trade:** `USDMXN` (M5 from 2021-01-04). **Not in `COSTS_FTMO.csv`** — RT is an estimate; U2 remeasure before any PREREG. Binding RT = max(est, U2).  
**Track 4 + D-100 + D-097 carry:** A multi-day USD/MXN jump is a carry unwind; the next NY cash session fades it. Intradag-vlak (no overnight MXN swap).

**Gate (estimate, all-hours spread, COSTS method):**  
M5 2024-01-01…2026-09-30 spread median **2,47 bp** (session 15:30–21:00 median 1,88 bp, not used). Commission est. **0,24 bp/side** = €2,25 / (100k USD ÷ ~1,08) .  
RT_est = 2,47 + 2×0,24 = **2,96 bp** → gate 3 × 2,96 = **8,88 bp**. Swap 0 (EOD flat).

**D-094a:** train 2021–2023. Reden **(b)**: USDMXN M5 covers the FTMO train window (USDZAR starts 2022 — not used). Mechanism is EM carry-crash fade, not a G10 pair fork of the dead 5d LO set.

**Onderscheid:**
- ≠ **N90/N94/N96/N99/N102/N104/N106/N109/N111** 5d LO carry+mom (overnight G10; this is **one NY session**, EM, one-sided fade)
- ≠ **N84 AUDNZD** stretch DIAG_FAIL (AU–NZ commodity-FX cross ≠ MXN high-carry)
- ≠ **N77** FX6 vol-timed XS / **N28** EURJPY Lon→NY / L60 FX-med BARRED
- ≠ **N110/N131 DXY** / **N115 EURUSD→US500**
- ≠ N75–N135 equity-ETF z40→US500 / thr-grid / soft gate / overnight

## Regel
**Signal (dag t, last M5 ≤ 22:00 CET):**
1. `ret5_bp = 1e4 × (C_t / C_{t−5} − 1)` on USDMXN day-close.
2. **Only the crash-fade side:** `ret5_bp ≥ +150` → **SHORT** USDMXN next session (buy MXN after a USD spike); else skip. No long-USD leg. Threshold **150 bp frozen** — no grid.

**Execution (dag t+1) — D-100 session-flat:**
3. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
4. Exit: flat ≤ **21:00 CET** same day. **No overnight.**
5. Non-overlapping (≤1/day).

## Pre-screen
- Data: `data/m5gz/USDMXN.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **8,88** bp (or 3×U2-RT if higher), **N ≥ 150**.
- PASS → PREREG_FTMO_N137 only after RT is in COSTS. FAIL → STOP (geen thr-grid, geen USDZAR/USDMXN twin, geen 5d hold, geen overnight, geen soft gate).
