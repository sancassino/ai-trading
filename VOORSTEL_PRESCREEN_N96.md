# VOORSTEL_PRESCREEN_N96 — CADJPY Long-Only 5d Carry+Momentum (D-100 family B; NEW_FAMILY U)

**Status:** **UNDERPOWERED** — D-092.1 Strateeg `n96_n97` (mean **+16,45 ≥ 4,80** maar **N=112≪150**; years 2021 +12,19 / 2022 +23,75 / 2023 +13,76); **geen PREREG**; no inflate-N retune (2026-10-02 ~21:20 CEST).
**Auteur:** Strateeg (Grok). **NEW_FAMILY U** (CADJPY oil-yen carry+momentum long-only — nooit eerder geprobeerd).  
**Instrument:** `CADJPY` (RT **1,60 bp** — M5 spread_med≈0,68 bp + FX commissie≈0,46×2; swap_long CAD vs JPY = earn → 0 in gate per D-100).  
**Track 4 + D-100 family B:** CADJPY long-only 5d swing. Long = structurele CAD carry vs JPY (BoC policy >> BoJ; CAD = olie-commodity currency — Chen & Rogoff 2003) + positief 5d momentum.

**Gate (long-only; 4 nachten; swap earn → 0 in gate per D-100):**  
1,60 + 4 × max(swap_long_cost, 0) = 1,60 → gate 3 × 1,60 = **4,80 bp**.  
(Swap-credit telt NIET als alfa; bruto = signed prijsrendement.)

**D-094a:** train 2021–2023. Reden **(b)**: FX carry + TSMOM op oil-yen cross (Menkhoff et al. 2012 FX TSMOM; Burnside et al. 2011 carry; CAD/JPY = hoog-vol commodity-yen met persistentie bij positief momentum; FTMO-M5 = kosten). Herhaal in PREREG.

**Onderscheid:**
- ≠ **N94** NZDJPY LO 5d FAIL (NZD dairy/agri ≠ CAD oil; ander cross + ander commodity-regime)
- ≠ **N90** GBPJPY LO 5d UNDERPOWERED (GBP≠CAD; BoE≠BoC)
- ≠ **N58** AUDJPY LO 20→10 FAIL (AUD≠CAD; lookback 20≠5)
- ≠ **N62** GBPJPY LO 20→10 FAIL / **L60 FX-med** BARRED / **N91** AUDUSD DIAG_FAIL
- ≠ **N93** SECTOR_DISP DEAD / VIX_TERM / ORB-meta / UKOIL-OVN / CORN / NY-2h / N75–N93 restarts

## Regel
- `ret5 = close_t / close_{t−5} − 1` (dagclose uit M5; laatste bar ≤22:00 CET)
- `ret5 > 0` → **LONG** op close_t
- `ret5 ≤ 0` → skip (geen short-been; short CADJPY swap structureel duur)
- Hold: exit close_{t+5}. **Non-overlapping**. Alleen LONG.

## Pre-screen
- Data: `data/m5gz/CADJPY.csv.gz` → dagclose, train **2021-01-01 … 2023-12-31**.
- Gate: mean bruto ≥ **4,80 bp**, N ≥ 150.
- PASS → PREREG_FTMO_N96. FAIL → STOP (geen ret10-switch, geen NZDJPY/AUDJPY-add, geen soft gate).
