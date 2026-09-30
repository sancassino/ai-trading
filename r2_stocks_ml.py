"""R2: LightGBM cross-sectioneel op 41 US-aandelen (M5, kwartier-raster), volgens PREREG_R2.md."""
import bisect
import math
from collections import defaultdict
from datetime import date, datetime, timedelta

import lightgbm as lgb
import numpy as np

from b4_sim import load
from q4_ml import PARAMS, rsi

SYMS = open("universe_us41.txt").read().strip().split(",")
COMM = 0.00002


def earnings_days():
    ev = defaultdict(list)
    for line in open("earnings.csv"):
        if line[0] in "#s":
            continue
        s, ts = line.strip().split(";")
        t = datetime.strptime(ts, "%Y-%m-%d %H:%M")
        d = t.date() + (timedelta(days=1) if t.hour >= 16 else timedelta(0))
        ev[s].append(d.toordinal())
    return {s: sorted(v) for s, v in ev.items()}


def build(sym, spx, ev):
    bars = load(sym)
    ny = [b[0] - timedelta(hours=7) for b in bars]
    day = np.array([t.date().toordinal() for t in ny])
    o = np.array([b[1] for b in bars]); h = np.array([b[2] for b in bars]); l = np.array([b[3] for b in bars])
    c = np.array([b[4] for b in bars]); sp = np.array([b[5] for b in bars])
    n = len(c)
    # sessie = alle bars van de NY-datum met ≥ 60 bars
    counts = defaultdict(int)
    for dd in day:
        counts[dd] += 1
    valid = np.array([counts[dd] >= 60 for dd in day])
    first = np.r_[True, day[1:] != day[:-1]]
    k_in_day = np.zeros(n, int); last_idx = np.zeros(n, int)
    start = 0
    for i in range(1, n + 1):
        if i == n or day[i] != day[i - 1]:
            k_in_day[start:i] = np.arange(i - start); last_idx[start:i] = i - 1; start = i
    cs = np.cumsum(np.r_[0.0, np.log(c[1:] / c[:-1])])
    def back(k):
        out = np.full(n, np.nan); out[k:] = cs[k:] - cs[:-k]; return out
    tr = np.maximum(h - l, np.abs(np.r_[np.nan, c[:-1]] - h))
    atr = np.convolve(np.nan_to_num(tr), np.ones(48) / 48, mode="full")[:n]; atr_ = np.where(atr > 0, atr, np.nan)
    dhi = np.maximum.accumulate(h); dlo = np.minimum.accumulate(l)  # per dag herstart hieronder
    dhi = h.copy(); dlo = l.copy(); dopen = o.copy(); gap = np.full(n, np.nan); prev_close = None
    for i in range(n):
        if first[i]:
            dopen[i] = o[i]; gap[i] = o[i] / prev_close - 1 if prev_close else np.nan
        else:
            dhi[i] = max(dhi[i - 1], h[i]); dlo[i] = min(dlo[i - 1], l[i]); dopen[i] = dopen[i - 1]; gap[i] = gap[i - 1]
        if i + 1 == n or day[i + 1] != day[i]:
            prev_close = c[i]
    dtd = np.log(c / dopen)
    # US500 op servertijd uitgelijnd
    st = np.array([b[0] for b in bars], dtype="datetime64[m]")
    idx = np.clip(np.searchsorted(spx["t"], st, side="right") - 1, 0, None)
    spx12 = spx["r12"][idx]; spxdtd = spx["dtd"][idx]
    e = ev.get(sym, [])
    def near(dd):
        j = bisect.bisect_left(e, dd)
        cand = [e[x] - dd for x in (j - 1, j) if 0 <= x < len(e)]
        return float(np.clip(min(cand, key=abs), -10, 10)) if cand else 10.0
    earn = np.array([near(dd) for dd in day])
    f = {"r1": back(1), "r3": back(3), "r12": back(12), "r48": back(48), "rng_atr": (h - l) / atr_,
         "dist_hi": (dhi - c) / atr_, "dist_lo": (c - dlo) / atr_, "tod_s": np.sin(2 * np.pi * k_in_day / 78),
         "tod_c": np.cos(2 * np.pi * k_in_day / 78), "dow": np.array([t.weekday() for t in ny], float), "gap": gap,
         "rsi2": rsi(c, 2), "rsi14": rsi(c, 14), "rs12": back(12) - spx12, "rsdtd": dtd - spxdtd, "earn": earn}
    grid = valid & (k_in_day % 3 == 0) & (k_in_day >= 3)
    return {"st": st, "c": c, "sp": sp, "day": day, "k": k_in_day, "last": last_idx, "f": f, "grid": grid,
            "month": np.array([t.year * 12 + t.month - 1 for t in ny]), "year": np.array([t.year for t in ny]), "sym": sym}


def spx_series():
    bars = load("US500cash")
    t = np.array([b[0] for b in bars], dtype="datetime64[m]"); c = np.array([b[4] for b in bars])
    ny = [b[0] - timedelta(hours=7) for b in bars]; day = np.array([x.date().toordinal() for x in ny])
    cs = np.cumsum(np.r_[0.0, np.log(c[1:] / c[:-1])]); r12 = np.full(len(c), np.nan); r12[12:] = cs[12:] - cs[:-12]
    dopen = c.copy()
    for i in range(1, len(c)):
        dopen[i] = dopen[i - 1] if day[i] == day[i - 1] else c[i]
    return {"t": t, "r12": r12, "dtd": np.log(c / dopen)}


FEATS = ["r1", "r3", "r12", "r48", "rng_atr", "dist_hi", "dist_lo", "tod_s", "tod_c", "dow", "gap", "rsi2", "rsi14", "rs12", "rsdtd", "earn", "rank12", "sym"]


def main():
    spx = spx_series(); ev = earnings_days()
    data = [build(s, spx, ev) for s in SYMS]
    # cross-sectionele rang van r12 per tijdstip (kwartier-raster)
    pool = defaultdict(list)
    for k, d in enumerate(data):
        for i in np.where(d["grid"])[0]:
            v = d["f"]["r12"][i]
            if np.isfinite(v):
                pool[d["st"][i]].append((v, k, i))
    for d in data:
        d["f"]["rank12"] = np.full(len(d["c"]), np.nan)
    for t, lst in pool.items():
        lst.sort()
        for r, (v, k, i) in enumerate(lst):
            data[k]["f"]["rank12"][i] = r / max(len(lst) - 1, 1)
    for label, mode in (("(a) 60 min", 12), ("(b) tot sessieslot", "close")):
        Xs, ys, ms, srcs, poss = [], [], [], [], []
        for k, d in enumerate(data):
            n = len(d["c"]); i = np.where(d["grid"])[0]
            j = np.minimum(i + 12, d["last"][i]) if mode == 12 else d["last"][i]
            ok = j > i
            if mode == 12:
                ok &= (i + 12) <= d["last"][i]
            i, j = i[ok], j[ok]
            y = d["c"][j] / d["c"][i] - 1
            X = np.column_stack([d["f"][f][i] for f in FEATS[:-1]] + [np.full(len(i), k, float)]).astype(np.float32)
            good = np.isfinite(y) & np.all(np.isfinite(X[:, :13]), axis=1)
            Xs.append(X[good]); ys.append(y[good]); ms.append(d["month"][i][good]); srcs.append(np.full(good.sum(), k)); poss.append(np.c_[i[good], j[good]])
        X = np.vstack(Xs); y = np.concatenate(ys); m = np.concatenate(ms); src = np.concatenate(srcs); pos = np.vstack(poss)
        trades = []
        for tm in sorted(x for x in set(m.tolist()) if x >= 2022 * 12):
            trm = (m >= tm - 6) & (m < tm - 0)
            # purging niet nodig: targets eindigen binnen dezelfde handelsdag, dus nooit in de testmaand
            tr_idx = np.where(trm)[0][::2]
            te_idx = np.where(m == tm)[0]
            if len(tr_idx) < 5000 or len(te_idx) == 0:
                continue
            model = lgb.LGBMRegressor(**PARAMS).fit(X[tr_idx], y[tr_idx], categorical_feature=[len(FEATS) - 1])
            ptr = model.predict(X[tr_idx]); hi, lo = np.percentile(ptr, 95), np.percentile(ptr, 5)
            pte = model.predict(X[te_idx]); busy = {}
            for q, p in zip(te_idx, pte):
                k = src[q]; i, j = pos[q]
                if i < busy.get(k, -1):
                    continue
                side = 1 if p >= hi else (-1 if p <= lo else 0)
                if not side:
                    continue
                d = data[k]
                gross = side * (d["c"][j] / d["c"][i] - 1)
                cost = (d["sp"][i] if side > 0 else d["sp"][j]) / d["c"][i] + 2 * COMM
                trades.append((int(d["year"][i]), str(d["st"][i])[:10], gross - cost))
                busy[k] = j
        x = np.array([t[2] for t in trades]); tt = x.mean() / x.std(ddof=1) * math.sqrt(len(x))
        yr = defaultdict(list); daily = defaultdict(float)
        for t in trades:
            yr[t[0]].append(t[2]); daily[t[1]] += t[2] / len(SYMS)
        dv = np.array(list(daily.values())); sr = dv.mean() / dv.std() * math.sqrt(252)
        pos_y = sum(np.mean(v) > 0 for v in yr.values())
        print(f"{label}: N {len(x)} | netto {x.mean()*1e4:+.2f} bp/trade | OOS t {tt:+.2f} | jaren+ {pos_y}/{len(yr)} | SR na kosten {sr:+.2f} | "
              + " ".join(f"{k}:{np.mean(v)*1e4:+.1f}({len(v)})" for k, v in sorted(yr.items())), flush=True)
        print("   → " + ("permutatietest nodig" if tt >= 3 and pos_y >= 4 else "afgewezen (OOS t < 3 of < 4/5 jaren positief)"), flush=True)


if __name__ == "__main__":
    main()
