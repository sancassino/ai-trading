# VOORSTEL_PRESCREEN_N103 — GER40 Lon-AM → US30 NY industrial lead-lag (NEW_FAMILY Z)

**Status:** **OPEN PREREG** — D-092.1 PASS `n102_n103` (mean +1,75 ≥ 1,35; N=286); `PREREG_FTMO_N103_GER40_US30_INDUSTRIAL.md` (filed 2026-10-02 ~22:05 CEST).  
**Auteur:** Strateeg (Grok). **NEW_FAMILY Z** (EU industrial equity AM impulse → US industrial PM same-dir session-flat — nooit deze setup).  
**Signal:** `GER40cash` (Lon-AM impulse). **Trade:** `US30cash` (RT **0,45** bp; swap 0 — **EOD flat**).  
**Track 2 + D-102 adjacent:** EU industrial risk impulse → Dow afternoon continuation; intradag-vlak (geen swap).

**Gate:** 3 × US30 RT = 3 × 0,45 = **1,35** bp.

**D-094a:** train 2021–2023. Reden **(b)**: cross-Atlantic industrial equity lead–lag (DAX morning risk → US industrials afternoon); classic macro microstructure, not oil→tech and not GER→US cash-open cont. FTMO-M5 both series. Herhaal in PREREG.

**Onderscheid:**
- ≠ **N98** USOIL→US100 DIAG_FAIL (olie→tech; dit = **EU equity→US industrial**)
- ≠ **S2-GER_US_LEAD** STOP (GER Europe-AM → **US open** on US100/indices — ander target/window; dit = Lon-AM GER → **US30** NY cash-session)
- ≠ **N85** US500→US100 DIAG_FAIL (US large→tech; dit = **GER→US30**)
- ≠ **N41 / N35** EU→US cont FAIL_T (US100/own-index; dit = GER signal → **US30** trade leg)
- ≠ **N93** SECTOR_DISP / VIX / ORB / L60 / UKOIL-OVN / CORN / NY-2h / N75–N101 restarts

## Regel
1. Lon-AM GER impulse: `ger_am_bp = 1e4 × (GER40cash_close@12:00 / GER40cash_close@08:00 − 1)` (first M5 in ±15 min windows).
2. Trade only if `|ger_am_bp| ≥ 40`.
3. Same-direction US30: ger_am ≥ +40 → **LONG** US30; ger_am ≤ −40 → **SHORT** US30.
4. Entry: US30 close of first M5 in **[15:30, 15:45] CET**. If missing, skip day.
5. Exit: flat at **21:00 CET** same day. **No overnight.**
6. Non-overlapping (≤1/day).

## Pre-screen
- Data: `data/m5gz/GER40cash.csv.gz` + `data/m5gz/US30cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **1,35** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N103. FAIL → STOP (geen thr-grid, geen US100 substitute → N41/N85 clone, geen GER→US-open rewrite → S2-GER_US clone, geen overnight).
