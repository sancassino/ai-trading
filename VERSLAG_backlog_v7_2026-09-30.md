# Verslag BACKLOG v7 (L1–L5) — 2026-09-30

| Taak | Uitkomst |
|---|---|
| L1 lange intraday-data | **Geblokkeerd.** Dukascopy-datafeed geeft 429 (rate-limit; bulk alleen via betaalde AWS-S3 'Requester Pays'); HistData blokkeert geautomatiseerde downloads (betaald abonnement voor automatisering); Stooq heeft een botcheck. Niets omzeild. |
| L2 ORB 2010–2020 | Niet uitgevoerd (afhankelijk van L1). |
| L3(a) pre-FOMC 1994–2026 | Formeel geslaagd (N 264, +22,9 bp, t 3,03), maar effect 1994–2011 +33,7 bp (t 3,3) → 2012–2026 +9,8 bp (t 0,9); 2021–26 dagproxy ≈ 0. Niet betrouwbaar. |
| L3(b) nachten op Dukascopy | Niet uitgevoerd (L1). |
| L4 portefeuille lange steekproef | Niet uitgevoerd (L1). PLAFOND_RAPPORT bijgewerkt: ≈ €100–250/mnd. |
| L5 forward-weekrapport | Gebouwd: forward_week.py, cron maandag 22:45 UTC → forward/weekrapport.md (eerste: 2026-10-05). |

**Nodig van Sandro om L1–L4 te kunnen doen (kies één):** (1) AWS-account voor Dukascopy-S3 (kosten naar schatting enkele
dollars), (2) HistData-bestanden handmatig downloaden (≈ 80 bestanden: SPXUSD, NSXUSD, GRXEUR, XAUUSD, EURUSD, ASCII M1,
2010–2026) en in `data/long_m1/` zetten, of (3) een betaalde databron.
