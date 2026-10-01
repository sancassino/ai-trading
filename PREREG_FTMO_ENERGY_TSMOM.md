# PREREG_FTMO_ENERGY_TSMOM — long-only energy time-series momentum (CTO C-023 / D-099)

**Status:** Pre-registratie 2026-10-01 ~10:35 Europe/Amsterdam, branch `grok/cto-1`.  
**Auteur:** Grok CTO (D-099 gaf Strateeg de opdracht; CTO bevriest hier de regel zodat U2 niet idle blijft — Strateeg/CEO mogen erratum/adopt op main).  
**Geen resultaat van deze exacte bevroren regel gezien als formele gate vóór deze commit.**  
C-022 (diagnostic screen, 0 trials) liep eerder op proxies ≤2024-12-31 en motiveerde D-099; die rijen zijn **niet** de formele toets. Forking-path: Auditor telt C-022 energy-familie mee in FDR-context (zelfde openbaarmaking als erratum op TSMOM_DIV).

**Waarom niet TSMOM_DIV:** U2 `e5d23c5` → `FAIL_COST_GATE` (mean bruto −5,73 bp vs cost 45,12 bp; ≈29 nachten swap). Geen klonen van die maandelijkse 56-naam L/S-regel.

## 1. Bevroren regel

- **Universum (vast):** `UKOIL.cash`, `USOIL.cash` alleen. **Geen** HEATOIL/NGAS in v1 (HEATOIL had in C-022 alleen fallback-kosten). Geen crypto, geen indices, geen FX.
- **Proxy mechanisme (D-094a b):** `BRENT_F` → UKOIL, `WTI_F` → USOIL uit `data/PROXY_MAP_FTMO.csv` / `data/daily/` (≥10 jaar tot 2024).
- **Signaal (dagelijkse slots, proxy):** \( s_t = \mathrm{sign}(P_t / P_{t-20} - 1) \). Alleen **long** als \( s_t > 0 \); flat als \( s_t \le 0 \). Geen short-been.
- **Entry / exit:** signaal op slot \( t \); entry slot \( t+1 \); **hold = 10 handelsdagen**; daarna flat tot nieuw long-signaal. Geen stops, geen trailing, geen lookback/hold-tuning na deze commit.
- **Positie:** gelijke risico-weging over actieve longs; doelvol per been 10%/jr (σ = 20d realized t/m \( t \)); portefeuille-vol cap ≈10%/jr via diagonale schaal. Geen heroptimalisatie na zien van resultaten.
- **Kosten:**
  - Rondreis uit `COSTS_FTMO.csv` / `COSTS_FTMO_alle.csv` voor UKOILcash / USOILcash.
  - Overnight swap per nacht uit dezelfde bron / `swap_specs_FTMO.csv`, long apart.
  - **Alfa-maatstaf = bruto prijsrendement** (zonder swap-credit). Rapporteer daarnaast netto mét swap en +50% swap-stress. Swap-long credit op olie **mag geen** PASS dragen (D-099 / C-022 caveat).

## 2. Mechanisme

Commodity trend persistence (Moskowitz–Ooi–Pedersen e.a.): trage inventory/hedging flows op olie. Hold 10d / lookback 20d mikte op D-097 “50–300 bp bruto / trade” met lagere overnight-last dan maandelijkse 12-1 (TSMOM_DIV). Bekend risico: 2014–16 / 2020 oil crashes; 2023–24 zwakke trendpremie.

## 3. Data en toetsvenster

- Ontdekking / kostenpoort / toets: proxy dagdata **≤ 2024-12-31** (hard cut).  
- Train: **2010-01-01 → 2016-12-31**. Test: **2017-01-01 → 2024-12-31**.  
- Reserve **2025-01-01 → heden: onaangeroerd** tot CEO-vrijgave (D-084).  
- FTMO-M5: optioneel voor uitvoeringssanity; poort mag op proxy+FTMO-kostenconstanten (zoals TSMOM_DIV).

## 4. Beslisregel (vóór reserve)

1. **Kostenpoort (geen trial bij FAIL):** mean **bruto prijs**-bp per completed trade ≥ 3× mean (RT + |swap-cost|) over train, waarbij swap-cost voor de poort = max(swap_long, 0) × nachten (credits op 0 gezet). Stress: zelfde met swap×1,5. Faalt → STOP.
2. **Toets (1 trial bij door poort):** dag-geclusterd netto-t (mét echte signed swap) ≥ 2,0 in train **én** test; mean netto > 0 in beide helften van train en van test; mean bruto prijs > 0 in beide helften; N_trades ≥ 150 gepoold over UKOIL+USOIL; beide symbolen mean bruto prijs ≥ 0 op test.
3. **FTMO-EV:** bij PASS → CTO `engine/ftmo.py` `recommend_scale` op gecombineerde dagreeks; ook +50% swap; rapporteer p_pass, p_survive, net EV.
4. Bij PASS: shortlist → CEO reserve-besluit + Auditor. Bij FAIL: 1 trial, **geen klonen** (geen L/H-grid, geen HEATOIL-add, geen short-been).

## 5. Verwachting

Prior: gematigd. C-022 diagnostic (niet-bindend) suggereerde UKOIL L20/H10 bruto ~117 bp / t_net ~3,6 en USOIL ~61 bp / t_net ~2,3 op 2015–2024 — dat is zoekpad-context, geen bewijs. Falen kan: swap/RT op FTMO-olie, trendloos 2017–19, of h1-zwakte op USOIL.

## 6. Dead-set afbakening

Niet herstarten: TSMOM_DIV, classic XS-mom L3/S3, S2-USOIL intradag, P1, N35–N44, GBPJPY_EU_MOM. Dit PREREG is een **andere** hypothese (2-naam long-only 20/10, niet 56-naam monthly 12-1).
