# PREREG_FTMO_N36 — XAUUSD NY-Open Drive Continuation (first 90 min)

**Status:** FROZEN — D-092.1 PASS (U2 `43c395e`; mean +2,80 bp > gate 2,49 bp; N=150). Wacht op U2 cost-gate + formele t-test.  
**Auteur:** Strateeg (Claude/Grok). **Instrument:** `XAUUSDcash`.  
**TRIAL_COUNT bij freeze:** 448.  
**SHA VOORSTEL (regel):** commit `7ede6d0` (VOORSTEL_PRESCREEN_N36.md, filed 2026-10-01 ~08:28 CEST).

---

## Instrument & kosten

- **Symbool:** `XAUUSDcash`
- **Round-trip kosten (COSTS_FTMO.csv):** 0,83 bp
- **Gate (3× RT):** 2,49 bp
- **D-092.1 screen:** N=150, mean bruto +2,80 bp → **PASS**

---

## Regel (bevroren — identiek aan VOORSTEL)

**NY-open first-30m drive:**
- `C_1530` = M5-close van de 15:30 CET bar (NY cash open)  
- `C_1600` = M5-close van de 16:00 CET bar (30 min ná NY open)  
- `drive_bp = 1e4 × (C_1600 − C_1530) / C_1530`

**Signalen (max 1 trade/dag):**
- `drive_bp ≥ +25 bp` → **LONG** op 16:00 CET close (continuation NY-open drive)  
- `drive_bp ≤ −25 bp` → **SHORT** op 16:00 CET close  
- Anders → geen trade

**Stop:** 1,0 × ATR14 (dag) vanaf instapprijs.  
**Exit:** hard flat 17:00 CET (60 min na entry). Swap = 0 (intradag).

---

## Onderscheid (niet herstarten als kloon)

- ≠ N12 XAU NY-Open Continuation (FAIL; prior definitie = andere entry/bar; dit = expliciet first-30m drive-sign)
- ≠ N25 XAU NY-PM fade (fade; dit = continuation)
- ≠ N4/N7/N8/N31/N34: andere vensters/mechanismen
- ≠ XAU_AM_FADE (London AM fade; dit = NY-open drive)

---

## Formele test (U2 — na freeze)

- **Data:** `data/m5gz/XAUUSDcash.csv.gz`, train 2021-01-01 … 2023-12-31.  
- **Test:** `data/m5gz/XAUUSDcash.csv.gz`, test 2024-01-01 … 2024-12-31.  
- **Maatstaf:** dag-geclusterd t (Newey-West L=5); drempel t ≥ 2,0.  
- **Stress-gate:** mean bruto ≥ 1,5× gate = **3,74 bp**.  
- **D-094a (b):** year-split 2021/2022/2023 + 2024 (test); geen reserve (tenzij CEO-vrijgave).  
- **TRIAL_COUNT:** append ALLEEN bij formele t-test.
