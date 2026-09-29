# PREREG B4 — intraday op FTMO-M5-data 2021–2026 (vastgelegd vóór berekening, 2026-09-29)

## Data (datakenmerken gecontroleerd vóór resultaten)
- FTMO M5-bars (bid) met spread per bar, geëxporteerd via `mt5_export_m5.py` (MaxBars van de terminal
  verhoogd van 100.000 naar 5.000.000; backup `common.ini.bak_maxbars100000`). Symbolen: US500, US100,
  US30, GER40, UK100 (.cash), XAUUSD, EURUSD. 2021 is voor US500/US100/UK100 maar ~1/3 gevuld en voor
  GER40 vrijwel leeg (bekend FTMO-datagat).
- Servertijd = New York + 7 uur (bevestigd: US-cash-open op 16:30 server, Frankfurt/Londen-open 10:00).
  Omrekening naar lokale sessietijd via zoneinfo (NY-tijd = server − 7u).
- Sessies (lokaal): US500/US100/US30/XAUUSD New York 09:30–16:00; GER40 Frankfurt 09:00–17:30;
  UK100/EURUSD Londen 08:00–16:30. Een sessiedag telt alleen als de bar op het openingstijdstip en de
  laatste bar vóór sluiting bestaan.
- Kosten: spread van de bar (punten × point): long betaalt de spread van de instapbar, short die van de
  uitstapbar (bars zijn bid). Commissie per kant (afgeleid uit eigen MT5-runs): indices 0; XAUUSD
  €2,00/lot ≈ 0,0006% notional; EURUSD €2,25/lot ≈ 0,00225% notional.

## Strategieën (één parameterset, literatuur)
- (a) Opening-range breakout: OR = high/low van de eerste 30 min (6 bars). Vanaf de 7e bar: eerste
  doorbraak boven OR-high → long (vul op OR-high, of bar-open als die al erboven ligt), stop = OR-low;
  omgekeerd short. Eén trade per dag. Uitstap op stop (vul op stop of slechtere open) of op het slot van
  de laatste sessiebar. Raakt een bar zowel instap als stop, of breekt een bar beide kanten: verlies
  (conservatief). R = OR-hoogte.
- (b) Laatste-30-minuten-momentum (Gao/Han/Li/Zhou 2018): s = teken(r1 + r12), r1 = vorige sessieslot →
  slot van de bar die eindigt op open+30 min, r12 = rendement van sluiting−60 → sluiting−30 min.
  Instap op de open van de bar die begint op sluiting−30 min, uitstap op het sessieslot.
- (c) Eerste-uur-reversal na gap: gap = open eerste bar / vorige sessieslot − 1. Als |gap| > 0,5%:
  positie tegen de gap in op de open van de eerste bar, uitstap op het slot van de bar die eindigt op
  open+60 min.

## Evaluatie en beslisregel (per strategie, trades gepoold over de 7 symbolen)
- Per trade netto rendement (% van notional); voor (a) ook in R.
- Train 2021-01..2023-12, test 2024-01..2026-09.
- **Beslisregel:** t-stat (per-trade netto rendementen) ≥ 3 in train **én** in test, N ≥ 500,
  netto expectancy > 0 in ≥ 4 van de 6 kalenderjaren. Plus per symbool, per jaar, DSR (N = 326).
- Trials +3 → TRIAL_COUNT 326.
