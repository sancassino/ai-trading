#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N142 US30_US500_XS + N143 XLE_ENERGY_EQUITY_STRESS.

Freeze (no thr-grid, no soft gate, no swap-credit alpha):
  N142: ratio US30cash/US500cash z40 thr ±1.5 basis fade, BOTH legs,
        entry next session 15:30 CET, flat ≤21:00. Gate 3.69 bp
        = 3 × (RT_US30 0.45 + RT_US500 0.78). Both in COSTS. Swap 0.
  N143: XLE daily level z40 thr ±1.0 fade_extreme → US500cash only,
        same clock. Gate 2.34 bp = 3 × RT_US500 0.78. Swap 0.
        Lane-A day_t 2.29 is not a PASS. No overnight US100.

Clone bar (precommitted; decided before the run):
  FAIL_CLONE if |z Pearson| ≥ 0.90, or
  (sign agreement on both-active ≥ 0.85 AND both-active/candidate-active ≥ 0.70).

  N142 binding peers:
    US100/US500 ratio z40 (N81 thr ±1.0 and same-thr ±1.5);
    GER40/UK100 ratio z40 (N138);
    XLE z40 thr ±1.0 (N143 signal);
    N103 GER-AM → US30 same-dir vs the US30 leg;
    N92 US100 NY-2h mom vs the US30 leg and vs the US500 leg;
    N41 US30 EU→US cont vs the US30 leg;
    N35 US100 EU→US cont vs the US500 leg;
    IDX_SHORT-style US30 20d short-only vs the US30 leg
    (same-sign index TSMOM, not an opposite-leg basis).
  A clone is FAIL even if the mean clears 3.69. Do not rewrite as
  US100/US500, GER→US30, or a single-leg US30.

  N143 binding peers:
    UNG z40 (N112 thr ±1.5 and same-thr ±1.0);
    XLF z40 thr ±1.5 (N134);
    DBC z40 thr ±1.0;
    HEATOIL/BRENT crack z60 thr ±0.5 (N101);
    N98 USOIL Lon-AM → US100 vs the US500 side;
    N140 XAU/UKOIL z40 vs the US500 side (oil XS);
    ENERGY_TSMOM UKOIL 20d long-only vs the US500 side;
    N142 US500 leg (the other OPEN; do not pool).

Train trades only: entry date in 2021-01-01..2023-12-31. No 2024+ prices
in the signal. z uses ddof=0.
"""
from __future__ import annotations
import gzip, io, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n142_n143_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
MIN_N = 150
GATE_142 = 3.69
GATE_143 = 2.34
Z_CLONE = 0.90
AGREE_CLONE = 0.85
COVER_CLONE = 0.70


def load_m5(sym: str, end=TRAIN_END) -> pd.DataFrame:
    path = ROOT / "data" / "m5gz" / f"{sym}.csv.gz"
    with gzip.open(path, "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df = df.dropna(subset=["close"]).sort_values("time")
    return df[(df["time"] >= TRAIN_START) & (df["time"] <= end)].reset_index(drop=True)


def load_daily_close(sym: str) -> pd.Series:
    path = ROOT / "data" / "daily" / f"{sym}.csv"
    raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    body = [ln for ln in raw if not ln.startswith("#")]
    sep = ";" if body and ";" in body[0] else ","
    df = pd.read_csv(io.StringIO("\n".join(body)), sep=sep)
    cols = {c.lower().replace(" ", ""): c for c in df.columns}
    dc = cols.get("date") or cols.get("observation_date")
    cc = cols.get("adjclose") or cols.get("close")
    s = pd.Series(
        pd.to_numeric(df[cc], errors="coerce").values,
        index=pd.DatetimeIndex(
            pd.to_datetime(df[dc].astype(str).str.replace(".", "-", regex=False))
        ).normalize(),
        name=sym,
    )
    s = s[~s.index.duplicated(keep="last")].sort_index().dropna()
    # No 2024+ prices in the z.
    return s[s.index <= TRAIN_END]


def first_bar_at(g, day, h, m=0, span_min=15):
    t0 = day + pd.Timedelta(hours=h, minutes=m)
    t1 = t0 + pd.Timedelta(minutes=span_min)
    exact = g[g["time"] == t0]
    if len(exact):
        return exact.iloc[0]
    win = g[(g["time"] >= t0) & (g["time"] <= t1)]
    return win.iloc[0] if len(win) else None


def last_bar_le(g, day, h, m=0):
    t = day + pd.Timedelta(hours=h, minutes=m)
    win = g[g["time"] <= t]
    return win.iloc[-1] if len(win) else None


def daily_close_22(df: pd.DataFrame) -> pd.Series:
    d = df.copy()
    d["day"] = d["time"].dt.normalize()
    cut = d["day"] + pd.Timedelta(hours=22)
    sub = d[d["time"] <= cut]
    s = sub.groupby("day")["close"].last().sort_index()
    return s[s > 0]


def zscore(sig: pd.Series, window: int) -> pd.Series:
    mu = sig.rolling(window, min_periods=window).mean()
    sd = sig.rolling(window, min_periods=window).std(ddof=0).replace(0, np.nan)
    return (sig - mu) / sd


def by_day(df: pd.DataFrame) -> dict:
    d = df.copy()
    d["day"] = d["time"].dt.normalize()
    return {day: g for day, g in d.groupby("day", sort=False)}


def leg_ret_bp(g, day, side: int, h0, m0, h1, m1):
    b0 = first_bar_at(g, day, h0, m0, 15)
    b1 = last_bar_le(g, day, h1, m1)
    if b0 is None or b1 is None:
        return None
    if b1["time"] <= b0["time"]:
        return None
    p0 = float(b0["close"])
    p1 = float(b1["close"])
    if p0 <= 0 or p1 <= 0:
        return None
    return side * 1e4 * (p1 / p0 - 1.0)


def screen_xs(a: pd.DataFrame, b: pd.DataFrame, h0, m0, h1, m1, name_a="a", name_b="b", thr=1.5):
    ca = daily_close_22(a)
    cb = daily_close_22(b)
    both = pd.concat([ca.rename("a"), cb.rename("b")], axis=1).dropna()
    ratio = (both["a"] / both["b"]).rename("ratio")
    z40 = zscore(ratio, 40)
    pos = pd.Series(0.0, index=ratio.index)
    pos[z40 > thr] = -1.0
    pos[z40 < -thr] = 1.0
    ga = by_day(a)
    gb = by_day(b)
    trades = []
    days = list(pos.index)
    n_sig = 0
    n_skip_bar = 0
    for i in range(1, len(days)):
        sig_day = days[i - 1]
        day = days[i]
        if day < TRAIN_START or day > TRAIN_END:
            continue
        side = float(pos.loc[sig_day])
        if side == 0.0 or not np.isfinite(side):
            continue
        n_sig += 1
        gda = ga.get(day)
        gdb = gb.get(day)
        if gda is None or gdb is None:
            n_skip_bar += 1
            continue
        r_a = leg_ret_bp(gda, day, int(side), h0, m0, h1, m1)
        r_b = leg_ret_bp(gdb, day, int(-side), h0, m0, h1, m1)
        if r_a is None or r_b is None:
            n_skip_bar += 1
            continue
        trades.append(
            {
                "date": str(pd.Timestamp(day).date()),
                "signal_day": str(pd.Timestamp(sig_day).date()),
                "side": int(side),
                f"{name_a}_bp": r_a,
                f"{name_b}_bp": r_b,
                "bruto_bp": r_a + r_b,
                "z40": None if not np.isfinite(z40.loc[sig_day]) else round(float(z40.loc[sig_day]), 4),
            }
        )
    meta = {"n_signal_days": n_sig, "n_skip_missing_bar": n_skip_bar}
    return trades, ratio, z40, pos, meta


def screen_level_session(sig: pd.Series, us: pd.DataFrame, window: int, thr: float):
    """fade_extreme: z>+thr short the index, z<-thr long. Trade next US500 session."""
    sig = sig.sort_index()
    sig = sig[sig.index <= TRAIN_END]
    z = zscore(sig, window)
    pos = pd.Series(0.0, index=sig.index)
    pos[z > thr] = -1.0
    pos[z < -thr] = 1.0
    ud = us.copy()
    ud["day"] = ud["time"].dt.normalize()
    days = sorted(ud["day"].unique())
    groups = {day: g for day, g in ud.groupby("day", sort=False)}
    trades = []
    n_sig = 0
    n_skip = 0
    for day in days:
        if day < TRAIN_START or day > TRAIN_END:
            continue
        prior = pos[pos.index < day]
        if prior.empty:
            continue
        side = float(prior.iloc[-1])
        if side == 0.0 or not np.isfinite(side):
            continue
        n_sig += 1
        g = groups.get(day)
        if g is None or g.empty:
            n_skip += 1
            continue
        bruto = leg_ret_bp(g, day, int(side), 15, 30, 21, 0)
        if bruto is None:
            n_skip += 1
            continue
        sig_day = prior.index[-1]
        trades.append(
            {
                "date": str(pd.Timestamp(day).date()),
                "signal_day": str(pd.Timestamp(sig_day).date()),
                "side": int(side),
                "bruto_bp": bruto,
                "z": None if not np.isfinite(z.loc[sig_day]) else round(float(z.loc[sig_day]), 4),
            }
        )
    return trades, z, pos, {"n_signal_days": n_sig, "n_skip_missing_bar": n_skip}


def ratio_z_pos(cache, sym_a, sym_b, window=40, thr=1.5):
    ca = daily_close_22(cache[sym_a])
    cb = daily_close_22(cache[sym_b])
    both = pd.concat([ca.rename("a"), cb.rename("b")], axis=1).dropna()
    ratio = both["a"] / both["b"]
    z = zscore(ratio, window)
    pos = pd.Series(0.0, index=ratio.index)
    pos[z > thr] = -1.0
    pos[z < -thr] = 1.0
    return z, pos


def level_z_pos(sym, window, thr):
    s = load_daily_close(sym)
    z = zscore(s, window)
    pos = pd.Series(0.0, index=s.index)
    pos[z > thr] = -1.0
    pos[z < -thr] = 1.0
    return z, pos


def align(z, pos, index):
    if z is None:
        return None, pos.reindex(index).fillna(0.0)
    zz = z.reindex(index, method="ffill")
    pp = pos.reindex(index, method="ffill").fillna(0.0)
    return zz, pp


def clone_pair(name, z_c, pos_c, z_p, pos_p) -> dict:
    both = pos_c.to_frame("c").join(pos_p.rename("p"), how="inner").dropna()
    both = both[(both.index >= TRAIN_START) & (both.index <= TRAIN_END)]
    active = both[both["c"] != 0]
    both_on = active[active["p"] != 0]
    agree = float((both_on["c"] == both_on["p"]).mean()) if len(both_on) else None
    cover = float(len(both_on) / len(active)) if len(active) else None
    corr = None
    if z_c is not None and z_p is not None:
        zz = z_c.to_frame("c").join(z_p.rename("p"), how="inner").dropna()
        zz = zz[(zz.index >= TRAIN_START) & (zz.index <= TRAIN_END)]
        if len(zz) > 30:
            corr = float(zz["c"].corr(zz["p"]))
    is_clone = False
    if corr is not None and abs(corr) >= Z_CLONE:
        is_clone = True
    if agree is not None and cover is not None and agree >= AGREE_CLONE and cover >= COVER_CLONE:
        is_clone = True
    return {
        "peer": name,
        "z_corr_train": None if corr is None else round(corr, 4),
        "sign_agree_both_active": None if agree is None else round(agree, 4),
        "both_active_over_cand": None if cover is None else round(cover, 4),
        "n_cand_active": int(len(active)),
        "n_both_active": int(len(both_on)),
        "clone": is_clone,
    }


def impulse_pos(df, h0, m0, h1, m1, thr, fade: bool) -> pd.Series:
    groups = by_day(df)
    pos = {}
    for day, g in groups.items():
        b0 = first_bar_at(g, day, h0, m0, 15)
        b1 = first_bar_at(g, day, h1, m1, 15)
        if b0 is None or b1 is None or b1["time"] <= b0["time"]:
            continue
        p0 = float(b0["close"])
        p1 = float(b1["close"])
        if p0 <= 0 or p1 <= 0:
            continue
        move = 1e4 * (p1 / p0 - 1.0)
        if abs(move) < thr:
            continue
        sign = 1.0 if move > 0 else -1.0
        pos[day] = -sign if fade else sign
    return pd.Series(pos, dtype=float).sort_index()


def ny2h_pos(df) -> pd.Series:
    """N92: sign of US100 15:30→17:30, held after 17:30. Position dated that day."""
    groups = by_day(df)
    pos = {}
    for day, g in groups.items():
        b0 = first_bar_at(g, day, 15, 30, 15)
        b1 = first_bar_at(g, day, 17, 30, 15)
        if b0 is None or b1 is None or b1["time"] <= b0["time"]:
            continue
        p0 = float(b0["close"])
        p1 = float(b1["close"])
        if p0 <= 0 or p1 <= 0 or p1 == p0:
            continue
        pos[day] = 1.0 if p1 > p0 else -1.0
    return pd.Series(pos, dtype=float).sort_index()


def short_tsmom20(df) -> tuple[pd.Series, pd.Series]:
    """IDX_SHORT-style: 20d return < 0 → short (-1). Same-sign index TSMOM, not a basis."""
    c = daily_close_22(df)
    ret = c / c.shift(20) - 1.0
    pos = pd.Series(0.0, index=c.index)
    pos[ret < 0] = -1.0
    return ret, pos


def oil_long_tsmom20(df) -> pd.Series:
    c = daily_close_22(df)
    ret = c / c.shift(20) - 1.0
    pos = pd.Series(0.0, index=c.index)
    pos[ret > 0] = 1.0
    return pos


def trade_pos(trades) -> pd.Series:
    return pd.Series(
        {pd.Timestamp(t["date"]): float(t["side"]) for t in trades}, dtype=float
    ).sort_index()


def verdict(trades, gate, label, instrument, notes=""):
    n = len(trades)
    base = {
        "id": label,
        "instrument": instrument,
        "n": n,
        "mean_bruto_bp": None,
        "gate_bp": gate,
        "verdict": "FAIL",
        "notes": notes,
    }
    if n == 0:
        return base
    arr = np.array([t["bruto_bp"] for t in trades], dtype=float)
    mean = float(arr.mean())
    if n >= MIN_N and mean >= gate:
        v = "PASS_may_PREREG"
    elif mean >= gate and n < MIN_N:
        v = "UNDERPOWERED"
    else:
        v = "FAIL"
    years = {}
    for y in (2021, 2022, 2023):
        ys = [t["bruto_bp"] for t in trades if t["date"].startswith(str(y))]
        if ys:
            years[str(y)] = round(float(np.mean(ys)), 4)
    base.update(
        {
            "mean_bruto_bp": round(mean, 4),
            "median_bruto_bp": round(float(np.median(arr)), 4),
            "stress_gate_bp": round(gate * 1.5, 4),
            "stress_note": (
                "PASS_stress_informal"
                if mean >= gate * 1.5
                else "BELOW_stress_1.5x (info only; own gate is the cost gate)"
            ),
            "verdict": v,
            "hit_rate": round(float((arr > 0).mean()), 4),
            "n_long_basket": int(sum(1 for t in trades if t.get("side", 0) > 0)),
            "n_short_basket": int(sum(1 for t in trades if t.get("side", 0) < 0)),
            "years": years,
        }
    )
    return base


def apply_clone(summary, clones):
    hit = [k for k, v in clones.items() if v.get("clone") and v.get("binding", True)]
    summary["clone_hits"] = hit
    if hit:
        summary["verdict"] = "FAIL_CLONE"
        if "CLONE" not in summary["notes"]:
            summary["notes"] += " | CLONE of " + ",".join(hit) + " — no PREREG"
    return summary


def bundle(z_c, pos_c, peers):
    out = {}
    for name, z_p, pos_p, binding in peers:
        z_u, p_u = align(z_p, pos_p, pos_c.index)
        rec = clone_pair(name, z_c, pos_c, z_u, p_u)
        rec["binding"] = binding
        out[name] = rec
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    need = (
        "US30cash", "US500cash", "US100cash", "GER40cash", "UK100cash",
        "UKOILcash", "USOILcash", "XAUUSD",
    )
    cache = {s: load_m5(s) for s in need}

    t142, ratio142, z142, pos142, meta142 = screen_xs(
        cache["US30cash"], cache["US500cash"], 15, 30, 21, 0, "us30", "us500", thr=1.5
    )
    xle = load_daily_close("XLE")
    t143, z143, pos143, meta143 = screen_level_session(xle, cache["US500cash"], 40, 1.0)

    z_nq, pos_nq = ratio_z_pos(cache, "US100cash", "US500cash", 40, 1.5)
    z_nq81, pos_nq81 = ratio_z_pos(cache, "US100cash", "US500cash", 40, 1.0)
    z_geuk, pos_geuk = ratio_z_pos(cache, "GER40cash", "UK100cash", 40, 1.5)
    z_xle, pos_xle = level_z_pos("XLE", 40, 1.0)
    z_ung, pos_ung = level_z_pos("UNG", 40, 1.5)
    z_ung1, pos_ung1 = level_z_pos("UNG", 40, 1.0)
    z_xlf, pos_xlf = level_z_pos("XLF", 40, 1.5)
    z_dbc, pos_dbc = level_z_pos("DBC", 40, 1.0)
    # crack
    ho = load_daily_close("HEATOIL_F")
    br = load_daily_close("BRENT_F")
    crack = (ho / br).dropna()
    z_ck = zscore(crack, 60)
    pos_ck = pd.Series(0.0, index=crack.index)
    pos_ck[z_ck > 0.5] = -1.0
    pos_ck[z_ck < -0.5] = 1.0

    # N140 XAU/UKOIL z (signal only; not re-traded)
    z_oil, pos_oil = ratio_z_pos(cache, "XAUUSD", "UKOILcash", 40, 1.5)
    energy = oil_long_tsmom20(cache["UKOILcash"])

    n103 = impulse_pos(cache["GER40cash"], 8, 0, 12, 0, 40.0, fade=False)
    n92 = ny2h_pos(cache["US100cash"])
    n41 = impulse_pos(cache["US30cash"], 9, 0, 15, 0, 40.0, fade=False)
    n35 = impulse_pos(cache["US100cash"], 9, 0, 15, 0, 40.0, fade=False)
    n98 = impulse_pos(cache["USOILcash"], 8, 0, 12, 0, 40.0, fade=False)
    _, pos_short30 = short_tsmom20(cache["US30cash"])

    side142 = trade_pos(t142)
    us30_leg = side142
    us500_leg = -side142
    side143 = trade_pos(t143)

    c142 = bundle(z142, pos142, [
        ("US100_US500_z40_thr1.5", z_nq, pos_nq, True),
        ("N81_US100_US500_z40_thr1.0", z_nq81, pos_nq81, True),
        ("N138_GER_UK_z40", z_geuk, pos_geuk, True),
        ("XLE_z40_thr1.0", z_xle, pos_xle, True),
    ])
    # leg-level session clones (no z)
    def leg_clone(key, leg, peer):
        rec = clone_pair(key, None, leg, None, peer.reindex(leg.index).fillna(0.0))
        rec["binding"] = True
        c142[key] = rec

    leg_clone("N103_GER_AM_vs_US30_leg", us30_leg, n103)
    leg_clone("N92_US100_NY2H_vs_US30_leg", us30_leg, n92)
    leg_clone("N92_US100_NY2H_vs_US500_leg", us500_leg, n92)
    leg_clone("N41_US30_EU_vs_US30_leg", us30_leg, n41)
    leg_clone("N35_US100_EU_vs_US500_leg", us500_leg, n35)
    leg_clone("IDX_SHORT_US30_ret20_vs_US30_leg", us30_leg, pos_short30)

    c143 = bundle(z143, pos143, [
        ("UNG_z40_thr1.5_N112", z_ung, pos_ung, True),
        ("UNG_z40_thr1.0", z_ung1, pos_ung1, True),
        ("XLF_z40_N134", z_xlf, pos_xlf, True),
        ("DBC_z40_thr1.0", z_dbc, pos_dbc, True),
        ("CRACK_z60_N101", z_ck, pos_ck, True),
        ("N140_XAU_UKOIL", z_oil, pos_oil, True),
        ("N142_US30_US500", z142, pos142, True),
    ])
    def leg_clone143(key, peer):
        rec = clone_pair(key, None, side143, None, peer.reindex(side143.index).fillna(0.0))
        rec["binding"] = True
        c143[key] = rec

    leg_clone143("N98_USOIL_AM_vs_US500_side", n98)
    leg_clone143("ENERGY_TSMOM_UKOIL_L20_vs_US500_side", energy)
    leg_clone143("N142_US500_leg", us500_leg)

    s142 = verdict(
        t142, GATE_142, "N142", "US30cash+US500cash",
        "US30_US500_XS z40/±1.5 both legs 15:30→21:00; gate 3.69 = 3*(0.45+0.78); swap 0; NEW_FAMILY BK; RTs in COSTS",
    )
    s142["meta"] = meta142
    s142["rt_in_costs"] = True
    apply_clone(s142, c142)
    s142["clone"] = c142

    s143 = verdict(
        t143, GATE_143, "N143", "US500cash",
        "XLE_ENERGY_EQUITY_STRESS z40/±1.0 fade_extreme → US500 15:30→21:00; gate 2.34; swap 0; NEW_FAMILY BL; S2 5a21939; Lane-A day_t 2.29 is not this screen",
    )
    s143["meta"] = meta143
    s143["rt_in_costs"] = True
    s143["lane_a_day_t"] = 2.29
    s143["lane_a_not_a_pass"] = True
    apply_clone(s143, c143)
    s143["clone"] = c143

    pd.DataFrame(t142).to_csv(OUT / "n142_trades_train.csv", index=False)
    pd.DataFrame(t143).to_csv(OUT / "n143_trades_train.csv", index=False)

    def pub(s):
        return {k: v for k, v in s.items() if k != "clone"}

    summary = {
        "N142": pub(s142),
        "N143": pub(s143),
        "N142_clones": c142,
        "N143_clones": c143,
        "gates": {"N142": GATE_142, "N143": GATE_143},
        "clone_rule": {"abs_z_corr_ge": Z_CLONE, "sign_agree_ge": AGREE_CLONE, "cover_ge": COVER_CLONE},
        "train": "2021-01-01..2023-12-31 entry dates only",
        "min_n": MIN_N,
        "swap": 0,
        "session": "15:30-21:00 CET",
        "no_thr_grid": True,
        "no_2024_in_signal": True,
    }
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2, default=str))

    def line(tag, s):
        return (
            f"- **{tag}**: N={s['n']} mean={s['mean_bruto_bp']} "
            f"med={s.get('median_bruto_bp')} gate={s['gate_bp']} → **{s['verdict']}** "
            f"years={s.get('years')} L/S={s.get('n_long_basket')}/{s.get('n_short_basket')} "
            f"hits={s.get('clone_hits')} meta={s.get('meta')}\n"
        )

    md = (
        "# D-092.1 N142/N143 pre-screen (train 2021–2023)\n\n"
        + line("N142 US30_US500_XS", s142)
        + line("N143 XLE_ENERGY_EQUITY_STRESS", s143)
        + "\nClone detail is in prescreen.json. No thr-grid. No 2024+ selection. Lane-A day_t is not this gate.\n"
    )
    (OUT / "prescreen.md").write_text(md)
    print(json.dumps({"N142": pub(s142), "N142_clones": c142, "N143": pub(s143), "N143_clones": c143}, indent=2, default=str))


if __name__ == "__main__":
    main()
