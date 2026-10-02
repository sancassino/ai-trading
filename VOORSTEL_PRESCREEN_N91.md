# VOORSTEL_PRESCREEN_N91 — AUDUSD Long-Only 5d Carry+Momentum (D-100 family B; NEW_FAMILY P)

**Status:** **OPEN** — pipeline aanvulling na N88/N89 informele pre-screen FAIL (filed 2026-10-01 ~17:50 CEST).  
**Auteur:** Strateeg (Claude). **NEW_FAMILY P** (AUDUSD commodity-currency carry+momentum long-only — nooit eerder geprobeerd).  
**Instrument:** `AUDUSD` (RT **0,45 bp** — COSTS_FTMO; swap_long positief = earn bij long AUD).  
**Track 4 + D-100 family B:** AUDUSD long-only 5d swing. Long = AUD commodity-currency carry vs USD (RBA policy rate structureel hoger dan Fed rate; Chen & Rogoff 2003) + positief 5d momentumsignaal. Overnight long AUDUSD = positieve carry.

**Gate (long-only; 4 nachten; swap earn → 0 in gate per D-100):**  
0,45 + 4 × max(swap_long_cost, 0) = 0,45 + 0 = **0,45 bp** → gate 3 × 0,45 = **1,35 bp**.  
(Swap-credit telt NIET als alfa per D-100; alleen RT in gate.)

**D-094a:** train 2021–2023. Reden **(b)**: AUD commodity-currency carry (Chen & Rogoff 2003 resource currency; Lustig & Verdelhan 2007 carry premium; RBA–Fed rente-differentieel 2021–2023 positief voor AUD; FTMO-M5 = kosten). Herhaal in PREREG.

**Onderscheid:**
- ≠ **FX_EUR_SHORT_TSMOM** FAIL_T (EUR-short EURUSD/EURAUD; dit = AUD-long AUDUSD)
- ≠ **N88** EURGBP short-only (GBP/EUR cross; dit = AUD/USD commodity-currency)
- ≠ **N90** GBPJPY long-only (GBP/JPY; ander mechanisme ander paar)
- ≠ **L60 FX-med** BARRED (USDJPY/EURJPY mid-term; dit = AUDUSD commodity carry)
- ≠ enig intradag / gap-fade / equity-index / metals

## Regel
- `ret5 = close_t / close_{t−5} − 1` (dagclose uit M5; laatste bar ≤22:00 CET)
- `ret5 > 0` → **LONG** op close_t (positief momentum = carry-richting bevestigd)
- `ret5 < 0` → skip (geen short-been; long-only carry-richting)
- Hold: exit close_{t+5}. **Non-overlapping**. Alleen LONG.

## Pre-screen
- Data: `data/m5gz/AUDUSD.csv.gz` → dagclose, train **2021-01-01 … 2023-12-31**.
- Gate: mean bruto ≥ **1,35 bp**, N ≥ 150.
- PASS → PREREG_FTMO_N91. FAIL → STOP (geen ret10-switch, geen AUDCAD-add).
