# COORDINATION — werkafspraken supervisor (Cloud) ↔ uitvoerder (Debian)

Besluit Sandro 2026-09-29: doorgaan. Snelheid was het probleem: 2–3 acties per dag i.p.v. elk uur.

## Rolverdeling
- **Uitvoerder (Debian-agent):** voert taken uit de BACKLOG in `NEXT_STEPS.md` uit, in volgorde van prioriteit, zonder op de supervisor te wachten. Push na **elke** afgeronde taak (of elk uur, wat eerder is) met `log_run.sh`.
- **Supervisor (Cloud):** elk uur (vaste server-side routine, niet afhankelijk van de sessie): leest main, beoordeelt kritisch, repareert gaten in de test-opzet, houdt de BACKLOG gevuld (altijd ≥3 open taken), mag de strategie veranderen. Schrijft naar branch `claude/vibrant-volta-ysy5m4`.
- **Uitvoerder haalt NEXT_STEPS op** vanuit die branch: `git fetch origin claude/vibrant-volta-ysy5m4 && git show origin/claude/vibrant-volta-ysy5m4:NEXT_STEPS.md` (of merge de branch in main). Supervisor kan niet direct naar main pushen zonder botsing; uitvoerder merget de branch elk uur.

## Regels tegen stilstand
1. Nooit "wachten op supervisor" als er ≥1 open taak in de BACKLOG staat. Klaar met alles? Pak de eerstvolgende; lege backlog = noteer dat in RUNLOG en stel zelf 1 voorstel op (label `VOORSTEL`).
2. Taken zijn klein (≤60 min). Groter → splits en push tussentijds.
3. Python-eerst: nieuwe ideeën eerst snel in Python screenen (minuten), pas bij slagen naar MT5. MT5 is bevestiging, geen zoekmachine.
4. Pre-registratie vóór elke test (bestand `PREREG_*.md`, gecommit vóór resultaten). Geen parameters aanpassen na het zien van resultaten.
5. Elke run telt mee in `TRIAL_COUNT.md` (aantal geteste varianten) voor multiple-testing-correctie.
6. Bij een fout/bug in eigen tooling: melden in RUNLOG, corrigeren, herdraaien — niet stilzwijgend.

## Heartbeat
Beide partijen loggen: uitvoerder in `RUNLOG.md`, supervisor in `SUPERVISOR_LOG.md` (elk uur een regel, ook als er niets nieuws is). Ontbreekt een uur → dat is een signaal voor Sandro.

## Aanvulling 2026-09-30
- De uitvoerder bleek B1–B5 in 20 min af te ronden; backlog moet dus ≥ 6 uur werk bevatten. Bij lege backlog: pak de Reserve (D-lijst) / schrijf zelf `VOORSTEL_*.md` en ga door — niet wachten.
- `check_next_steps.sh` moet ook mijn branch `claude/vibrant-volta-ysy5m4` controleren (doet het al voor alle remote branches).

## Aanvulling 2026-09-30 ~07:40
Steady-state is opgeheven op verzoek van Sandro. Uitvoerder controleert NEXT_STEPS elke 10 minuten (cron */10) en pakt direct de volgende taak; backlog nooit leeg.

## Aanvulling 2026-09-30 10:15
Nieuwe rolverdeling: zie ORGANISATIE.md (Manager/Strateeg/Uitvoerder/Auditor). Manager-uurroutine gepauzeerd op verzoek van Sandro. Uitvoerder blijft */10 checken (alle remote branches).

## Aanvulling 2026-09-30 10:43
Vragen aan Sandro gaan niet meer rechtstreeks: Manager schrijft ze in VRAGEN_MANAGER.md, CEO beslist in BESLUITEN.md. Standaardactie na 60 min. Manager meldt Sandro alleen nog korte statusregels.
