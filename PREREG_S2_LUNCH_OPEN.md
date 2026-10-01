# PREREG_S2_LUNCH_OPEN — US lunch open-anchor fade (intraday-vlak)

**Status:** Pre-registratie 2026-10-01 ~02:45 Europe/Amsterdam, branch `grok/strateeg-2`.  
**Auteur:** Strateeg-2. **Geen formele trial-resultaten vóór deze commit.**  
**D-092.1:** kost-pre-screen PASS op train 2021–2023 (zie `results/strateeg2_prescreen/`) vóór deze PREREG.  
**NEXT_STEPS v53 / C-010:** non-clone na dead set + FAIL pre-screens (PLM/NR7/Failed-OR/XAU-N7/N8).  
**≠** MIDDAY_VWAP (geen VWAP; anker = session open; entry 17:00 AMS ≠ 12–13 ET VWAP-venster); **≠** N1 (T+30 open-drive fade, 1,5×D1-ATR); **≠** IB_FADE (geen IB-range/quintile); **≠** VWAP_PB (fade ≠ continuation); **≠** N3/N5/ORB/GER_US.

**Universum (screen top-RT):** `US30cash` (RT 0,45 bp), `US100cash` (RT 0,66 bp). Beide in SymbolList_FTMO + `data/m5gz/`.

---

## 0. D-092.1 pre-screen (train only — geen selectie op test/reserve)

| Been | N | mean bruto | gate 3×RT | Uitkomst |
|------|--:|----------:|----------:|----------|
| US30cash | 134 | +5,74 bp | 1,35 bp | PASS |
| US100cash | 99 | +3,33 bp | 1,98 bp | PASS |
| **Pooled** | **233** | **+4,72 bp** | **1,62 bp** (3× gewogen RT) | **PASS** |

Skew pooled ≈ +1,52 (positief). Artefacts: `scripts/s2_d092_prescreen_candidates.py`, `results/strateeg2_prescreen/LUNCH_OPEN_FADE_trades_train.csv`.  
**Verboden:** drempels/vensters wijzigen na zien van test/reserve. Report-only: 0,30× / 0,50× ATR-filter.

---

## 1. Bevroren regel (exact — identiek aan pre-screen)

**Mechanisme:** na een duidelijke US-ochtendimpuls (open → T+90) trekt prijs vaak terug richting de auction-open tijdens de lunch-inventarisatie. We **faden de ochtendbeweging terug naar session-open**, niet naar VWAP en niet via IB-extremen.

**Kalender:** Europe/Amsterdam (DST gelijk aan bestaande M5-sims).  
**Session open:** 15:30 Europe/Amsterdam (= 09:30 ET).

**Signalen (max 1 trade / symbool / dag):**
- `P_open` = M5-open van de 15:30-bar  
- `P_entry` = M5-close van de 17:00-bar (T+90)  
- `morn_bp = 1e4 × (P_entry − P_open) / P_open`  
- `atr_bp = 1e4 × ATR(14, D1_prior) / P_open` (ATR van voorgaande dagen; geen lookahead)  
- Als `morn_bp ≥ +0,40 × atr_bp` → **SHORT** op 17:00-close  
- Als `morn_bp ≤ −0,40 × atr_bp` → **LONG** op 17:00-close  
- Anders → geen trade

**Exit (swap = 0, daily-flat):**
1. **Target:** `P_open` (positief-scheef: win ≈ afstand entry→open)  
2. **Stop:** voorbij ochtend-extreem (15:30–17:00 high/low) met buffer `0,15 ×` ochtendrange:
   - SHORT: stop = `morn_high + 0,15 × (morn_high − morn_low)`  
   - LONG: stop = `morn_low − 0,15 × (morn_high − morn_low)`  
   - Same-bar target+stop → **stop wint**
3. **Time:** hard flat **19:00 Europe/Amsterdam** (≈ 13:00 ET) — lunch-venster; vóór late-middag / close-drive (dode N3)

**Sizing:** 0,75% risico per trade (stop-afstand → notional).  
**Verboden na zien:** 0,40× ATR-filter, 0,15× stop-buffer, 17:00 entry, 19:00 flat, open-anker wijzigen.

---

## 2. Kosten & poort

- RT: US30 0,45 bp / US100 0,66 bp (`COSTS_FTMO.csv` / screen).  
- Poort train (2021–2023, pooled): **getekend gemiddeld bruto bp/trade ≥ 3×** gewogen RT — **al PASS in §0**.  
- Formele U2/CTO cost-gate herhaalt +50% RT-stress. FAIL → STOP, geen TRIALS-append.

---

## 3. Data / venster

- M5gz: `US30cash`, `US100cash` (`data/m5gz/`).  
- **Train:** 2021-01-01 … 2023-12-31  
- **Test:** 2024-01-01 … 2024-12-31  
- **Reserve 2025→ ONAANGERAAKT** (D-084 / D-091.5 / D-092).

---

## 4. Beslisregel

1. Kostenpoort (+50% stress) eerst. PASS → TRIAL_COUNT +1.  
2. Dag-geclusterde netto t ≥ 2,0 train én test; mean netto > 0 beide; **N_trades ≥ 150** pooled train (pre-screen N=233).  
3. Kosten < 50% bruto. Skew dag-PnL > 0 **of** max dagdip ≤ −1,5% bij 0,75% risk.  
4. Corr vs MIDDAY_VWAP / N1 / IB_FADE / A1-ORB dagreeksen (informatief); |ρ| > 0,5 vs MIDDAY of N1 ⇒ label "residual clone", geen shortlist.  
5. `ftmo_ev()`; p95 dagverlies ≤ 2%; **FTMO-EV ≥ €150/poging**.

---

## 5. Faalrisico's

Trend-dagen zonder lunch-revert (stop raakt vaak — pre-screen: ~55% stop-exits); median bruto negatief terwijl mean positief (scheve winnaars — power/t gevoelig); US30/US100 hoog gecorreleerd → pool ≠ 2× onafhankelijk; 19:00 flat mist late continuation (bewust vs N3).

---

## 6. Neven-screen (geen PREREG deze cyclus)

`UK_AM_FADE` (UK100 London-AM extension fade) pre-screen PASS (N=86, mean +8,47 bp ≥ gate 4,26) maar **N ≪ 150** → geen PREREG tot power-pad bestaat. `EUR_NY_FADE` FAIL (mean −0,69 bp). Details in `results/strateeg2_prescreen/prescreen.md`.

---

**Bevroren:** 2026-10-01 02:45 CEST — D-092.1 pre-screened non-clone (v53 / C-010).  
**Auteur:** Strateeg-2 (`grok/strateeg-2`)
