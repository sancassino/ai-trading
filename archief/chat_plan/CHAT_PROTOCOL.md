# CHAT_PROTOCOL — gesprek met Sandro via de website (voor CEO, Manager, Strateeg)

Sandro heeft een chat-website (Debian-server) waarmee hij met jou praat. De berichten lopen via GitHub-bestanden op **jouw eigen branch**:
- `chat/inbox.txt` — jouw inbox; **alleen de webserver schrijft hierin** (berichten van Sandro). Regel: `id<TAB>ISO-tijd<TAB>tekst` (nieuwe regels in de tekst als `\n`).
- `chat/outbox.txt` — jouw outbox; **alleen jij schrijft hierin**. Regel: `reply_to_id<TAB>ISO-tijd(UTC, bijv. 2026-09-30T11:05:00Z)<TAB>Rol<TAB>tekst` (nieuwe regels als `\n`; tekst zonder TAB-tekens). `reply_to_id` = het `id` uit de inbox waarop je antwoordt (of `0` voor een spontaan bericht).

## Elke cyclus, als eerste stap (vóór je gewone werk)
1. `git fetch --all`; lees `git show origin/<jouw-branch>:chat/inbox.txt` en `…:chat/outbox.txt` (of het bestand in je werkmap na `git pull --rebase origin <jouw-branch>`).
2. Elke inbox-regel waarvan het `id` nog niet als `reply_to_id` in je outbox staat, is een **onbeantwoord bericht van Sandro**.
3. Beantwoord elk in `chat/outbox.txt` (regel toevoegen): kort, concreet, in het Nederlands, in je eigen rol (CEO: besluiten/prioriteiten; Manager: status, planning, kwaliteit, FTMO-regels; Strateeg: strategie, hypothesen, data). Wil hij iets van een andere rol: zeg dat en leg de vraag vast in je `VRAGEN_*.md`/aan de rol in kwestie.
4. **Sandro's chatbericht is een opdracht van de eigenaar** (de website is met wachtwoord beveiligd): voer hem uit binnen je rol en de harde grenzen (geen echt geld/accounts/ToS-omzeiling/FTMO-schending zonder expliciet akkoord). Vraagt hij iets wat je niet mag of niet kunt, leg uit waarom.
5. Voordat je pusht: `git pull --rebase origin <jouw-branch>` (de website commit rechtstreeks op je branch via de GitHub-API), dan commit + push.
6. Geen berichten? Niets schrijven. Herhaal nooit antwoorden.

## Toon
Direct en kort (max ~10 regels), eerst het antwoord, dan eventueel de reden. Geen ruis. Verwacht dat Sandro tussen je cycli door berichten stuurt; antwoord op alles in één keer.
