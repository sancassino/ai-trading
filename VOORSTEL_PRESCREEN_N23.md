# VOORSTEL_PRESCREEN_N23 — US100cash Swing 2d TSMOM (met FTMO-swap in gate)

**Status:** **geen PREREG — U2 D-092.1 FAIL** (U2 `a1756a7` op `claude/uitvoerder2-r`; train 2021–2023: N=377, mean **+4,46** < gate **13,68** bp; long-split +10,83 nog onder gate). Geen herstart / geen dunnere 2d-TSMOM-variant. Vervangen door N24+ (D-094).  
**Auteur:** Strateeg (Grok).  
**Instrument:** `US100cash` (RT intraday **0,66 bp**; swap_long **1,95** / swap_short **0,21** bp/nacht — COSTS_FTMO).  
**Track 4:** andere horizon — swing 2 dagen TSMOM (niet intradag-ORB).  
**Grond:** Klassiek time-series momentum: teken van 20-dags return op D-close voorspelt de volgende 2 closes. Lage rt_over_day op US100 (screen #1) maakt overnight holds haalbaarder dan op high-RT commodities, mits swap in de poort zit. **Geen** maand-sleeve zoals dood B1 FX overnight-month.

**D-094a:** FTMO D1-reeks kort; schriftelijke reden **(b)**: TSMOM op equity indices is literatuur-standaard over 10+ jaar (proxy `data/daily/NDX.csv` / Nasdaq); FTMO D1/M5 toetst kosten+swap+uitvoering. Herhaal in PREREG. Optioneel later poolen met US30/US500 → pad naar **(c)**.

**Overnight swap (expliciet):** hold = 2 handelsdagen → typisch **2 nachten**.  
- Geschatte roundtrip-kosten long-bias: RT 0,66 + 2×1,95 = **4,56 bp** → gate 3× = **13,68 bp** (conservatief, long-swap).  
- Short: RT 0,66 + 2×0,21 = **1,08 bp** → 3× = **3,24 bp**.  
- **Binding pre-screen gate (pooled long+short):** mean bruto ≥ **13,68 bp** (worst-case 3× long-side cost), zodat beide kanten de long-swap drempel halen; U2 rapporteert ook side-split mean. Alternatief acceptabel: per-trade cost = RT + n_nights×swap_side, dan mean (bruto − 0) vs gate op **net** — maar D-092.1 pre-screen is **bruto** ≥ 3× RT_effective; hier RT_effective = 4,56 bp.

---

## Idee (mechanisme)

Equity-index TSMOM: trending regimes houden 2–5 dagen aan. Regel is close-to-close, geen ORB, geen intraday fade. Onderscheid van B1: B1 = FX multi-pair maand-hold met swap-drag FAIL; dit = **single index, 2-dagen hold**, swap meegenomen in gate.

**Onderscheid van dode sleeves:**
- ≠ **B1 TSMOM FX overnight-month** (dead; FX universum + ~20+ nachten)
- ≠ A1/F2-ORB / N11 / N15–N17 (intraday ORB)
- ≠ N3 close-drive (intraday US100 PM)
- ≠ C17/A4 FOMC D1 (event-kalender, multi-night week)

---

## Regel (bevriesbaar zodra screen PASS)

**Signal (D1):**  
- `ret20 = close_t / close_{t-20} − 1`  
- Als `ret20 > 0` → **LONG** op close_t  
- Als `ret20 < 0` → **SHORT** op close_t  
- Als `ret20 == 0` → skip  

**Hold:** precies **2** handelsdagen (exit op close_{t+2}). Max 1 nieuwe entry per dag; geen pyramid; flat weekend telt als nachten volgens FTMO swap-kalender (U2: gebruik `swap_specs` / COSTS nachten tussen entry en exit).

**Stop (optioneel pre-screen uit):** geen intraday stop in bruto-screen (zuivere 2d close-to-close); formele PREREG mag 2×ATR14 D1 toevoegen — **niet** in deze pre-screen (houd regel bevroren = pure TSMOM).

**Swap:** trek **niet** van bruto af in de D-092.1 mean (bruto blijft bruto); wel verhoog RT_effective in de **gate** zoals hierboven (13,68 bp).

---

## Pre-screen aanvraag (Uitvoerder-2)

- **Data (voorkeur):** D1 uit `data/m5gz/US100cash.csv.gz` geresampled naar dag-close (laatste M5 van reguliere sessie / 22:00 CET bar), train **2021-01-01 … 2023-12-31**.  
  Fallback: `data/ftmo_d1ohlc_US500_US100.txt` gefilterd op `US100.cash` indien M5-resampling te zwaar — zelfde train-window.
- **Regel:** ret20-sign → entry close_t, exit close_{t+2}; signed bruto 2d return in bp.
- **Maatstaf:** signed mean bruto bp + median + N (N = aantal trades; overlapping holds OK als aparte entries of non-overlap — **kies non-overlap**: nieuwe entry alleen als flat; verwacht N≈ train_days/2 ≥ 150? Bij non-overlap ~250 trading days/yr ×3 /2 ≈ 375 — OK). **Gebruik non-overlapping entries** (wacht tot exit voor nieuwe signal).
- **Gate:** mean bruto ≥ **13,68 bp** (3 × (0,66 + 2×1,95)). N≥150.
- **Geen test/reserve aanraken.**
- **Uitkomst:** PASS + N≥150 → PREREG_FTMO_N23 met volledige swap-tabel + D-094a (b). FAIL → STOP.
