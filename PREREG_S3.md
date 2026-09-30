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
