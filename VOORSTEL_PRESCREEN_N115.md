# VOORSTEL_PRESCREEN_N115 — EURUSD Lon-AM → US500 NY macro-beta session-flat (NEW_FAMILY AJ)

**Status:** **OPEN** — pipeline refill after C-036 closed N104–N111 (filed 2026-10-02 ~22:57 CEST).  
**Auteur:** Strateeg (Grok). **NEW_FAMILY AJ** (EURUSD Lon-AM impulse → same-dir US500 NY cash-session continuation — FX macro-beta → equity, EOD flat).  
**Signal:** `EURUSD` (Lon-AM impulse). **Trade:** `US500cash` (RT **0,78** bp; swap 0 — **session-flat**).  
**Track 2 + D-100:** EUR strength (USD weakness) in Lon morning as risk-on / global-growth proxy → US equity afternoon same-dir; intradag-vlak.

**Gate:** 3 × US500 RT = 3 × 0,78 = **2,34** bp.

**D-094a:** train 2021–2023. Reden **(b)**: EURUSD morning risk prices global risk appetite that persists into US cash equity (macro FX→equity beta); microstructure distinct from trading DXY itself and from DXY→index **opposite** fade. FTMO-M5 both series. Herhaal in PREREG.

**Onderscheid:**
- ≠ **N110** DXY Lon→EU-PM DIAG_FAIL (trades **DXY** on itself Lon→EU — this = **EURUSD→US500** Lon→NY)
- ≠ **N83** DXY overnight → US100 **opposite** UNDERPOWERED (opposite fade ≠ same-dir continuation; DXY≠EURUSD; US100≠US500)
- ≠ **N103** GER40→US30 FAIL_STRESS / **N85** US500→US100 DIAG (equity→equity ≠ FX→equity)
- ≠ FX LO 5d carry set / L60 / EMB / CRACK / SECTOR_DISP / VIX / ORB / N75–N111 restarts

## Regel
1. Lon-AM EURUSD impulse: `eur_am_bp = 1e4 × (EURUSD_close@12:00 / EURUSD_close@08:00 − 1)` (first M5 in ±15 min; CET).
2. Trade only if `|eur_am_bp| ≥ 25` (FX daily ranges; thr fixed a priori).
3. Same-direction US500: eur_am ≥ +25 → **LONG** US500; eur_am ≤ −25 → **SHORT** US500.
4. Entry: US500 close of first M5 in **[15:30, 15:45] CET**. If missing, skip day.
5. Exit: flat at **21:00 CET** same day. **No overnight.**
6. Non-overlapping (≤1/day).

## Pre-screen
- Data: `data/m5gz/EURUSD.csv.gz` + `data/m5gz/US500cash.csv.gz`; train **2021-01-01 … 2023-12-31**.
- Gate: signed mean bruto ≥ **2,34** bp, **N ≥ 150**.
- PASS → PREREG_FTMO_N115. FAIL → STOP (geen thr-grid, geen DXY substitute → N110/N83 clone, geen US100 rewrite, geen overnight, geen soft gate).
