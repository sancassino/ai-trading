"""Samenvatting van een MomentumRotation-run op basis van deals + dagelijkse equity-log.

Gebruik: python3 analyze_daily.py results/plateau/PL_t2_l3_r10.csv [meer.csv ...]
Verwacht naast elk deals-bestand het bijbehorende *_daily.csv.

Drawdowns worden op DAGELIJKSE EQUITY (incl. zwevende verliezen) gemeten, niet
alleen op gesloten deals zoals dd_check.py deed. FTMO-dagverlies = daling van
de dag-minimum-equity t.o.v. de BALANCE bij dagstart, als % van het
startkapitaal -- FTMO-regel: equity moet boven (balance om 00:00 CE(S)T - 5%
van het startkapitaal) blijven, dus meegenomen zwevend verlies telt mee.
"""
import csv, os
import sys
from collections import defaultdict

START = float(os.environ.get("ACCOUNT_START", 100000))


def load_daily(path):
    rows = []
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f, delimiter=";"):
            if not r.get("date"):
                continue
            rows.append((r["date"], float(r["start_balance"]), float(r["start_equity"]),
                         float(r["min_equity"]), float(r["end_equity"])))
    return rows


def load_deals(path):
    out = []
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f, delimiter=";"):
            if r.get("close_time"):
                out.append((r["close_time"], r["symbol"], float(r["profit"])))
    return out


def summarize(deals_path):
    daily = load_daily(deals_path.replace(".csv", "_daily.csv"))
    deals = load_deals(deals_path)
    net = sum(p for _, _, p in deals)
    months = len(daily) / 21.0
    yearly = defaultdict(float)
    for d, _, p in deals:
        yearly[d[:4]] += p

    peak = START
    max_dd_peak = 0.0
    max_dd_static = 0.0
    worst_day = 0.0
    worst_day_date = None
    worst_strict = 0.0  # strengste lezing: referentie = max(balance, equity) om middernacht
    for d, sb, se, mn, en in daily:
        max_dd_static = max(max_dd_static, (START - mn) / START)
        max_dd_peak = max(max_dd_peak, (peak - mn) / peak)
        peak = max(peak, en)
        loss = (sb - mn) / START
        if loss > worst_day:
            worst_day, worst_day_date = loss, d
        worst_strict = max(worst_strict, (max(sb, se) - mn) / START)

    return {
        "file": deals_path.split("/")[-1],
        "net": net,
        "per_month": net / months if months else 0.0,
        "years_pos": sum(1 for v in yearly.values() if v > 0),
        "years": len(yearly),
        "yearly": dict(sorted(yearly.items())),
        "dd_peak": max_dd_peak,
        "dd_static": max_dd_static,
        "worst_day": worst_day,
        "worst_day_date": worst_day_date,
        "worst_strict": worst_strict,
        "trades": len(deals),
    }


if __name__ == "__main__":
    print(f"{'file':<22}{'net':>10}{'/mnd':>8}{'jaren+':>8}{'DDpeak':>8}{'DDstat':>8}{'dagDD':>7}{'streng':>7}  per jaar")
    for p in sys.argv[1:]:
        s = summarize(p)
        yrs = " ".join(f"{y[2:]}:{v/1000:+.1f}k" for y, v in s["yearly"].items())
        print(f"{s['file']:<22}{s['net']:>10,.0f}{s['per_month']:>8,.0f}{s['years_pos']:>5}/{s['years']:<2}"
              f"{s['dd_peak']*100:>7.1f}%{s['dd_static']*100:>7.1f}%{s['worst_day']*100:>6.1f}%{s['worst_strict']*100:>6.1f}%  {yrs}")
