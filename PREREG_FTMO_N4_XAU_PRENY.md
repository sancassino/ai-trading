# PREREG_FTMO_N4 — XAU Pre-NY Range Breakout (FTMO-EV variant)

**Status:** Pre-registratie 2026-10-01 01:30 Europe/Amsterdam, branch `claude/trusting-faraday-34tsmg`.  
**Auteur:** Strateeg (Claude). **Geen resultaten vóór deze commit.**  
**Tier:** D-091.3 (nieuw, non-clone); screen top-10 (XAU RT-ratio gunstig; `results/screen_cost_vol.csv`).  
**Relatie:** Distinct van XAU_AM_FADE (fade van London-ochtend, ander tijdvenster + tegengestelde richting), A1 ORB (indices, ochtend-session), GS02 (Asian-range FX-fade). Nieuw mechanisme: pre-NY range-compressie + US institutionele goudorders.

---

## 1. Bevroren regel (exact)

**Idee (structurele bron):** In de periode 13:00–15:00 CET (07:00–09:00 ET) comprimeert de XAU-markt: Aziatische sessiespelers sluiten posities, Europese sessie windt af, en US spelers zijn nog niet actief. Bij NY open (15:00 CET / 09:00 ET) komen US institutionele goudorders op de markt: ETF-rebalancers, hedgefondsen met macro-posities, en commodity-handelaars. Dit veroorzaakt een directionale impuls die de gecomprimeerde range breekt. Mechanisme: liquiditeits-vacuüm + institutionele orderflow, niet patroon-mining.

**Universe (vooraf vast):** `XAUUSDcash` (goud, FTMO-cfd).

**Pre-NY range (PNR):** hoog/laag van bars 13:00–14:55 CET (gebaseerd op M5; 24 bars = 2 uur), vastgezet op 14:55 CET.

**Entry (op NY open):**
- **Long** bij eerste M5-slotkoers > PNR_high ná 15:00 CET, of bij breakout van PNR_high op dezelfde M5-bar.
- **Short** bij eerste M5-slotkoers < PNR_low ná 15:00 CET.
- OCO: zodra één kant geactiveerd, andere geannuleerd.
- Max 1 trade per dag; geen herentry.
- **Minimale PNR-breedte:** PNR_high − PNR_low ≥ 0,10% van PNR_midpoint. Als de range te smal is (< 0,10%) → geen trade die dag (vermijdt nep-breakouts in ultra-platte periodes).

**Stop:** PNR-tegenoverliggende kant (stop = PNR_low voor long, PNR_high voor short).

**Exit:** flat op 17:30 CET (15:30 ET, 2,5 uur na NY open). Houdduur ≈ 2,5 uur; swap = 0.

**Kosten (FTMO-cfd):**
- XAUUSDcash rondreis: spread + commissie ≈ 0,83 bp (COSTS_FTMO.csv, S0-meting).
- Swap = 0 (intradag).
- Kostenpoort-drempel: mean bruto ≥ 3 × 0,83 = **2,49 bp** (train 2021–2023).

---

## 2. Varianten

Geen varianten; één bevroren regel. De minimale range-breedte 0,10% is vooraf vastgelegd op basis van economische logica (te smalle range = geen compressie-effect). Geen post-hoc aanpassing.

---

## 3. Instrumenten en data

- FTMO-M5 `data/m5gz/XAUUSDcash.csv.gz` (of `data/m5/`), 2021–2026.
- Kosten: `COSTS_FTMO.csv` (main).
- **Geen 2025-data** voor kostenpoort of beslisregel.

---

## 4. Train/test en beslisregel

- **Train:** 2021-01-01 … 2023-12-31.
- **Test:** 2024-01-01 … 2024-12-31 (plafond ≤ 2024-12-31).
- **Reserve:** 2025-01-01 → **ONAANGERAAKT** (D-084/D-091.5).
- **Beslisregel (vooraf):**
  - Kostenpoort (gratis): mean bruto ≥ 2,49 bp op train → anders **STOP, geen trial**.
  - Kostenpoort PASS: dag-geclusterd t (Newey-West, L=5) ≥ 2,0 (train) **en** test-t ≥ 1,5 **en** FTMO-EV ≥ €100/poging → **bevestigd**.
  - t < 1 of netto ≤ 0 → **verworpen** (trial +1).
- **DSR:** TRIAL_COUNT + 1 na kostenpoort-PASS.
- **Verwachte N:** ≈ 200–220 handelsdagen/jaar × ~80% filter (PNR-breedte ≥ 0,10%) × 3 jaar = ≈ 480–530 trades.

---

## 5. Faalrisico's

1. XAU_AM_FADE-gate PASS (18,7 bp bruto) suggereert dat XAU ochtend-fade-edge bestaat — pre-NY breakout is een ander (en tegengesteld) mechanisme; kan interfereren.
2. Breedte-filter 0,10% is economisch gemotiveerd maar kan te smal of te ruim zijn voor het regime.
3. XAU/USD gecorreleerd met DXY-beweging na NY open — deels FX-risico, niet puur goud-specifiek.
4. N per jaar ≈ 160–175 → power train-t ≥ 2,0 vereist SR ≈ 0,5 train (haalbaar bij 2–3× kosten).
