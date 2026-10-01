# PREREG_FTMO_N35 — US100cash Europe-Session Momentum → US Open Continuation

**Status:** FROZEN — D-092.1 PASS (U2 `43c395e`; mean +6,60 bp > gate 1,98 bp; N=214). Wacht op U2 cost-gate + formele t-test.  
**Auteur:** Strateeg (Claude/Grok). **Instrument:** `US100cash`.  
**TRIAL_COUNT bij freeze:** 448.  
**SHA VOORSTEL (regel):** commit `7ede6d0` (VOORSTEL_PRESCREEN_N35.md, filed 2026-10-01 ~08:28 CEST).

---

## Instrument & kosten

- **Symbool:** `US100cash`
- **Round-trip kosten (COSTS_FTMO.csv):** 0,66 bp
- **Gate (3× RT):** 1,98 bp
- **D-092.1 screen:** N=214, mean bruto +6,60 bp → **PASS**

---

## Regel (bevroren — identiek aan VOORSTEL)

**Europe-session momentum:**
- `C_0900` = M5-close van de 09:00 CET bar  
- `C_1500` = M5-close van de 15:00 CET bar  
- `eu_bp = 1e4 × (C_1500 − C_0900) / C_0900`

**Signalen (max 1 trade/dag):**
- `eu_bp ≥ +40 bp` → **LONG** op 15:30 CET close (continuation EU-trend in US-open)  
- `eu_bp ≤ −40 bp` → **SHORT** op 15:30 CET close  
- Anders → geen trade

**Stop:** 1,0 × ATR14 (dag) vanaf instapprijs.  
**Exit:** hard flat 17:00 CET (90 min na entry). Swap = 0 (intradag).

---

## Onderscheid (niet herstarten als kloon)

- ≠ N3 US100 close-drive (14:30–15:55 ET; dit = EU-uren als signal)
- ≠ N14 US100 NY pre-market momentum (pre-market move; dit = EU-sessie move)
- ≠ N20 US30 PM continuation (andere entry-tijd en instrument)
- ≠ ORB-familie (N11/N15–N17): geen range-breakout; dit = session-level trend

---

## Formele test (U2 — na freeze)

- **Data:** `data/m5gz/US100cash.csv.gz`, train 2021-01-01 … 2023-12-31.  
- **Test:** `data/m5gz/US100cash.csv.gz`, test 2024-01-01 … 2024-12-31.  
- **Maatstaf:** dag-geclusterd t (Newey-West L=5); drempel t ≥ 2,0.  
- **Stress-gate:** mean bruto ≥ 1,5× gate = **2,97 bp**.  
- **D-094a (b):** year-split 2021/2022/2023 + 2024 (test); geen reserve (tenzij CEO-vrijgave).  
- **TRIAL_COUNT:** append ALLEEN bij formele t-test.
