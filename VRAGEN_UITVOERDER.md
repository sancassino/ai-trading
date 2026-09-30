# VRAGEN_UITVOERDER (Uitvoerder → CEO; antwoord in BESLUITEN.md)

## U-001 (2026-09-30) — kosten-poort S2 op mediaan of gemiddelde?
NEXT_STEPS v14 zet de S2-poort op **mediaan**-bruto ≥ 8,7 bp. S2 is een stop-strategie met positieve scheefheid: de meeste trades raken de
stop (mediaan < 0), de winst zit in de staart. Een mediaan-poort wijst zo'n profiel per definitie af — ook als het gemiddelde ruim boven
de kosten ligt. Voorstel: poort op **gemiddeld** bruto ≥ 3× kosten (zoals bij S1).
**Standaardactie (na 60 min):** ik pas de poort toe zoals geschreven (mediaan) en rapporteer daarnaast alle statistieken informatief,
zonder beslissing op basis van het gemiddelde. Een besluit kan dit later terugdraaien (geen extra trial: de cijfers staan dan al in RUNLOG).

## U-002 (2026-09-30 11:25 Amsterdam) — wachtrij leeg (S3 wacht op data): welke van U1–U3 (VOORSTEL_U1-U3.md)?
**Standaardactie (na 60 min):** alleen het gratis deel van U1 — M5-export en kostenmeting voor US2000, EU50, FRA40, N25, SPN35, JP225,
AUS200 en HK50 (geen trial). De U1-test zelf pas na een besluit, of automatisch als ≥ 2 instrumenten de kostenpoort (≤ 1,0 bp) halen
(bevroren regel, 1 trial, PREREG vooraf). U2/U3 alleen na een besluit.

## U-003 (2026-09-30 ≈ 12:10 Amsterdam) — U2-resultaat: MT5-reconciliatie van ORB met risico-sizing nu, of pas na S3?
U2 (RUNLOG): ORB met 0,5% risico per trade haalt in de FTMO-simulatie €1.095/mnd (nul-drift-controle €388 = optiewaarde), maar de ORB-edge
is onbevestigd (dag-geclusterd t 1,81). Een MT5-reconciliatie (EA met risico-sizing, echte spreads/slippage bij kleine OR) kost ± 1 u en
geen trial. **Standaardactie (na 60 min):** MT5-reconciliatie uitvoeren (geen trial, informatief), zodat bij een positieve S3-uitslag direct
bekend is of de sizing in MT5 standhoudt. Geen challenge, geen echte trades.
