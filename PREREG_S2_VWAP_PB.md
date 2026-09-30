# PREREG_S2_VWAP_PB — Morning-trend VWAP pullback continuation (intraday-vlak)

**Status:** Pre-registratie 2026-10-01 ~00:49 Europe/Amsterdam, branch `grok/strateeg-2`.  
**Auteur:** Strateeg-2. **Geen resultaten vóór deze commit.**  
**D-091.3 / NEXT_STEPS v46:** non-clone na N3/N4 + MIDDAY_VWAP STOP; screen top-10 (`US100cash`/`US30cash`).  
**≠** `PREREG_S2_MIDDAY_VWAP` (die *fadet* afwijking *van* VWAP); **≠** N1 (T+30 open-drive fade); **≠** ORB/A1/GS01 (geen OR-break); **≠** N3 (close-drive).

**Universum:** `US100cash` (RT 0,66 bp), `US30cash` (RT 0,45 bp).

---

## 1. Bevroren regel (exact)

**Mechanisme:** na een duidelijke ochtendrichting trekt prijs vaak terug naar sessie-VWAP (inventory refill) vóór trend-hervatting. We kopen/verkopen de **pullback naar VWAP in de richting van de ochtendtrend** — continuation, geen mean-reversion-fade.

**Session:** US cash open → close (zelfde DST als bestaande M5-sims).

**VWAP:** cumulatief typical-price VWAP = Σ((H+L+C)/3)/n vanaf session_open (of volume-VWAP als volume aanwezig).

**Ochtend-bias (vast om T0+90 min):**
- `morn_bp = 1e4 × (P_T90 − P_open) / P_open`
- `atr_bp = 1e4 × ATR(14,D1) / P_open`
- Bias **LONG** als `morn_bp ≥ +0,30 × atr_bp`
- Bias **SHORT** als `morn_bp ≤ −0,30 × atr_bp`
- Anders → geen trade die dag

**Pullback-entry (T0+105 … T0+210, eerste touch, max 1/dag):**
- LONG-bias: als M5 low ≤ VWAP ≤ M5 high **én** `P_close ≥ VWAP` → **LONG** op die bar-close  
  (prijs heeft VWAP geraakt vanuit boven / hervat boven VWAP)
- SHORT-bias: als M5 low ≤ VWAP ≤ M5 high **én** `P_close ≤ VWAP` → **SHORT** op die bar-close
- Geen VWAP-touch in venster → flat

**Exit (swap = 0):**
1. **Target:** ochtend-extreem (LONG → H_open_T90; SHORT → L_open_T90); bij touch → flat  
2. **Stop:** `0,50 × atr_bp` voorbij VWAP *tegen* bias (LONG-stop onder VWAP; SHORT-stop boven VWAP). Same-bar → stop wint.  
3. **Time:** flatten T0+300 min (≈ 14:30 ET) — bewust vóór N3 close-drive venster

**Verboden na zien:** 0,30× bias, entry-venster, target=ochtend-extreem, 0,50× stop, T0+300 flat wijzigen. Report-only: bias 0,20× / 0,45×.

**≠ MIDDAY_VWAP:** MIDDAY short wanneer `dev_bp` *boven* VWAP (fade); dit *long* bij pullback *naar* VWAP na up-ochtend (continuation).  
**≠ N1:** N1 fadet grote T+30 drive terug naar open; dit volgt ochtendtrend na latere VWAP-test.

---

## 2. Kosten & poort

- RT: US100 0,66 / US30 0,45 bp (`COSTS_FTMO.csv`).  
- Poort train (2021–2023, pooled): **getekend gemiddeld bruto bp/trade ≥ 3×** gewogen RT.  
- +50% RT-stress. FAIL → STOP, geen trial.

---

## 3. Data / venster

- M5gz US100/US30 2021–2024-12.  
- **Train:** 2021-01-01 … 2023-12-31  
- **Test:** 2024-01-01 … 2024-12-31  
- **Reserve 2025→ ONAANGERAAKT**.

---

## 4. Beslisregel

1. Kostenpoort eerst. PASS → TRIAL_COUNT +1.  
2. Dag-geclusterde netto t ≥ 2,0 train én test; mean netto > 0 beide; N_trades ≥ 150 pooled train.  
3. Kosten < 50% bruto. Skew dag-PnL rapporteren (verwacht > 0 bij runners naar ochtend-extreem).  
4. Corr vs MIDDAY_VWAP / N1 / A1-ORB (informatief; teken-corr vs MIDDAY verwacht ≤ 0).  
5. `ftmo_ev()`; p95 dagverlies ≤ 2%; FTMO-EV ≥ €150/poging.

---

## 5. Faalrisico's

Ochtendtrend faalt na VWAP-touch (V-vormige omkeer); smalle ochtenden → weinig bias-dagen; overlap-PnL met dode MIDDAY op grote trend-dagen (corr-check verplicht); target=ochtend-extreem kan te dicht bij entry liggen → bruto < 3× RT.

---

**Bevroren:** 2026-10-01 00:49 CEST — D-091.3 non-clone (v46 urgent).  
**Auteur:** Strateeg-2 (`grok/strateeg-2`)
