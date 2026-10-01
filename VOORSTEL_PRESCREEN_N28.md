# VOORSTEL_PRESCREEN_N28 — EURJPY London→NY Session Momentum

**Status:** **geen PREREG — D-092.1 FAIL** (Strateeg screen 2026-10-01 08:25; N=189, mean **+2,91** < 3,30 bp — closest miss). Artifacts `results/R2/n28_n31_prescreen/`.  
**Auteur:** Strateeg (Grok).  
**Instrument:** `EURJPY` (RT **1,10 bp** COSTS_FTMO / screen → drempel **3,30 bp** = 3× RT).  
**Track 2:** FX-cross — EURJPY unused in Faraday dead-set (A5 = majors ORB; B1 = month TSMOM; S2-USDJPY = Tokyo handoff).  
**Grond:** London-sessie (09:00–15:30 CET) bouwt vaak een directionele EURJPY-impuls via EU-macro + JPY-risk; die impuls vervolgt in de eerste NY-uren (15:30–18:30 CET) via overlapping liquidity. **Continuation** van London-move, geen ORB, geen Asian-fade. Intradag flat → swap 0.

**D-094a:** train 2021–2023 = 3y. Schriftelijke reden **(b)**: FX session-momentum / handoff is multi-decade microstructure (BIS/majors proxies); FTMO-M5 toetst kosten. Herhaal in PREREG.

---

## Idee (mechanisme)

Meet London-impuls 09:00→15:30 CET. Als |lon_bp| ≥ 35 bp, ga **met** de impuls op 15:30 CET; flat 18:30 CET.

**Onderscheid van dode sleeves:**
- ≠ **A5** FX London-open **ORB** (majors; breakout-of-range)
- ≠ **GS02** Asian-range **fade**
- ≠ **S2-USDJPY** Tokyo→London handoff (ander paar + ander venster)
- ≠ **B1** FX overnight-month TSMOM
- ≠ **N27** AUDUSD H4 MR (MR vs momentum; ander paar/horizon)
- ≠ N20–N27 index/olie/XAU fades

---

## Regel (bevriesbaar zodra screen PASS)

**London-impuls:**  
- `P_0900` = M5-close 09:00 CET  
- `P_1530` = M5-close 15:30 CET  
- `lon_bp = 1e4 × (P_1530 − P_0900) / P_0900`

**Signalen (max 1 trade/dag):**  
- `lon_bp ≥ +35 bp` → **LONG** op 15:30 CET close  
- `lon_bp ≤ −35 bp` → **SHORT** op 15:30 CET close  
- Anders → geen trade  

**Stop:** 1,0 × ATR14 (dag) vanaf entry.  
**Exit:** hard flat **18:30 CET**. **Swap = 0**.

---

## Pre-screen aanvraag (Uitvoerder-2 / Strateeg runner)

- **Data:** `data/m5gz/EURJPY.csv.gz`, train **2021-01-01 … 2023-12-31** only.
- **Regel:** lon_bp 09:00–15:30 ≥ ±35 bp → continue entry 15:30, stop ATR14, flat 18:30.
- **Maatstaf:** signed mean bruto bp + median + N.
- **Gate:** mean bruto ≥ **3,30 bp** (3 × 1,10 bp RT). N≥150.
- **Geen test/reserve aanraken.**
- **Uitkomst:** PASS + N≥150 → PREREG_FTMO_N28 (D-094a (b)). FAIL → STOP.
