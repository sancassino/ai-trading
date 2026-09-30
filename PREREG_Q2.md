# PREREG Q2 — aandelen-earnings-events op FTMO-CFD's (vastgelegd vóór berekening, 2026-09-30)

## Data
- Universum: de 41 US-genoteerde namen uit `universe_stocks49.txt` (de 8 Europese namen vallen af: andere sessie).
- Earningsdatums + tijdstip: Yahoo via `yfinance` (get_earnings_dates, limit 40; opgehaald 2026-09-30) → `earnings.csv`.
  SEC EDGAR niet gebruikt (vereist contact-e-mail in de User-Agent). Kwaliteitscheck: aandeel events met |gap| > 2% en
  vergelijking met de gemiddelde |gap| op niet-eventdagen (moet duidelijk hoger zijn).
- Eventdag: tijdstip ≥ 16:00 ET → volgende handelsdag; < 09:30 ET → zelfde dag; overdag of onbekend (00:00) → overslaan.
- Koersen: FTMO-M5 2021–2026 (export via mt5_export_m5.py), US-sessie 09:30–16:00 ET.
## Regels (2 varianten)
- gap = open van de 09:30-bar / slot van de vorige sessie (15:55-bar) − 1; alleen events met |gap| > 2%.
  OR15 = high/low van 09:30–09:45 (3 bars). Instap op de open van de 09:45-bar.
- (a) **Continuatie:** positie in de richting van de gap; stop = tegenovergestelde kant van OR15; uitstap op het slot van de 15:55-bar.
- (b) **Fade:** positie tegen de gap in; stop = OR15-uiterste in de gaprichting; uitstap 15:55-slot.
- Stop-fill: stopprijs of slechtere bar-open. Kosten: spread van de instapbar (long) resp. uitstapbar (short) + 0,002% commissie
  per kant; geen swap (intraday).
## Beslisregel (per variant)
Netto t ≥ 3 in train (2021–2023) én test (2024–2026), N ≥ 500, netto > 0 in ≥ 4/6 jaren, DSR(N = 396) > 0,5, en gemiddeld bruto
rendement per trade ≥ 3× de gemiddelde kosten. Trials +2 → 396.
