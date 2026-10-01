# PREREG_FTMO_N6 — GER40 Pre-Close Conditioneel Momentum (FTMO-EV variant)

**Status:** Pre-registratie 2026-10-01 02:05 Europe/Amsterdam, branch `claude/trusting-faraday-34tsmg`.  
**Uitkomst (Uitvoerder-2 `741639e` / CTO C-008 `9f5c843`, C-007):** **FORMEEL GESTOPT** — kostenpoort TRAIN FAIL. Dead set. Geen herstart zonder CEO.  
**Auteur:** Strateeg (Claude). Resultaten pas ná freeze-SHA.  
**Tier:** D-091.3 (nieuw, non-clone); screen top-10 (GER40 top-3 RT-ratio).  
**Relatie:** Distinct van A1 ORB / GS01 (ochtend-OR, gap-filter). Distinct van B4b (onvoorwaardelijke laatste-30-min, gefaald). **Conditionele** versie met 2-uur-trend-filter.

---

## 1. Bevroren regel (exact)

**Idee (structurele bron):** Bij de GER40-slotauction (18:00 CET) doen XETRA-ETF's, indexfondsen en derivaten-delta-hedgers hun dagelijkse herweging. Dit versterkt de richting van de dominante dagtrend in de laatste 30 minuten vóór de slotauction. B4b (onvoorwaardelijk laatste-30-min) faalde; de conditionering op de dagtrend is de hypothese die dit onderscheidt van een louter markt-microstructuur effect (positief-scheef ORB vs flat rebalancing).

**Universe (vooraf vast):** `GER40cash`.

**Dag-trend-filter (2-uur lookback):** bereken koersniveau op 15:30 CET t.o.v. 13:30 CET:
- **Long-signaal:** als close 15:30 CET > open 13:30 CET × 1.002 (+0,20%) → long entry op 17:30 CET close-bar.
- **Short-signaal:** als close 15:30 CET < open 13:30 CET × 0.998 (−0,20%) → short entry op 17:30 CET close-bar.
- Geen trade als |beweging| < 0,20%: geen trade die dag.

**Entry:** op close van 17:30 CET bar. One trade per dag; geen herentry.

**Stop:** 0,75 × ATR14 (dag) vanaf instapprijs. Tightere stop dan N3 vanwege korter houdvenster.

**Exit:** flat op 17:55 CET — 5 min vóór officiële XETRA-slotauction (18:00 CET). Houdduur ≈ 25 min; swap = 0 (intradag-vlak).

**Kosten (FTMO-cfd):**
- GER40cash rondreis: spread + commissie ≈ 1,40 bp (COSTS_FTMO.csv, S0-meting).
- Swap = 0 (intradag).
- Kostenpoort-drempel: mean bruto ≥ 3 × 1,40 = **4,20 bp** (train 2021–2023). Streng, maar GER40 heeft hoge volatiliteit (dagrange ≈ 60–100 bp).

---

## 2. Varianten

Geen varianten; één bevroren regel. Trend-drempel 0,20% vooraf economisch gemotiveerd (GER40-dagrange ≈ 0,5–1,5%; 0,20% = ondergrens zinvolle directionaliteit). Geen post-hoc aanpassing.

---

## 3. Instrumenten en data

- FTMO-M5 `data/m5gz/GER40cash.csv.gz` (of `data/m5/`), 2021–2026.
- Dag-ATR14 uit sessie-OHLC.
- Kosten: `COSTS_FTMO.csv` (main).
- **Geen 2025-data** voor kostenpoort of beslisregel.

---

## 4. Train/test en beslisregel

- **Train:** 2021-01-01 … 2023-12-31.
- **Test:** 2024-01-01 … 2024-12-31 (plafond ≤ 2024-12-31).
- **Reserve:** 2025-01-01 → **ONAANGERAAKT** (D-084/D-091.5).
- **Beslisregel (vooraf):**
  - Kostenpoort (gratis): mean bruto ≥ 4,20 bp op train → anders **STOP, geen trial**.
  - Kostenpoort PASS: dag-geclusterd t (Newey-West, L=5) ≥ 2,0 (train) **en** test-t ≥ 1,5 **en** FTMO-EV ≥ €100/poging → **bevestigd**.
  - t < 1 of netto ≤ 0 → **verworpen** (trial +1).
- **DSR:** TRIAL_COUNT + 1 na kostenpoort-PASS.
- **Verwachte N:** ≈ 120–160 signaal-dagen/jaar × 3 jaar = ≈ 360–480 trades.

---

## 5. Faalrisico's

1. B4b (onvoorwaardelijk) was negatief op GER40 → conditionering op 0,20%-trend is extra hypothese; kan onvoldoende selectief zijn.
2. Kostenpoort-drempel 4,20 bp is streng: met 25 min houdvenster moet gemiddelde move ≥ 4,20 bp zijn — dat vereist ca. 0,4% dagmove in de richting.
3. In laag-volregime (2024 GER40) zijn de 0,20%-drempel-signalen minder betrouwbaar.
4. Kleine houdperiode (25 min): transactie-timing-gevoeligheid groot.
