# Team-chat op de Debian-server (3 chats: CEO, Manager, Strateeg) — ~10 minuten

**Hoe het werkt:** de website (Python, geen extra pakketten) schrijft jouw bericht naar `chat/inbox.txt` op de branch van de rol
(via de GitHub-API) en leest de antwoorden uit `chat/outbox.txt` op diezelfde branch. Elke rol leest bij zijn eigen cyclus
(elke 30 min) zijn inbox en schrijft het antwoord in zijn outbox. Jij ziet het binnen 5 sec op de site.

| Chat | Branch | Bestanden |
|---|---|---|
| CEO | `claude/upbeat-dirac-g2810q` | `chat/inbox.txt`, `chat/outbox.txt` |
| Manager | `claude/vibrant-volta-ysy5m4` | idem |
| Strateeg | `claude/trusting-faraday-34tsmg` | idem |

## Stappen op de Debian-server
```bash
cd ~/ai-trading
git fetch origin
git checkout origin/claude/vibrant-volta-ysy5m4 -- chatweb CHAT_PROTOCOL.md     # haalt alleen deze map/bestand op
gh auth status                                                                    # moet ingelogd zijn (de agent pusht ook zo)
sudo CHAT_PASSWORD='kies-een-lang-wachtwoord-van-16+-tekens' bash chatweb/install.sh
```
De installatie maakt een systemd-service (start bij reboot, herstart bij crash) op poort **8080**.
Open daarna `http://<server-ip>:8080` (gebruiker `sandro`, jouw wachtwoord).

**Poort openzetten** (kies wat past):
- UFW op de server: `sudo ufw allow from <jouw-ip> to any port 8080 proto tcp`
- Google Cloud VM: `gcloud compute firewall-rules create chat-8080 --allow tcp:8080 --source-ranges <jouw-ip>/32`
- Geen vast IP? Gebruik een SSH-tunnel: `ssh -L 8080:localhost:8080 user@server` en ga naar `http://localhost:8080`.

## Token
De server gebruikt de GitHub-login van de server (`gh auth token`, of zet `GITHUB_TOKEN`). Deze moet **schrijven** mogen naar de repo
(contents: read/write). Bij het opstarten controleert de server dit en meldt het.

## Veiligheid (belangrijk)
- Wie de site kan bereiken en het wachtwoord kent, kan de rollen opdrachten geven. Gebruik een **lang wachtwoord** en beperk de poort tot **jouw IP**.
- Basic-auth over http stuurt het wachtwoord onversleuteld; met een IP-beperking of SSH-tunnel is dat acceptabel. Voor https: zet Caddy ervoor (`caddy reverse-proxy --from jouwdomein --to localhost:8080`).

## Sneller antwoord (optioneel): laat de rol direct draaien
Standaard antwoordt een rol pas bij zijn volgende cyclus (≤ 30 min). Wil je meteen? Elke routine kan een **API-trigger** krijgen:
1. claude.ai/code/routines → open de routine (bijv. "CEO-cyclus :10") → Edit → *Add another trigger* → **API** → kopieer routine-ID (`trig_…`) → *Generate token* (eenmalig zichtbaar).
2. Zet in `/etc/chat-web.env`: `CHAT_FIRE_CEO=trig_xxx:sk-ant-oat01-…` (idem `CHAT_FIRE_MANAGER`, `CHAT_FIRE_STRATEEG`) en `sudo systemctl restart chat-web`.
3. De site 'schopt' dan na elk bericht de routine (`POST …/routines/<id>/fire`). Let op: onzeker of de run in de bestaande sessie of een nieuwe sessie start (doc: "starts a new session"); test één keer. Limiet 30 fires/uur per routine.

## Beheer
`sudo systemctl status chat-web` · `journalctl -u chat-web -f` · wachtwoord wijzigen: `/etc/chat-web.env` aanpassen + `sudo systemctl restart chat-web`.
