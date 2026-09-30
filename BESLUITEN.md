# BESLUITEN (CEO) — eigenaar: CEO · branch claude/upbeat-dirac-g2810q
Formaat: **D-nnn · antwoordt op <ID> · besluit · reden · wie doet wat · geldig tot/heroverweeg wanneer.**
Manager/Strateeg/Uitvoerder halen dit bestand op met `git show origin/claude/upbeat-dirac-g2810q:BESLUITEN.md`.

## 2026-09-30 10:55 Amsterdam — antwoorden op M-001…M-007

**D-001 · M-001 (lange ORB-data)** · **BESLOTEN: optie A (HistData, gratis) — maar verkleind.** Alleen **2011 t/m 2020** nodig (2021–26 hebben we al via FTMO): 4 instrumenten × 10 jaar ≈ **40 zips i.p.v. ~100**; 2010-11 en 2021+ NIET downloaden. Volgorde voor Sandro: SPX → NSX → GRX → XAU (SPX alleen levert al een voorlopige S3-uitslag). Dukascopy/AWS (creditcard-account) en betaalde sets: **niet nu** (geld/account = Sandro-grens; pas overwegen als HistData onbruikbaar blijkt). Andere MT5-demo: **nee** (account op Sandro's naam, onzeker).
· Reden: hoogste waarde/kosten in het project; kleinste mens-inspanning. · Wie: CEO zet A-01 in `SANDRO_ACTIES.md` en meldt Sandro. Manager past `DATA_REQUEST_SANDRO.md` aan naar "alleen 2011–2020, SPX→NSX→GRX→XAU". Uitvoerder maakt S3-voorbereiding (parser+PREREG) af **vóór** de data landt. · Heroverweeg: als data niet vóór **vr 3 okt 12:00** binnen is → zie D-004.

**D-002 · M-002 (FTMO-fee/accountgroottes)** · **BESLOTEN: standaardactie B** (doorrekenen met aanname, elke EV/frontier labelen "onder aanname fee €540/€80k"). De fee wijzigt het go/no-go van het *onderzoek* niet; hij telt pas bij de beslissing om een echte evaluatie te kopen — en die aankoop is sowieso Sandro's beslissing. Wél 2 min Sandro-werk als lage prioriteit (A-02). · Wie: Manager labelt; CEO A-02. · Heroverweeg: zodra een kandidaat de S3/S1-beslisregels haalt.

**D-003 · M-003 (streefdoel)** · **BESLOTEN: optie C + tussendoelen.** €800–900/mnd blijft de ambitie, maar succes wordt in trappen gemeten:
 - **Trap 1 (bewijs):** ORB bevestigd op 2011–20 (S3 "bevestigd").
 - **Trap 2 (waarde):** ≥ 1 dagelijks-vlakke, positief-scheve sleeve met netto SR ≥ 0,8 die de kostenpoort haalt.
 - **Trap 3 (geld):** Q1b-frontier ≥ €300/mnd onder FTMO-mechaniek → dan pas besluit over echte evaluatie (Sandro).
 Trap 3 is het realistische tussendoel; €800–900 alleen als Trap 2 twee onafhankelijke sleeves oplevert. Eerlijk: kans op €800–900 ≤ 10%, op Trap 1 ≈ 35–40%. · Wie: Manager neemt trappen op in `EINDVERSLAG.md`. · Heroverweeg: na S0–S3.

**D-004 · M-004 (stopcriteria)** · **BESLOTEN: A + harde datum.** Projectniveau-stop/pauze (CEO meldt Sandro met reden) als:
 1. S3 = **verworpen** of **onbeslist** (na volledige data) **en** S1 én S2 falen hun beslisregel of kostenpoort; óf
 2. **vr 3 okt 12:00**: geen lange data binnen én S1/S2 niet positief → bevriezen op forward-paper (Q6), Uitvoerder-cyclus terug naar 1×/uur.
 Tussentijds: elke 24 u een evaluatie in `EINDVERSLAG.md` (Manager) + mini-review CEO elke 3 u. **Nieuw:** S1 deelt het mechanisme met ORB. Verwerpt S3 de ORB, dan krijgt S1 een lagere prior → S1 alleen nog als afronding, geen extra varianten. · Wie: Manager bewaakt; CEO beslist bij trigger.

**D-005 · M-005 (Auditor)** · **BESLOTEN: B** — pas als een kandidaat een beslisregel haalt. Dan óók vóór elke echte-geld-stap. · Wie: CEO triggert.

**D-006 · M-006 (drempel S3)** · **BESLOTEN: aanhouden (t ≥ 2,5 + Manager-aanscherping), met 2 toevoegingen:** (i) t-waarde **dag-geclusterd** (of blok-bootstrap per dag) berekenen, want US500/US100/GER40 bewegen gecorreleerd — gepoolde t over symbolen overschat anders het bewijs; (ii) drempels staan vast in PREREG_S3 **vóór** de data wordt aangeraakt (geen aanpassing na de eerste blik). Eén frozen regel, één test — dit is geen zoektocht, dus geen t ≥ 3,5. · Wie: Uitvoerder (PREREG_S3), Manager toetst.

**D-007 · M-007 (ritme)** · **BESLOTEN: houden** (Manager :05/:35, CEO :10/:40, Strateeg :20/:50, Uitvoerder */10). Verbeteringen: (a) **lege cycli goedkoop houden** — één regel in eigen log, niet opnieuw alles herlezen; (b) Uitvoerder mag een lopende taak niet voor een lagere prioriteit laten liggen: bij elke */10-check herordenen volgens NEXT_STEPS-volgorde; (c) **S3 preempt** alles zodra `data/long_m1/` gevuld is.

## 2026-09-30 10:55 — Extra besluiten (proces/prioriteit)

**D-008 · Prioriteit Uitvoerder** · Volgorde: **S0 (cap 30 min) → S1 → S2 (cap 2 u, kostenpoort eerst) → S3-voorbereiding** (PREREG_S3, parser, test op synthetisch mini-bestand; klaar binnen ~3 u). S3-run zodra data landt. Reden: data-aankomst is het kritieke pad en hangt van een mens af; alles wat parallel kan, doet de Uitvoerder nu. S1/S2: **kostenpoort faalt = stop zonder trial-telling**, geen "even proberen".

**D-009 · Reserve-lijst Strateeg** · **SCHRAPPEN: S4** (FX-H4-trend is met R4 al afgewezen; D1-variant zelfde familie), **S5 en S7** (N te klein om ooit t ≥ 3 te halen — Strateeg zegt het zelf). **S6 (olie-voorraad)**: alleen exploratief, laagste prioriteit. **R1/R2/R4 vervallen** (klaar). Strateeg: lever nieuwe voorstellen alleen als ze (i) dagelijks-vlak/positief-scheef zijn, (ii) N ≥ 500 kunnen halen, (iii) draaien op data die we al hebben of gratis+geautomatiseerd kunnen krijgen. Denk ook aan **wat het verschil maakt buiten "nog een signaal"**: bv. portefeuille-/sizing-mechaniek onder FTMO-regels, en of ORB+RSI(2) samen de FTMO-slaagkans verhogen (Q1b-achtig, gratis analyse).

**D-010 · S2-verwachting** · S2 mag door, maar met verwachtingsmanagement: N = 859 events → weinig power; Q2 faalde al (t 1,35/0,91). Uitvoerder rapporteert **bruto-mediaan vs 8,7 bp poort eerst**; faalt die, dan stopt S2 na de poort.
