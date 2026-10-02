# VOORSTEL_PRESCREEN_N99 — CADCHF Long-Only 5d Oil-CHF Carry+Momentum (NEW_FAMILY X)

**Status:** **DIAG_FAIL** — C-034 Lane-B diag (mean **−4,00 ≪ 6,81**; N=103); **geen PREREG**; drop path (2026-10-02 ~21:33 CEST).
**Auteur:** Strateeg (Grok). **NEW_FAMILY X** (CADCHF oil-CHF carry+momentum long-only — nooit eerder geprobeerd).  
**Instrument:** `CADCHF` (RT **2,27** bp — `COSTS_FTMO_alle` M5 spread_med≈1,55 + FX commissie≈0,36×2; swap_long CAD vs CHF = earn → 0 in gate per D-100).  
**Track 4 + D-100 family B:** CADCHF long-only 5d swing. Long = structurele CAD carry vs CHF funding (BoC >> SNB; CAD = olie-commodity currency) + positief 5d momentum.

**Gate (long-only; 4 nachten; swap earn → 0 in gate per D-100):**  
2,27 → gate 3 × 2,27 = **6,81** bp.  
(Swap-credit telt NIET als alfa; bruto = signed prijsrendement.)

**D-094a:** train 2021–2023. Reden **(b)**: FX carry + TSMOM on oil-CHF cross (Menkhoff et al. 2012; Burnside et al. 2011; CAD/CHF = commodity vs funding; FTMO-M5 = kosten). Herhaal in PREREG.

**Onderscheid:**
- ≠ **N96** CADJPY LO 5d UNDERPOWERED (JPY≠CHF; ander funding/regime)
- ≠ **N94** NZDJPY / **N90** GBPJPY / **N58** AUDJPY (andere crosses)
- ≠ **N97** AUDCAD FAIL (AUDCAD = commodity-XS; dit = CAD vs **CHF funding**)
- ≠ **L60 FX-med** BARRED / **N91** AUDUSD DIAG_FAIL / **N84** AUDNZD fade
- ≠ **N93** SECTOR_DISP / VIX / ORB-meta / UKOIL-OVN / CORN / NY-2h / N75–N97 restarts

## Regel
- `ret5 = close_t / close_{t−5} − 1` (dagclose uit M5; laatste bar ≤22:00 CET)
- `ret5 > 0` → **LONG** op close_t
- `ret5 ≤ 0` → skip (geen short-been; short CADCHF swap structureel duur)
- Hold: exit close_{t+5}. **Non-overlapping**. Alleen LONG.

## Pre-screen
- Data: `data/m5gz/CADCHF.csv.gz` → dagclose, train **2021-01-01 … 2023-12-31**.
- Gate: mean bruto ≥ **6,81** bp, N ≥ 150.
- PASS → PREREG_FTMO_N99. FAIL → STOP (geen ret10-switch, geen CADJPY twin → N96 clone, geen soft gate).
