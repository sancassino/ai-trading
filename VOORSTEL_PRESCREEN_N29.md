# VOORSTEL_PRESCREEN_N29 — GBPUSD London-Open Midday Deviation Fade

**Status:** **geen PREREG — D-092.1 FAIL** (Strateeg screen 2026-10-01 08:25; N=122≪150, mean **−1,20** < 2,10 bp). Artifacts `results/R2/n28_n31_prescreen/`.  
**Auteur:** Strateeg (Grok).  
**Instrument:** `GBPUSD` (RT **0,70 bp** → drempel **2,10 bp** = 3× RT).  
**Track 2:** FX major — London midday inventory fade vs London-open, **niet** ORB-breakout.  
**Grond:** Na London-open (09:00 CET) loopt GBPUSD vaak door tot midday; rond 12:00–15:00 CET unwindt een deel van de ochtendextensie terug richting London-open (UK lunch / pre-US positioning). Pure prijsregel. Swap 0.

**D-094a:** train 2021–2023 = 3y. Schriftelijke reden **(b)**: FX midday mean-reversion vs session-open is standaard microstructure; multi-decade GBPUSD proxy. Herhaal in PREREG.

---

## Idee (mechanisme)

`dev` vs London-open om 12:00 CET. Als |dev| ≥ 30 bp → fade; flat 15:00 CET (vóór US cash-open).

**Onderscheid van dode sleeves:**
- ≠ **A5** London-open **ORB breakout** (dit = **fade** van open-deviatie, entry midday)
- ≠ **GS02** Asian-range fade (ander anker/tijd)
- ≠ **N27** AUDUSD H4 SMA-MR (ander anker: session-open vs SMA20 H4)
- ≠ **N21** GER40 afternoon fade / index fades
- ≠ B1 month TSMOM

---

## Regel (bevriesbaar zodra screen PASS)

**London-open afwijking:**  
- `P_lon` = M5-close 09:00 CET  
- `P_1200` = M5-close 12:00 CET  
- `dev_bp = 1e4 × (P_1200 − P_lon) / P_lon`

**Signalen (max 1 trade/dag):**  
- `dev_bp ≥ +30 bp` → **SHORT** op 12:00 CET close  
- `dev_bp ≤ −30 bp` → **LONG** op 12:00 CET close  
- Anders → geen trade  

**Stop:** 1,0 × ATR14 (dag).  
**Exit:** hard flat **15:00 CET**. **Swap = 0**.

---

## Pre-screen aanvraag

- **Data:** `data/m5gz/GBPUSD.csv.gz`, train **2021-01-01 … 2023-12-31**.
- **Regel:** |dev| vs 09:00 ≥ 30 bp @12:00 → fade, flat 15:00.
- **Gate:** mean bruto ≥ **2,10 bp**. N≥150.
- **Geen test/reserve.** PASS → PREREG_FTMO_N29 (D-094a (b)).
