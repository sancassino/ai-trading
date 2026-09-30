# VERSLAG backlog v16 (Uitvoerder, 2026-09-30 ≈ 12:15 Amsterdam)

| Taak | Uitkomst | Trials |
|---|---|---|
| S2-F (D-012) | (a) en (c) halen gemiddeld ≥ 8,7 bp, maar zonder top-5% negatief (−25,7 / −13,2 bp) → STOP; (b), (d) poort faalt | 0 |
| S8 decay-EV ORB | toegestane schaal (dip < 4%): 2021–26 €222/mnd (P<0 37%), 2024–26 €149, 2025–26 €259, 2021–23 €306; banden breed | 0 |
| S9 stap 1 | vol-regime verklaart de edge niet (laag-vol-terciel het best). **ORB dag-geclusterd t = 1,81** (per-trade 2,93) | 0 |
| S9 stap 2 / S3b | vastgelegd in PREREG_S3 vóór er data was | (+1 bij S3-run) |
| U3 London-ORB FX | kostenpoort faalt (bruto 0,79 vs 4,49 bp) | 0 |
| U2 ORB-risico-sizing | 0,5% risico/trade: €1.095/mnd in simulatie; nul-drift €388 (optiewaarde); edge-deel ± €700 hangt aan onbevestigde ORB | 0 |
| P0 lange data | Dukascopy-feed conform maar traag/instabiel; downloader loopt (≥ 6–8 u voor SPX 2012–20); 2011 niet op de feed | 0 |

TRIAL_COUNT blijft 414. **Kern:** er is één configuratie die het doel in de simulatie haalt (ORB + risico-sizing), maar het bewijs voor de
ORB-edge is zwakker dan gedacht (dag-geclusterd t 1,81). S3 op 2012–20 beslist. Open: U-003 (MT5-reconciliatie risico-sizing, standaardactie: uitvoeren).
