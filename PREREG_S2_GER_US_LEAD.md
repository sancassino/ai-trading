# PREREG_S2_GER_US_LEAD — GER40 Europe-AM impulse → US100/US500 open continuation (intraday-vlak)

**Status:** Pre-registratie 2026-10-01 ~00:49 Europe/Amsterdam, branch `grok/strateeg-2`.  
**Auteur:** Strateeg-2. **Geen resultaten vóór deze commit.**  
**D-091.3 / NEXT_STEPS v46:** non-clone na N3/N4 STOP; screen top-10 (`US100cash`/`US500cash`/`GER40cash`).  
**≠** N2 (zelfde-sessie US100↔US500 z-score pair); **≠** ORB/A1/GS01 (geen opening-range break); **≠** dode S2-GER40_OPEN (handelden GER40 zelf bij Frankfurt-open); **≠** N3 (US100 close-drive); **≠** N1 (open-drive fade).

**Universum (executie):** `US100cash` (primair, RT 0,66 bp), `US500cash` (secundair, RT 0,78 bp).  
**Signaalbron (geen trade):** `GER40cash` Europe-AM impuls.

---

## 1. Bevroren regel (exact)

**Mechanisme:** Europese cash-impuls op GER40 (Frankfurt-ochtend tot pre-US) is vaak een *lead* voor US cash-open: macro/risk-on flow die eerst DAX raakt, daarna US indices. We handelen **US-index in de richting van de GER40-impuls bij US cash-open**, niet GER40 zelf en niet een OR-break.

**Kalender:** Europe/Amsterdam (DST gelijk aan bestaande M5-sims).

**GER40 impuls-venster:** 09:00–15:15 Europe/Amsterdam.  
`ger_bp = 1e4 × (P_GER_1515 − P_GER_0900) / P_GER_0900`  
`atr_ger_bp = 1e4 × ATR(14,D1_GER) / P_GER_0900`

**Filter (max 1 trade / symbool / dag):**
- Als `ger_bp ≥ +0,40 × atr_ger_bp` → **LONG** US-index op US cash-open M5-close (≈ 15:30 Amsterdam / 09:30 ET)
- Als `ger_bp ≤ −0,40 × atr_ger_bp` → **SHORT** US-index op US cash-open M5-close
- Anders → geen trade die dag

**Exit (swap = 0, daily-flat):**
1. **Target:** `+1,0 × atr_us_bp` in trade-richting (`atr_us_bp = 1e4 × ATR(14,D1_US) / P_US_open`)
2. **Stop:** `0,75 × atr_us_bp` tegen trade-richting (same-bar → stop wint)
3. **Time:** hard flat 20:00 Europe/Amsterdam (≈ 14:00 ET) — vóór close-drive-regime van dode N3

**Verboden na zien:** 0,40× filter, 09:00–15:15 anker, 20:00 flat, target/stop ATR-multiples wijzigen. Report-only: 0,30× / 0,55× GER-filter.

**≠ N2:** N2 is intraday *relative* US100−US500 z-score (beide US, pair); dit is *cross-session lead* GER→US, single-leg directional.  
**≠ S2-GER40_OPEN:** die tradede GER40 open-drive; hier is GER alleen signaal, executie = US.

---

## 2. Kosten & poort

- RT: US100 0,66 / US500 0,78 bp (`COSTS_FTMO.csv`).  
- Poort train (2021–2023, pooled over symbolen met trades): **getekend gemiddeld bruto bp/trade ≥ 3×** gewogen RT.  
  - US100-drempel ≥ 1,98 bp; US500 ≥ 2,34 bp.  
- +50% RT-stress. FAIL → STOP, geen trial.

---

## 3. Data / venster

- M5gz: `GER40cash`, `US100cash`, `US500cash` 2021–2024-12.  
- **Train:** 2021-01-01 … 2023-12-31  
- **Test:** 2024-01-01 … 2024-12-31  
- **Reserve 2025→ ONAANGERAAKT** (D-084 / D-091.5).

---

## 4. Beslisregel

1. Kostenpoort eerst. PASS → TRIAL_COUNT +1.  
2. Dag-geclusterde netto t ≥ 2,0 train én test; mean netto > 0 beide; N_trades ≥ 150 pooled train.  
3. Kosten < 50% bruto. Skew dag-PnL > 0 of max dagdip ≤ −1,5% bij 0,75% risk.  
4. Corr vs N2 / vs A1-ORB / vs S2-GER40_OPEN (informatief; |ρ| > 0,5 vs dode GER40_OPEN ⇒ "residual clone", geen shortlist).  
5. `ftmo_ev()`; p95 dagverlies ≤ 2%; FTMO-EV ≥ €150/poging.

---

## 5. Faalrisico's

GER→US lead zwak buiten EU-macro-dagen; US gap tegen GER-impuls → stop-cascade; 20:00 flat mist late continuatie (bewust vs N3); lage N als 0,40× te streng.

---

**Bevroren:** 2026-10-01 00:49 CEST — D-091.3 non-clone (v46 urgent).  
**Auteur:** Strateeg-2 (`grok/strateeg-2`)
