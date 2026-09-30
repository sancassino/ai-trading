# PREREG_FTMO_B1 — TSMOM-mix op FX (C05-FX) — FTMO-EV

**Status:** Pre-registratie 2026-09-30 22:08 Europe/Amsterdam (poort-amend 22:15: signed mean, NEXT_STEPS v38), branch `claude/trusting-faraday-34tsmg`.  
**Uitkomst (Uitvoerder-2, `18c7996`, 22:27 CEST):** **FORMEEL GESTOPT** — kostenpoort TRAIN FAIL (signed mean bruto −16,94 bp vs drempel 36,05 bp). Geen herstart; **geen nieuwe overnight maand-sleeves** (NEXT_STEPS v39/v41).  
**Auteur:** Strateeg (Grok). Resultaten pas ná freeze-SHA; gate-run landde op `claude/uitvoerder2-r`.  
**Tier:** B1 (STRATEGIE_CATALOGUS §9). Post-A4 prio (NEXT_STEPS v37 / Manager `beb2a3b`).  
**Relatie:** C05 uit `PREREG_CAT1.md`, **alleen** op FTMO-FX-majors (geen indices/goud). **≠ B2/C12** (carry-primary + trendfilter).  
**Venster:** zelfde freeze als A4/A5 CTO-deblokker — train 2021–2023, test 2024, reserve 2025→ ONAANGERAAKT.

---

## 1. Bevroren regel (exact)

**Idee (Hurst–Ooi–Pedersen TSMOM-mix):** multi-horizon tijdreeksmomentum diversifieert look-ahead-ruis; op FX is overnight swap ≈ renteverschil/carry → long/short kan structureel goedkoper dan index-long (A4 faalde op swap-drag).

**Universe (vooraf vast — U12-FX zonder NZDUSD):**  
`EURUSD`, `GBPUSD`, `USDJPY`, `AUDUSD`, `USDCAD`, `USDCHF`.  
NZDUSD **uit** (rondreis 1,85 bp in `COSTS_FTMO.csv`; CAT1-precedent). Alle zes staan in `SymbolList_FTMO.csv`.

**Signaal (identiek C05, maandeinde):**
- Per paar: teken van 21d-, 63d- en 252d-slot/slot-rendement; positie_raw = gemiddelde van de drie tekens ∈ {−1, −⅔, −⅓, 0, ⅓, ⅔, 1}.
- Gewicht = positie_raw × (0,10 / σ60), σ60 = annualiserede vol uit 60 dagreturns; **cap |gewicht| ≤ 3**.
- Herweging: **laatste handelsdag van de kalendermaand** (close→close tot volgende herweging).
- Equal-risk over de 6 paren: elk paar krijgt 1/6 van het portefeuille-risicobudget vóór de FTMO-schaal (§3).

**Vehikel:** FTMO FX-CFD. Geen future/ETF.

**Kosten (FTMO-cfd, gemeten — niet inventeren):**
- Rondreis bij herweging: `COSTS_FTMO.csv` `roundtrip_intraday_bp` (S0, 2026-09-30).
- Swap elke kalendernacht long/short apart; **vrijdag → maandag = 3×** nacht.
- +50% swap-gevoeligheid verplicht (tijdvariabele swaps; RUNLOG).

| Pair | RT bp | swap_long bp/nacht | swap_short bp/nacht |
|------|------:|-------------------:|--------------------:|
| EURUSD | 0,63 | 1,13 | −0,14 |
| GBPUSD | 0,70 | 0,46 | 0,30 |
| USDJPY | 0,78 | −0,37 | 1,58 |
| AUDUSD | 1,22 | 0,45 | 0,87 |
| USDCAD | 0,80 | −0,09 | 0,98 |
| USDCHF | 1,01 | −0,39 | 2,17 |

Bron: `COSTS_FTMO.csv`. Annualized cross-check: `data/swap_specs_fx.csv` (informatief; trial gebruikt bp/nacht-tabel hierboven).

**Kosten-poort (vóór trial telt — gratis op train; NEXT_STEPS v38 / Strateeg-2):**  
**Getekend gemiddelde** maand-bruto (niet mediaan |maand-bruto|) over pair-maanden op train ≥ **3×** gemiddelde (rondreis + swap×nachten voor de genomen kant) over diezelfde pair-maanden.  
Hold ≈ 20–23 kalendernachten per maand. Mediaan |bruto| blijft informatief. Indien poort FAIL → **STOP**, append TRIALS als stop:kostenpoort, geen verdere analyse.

---

## 2. Data

- **Primair (formele trial):** `data/daily/FX_EURUSD.csv` … `FX_USDCHF.csv` (FRED-noon proxies in repo) + kostenmodel §1.  
- **Gevoeligheid (geen tweede trial):** waar FTMO D1-closes bestaan, herhaal netto-reeks informatief.  
- Geen M5 nodig (maand-omloop). A5/S2-M5-kandidaten blijven geparkeerd.

---

## 3. Sizing en FTMO-EV

- Startgewicht zoals C05 (10%/σ60, cap 3), daarna **één globale schaalfactor** zodat op train de **p95 dagverlies ≤ 2%** van account (€80k) — bindend voor FTMO-EV (D-016/D-085).  
- Maatstaf: `engine/ftmo.py` `ftmo_ev()` op de dagelijkse netto-equityreeks (cfd-kosten in).  
- Rapporteer: per-pair contribution + gecombineerde portefeuille.

---

## 4. Train/test en beslisregel

- **Train:** 2021-01-01 … 2023-12-31  
- **Test:** 2024-01-01 … 2024-12-31 (plafond ≤ 2024-12-31)  
- **Reserve:** 2025-01-01 → **ONAANGERAAKT** (D-084; geen CEO-vrijgave)  
- **Beslisregel (vooraf, gelijk A4-vorm):**
  - Netto dag-geclusterd t (Newey-West, train) ≥ 2,5 **EN** test-t ≥ 1,5 **EN** FTMO-EV_netto ≥ €150/poging → door naar shortlist  
  - t < 1 of netto ≤ 0 → verworpen  
  - Daartussen → onbeslist (niet opschalen)  
- Kosten-poort eerst.  
- **DSR:** TRIAL_COUNT + 1 bij openen formele trial (na poort PASS).  
- **≤ 1 variant** in dit PREREG (geen second lookback-set).

---

## 5. Afgrenzing B2 / C12

| | B1 (dit) | B2 / C12 |
|--|----------|----------|
| Primair signaal | TSMOM-mix tekens 1/3/12m | Carry (rente/swap) + trendfilter |
| Positie zonder trend | 0 (flat als alle horizons 0) | Carry mag lonen zonder trend |
| Trial-familie | apart | apart; niet combineren in één PREREG |

---

## 6. Faalrisico's (vooraf)

1. Maand-omloop + swap over ~22 nachten ≈ 10–25 bp/maand drag → poort kan FAIL zoals A4.  
2. FRED-noon ≠ FTMO-executie (timing/spread).  
3. N maanden train ≈ 36 × 6 pairs — power voor t ≥ 2,5 is krap; dag-cluster helpt.  
4. Correlatie tussen USD-pairs → effectieve N lager.

---

## 7. Uitvoerder-checklist

1. Checkout deze PREREG-SHA.  
2. Bouw maandelijkse posities §1 op train; pas kosten toe; **kostenpoort**.  
3. Bij PASS: formele trial + TRIALS-append + `ftmo_ev()`; bij FAIL: stop + TRIALS stop-regel.  
4. Geen 2025-data. Geen parameterwijziging na zien.

---
**Bevroren:** 2026-09-30 22:08 CEST — post-A4 prio B1; poort-clarificatie 22:15 CEST (signed mean, v38).  
**Auteur:** Strateeg (`claude/trusting-faraday-34tsmg`)
