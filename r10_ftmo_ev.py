"""r10_ftmo_ev.py — FTMO-EV herbeoordeling catalogus-sleeves met CTO engine/ftmo.py.

Gebruikt de vectorized CTO-implementatie (restart=True, horizon=504 dagen = ~24 mnd).
Metriek: net_ev_monthly, p_pass_2, p_survive, exp_payout_monthly.
Vehikel: cfd (COSTS_FTMO.csv).

Scales getest: 0.25, 0.5, 1.0 + auto (p99-dagverlies ≤ 4%).
"""
import os
import sys
import numpy as np
from datetime import date

from engine.ftmo import ftmo_ev

SERIES_DIR = "results/R2/series"
START_DATE = date(2001, 1, 1)
START_DATE_SHORT = date(2015, 1, 1)

SHORTLIST = [
    ("C02_faber",        "basis", "cfd", START_DATE,       "maandelijks; indices CFD"),
    ("C52_allweather",   "basis", "cfd", START_DATE_SHORT, "wekelijks; SPY+IEF(❌)+GLD"),
    ("C52_allweather",   "lang",  "cfd", START_DATE,       "wekelijks; SPY+BOND10_SYN(❌)+GOLD_F"),
    ("C17_fomc_cycle",   "basis", "cfd", START_DATE_SHORT, "A4; FOMC-cyclus; SPX CFD"),
    ("C54_carver",       "basis", "cfd", START_DATE,       "multi-instrument; FX/goud/olie"),
    ("C54_carver",       "qa",    "cfd", START_DATE_SHORT, "multi-instrument 2015→"),
    ("C55_daa",          "basis", "cfd", START_DATE_SHORT, "DAA; ETFs (❌ FTMO)"),
    ("C44_krediet",      "basis", "cfd", START_DATE_SHORT, "krediet; N=17jr"),
    ("C16_halloween",    "basis", "cfd", START_DATE,       "seizoen; SPX/indices"),
    ("C33_trend_lowvol", "basis", "cfd", START_DATE,       "trend+vol; SPX"),
]


def load_total(path: str, start: date) -> np.ndarray:
    rets = []
    with open(path) as f:
        f.readline()
        for line in f:
            parts = line.strip().split(";")
            if not parts[0][:4].isdigit():
                continue
            d = date.fromisoformat(parts[0])
            if d < start:
                continue
            rets.append(float(parts[2]))  # 'total' kolom
    return np.array(rets, dtype=float)


def p99_daily_loss(rets: np.ndarray) -> float:
    losses = np.maximum(0.0, -rets)
    return float(np.percentile(losses, 99)) if len(losses) > 50 else float("nan")


def auto_scale(rets: np.ndarray, target: float = 0.04) -> float:
    p99 = p99_daily_loss(rets)
    if np.isnan(p99) or p99 <= 0:
        return float("nan")
    return min(1.0, target / p99)


def assess(rule, variant, vehicle, start, note, n_paths=10_000, seed=7):
    fname = f"{rule}__{variant}__{vehicle}.csv"
    path = os.path.join(SERIES_DIR, fname)
    if not os.path.exists(path):
        return {"rule": rule, "variant": variant, "note": note, "status": "geen_serie"}

    rets = load_total(path, start)
    n = len(rets)
    if n < 100:
        return {"rule": rule, "variant": variant, "note": note, "status": f"te_kort_N={n}"}

    yrs = n / 252.0
    sr = float(rets.mean() / rets.std() * np.sqrt(252)) if rets.std() > 0 else float("nan")
    maxDD = float(np.max(1 - np.cumprod(1 + rets) / np.maximum.accumulate(np.cumprod(1 + rets))))
    p99_dl = p99_daily_loss(rets)
    sc = auto_scale(rets)

    def run(scale):
        return ftmo_ev(rets, n_paths=n_paths, scale=scale, seed=seed)

    r1  = run(1.0)
    rh  = run(0.5)
    rq  = run(0.25)
    rsc = run(sc) if not np.isnan(sc) else {}

    return {
        "rule": rule, "variant": variant, "note": note,
        "start": str(start), "n_days": n, "years": round(yrs, 1),
        "SR_cfd": round(sr, 3),
        "maxDD_cfd": round(maxDD, 3),
        "p99_dl": round(p99_dl, 4),
        "auto_scale": round(sc, 3) if not np.isnan(sc) else "nan",

        "p_pass_2_1x":  round(r1.get("p_pass_2", float("nan")), 3),
        "net_ev_monthly_1x":  round(r1.get("net_ev_monthly", float("nan")), 0),
        "exp_ppm_1x": round(r1.get("exp_payout_monthly", float("nan")), 0),

        "p_pass_2_half": round(rh.get("p_pass_2", float("nan")), 3),
        "net_ev_monthly_half": round(rh.get("net_ev_monthly", float("nan")), 0),

        "p_pass_2_auto": round(rsc.get("p_pass_2", float("nan")), 3) if rsc else "nan",
        "net_ev_monthly_auto": round(rsc.get("net_ev_monthly", float("nan")), 0) if rsc else "nan",
        "exp_ppm_auto": round(rsc.get("exp_payout_monthly", float("nan")), 0) if rsc else "nan",
        "p_survive_auto": round(rsc.get("p_survive", float("nan")), 3) if rsc else "nan",

        "status": "ok"
    }


def write_report(results, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("# Run 10 — FTMO-EV herbeoordeling (CTO engine, restart=True, horizon=24mnd)\n\n")
        f.write(f"Datum: {date.today()} | CTO engine/ftmo.py | Bootstrap 10.000 paden, blok 21 d\n")
        f.write("Maatstaf: net_ev_monthly (netto €/mnd over 24-mnd horizon incl. restarts)\n")
        f.write("Verboden: scale > 4% p99-dagverlies als aanbeveling (D-016/D-085)\n\n")

        f.write("## Samenvatting: net_ev_monthly per sleeve\n\n")
        f.write("| Sleeve | N jr | SR(cfd) | maxDD | p99-dl | scale_auto | p_pass_2@auto | net_EV€/mnd@auto | exp_ppm@auto | p_survive@auto |\n")
        f.write("|--------|------|---------|-------|--------|-----------|--------------|-----------------|-------------|---------------|\n")
        for r in results:
            if r.get("status") != "ok":
                f.write(f"| {r['rule']}__{r['variant']} | — | — | — | — | — | — | {r.get('status','?')} | — | — |\n")
                continue
            f.write(
                f"| {r['rule']}__{r['variant']} "
                f"| {r['years']} "
                f"| {r['SR_cfd']} "
                f"| {r['maxDD_cfd']:.0%} "
                f"| {r['p99_dl']:.1%} "
                f"| {r['auto_scale']} "
                f"| {r['p_pass_2_auto']} "
                f"| {r['net_ev_monthly_auto']} "
                f"| {r['exp_ppm_auto']} "
                f"| {r['p_survive_auto']} "
                f"|\n"
            )

        f.write("\n## Detail: 3 scales (1×, 0.5×, auto)\n\n")
        f.write("| Sleeve | p_pass_2@1× | net_ev/mnd@1× | p_pass_2@0.5× | net_ev/mnd@0.5× | p_pass_2@auto | net_ev/mnd@auto |\n")
        f.write("|--------|------------|--------------|--------------|----------------|--------------|----------------|\n")
        for r in results:
            if r.get("status") != "ok":
                continue
            f.write(
                f"| {r['rule']}__{r['variant']} "
                f"| {r['p_pass_2_1x']} | €{r['net_ev_monthly_1x']} "
                f"| {r['p_pass_2_half']} | €{r['net_ev_monthly_half']} "
                f"| {r['p_pass_2_auto']} | €{r['net_ev_monthly_auto']} "
                f"|\n"
            )

        f.write("\n## Ranking (FTMO-uitvoerbaar; net_ev_monthly@auto, hoogste eerst)\n\n")
        ftmo_ok = [r for r in results if r.get("status") == "ok"]
        ranked = sorted(ftmo_ok, key=lambda r: (
            float(r["net_ev_monthly_auto"]) if r["net_ev_monthly_auto"] != "nan" else -9999
        ), reverse=True)
        for i, r in enumerate(ranked, 1):
            f.write(f"{i}. **{r['rule']}__{r['variant']}**: €{r['net_ev_monthly_auto']}/mnd "
                    f"(p_pass_2={r['p_pass_2_auto']}, SR={r['SR_cfd']}) — {r['note']}\n")

        f.write("\n## Methodische noot\n\n")
        f.write("- `restart=True`: bij breach betaalt de simulant opnieuw fee en start fase 1 opnieuw.\n")
        f.write("- `net_ev_monthly` = mean(cash − fees) / 24 mnd → vergelijkbaar over sleeves.\n")
        f.write("- `exp_payout_monthly` = mean(cash) / 24 mnd (bruto, excl. fee-aftrek).\n")
        f.write("- `auto_scale` = min(1.0, 4% / p99-dagverlies) — D-016/D-085 limiet.\n")
        f.write("- Negatieve `net_ev_monthly`: fee-kosten > verwachte uitbetalingen over horizon.\n")

    return path


def main():
    print("Run 10: FTMO-EV herbeoordeling (CTO engine, restart=True)")
    print("=" * 70)
    results = []
    for args in SHORTLIST:
        rule, variant = args[0], args[1]
        print(f"  {rule} {variant} ... ", end="", flush=True)
        r = assess(*args)
        results.append(r)
        if r.get("status") == "ok":
            print(f"ok | net_ev/mnd@auto={r['net_ev_monthly_auto']}, p_pass_2@auto={r['p_pass_2_auto']}")
        else:
            print(r.get("status", "?"))

    out = write_report(results, "results/R2/run10_ftmo_ev.md")
    print(f"\nRapport: {out}")
    return results


if __name__ == "__main__":
    main()
