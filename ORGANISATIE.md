# ORGANISATIE — trading-research firm (ingesteld 2026-09-30)

**Doel:** ≈ €800–900/mnd uit FTMO €80k, binnen alle regels, aantoonbaar (geen hindsight, geen loterij). Constraint: de Cloud-chats hebben géén SSH; alles via GitHub (`sancassino/ai-trading`).

## Rollen
| Rol | Wie | Eigenaar van | Mag NIET |
|---|---|---|---|
| **Eigenaar / CIO** | Sandro | doel, budget, beslissingen (stoppen/doorgaan/data kopen), echte accounts | — |
| **Manager (COO + Risk/Compliance + Statistiek-QA)** | deze chat (Claude, Cloud) | `NEXT_STEPS.md` (uitvoerwachtrij), `EINDVERSLAG.md`, `COORDINATION.md`, `SUPERVISOR_LOG.md`, FTMO-regels/compliance, kwaliteit van resultaten (lookahead, kosten, DSR, reproduceerbaarheid), rapportage aan Sandro, escalaties | nieuwe hypothesen bedenken (hoort bij Strateeg), zelf stoppen zonder Sandro |
| **Strateeg / Head of Research** | NIEUWE Claude-chat (Cloud) | `STRATEGIE_PLAN.md`, `VOORSTEL_S*.md` (+PREREG), `STRATEGIE_LOG.md`; hypothesen met economische logica; keuze markten/instrumenten/producten/prop-firms; gap-analyse van data en tests; kosten-eerst-screening; vertaalt inzichten naar taken | zelf tests draaien of NEXT_STEPS.md schrijven; regels na resultaat aanpassen |
| **Uitvoerder (Quant/Engineer/Data)** | Debian-agent | uitvoering, MT5, Python, data-export/-download, RUNLOG.md, PREREG/verslagen, forward-test | eigen nieuwe strategiefamilies zonder Voorstel; regels na resultaat wijzigen |
| **Auditor (Red team)** | optioneel later, aparte chat, op afroep | onafhankelijke controle van elke kandidaat die een beslisregel haalt | — |

## Werkstroom
1. Strateeg schrijft **Voorstel** (economische logica, verwachte bruto bp vs kosten, data-eis, PREREG-concept, beslisregel, verwacht SR + dip-profiel) → `VOORSTEL_S<n>.md` op zijn branch.
2. Manager toetst binnen het uur (kosten-eerst, multiple testing, FTMO-conform, haalbaar) → zet goedgekeurde items in `NEXT_STEPS.md` (≥ 3 open, prioriteit) en meldt afwijzing met reden.
3. Uitvoerder voert uit (PREREG eerst) → RUNLOG → push. Bij bevinding: Strateeg (ideeën) en Manager (kwaliteit) reageren.
4. Manager rapporteert aan Sandro (kort) en escaleert alleen beslissingen die van Sandro zijn.
5. Auditor (op afroep) controleert kandidaten vóór er echt geld of een challenge-fee aan te pas komt.

## Bestandseigendom (voorkomt merge-conflicten; ieder eigen branch)
- Manager: `claude/vibrant-volta-ysy5m4` (`NEXT_STEPS.md`, `EINDVERSLAG.md`, `COORDINATION.md`, `ORGANISATIE.md`, `SUPERVISOR_LOG.md`, `EVALUATIE_*.md`)
- Strateeg: eigen branch (auto-toegewezen `claude/…`): `STRATEGIE_PLAN.md`, `STRATEGIE_LOG.md`, `VOORSTEL_S*.md`
- Uitvoerder: `main` (alles onder results/, RUNLOG, PREREG, verslagen). De uitvoerder-check (`check_next_steps.sh`, */10) leest alle remote branches.

## Ritme
- Uitvoerder: */10-check, werkt continu.
- Manager: elke 30 min (twee routines: :05 en :35 Amsterdam; routines kunnen niet vaker dan 1×/uur).
- Strateeg: elke 30 min (twee routines :20 en :50 Amsterdam in zijn eigen chat) + op verzoek. Bij geen nieuws: één logregel, geen actie.

## Regels (voor iedereen)
- PREREG vóór resultaat; TRIAL_COUNT bijwerken; t ≥ 3 in train én test (families met veel kandidaten t ≥ 3,5); geen grids.
- Geen omzeilen van beperkingen van websites/APIs; geen gokgedrag/loterijconstructies (FTMO-voorwaarden); geen echte-geld-acties zonder Sandro.
- Elk resultaat: SR na kosten, correlatie met bestaande sleeves, dip-profiel (dagverlies/dip), scheefheid.
- Doel-lat (Q1/Q1b/R3): elke-dag-vlak + positief-scheef → SR ≈ 1 nodig; overnight/negatief-scheef → SR 3–4. Zoek daarom dagelijks-vlakke, positief-scheve, kosten-lage strategieën.


## Aanvulling 2026-09-30 10:43 — CEO-rol en beslissingsproces
- **CEO (nieuwe Claude-chat, eigen branch)** beslist over alles wat de Manager/Strateeg/Uitvoerder aan vragen, blokkades en trade-offs hebben, met als mandaat: sneller, slimmer, beter. Sandro beslist niet meer mee, tenzij de CEO iets in \`SANDRO_ACTIES.md\` zet (handmatige acties, geld, accounts, juridisch).
- **Bestanden:** \`VRAGEN_MANAGER.md\` (Manager), \`VRAGEN_STRATEEG.md\` (Strateeg), \`VRAGEN_UITVOERDER.md\` (Uitvoerder, in RUNLOG-branch main) → CEO beantwoordt in \`BESLUITEN.md\` en beheert \`SANDRO_ACTIES.md\`. IDs: M-nnn, S-nnn, U-nnn; besluit-ID D-nnn met verwijzing.
- **Nooit wachten:** elke vraag heeft een *standaardactie*; na 60 minuten zonder besluit voert de vragensteller die uit en gaat door. Een besluit kan een standaardactie later terugdraaien.
- **Ritme (Amsterdam):** Manager :05/:35 · CEO :10/:40 · Strateeg :20/:50 · Uitvoerder */10.
- **Harde grenzen (CEO mag niet zelf):** echt geld/betalingen, echte accounts of trades, accounts op Sandro's naam aanmaken, omzeilen van ToS/beperkingen van sites/APIs, FTMO-voorwaarden schenden. Dit gaat via \`SANDRO_ACTIES.md\`. Projectniveau-beslissingen (stoppen/doel wijzigen) mag de CEO nemen, maar hij **meldt** ze aan Sandro (geen toestemming vragen); Sandro kan altijd overrulen.


## Aanvulling 2026-09-30 13:07 — CEO_MANDAAT bindend (D-031)
Rolverdeling volgens `CEO_MANDAAT.md` (CEO-branch): alleen Sandro beslist over stoppen/bevriezen/geld/echte trades; CEO beslist operationeel/strategisch; Manager = uitvoerend COO + QA (mag schriftelijk blokkeren op methodische gronden, wijzigt/verscherpt/vertraagt geen CEO-besluiten); Strateeg = richting/catalogus/voorstellen; Uitvoerder = werkstromen D/R/F. Programma: `PROGRAMMA_FASE2.md`.
