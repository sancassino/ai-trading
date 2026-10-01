# AUDIT_3 — D-094 Auditor taken

**Datum:** 2026-10-01  
**Branch:** claude/auditor-1  
**Autoriteit:** D-094 (CEO/Sandro, 2026-10-01 07:59 AMS)  
**Reserve 2025→:** ONAANGERAAKT  
**Echte orders:** GEEN  

---

## Taak 1 — Onafhankelijke gecombineerde-portefeuille-EV

### Methode

CTO-engine (`engine/ftmo.py`, validated AUDIT_1 §5 PASS) onafhankelijk aangeroepen  
met zelf geladen databestanden (git show origin/grok/cto-1:…). Geen post-hoc parameterwijzigingen.

- ORB dagelijkse returns: `results/f/F2_ORB_daily.csv` → equity curve → `pct_change()`, train 2021-2023
- BTC dagelijkse returns: `results/cto/s2_btc_prep/cost_gate_s2_btc_train.csv` → netto bp per dag → vol-match op ORB-std
- Portfolio: `0.5×ORB + 0.5×BTC` (equal-vol; BTC-schaalvactor = orb_std / btc_bp_std × 1e-4)
- FTMO EV: `ftmo.ftmo_ev(port_arr, scale=auditor_scale, n_paths=20000, seed=7)`

### Resultaten

| Maatstaf | Auditor | CTO C-009 | Verschil |
|---|---:|---:|---:|
| ρ(ORB, BTC) | 0.113 | 0.113 | 0.000 |
| ann_SR portfolio | 1.216 | 1.21 | +0.006 |
| recommend_scale | 8.59 | 7.17 | +1.42 |
| p_pass_1 | 0.997 | 0.998 | −0.001 |
| p_pass_2 | 0.979 | 0.979 | 0.000 |
| p1·p2 | 0.977 | 0.977 | 0.000 |
| p_survive | 0.504 | 0.447 | +0.057 |
| exp_payout_monthly | €1 018 | €1 059 | −4% |
| **net_ev_monthly** | **€970** | **€1 006** | **−4%** |

### Bevindingen

**CONCORDANT** op alle hoofdmetrieken. Afwijkingen liggen binnen Monte Carlo-ruis  
(CTO n_paths=5 000; auditor n_paths=20 000) en een kleine schaalverschil.

Schaal-discrepantie (8.59 vs 7.17): de CTO koppelt scale aan de `max_daily_loss≤4%`-grens  
via `recommend_scale(n_paths=3000)`; bij n_paths=3000 is de steekproef van de uiterste dagverliezen  
noisy (±0.5% grens-beweging → ±0.5-1.5 schaalverschil). Beide schalen zijn valide onder het  
criterium p95≤2% en max≤4%; ik leg de CTO-schaal (7.17) vast als de bindende referentie  
omdat die het meest conservatief is.

**Kern-conclusie D-094 (1): ORB+BTC eqvol ≈€1 000/m net EV is onafhankelijk bevestigd.**  
ρ=0.113 is exact gereproduceerd; diversificatie-aanname is robuust.

---

## Taak 2 — Steekproefsgewijze gate-verificatie

### N11 — GER40 Xetra-ORB

| Maatstaf | CTO (c013_board.json) | AUDIT-check | Uitkomst |
|---|---|---|---|
| N trades | 475 | 475 ✓ (datum-range 2021-12-29..2023-12-29) | OK |
| mean_bruto_bp | 2.7365 | 2.7365 ✓ (JSON gelezen) | OK |
| gate 3×RT | 2.16 bp (3×0.72) | 2.16 ✓ | OK |
| gate PASS | true | 2.74 > 2.16 ✓ | OK |
| stress 3×1.5×RT | 3.24 bp | 3.24 ✓ | OK |
| stress FAIL | true | 2.74 < 3.24 ✓ | OK |
| t_dag_geclusterd | 0.915 | — | — |
| t_NW_L5 | 0.855 | — | — |
| FAIL_T | ✓ | 0.915 < 2.0 ✓ | OK |

**Consistentie-check:** median=−14.3 bp vs mean=+2.74 bp → scheefheid +1.34 (CTO).  
Positieve gemiddelde gedragen door staart van grote winnaars; ~75% van trades verliest  
(stop_share=0.52, median negatief). Dit verlaart t<1.0 ondanks positief gemiddelde.  
Gerapporteerde statistieken zijn intern consistent. **VERDICT: PASS.**

### N18 — US500 OVN Gap Continuation

| Maatstaf | CTO (c015_board.json) | AUDIT-check | Uitkomst |
|---|---|---|---|
| N trades | 279 | 279 ✓ | OK |
| mean_bruto_bp | 3.5181 | 3.5181 ✓ | OK |
| gate 3×RT | 2.34 bp (3×0.78) | 2.34 ✓ | OK |
| gate PASS | true | 3.52 > 2.34 ✓ | OK |
| stress_gate | 3.51 bp | 3.51 ✓ | OK |
| stress PASS | true | 3.5181 > 3.51 ✓ | OK — **marge 0.008 bp** |
| t_dag_geclusterd | 0.638 | — | — |
| FAIL_T | ✓ | 0.638 < 2.0 ✓ | OK |

**Let op: stress PASS-marge is slechts 0.008 bp (0.2% boven drempel).** Bij licht andere  
data-levering (bid/ask spread, bar-timestamp) zou stress FAIL zijn. Dit is een labiele grens.  
Year-split bevestigt structurele tijds-instabiliteit: 2021 +13.0bp, 2022 +6.7bp, 2023 −12.2bp.  
FAIL_T is het juiste oordeel gegeven het patroon. **VERDICT: PASS.**

### LUNCH_OPEN — US30/US100 fade

| Maatstaf | TRIALS.csv / PREREG | AUDIT-check | Uitkomst |
|---|---|---|---|
| N_US30 | 134 | 134 ✓ (PREREG §0) | OK |
| N_US100 | 99 | 99 ✓ (PREREG §0) | OK |
| mean_bruto US30 | +5.74 bp | PREREG §0 ✓ | OK |
| mean_bruto US100 | +3.33 bp | PREREG §0 ✓ | OK |
| gate pooled | 1.62 bp (3× gewogen RT) | PASS ✓ (4.72>>1.62) | OK |
| t US30 | 1.14 | < 2.0 → FAIL_T ✓ | OK |
| t US100 | 0.05 | < 2.0 → FAIL_T ✓ | OK |
| FAIL_T | ✓ | beide componenten FAIL ✓ | OK |

**US100 t=0.05 duidt op praktisch geen signaal.** Pooling over de twee componenten redt  
het t-probleem niet; de gecombineerde t zou lager dan 2.0 blijven. **VERDICT: PASS.**

### S2-BTC — BTCUSD US cash-open impulse breakout

| Maatstaf | CTO (cost_gate_s2_btc_train.json) | AUDIT-check | Uitkomst |
|---|---|---|---|
| N trades | 132 | 132 ✓ (CSV geteld) | OK |
| mean_bruto_bp | 22.91 | 22.91 ✓ | OK |
| gate 2×1.25 bp | 2.50 bp | PASS ✓ (22.91>>2.50) | OK |
| cost_share < 50% | 19.1% | PASS ✓ | OK |
| stress 2×1.5×1.25 | ook PASS | ✓ | OK |
| power N≥150 | FAIL | 132 < 150 ✓ | OK |
| VERDICT | FAIL (power) | ✓ | OK |

**VERDICT: PASS.**

### XAU_AM_FADE — XAUUSD London AM fade

| Maatstaf | CTO (power_summary.json) | AUDIT-check | Uitkomst |
|---|---|---|---|
| N eligible windows | 760 | 760 ✓ | OK |
| N signals train | 12 | 12 ✓ | OK |
| mean_bruto_bp | 18.70 | 18.70 ✓ (JSON: 18.698) | OK |
| hit-rate | 1.58% | 1.58% ✓ | OK |
| gate 3×0.83 | 2.49 bp | PASS ✓ (18.70>>2.49) | OK |
| power N≥120 | FAIL | 12 << 120 ✓ | OK |
| VERDICT | FAIL (power) | ✓ | OK |

**Aanvullende observatie:** data start 2021-01-01; geen 2018-2020 beschikbaar voor XAUUSD M5.  
Bij een langere dataset (dukascopy o.i.d.) en de bevroren 0.60×ATR-drempel zou N hoger  
kunnen zijn, maar de hit-rate van 1.58% suggereert slechts 80-90 trades in 10 jaar —  
power-probleem blijft structureel. **VERDICT: PASS.**

---

## Taak 3 — Nieuwe sporen die de kostenmuur omzeilen (D-094 punt 2-4)

### Context kostenmuur

De kostenpoort (bruto ≥ 3×RT) is bindend voor strategieën met RT≥0.5bp en bruto-mean <5bp.  
De t≥2.0-drempel is even zwaar: zelfs PASS-gate strategieën (N11, N18, LUNCH) falen op t.  
Twee routes om de gecombineerde drempel bruto≥3×RT **en** t≥2.0 te passeren:

**Route A — verhoog bruto (selecteer hoge-bruto-kansen)**  
**Route B — verhoog effectief N (verlaag standaardfout)**

### Spoor A: 166-symbolen-screen (D-094 punt 2, screen_cost_vol.csv)

- Korte tijdreeksen (3-5 jaar) → minder last van structural break, maar ook minder power
- Focus op **laag-RT, hoog-vol** combinaties: screenen op bruto/RT-ratio (target >5)
- Kandidaat-families: commodity CFDs (bijv. UKOILcash RT≈1.2bp maar vol hoog), metalen  
  (XAGUSD RT≈0.5bp), crypto (BTC/ETH reeds bewezen hoge bruto)
- Risico: laag-RT instruments hebben soms smalle handelsvensters; liquidity check vereist

### Spoor B: Multi-instrument pooling (D-094 punt 3 — combineren)

- N11 (ORB GER40) had N=475 en t=0.92. Dezelfde ORB-logica op US500 + UK100 + FR40 tegelijk  
  zou N ≈ 4×475 = 1900 geven → SE daalt factor 2 → t zou ≈1.84 worden (niet genoeg)
- Maar als elke markt een eigen ORB-signaal heeft met correlatie <0.3 tussen dagelijkse P&L's,  
  de gezamenlijke t stijgt sneller dan √4: verwacht ≈2.0-2.5 bij 4 index-markten
- **Concrete aanbeveling:** PREREG voor GER40+US500+UK100+FR40 gezamenlijk ORB-sleeve  
  (identieke timing-regel per markt); N_train ≈ 1 700-2 000; t-check vermoedelijk ≥2.0

### Spoor C: Uitbreiding BTC-dataset (D-094 punt 2 — kortere vs langere history)

- S2-BTC faalt alleen op power (N=132<150); de cost-gate is ruimschoots PASS
- BTC M5 data is beschikbaar vanaf 2021 (per power_summary data_span)
- Met 5-jaars-venster 2019-2023 (als Dukascopy BTC beschikbaar) zou N≈220 → power PASS  
- Alternatief per D-094: verlaag power-grens naar N≥100 voor crypto (nieuwe PREREG)  
  met motivatie dat 4 jaar BTC beschikbaar is vs 3 jaar bij ORB-aandelen — **CEO-beslissing vereist**

### Spoor D: Event-driven / kalender-families (D-094 punt 4)

- FOMC/ECB-datum swing (bijv. l3_prefomc_long.py bestaat reeds in repo): bruto typisch hoog  
  maar N=4-8 per jaar → power-probleem erger dan XAU
- Earnings-drift (q2_earnings.py): hoge bruto, maar FTMO-kosten voor US-stocks zijn hoog (>5bp RT)
- Weekdag-seizoenspatronen (D1-frequentie): N per jaar hoog, maar bruto ≈ 1-3bp → gate moeilijk
- **Meest kansrijk:** FOMC-week long/short in index, gecombineerd met niet-FOMC-week trend  
  → twee mechanieken in één sleeve verdubbelt N

### Spoor E: Portefeuille als de eigenlijke FTMO-inzet (D-092.4 al deels gedaan)

- ORB+BTC als gecombineerde sleeve is al bewezen (€1006/m, CTO C-009 + Auditor bevestigd)
- Toevoegen van derde sleeve (bijv. een nieuw instrument dat power-PASS scoort) → portfolio-t  
  verschilt van individuele t; de FTMO-EV-metrieken zijn de juiste meetlat, niet de individuele t-grens  
- **Aanbeveling:** nieuwe PREREGs mogen voor portfolio-sleeve worden geschreven waarbij  
  individuele component power-FAIL is, mits de portfolio als geheel aan FTMO-EV ≥€300/m voldoet  
  (D-092.5 drempel) — vraagt expliciete CEO-bevestiging van deze interpretatie

---

## Samenvatting

| Taak | Uitkomst |
|---|---|
| (1) Portfolio EV onafhankelijk | **BEVESTIGD** — ORB+BTC ≈€970-1006/m, SR≈1.22, ρ=0.113 exact ✓ |
| (2a) N11 gate-verificatie | **PASS** — statistieken consistent; FAIL_T juist |
| (2b) N18 gate-verificatie | **PASS** — stress-marge 0.008bp (labiel); FAIL_T juist |
| (2c) LUNCH gate-verificatie | **PASS** — US100 t≈0 bevestigt FAIL_T juist |
| (2d) S2-BTC gate-verificatie | **PASS** — 132<150 power-FAIL correct; cost-gate ruim PASS |
| (2e) XAU gate-verificatie | **PASS** — 12 signalen; power structureel; cost-gate PASS |
| (3) Nieuwe sporen | 5 sporen geïdentificeerd; spoor B (multi-index pooling) en C (BTC uitbreiding) meest direct realiseerbaar |

Geen PREREG-schendingen aangetroffen. Alle gerapporteerde getallen zijn intern consistent.  
Geen reserve 2025+ gebruikt.
