# VOORSTEL_PRESCREEN_N102 — USDCHF Long-Only 5d USD-CHF Carry+Momentum (NEW_FAMILY Y)

**Status:** **OPEN** — pipeline replace after C-034 N98/N99 DIAG_FAIL (filed 2026-10-02 ~21:56 CEST).  
**Auteur:** Strateeg (Grok). **NEW_FAMILY Y** (USDCHF USD-vs-CHF funding carry+momentum long-only — nooit als deze setup).  
**Instrument:** `USDCHF` (RT **1,01** bp — `COSTS_FTMO.csv`; swap_long **−0,39** = earn → 0 in gate per D-100).  
**Track 4 + D-100 family B:** USDCHF long-only 5d swing. Long = USD vs CHF funding (Fed >> SNB) + positief 5d momentum.

**Gate (long-only; 4 nachten; swap earn → 0 in gate per D-100):**  
1,01 → gate 3 × 1,01 = **3,03** bp.  
(Swap-credit telt NIET als alfa; bruto = signed prijsrendement.)

**D-094a:** train 2021–2023. Reden **(b)**: FX carry + TSMOM on USD/CHF (Menkhoff et al. 2012; funding-currency short CHF; FTMO-M5 = kosten). Herhaal in PREREG. ≥5y proxy + FTMO-M5 train.

**Onderscheid:**
- ≠ **N99** CADCHF LO oil-CHF DIAG_FAIL (CAD≠USD; olie-commodity vs pure USD funding)
- ≠ **N74** USDCHF L60/H10 BARRED (L60 FX-med family closed — dit = **5d** LO carry+mom, niet L60)
- ≠ **N96** CADJPY / **N94** NZDJPY / **N90** GBPJPY / **N91** AUDUSD / **N97** AUDCAD
- ≠ **N98** USOIL→US100 / **N93** SECTOR_DISP / VIX / ORB-meta / UKOIL-OVN / CORN / NY-2h / N75–N101 restarts

## Regel
- `ret5 = close_t / close_{t−5} − 1` (dagclose uit M5; laatste bar ≤22:00 CET)
- `ret5 > 0` → **LONG** op close_t
- `ret5 ≤ 0` → skip (geen short-been; short USDCHF swap structureel duur — swap_short 2,17)
- Hold: exit close_{t+5}. **Non-overlapping**. Alleen LONG.

## Pre-screen
- Data: `data/m5gz/USDCHF.csv.gz` → dagclose, train **2021-01-01 … 2023-12-31**.
- Gate: mean bruto ≥ **3,03** bp, N ≥ 150.
- PASS → PREREG_FTMO_N102. FAIL → STOP (geen ret10-switch, geen CADCHF twin → N99 clone, geen L60 rewrite, geen soft gate).
