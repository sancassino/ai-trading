# PREREG_FTMO_N5 — US500/US100 Opening Gap Fill (FTMO-EV variant)

**Status:** Pre-registratie 2026-10-01 02:05 Europe/Amsterdam, branch `claude/trusting-faraday-34tsmg`.  
**Auteur:** Strateeg (Claude). **Geen resultaten vóór deze commit.**  
**Tier:** D-091.3 (nieuw, non-clone, cyclus 3/4); screen top-10 (US500/US100 top-RT).  
**Relatie:** Distinct van A1 ORB / GS01 (ORB = gap-continuation; dit = gap-fade, tegengestelde richting). Distinct van N3 (N3 = last-hour trend-continuation; dit = opening-gap-reversion). Nieuw mechanisme: overnight overreactie + liquiditeits-absorptie bij open.

---

## 1. Bevroren regel (exact)

**Idee (structurele bron):** Wanneer US-indices significant gap-up of gap-down openen, weerspiegelt de prijs bij open de informatie van overnight nieuws. Market makers en arbitrage-handelaars absorberen de orderflow in de eerste 30–60 minuten, wat vaak leidt tot een partiële fill van de gap. Mechanisme: overnight overreaction + directional mean-reversion door market-making flow — structureel, niet patroon-mining. Onderscheidend van GS01 (gap-continuation; GS01 koopt breakout nà gap omhoog): dit is de tegengestelde thesis.

**Universe (vooraf vast):** `US500cash`, `US100cash` (twee symbolen; gepoolde familie).

**Gap-definitie:** `gap = session_open / prior_session_close − 1` (berekend op exacte OHLC van eerste M5-bar versus laatste M5-bar vorige sessie).

**Signaal-filter:** alleen handelen als |gap| ≥ **0,30%**.
- **Gap up ≥ +0,30%:** short entry op close van eerste M5-bar (15:30 CET / 09:30 ET) — verwacht partiële fill.
- **Gap down ≤ −0,30%:** long entry op close van eerste M5-bar — verwacht partiële fill.
- Geen trade als |gap| < 0,30%; max 1 trade per symbool per dag.

**Stop:** 1,5 × ATR14 (dag; gebaseerd op vorige 14 sessie-OHLC's). Stop dient als risicobegrenzer bij gap-verlenging.

**Exit:** flat op 11:00 ET (17:00 CET), d.w.z. na ≈ 90 min. Houdduur ≈ 90 min; swap = 0 (intradag-vlak).

**Kosten (FTMO-cfd):**
- US500cash rondreis: ≈ 0,70 bp; US100cash: ≈ 0,60 bp. Gewogen gemiddelde ≈ 0,65 bp.
- Swap = 0 (intradag).
- Kostenpoort-drempel: mean bruto ≥ 3 × 0,65 = **1,95 bp** (pooled, train 2021–2023).

---

## 2. Varianten

Geen varianten; één bevroren regel. Drempel 0,30% vooraf economisch gemotiveerd (kleinere gaps = ruis; grotere = trends). Geen post-hoc aanpassing.

---

## 3. Instrumenten en data

- FTMO-M5 `data/m5gz/US500cash.csv.gz` en `US100cash.csv.gz`, 2021–2026.
- Dag-ATR14 uit sessie-OHLC.
- Kosten: `COSTS_FTMO.csv` (main).
- **Geen 2025-data** voor kostenpoort of beslisregel.

---

## 4. Train/test en beslisregel

- **Train:** 2021-01-01 … 2023-12-31.
- **Test:** 2024-01-01 … 2024-12-31 (plafond ≤ 2024-12-31).
- **Reserve:** 2025-01-01 → **ONAANGERAAKT** (D-084/D-091.5).
- **Beslisregel (vooraf):**
  - Kostenpoort (gratis): pooled mean bruto ≥ 1,95 bp op train → anders **STOP, geen trial**.
  - Kostenpoort PASS: dag-geclusterd t (Newey-West, L=5) ≥ 2,0 (train) **en** test-t ≥ 1,5 **en** FTMO-EV ≥ €100/poging → **bevestigd**.
  - t < 1 of netto ≤ 0 → **verworpen** (trial +1).
- **DSR:** TRIAL_COUNT + 1 na kostenpoort-PASS.
- **Verwachte N:** ≈ 60–100 gap-dagen/jaar × 3 jaar × 2 symbolen = ≈ 360–600 trades (filter ≥ 0,30%).

---

## 5. Faalrisico's

1. Gap-fill effect is al sterk gepubliceerd (Berkman et al. 2012, e.v.) → in-sample overlap 2021–2023.
2. Na-uren-news gaps zijn groter en reverteren minder (fat gaps → trend continuation) → ATR-stop dekt worst case.
3. 2022-type volatiliteitsregime: grote gaps reverteren wél; 2024 laag-vol: weinig signals.
4. GS01 + dit zijn tegengesteld op dezelfde data → uitkomsten zijn anti-gecorreleerd (rapporteer correlatie).
