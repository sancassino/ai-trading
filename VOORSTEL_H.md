# VOORSTEL H — nieuwe hypothesen met economische logica (2026-09-30)

Context: Q1 toont dat €800–900/mnd onder de echte FTMO-mechaniek een Sharpe ≈ 4 vereist; geen enkele gepubliceerde anomalie
komt daar alleen in de buurt. Deze hypothesen richten zich op **stromen** (flows) met een aanwijsbare, terugkerende oorzaak,
getest op lange data (Yahoo, 1993–2026) zodat de power voldoende is, en daarna op FTMO. Elk = 1 trial, vaste regels.

1. **H1 Maandeinde-herbalancering (best onderbouwd — wordt nu uitgevoerd).** Pensioenfondsen en balansfondsen herbalanceren
   naar vaste gewichten aandelen/obligaties aan het eind van de maand. Als aandelen de maand tot dan toe sterk beter deden dan
   obligaties, moeten zij aandelen verkopen (en omgekeerd). Literatuur: o.a. Harvey et al. (2025) "Unexpected Predictability in
   Stock Returns from Rebalancing". Regel: op het slot van de 5e laatste handelsdag van de maand: relatief rendement MTD
   = SPY − TLT; is dat > 0 → short SPY tot het maandslot, < 0 → long SPY tot het maandslot.
2. **H2 Pre-feestdag-effect.** Dag vóór een US-beursfeestdag: lagere short-interesse/positieve stemming (Ariel 1990). Regel: long
   SPY van slot t−1 tot slot van de laatste handelsdag vóór de feestdag. Klein N (± 9/jaar), lange data nodig.
3. **H3 RSI(2)-overnight alleen bij hoge VIX.** Liquiditeitsvoorzieners vragen meer vergoeding bij hoge onzekerheid (Nagel 2012:
   omkeerrendementen hoger bij hoge VIX). Regel: bestaande RSI(2) max-1-nacht-variant, alleen als VIX (^VIX) > 20 bij instap.
   (Let op: G3-H3 met gerealiseerde vol faalde; hier de implied vol als toestandsvariabele.)
