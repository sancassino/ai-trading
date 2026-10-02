#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N148 USDJPY_US100_RISK_XS + N149 EURUSD_GER40_EUROPE_XS.

Gates are the COSTS_FTMO.csv round-trips, frozen before any train PnL.

  N148 USDJPY RT 0.78 + US100cash RT 0.66 = 1.44 → gate 3× = 4.32 bp.
  N149 EURUSD RT 0.63 + GER40cash RT 0.72 = 1.35 → gate 3× = 4.05 bp.

Session-flat 15:30→21:00 CET is the cheapest side: swap is 0 and is in the
gate as 0. Overnight would add a positive cost on at least one side
(USDJPY short 1.58; US100 long 1.95; EUR long 1.13; GER long 1.79).

Clone bar (precommitted in the VOORSTELs; decided before the run):
  FAIL_CLONE if |z Pearson| >= 0.90, or
  (sign agree on both-active >= 0.85 AND cover >= 0.70).
  A clone is not a PASS. No thr-grid. No soft gate. No single-leg rewrite.

Must-not-equal (binding):
  N148: N92 US100 NY-2h mom, USDJPY LO L60 FX-med, US100 overnight 20d sign,
        US100/US500 z40, US30/US500 z40, N81, N131 US500 day-sign, N149.
  N149: N103 GER AM day-sign, EURNZD LO 5d, N115 EUR Lon-AM sign,
        GER/UK z40, N138, N142, N148.

Train trades only: entry date in 2021-01-01..2023-12-31. No 2024+ prices
in the signal. z uses ddof=0. Threshold ±1.5 frozen.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n148_n149_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
MIN_N = 150
Z_CLONE = 0.90
AGREE_CLONE = 0.85
COVER_CLONE = 0.70

COSTS_RT = {
    "USDJPY": 0.78,
    "US100cash": 0.66,
    "EURUSD": 0.63,
    "GER40cash": 0.72,
}
GATE_148 = 3.0 * (COSTS_RT["USDJPY"] + COSTS_RT["US100cash"])  # 4.32
GATE_149 = 3.0 * (COSTS_RT["EURUSD"] + COSTS_RT["GER40cash"])  # 4.05


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


def screen_xs(a, b, h0, m0, h1, m1, name_a, name_b, thr=1.5):
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
    meta = {
        "n_signal_days": n_sig,
        "n_skip_missing_bar": n_skip_bar,
        "n_ratio_days": int(len(ratio)),
        "ratio_first": str(pd.Timestamp(ratio.index.min()).date()) if len(ratio) else None,
        "ratio_last": str(pd.Timestamp(ratio.index.max()).date()) if len(ratio) else None,
    }
    return trades, ratio, z40, pos, meta


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


def ny2h_pos(df) -> pd.Series:
    """N92: sign of US100 15:30→17:30. Position dated that day."""
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


def impulse_pos(df, h0, m0, h1, m1, thr) -> pd.Series:
    """Same-dir impulse sign. Dated that day. 0 if |move| < thr."""
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
        pos[day] = 1.0 if move > 0 else -1.0
    return pd.Series(pos, dtype=float).sort_index()


def lo_ret_pos(close: pd.Series, lookback: int) -> pd.Series:
    """Long-only: +1 when lookback return > 0, else 0. Dated on the signal day."""
    ret = close / close.shift(lookback) - 1.0
    pos = pd.Series(0.0, index=close.index)
    pos[ret > 0] = 1.0
    return pos


def tsmom_sign(close: pd.Series, lookback: int) -> pd.Series:
    """Bilateral overnight TSMOM sign. +1 up, -1 down, 0 if flat/na."""
    ret = close / close.shift(lookback) - 1.0
    pos = pd.Series(0.0, index=close.index)
    pos[ret > 0] = 1.0
    pos[ret < 0] = -1.0
    return pos


def n81_us100_pos(cache) -> pd.Series:
    """N81: ln(US100/US500) z20 > +1 → short US100. Hostile side flat."""
    ca = daily_close_22(cache["US100cash"])
    cb = daily_close_22(cache["US500cash"])
    both = pd.concat([ca.rename("a"), cb.rename("b")], axis=1).dropna()
    r = np.log(both["a"] / both["b"])
    z = zscore(r, 20)
    pos = pd.Series(0.0, index=r.index)
    pos[z > 1.0] = -1.0  # short US100
    return pos


def n131_us500_pos() -> pd.Series:
    """N131: DXY z120>0.5 and d20>0 → short US500; z120<-0.5 and d20<0 → long."""
    dxy = load_daily_close("DXY")
    z120 = zscore(dxy, 120)
    d20 = dxy / dxy.shift(20) - 1.0
    pos = pd.Series(0.0, index=dxy.index)
    pos[(z120 > 0.5) & (d20 > 0)] = -1.0
    pos[(z120 < -0.5) & (d20 < 0)] = 1.0
    return pos


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
    need = ("USDJPY", "US100cash", "EURUSD", "GER40cash", "US500cash", "US30cash", "UK100cash", "EURNZD")
    cache = {}
    for s in need:
        cache[s] = load_m5(s, TRAIN_START - pd.Timedelta(days=120), TRAIN_END)

    days = {s: int(cache[s]["time"].dt.normalize().nunique()) if len(cache[s]) else 0 for s in need}
    # Warmup days before 2021 are allowed in the z; train-day count is the gate for DIAG.
    def train_days(sym):
        t = cache[sym]["time"]
        m = (t >= TRAIN_START) & (t <= TRAIN_END)
        return int(t[m].dt.normalize().nunique())

    td = {s: train_days(s) for s in need}
    hist_148 = td["USDJPY"] < 150 or td["US100cash"] < 150
    hist_149 = td["EURUSD"] < 150 or td["GER40cash"] < 150

    t148, _, z148, pos148, meta148 = screen_xs(
        cache["USDJPY"], cache["US100cash"], 15, 30, 21, 0, "usdjpy", "us100", thr=1.5
    )
    t149, _, z149, pos149, meta149 = screen_xs(
        cache["EURUSD"], cache["GER40cash"], 15, 30, 21, 0, "eur", "ger", thr=1.5
    )
    meta148["train_days"] = {"USDJPY": td["USDJPY"], "US100cash": td["US100cash"]}
    meta149["train_days"] = {"EURUSD": td["EURUSD"], "GER40cash": td["GER40cash"]}
    meta148["rt_in_costs"] = True
    meta149["rt_in_costs"] = True
    meta148["swap_bp"] = 0
    meta149["swap_bp"] = 0
    meta148["session"] = "15:30-21:00 CET cheapest side (overnight swap excluded)"
    meta149["session"] = "15:30-21:00 CET cheapest side (overnight swap excluded)"

    z_us, pos_us = ratio_z_pos(cache, "US100cash", "US500cash", 40, 1.5)
    z_u30, pos_u30 = ratio_z_pos(cache, "US30cash", "US500cash", 40, 1.5)
    z_geuk, pos_geuk = ratio_z_pos(cache, "GER40cash", "UK100cash", 40, 1.5)

    c_jpy = daily_close_22(cache["USDJPY"])
    c_us100 = daily_close_22(cache["US100cash"])
    c_eur = daily_close_22(cache["EURUSD"])
    c_nzd = daily_close_22(cache["EURNZD"])
    # EURNZD is a cross; LO is on the cross itself (long EUR vs NZD).
    pos_l60 = lo_ret_pos(c_jpy, 60)
    pos_ovn = tsmom_sign(c_us100, 20)
    pos_n92 = ny2h_pos(cache["US100cash"])
    pos_n81 = n81_us100_pos(cache)
    pos_n131 = n131_us500_pos()
    pos_n103 = impulse_pos(cache["GER40cash"], 8, 0, 12, 0, 40)
    pos_n115 = impulse_pos(cache["EURUSD"], 8, 0, 12, 0, 25)
    pos_eurnzd = lo_ret_pos(c_nzd, 5)

    us100_leg_148 = (-pos148).rename("us100_leg")
    jpy_leg = pos148.rename("usdjpy_leg")
    ger_leg = (-pos149).rename("ger_leg")
    eur_leg = pos149.rename("eur_leg")

    c148 = bundle(z148, pos148, [
        ("US100_US500_z40", z_us, pos_us, True),
        ("US30_US500_z40_N142", z_u30, pos_u30, True),
        ("EUR_GER40_z40_N149", z149, pos149, True),
    ])
    c148["N81_US100_leg"] = leg_clone("N81_US100_leg", us100_leg_148, pos_n81)
    c148["N142_sign"] = leg_clone("N142_sign", pos148, pos_u30)
    c148["N131_US500_day_sign_vs_US100_leg"] = leg_clone(
        "N131_US500_day_sign_vs_US100_leg", us100_leg_148, pos_n131
    )
    c148["N92_US100_NY2H_vs_US100_leg"] = leg_clone("N92_US100_NY2H_vs_US100_leg", us100_leg_148, pos_n92)
    c148["N149_sign"] = leg_clone("N149_sign", pos148, pos149)
    c148["USDJPY_L60_LO_vs_JPY_leg"] = leg_clone("USDJPY_L60_LO_vs_JPY_leg", jpy_leg, pos_l60)
    c148["US100_OVN_20d_vs_US100_leg"] = leg_clone("US100_OVN_20d_vs_US100_leg", us100_leg_148, pos_ovn)

    c149 = bundle(z149, pos149, [
        ("GER40_UK100_z40_N138", z_geuk, pos_geuk, True),
        ("USDJPY_US100_z40_N148", z148, pos148, True),
        ("US30_US500_z40_N142", z_u30, pos_u30, True),
    ])
    c149["N138_sign"] = leg_clone("N138_sign", pos149, pos_geuk)
    c149["N103_GER_day_sign_vs_GER_leg"] = leg_clone("N103_GER_day_sign_vs_GER_leg", ger_leg, pos_n103)
    c149["N142_sign"] = leg_clone("N142_sign", pos149, pos_u30)
    c149["N148_sign"] = leg_clone("N148_sign", pos149, pos148)
    c149["EURNZD_LO_5d_vs_EUR_leg"] = leg_clone("EURNZD_LO_5d_vs_EUR_leg", eur_leg, pos_eurnzd)
    c149["N115_EUR_LonAM_vs_EUR_leg"] = leg_clone("N115_EUR_LonAM_vs_EUR_leg", eur_leg, pos_n115)

    s148 = verdict(
        t148, GATE_148, "N148", "USDJPY+US100cash",
        (
            "USDJPY_US100_RISK_XS z40/±1.5 both legs 15:30→21:00; "
            f"COSTS gate 3*({COSTS_RT['USDJPY']}+{COSTS_RT['US100cash']}); swap 0; NEW_FAMILY BQ"
        ),
        history_missing=hist_148,
    )
    s148["meta"] = meta148
    s148["costs_rt"] = {"USDJPY": COSTS_RT["USDJPY"], "US100cash": COSTS_RT["US100cash"]}
    s148["rt_in_costs"] = True
    apply_clone(s148, c148)
    s148["clone"] = c148

    s149 = verdict(
        t149, GATE_149, "N149", "EURUSD+GER40cash",
        (
            "EURUSD_GER40_EUROPE_XS z40/±1.5 both legs 15:30→21:00; "
            f"COSTS gate 3*({COSTS_RT['EURUSD']}+{COSTS_RT['GER40cash']}); swap 0; NEW_FAMILY BR"
        ),
        history_missing=hist_149,
    )
    s149["meta"] = meta149
    s149["costs_rt"] = {"EURUSD": COSTS_RT["EURUSD"], "GER40cash": COSTS_RT["GER40cash"]}
    s149["rt_in_costs"] = True
    apply_clone(s149, c149)
    s149["clone"] = c149

    pd.DataFrame(t148).to_csv(OUT / "n148_trades_train.csv", index=False)
    pd.DataFrame(t149).to_csv(OUT / "n149_trades_train.csv", index=False)

    def pub(s):
        return {k: v for k, v in s.items() if k != "clone"}

    summary = {
        "N148": pub(s148),
        "N149": pub(s149),
        "N148_clones": c148,
        "N149_clones": c149,
        "gates": {"N148": round(GATE_148, 4), "N149": round(GATE_149, 4)},
        "costs_rt": COSTS_RT,
        "clone_rule": {"abs_z_corr_ge": Z_CLONE, "sign_agree_ge": AGREE_CLONE, "cover_ge": COVER_CLONE},
        "train": "2021-01-01..2023-12-31 entry dates only",
        "min_n": MIN_N,
        "swap": 0,
        "session": "15:30-21:00 CET",
        "no_thr_grid": True,
        "no_2024_in_signal": True,
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
        "# D-092.1 N148/N149 pre-screen (train 2021–2023)\n\n"
        + line("N148 USDJPY_US100_RISK_XS", s148)
        + line("N149 EURUSD_GER40_EUROPE_XS", s149)
        + "\nGates from COSTS_FTMO.csv round-trips. Session-flat so swap=0 is in the gate. "
        + "No thr-grid. No 2024+ selection. No softer session spread.\n"
    )
    (OUT / "prescreen.md").write_text(md)
    print(json.dumps({"N148": pub(s148), "N149": pub(s149), "clones148": c148, "clones149": c149}, indent=2, default=str))


if __name__ == "__main__":
    main()
