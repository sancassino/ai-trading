# PREREG CAT4 — catalogusrun 4 (Uitvoerder-2; D-063: v1.2-diversifiers) — vastgelegd vóór berekening, 2026-09-30 (≈ 16:45 Amsterdam)

Engine/gates/vehikelset zoals PREREG_CAT2/3 en PREREG_PORT (etf 13 bp/TER 0,07%; ontdekking ≤ 2024-12-31; reserve niet aangeraakt). **5 trials** (C57, C58, C59, C60, C61; 1 variant elk) → TRIAL_COUNT 440.
C62/C63 alleen compleetheid (geen sleeve; C63 geschrapt), C64 (managed-futures-UCITS) watch-list, DBMF-correlatie als evidentie (geen trial) — indien data beschikbaar.
| ID | regel (exact) | instrument(en) | vehikel | sample / label |
|---|---|---|---|---|
| C57 | maandeinde: per klasse gewicht 1/5 als maandeindslot > gemiddelde van de laatste 10 maandeinden (adj.), anders kas; ontbrekende klasse = kas | SPY, EFA, IEF, GLD, DBC | etf | 2003→ (GLD 2004-11, DBC 2006-02 komen later binnen); benchmark 60/40 SPY/IEF |
| C58 | idem op één activum: long GLD, anders kas | GLD | etf | 2005-09→ = 19,3 jr → **label 'korte reeks'**; regime 2001–11 goud-bull |
| C59 | idem: long DBC, anders kas | DBC | etf | 2007-02→ ≈ 17,9 jr → **'korte reeks'** |
| C60 | idem op synthetische 10j-Treasury (TR, D=8/C=80 uit ^TNX); **jaren 70–00 apart gerapporteerd** | BOND10_SYN | etf | 1963→ ; benchmark B&H obligatie |
| C61 | maandeinde: SPX-slot > SMA(10 maandeinden) → +1× SPX (TR waar de engine SPX_TR heeft), anders −1× **dagelijks gereset inverse-ETF** (vehikel `etf_inverse`: TER 0,50% op het short-deel, 13 bp rondreis, kapitaal verdient rf; totaal = p·r + rf·(1 − long-deel)) | SPX | etf_inverse | 1928→ ; variant (a) 'long/cash' is C02 (SPX-deel) en telt niet apart |
**C61-compounding-test (vooraf, verplicht vóór lezing van C61):** het engine-model is dagelijks herwogen (−1× per dag). Ik toon met de bear-episodes 2000–03 en 2007–09 dat (i) −Σ dagrendementen ≠ −(periode-rendement) en (ii) de dagelijks-gereste inverse over de episode het pad-afhankelijke verschil laat zien; C61 telt alleen als de conventie klopt.
**Diversifier-screen (vooraf, vehikelrapport, geen trial):** (i) corr overschot met C02, C52 lang, SPX-excess ≤ 0,3; (ii) ΔSR en ΔmaxDD van P-ETF-a bij toevoeging als derde sleeve (methode PREREG_PORT §2 P-ETF-a, gelijk-1/σ); (iii) uitvoerbaarheid UCITS/ETC (TER web-claim); (iv) ≥ 20 jr of 'korte reeks'-label.
**Verwachting (vooraf):** C57 SR 0,4–0,6 maar corr met C02 ≈ 0,5–0,6 → geen diversifier; C58/C59 SR 0,2–0,5, korte reeks, lage t; C60 SR 0,2–0,4 met zwak 1970–81 en pijnlijk 2022; C61 SR ≈ C02 ± 0,1 en hogere kosten; verwacht 0–2 door G-ontdekking en ≤ 1 die het screen haalt.
