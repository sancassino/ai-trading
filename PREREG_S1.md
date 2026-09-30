# PREREG S1 — Noise-area intraday-momentum (Zarattini–Aziz–Barbon 2024) op FTMO-indices (vastgelegd vóór berekening, 2026-09-30)

**Bron van de regel (S1a, geverifieerd):** volledige tekst van SFI RP 24-97 / SSRN 4824172, open-access kopie in de repository van de
Universiteit St. Gallen (alexandria.unisg.ch, item 71ef0a23-…; SSRN zelf gaf 403 — niet omzeild). Regel (§ 'Noise Area', 'Trailing stops'):
- move(t−i, HH:MM) = |Close(t−i, HH:MM) / Open(t−i, open) − 1|, i = 1…14; σ(t, HH:MM) = gemiddelde over de 14 vorige sessies.
- UB = max(Open_t, Close_{t−1}) × (1 + σ), LB = min(Open_t, Close_{t−1}) × (1 − σ) (gap-aanpassing uit het paper).
- Beslissen alleen op HH:00 en HH:30 (eerste beslissing 30 min na de open, US 10:00); long als koers > UB, short als < LB.
- Trailing stop (alleen op de beslismomenten): long sluit als koers < max(UB, VWAP), short als koers > min(LB, VWAP); na sluiten
  direct omkeren als de koers buiten de andere band ligt; alles dicht bij de sessie-sluiting. VWAP alleen over sessie-uren.
- Paper-grootte: aandelen = AUM × min(4, 2% / σ_dag,14) / open.

**Vertaling naar FTMO-M5 (vast):** koers op HH:MM = slot van de M5-bar die om HH:MM−5 begint; open = open van de eerste sessiebar;
Close_{t−1} = slot van de laatste bar van de vorige volledige sessie; VWAP = Σ(typische prijs × tick_volume) / Σ tick_volume vanaf de open
(tick_volume als volume-proxy, data/m5_vol). Sessies zoals b4_sim.SYMS: US500/US100/US30 09:30–16:00 New York, GER40 09:00–17:30 Berlijn.
Kosten per trade: spread van de instapbar (long) / uitstapbar (short) + 2× commissie (indices 0; COSTS_FTMO.csv).
Grootte per symbool voor de dagreeks: equity/4 × min(4, 2% / σ_dag,14); per-trade-statistiek ongewogen in bp.

**Varianten (4, vast; familie van 4):** (a) paper-basis (30 min, band+VWAP, σ 14 d); (b) beslissen elk uur (open+60, +120, …);
(c) zonder VWAP (stop = eigen band); (d) σ-venster 28 dagen.

**Kosten-poort (eerst, op train 2021–2023):** gemiddelde bruto bp/trade ≥ 3× gemiddelde kosten/trade. Variant die faalt → stop, geen trial.
**Beslisregel per variant die de poort haalt:** netto t ≥ 3,5 in train (2021–23) én test (2024–26); N ≥ 500 trades; ≥ 4/6 jaar positief;
+50% spread: t ≥ 2 in test. Rapporteer apart de echte out-of-sample na het paper-venster **2025-01…2026-09** (moet positief zijn),
dagreeks-SR, skew, max dagdip, en correlatie van de dagreeks met ORB (results/f/F2_ORB_daily.csv; > 0,7 = geen nieuwe sleeve).
TRIAL_COUNT +1 per variant die de poort haalt (basis 410).
