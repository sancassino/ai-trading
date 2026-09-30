# PREREG_FTMO_C17 — FOMC-cyclus D1 op index-CFD (FTMO-EV variant)

**Status:** Pre-registratie 2026-09-30 21:55 Europe/Amsterdam, branch `claude/trusting-faraday-34tsmg`.  
**Auteur:** Strateeg (Claude). **Geen resultaten vóór deze commit.**  
**Relatie:** C17 FOMC-cyclus eerder getest via ETF-vehikel (t 2,85, SR 0,52); dit herhaalt de bevroren C17-regel op cfd-vehikel met FTMO-EV als maatstaf. **Geen nieuwe hypothese; hertest op FTMO-instrument.**

---

## 1. Bevroren regel (exact — identiek aan C17-definitie in catalogus)

**Idee (Cieslak–Morse–Vissing-Jorgensen 2019):** aandelenrendementen zijn geconcentreerd in de even weken van de 8-weekse FOMC-vergadercyclus (week 0, 2, 4, 6 = "FOMC-weken"); correcties in oneven weken. Mechanisme: Fed-communicatie en informele guidance lekken via verwachte monetaire-beleidswijzigingen. Structurele bron, geen patroon-mining.

**Universe (vooraf vast):** `US500cash`, `US100cash`, `GER40cash`.

**Signaal:**
- Bereken FOMC-cyclus-week (0 t/m 7) per kalenderdag: week 0 = kalenderweek van de vorige FOMC-vergadering (of eerste dag na), doorlopend per 8 weken.
- **Long** op close van dag vóór even week (week 0, 2, 4, 6 start), exit op close van laatste dag van die even week (5 werkdagen houden).
- **Geen positie** in oneven weken (1, 3, 5, 7).
- One trade per symbool per cyclus; geen intraday-management.

**Vehikel:** FTMO index-CFD (US500cash, US100cash, GER40cash). GEEN ETF.

**Kosten (FTMO-cfd):**
- Rondreis spread + commissie per symbool (uit COSTS_FTMO.csv / S0-meting).
- Swap per nacht: uit dagelijkse FTMO-snapshot (data/ftmo_specs/); variabel — conservatief: +50%-gevoeligheid.
- Houdduur ≈ 5 nachten per trade → swap-impact materieel (US500 long swap ≈ −5 tot −7%/jr = ≈ −1,5 tot −2 bp/nacht × 5 ≈ −8 tot −10 bp/trade).

**Kosten-poort (vóór trial telt):** netto mediaan-bruto per trade ≥ 3× rondreis-kosten inclusief swap (≈ ≥ 15 bp bij huidige kostenscenario). Indien niet gehaald → **STOP, geen trial**.

---

## 2. Instrumenten en data

- FTMO-M5 (data/m5/) voor US500cash, US100cash, GER40cash — discovery/test-plafond ≤ 2024-12-31 (reserve 2025-01→ ONAANGERAAKT; D-084).
- D1 afsluiting via `data/daily/` of close van laatste M5-bar van de sessie.
- FOMC-vergaderdata: publiek beschikbaar via federalreserve.gov kalender; in `data/fomc_dates.csv` (of aanmaken).

---

## 3. FTMO-EV specificatie

**Maatstaf:** FTMO-EV = P(fase1_pass) × P(fase2_pass|fase1) × P(funded_12m) × E[uitbetaling/mnd] − fee/pogingen.

**Berekening:** `engine/ftmo.py` (`ftmo_ev()`) op dagelijkse equity-reeks van C17-regel op cfd-vehikel.

**Verwachting:** C17 haalt ETF-vehikel t 2,85 / SR 0,52. Met cfd-swap (houdduur ≈ 5 nachten) verwacht netto SR ≈ 0,3–0,5. FTMO-EV sterk afhankelijk van P(fase1_pass) die samenhangt met dagverlies-dip-profiel (ORB is positief scheef; C17 is D1-strategie met hogere per-trade-winstvariatie).

---

## 4. Train/test en beslisregel

- **Train:** 2021-01-01 … 2023-12-31 (bevroren 2021–2023; 3 jaar, ≈ 19 FOMC-cycli × 3 symbolen = ≈ 57 entries).
- **Test:** 2024-01-01 … 2024-12-31 (volledig kalenderjaar 2024; discovery/test-plafond ≤ 2024-12-31).
- **Reserve:** 2025-01-01 → **ONAANGERAAKT / UNTOUCHED** (niet openen, niet gebruiken; D-084 reserve geschorst).
- **Resolutie D-030 vs D-084:** oudere venstertaal (test doorlopend voorbij 2024, D-030-achtig) conflicteert met D-084 (reserve geschorst). Dit amendement krimpt het testvenster tot 2024 zodat de 2025-reserve bevroren blijft. **Geen CEO 2025-vrijgave nodig** voor dit amendement.
- **Beslisregel (vooraf):**
  - Netto dag-geclusterd t (Newey-West, train) ≥ 2,5 EN test-t ≥ 1,5 EN FTMO-EV ≥ €150/poging → **bevestigd, opnemen in A-tier**
  - t < 1 of netto ≤ 0 → **verworpen**
  - Daartussen → onbeslist (niet opschalen)
- **Kosten-poort eerst** (gratis, geen trial): als netto bruto < 3× kosten op train → stop, telt als trial maar geen verdere analyse.
- **DSR:** TRIAL_COUNT + 1 (huidige teller + 1 na openen dit PREREG).
- **FTMO-mechanica:** per symbool afzonderlijk + gecombineerd rapporteren.

---

## 5. Verwachte uitkomst en faalrisico's

- **Kans op bevestiging:** ≈ 15–20% (C17 ETF-t 2,85 is net onder lat; swap maakt het CFD-resultaat zwakker; power laag door N ≈ 57/39).
- **Faalrisico's:**
  1. Swap ≈ −8 tot −10 bp/trade doodt de edge (bruto ≈ 5–10 bp op indices → netto ≈ 0).
  2. FOMC-cyclus effect is 2001–2018 (paper), 2021–26 in steekproef → in-sample.
  3. Kosten-poort: kans groot dat het al op de poort valt.
  4. N te klein voor dag-geclusterde t ≥ 2,5.


---

## CTO amend note (2026-09-30 22:05 Europe/Amsterdam)

CTO default action under **D-084**: test window frozen to **2024-01-01 … 2024-12-31**; train **2021-01-01 … 2023-12-31**; reserve **2025-01-01 →** sealed until BESLUITEN release. Documented closed in `VRAGEN_CTO.md`. Source freeze also on `claude/trusting-faraday-34tsmg` @ `5fc3fb9`. No trial results in this amend.
