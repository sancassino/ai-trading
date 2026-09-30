#!/bin/bash
# Installeert de team-chat als systemd-service op de Debian-server. Gebruik:
#   cd ~/ai-trading && git pull origin claude/vibrant-volta-ysy5m4   (of: git fetch && git checkout origin/claude/vibrant-volta-ysy5m4 -- chatweb CHAT_PROTOCOL.md)
#   sudo CHAT_PASSWORD='kies-een-lang-wachtwoord' bash chatweb/install.sh
set -e
[ -n "$CHAT_PASSWORD" ] || { echo "Zet CHAT_PASSWORD (min. 10 tekens)"; exit 1; }
DIR="$(cd "$(dirname "$0")" && pwd)"
RUN_USER="${SUDO_USER:-$USER}"
TOKEN="${GITHUB_TOKEN:-$(sudo -u "$RUN_USER" gh auth token 2>/dev/null || true)}"
cat > /etc/chat-web.env <<ENV
CHAT_PASSWORD=$CHAT_PASSWORD
CHAT_PORT=${CHAT_PORT:-8080}
GITHUB_TOKEN=$TOKEN
ENV
chmod 600 /etc/chat-web.env
cat > /etc/systemd/system/chat-web.service <<UNIT
[Unit]
Description=Team-chat (GitHub-gekoppeld)
After=network-online.target
[Service]
User=$RUN_USER
EnvironmentFile=/etc/chat-web.env
ExecStart=/usr/bin/python3 $DIR/chat_server.py
Restart=always
RestartSec=5
[Install]
WantedBy=multi-user.target
UNIT
systemctl daemon-reload
systemctl enable --now chat-web
sleep 2
systemctl --no-pager status chat-web | head -12
echo "Klaar: http://$(curl -s ifconfig.me 2>/dev/null || echo <server-ip>):${CHAT_PORT:-8080}  (gebruiker: sandro)"
