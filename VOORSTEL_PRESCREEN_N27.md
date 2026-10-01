# VOORSTEL_PRESCREEN_N27 — AUDUSD H4 Mean-Reversion (SMA20 deviation)

**Status:** **OPEN** — awaiting U2 cost pre-screen (**D-094** track 4; optionele 4e vervanger; filed 2026-10-01 08:12).  
**Auteur:** Strateeg (Grok).  
**Instrument:** `AUDUSD` (RT **1,22 bp** COSTS_FTMO / screen → drempel **3,66 bp** = 3× RT; cost_in_costs_ftmo=True).  
**Track 4:** andere horizon — **H4** mean-reversion (niet intradag-ORB, niet 2d index-TSMOM).  
**Grond:** Op H4 mean-reverteert AUDUSD naar een langzame SMA wanneer de afwijking groot is; commodity-FX inventory + Asia/London handoff creëren overshoots die binnen één H4-bar deels terugkomen. Hold ≤1 H4 (12:00→16:00 CET) → swap 0.

**D-094a:** train 2021–2023 = 3y. Schriftelijke reden **(b)**: FX H4/D1 mean-reversion is breed gedocumenteerd op multi-decade FX (FRED/majors); FTMO-M5→H4 toetst kosten. ≠ B1 (maand TSMOM overnight). Herhaal in PREREG.

---

## Idee (mechanisme)

Resample M5→H4 (CET-aligned closes 00/04/08/12/16/20). Eenmaal per dag op de **12:00 CET** H4-close: als prijs ≥ ±40 bp van SMA20(H4), fade richting SMA; exit op **16:00 CET** H4-close (één bar later). Geen London ORB, geen Asian-range fade (GS02), geen Tokyo-handoff breakout.

**Onderscheid van dode sleeves:**
- ≠ **A5** FX London-open ORB / **GS02** Asian-range fade / **S2-USDJPY** Tokyo→London handoff
- ≠ **B1** FX overnight-month TSMOM (andere horizon + richting: MR vs momentum)
- ≠ **N23** US100 2d TSMOM
- ≠ N20–N22 index/olie session fades

---

## Regel (bevriesbaar zodra screen PASS)

**H4 setup (CET):**  
- Bouw H4 OHLC uit M5 (close = laatste M5 in H4-bucket).  
- `sma20` = SMA van H4-closes, lengte 20 (warm-up: skip tot sma beschikbaar in train).  
- Op bar met open-tijd 12:00 CET: `dev_bp = 1e4 × (close_1200 − sma20) / sma20`

**Signalen (max 1 trade/dag):**  
- `dev_bp ≥ +40 bp` → **SHORT** op 12:00 CET H4 close  
- `dev_bp ≤ −40 bp` → **LONG** op 12:00 CET H4 close  
- Anders → geen trade  

**Exit:** 16:00 CET H4 close (vast). **Stop:** 1,0 × ATR14(H4) optioneel in pre-screen uit (zuivere hold OK). **Swap = 0**.

---

## Pre-screen aanvraag (Uitvoerder-2)

- **Data:** `data/m5gz/AUDUSD.csv.gz` → H4 resample, train **2021-01-01 … 2023-12-31**.
- **Regel:** |dev| vs SMA20(H4) ≥ 40 bp op 12:00 CET → fade, exit 16:00 CET.
- **Maatstaf:** signed mean bruto bp + median + N.
- **Gate:** mean bruto ≥ **3,66 bp** (3 × 1,22 bp RT). N≥150.
- **Geen test/reserve aanraken.**
- **Uitkomst:** PASS + N≥150 → PREREG_FTMO_N27 (D-094a (b)). FAIL of N<150 → STOP.
