# PREREG D2 — goud vs reële rente, lead-lag (vastgelegd vóór berekening, 2026-09-29)

- Data: GLD (Yahoo adjusted, 2004-11..2026-09) als goudproxy; reële rente FRED DFII10 (10-jaars TIPS-rendement).
- Regel: op de eerste handelsdag van elke maand Δ = DFII10(t−2) − DFII10(t−2 − 20 handelsdagen)
  (t−2 = veilige publicatievertraging). Δ < 0 → long goud; Δ > 0 → short goud; Δ = 0 → flat. 100% notional,
  uitvoering op slot van de rebalansdag, houden tot de volgende rebalans.
- Kosten: spread 0,02% per kant (FTMO-XAU-mediaan 0,007%); financiering zoals FTMO nu (swap_specs_FTMO.csv):
  long −7,93%/jr, short −0,37%/jr (constant). Diagnostiek (geen beslisgrond): DTB3 ± 2%.
- Beslisregel: netto Sharpe ≥ 0,7, t ≥ 3, positief in beide helften (2005–2015, 2016–2026), DSR(N = 347) ≥ 0,5.
- Trials +1 → 347.
