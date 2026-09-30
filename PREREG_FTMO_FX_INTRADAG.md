# PREREG_FTMO_FX_INTRADAG — FX Intradag London-Open ORB (A5, FTMO-EV variant)

**Status:** Pre-registratie 2026-09-30 21:55 Europe/Amsterdam, branch `claude/trusting-faraday-34tsmg`.  
**Auteur:** Strateeg (Claude). **Geen resultaten vóór deze commit.**  
**Relatie:** A5-slot in catalogus §9; eerder getest als U3 (London-open ORB FX) — kostenpoort gefaald op FTMO-spread. Dit PREREG definieert de bevroren regel voor eventuele hertest bij lagere kostenramingen of smallere spread-majors. **Distinct van Grok GS02** (Asian-range fade) en distinct van U3 (eerder gefaald op kostenpoort, niet als formele trial geteld).

**⚠ KOSTEN-POORT EERST:** U3 heeft eerder de kostenpoort niet gehaald op FX-majors bij London-open. Dit PREREG bevat de bevroren regel; de poort-check (gratis) moet worden uitgevoerd vóór een formele trial telt. Als de poort opnieuw faalt → STOP, geen trial.

---

## 1. Bevroren regel (exact)

**Idee:** London-open (08:00 CET / 07:00 UTC) veroorzaakt liquiditeits- en order-onbalans via Europese institutionele flows en wisselwerking met overnight Asian-range. Momentum in de eerste 30 min geeft richting voor de rest van de ochtend. Structurele bron: market-microstructure, niet patroon-mining.

**Universe (vooraf vast):** EURUSD, GBPUSD, USDJPY, USDCHF. (AUD/NZD/CAD uitgesloten op hogere kosten.)

**Opening range (OR):** hoog/laag van 08:00–08:30 CET (6× M5), vastgezet op 08:30.

**Entry:**
- **Long** bij eerste M5-slotkoers > OR_high ná 08:30, of bij breakout van OR_high op dezelfde M5-bar (gebruik conservatief: dicht boven OR_high).
- **Short** bij eerste M5-slotkoers < OR_low ná 08:30.
- One-cancels-other (OCO): zodra één kant geactiveerd, andere geannuleerd.
- Max 1 trade per symbool per dag; geen herentry.

**Stop:** OR-tegenoverliggende kant (stop = OR_low voor long, OR_high voor short).

**Exit:** flat op 12:00 CET (niet sessie-einde: swap-vrij, kort houdvenster). Geen trailing.

**Filter (optioneel, variant b):** alleen handelen als spread op signaalmoment < 1,5× mediaan-spread van vorige 20 handelsdagen voor dat symbool+tijdstip (spread-filter om slechte liquiditeitsperiodes te vermijden). Variante (a) = zonder filter.

**Kosten (FTMO-cfd FX):**
- EURUSD rondreis ≈ 0,6–0,8 bp; GBPUSD ≈ 0,7–0,9 bp; USDJPY ≈ 0,7–1,0 bp (S0-tabel).
- Swap: houdduur ≤ 4 uur intradag → swap = 0.
- Bruto nodig ≥ 3× kosten ≈ ≥ 2,1–3,0 bp → **poort: mediaan bruto per trade ≥ 2,1 bp** (EURUSD-standaard).

**Kostenpoort (vóór trial):** mediaan netto-bruto ≥ 3× rondreis op train → anders STOP.

---

## 2. Varianten (≤ 2, vooraf vastgelegd)

- **(a) Standaard:** bovenstaande regel zonder spread-filter.
- **(b) Spread-filter:** bovenstaande + spread-filter (mediaan × 1,5); iets minder trades, betere uitvoering. Telt als aparte variant maar **niet als aparte trial** (één familie).

Familie = 1 trial (twee varianten samen; rapporteer beide, beslis op (a)).

---

## 3. Instrumenten en data

- FTMO-M5 FX: data/m5/ — EURUSD aanwezig; GBPUSD/USDJPY/USDCHF exporteren (D-086-taak Uitvoerder-1).
- Periode: train 2021-01-01 … 2023-12-31; test 2024-01-01 … 2024-12-31; reserve 2025-01-01 → ONAANGERAAKT (plafond ≤ 2024-12-31).
- Sessietijden CET/CEST DST-bewust.

---

## 4. FTMO-EV specificatie

**Maatstaf:** `engine/ftmo.py` `ftmo_ev()` op dagelijkse equity-reeks van FX-intradag-regel.

**Verwachting:** FX ORB heeft structureel lagere bruto per trade dan index ORB (FX efficiënter). U3 faalde al op kostenpoort. Kans op bevestiging ≈ 5–10%.

---

## 5. Train/test en beslisregel

- **Train:** 2021-01-01 … 2023-12-31 (bevroren 2021–2023).
- **Test:** 2024-01-01 … 2024-12-31 (volledig kalenderjaar 2024; discovery/test-plafond ≤ 2024-12-31).
- **Reserve:** 2025-01-01 → **ONAANGERAAKT / UNTOUCHED** (niet openen, niet gebruiken; D-084 reserve geschorst).
- **Resolutie D-030 vs D-084:** oudere venstertaal (test 2024–2026) conflicteert met D-084 (reserve geschorst). Dit amendement krimpt het testvenster tot 2024 zodat de 2025-reserve bevroren blijft. **Geen CEO 2025-vrijgave nodig** voor dit amendement.
- **Beslisregel (vooraf):**
  - Kosten-poort haalt → netto dag-geclusterd t (Newey-West) ≥ 2,5 (train) EN test-t ≥ 1,5 EN FTMO-EV ≥ €100/poging → **bevestigd**
  - Kostenpoort faalt → **verworpen direct** (geen trial toegevoegd aan TRIAL_COUNT)
  - Poort haalt maar t < 1 of netto ≤ 0 → **verworpen** (trial +1)
- **Correlatie:** rapporteer correlatie met ORB-index (A1) dagelijkse P&L; hoge correlatie (> 0,6) → geen nieuwe sleeve, alleen portefeuille-impact.
- **DSR:** TRIAL_COUNT + 1 bij formele trial.

---

## 6. Overlap met andere PREREG's

- **Grok GS02 (Asian-range fade):** DISTINCT — GS02 handelt de fade van de Asian-range, dit PREREG handelt London-open breakout; verschillende mechanisme (momentum vs fade) en tijdvenster.
- **U3 (eerder gefaald):** U3 was dezelfde family maar werd gestopt op kostenpoort zonder formele trial. Dit is het PREREG voor een hertest indien data/spreads gunstiger zijn. Indien opnieuw gefaald → niet opnieuw openen.
- **GS01 (gap-aligned index ORB):** DISTINCT — GS01 is index, dit is FX.


---

## CTO amend note (2026-09-30 22:05 Europe/Amsterdam)

CTO default action under **D-084**: test window frozen to **2024-01-01 … 2024-12-31**; train **2021-01-01 … 2023-12-31**; reserve **2025-01-01 →** sealed until BESLUITEN release. Documented closed in `VRAGEN_CTO.md`. Source freeze also on `claude/trusting-faraday-34tsmg` @ `5fc3fb9`. No trial results in this amend.
