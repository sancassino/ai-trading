# PREREG_S2_IB_FADE — US cash Initial-Balance extreme fade (intraday-vlak)

**Status:** Pre-registratie 2026-10-01 ~01:48 Europe/Amsterdam, branch `grok/strateeg-2`.  
**Auteur:** Strateeg-2. **Geen resultaten vóór deze commit.**  
**D-091 cyclus-4 / NEXT_STEPS v50 / C-008:** non-clone na C-007 kill (N6/GER_US_LEAD/VWAP_PB FAIL); screen top RT `US30cash`/`US100cash`.  
**≠** N1 (T+30 open-drive fade → open, 1,5×D1-ATR); **≠** A1/GS01/ORB (wij *faden* IB-extremen, we *breken* geen opening-range); **≠** N5 (gap-fill); **≠** MIDDAY_VWAP (middag VWAP-fade); **≠** VWAP_PB (ochtendtrend+VWAP-pullback continuation); **≠** N3 (close-drive); **≠** GER_US_LEAD.

**Universum:** `US30cash` (primair, RT 0,45 bp), `US100cash` (secundair, RT 0,66 bp). Beide in SymbolList_FTMO + `data/m5gz/`.

---

## 1. Bevroren regel (exact)

**Mechanisme:** de US cash **Initial Balance** (eerste 60 min) is vaak inventory-/auction-range. Als de IB *breed* is én de prijs sluit nabij een IB-extreem, is dat typisch late-IB aggressie die intradag mean-revertert richting IB-mid — geen OR-breakout-edge.

**Kalender:** Europe/Amsterdam (DST gelijk aan bestaande M5-sims).

**IB-venster:** 15:30–16:30 Europe/Amsterdam (= 09:30–10:30 ET).  
`IB_high` / `IB_low` = high/low van M5-bars in dat venster.  
`IB_mid = (IB_high + IB_low) / 2`  
`IB_range_bp = 1e4 × (IB_high − IB_low) / P_1530`  
`atr_bp = 1e4 × ATR(14, D1) / P_1530`  
`P_IB_close` = M5-close van de 16:25–16:30 bar (of laatste M5 in IB-venster).

**Filter (max 1 trade / symbool / dag):**
1. Breedte: `IB_range_bp ≥ 0,55 × atr_bp` (anders geen trade)
2. Extreem-positie in IB:
   - `pos = (P_IB_close − IB_low) / (IB_high − IB_low)` (guard: IB_high > IB_low)
   - Als `pos ≥ 0,80` → **SHORT** op IB-close (fade upper extreme)
   - Als `pos ≤ 0,20` → **LONG** op IB-close (fade lower extreme)
   - Anders → geen trade

**Exit (swap = 0, daily-flat):**
1. **Target:** `IB_mid` (positief-scheef: win ≈ afstand entry→mid; stop ruimer — zie hieronder)
2. **Stop:** voorbij IB-extreem met buffer `0,25 × IB_range`:
   - SHORT: stop = `IB_high + 0,25 × (IB_high − IB_low)`
   - LONG: stop = `IB_low − 0,25 × (IB_high − IB_low)`
   - Same-bar target+stop → **stop wint**
3. **Time:** hard flat 20:00 Europe/Amsterdam (≈ 14:00 ET) — vóór close-drive-regime van dode N3

**Verboden na zien:** 0,55× ATR-breedte, 0,80/0,20 pos-drempels, 0,25× stop-buffer, 15:30–16:30 IB, 20:00 flat wijzigen.  
**Report-only (geen selectie):** breedte 0,40× / 0,70×; pos 0,75/0,25.

**≠ N1:** N1 meet T+30 drive vs *open* met 1,5×D1-ATR en target→open; hier is trigger = *IB-range + IB-close quintile*, target→IB-mid, entry pas na volle 60 min IB.  
**≠ ORB:** ORB koopt/verkoopt *break* van OR; wij shortten/longen *binnen* een brede IB bij extreme close.

---

## 2. Kosten & poort

- RT: US30 0,45 bp / US100 0,66 bp (`COSTS_FTMO.csv`).  
- Poort train (2021–2023, pooled over symbolen met trades): **getekend gemiddeld bruto bp/trade ≥ 3×** gewogen RT.  
  - US30-drempel ≥ 1,35 bp; US100 ≥ 1,98 bp.  
- +50% RT-stress. FAIL → STOP, geen trial / geen TRIALS-append.

---

## 3. Data / venster

- M5gz: `US30cash`, `US100cash` 2021–2024-12 (`data/m5gz/`).  
- **Train:** 2021-01-01 … 2023-12-31  
- **Test:** 2024-01-01 … 2024-12-31  
- **Reserve 2025→ ONAANGERAAKT** (D-084 / D-091.5).

---

## 4. Beslisregel

1. Kostenpoort eerst. PASS → TRIAL_COUNT +1.  
2. Dag-geclusterde netto t ≥ 2,0 train én test; mean netto > 0 beide; **N_trades ≥ 150** pooled train.  
3. Kosten < 50% bruto. Skew dag-PnL > 0 **of** max dagdip ≤ −1,5% bij 0,75% risk.  
4. Corr vs N1 / vs A1-ORB / vs MIDDAY_VWAP dagreeksen (informatief); |ρ| > 0,5 vs N1 of ORB ⇒ label "residual clone", geen shortlist.  
5. `ftmo_ev()`; p95 dagverlies ≤ 2%; **FTMO-EV ≥ €150/poging**.

---

## 5. Faalrisico's

Trend-dagen met IB die de dagrange *start* (geen revert naar mid); te strenge 0,55× ⇒ lage N; 20:00 flat mist late continuatie (bewust vs N3); US30/US100 hoog gecorreleerd → pool ≠ 2× onafhankelijk.

---

**Bevroren:** 2026-10-01 01:48 CEST — D-091 cyclus-4 non-clone (v50 / C-008).  
**Auteur:** Strateeg-2 (`grok/strateeg-2`)
