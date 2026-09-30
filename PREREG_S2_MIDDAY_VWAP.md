# PREREG_S2_MIDDAY_VWAP — Midday VWAP mean-reversion fade (intraday-vlak)

**Status:** Pre-registratie 2026-10-01 ~00:00 Europe/Amsterdam, branch `grok/strateeg-2`.  
**Auteur:** Strateeg-2. **Geen resultaten vóór deze commit.**  
**Nacht D-091:** non-clone; **≠ ORB/breakout** (A1/A2/A5/GS01/S2-open); **≠ N1** (N1 = T+30 opening-drive fade); **≠ N2** (pair dispersie).  
**Universum (top COSTS aanwezig):** `US100cash`, `US30cash` (RT 0,66 / 0,45 bp).

---

## 1. Bevroren regel (exact)

**Mechanisme:** na de openingsliquiditeit trekt prijs vaak terug naar sessie-VWAP (inventory / dealer-hedging). We faden *afwijking van VWAP in het middagvenster*, niet de open-drive en niet een range-break.

**Session:** US cash open → close (zelfde DST als bestaande M5-sims).

**VWAP:** cumulatief volume-weighted average vanaf session_open tot entry-bar (M5; als volume ontbreekt → typical-price VWAP = Σ((H+L+C)/3)/n bars sinds open).

**Entry-venster:** T0+150 min tot T0+210 min (≈ 12:00–13:00 ET bij 09:30 open; 6× M5-checkpunten).  
Eerste bar in dat venster die voldoet:

- `dev_bp = 1e4 × (P_close − VWAP) / VWAP`
- `atr_bp = 1e4 × ATR(14,D1) / P_open` (voorgaande dagen)
- Als `dev_bp ≥ +0,75 × atr_bp` → **SHORT** op die bar-close (fade boven VWAP)
- Als `dev_bp ≤ −0,75 × atr_bp` → **LONG** op die bar-close
- Anders → geen trade die dag (max 1 trade/symbool/dag)

**Exit (swap = 0):**
1. **Target:** touch VWAP (M5 high/low door VWAP)  
2. **Stop:** `1,0 × |dev_bp|` verder van VWAP voorbij entry (same-bar → stop wint)  
3. **Time:** flatten T0+330 min (≈ 15:00 ET) of session close als eerder

**Verboden na zien:** 0,75×, entry-venster, target=VWAP wijzigen. Report-only sensitivity: 0,5× en 1,0× ATR.

**≠ N1:** N1 triggert op T+30 drive-magnitude t.o.v. open; dit triggert pas middag op VWAP-afwijking.  
**≠ ORB:** geen break van opening-range high/low.

---

## 2. Kosten & poort

- RT: US100 0,66 / US30 0,45 bp (`COSTS_FTMO.csv`).  
- Poort train (2021–2023, pooled): **getekend gemiddeld bruto bp/trade ≥ 3×** gewogen RT.  
- +50% RT-stress. FAIL → STOP, geen trial.

---

## 3. Data / venster

- M5gz US100/US30 2021–2024-12.  
- Train 2021–2023 / Test 2024 / **Reserve 2025→ ONAANGERAAKT**.

---

## 4. Beslisregel

1. Kostenpoort eerst. PASS → TRIAL_COUNT +1.  
2. Dag-geclusterde netto t ≥ 2,0 train én test; mean netto > 0 beide; N_trades ≥ 150 pooled train.  
3. Kosten < 50% bruto. Skew dag-PnL rapporteren (verwacht > 0).  
4. Corr vs N1 en vs B4a/GS01 ORB (informatief).  
5. `ftmo_ev()`; p95 dagverlies ≤ 2%; FTMO-EV ≥ €150/poging.

---

## 5. Faalrisico's

Trend-middagen zonder VWAP-touch; dun volume → slechte VWAP-proxy; overlap-PnL met N1 op grote open-dagen (corr-check verplicht).

---
**Bevroren:** 2026-10-01 00:00 CEST — nacht non-clone.  
**Auteur:** Strateeg-2 (`grok/strateeg-2`)
