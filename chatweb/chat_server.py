#!/usr/bin/env python3
"""Simpele chat-website: 3 chats (CEO, Manager, Strateeg) die via GitHub-bestanden met de rollen praten.

Per rol (eigen branch):
  chat/inbox.txt   <- alleen deze webserver schrijft (jouw berichten)   regel: id<TAB>tijd<TAB>tekst
  chat/outbox.txt  <- alleen de rol schrijft (antwoorden)               regel: reply_to_id<TAB>tijd<TAB>rol<TAB>tekst
Alleen Python 3 standaardbibliotheek nodig. Auth: HTTP Basic (wachtwoord uit CHAT_PASSWORD).
"""
import base64, json, os, subprocess, threading, time, urllib.request, urllib.error, urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from datetime import datetime, timezone

REPO = os.environ.get("CHAT_REPO", "sancassino/ai-trading")
PORT = int(os.environ.get("CHAT_PORT", "8080"))
USER = os.environ.get("CHAT_USER", "sandro")
PASSWORD = os.environ.get("CHAT_PASSWORD", "")
ROLES = {
    "ceo":      {"label": "CEO",      "branch": os.environ.get("BRANCH_CEO", "claude/upbeat-dirac-g2810q")},
    "manager":  {"label": "Manager",  "branch": os.environ.get("BRANCH_MANAGER", "claude/vibrant-volta-ysy5m4")},
    "strateeg": {"label": "Strateeg", "branch": os.environ.get("BRANCH_STRATEEG", "claude/trusting-faraday-34tsmg")},
}
INBOX, OUTBOX = "chat/inbox.txt", "chat/outbox.txt"
API = "https://api.github.com"
_lock = threading.Lock()
_etag = {}      # (branch,path) -> (etag, text)


def get_token():
    t = os.environ.get("GITHUB_TOKEN")
    if t:
        return t.strip()
    for cmd in (["gh", "auth", "token"],):
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=10).stdout.strip()
            if out:
                return out
        except Exception:
            pass
    try:  # git credential helper (zoals de agent gebruikt om te pushen)
        p = subprocess.run(["git", "credential", "fill"], input="protocol=https\nhost=github.com\n\n",
                           capture_output=True, text=True, timeout=10)
        for line in p.stdout.splitlines():
            if line.startswith("password="):
                return line.split("=", 1)[1].strip()
    except Exception:
        pass
    raise RuntimeError("Geen GitHub-token gevonden (zet GITHUB_TOKEN of log in met 'gh auth login')")


def gh(method, path, body=None, raw=False, etag=None):
    url = f"{API}/repos/{REPO}/{path}"
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {get_token()}")
    req.add_header("Accept", "application/vnd.github.raw" if raw else "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "ai-trading-chat")
    if etag:
        req.add_header("If-None-Match", etag)
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        req.add_header("Content-Type", "application/json")
    return urllib.request.urlopen(req, data=data, timeout=20)


def read_file(branch, path):
    """Geeft (tekst, bestaat). Gebruikt ETag zodat 304's niet meetellen voor de rate limit."""
    key = (branch, path)
    etag = _etag.get(key, (None, ""))[0]
    try:
        with gh("GET", f"contents/{path}?ref={urllib.parse.quote(branch, safe='')}", raw=True, etag=etag) as r:
            text = r.read().decode("utf-8", "replace")
            _etag[key] = (r.headers.get("ETag"), text)
            return text, True
    except urllib.error.HTTPError as e:
        if e.code == 304:
            return _etag[key][1], True
        if e.code == 404:
            return "", False
        raise


def append_line(branch, path, line, message):
    """Voeg één regel toe aan een bestand op een branch via de GitHub Contents API (met retry op conflict)."""
    q = urllib.parse.quote(branch, safe='')
    for attempt in range(5):
        sha, text = None, ""
        try:
            with gh("GET", f"contents/{path}?ref={q}") as r:
                j = json.loads(r.read().decode())
                sha = j["sha"]
                text = base64.b64decode(j["content"]).decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise
        if text and not text.endswith("\n"):
            text += "\n"
        new = text + line + "\n"
        body = {"message": message, "content": base64.b64encode(new.encode()).decode(), "branch": branch}
        if sha:
            body["sha"] = sha
        try:
            with gh("PUT", f"contents/{path}", body=body):
                _etag.pop((branch, path), None)
                return True
        except urllib.error.HTTPError as e:
            if e.code in (409, 422) and attempt < 4:
                time.sleep(0.6 * (attempt + 1))
                continue
            raise
    return False


def esc(t):
    return t.replace("\\", "\\\\").replace("\r", "").replace("\n", "\\n").replace("\t", " ")


def unesc(t):
    out, i = [], 0
    while i < len(t):
        if t[i] == "\\" and i + 1 < len(t):
            out.append("\n" if t[i + 1] == "n" else t[i + 1])
            i += 2
        else:
            out.append(t[i]); i += 1
    return "".join(out)


def messages(role):
    b = ROLES[role]["branch"]
    inbox, _ = read_file(b, INBOX)
    outbox, _ = read_file(b, OUTBOX)
    msgs, answered = [], set()
    for ln in outbox.splitlines():
        p = ln.split("\t", 3)
        if len(p) == 4:
            msgs.append({"from": p[2] or ROLES[role]["label"], "time": p[1], "text": unesc(p[3]), "reply_to": p[0]})
            answered.add(p[0])
    for ln in inbox.splitlines():
        p = ln.split("\t", 2)
        if len(p) == 3:
            msgs.append({"from": "Sandro", "time": p[1], "text": unesc(p[2]), "id": p[0], "answered": p[0] in answered})
    msgs.sort(key=lambda m: m["time"])
    return msgs


def fire_role(role):
    """Optioneel: routine direct laten draaien (API-trigger). CHAT_FIRE_<ROL>=trig_xxx:token"""
    v = os.environ.get(f"CHAT_FIRE_{role.upper()}", "")
    if ":" not in v:
        return
    tid, tok = v.split(":", 1)
    req = urllib.request.Request(f"https://api.anthropic.com/v1/claude_code/routines/{tid}/fire", method="POST",
                                 data=json.dumps({"text": "chat-bericht in chat/inbox.txt"}).encode())
    for k, val in (("Authorization", f"Bearer {tok}"), ("anthropic-beta", "experimental-cc-routine-2026-04-01"),
                   ("anthropic-version", "2023-06-01"), ("Content-Type", "application/json")):
        req.add_header(k, val)
    try:
        urllib.request.urlopen(req, timeout=15).read()
    except Exception as e:
        print("fire mislukt:", role, e)


PAGE = """<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Team-chat</title><style>
body{font-family:system-ui,sans-serif;margin:0;background:#f4f5f7;color:#111}
header{background:#1f2937;color:#fff;padding:10px 14px;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
header b{margin-right:10px}
.tab{padding:7px 14px;border-radius:6px;background:#374151;color:#fff;cursor:pointer;border:0;font-size:15px}
.tab.on{background:#2563eb}
#log{height:calc(100vh - 170px);overflow:auto;padding:12px;max-width:900px;margin:auto}
.m{margin:8px 0;padding:8px 12px;border-radius:10px;max-width:80%;white-space:pre-wrap;word-wrap:break-word}
.me{background:#dbeafe;margin-left:auto}.bot{background:#fff;border:1px solid #e5e7eb}
.t{font-size:11px;color:#6b7280;margin-bottom:2px}.w{font-size:11px;color:#b45309}
form{position:fixed;bottom:0;left:0;right:0;background:#fff;border-top:1px solid #ddd;padding:10px;display:flex;gap:8px;max-width:900px;margin:auto}
textarea{flex:1;height:52px;font-size:15px;padding:6px}button.s{padding:0 22px;font-size:15px;background:#2563eb;color:#fff;border:0;border-radius:6px}
#st{font-size:12px;color:#9ca3af;margin-left:auto}
</style></head><body>
<header><b>Team-chat</b><span id="tabs"></span><span id="st"></span></header>
<div id="log"></div>
<form id="f"><textarea id="tx" placeholder="Typ je bericht (Enter = verstuur, Shift+Enter = nieuwe regel)"></textarea><button class="s">Stuur</button></form>
<script>
const roles=__ROLES__;let cur=localStorage.getItem('role')||'ceo';let last='';
function tabs(){const t=document.getElementById('tabs');t.innerHTML='';for(const k in roles){const b=document.createElement('button');b.className='tab'+(k==cur?' on':'');b.textContent=roles[k];b.onclick=()=>{cur=k;localStorage.setItem('role',k);last='';tabs();load()};t.appendChild(b)}}
async function load(){try{const r=await fetch('/api/messages?role='+cur);const j=await r.json();const s=JSON.stringify(j);document.getElementById('st').textContent='bijgewerkt '+new Date().toLocaleTimeString();if(s===last)return;last=s;const el=document.getElementById('log');const atEnd=el.scrollTop+el.clientHeight>=el.scrollHeight-40;el.innerHTML='';for(const m of j.messages){const d=document.createElement('div');d.className='m '+(m.from==='Sandro'?'me':'bot');const t=document.createElement('div');t.className='t';t.textContent=m.from+' · '+m.time.replace('T',' ').slice(0,16)+'Z';d.appendChild(t);d.appendChild(document.createTextNode(m.text));if(m.from==='Sandro'&&m.answered===false){const w=document.createElement('div');w.className='w';w.textContent='wacht op antwoord (rollen kijken ongeveer elke 30 min)';d.appendChild(w)}el.appendChild(d)}if(atEnd||el.children.length<3)el.scrollTop=el.scrollHeight}catch(e){document.getElementById('st').textContent='fout: '+e}}
document.getElementById('f').onsubmit=async e=>{e.preventDefault();const tx=document.getElementById('tx');const v=tx.value.trim();if(!v)return;tx.value='';await fetch('/api/send',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({role:cur,text:v})});last='';load()};
document.getElementById('tx').onkeydown=e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();document.getElementById('f').requestSubmit()}};
tabs();load();setInterval(load,5000);
</script></body></html>"""


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _auth(self):
        h = self.headers.get("Authorization", "")
        if h.startswith("Basic "):
            try:
                u, _, p = base64.b64decode(h[6:]).decode().partition(":")
                if u == USER and p == PASSWORD:
                    return True
            except Exception:
                pass
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Team-chat"')
        self.end_headers()
        return False

    def _send(self, code, body, ctype="application/json"):
        b = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if not self._auth():
            return
        u = urllib.parse.urlparse(self.path)
        if u.path == "/":
            page = PAGE.replace("__ROLES__", json.dumps({k: v["label"] for k, v in ROLES.items()}))
            return self._send(200, page, "text/html")
        if u.path == "/api/messages":
            role = urllib.parse.parse_qs(u.query).get("role", ["ceo"])[0]
            if role not in ROLES:
                return self._send(404, "{}")
            try:
                with _lock:
                    return self._send(200, json.dumps({"messages": messages(role)}))
            except Exception as e:
                return self._send(500, json.dumps({"error": str(e), "messages": []}))
        self._send(404, "{}")

    def do_POST(self):
        if not self._auth():
            return
        if self.path != "/api/send":
            return self._send(404, "{}")
        try:
            n = int(self.headers.get("Content-Length", "0"))
            j = json.loads(self.rfile.read(n).decode())
            role, text = j["role"], j["text"].strip()
            if role not in ROLES or not text or len(text) > 8000:
                return self._send(400, '{"error":"ongeldig"}')
            now = datetime.now(timezone.utc)
            line = f"{int(now.timestamp()*1000)}\t{now.strftime('%Y-%m-%dT%H:%M:%SZ')}\t{esc(text)}"
            with _lock:
                append_line(ROLES[role]["branch"], INBOX, line, f"chat: bericht van Sandro voor {ROLES[role]['label']}")
            threading.Thread(target=fire_role, args=(role,), daemon=True).start()
            self._send(200, '{"ok":true}')
        except Exception as e:
            self._send(500, json.dumps({"error": str(e)}))


if __name__ == "__main__":
    if not PASSWORD or len(PASSWORD) < 10:
        raise SystemExit("Zet CHAT_PASSWORD (minimaal 10 tekens) — de site staat op internet.")
    get_token()  # faalt vroeg als er geen token is
    try:  # controle: kan de token in de repo schrijven?
        with gh("GET", "") as r:
            info = json.loads(r.read().decode())
        if not info.get("permissions", {}).get("push"):
            raise SystemExit("Token heeft geen schrijfrechten (contents:write) op " + REPO)
        print("GitHub-token OK; schrijfrechten aanwezig")
    except urllib.error.HTTPError as e:
        raise SystemExit(f"GitHub-toegang mislukt ({e.code}); controleer token/repo {REPO}")
    print(f"Team-chat op poort {PORT}; repo {REPO}")
    ThreadingHTTPServer(("0.0.0.0", PORT), H).serve_forever()
