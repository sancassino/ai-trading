# PREREG — ORB op extra indices (vastgelegd vóór berekening, 2 okt 2026)
Vraag: is de ORB-winst (US100 +5.9, GER40 +4.0, US500 +2.4) een index-effect? Out-of-instrument toets.
Regel: exact B4a-ORB (OR 30 min, stop = andere kant OR, uitstap sessieslot), GEEN parameters aangepast.
Nieuwe instrumenten: EU50cash (Berlin 09:00–17:30), FRA40cash (Berlin 09:00–17:30), JP225cash (Tokyo 09:00–15:00; FTMO-uren onzeker, alleen sessies die 'volledig' zijn).
Kosten: gem. kosten van GER40 (0.5bp) als schatting (spread-data ontbreekt in lokale M5; gevoeligheid: 1.5bp).
PASS: gepoold over de 3 nieuwe: gem netto > 0 bij 1.5bp-kosten met dag-t ≥ 2.0 én ≥ 2 van 3 symbolen positief. Trials +3 (TRIALS.csv).
Periode: alles <2025 voor oordeel; 2025+ alleen als beschrijvende bevestiging (reserve voor ORB is verbruikt).
