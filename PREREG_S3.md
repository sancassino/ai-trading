# PREREG S3 — ORB-bevestiging op 2011–2020 (bevroren B4a-regel, één test) — vastgelegd vóór er data is (2026-09-30)

**Regel (bevroren, niets aanpassen):** `b4_sim.run_orb` — OR = eerste 30 min van de cash-sessie, buy-/sell-stop OCO op OR-high/-low,
stop aan de andere kant, uit op de sessie-sluiting, 1 trade/dag/symbool; sessies en commissie uit `b4_sim.SYMS`
(US500/US100 09:30–16:00 New York, GER40 09:00–17:30 Berlijn, XAUUSD 09:30–16:00 New York, commissie XAU 0,0006%/kant).

**Data:** HistData M1 ASCII (optie B, D-001): SPXUSD → US500, NSXUSD → US100, GRXEUR → GER40, XAUUSD → XAUUSD, **2011-01 t/m 2020-12**.
Parser `s3_histdata.py`: tijdstempel = EST zonder zomertijd (UTC−5, HistData-documentatie) → UTC → FTMO-servertijd (New York-lokaal + 7 u);
M1 → M5 (open eerste, high max, low min, close laatste; bars op 5-min-grens). Sessie-afbakening via `b4_sim.sessions` (volledige sessies:
eerste bar op de open, laatste bar op sluiting − 5 min). De parser rapporteert of er quotes buiten de cash-uren staan (24-uurs,
futures-/CFD-afgeleid); de OR geldt dan op het cash-openingsuur, zoals bij FTMO.
**Kosten:** FTMO-spread 2021–26 per symbool en per lokaal tijdstip-van-de-dag (mediaan als fractie van de koers) × de koers van de bar;
+50% spread als robuustheid. HistData-spread wordt niet gebruikt.

**Beslisregel (vast, D-006 + M-008; geen aanpassing na de eerste blik):**
- t-waarde **dag-geclusterd**: per handelsdag het gemiddelde netto van alle symbolen die die dag handelen; t over dagen.
- **Bevestigd** = dag-geclusterde gepoolde netto t ≥ 2,5 **én** beide helften (2011–15, 2016–20) gemiddeld positief **én** gemiddeld
  ≥ 0,9 bp/trade **én** ≥ 2 van 3 (US500/US100/GER40) individueel positief.
- **Verworpen** = t < 1 **of** gemiddelde ≤ 0,5 bp/trade → ORB uit het portfolio.
- Anders **onbeslist** (niet opschalen).
- Label (M-008), met 2021–26 = FTMO-resultaat B4a op dezelfde symbolen (results/b4/B4_a_ORB_trades.csv):
  'bevestigd + blijvend' = bevestigd én 2021–26 ≥ 0,9 bp/trade én 2024–26 ≥ 0; 'bevestigd maar vervallen' = bevestigd, maar niet blijvend;
  'verworpen' / 'onbeslist' als boven. Alleen 'bevestigd + blijvend' telt als Trap 1 (D-003).
- Rapporteer ook: jaar-per-jaar bp 2011–2026 (gestapeld met FTMO 2021–26), per symbool, +50% spread, en een voorlopige uitslag met alleen SPX
  zodra dat bestand er is (voorlopig = geen beslissing).
- TRIAL_COUNT +1 (één test).

## Secundaire hypothese S3b — vol-regime (D-017, VOORSTEL_S9), vastgelegd 2026-09-30 ≈ 09:55Z, vóór er een bestand in data/long_m1/ stond
- Primair S3-label en -drempels blijven ongewijzigd; S3b is secundair en telt +1 trial.
- Regel: dezelfde bevroren ORB-B4a-trades, maar alleen op dagen met **20d-RV(t−1) > eigen 252d-mediaan**. RV = standaarddeviatie van de
  20 laatste slot-op-slot-dagrendementen van de volledige cash-sessies van dat symbool (t.e.m. dag t−1); mediaan over de 252 laatste
  RV-waarden (t.e.m. t−1). Opwarming: S3b-dagen pas vanaf de eerste dag met volledige historie (≈ 2012-02); geen andere drempels, geen grid.
- Beslisregel S3b: dag-geclusterde gepoolde netto t ≥ 2,5 binnen hoog-vol-dagen **én** beide helften (2011–15, 2016–20) positief **én**
  ≥ 0,9 bp/trade **én** verschil hoog-vol − laag-vol > 0 met dag-geclusterde t ≥ 2 (t van het verschil van de dagelijkse gemiddelden,
  Welch). Anders 'S3b verworpen'. Kostenpoort binnen hoog-vol: gemiddeld bruto ≥ 3× gemiddelde kosten, anders geen toets.
- Uitsluitend op 2011–2020; 2021–26 wordt voor S3b niet gebruikt (hindsight). Bron van de data: HistData óf de publieke Dukascopy-feed
  (P0, zelfde parser/formaat; bron wordt in de uitslag vermeld).

## Aanpassing primaire drempel (M-009, standaardactie C / NEXT_STEPS v17 N8) — vastgelegd 2026-09-30 ≈ 10:25Z, vóór er een bestand in data/long_m1/ stond
- **Bevestigd** vereist nu **eenzijdig dag-geclusterd t ≥ 2,0** (was t ≥ 2,5). Alle overige eisen ongewijzigd (beide helften positief,
  ≥ 0,9 bp/trade, ≥ 2 van 3 indices positief; 'blijvend' = FTMO 2021–26 ≥ 0,9 bp én 2024–26 ≥ 0; verworpen = t < 1 of ≤ 0,5 bp).
  S3b (vol-regime) houdt zijn eigen drempels. Periode wordt in de uitslag vermeld (Dukascopy-feed begint niet in 2011 → ≈ 2012–2020).
- **Power-annex** (n8_power.py, results/n8/N8_output.txt; dag-blok-bootstrap 21 d uit de FTMO-ORB-trades 2021–26 van de 4 S3-symbolen,
  3.000 simulaties): referentie FTMO 2021–26 op deze symbolen +3,38 bp/trade (2024–26 +1,65), dag-geclusterd t 2,90 (train 2,79 / test 1,12).
  | wereld (9 jaar) | (A) t ≥ 2,5: bevestigd / onbeslist / verworpen | (B) eenzijdig t ≥ 2,0 |
  |---|---|---|
  | effect op 2021–26-niveau | 88% / 11% / 1% | 95% / 4% / 0% |
  | effect gehalveerd | 18% / 56% / 26% | 33% / 41% / 26% |
  | nul (bruto 0, netto −kosten) | 0% / 1% / 99% | 0% / 1% / 99% |
  (10 jaar: 91/21/0% resp. 97/39/0% bevestigd.) Kanttekening: 'effect op 2021–26-niveau' neemt het steekproefgemiddelde als waarheid
  (winnaarsvloek → optimistisch); de halvering is het realistischer scenario. Label 'blijvend' vs 'vervallen' hangt alleen af van de
  vaste FTMO-referentie (nu: blijvend-voorwaarden vervuld).

## TERUGGEDRAAID (NEXT_STEPS v18, M-009 ingetrokken; D-006/D-023: S3-drempels vast) — 2026-09-30 ≈ 10:48Z, data/long_m1/ nog steeds leeg
- De aanpassing 'eenzijdig t ≥ 2,0' hierboven is **ingetrokken**. Geldend is weer: **bevestigd = dag-geclusterd t ≥ 2,5** plus alle overige eisen
  (ongewijzigd). Het power-annex blijft als informatie staan: bij een effect op 2021–26-niveau ≈ 88% kans op 'bevestigd', bij een gehalveerd
  effect ≈ 18% (dan meestal 'onbeslist').

## DEFINITIEF (CEO D-029/D-036) — 2026-09-30 ≈ 11:20Z, data/long_m1/ leeg
- De terugdraaiing hierboven ('TERUGGEDRAAID … t ≥ 2,5') is **ongeldig** (D-036). Geldend en **bevroren**: bevestigd = **eenzijdig dag-geclusterd
  t ≥ 2,0** + overige eisen ongewijzigd (beide helften positief, ≥ 0,9 bp/trade, ≥ 2 van 3 indices positief, label blijvend/vervallen).
  S3b houdt zijn eigen drempels. Dit bestand wordt hierna niet meer gewijzigd; de SHA-256 staat in RUNLOG.
