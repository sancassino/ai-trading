# VOORSTEL_PRESCREEN_N48 — USDJPY Swing 1d TSMOM (overnight; swap in gate)

**Status:** **OPEN** — awaiting cost pre-screen (**D-094** track 4; replace S2-GBPJPY FAIL_T slot; filed 2026-10-01 ~09:26).  
**Auteur:** Strateeg (Grok).  
**Instrument:** `USDJPY` (RT **0,78 bp**; swap_long **−0,37** / swap_short **+1,58** bp/nacht — COSTS_FTMO).  
**Track 4:** andere horizon — close-to-close **1 handelsdag** TSMOM (niet intradag session-mom).

**D-094a:** train 2021–2023. Reden **(b)**: FX daily TSMOM literatuur (Moskowitz–Ooi–Pedersen e.a.); FTMO D1/M5 toetst kosten+swap. Herhaal in PREREG.

**Overnight swap (expliciet):** hold = 1 nacht.  
- Worst-case (short): RT 0,78 + 1×1,58 = **2,36 bp** → gate 3× = **7,08 bp**.  
- Long ontvangt swap (−0,37) → lagere effectieve kost; binding gate = **7,08** (short-worst) zodat beide kanten de drempel halen.

**Onderscheid:**
- ≠ **B1** FX month TSMOM STOP (~20+ nachten)
- ≠ **N23** US100 2d TSMOM FAIL (ander instrument + 2d hold)
- ≠ **S2-USDJPY** Tokyo-range London intradag STOP
- ≠ **S2-GBPJPY** EU morning intradag mom FAIL_T
- ≠ **N28/N33** Lon→NY intradag mom FAIL; ≠ ORB / N35–N36


- ≠ **N40** GER mid-morn intradag FAIL_T; ≠ **N41** EU→US FAIL_T

## Regel
- D1 uit M5: `ret10 = close_t / close_{t-10} − 1`
- `ret10 > 0` → LONG op close_t; `ret10 < 0` → SHORT; `==0` → skip
- Hold: exit close_{t+1} (**1** handelsdag). **Non-overlapping** entries (wacht tot flat).
- Geen intraday stop in bruto pre-screen (zuivere 1d TSMOM).

## Pre-screen
- Data: `data/m5gz/USDJPY.csv.gz` → dag-close (laatste M5 / 22:00 CET), train 2021–2023.
- Maatstaf: signed mean bruto bp + median + N (non-overlap).
- Gate: mean bruto ≥ **7,08 bp**, N≥150. Geen test/reserve.
- PASS → PREREG_FTMO_N48 met swap-tabel. FAIL → STOP (geen hold/lookback dunnen).
