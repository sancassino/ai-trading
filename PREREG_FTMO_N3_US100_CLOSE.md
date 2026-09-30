# PREREG_FTMO_N3 — US100 Close-Drive Momentum (FTMO-EV variant)

**Status:** Pre-registratie 2026-10-01 01:30 Europe/Amsterdam, branch `claude/trusting-faraday-34tsmg`.  
**Auteur:** Strateeg (Claude). **Geen resultaten vóór deze commit.**  
**Tier:** D-091.3 (nieuw, non-clone); screen top-10 (US100 hoogste bruto/RT-ratio per `results/screen_cost_vol.csv`).  
**Relatie:** Distinct van A1 ORB (ochtend-OR, opening-mechanisme), GS01 (gap-filter, ochtend), XAU_AM_FADE (andere asset/tijd), B4b (onvoorwaardelijke laatste-30-min, gefaald). Nieuw mechanisme: end-of-session gamma-hedging + institutionele portefeuilleherweging.

---

## 1. Bevroren regel (exact)

**Idee (structurele bron):** In de laatste 60–90 min van de US equity-sessie (14:30–16:00 ET = 20:30–22:00 CET) voeren market makers delta/gamma-hedging uit op expirerende opties en doen institutionele fondsen hun dagelijkse herweging. Als de dag tot 14:30 ET al een duidelijke richting heeft, versterkt dit de beweging richting het einde. Mechanisme: optie-flow + rebalancings-inertie, geen patroon-mining.

**Universe (vooraf vast):** `US100cash`.

**Trend-filter (intraday richting):** bereken koers-beweging van 11:00 ET (17:00 CET) slotkoers t.o.v. 09:30 ET (15:30 CET) open:
- **Long-signaal:** als close 11:00 ET > open 09:30 ET × 1.003 (+0,30%) → long entry op 14:30 ET close-bar.
- **Short-signaal:** als close 11:00 ET < open 09:30 ET × 0.997 (−0,30%) → short entry op 14:30 ET close-bar.
- Geen signaal (movement < 0,30%): geen trade die dag.

**Entry:** op close van 14:30 ET bar (20:30 CET). One trade per dag; geen herentry.

**Stop:** 1× ATR14 (dag; gebaseerd op vorige 14 sessie-OHLC's) vanaf instapprijs.

**Exit:** flat op 15:55 ET (21:55 CET) — 5 min vóór officieel slotauction (vermijdt expiratie-volatiliteit van de allerlaatste minuten). Houdduur ≈ 85 min; swap = 0 (intradag-vlak).

**Kosten (FTMO-cfd):**
- US100cash rondreis: spread + commissie ≈ 0,60 bp (COSTS_FTMO.csv, S0-meting).
- Swap = 0 (intradag).
- Kostenpoort-drempel: mean bruto ≥ 3 × 0,60 = **1,80 bp** (train 2021–2023).

---

## 2. Varianten

Geen varianten; één bevroren regel. De 0,30%-drempel is voor commit vastgelegd op basis van economische logica (te kleine beweging = geen richting; te groot = te weinig trades). Geen post-hoc aanpassing toegestaan.

---

## 3. Instrumenten en data

- FTMO-M5 `data/m5gz/US100cash.csv.gz` (of `data/m5/`), 2021–2026.
- Dag-ATR14 uit sessie-OHLC (14 vorige dagen).
- Kosten: `COSTS_FTMO.csv` (main).
- **Geen 2025-data** voor kostenpoort of beslisregel.

---

## 4. Train/test en beslisregel

- **Train:** 2021-01-01 … 2023-12-31.
- **Test:** 2024-01-01 … 2024-12-31 (plafond ≤ 2024-12-31).
- **Reserve:** 2025-01-01 → **ONAANGERAAKT** (D-084/D-091.5).
- **Beslisregel (vooraf):**
  - Kostenpoort (gratis): mean bruto ≥ 1,80 bp op train → anders **STOP, geen trial**.
  - Kostenpoort PASS: dag-geclusterd t (Newey-West, L=5) ≥ 2,0 (train) **en** test-t ≥ 1,5 **en** FTMO-EV ≥ €100/poging → **bevestigd**.
  - t < 1 of netto ≤ 0 → **verworpen** (trial +1).
- **DSR:** TRIAL_COUNT + 1 na kostenpoort-PASS.
- **Verwachte N:** ≈ 120–180 signaal-dagen per jaar × 3 jaar train = ≈ 360–540 trades (filter filtert ~50–70%).

---

## 5. Faalrisico's

1. Filter te loos (0,30% levert te weinig selectiviteit op 30-min bar) → lage bruto.
2. 2022-regime hoog → trend-filter werkt in trending markten maar niet in sideways/mean-revert 2024.
3. Optie-flow is onzichtbaar in OHLC-data; mechanisme is moeilijk te falsifiëren.
4. B4b (onvoorwaardelijke laatste-30-min) was negatief → conditionering op dagtrend is de extra hypothese die dit onderscheidt.
