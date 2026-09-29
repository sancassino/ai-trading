"""Walk-forward-validatie op de dagelijkse equity-logs van een set configs.

Per config worden maandrendementen afgeleid (equity bij de eerste dag van elke
maand), zodat compounding-verschillen tussen runs geen rol spelen. Daarna
rollende vensters: train = N maanden, test = de M maanden erna, stap S.
Per venster:
  - "keuze": de config met het hoogste train-rendement, gemeten op test;
  - "ensemble": gemiddelde van alle configs (geen keuze nodig);
  - rangcorrelatie train<->test tussen de configs.

Gebruik: python3 walk_forward.py "results/eur/EUR_t?_l?_r10_g0_e30_daily.csv" [--train 24 --test 6 --step 3]
Bedragen = gemiddeld maandrendement x ACCOUNT_START (default 80000).
"""
import argparse
import csv
import glob
import os
import statistics

START = float(os.environ.get("ACCOUNT_START", 80000))


def monthly_returns(path):
    first = {}
    last_eq = None
    for r in csv.DictReader(open(path, encoding="utf-8-sig"), delimiter=";"):
        if not r.get("date"):
            continue
        m = r["date"][:7]
        first.setdefault(m, float(r["start_equity"]))
        last_eq = float(r["end_equity"])
    months = sorted(first)
    rets = {}
    for i, m in enumerate(months):
        nxt = first[months[i + 1]] if i + 1 < len(months) else last_eq
        rets[m] = nxt / first[m] - 1
    return rets


def compound(rs):
    x = 1.0
    for r in rs:
        x *= 1 + r
    return x - 1


def spearman(a, b):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        out = [0] * len(v)
        for pos, i in enumerate(order):
            out[i] = pos
        return out
    ra, rb = rank(a), rank(b)
    n = len(a)
    return 1 - 6 * sum((x - y) ** 2 for x, y in zip(ra, rb)) / (n * (n * n - 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pattern", nargs="+")
    ap.add_argument("--train", type=int, default=24)
    ap.add_argument("--test", type=int, default=6)
    ap.add_argument("--step", type=int, default=3)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    files = sorted({f for p in a.pattern for f in glob.glob(p)})
    names = [os.path.basename(f).replace("_daily.csv", "") for f in files]
    data = [monthly_returns(f) for f in files]
    months = sorted(set.intersection(*[set(d) for d in data]))
    rows = []
    s = 0
    while s + a.train + a.test <= len(months):
        tr = months[s:s + a.train]
        te = months[s + a.train:s + a.train + a.test]
        tr_ret = [compound([d[m] for m in tr]) for d in data]
        te_ret = [compound([d[m] for m in te]) for d in data]
        best = max(range(len(files)), key=lambda i: tr_ret[i])
        ens = compound([statistics.mean(d[m] for d in data) for m in te])
        rows.append((te[0], te[-1], names[best], te_ret[best], ens, spearman(tr_ret, te_ret),
                     sum(x > 0 for x in te_ret) / len(te_ret)))
        s += a.step
    if not a.quiet:
        print(f"{len(files)} configs, {len(months)} maanden, train {a.train} / test {a.test} / stap {a.step}")
        print(f"{'test':<17}{'keuze (beste train)':<30}{'keuze':>8}{'ensemble':>9}{'rho':>6}{'%cfg+':>7}")
        for t0, t1, n, k, e, rho, pos in rows:
            print(f"{t0}..{t1:<8}{n:<30}{k*100:>7.1f}%{e*100:>8.1f}%{rho:>6.2f}{pos*100:>6.0f}%")
    k = [r[3] for r in rows]
    e = [r[4] for r in rows]
    per_month = lambda xs: statistics.mean(xs) / a.test * START
    print(f"SAMENVATTING ({len(rows)} vensters): keuze gem. {per_month(k):,.0f}/mnd, {sum(x > 0 for x in k)}/{len(k)} vensters+ | "
          f"ensemble gem. {per_month(e):,.0f}/mnd, {sum(x > 0 for x in e)}/{len(e)} vensters+ | "
          f"keuze>ensemble in {sum(x > y for x, y in zip(k, e))}/{len(k)} | gem. rho {statistics.mean(r[5] for r in rows):.2f}")


if __name__ == "__main__":
    main()
