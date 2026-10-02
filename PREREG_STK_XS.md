# PREREG — aandelen cross-sectioneel intraday (2 okt 2026)
Universum: 30 US-aandelen-CFD op FTMO. Dagelijks (open 09:30 NY -> slot 16:00 NY). Signalen uit data t/m gisteren-slot of open vandaag:
S1: long 6 laagste / short 6 hoogste voorgaande-dag-rendement (reversal); S2: long 6 hoogste / short 6 laagste overnight-gap (open/prev close −1) (gap-momentum); S3: tegengesteld aan S2 (gap-reversal); S4: S1 maar rendement van laatste 30 min gisteren.
Kosten: per been rondreis uit COSTS_FTMO_alle (2.5–40 bp, mediaan ~5bp) + 0.002%/kant. Geen swap (intraday). Equal weight.
Train 2021–2023, test 2024; 2025+ ongebruikt. PASS: netto > 0 en dag-t >= 2 in train én test. Trials +4 (CEO-T11).
