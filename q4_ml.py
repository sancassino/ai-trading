"""Q4: LightGBM op M5-features met maandelijkse walk-forward + purging, exact volgens PREREG_Q4.md.
Gebruik: .venv/bin/python q4_ml.py [--permute N]"""
import math
import sys
from collections import defaultdict
from datetime import timedelta
from zoneinfo import ZoneInfo

import lightgbm as lgb
import numpy as np

from b4_sim import NY, SYMS, load

SYM4 = ["US500cash", "US100cash", "GER40cash", "XAUUSD"]
HORIZONS = [3, 6, 12]
PARAMS = dict(n_estimators=200, learning_rate=0.05, num_leaves=31, min_child_samples=200, subsample=0.8, subsample_freq=1,
              colsample_bytree=0.8, random_state=7, verbose=-1, n_jobs=2)
FEATS = ["r1", "r3", "r12", "r48", "rng_atr", "dist_hi", "dist_lo", "tod_s", "tod_c", "dow", "gap", "rsi2", "rsi14", "cross12", "sym"]


def rsi(c, n):
    out = np.full(len(c), np.nan)
    d = np.diff(c, prepend=c[0])
    g, l = np.maximum(d, 0), np.maximum(-d, 0)
    ag = al = None
    for i in range(1, len(c)):
        if ag is None:
            ag, al = g[i], l[i]
        else:
            ag = (ag * (n - 1) + g[i]) / n; al = (al * (n - 1) + l[i]) / n
        out[i] = 100.0 if al == 0 else 100 - 100 / (1 + ag / al)
    return out


def build(sym):
    tzname, (oh, om), (ch, cm), comm = SYMS[sym]
    tz = ZoneInfo(tzname)
    bars = load(sym)
    t_srv = [b[0] for b in bars]
    o = np.array([b[1] for b in bars]); h = np.array([b[2] for b in bars]); l = np.array([b[3] for b in bars])
    c = np.array([b[4] for b in bars]); sp = np.array([b[5] for b in bars])
    local = [(t - timedelta(hours=7)).replace(tzinfo=NY).astimezone(tz) for t in t_srv]
    mins = np.array([(x.hour * 60 + x.minute) - (oh * 60 + om) for x in local])
    sess_len = (ch * 60 + cm) - (oh * 60 + om)
    in_sess = (mins >= 0) & (mins < sess_len)
    day = np.array([x.date().toordinal() for x in local])
    n = len(c)
    lr = np.zeros(n); lr[1:] = np.log(c[1:] / c[:-1])
    cs = np.cumsum(lr)
    def back(k):
        out = np.full(n, np.nan); out[k:] = cs[k:] - cs[:-k]; return out
    tr = np.maximum(h - l, np.abs(np.r_[np.nan, c[:-1]] - h))
    atr = np.convolve(np.nan_to_num(tr), np.ones(48) / 48, mode="full")[:n]
    # dag-hoog/laag en gap binnen de sessie
    dhi = np.full(n, np.nan); dlo = np.full(n, np.nan); gap = np.full(n, np.nan)
    cur, hi_, lo_, open_, prev_close, last_close = None, None, None, None, None, None
    for i in range(n):
        if not in_sess[i]:
            continue
        if day[i] != cur:
            cur = day[i]; hi_, lo_, open_ = h[i], l[i], o[i]
            prev_close = last_close
        hi_ = max(hi_, h[i]); lo_ = min(lo_, l[i])
        dhi[i], dlo[i] = hi_, lo_
        gap[i] = open_ / prev_close - 1 if prev_close else np.nan
        last_close = c[i]
    dow = np.array([x.weekday() for x in local])
    f = {
        "r1": back(1), "r3": back(3), "r12": back(12), "r48": back(48),
        "rng_atr": (h - l) / np.where(atr > 0, atr, np.nan),
        "dist_hi": (dhi - c) / np.where(atr > 0, atr, np.nan), "dist_lo": (c - dlo) / np.where(atr > 0, atr, np.nan),
        "tod_s": np.sin(2 * np.pi * mins / max(sess_len, 1)), "tod_c": np.cos(2 * np.pi * mins / max(sess_len, 1)),
        "dow": dow.astype(float), "gap": gap, "rsi2": rsi(c, 2), "rsi14": rsi(c, 14),
    }
    return {"t": np.array(t_srv, dtype="datetime64[m]"), "c": c, "sp": sp, "in_sess": in_sess, "day": day, "mins": mins, "sess_len": sess_len,
            "f": f, "comm": comm, "month": np.array([x.year * 12 + x.month - 1 for x in local]), "cs": cs, "year": np.array([x.year for x in local])}


def cross_feature(data):
    """rendement laatste 12 bars van US500 (voor anderen) / GER40 (voor US500), op servertijd uitgelijnd"""
    for s, d in data.items():
        ref = data["GER40cash" if s == "US500cash" else "US500cash"]
        idx = np.searchsorted(ref["t"], d["t"], side="right") - 1
        r12 = np.full(len(ref["c"]), np.nan); r12[12:] = ref["cs"][12:] - ref["cs"][:-12]
        v = np.where(idx >= 0, r12[np.clip(idx, 0, None)], np.nan)
        # ouder dan 30 min = ontbrekend
        age = (d["t"] - ref["t"][np.clip(idx, 0, None)]).astype("timedelta64[m]").astype(float)
        d["f"]["cross12"] = np.where(age <= 30, v, np.nan)


def dataset(data, H):
    rows = []
    for k, (s, d) in enumerate(data.items()):
        n = len(d["c"])
        j = np.arange(n) + H
        valid = d["in_sess"] & (j < n)
        jj = np.clip(j, 0, n - 1)
        same = valid & (d["day"][jj] == d["day"]) & d["in_sess"][jj] & (d["mins"][jj] > d["mins"])
        y = np.where(same, d["c"][jj] / d["c"] - 1, np.nan)
        X = np.column_stack([d["f"][f] for f in FEATS[:-1]] + [np.full(n, k, float)])
        ok = same & np.isfinite(y) & np.all(np.isfinite(X[:, :13]), axis=1)
        idx = np.where(ok)[0]
        rows.append((s, idx, X[idx], y[idx], d["month"][idx], d))
    return rows


def walk_forward(rows, H, permute=False, seed=0):
    rng = np.random.default_rng(seed)
    X = np.vstack([r[2] for r in rows]); y = np.concatenate([r[3] for r in rows]); m = np.concatenate([r[4] for r in rows])
    src = np.concatenate([np.full(len(r[1]), k) for k, r in enumerate(rows)]); pos = np.concatenate([r[1] for r in rows])
    months = sorted(set(m.tolist()))
    first_test = 2022 * 12
    trades = []
    for tm in [x for x in months if x >= first_test]:
        tr_mask = (m >= tm - 6) & (m < tm)
        # purging: target-venster (H bars) mag niet in de testmaand vallen → laatste H rijen per bron vóór de testmaand eruit
        for k in range(len(rows)):
            sel = np.where(tr_mask & (src == k))[0]
            if len(sel) > H:
                tr_mask[sel[-H:]] = False
        te_mask = m == tm
        if tr_mask.sum() < 5000 or te_mask.sum() == 0:
            continue
        ytr = y[tr_mask].copy()
        if permute:
            rng.shuffle(ytr)
        model = lgb.LGBMRegressor(**PARAMS).fit(X[tr_mask], ytr, categorical_feature=[len(FEATS) - 1])
        ptr = model.predict(X[tr_mask]); hi, lo = np.percentile(ptr, 95), np.percentile(ptr, 5)
        pte = model.predict(X[te_mask])
        te_idx = np.where(te_mask)[0]
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
            cost = (d["sp"][i] if side > 0 else d["sp"][j]) / d["c"][i] + 2 * d["comm"]
            trades.append((int(d["year"][i]), gross - cost))
            busy[k] = j
    return trades, (model.booster_.feature_importance("gain") if trades else None)


def summarize(trades):
    x = np.array([t[1] for t in trades])
    t = x.mean() / x.std(ddof=1) * math.sqrt(len(x)) if len(x) > 2 else float("nan")
    yr = defaultdict(list)
    for y_, v in trades:
        yr[y_].append(v)
    return t, x.mean(), len(x), {k: (np.mean(v), len(v)) for k, v in sorted(yr.items())}


def main():
    perm_n = int(sys.argv[sys.argv.index("--permute") + 1]) if "--permute" in sys.argv else 100
    data = {s: build(s) for s in SYM4}
    cross_feature(data)
    for H in HORIZONS:
        rows = dataset(data, H)
        trades, imp = walk_forward(rows, H)
        t, mean, n, yr = summarize(trades)
        pos = sum(v[0] > 0 for v in yr.values())
        print(f"H={H} ({H*5} min): N {n} | netto {mean*1e4:+.2f} bp/trade | OOS t {t:+.2f} | jaren+ {pos}/{len(yr)} | "
              + " ".join(f"{y}:{v[0]*1e4:+.1f}({v[1]})" for y, v in yr.items()))
        if imp is not None:
            order = np.argsort(imp)[::-1][:6]
            print("    top-features (gain, laatste fold): " + ", ".join(f"{FEATS[i]}" for i in order))
        if t >= 3:
            ts = [summarize(walk_forward(rows, H, permute=True, seed=s)[0])[0] for s in range(perm_n)]
            p = (1 + sum(x >= t for x in ts)) / (1 + len(ts))
            print(f"    permutatietest ({perm_n}×): p = {p:.3f} → {'GESLAAGD' if p < 0.01 and pos >= 4 else 'afgewezen'}")
        else:
            print("    → afgewezen (OOS t < 3; permutatietest niet nodig volgens prereg)")


if __name__ == "__main__":
    main()
