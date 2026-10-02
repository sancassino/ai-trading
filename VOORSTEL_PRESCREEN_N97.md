# VOORSTEL_PRESCREEN_N97 — AUDCAD Long-Only 5d Commodity-XS Momentum (NEW_FAMILY V)

**Status:** **geen PREREG — D-092.1 FAIL** — Strateeg `n96_n97` (N=101, mean **−8,87 < 4,50**; years 2021 −13,04 / 2022 +1,26 / 2023 −15,72); STOP (2026-10-02 ~21:20 CEST).
**Auteur:** Strateeg (Grok). **NEW_FAMILY V** (AUDCAD commodity-currency relative 5d momentum long-only — nooit als deze setup).  
**Instrument:** `AUDCAD` (RT **1,50 bp** — M5 spread_med≈0,56 bp + FX commissie≈0,46×2; long AUD vs CAD — swap near-neutral / mild earn → 0 in gate per D-100).  
**Track 4 + XS:** AUD vs CAD relative commodity-cycle / rate-diff momentum (Australia iron ore / China-beta vs Canada oil). Long-only when 5d AUDCAD momentum positief.

**Gate (long-only; 4 nachten; swap earn/neutral → 0 in gate):**  
1,50 → gate 3 × 1,50 = **4,50 bp**.

**D-094a:** train 2021–2023. Reden **(b)**: cross-sectionele commodity-currency relative momentum (AU vs CA; Menkhoff FX TSMOM; commodity-currency literatuur Chen & Rogoff; FTMO-M5 = kosten). Herhaal in PREREG.

**Onderscheid:**
- ≠ **N84** AUDNZD rate-diff stretch **fade** DIAG_FAIL (AUDNZD ≠ AUDCAD; fade ≠ momentum; NZD ≠ CAD)
- ≠ **N91** AUDUSD LO 5d DIAG_FAIL (USD-leg ≠ CAD-leg)
- ≠ **N94** NZDJPY / **N96** CADJPY (JPY-leg ≠ CAD-cross AUDCAD)
- ≠ **N77** FX6 vol-timed XS rev DIAG_FAIL (6-pair basket reversal ≠ single AUDCAD mom)
- ≠ **N93** SECTOR_DISP / VIX / L60 / UKOIL-OVN / CORN / ORB-meta / NY-2h / N75–N93 restarts

## Regel
- `ret5 = close_t / close_{t−5} − 1` (dagclose uit M5; ≤22:00 CET)
- `ret5 > 0` → **LONG** AUDCAD op close_t
- `ret5 ≤ 0` → skip (geen short-been deze freeze)
- Hold: exit close_{t+5}. **Non-overlapping**. Alleen LONG.

## Pre-screen
- Data: `data/m5gz/AUDCAD.csv.gz` → dagclose, train **2021-01-01 … 2023-12-31**.
- Gate: mean bruto ≥ **4,50 bp**, N ≥ 150.
- PASS → PREREG_FTMO_N97. FAIL → STOP (geen fade-rewrite → N84 clone, geen AUDNZD twin, geen soft gate).
