# VOORSTEL F (G3) — 3 nieuwe hypothesen in de stijl 'kortetermijn-omkeer dag + intraday-breakout' (2026-09-30)

Alle drie met vaste literatuurparameters, pre-registratie hieronder, elk telt als 1 trial. Data FTMO (D1 / M5) 2021–2026 en
waar mogelijk Yahoo 1990–2026. Kosten als E1 (dag) resp. B4 (intraday).

## H1 — NR7-opening-range-breakout (Crabel 1990) — BEST ONDERBOUWD, wordt nu uitgevoerd
Motivatie: de ORB-poot is kostengevoelig (1,7 bp/trade). Crabel: breakouts na een 'narrow range'-dag (kleinste dagrange van
de laatste 7 dagen) hebben een grotere vervolgbeweging → hogere bp/trade bij veel minder trades → minder kostengevoelig.
Regel: B4a-ORB (30 min, stop andere kant, sessie-einde), **alleen op dagen waarvan de vorige sessie de kleinste high-low
(sessie) had van de laatste 7 sessies**. 7 FTMO-symbolen van B4 (vast, niet alleen de goede).
Beslisregel (als B4): t ≥ 3 in train 2021–23 én test 2024–26, N ≥ 500, expectancy > 0 in ≥ 4/6 jaren; plus bp/trade ≥ 2×
die van B4a (anders geen kostenvoordeel).

## H2 — 'Double 7s' (Connors & Alvarez 2009), dag-omkeer
Long als slot = laagste slot van 7 dagen én slot > SMA200; uitstap als slot = hoogste slot van 7 dagen. FTMO-D1 op de 6 E1-symbolen
en Yahoo 1990–2026 (B2-universum). Beslisregel als B2: t ≥ 3 (Yahoo 1990–2026), beide helften positief, DSR ≥ 0,5, en op FTMO
2021–26 netto positief. (Verwacht sterk gecorreleerd met RSI(2) → zelfde dagverliesprobleem.)

## H3 — RSI(2) alleen in hoog-vol-regime
RSI(2)-regel ongewijzigd, maar alleen instappen als de 20-daagse gerealiseerde vol van het instrument boven zijn eigen
252-daagse mediaan ligt (bekend vooraf). Literatuur: omkeer sterker bij hoge vol. Beslisregel: Sharpe-verbetering ≥ 0,15 t.o.v.
RSI(2) op Yahoo 1990–2026 én FTMO 2021–26 niet slechter.

Volgorde: H1 nu; H2/H3 als H1 klaar is (H2/H3 dragen het dagverliesprobleem van RSI(2) mee → lagere prioriteit).
