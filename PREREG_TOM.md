# PREREG — Turn-of-month (vastgelegd vóór berekening, 2 okt 2026)
Mechanisme: maandelijkse kapitaalstromen (salaris/pensioen) -> koopdruk rond maandwissel (Ariel 1987, Lakonishok-Smidt 1988).
Regel (1 parameterset): long index vanaf slot van de 2e-laatste handelsdag van de maand tot slot van de 3e handelsdag van de volgende maand (~5 nachten). Indices: SPX_TR(proxy US500), NDX, DAX, FTSE, N225, STOXX50, DJI.
Kosten: spread 0.8bp + swap long 7.5%/jr (=2.05bp/nacht x ~5 = 10bp) => 11bp per rondreis. Gate: bruto gem. >= 3x spread-kosten (zie gate) en netto > 0.
Periode: 1990-2015 (train), 2016-2024 (test); 2025+ ongebruikt. PASS: netto >0 en dag-gecorrigeerde t >= 2 in train EN test, >=5/7 indices positief in test, >=60% jaren positief.
Trials +7 (CEO-T9).
