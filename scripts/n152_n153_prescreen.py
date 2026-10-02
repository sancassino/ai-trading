#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N152 GBP_NZD + N153 EUR_CAD.

Gates frozen from COSTS_FTMO.csv before any train PnL.

  N152 GBPUSD RT 0.70 + NZDUSD RT 1.85 = 2.55 → gate 3× = 7.65 bp.
  N153 EURUSD RT 0.63 + USDCAD RT 0.80 = 1.43 → gate 3× = 4.29 bp.

Session-flat 15:30→21:00 CET is the cheap side: swap is 0 and is in the
gate as 0. A two-sided overnight book cannot lock the receiving side.

N152 trades the currencies: z>+1.5 → short GBPUSD + long NZDUSD;
z<-1.5 → long GBPUSD + short NZDUSD. Opposite quote signs (NZD is the
base of NZDUSD).

N153 trades the currencies, not the USDCAD quote as if it were CAD:
z>+1.5 → short EURUSD + long CAD = short USDCAD;
z<-1.5 → long EURUSD + short CAD = long USDCAD.
Both quoted CFDs therefore take the same sign. Ratio is still
EURUSD/USDCAD as frozen in the VOORSTEL (z is scale-free).

Clone bar (precommitted; decided before the run):
  FAIL_CLONE if |z Pearson| >= 0.90, or
  (sign agree on both-active >= 0.85 AND cover >= 0.70).
  A clone is not a PASS. No thr-grid. No soft gate. No single-leg rewrite.
  No inline replacement.

Must-not-equal (binding):
  N152: GBPAUD z40, AUDNZD z40, EURNZD z40, XAG/US30 z40, EURJPY/USDCHF z40,
        N111 GBPAUD 5d LO vs the GBP leg, N106 EURNZD 5d LO,
        N84 AUDNZD stretch-fade, N90 GBPJPY 5d LO vs the GBP leg,
        N94 NZDJPY 5d LO vs the NZD leg,
        L60 FX-med (GBPUSD, NZDUSD, GBPNZD cross, USDJPY, EURJPY),
        GBP session N29 midday fade and N38 London-morning continuation
        vs the GBP leg, and N153.
  N153: AUDCAD z40, EURGBP z40, CADCHF z40, EUR/GER40 z40,
        EURJPY/USDCHF z40, XAG/US30 z40,
        N97 AUDCAD 5d LO, N99 CADCHF 5d LO, N96 CADJPY 5d LO,
        N88 EURGBP 5d short-only, USDCAD L60, EURUSD L60, EURCAD L60,
        EURNZD 5d LO, N149, N151, N152.

Train trades only: entry date in 2021-01-01..2023-12-31. No 2024+ prices
in the signal. z uses ddof=0. Threshold ±1.5 frozen.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n152_n153_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
MIN_N = 150
Z_CLONE = 0.90
AGREE_CLONE = 0.85
COVER_CLONE = 0.70

COSTS_RT = {
    "GBPUSD": 0.70,
    "NZDUSD": 1.85,
    "EURUSD": 0.63,
    "USDCAD": 0.80,
}
GATE_152 = 3.0 * (COSTS_RT["GBPUSD"] + COSTS_RT["NZDUSD"])  # 7.65
GATE_153 = 3.0 * (COSTS_RT["EURUSD"] + COSTS_RT["USDCAD"])  # 4.29


def load_m5(sym: str, start, end) -> pd.DataFrame:
    path = ROOT / "data" / "m5gz" / f"{sym}.csv.gz"
    df = pd.read_csv(path, sep=";", compression="gzip", comment="#")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df = df.dropna(subset=["close"]).sort_values("time")
    df = df[(df["time"] >= start) & (df["time"] <= end)].reset_index(drop=True)
    return df[["time", "close"]]


def load_daily_close(sym: str) -> pd.Series:
    path = ROOT / "data" / "daily" / f"{sym}.csv"
    raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    body = [ln for ln in raw if not ln.startswith("#")]
    sep = ";" if body and ";" in body[0] else ","
    df = pd.read_csv(pd.io.common.StringIO("\n".join(body)), sep=sep)
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


def screen_xs(a, b, h0, m0, h1, m1, name_a, name_b, thr=1.5, b_sign=-1):
    """b_sign=-1: opposite quote (N152). b_sign=+1: same quote sign (N153 CAD)."""
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
        r_b = leg_ret_bp(gdb, day, int(b_sign * side), h0, m0, h1, m1)
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
    meta = {
        "n_signal_days": n_sig,
        "n_skip_missing_bar": n_skip_bar,
        "n_ratio_days": int(len(ratio)),
        "ratio_first": str(pd.Timestamp(ratio.index.min()).date()) if len(ratio) else None,
        "ratio_last": str(pd.Timestamp(ratio.index.max()).date()) if len(ratio) else None,
        "b_sign": b_sign,
    }
    return trades, ratio, z40, pos, meta


def level_z_pos_m5(cache, sym, window=40, thr=1.5):
    s = daily_close_22(cache[sym])
    z = zscore(s, window)
    pos = pd.Series(0.0, index=s.index)
    pos[z > thr] = -1.0
    pos[z < -thr] = 1.0
    return z, pos


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


def daily_ratio_z_pos(sym_a, sym_b, window, thr):
    a = load_daily_close(sym_a)
    b = load_daily_close(sym_b)
    ratio = (a / b).dropna()
    ratio = ratio[(ratio.index >= TRAIN_START - pd.Timedelta(days=window * 3)) & (ratio.index <= TRAIN_END)]
    z = zscore(ratio, window)
    pos = pd.Series(0.0, index=ratio.index)
    pos[z > thr] = -1.0
    pos[z < -thr] = 1.0
    return z, pos


def lo_ret_pos(close: pd.Series, lookback: int) -> pd.Series:
    ret = close / close.shift(lookback) - 1.0
    pos = pd.Series(0.0, index=close.index)
    pos[ret > 0] = 1.0
    return pos


def so_ret_pos(close: pd.Series, lookback: int) -> pd.Series:
    """N88: ret5<0 → short (-1); else flat."""
    ret = close / close.shift(lookback) - 1.0
    pos = pd.Series(0.0, index=close.index)
    pos[ret < 0] = -1.0
    return pos


def session_move_pos(df, h0, m0, h1, m1, thr, fade: bool) -> pd.Series:
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
        sgn = 1.0 if move > 0 else -1.0
        pos[day] = -sgn if fade else sgn
    return pd.Series(pos, dtype=float).sort_index()


def audnzd_stretch_pos(df) -> pd.Series:
    """N84: |stretch vs MA20|≥40 bp at 08:00, fade."""
    close = daily_close_22(df)
    ma20 = close.rolling(20, min_periods=20).mean()
    groups = by_day(df)
    pos = {}
    for day, g in groups.items():
        # MA20 uses prior closes only (signal day is prior close series shifted)
        prev = ma20.shift(1)
        if day not in prev.index or not np.isfinite(prev.loc[day]):
            continue
        b0 = first_bar_at(g, day, 8, 0, 15)
        if b0 is None:
            continue
        p0 = float(b0["close"])
        ma = float(prev.loc[day])
        if p0 <= 0 or ma <= 0:
            continue
        stretch = 1e4 * (p0 / ma - 1.0)
        if stretch >= 40:
            pos[day] = -1.0
        elif stretch <= -40:
            pos[day] = 1.0
    return pd.Series(pos, dtype=float).sort_index()


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


def verdict(trades, gate, label, instrument, notes, history_missing=False):
    n = len(trades)
    base = {
        "id": label,
        "instrument": instrument,
        "n": n,
        "mean_bruto_bp": None,
        "gate_bp": round(float(gate), 4),
        "verdict": "FAIL",
        "notes": notes,
    }
    if history_missing or n == 0:
        base["verdict"] = "DIAG_FAIL"
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


def leg_clone(name, leg, peer):
    rec = clone_pair(name, None, leg, None, peer.reindex(leg.index).fillna(0.0))
    rec["binding"] = True
    return rec


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    need = (
        "GBPUSD", "NZDUSD", "EURUSD", "USDCAD",
        "GBPAUD", "AUDNZD", "EURNZD", "AUDCAD", "EURGBP", "CADCHF", "CADJPY",
        "GBPJPY", "NZDJPY", "GBPNZD", "EURCAD",
        "XAGUSD", "US30cash", "EURJPY", "USDCHF", "GER40cash", "USDJPY", "AUDUSD",
    )
    cache = {}
    for s in need:
        cache[s] = load_m5(s, TRAIN_START - pd.Timedelta(days=120), TRAIN_END)

    def train_days(sym):
        t = cache[sym]["time"]
        m = (t >= TRAIN_START) & (t <= TRAIN_END)
        return int(t[m].dt.normalize().nunique())

    td = {s: train_days(s) for s in need}
    days = {s: int(cache[s]["time"].dt.normalize().nunique()) if len(cache[s]) else 0 for s in need}
    hist_152 = td["GBPUSD"] < 150 or td["NZDUSD"] < 150
    hist_153 = td["EURUSD"] < 150 or td["USDCAD"] < 150

    t152, _, z152, pos152, meta152 = screen_xs(
        cache["GBPUSD"], cache["NZDUSD"], 15, 30, 21, 0, "gbp", "nzd", thr=1.5, b_sign=-1
    )
    t153, _, z153, pos153, meta153 = screen_xs(
        cache["EURUSD"], cache["USDCAD"], 15, 30, 21, 0, "eur", "usdcad", thr=1.5, b_sign=+1
    )
    meta152["train_days"] = {"GBPUSD": td["GBPUSD"], "NZDUSD": td["NZDUSD"]}
    meta153["train_days"] = {"EURUSD": td["EURUSD"], "USDCAD": td["USDCAD"]}
    meta152["cad_convention"] = "n/a"
    meta153["cad_convention"] = "LONG CAD = short USDCAD (same quote sign as EUR leg)"
    for meta in (meta152, meta153):
        meta["rt_in_costs"] = True
        meta["swap_bp"] = 0
        meta["session"] = "15:30-21:00 CET cheapest side (overnight swap excluded)"

    z_gbpaud, pos_gbpaud = level_z_pos_m5(cache, "GBPAUD")
    z_audnzd, pos_audnzd = level_z_pos_m5(cache, "AUDNZD")
    z_eurnzd, pos_eurnzd_z = level_z_pos_m5(cache, "EURNZD")
    z_audcad, pos_audcad_z = level_z_pos_m5(cache, "AUDCAD")
    z_eurgbp, pos_eurgbp = level_z_pos_m5(cache, "EURGBP")
    z_cadchf, pos_cadchf_z = level_z_pos_m5(cache, "CADCHF")
    z_xagus, pos_xagus = ratio_z_pos(cache, "XAGUSD", "US30cash")
    z_ejchf, pos_ejchf = ratio_z_pos(cache, "EURJPY", "USDCHF")
    z_eurger, pos_eurger = ratio_z_pos(cache, "EURUSD", "GER40cash")
    # own-cross reconstruction is diagnostic only (should match the ratio)
    z_gbpnzd, pos_gbpnzd = level_z_pos_m5(cache, "GBPNZD")
    z_eurcad, pos_eurcad_z = level_z_pos_m5(cache, "EURCAD")

    c_gbp = daily_close_22(cache["GBPUSD"])
    c_nzd = daily_close_22(cache["NZDUSD"])
    c_eur = daily_close_22(cache["EURUSD"])
    c_cad = daily_close_22(cache["USDCAD"])
    c_jpy = daily_close_22(cache["USDJPY"])
    c_ej = daily_close_22(cache["EURJPY"])
    c_gbpaud = daily_close_22(cache["GBPAUD"])
    c_eurnzd = daily_close_22(cache["EURNZD"])
    c_gbpjpy = daily_close_22(cache["GBPJPY"])
    c_nzdjpy = daily_close_22(cache["NZDJPY"])
    c_audcad = daily_close_22(cache["AUDCAD"])
    c_cadchf = daily_close_22(cache["CADCHF"])
    c_cadjpy = daily_close_22(cache["CADJPY"])
    c_eurgbp = daily_close_22(cache["EURGBP"])
    c_gbpnzd = daily_close_22(cache["GBPNZD"])
    c_eurcad = daily_close_22(cache["EURCAD"])

    pos_gbp_l60 = lo_ret_pos(c_gbp, 60)
    pos_nzd_l60 = lo_ret_pos(c_nzd, 60)
    pos_gbpnzd_l60 = lo_ret_pos(c_gbpnzd, 60)
    pos_jpy_l60 = lo_ret_pos(c_jpy, 60)
    pos_ej_l60 = lo_ret_pos(c_ej, 60)
    pos_eur_l60 = lo_ret_pos(c_eur, 60)
    pos_cad_l60 = lo_ret_pos(c_cad, 60)
    pos_eurcad_l60 = lo_ret_pos(c_eurcad, 60)

    pos_gbpaud_lo = lo_ret_pos(c_gbpaud, 5)
    pos_eurnzd_lo = lo_ret_pos(c_eurnzd, 5)
    pos_gbpjpy_lo = lo_ret_pos(c_gbpjpy, 5)
    pos_nzdjpy_lo = lo_ret_pos(c_nzdjpy, 5)
    pos_audcad_lo = lo_ret_pos(c_audcad, 5)
    pos_cadchf_lo = lo_ret_pos(c_cadchf, 5)
    pos_cadjpy_lo = lo_ret_pos(c_cadjpy, 5)
    pos_eurgbp_so = so_ret_pos(c_eurgbp, 5)

    pos_n29 = session_move_pos(cache["GBPUSD"], 9, 0, 12, 0, 30.0, fade=True)
    pos_n38 = session_move_pos(cache["GBPUSD"], 8, 0, 11, 30, 30.0, fade=False)
    pos_n84 = audnzd_stretch_pos(cache["AUDNZD"])

    # Currency legs. N152 side +1 = long GBP, short NZD.
    gbp_leg = pos152.rename("gbp_leg")
    nzd_leg = (-pos152).rename("nzd_leg")
    # N153 side +1 = long EUR, short CAD = long USDCAD. CAD-currency leg = -side.
    eur_leg = pos153.rename("eur_leg")
    cad_ccy_leg = (-pos153).rename("cad_ccy_leg")

    c152 = bundle(z152, pos152, [
        ("GBPAUD_z40", z_gbpaud, pos_gbpaud, True),
        ("AUDNZD_z40", z_audnzd, pos_audnzd, True),
        ("EURNZD_z40", z_eurnzd, pos_eurnzd_z, True),
        ("XAG_US30_N150", z_xagus, pos_xagus, True),
        ("EURJPY_USDCHF_N151", z_ejchf, pos_ejchf, True),
        ("EUR_CAD_N153", z153, pos153, True),
        ("GBPNZD_own_cross_z40", z_gbpnzd, pos_gbpnzd, False),
    ])
    c152["N111_GBPAUD_LO_vs_GBP_leg"] = leg_clone("N111_GBPAUD_LO_vs_GBP_leg", gbp_leg, pos_gbpaud_lo)
    c152["N106_EURNZD_LO_vs_basket"] = leg_clone("N106_EURNZD_LO_vs_basket", pos152, pos_eurnzd_lo)
    c152["N106_EURNZD_LO_vs_NZD_leg"] = leg_clone("N106_EURNZD_LO_vs_NZD_leg", nzd_leg, -pos_eurnzd_lo)
    c152["N84_AUDNZD_stretch"] = leg_clone("N84_AUDNZD_stretch", pos152, pos_n84)
    c152["N90_GBPJPY_LO_vs_GBP_leg"] = leg_clone("N90_GBPJPY_LO_vs_GBP_leg", gbp_leg, pos_gbpjpy_lo)
    c152["N94_NZDJPY_LO_vs_NZD_leg"] = leg_clone("N94_NZDJPY_LO_vs_NZD_leg", nzd_leg, pos_nzdjpy_lo)
    c152["GBPUSD_L60_vs_GBP_leg"] = leg_clone("GBPUSD_L60_vs_GBP_leg", gbp_leg, pos_gbp_l60)
    c152["NZDUSD_L60_vs_NZD_leg"] = leg_clone("NZDUSD_L60_vs_NZD_leg", nzd_leg, pos_nzd_l60)
    c152["GBPNZD_L60_vs_basket"] = leg_clone("GBPNZD_L60_vs_basket", pos152, pos_gbpnzd_l60)
    c152["USDJPY_L60_vs_basket"] = leg_clone("USDJPY_L60_vs_basket", pos152, pos_jpy_l60)
    c152["EURJPY_L60_vs_basket"] = leg_clone("EURJPY_L60_vs_basket", pos152, pos_ej_l60)
    c152["N29_GBP_midday_fade_vs_GBP_leg"] = leg_clone("N29_GBP_midday_fade_vs_GBP_leg", gbp_leg, pos_n29)
    c152["N38_GBP_Lon_mom_vs_GBP_leg"] = leg_clone("N38_GBP_Lon_mom_vs_GBP_leg", gbp_leg, pos_n38)
    c152["N153_sign"] = leg_clone("N153_sign", pos152, pos153)

    c153 = bundle(z153, pos153, [
        ("AUDCAD_z40", z_audcad, pos_audcad_z, True),
        ("EURGBP_z40", z_eurgbp, pos_eurgbp, True),
        ("CADCHF_z40", z_cadchf, pos_cadchf_z, True),
        ("EUR_GER40_N149", z_eurger, pos_eurger, True),
        ("EURJPY_USDCHF_N151", z_ejchf, pos_ejchf, True),
        ("XAG_US30_N150", z_xagus, pos_xagus, True),
        ("GBP_NZD_N152", z152, pos152, True),
        ("EURCAD_own_cross_z40", z_eurcad, pos_eurcad_z, False),
    ])
    c153["N97_AUDCAD_LO_vs_basket"] = leg_clone("N97_AUDCAD_LO_vs_basket", pos153, pos_audcad_lo)
    c153["N99_CADCHF_LO_vs_CAD_leg"] = leg_clone("N99_CADCHF_LO_vs_CAD_leg", cad_ccy_leg, pos_cadchf_lo)
    c153["N96_CADJPY_LO_vs_CAD_leg"] = leg_clone("N96_CADJPY_LO_vs_CAD_leg", cad_ccy_leg, pos_cadjpy_lo)
    c153["N88_EURGBP_SO_vs_EUR_leg"] = leg_clone("N88_EURGBP_SO_vs_EUR_leg", eur_leg, pos_eurgbp_so)
    c153["USDCAD_L60_vs_CAD_quote"] = leg_clone("USDCAD_L60_vs_CAD_quote", pos153, pos_cad_l60)
    c153["EURUSD_L60_vs_EUR_leg"] = leg_clone("EURUSD_L60_vs_EUR_leg", eur_leg, pos_eur_l60)
    c153["EURCAD_L60_vs_basket"] = leg_clone("EURCAD_L60_vs_basket", pos153, pos_eurcad_l60)
    c153["USDJPY_L60_vs_basket"] = leg_clone("USDJPY_L60_vs_basket", pos153, pos_jpy_l60)
    c153["EURJPY_L60_vs_basket"] = leg_clone("EURJPY_L60_vs_basket", pos153, pos_ej_l60)
    c153["EURNZD_LO_vs_EUR_leg"] = leg_clone("EURNZD_LO_vs_EUR_leg", eur_leg, pos_eurnzd_lo)
    c153["N149_sign"] = leg_clone("N149_sign", pos153, pos_eurger)
    c153["N151_sign"] = leg_clone("N151_sign", pos153, pos_ejchf)
    c153["N152_sign"] = leg_clone("N152_sign", pos153, pos152)

    s152 = verdict(
        t152, GATE_152, "N152", "GBPUSD+NZDUSD",
        (
            "GBPUSD_NZDUSD_CABLE_KIWI_XS z40/±1.5 both legs 15:30→21:00; "
            f"COSTS gate 3*({COSTS_RT['GBPUSD']}+{COSTS_RT['NZDUSD']}); swap 0; NEW_FAMILY BU"
        ),
        history_missing=hist_152,
    )
    s152["meta"] = meta152
    s152["costs_rt"] = {"GBPUSD": COSTS_RT["GBPUSD"], "NZDUSD": COSTS_RT["NZDUSD"]}
    s152["rt_in_costs"] = True
    apply_clone(s152, c152)
    s152["clone"] = c152

    s153 = verdict(
        t153, GATE_153, "N153", "EURUSD+USDCAD",
        (
            "EURUSD_USDCAD_ATLANTIC_XS z40/±1.5 both legs 15:30→21:00; "
            "LONG CAD = short USDCAD; "
            f"COSTS gate 3*({COSTS_RT['EURUSD']}+{COSTS_RT['USDCAD']}); swap 0; NEW_FAMILY BV"
        ),
        history_missing=hist_153,
    )
    s153["meta"] = meta153
    s153["costs_rt"] = {"EURUSD": COSTS_RT["EURUSD"], "USDCAD": COSTS_RT["USDCAD"]}
    s153["rt_in_costs"] = True
    apply_clone(s153, c153)
    s153["clone"] = c153

    pd.DataFrame(t152).to_csv(OUT / "n152_trades_train.csv", index=False)
    pd.DataFrame(t153).to_csv(OUT / "n153_trades_train.csv", index=False)

    def pub(s):
        return {k: v for k, v in s.items() if k != "clone"}

    summary = {
        "N152": pub(s152),
        "N153": pub(s153),
        "N152_clones": c152,
        "N153_clones": c153,
        "gates": {"N152": round(GATE_152, 4), "N153": round(GATE_153, 4)},
        "costs_rt": COSTS_RT,
        "clone_rule": {"abs_z_corr_ge": Z_CLONE, "sign_agree_ge": AGREE_CLONE, "cover_ge": COVER_CLONE},
        "train": "2021-01-01..2023-12-31 entry dates only",
        "min_n": MIN_N,
        "swap": 0,
        "session": "15:30-21:00 CET",
        "no_thr_grid": True,
        "no_2024_in_signal": True,
        "no_inline_replacement": True,
        "gate_source": "COSTS_FTMO.csv roundtrip_intraday_bp; not a session median",
        "loaded_days_incl_warmup": days,
        "train_days": td,
    }
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2, default=str))

    def line(tag, s):
        return (
            f"- **{tag}**: N={s['n']} mean={s['mean_bruto_bp']} "
            f"med={s.get('median_bruto_bp')} gate={s['gate_bp']} "
            f"→ **{s['verdict']}** years={s.get('years')} "
            f"L/S={s.get('n_long_basket')}/{s.get('n_short_basket')} "
            f"hits={s.get('clone_hits')} meta={s.get('meta')}\n"
        )

    md = (
        "# D-092.1 N152/N153 pre-screen (train 2021–2023)\n\n"
        + line("N152 GBPUSD_NZDUSD_CABLE_KIWI_XS", s152)
        + line("N153 EURUSD_USDCAD_ATLANTIC_XS", s153)
        + "\nGates from COSTS_FTMO.csv round-trips. Session-flat so swap=0 is in the gate. "
        + "N153 LONG CAD is short USDCAD. No thr-grid. No 2024+ selection. "
        + "No softer session spread. No inline replacement.\n"
    )
    (OUT / "prescreen.md").write_text(md)
    print(json.dumps({"N152": pub(s152), "N153": pub(s153)}, indent=2, default=str))
    print("---CLONES152---")
    for k, v in c152.items():
        if v.get("clone") or (v.get("z_corr_train") and abs(v["z_corr_train"]) > 0.5) or (v.get("sign_agree_both_active") or 0) > 0.7:
            print(k, v)
    print("---CLONES153---")
    for k, v in c153.items():
        if v.get("clone") or (v.get("z_corr_train") and abs(v["z_corr_train"]) > 0.5) or (v.get("sign_agree_both_active") or 0) > 0.7:
            print(k, v)


if __name__ == "__main__":
    main()
