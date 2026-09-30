"""I3: event-lijst bouwen + verifiëren (FOMC/NFP/CPI) en event-drift testen, exact volgens PREREG_I3.md."""
import math
import statistics
from collections import defaultdict
from datetime import date, datetime, timedelta

from b4_sim import NY, load

FOMC = """2021-01-27 2021-03-17 2021-04-28 2021-06-16 2021-07-28 2021-09-22 2021-11-03 2021-12-15 2022-01-26 2022-03-16
2022-05-04 2022-06-15 2022-07-27 2022-09-21 2022-11-02 2022-12-14 2023-02-01 2023-03-22 2023-05-03 2023-06-14 2023-07-26
2023-09-20 2023-11-01 2023-12-13 2024-01-31 2024-03-20 2024-05-01 2024-06-12 2024-07-31 2024-09-18 2024-11-07 2024-12-18
2025-01-29 2025-03-19 2025-05-07 2025-06-18 2025-07-30 2025-09-17 2025-10-29 2025-12-10 2026-01-28 2026-03-18 2026-04-29
2026-06-17 2026-07-29 2026-09-16""".split()
NFP = """2021-02-05 2021-03-05 2021-04-02 2021-05-07 2021-06-04 2021-07-02 2021-08-06 2021-10-08 2021-11-05 2021-12-03 2022-01-07
2022-02-04 2022-03-04 2022-04-01 2022-05-06 2022-06-03 2022-07-08 2022-08-05 2022-09-02 2022-10-07 2022-11-04 2022-12-02
2023-01-06 2023-02-03 2023-03-10 2023-04-07 2023-05-05 2023-06-02 2023-07-07 2023-08-04 2023-09-01 2023-10-06 2023-11-03
2023-12-08 2024-01-05 2024-02-02 2024-03-08 2024-04-05 2024-05-03 2024-06-07 2024-07-05 2024-08-02 2024-09-06 2024-10-04
2024-11-01 2024-12-06 2025-01-09 2025-02-07 2025-03-07 2025-04-04 2025-05-02 2025-06-06 2025-07-03 2025-08-01 2025-09-05
2025-11-20 2025-12-16 2026-01-09 2026-02-11 2026-03-06 2026-04-03 2026-05-08 2026-06-05 2026-07-02 2026-08-07 2026-09-04""".split()
CPI = """2021-02-10 2021-03-10 2021-04-13 2021-05-12 2021-06-10 2021-07-13 2021-08-11 2021-09-14 2021-10-13 2021-11-10 2021-12-10
2022-01-12 2022-02-10 2022-03-10 2022-04-12 2022-05-11 2022-06-10 2022-07-13 2022-08-10 2022-09-13 2022-10-13 2022-11-10
2022-12-13 2023-01-12 2023-02-14 2023-03-14 2023-04-12 2023-05-10 2023-06-13 2023-07-12 2023-08-10 2023-09-13 2023-10-12
2023-11-14 2023-12-12 2024-01-15 2024-02-13 2024-03-12 2024-04-10 2024-05-15 2024-06-12 2024-07-11 2024-08-14 2024-09-11
2024-10-10 2024-11-13 2024-12-11 2025-01-13 2025-02-12 2025-03-12 2025-04-10 2025-05-13 2025-06-11 2025-07-15 2025-08-12
2025-09-11 2025-10-24 2025-12-18 2026-01-13 2026-02-13 2026-03-11 2026-04-10 2026-05-12 2026-06-10 2026-07-14 2026-08-12
2026-09-11""".split()


def ny_bars(sym):
    """dict NY-datum -> {(uur, minuut): bar(o,h,l,c,spread)} op NY-tijd"""
    out = defaultdict(dict)
    for b in load(sym):
        t = b[0] - timedelta(hours=7)  # servertijd = NY + 7
        out[t.date()][(t.hour, t.minute)] = b[1:]
    return out


def verify(bars, candidates, kind):
    """bevestigt releasedatums via 08:30-bar-range ≥ 2× mediaan van 20 voorgaande niet-eventdagen"""
    days = sorted(d for d in bars if (8, 30) in bars[d])
    rng = {d: (bars[d][(8, 30)][1] - bars[d][(8, 30)][2]) / bars[d][(8, 30)][0] for d in days}
    cand = {date.fromisoformat(x) for x in candidates}

    def ratio(d):
        prev = [x for x in days if x < d and x not in cand][-20:]
        return rng[d] / statistics.median([rng[x] for x in prev]) if d in rng and len(prev) >= 10 else 0.0

    rows = []
    for c in sorted(cand):
        if ratio(c) >= 2:
            rows.append((c, kind, "bron, bevestigd"))
            continue
        k = days.index(min(days, key=lambda x: abs((x - c).days)))
        near = [d for d in days[max(0, k - 2):k + 3] if d != c and ratio(d) >= 2]
        if len(near) == 1:
            rows.append((near[0], kind, f"gecorrigeerd van {c}"))
        else:
            rows.append((c, kind, "NIET bevestigd — uitgesloten"))
    # maanden zonder datum
    months = {(d.year, d.month) for d, _, _ in rows}
    lo, hi = (0, 10) if kind == "NFP" else (7, 16)
    for y in range(2021, 2027):
        for m in range(1, 13):
            if (y, m) in months or date(y, m, 1) > max(days) or date(y, m, 1) < min(days):
                continue
            md = [d for d in days if d.year == y and d.month == m][lo:hi]
            hits = [d for d in md if ratio(d) >= 2 and d not in {r[0] for r in rows}]
            if len(hits) == 1:
                rows.append((hits[0], kind, "toegevoegd (maand ontbrak in bron)"))
    return rows


def pre_fomc(bars, fomc, sym_spread_mult=1.0):
    out = []
    days = sorted(bars)
    for f in fomc:
        if f not in bars or (13, 55) not in bars[f]:
            continue
        prev = [d for d in days if d < f and (15, 55) in bars[d]]
        if not prev:
            continue
        eb, xb = bars[prev[-1]][(15, 55)], bars[f][(13, 55)]
        entry, ex = eb[3], xb[3]
        nights = (f - prev[-1]).days
        out.append((f, (ex - entry) / entry - eb[4] / entry - 0.0495 * nights / 365))
    return out


def post_news(bars, dates, point):
    out = []
    for d in dates:
        b = bars.get(d, {})
        if (8, 30) not in b or (9, 0) not in b:
            continue
        o, h, l, c, sp = b[(8, 30)]
        if c == o:
            continue
        side = 1 if c > o else -1
        ex = b[(9, 0)][3]
        cost = 2 * (b[(8, 30)][4] if side > 0 else b[(9, 0)][4]) / c
        out.append((d, side * (ex - c) / c - cost))
    return out


def report(name, trades):
    x = [n for _, n in trades]
    t = statistics.mean(x) / statistics.stdev(x) * math.sqrt(len(x))
    h1 = [n for d, n in trades if d <= date(2023, 12, 31)]; h2 = [n for d, n in trades if d > date(2023, 12, 31)]
    ok = t >= 2.5 and statistics.mean(h1) * statistics.mean(h2) > 0 and statistics.mean(x) > 0
    print(f"{name:<34} N {len(x):>3} | {statistics.mean(x)*1e4:+.2f} bp | t {t:+.2f} | 2021–23 {statistics.mean(h1)*1e4:+.1f} bp (N {len(h1)}) | "
          f"2024–26 {statistics.mean(h2)*1e4:+.1f} bp (N {len(h2)}) → {'GESLAAGD' if ok else 'afgewezen'}")


def main():
    bars = {s: ny_bars(s) for s in ("US500cash", "US100cash")}
    # load() levert spread in prijs (punten × point), dus direct bruikbaar
    ev = [(date.fromisoformat(d), "FOMC", "bron (federalreserve.gov)") for d in FOMC]
    ev += verify(bars["US500cash"], NFP, "NFP") + verify(bars["US500cash"], CPI, "CPI")
    ev.sort()
    with open("events.csv", "w") as f:
        f.write("# bronnen: federalreserve.gov/monetarypolicy/fomccalendars.htm; bls.gov/bls/news-release/empsit.htm en cpi.htm "
                "(opgehaald 2026-09-30); NFP/CPI geverifieerd met US500-M5 08:30-ET-range (PREREG_I3)\ndate;event;status\n")
        for d, k, s in ev:
            f.write(f"{d};{k};{s}\n")
    for k in ("NFP", "CPI"):
        st_ = defaultdict(int)
        for d, kk, s in ev:
            if kk == k:
                st_[s.split(' ')[0]] += 1
        print(f"{k}: " + ", ".join(f"{a} {b}" for a, b in st_.items()))
    print("correcties:", [(str(d), k, s) for d, k, s in ev if "gecorrigeerd" in s or "toegevoegd" in s or "NIET" in s])
    fomc = [d for d, k, _ in ev if k == "FOMC"]
    news = [d for d, k, s in ev if k in ("NFP", "CPI") and "NIET" not in s]
    a, b = [], []
    for s in ("US500cash", "US100cash"):
        a += pre_fomc(bars[s], fomc)
        b += post_news(bars[s], news, None)
    report("(a) pre-FOMC-drift (US500+US100)", a)
    report("(b) post-nieuws-momentum 30 min", b)


if __name__ == "__main__":
    main()
