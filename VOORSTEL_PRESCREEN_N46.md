# VOORSTEL_PRESCREEN_N46 — EURGBP London Fix Extension Fade

**Status:** **OPEN** — awaiting cost pre-screen (**D-094** track 2; replace N35 FAIL_T; filed 2026-10-01 ~09:26).  
**Auteur:** Strateeg (Grok).  
**Instrument:** `EURGBP` (RT **1,04 bp** COSTS_FTMO → gate **3,12 bp** = 3×RT).  
**Track 2:** FX cross — London-fix extensie-fade (niet session-mom, niet ORB). Swap 0.

**D-094a:** train 2021–2023. Reden **(b)**: FX London-fix inventory / news-impulse fade is multi-decade microstructure (EURGBP cross); FTMO-M5 = kosten. Herhaal in PREREG.

**Onderscheid (anti-kloon dead-set):**
- ≠ **S2-GBPJPY** EU morning **mom cont** FAIL_T (ander paar + continuation vs fade)
- ≠ **N38/N42** Lon morning mom FAIL (mom vs fade; andere paren)
- ≠ **N29** GBPUSD midday fade FAIL (ander paar + ander venster 12:00→15:00)
- ≠ **A5/GS02** London ORB / Asian-range fade
- ≠ **N35/N36** index/XAU cont FAIL_T; ≠ ORB-familie


- ≠ **N40** GER40 mid-morning mom FAIL_T; ≠ **N41** US30 EU→US FAIL_T; ≠ N44 barred EU→US parallel

## Regel
- `ext_bp = 1e4×(C_1030−C_0800)/C_0800`
- `|ext| ≥ 25` → side = **−sign(ext)** (fade); entry 10:30 close; stop 1×ATR14; flat **13:30 CET**
- Max 1/dag; swap 0

## Pre-screen
- Data: `data/m5gz/EURGBP.csv.gz`, train **2021-01-01 … 2023-12-31** only.
- Gate: mean bruto ≥ **3,12 bp**, N≥150. Geen test/reserve.
- PASS → PREREG_FTMO_N46. FAIL → STOP (geen drempel-retune).
