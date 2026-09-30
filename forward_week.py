"""Wekelijks forward-verslag (NEXT_STEPS v7, L5). Draait maandag 22:45 UTC via cron na forward_paper.py.
Voegt een blok toe aan forward/weekrapport.md en pusht. Regels/alarmen volgens forward/README.md (K2)."""
import csv, math, os, statistics, subprocess
from datetime import date, datetime, timedelta, timezone
DIR = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(DIR, "forward")
S = 80000.0

def main():
    p = os.path.join(F, "paper_daily.csv")
    rows = list(csv.DictReader(open(p), delimiter=";")) if os.path.exists(p) else []
    today = datetime.now(timezone.utc).date()
    lines = [f"\n## Week t/m {today} (automatisch)"]
    if not rows:
        lines.append("- Nog geen verwerkte forward-dagen (cron-log: forward/cron.log).")
    else:
        d0 = datetime.strptime(rows[0]["date"], "%Y.%m.%d").date(); d1 = datetime.strptime(rows[-1]["date"], "%Y.%m.%d").date()
        seen = {r["date"] for r in rows}
        missing = [d for d in (d0 + timedelta(n) for n in range((d1 - d0).days + 1)) if d.weekday() < 5 and d.strftime("%Y.%m.%d") not in seen]
        eq = [float(r["end_equity"]) for r in rows]; st = [float(r["start_equity"]) for r in rows]
        rets = [e / s - 1 for e, s in zip(eq, st)]
        peak, dd, worst = S, 0.0, 0.0
        for r in rows:
            peak = max(peak, float(r["end_equity"])); dd = max(dd, 1 - float(r["min_equity"]) / peak)
            worst = max(worst, (float(r["start_balance"]) - float(r["min_equity"])) / S)
        n = len(rets); months = n / 21
        sr = statistics.mean(rets) / statistics.stdev(rets) * math.sqrt(252) if n > 2 and statistics.stdev(rets) > 0 else float("nan")
        se = math.sqrt(252 / n) if n > 2 else float("nan")
        orb = []
        tp = os.path.join(F, "paper_trades.csv")
        if os.path.exists(tp):
            for r in csv.DictReader(open(tp), delimiter=";"):
                if r["leg"] == "ORB" and r["detail"].endswith(")"):
                    orb.append(float(r["detail"].split(" bp")[0]))
        lines += [f"- Dagen {n} ({d0} t/m {d1}); equity €{eq[-1]:,.2f} (P&L €{eq[-1]-S:+,.2f}); ≈ €{(eq[-1]-S)/max(months,1e-9):,.0f}/mnd",
                  f"- Geschatte jaarlijkse SR {sr:+.2f} (± {se:.2f} 1 SE — bij < 6 maanden statistisch vrijwel zonder betekenis, zie K2)",
                  f"- ORB: {len(orb)} trades, gemiddeld {statistics.mean(orb) if orb else float('nan'):+.2f} bp/trade (backtest +1,7 bp)",
                  f"- Slechtste FTMO-dagverlies {worst*100:.2f}%, max DD {dd*100:.2f}%",
                  f"- Alarm (K2-regel 1): {'JA — review nodig' if worst >= 0.04 or dd >= 0.08 else 'nee'}",
                  f"- Ontbrekende werkdagen (cron-gaten of beursvrije dagen): {', '.join(map(str, missing)) if missing else 'geen'}",
                  "- Aannames: slot-tot-slot voor RSI (geen intraday-dip), geen slippage, geen EUR-conversie → optimistisch."]
    path = os.path.join(F, "weekrapport.md")
    if not os.path.exists(path):
        open(path, "w").write("# Forward-weekrapport (papieren test, zie forward/README.md)\n")
    open(path, "a").write("\n".join(lines) + "\n")
    subprocess.run(["git", "-C", DIR, "add", "forward/weekrapport.md"], check=False)
    subprocess.run(["git", "-C", DIR, "commit", "-q", "-m", f"forward: weekrapport {today}", "-m", "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"], check=False)
    subprocess.run(["git", "-C", DIR, "push", "-q", "origin", "HEAD:main"], check=False)

if __name__ == "__main__":
    main()
