# VOORSTEL_PRESCREEN_N98 — USOILcash Lon-AM → US100cash NY risk-on lead-lag (NEW_FAMILY W)

**Status:** **DIAG_FAIL** — C-034 Lane-B diag (mean **−3,79 ≪ 1,98**; N=356); **geen PREREG**; drop path (2026-10-02 ~21:33 CEST).
**Auteur:** Strateeg (Grok). **NEW_FAMILY W** (energy→equity same-day risk-on lead-lag session-flat — nooit deze setup).  
**Signal:** `USOILcash` (Lon-AM impulse). **Trade:** `US100cash` (RT **0,66** bp; swap 0 — **EOD flat**).  
**Track 2 + D-102 adjacent:** oil morning risk impulse → Nasdaq afternoon continuation; intradag-vlak (geen swap).

**Gate:** 3 × US100 RT = 3 × 0,66 = **1,98** bp.

**D-094a:** train 2021–2023. Reden **(b)**: commodity risk-on transmission into US tech beta is a classic macro lead–lag (oil shock → risk appetite); FTMO-M5 both series toetsen kosten/uitvoering. Herhaal in PREREG.

**Onderscheid:**
- ≠ **N85** US500→US100 lead-lag DIAG_FAIL (equity→equity; dit = **olie→equity**)
- ≠ **N83** DXY→US100 opposite UNDERPOWERED (USD macro; dit = energy risk-on same-dir)
- ≠ **UKOIL-OVN / N80** OVN-gap BARRED (overnight oil; dit = Lon-AM→NY same-day flat on **US100**)
- ≠ **ENERGY_TSMOM / N22 / N43 / N76** oil-sleeve TSMOM/MR (trade leg = US100, not oil)
- ≠ **N92** NY-2h mom / **N93** SECTOR_DISP / VIX_TERM / ORB-meta / L60 / CORN / N75–N97 restarts

## Regel
1. Lon-AM oil impulse: `oil_am_bp = 1e4 × (USOILcash_close@12:00 / USOILcash_close@08:00 − 1)` (first M5 in ±15 min windows).
2. Trade only if `|oil_am_bp| ≥ 40`.
3. Same-direction US100: oil_am ≥ +40 → **LONG** US100; oil_am ≤ −40 → **SHORT** US100.
4. Entry: US100 close of first M5 in **[15:30, 15:45] CET**. If missing, skip day.
5. Exit: flat at **21:00 CET** same day. **No overnight.**
6. Non-overlapping (≤1/day).

## Pre-screen
- Data: `data/m5gz/USOILcash.csv.gz` + `data/m5gz/US100cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **1,98** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N98. FAIL → STOP (geen thr-grid, geen UKOIL twin, geen overnight oil rewrite → N80 clone, geen US500 substitute → N85 clone).
