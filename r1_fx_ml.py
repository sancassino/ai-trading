"""R1: kosten per FX-paar + LightGBM walk-forward op 15 FX-/goudsymbolen, exact volgens PREREG_R1.md."""
import math
import sys
from collections import defaultdict
from datetime import timedelta
from zoneinfo import ZoneInfo

import lightgbm as lgb
import numpy as np

from b4_sim import NY, load
from q4_ml import PARAMS, rsi

SYMS = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF", "NZDUSD", "EURGBP", "EURJPY", "GBPJPY", "AUDJPY",
        "EURCHF", "EURAUD", "GBPAUD", "XAUUSD"]
TO_EUR = {"EUR": 1.0, "USD": 0.88, "GBP": 1.17, "AUD": 0.58, "NZD": 0.52, "CHF": 1.07, "CAD": 0.64, "JPY": 0.0059}
LON = ZoneInfo("Europe/London")
HORIZONS = [3, 6, 12]
FEATS = ["r1", "r3", "r12", "r48", "rng_atr", "dist_hi", "dist_lo", "tod_s", "tod_c", "dow", "rsi2", "rsi14", "usd12", "tri", "ref12", "sym"]


def comm_frac(sym, price):
    if sym == "XAUUSD":
        return 2.00 / (100 * price * TO_EUR["USD"])
    return 2.25 / (100000 * TO_EUR[sym[:3]])


def build(sym):
    bars = load(sym)
    t = np.array([b[0] for b in bars], dtype="datetime64[m]")
    o = np.array([b[1] for b in bars]); h = np.array([b[2] for b in bars]); l = np.array([b[3] for b in bars])
    c = np.array([b[4] for b in bars]); sp = np.array([b[5] for b in bars])
    local = [(b[0] - timedelta(hours=7)).replace(tzinfo=NY).astimezone(LON) for b in bars]
    mins = np.array([x.hour * 60 + x.minute - 7 * 60 for x in local])
    dow = np.array([x.weekday() for x in local])
    in_sess = (mins >= 0) & (mins < 600) & (dow < 5)
    day = np.array([x.date().toordinal() for x in local])
    n = len(c)
    cs = np.cumsum(np.r_[0.0, np.log(c[1:] / c[:-1])])
    def back(k):
        out = np.full(n, np.nan); out[k:] = cs[k:] - cs[:-k]; return out
    tr = np.maximum(h - l, np.abs(np.r_[np.nan, c[:-1]] - h))
    atr = np.convolve(np.nan_to_num(tr), np.ones(48) / 48, mode="full")[:n]
    dhi = np.full(n, np.nan); dlo = np.full(n, np.nan)
    cur = hi_ = lo_ = None
    for i in range(n):
        if not in_sess[i]:
            continue
        if day[i] != cur:
            cur, hi_, lo_ = day[i], h[i], l[i]
        hi_ = max(hi_, h[i]); lo_ = min(lo_, l[i]); dhi[i], dlo[i] = hi_, lo_
    atr_ = np.where(atr > 0, atr, np.nan)
    f = {"r1": back(1), "r3": back(3), "r12": back(12), "r48": back(48), "rng_atr": (h - l) / atr_,
         "dist_hi": (dhi - c) / atr_, "dist_lo": (c - dlo) / atr_, "tod_s": np.sin(2 * np.pi * mins / 600),
         "tod_c": np.cos(2 * np.pi * mins / 600), "dow": dow.astype(float), "rsi2": rsi(c, 2), "rsi14": rsi(c, 14)}
    return {"t": t, "c": c, "sp": sp, "in_sess": in_sess, "day": day, "mins": mins, "f": f, "cs": cs,
            "month": np.array([x.year * 12 + x.month - 1 for x in local]), "year": np.array([x.year for x in local]), "sym": sym}


def align(ref, t):
    idx = np.searchsorted(ref["t"], t, side="right") - 1
    ok = idx >= 0
    age = np.where(ok, (t - ref["t"][np.clip(idx, 0, None)]).astype(float), 1e9)
    return np.clip(idx, 0, None), ok & (age <= 15)


def cross(data):
    usd_legs = {"EURUSD": -1, "GBPUSD": -1, "AUDUSD": -1, "NZDUSD": -1, "USDJPY": 1, "USDCAD": 1, "USDCHF": 1}
    for s, d in data.items():
        n = len(d["c"]); acc = np.zeros(n); cnt = np.zeros(n)
        for u, sign in usd_legs.items():
            ref = data[u]; idx, ok = align(ref, d["t"])
            r12 = np.full(len(ref["c"]), np.nan); r12[12:] = ref["cs"][12:] - ref["cs"][:-12]
            v = np.where(ok, r12[idx], np.nan) * sign
            acc += np.nan_to_num(v); cnt += np.isfinite(v)
        d["f"]["usd12"] = np.where(cnt > 0, acc / np.maximum(cnt, 1), np.nan)
        vals = []
        for u in ("EURUSD", "USDJPY", "EURJPY"):
            idx, ok = align(data[u], d["t"]); vals.append(np.where(ok, np.log(data[u]["c"][idx]), np.nan))
        d["f"]["tri"] = (vals[0] + vals[1] - vals[2]) * 1e4
        refsym = "GBPUSD" if s == "EURUSD" else "EURUSD"
        ref = data[refsym]; idx, ok = align(ref, d["t"])
        r12 = np.full(len(ref["c"]), np.nan); r12[12:] = ref["cs"][12:] - ref["cs"][:-12]
        d["f"]["ref12"] = np.where(ok, r12[idx], np.nan)


def rows_for(data, H):
    rows = []
    for k, (s, d) in enumerate(data.items()):
        n = len(d["c"]); j = np.arange(n) + H; jj = np.clip(j, 0, n - 1)
        same = d["in_sess"] & (j < n) & (d["day"][jj] == d["day"]) & d["in_sess"][jj] & (d["mins"][jj] > d["mins"])
        y = np.where(same, d["c"][jj] / d["c"] - 1, np.nan)
        X = np.column_stack([d["f"][f] for f in FEATS[:-1]] + [np.full(n, k, float)])
        ok = same & np.isfinite(y) & np.all(np.isfinite(X[:, :12]), axis=1)
        idx = np.where(ok)[0]
        rows.append((s, idx, X[idx].astype(np.float32), y[idx], d["month"][idx], d))
    return rows


def walk(rows, H, permute=False, seed=0):
    rng = np.random.default_rng(seed)
    X = np.vstack([r[2] for r in rows]); y = np.concatenate([r[3] for r in rows]); m = np.concatenate([r[4] for r in rows])
    src = np.concatenate([np.full(len(r[1]), k) for k, r in enumerate(rows)]); pos = np.concatenate([r[1] for r in rows])
    trades = []
    for tm in sorted(x for x in set(m.tolist()) if x >= 2022 * 12):
        trm = (m >= tm - 6) & (m < tm)
        for k in range(len(rows)):
            sel = np.where(trm & (src == k))[0]
            if len(sel) > H:
                trm[sel[-H:]] = False
        tr_idx = np.where(trm)[0][::4]
        te_idx = np.where(m == tm)[0]
        if len(tr_idx) < 5000 or len(te_idx) == 0:
            continue
        ytr = y[tr_idx].copy()
        if permute:
            rng.shuffle(ytr)
        model = lgb.LGBMRegressor(**PARAMS).fit(X[tr_idx], ytr, categorical_feature=[len(FEATS) - 1])
        ptr = model.predict(X[tr_idx]); hi, lo = np.percentile(ptr, 95), np.percentile(ptr, 5)
        pte = model.predict(X[te_idx])
        busy = {}
        for q, p in zip(te_idx, pte):
            k = src[q]; i = pos[q]; d = rows[k][5]
            if i < busy.get(k, -1):
                continue
            side = 1 if p >= hi else (-1 if p <= lo else 0)
            if side == 0:
                continue
            j = i + H
            gross = side * (d["c"][j] / d["c"][i] - 1)
            cost = (d["sp"][i] if side > 0 else d["sp"][j]) / d["c"][i] + 2 * comm_frac(d["sym"], d["c"][i])
            trades.append((int(d["year"][i]), d["sym"], str(d["t"][i]), gross - cost))
            busy[k] = j
    return trades


def main():
    data = {s: build(s) for s in SYMS}
    print("Stap 1 — kosten per symbool in de modeluren (per kant, bp): mediane halve spread + commissie")
    for s, d in data.items():
        m = d["in_sess"]
        half = np.median(d["sp"][m] / d["c"][m]) / 2 * 1e4
        comm = comm_frac(s, float(np.median(d["c"][m]))) * 1e4
        print(f"  {s:<7} spread {2*half:.2f} bp (half {half:.2f}) + commissie {comm:.2f} → per kant {half+comm:.2f} bp {'< 0,8' if half+comm < 0.8 else ''}")
    cross(data)
    for H in HORIZONS:
        rows = rows_for(data, H)
        tr = walk(rows, H)
        x = np.array([t[3] for t in tr])
        tt = x.mean() / x.std(ddof=1) * math.sqrt(len(x))
        yr = defaultdict(list); sy = defaultdict(list); eff = len({t[2] for t in tr})
        for t in tr:
            yr[t[0]].append(t[3]); sy[t[1]].append(t[3])
        pos = sum(np.mean(v) > 0 for v in yr.values())
        daily = defaultdict(float)
        for t in tr:
            daily[t[2][:10]] += t[3] / len(SYMS)
        dv = np.array(list(daily.values())); sr = dv.mean() / dv.std() * math.sqrt(252) if len(dv) > 2 else float("nan")
        print(f"\nH={H} ({H*5} min): N {len(x)} (effectief {eff}) | netto {x.mean()*1e4:+.2f} bp | OOS t {tt:+.2f} | jaren+ {pos}/{len(yr)} | SR na kosten {sr:+.2f}")
        print("   per jaar: " + " ".join(f"{y}:{np.mean(v)*1e4:+.2f}({len(v)})" for y, v in sorted(yr.items())))
        print("   per symbool t: " + " ".join(f"{s}:{np.mean(v)/np.std(v, ddof=1)*math.sqrt(len(v)):+.1f}" for s, v in sy.items() if len(v) > 2))
        if tt >= 3 and pos >= 4:
            ts = []
            for sd in range(100):
                px = np.array([t[3] for t in walk(rows, H, permute=True, seed=sd)])
                ts.append(px.mean() / px.std(ddof=1) * math.sqrt(len(px)))
            p = (1 + sum(v >= tt for v in ts)) / 101
            print(f"   permutatietest: p = {p:.3f} → {'GESLAAGD' if p < 0.01 else 'afgewezen'}")
        else:
            print("   → afgewezen (OOS t < 3 of < 4/5 jaren positief)")


if __name__ == "__main__":
    main()
