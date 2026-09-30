"""N5: onafhankelijke herimplementatie van de RSI(2)-kern en trade-voor-trade-vergelijking (PREREG_N5.md).
Deze code importeert voor de BEREKENING geen eigen simulatoren; e1/k1 worden alleen geïmporteerd om te VERGELIJKEN."""
import csv
from datetime import date, datetime, timedelta


# ---------- onafhankelijke kern ----------
def wilder_rsi(closes, n=2):
    out = [None] * len(closes)
    if len(closes) <= n:
        return out
    gains = [max(closes[i] - closes[i - 1], 0.0) for i in range(1, n + 1)]
    losses = [max(closes[i - 1] - closes[i], 0.0) for i in range(1, n + 1)]
    ag, al = sum(gains) / n, sum(losses) / n
    out[n] = 100.0 if al == 0 else 100.0 - 100.0 / (1.0 + ag / al)
    for i in range(n + 1, len(closes)):
        ch = closes[i] - closes[i - 1]
        ag = (ag * (n - 1) + max(ch, 0.0)) / n
        al = (al * (n - 1) + max(-ch, 0.0)) / n
        out[i] = 100.0 if al == 0 else 100.0 - 100.0 / (1.0 + ag / al)
    return out


def sma_incl(closes, n=200):
    out, s = [None] * len(closes), 0.0
    for i, c in enumerate(closes):
        s += c
        if i >= n:
            s -= closes[i - n]
        if i >= n - 1:
            out[i] = s / n
    return out


def trades(dates, opens, closes, mode, start=None):
    """mode 'orig': uitstap slot eerste dag RSI>70; 'max1': uitstap open volgende dag. Retourneert (instap, uitstap, bruto)."""
    rsi, sma = wilder_rsi(closes), sma_incl(closes)
    out, i = [], 0
    while i < len(closes) - 1:
        sig = rsi[i] is not None and sma[i] is not None and rsi[i] < 10 and closes[i] > sma[i]
        if sig and (start is None or dates[i] >= start):
            if mode == "max1":
                out.append((dates[i], dates[i + 1], opens[i + 1] / closes[i] - 1))
                i += 1
                continue
            j = next((k for k in range(i + 1, len(closes)) if rsi[k] is not None and rsi[k] > 70), None)
            if j is None:
                break
            out.append((dates[i], dates[j], closes[j] / closes[i] - 1))
            i = j + 1
            continue
        i += 1
    return out


# ---------- data ----------
def ftmo_d1(sym):
    rows = sorted((datetime.strptime(r["date"], "%Y.%m.%d").date(), float(r["close"]))
                  for r in csv.DictReader(open(f"{sym}_rates.csv"), delimiter=";"))
    return [d for d, _ in rows], [c for _, c in rows]


def yahoo_ohlc(name):
    rows = [(datetime.strptime(r["date"], "%Y.%m.%d").date(), float(r["open"]), float(r["close"]))
            for r in csv.DictReader(open(f"data/ohlc/{name}.csv"), delimiter=";")]
    rows = [x for x in rows if x[0].year >= 1990]
    return [x[0] for x in rows], [x[1] for x in rows], [x[2] for x in rows]


def compare(label, mine, ref, tol=1e-9):
    """vergelijk lijsten (instap, uitstap, rendement)"""
    a = {(x[0], x[1]): x[2] for x in mine}
    b = {(x[0], x[1]): x[2] for x in ref}
    common = set(a) & set(b)
    diff_ret = [k for k in common if abs(a[k] - b[k]) > tol]
    only_a, only_b = sorted(set(a) - set(b)), sorted(set(b) - set(a))
    pct = len(common) / max(len(a), len(b)) * 100 if (a or b) else 100
    print(f"  {label:<34} mijn {len(a):>4} | ref {len(b):>4} | gelijk {len(common):>4} ({pct:.1f}%) | "
          f"rendement-afwijking {len(diff_ret)} | alleen mijn {len(only_a)} | alleen ref {len(only_b)}")
    return only_a[:3], only_b[:3]


def main():
    import e1_rsi2_ftmo as e1           # alleen ter vergelijking
    import k1_nights as k1
    from b2_sim import rsi2 as ref_rsi2
    print("(1) RSI-definitie: klassieke Wilder-seed vs b2_sim.rsi2 (seed = eerste verandering) — verschil na opwarming:")
    d, c = ftmo_d1("US500cash")
    mine, ref = wilder_rsi(c), ref_rsi2(c)
    diffs = [abs(mine[i] - ref[i]) for i in range(10, len(c)) if mine[i] is not None and ref[i] is not None]
    print(f"    max |Δ RSI| vanaf bar 10: {max(diffs):.2e} (Wilder n=2 vergeet de seed na enkele bars)")
    print("(2) Trade-voor-trade, oorspronkelijke uitstap (RSI>70), FTMO-D1 2021–2026, vs e1-logica:")
    for sym in e1.SWAP_LONG:
        d, c = ftmo_d1(sym)
        mine = [t for t in trades(d, c, c, "orig") if t[0] >= e1.LO]
        # referentie: e1-toestandsmachine opnieuw uitgelezen als trades
        rs = ref_rsi2(c)
        sma = [sum(c[i - 199:i + 1]) / 200 if i >= 199 else None for i in range(len(c))]
        ref, inpos, ent = [], False, None
        for i in range(1, len(c)):
            if inpos and rs[i] is not None and rs[i] > 70:
                ref.append((d[ent], d[i], c[i] / c[ent] - 1)); inpos = False
            elif not inpos and rs[i] is not None and sma[i] and rs[i] < 10 and c[i] > sma[i]:
                inpos, ent = True, i
        ref = [t for t in ref if t[0] >= e1.LO]
        oa, ob = compare(sym, mine, ref)
        if oa or ob:
            print(f"      voorbeelden alleen-mijn {oa} | alleen-ref {ob}")
    print("(3) Max 1 nacht, Yahoo (SPY/QQQ/GLD/DAX/N225), bruto (zonder kosten) vs k1-logica:")
    for name in ("SPY", "QQQ", "GLD", "DAX", "N225"):
        d, o, c = yahoo_ohlc(name)
        mine = trades(d, o, c, "max1")
        _, var = k1.analyse(list(zip(d, o, c)), lambda i: 0.0, lambda k: 0.0, lambda dd, n: 0.0)
        ref = [(x[0], None, x[1]) for x in var["a"]]
        mine2 = [(x[0], None, x[2]) for x in mine]
        compare(name, mine2, ref, tol=1e-9)
    print("(4) Swap: FTMO swap_rollover3days = 5 (vrijdag, zie mt5_swap_specs/SymbolInfoDump). Python rekent kalendernachten:")
    print("    vrijdag→maandag = 3 nachten in beide methoden; totaal per trade identiek, alleen het boekmoment verschilt.")
    print("(5) EA RSI2Sleeve: CopyBuffer(h, 0, 1, 1) en iClose(s, D1, 1) → uitsluitend de laatst afgesloten D1-bar (bar 1).")
    print("(6) Stop-fills: b4_sim vult stops op de stopprijs of de slechtere bar-open (gaps); MT5-tester vult op de exacte")
    print("    stopprijs zonder slippage → beide optimistisch bij snelle markten; G1 (+1 punt slippage) kwantificeert dit.")


if __name__ == "__main__":
    main()
