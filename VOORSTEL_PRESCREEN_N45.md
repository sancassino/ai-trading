# VOORSTEL_PRESCREEN_N45 — ETHUSD Asia-Session Momentum → EU Open Continuation

**Status:** **geen PREREG — D-092.1 FAIL** Strateeg `n45_n51` (N=61, mean **-81.7865** < gate **54.0**; FAIL_MEAN). Geen retune.
**Auteur:** Strateeg (Claude).  
**Instrument:** `ETHUSD` (RT **18,0 bp** FTMO-crypto default; `missing_from_COSTS_FTMO` → `results/screen_cost_vol.csv`).  
**Gate:** 3 × 18,0 = **54,0 bp**.  
**Track 2 + D-097:** crypto — Asia-session directional move (00:00–08:00 CET) vervolgt in vroege EU-sessie (08:00–12:00 CET). Swap 0 (intradag). D-097: ≥50 bp bruto/trade past bij ETHUSD vol (daagse vol ±500 bp).

**D-094a:** train 2021–2023. Reden **(b)**: crypto Asia-EU session-handoff microstructure (BTC/ETH Asia spot + derivatives; well-documented in crypto-microstructure literatuur); FTMO-M5 kosten = crypto default 18 bp RT. Herhaal in PREREG.

**Onderscheid (anti-kloon):**
- ≠ **S2-BTC** strategy (ander instrument + ander mechanisme)
- ≠ **N39** crypto Asia handoff (FAIL — ander symbool/definitie)
- ≠ **N47** USDCHF Asia→Lon FX handoff (crypto vs FX; andere drempel/logica)
- ≠ **N35/N41** EU→US index cont FAIL_T (ander instrument + ander venster)
- ≠ **N48** USDJPY 1d TSMOM (dagelijks vs Asia intradag)
- ≠ enig ORB of London-fix mechanisme

## Regel
- `asia_bp = 1e4 × (C_0800 − C_0000) / C_0000`  
  (M5-close van 08:00 CET bar min M5-close van 00:00 CET bar, in bp)
- `|asia_bp| ≥ 300` → **side = sign(asia_bp)**; entry 08:00 CET close  
  (drempel 300 bp = filterruis bij crypto; verwacht ±500 bp daagse vol)
- **Stop:** 2,0 × ATR14 (dag) vanaf instapprijs  
- **Exit:** hard flat **12:00 CET** (4 uur na entry). Swap = 0 (intradag).
- Max 1 trade/dag; geen overlap.

## Pre-screen
- Data: `data/m5gz/ETHUSD.csv.gz`, train **2021-01-01 … 2023-12-31** only.
- Maatstaf: mean bruto (bp), N (non-overlap, max 1/dag).
- Gate: mean bruto ≥ **54,0 bp**, N ≥ 150.
- PASS → PREREG_FTMO_N45. FAIL → STOP (geen drempel-retune; geen ander crypto-kloon).
