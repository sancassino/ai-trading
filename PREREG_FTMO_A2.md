# PREREG_FTMO_A2 — Stocks-in-Play ORB earnings (FASE 3 heropening) — FTMO-EV

**Status:** Pre-registratie BEVROREN 2026-09-30 22:15 Europe/Amsterdam, branch `claude/trusting-faraday-34tsmg`.  
**Auteur:** Strateeg (Grok). **Geen resultaten vóór deze commit.**  
**Tier:** A2 (STRATEGIE_CATALOGUS §9). Post-A4 prio 2 (NEXT_STEPS v38: B1→A2 parallel).  
**Relatie:** heropening van `PREREG_S2.md` die stopte op **mediaan**-kostenpoort. Dit is **1 nieuwe trial-familie** onder D-012 (poort op **gemiddelde** bruto) + dag-geclusterde t + FTMO-EV — niet dezelfde S2-trial opnieuw labelen.  
**Venster:** train 2021–2023, test 2024, reserve 2025→ ONAANGERAAKT (D-084; CTO-deblokker).

---

## 1. Bevroren regel (exact)

**Idee (Zarattini–Barbon–Aziz, SFI RP 24-98 / SSRN 4729284):** op earnings-dagen is de opening range een information-driven imbalance; handelen **alleen in OR-richting** (paper) vangt continuation met vaste stop en EOD-exit. Structurele catalyst (earnings), geen patroon-mining. Intraday-vlak → swap = 0.

**Universe (vooraf vast):** `universe_us41.txt` (41 US-namen; zelfde als S2).  
Alle 41 staan in `COSTS_FTMO_alle.csv` (D-086, main @ fetch-tijd).

**Opening range (OR):** eerste 5-min kaars van de NY-handelsdatum op FTMO-M5 (S2/Q2-fix: eerste bar = OR, ook als FTMO pas om 09:35 opent).

**Entry (alleen OR-richting — paper):**
- OR slot > open → buy-stop op OR_high (long only die kant).
- OR slot < open → sell-stop op OR_low (short only die kant).
- Doji (slot = open) → geen trade.
- Max 1 trade per symbool per earnings-eventdag; geen herentry; max 5 gelijktijdige posities.

**Stop (primaire variant — enige bindende):** paper **(b)** — stop = 10% van ATR14 (dag) vanaf instapprijs.  
**Exit:** sessie-sluiting (EOD) of stop — **geen overnight** (swap = 0).

**Earnings-filter:** events uit `earnings.csv`; tijd ≤ 09:30 ET → zelfde handelsdag; anders volgende handelsdag. Alleen die dagen zijn tradebaar.

**Sizing:** risico 1% account-equity per trade; hefboom ≤ 4× (paper/S2).

**Geen tweede variant in deze trial-familie.** (Oude S2 (a)/(c)/(d) niet meegenomen — ≤ 1 variant.)

---

## 2. Kosten (gemeten — niet inventeren)

Bron: `COSTS_FTMO_alle.csv` (D-086; comment: aandelen mediaan onzeker bij hoge `aandeel_spread0`; Q2 mat ≈ 2,9 bp historisch).

**Per-trade rondreis** = `rondreis_bp` van dat symbool (spread_med + 2× commissie 0,20 bp/kant).  
US41 snapshot (alle 41 gevonden; geen missings):

| Samenvatting US41 | bp |
|------------------|---:|
| Mediaan rondreis | 6,41 |
| Gemiddelde rondreis | 8,99 |
| Min (MSFT) | 2,48 |
| Max (GME) | 40,54 |

**3× mediaan-RT ≈ 19,23 bp; 3× mean-RT ≈ 26,98 bp** — informatief. Bindende poort gebruikt **trade-gewogen** kosten (§3).

+50% spread-stress verplicht (rapportage).  
Hoge-RT-namen (o.a. GME, PFE, T, NKE, BAC) blijven in universum (geen post-hoc schrappen).

---

## 3. Kosten-poort (vóór trial telt — D-012)

Op **train 2021–2023**:
1. Bereken per trade bruto bp (vóór kosten).
2. **Poort:** **gemiddelde** bruto over trades ≥ **3×** gemiddelde rondreis van diezelfde trades (trade-gewogen mean RT).  
3. Secundair (informatief, geen fail): mediaan bruto; gemiddelde bruto zonder top-5% winnende trades > 0 (D-012 staartcheck).  
4. +50% spread: zelfde gemiddelde-poort als gevoeligheid.

**FAIL → STOP**, append TRIALS als `stop:kostenpoort`, **geen** formele trial-telling / geen FTMO-EV.  
**PASS →** TRIAL_COUNT + 1, verder §5.

*(Verschil met oude S2: mediaan-poort 8,7 bp faalde per definitie op positief-scheve stop-profielen — D-012.)*

---

## 4. Data

- FTMO-M5 aandelen voor US41 (`data/m5/` of VM-export).  
- `earnings.csv` (repo; Yahoo via yfinance, opgehaald 2026-09-30).  
- Dag-ATR14 uit sessie-OHLC (14 vorige dagen), zoals S2.  
- Kosten: `COSTS_FTMO_alle.csv` (main/D-086).  
- **Geen 2025-bars** voor poort of beslisregel.

---

## 5. Train/test en beslisregel

- **Train:** 2021-01-01 … 2023-12-31  
- **Test:** 2024-01-01 … 2024-12-31 (plafond ≤ 2024-12-31)  
- **Reserve:** 2025-01-01 → **ONAANGERAAKT** (D-084)

**Na poort PASS:**
1. Netto dag-geclusterde t (Newey–West) ≥ **2,0** op train **én** op test 2024.  
2. N ≥ 100 events per helft (train-helften 2021–22 / 2023; test als één blok 2024 met N≥100 of rapporteer power-tekort).  
3. ≥ 4 van 4 kalenderjaren 2021–24 met mean netto > 0 — zo niet: label "onbeslist", niet shortlist.  
4. Scheefheid dag-P&L > 0 of max dagdip ≤ −2% bij 1%-risk / ≤5 concurrent.  
5. **FTMO-EV** via `engine/ftmo.py` ≥ **€80/poging netto** (p95 dagverlies ≤ 2% sizing-bindend; schaal > 4% alleen bovengrens, D-016/D-085).  
6. Correlatie dagreeks met A1/B4a index-ORB: informatief; |ρ| > 0,5 → label "equity-ORB-beta", shortlist alleen bij Δ FTMO-EV > €50 vs A1.

**Verworpen:** poort FAIL; of t < 1 / netto ≤ 0 op train of test.  
**Onbeslist:** tussen t∈[1, 2) of EV < €80 maar t≥2 — niet opschalen.

**DSR:** +1 trial alleen na poort PASS.  
**Verboden:** post-hoc universum-trimmen, OR-lengte wijzigen, earnings-window tunen, tweede stop/exit kiezen na zien.

---

## 6. Afgrenzing

| | Dit (A2) | Oude S2 | A1 / GS01 |
|--|----------|---------|-----------|
| Poort | Gemiddelde bruto ≥ 3× RT (D-012) | Mediaan ≥ 8,7 bp | Index CFD RT |
| Inferentie | Dag-cluster t≥2,0 + FTMO-EV | Trade-t ≥ 3,5 | Index multi-ORB |
| Universum | US41 earnings | Idem | US500/US100/GER40 |
| Swap | 0 (EOD) | 0 | 0 |

≠ Strateeg-2 S2-* (XAU/GER40/USOIL/BTC) — andere instrumenten/vensters.

---

## 7. Faalrisico's (vooraf)

1. Gemeten US41 median RT 6,41 bp ⇒ 3× ≈ 19 bp — poort strenger dan oude 8,7 bp-aanname; FAIL waarschijnlijk.  
2. Hoge `aandeel_spread0` op veel namen → mediaan-spread onzeker (D-086 comment).  
3. Earnings-dekking in `earnings.csv` is recent Yahoo-limit; pre-2024 gaps → N/power-risico (rapporteer coverage per jaar vóór trial).  
4. Correlatie met index-ORB kan hoog zijn op risk-on earnings-dagen.

---

## 8. Uitvoerder-checklist

1. Checkout deze PREREG-SHA.  
2. Coverage-tabel earnings × US41 × jaar 2021–24 (geen P&L).  
3. Kostenpoort train (§3); bij FAIL stop + TRIALS-regel.  
4. Bij PASS: formele trial + `ftmo_ev()`; geen 2025; geen parametertuning.

---
**Bevroren:** 2026-09-30 22:15 CEST — stub → volledige freeze (NEXT_STEPS v38 prio 2).  
**Auteur:** Strateeg (`claude/trusting-faraday-34tsmg`)
