# VOORSTEL_PRESCREEN_N129 — PPLT_PLATINUM_STRESS → US500cash session-flat (NEW_FAMILY AX)

**Status:** **OPEN** — D-094 refill after N126 D-092.1 FAIL + N127 PASS→PREREG (filed 2026-10-03 ~00:10 CEST).  
**Auteur:** Strateeg (Grok). **NEW_FAMILY AX** (platinum ETF **level** stress → equity session-flat — industrial precious / auto-catalyst channel; **≠ SILVER_GOLD** SLV/GLD ratio / **≠ XAU** / **≠ CPER** copper).  
**Signal:** Yahoo/proxy **PPLT** (abrdn Physical Platinum Shares). **Trade:** `US500cash` (RT **0,78** bp; swap 0 — **session-flat**).  
**Track 4 + D-100 + D-097 commodities:** Platinum industrial-precious stress as auto/industrial risk timing for DM large-cap; intradag-vlak.

**Gate:** 3 × US500 RT = 3 × 0,78 = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: PPLT as **platinum level** ≠ SILVER_GOLD ratio (N113), ≠ XAU fades, ≠ CPER copper (N117), ≠ DBA ag (N126). FTMO-M5 for costs.

**Onderscheid:**
- ≠ **N113 SILVER_GOLD** FAIL_COST / **N117 CPER** FAIL_STRESS / **N126 DBA** FAIL / XAU intradag dead set
- ≠ **N124/N125** / **N127 EWZ** / TLT/TIP/HYG/VNQ/EEM/EMB/IWM/SECTOR_DISP/VIX
- ≠ N75–N128 clones / PPLT CFD trade leg / overnight / thr-grid / soft gate

## Regel
**Signal (dag t):**
1. `z40 = (PPLT_t − mean_40(PPLT)) / stdev_40(PPLT)`.
2. **stress_buy:** `z40 > +1,5` → **SHORT** US500; `z40 < −1,5` → **LONG**; else skip.

**Execution (dag t+1, US500cash) — D-100 session-flat:**
3. Entry: first M5 ≥ **15:30 CET** (span ≤15 min). Missing → skip.
4. Exit: flat ≤ **21:00 CET** same day. **No overnight.**
5. Non-overlapping (≤1/day).

## Pre-screen
- Data: `data/daily/PPLT.csv` + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **2,34** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N129. FAIL → STOP (geen SLV/GLD rewrite, geen overnight, geen soft gate).
