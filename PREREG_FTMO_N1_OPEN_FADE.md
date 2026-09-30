# PREREG_FTMO_N1 — Opening-drive exhaustion FADE (intraday-vlak)

**Status:** Pre-registratie 2026-09-30 23:55 Europe/Amsterdam, branch `claude/trusting-faraday-34tsmg`.  
**Uitkomst (Uitvoerder-2, `8c7a8e1`, ~00:05 CEST):** **FORMEEL GESTOPT** — poort n=0 (1,5× D1-ATR nooit geraakt door 30-min drive op train). Geen trial. U2-note: drempel lijkt mis-scaled (max |drive|/ATR ≈ 0,3–0,9) — **geen post-hoc heropening** zonder CEO/nieuw distinct PREREG.  
**Auteur:** Strateeg (Grok).  
**D-091 prio 3:** niet-kloon; **≠ ORB/breakout** (A1/A2/A5/GS01/S2-open).  
**Universum (top cost/vol-screen, COSTS aanwezig):** `US100cash`, `US30cash`, `US500cash` (rank_day 1–2–4 in `results/screen_cost_vol.csv`).

---

## 1. Bevroren regel (exact)

**Mechanisme:** na een *grote* openingsdrive is er tijdelijke liquiditeitsonbalans / stop-cascade; een deel mean-revert naar de open vóór EOD. Positief-scheef als stop op continuatie strak is en winstdoel dichtbij open ligt.

**Session:** cash-sessie per symbool (zelfde DST-conventie als bestaande ORB-sims / `b4_sim` open-tijd).

**Drive-venster:** van session_open tot T0+30 min (6× M5).  
`drive_bp = 1e4 × (P_T30 − P_open) / P_open`.  
`atr_bp = 1e4 × ATR(14, D1) / P_open` (ATR op voorgaande D1-closes).

**Trigger (één trade/symbool/dag, max één richting):**
- Als `drive_bp ≥ +1,5 × atr_bp` → **SHORT** op close van T+30-bar (fade omhoog-drive).
- Als `drive_bp ≤ −1,5 × atr_bp` → **LONG** op close van T+30-bar (fade omlaag-drive).
- Anders → geen trade.

**Exit (intraday-vlak, swap = 0):**
1. **Target:** mid tussen entry en open (`0,5 × |P_entry − P_open|` terug naar open) — first touch / M5 close door target.
2. **Stop:** `1,0 × |drive|` voorbij entry in drive-richting (continuatie). Same-bar target+stop → **stop wint**.
3. **Time stop:** flatten op session close als nog open.

**Verboden na zien:** drempel 1,5×, 30-min venster, target/stop-ratio wijzigen. Vooraf-sensitivity (alleen rapporteren, geen selectie): drempel 1,25× en 1,75× ATR.

**≠ ORB:** ORB handelt *with* break van opening-range high/low. N1 handelt *tegen* een al voltooide 30-min drive en vereist magnitude-filter; geen OR-high/low breakout-orders.

---

## 2. Kosten & poort

- RT uit `COSTS_FTMO.csv`: US100 0,66 / US30 0,45 / US500 0,78 bp.  
- Poort (train 2021–2023, pooled primary): **getekend gemiddeld bruto bp/trade ≥ 3×** gewogen gemiddelde RT van trades.  
- +50% spread-gevoeligheid rapporteren. FAIL → STOP, geen trial-analyse.

---

## 3. Data / venster

- M5gz index-reeks 2021–2024-12.  
- **Train:** 2021-01-01 … 2023-12-31  
- **Test:** 2024-01-01 … 2024-12-31  
- **Reserve 2025-01→ ONAANGERAAKT** (D-084 / D-091.5).

---

## 4. Stats & FTMO-EV

1. Poort eerst. Bij PASS → TRIAL_COUNT +1.  
2. Dag-geclusterde netto t (Newey-West) ≥ 2,0 train **én** test; mean netto bp > 0 beide helften; N_trades ≥ 150 pooled train.  
3. Skew van dag-PnL rapporteren (verwacht > 0).  
4. Correlatie dag-PnL vs B4a/GS01 ORB-series (informatief; hoge corr → minder diversificatie).  
5. `engine/ftmo.py` na PASS; sizing p95 dagverlies ≤ 2%.

---

## 5. Faalrisico's

Drive-dagen te zeldzaam (N); continuatie-regime (2022 trend) eet fades; target te strak → weinig wins na kosten; overlap met dode C40 H1-omkeer — distinct door ATR-magnitude + 30-min fix + target-naar-open.

---
**Bevroren:** 2026-09-30 23:55 CEST — D-091 nacht.  
**Auteur:** Strateeg (`claude/trusting-faraday-34tsmg`)
