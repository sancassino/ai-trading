# Verslag NEXT_STEPS ronde 2 (2026-09-29)

**Uitkomst: beide families AFGEWEZEN volgens de vooraf vastgelegde beslisregel. Geen MT5-implementatie.
Het onderzoek stopt hier en wacht op een beslissing van Sandro (zie EINDVERSLAG.md).**

Pre-registratie: `PREREG_ronde2.md`, gecommit vóór enige berekening (commit ddec629). Code:
`ronde2_sim.py` (exact de pre-registratie). Data: Yahoo adjusted close (ETF's; GLD/USO/DBC vóór
start gespliced met GC=F/CL=F/^SPGSCI), FRED H.10-wisselkoersen, FRED DTB3 en IR3TIB01-rentes
(1 maand vertraagd). Periode 2000-01-04 t/m 2026-09-21 (26,7 jaar). Volledige output:
`results/ronde2/R2_output.txt`, dagreeksen `results/ronde2/R2_fam*_daily.csv`.

## Resultaten (netto, 10% vol-target, hefboomcap 4)

| | Familie 1: trend multi-asset | Familie 2: G10 carry + trend | Referentie SPY b&h @10% vol |
|---|---|---|---|
| Netto CAGR | +1,50%/jr | −1,00%/jr | +5,72%/jr |
| Volatiliteit | 11,3% | 11,0% | 10,0% |
| Sharpe (netto) | **0,19** | **−0,04** | 0,41 |
| Max DD maand / dag-equity | 39,1% / 42,7% | 68,1% / 70,4% | 28,4% / 31,7% |
| Jaren positief | 16/27 (59%) | 11/27 (41%) | 21/27 (78%) |
| Slechtste dag | −4,83% | −5,14% | −5,68% |
| €/mnd op €80k | ≈ €100 | ≈ −€67 | ≈ €381 |
| Gem. bruto hefboom | 2,21 | 2,85 | 0,52 |

Episodes: familie 1 — 2000–02 +21,5%, 2008 +17,5%, 2020 +1,8%, 2022 +17,5% (crisisbescherming werkt,
maar 2009–2024 overwegend negatief: −9,6, −6,3, −2,6, −4,2, −15,5, −12,9, −9,9, −6,2, −15,7).
Familie 2 — 2000–02 +37,6%, 2008 −16,9% (carry-crash), 2020 −9,0%, 2022 +1,7%; sinds 2006 vrijwel
alleen negatieve jaren.

Per jaar familie 1: 00:+0,0 01:+9,3 02:+11,2 03:+21,7 04:+13,1 05:−1,5 06:−6,5 07:+12,4 08:+17,5
09:−9,6 10:+3,3 11:−6,3 12:−2,6 13:+10,2 14:−4,2 15:+9,7 16:−15,5 17:+2,6 18:−12,9 19:+2,2 20:+1,8
21:−9,9 22:+17,5 23:−6,2 24:−15,7 25:+7,6 26:+4,7

Per jaar familie 2: 00:+4,6 01:+5,2 02:+25,1 03:+33,7 04:+10,3 05:+3,5 06:−7,1 07:+6,2 08:−16,9
09:+3,0 10:−9,0 11:−3,4 12:−2,7 13:−16,6 14:−3,7 15:−0,9 16:−1,0 17:−12,6 18:−7,1 19:+2,4 20:−9,0
21:−1,1 22:+1,7 23:−4,2 24:−10,6 25:−5,8 26:+4,0

## Beslisregel (Sharpe ≥ 0,7; ≥ 65% jaren+; DD < 15%; dagverlies < 5%)
| Criterium | Familie 1 | Familie 2 |
|---|---|---|
| Sharpe ≥ 0,7 | 0,19 ✗ | −0,04 ✗ |
| ≥ 65% jaren positief | 59% ✗ | 41% ✗ |
| Max DD < 15% | 39,1% ✗ | 68,1% ✗ |
| Dagverlies < 5% | 4,83% ✓ | 5,14% ✗ |
| **Oordeel** | **afgewezen** | **afgewezen** |

## Gemelde afwijkingen / controles
- **Bugfix (conform pre-registratie gemeld):** de eerste run trok in de Sharpe de korte rente af,
  terwijl de P&L al excess is (longs betalen de korte rente, CFD-cash rendeert niet). Vóór fix:
  Sharpe 0,02 / −0,21; na fix 0,19 / −0,04. Overige cijfers ongewijzigd. Referentie ongewijzigd
  (daar verdient de cash-rest wél rente).
- Lookahead gecontroleerd: signaal/vol t/m vorige slot, rentes 1 maand vertraagd, uitvoering op slot.
- Implementatiedetail familie 2 (vastgelegd vóór resultaten, hier expliciet): elke poot eerst naar
  10% vol geschaald, dan 50/50, dan geheel naar 10% vol.
- JPY doet pas vanaf 2002-05 mee in de carry-rangschikking (rente pas vanaf 2002-04).
- **Diagnostiek (geen beslisgrond):** zonder spread en markup (alleen financiering tegen de korte
  rente) familie 1 Sharpe 0,58, DD 19,7%, 70% jaren+; familie 2 Sharpe 0,42, DD 28,4%, 67%. Ook
  dan faalt de beslisregel. De CFD-markups (±4%/jr bij ~2–3× bruto hefboom) zijn doorslaggevend.

## Conclusie
Consistent met de prior van de supervisor: bekende publieke edges halen na CFD-kosten geen Sharpe
in de buurt van 0,7, laat staan de ≳1,5 die €880–2.000/mnd bij max 10% DD vereist. Beide families
verslaan een simpele SPY-positie op gelijke vol niet. **Stop; beslissing Sandro nodig** (EINDVERSLAG.md:
A stoppen / andere familie, B doel verlagen).
