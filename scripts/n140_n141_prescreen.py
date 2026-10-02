#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N140 XAU_UKOIL_XS + N141 XAG_UKOIL_XS.

Freeze (no thr-grid, no soft gate, no swap-credit alpha):
  N140: ratio XAUUSD/UKOILcash z40 thr ±1.5 basis fade, BOTH legs,
        entry next session 15:30 CET, flat ≤21:00. Gate 10.62 bp
        = 3 × (RT_XAU 0.83 + RT_UKOIL 2.71). Both in COSTS. Swap 0.
  N141: ratio XAGUSD/UKOILcash z40 thr ±1.5 basis fade, BOTH legs,
        same clock. Gate 23.34 bp = 3 × (RT_XAG 5.07 + RT_UKOIL 2.71).
        Both in COSTS. Swap 0.

Clone bar (precommitted in the VOORSTELs + the barred list; decided before the run):
  FAIL_CLONE if |z Pearson| ≥ 0.90, or
  (sign agreement on both-active ≥ 0.85 AND both-active/candidate-active ≥ 0.70).
  N140 binding peers: UKOIL/USOIL z40 (N136 BRENT_WTI); XAU/XAG z40 (N75);
        SLV/GLD z40 thr±1.0 fade (N113 SILVER_GOLD); HEATOIL/BRENT z60 thr±0.5
        (N101 CRACK); UNG z40 thr±1.5 stress (N112 GAS); PPLT z40 thr±1.5
        stress (N129); N95 XAU Lon→NY continuation vs the XAU leg;
        N10 XAU mid-London fade vs the XAU leg; N80 UKOIL-OVN vs the UKOIL leg.
  N141 binding peers: the same oil/metal bars, plus N140 itself, N82 XAG
        AM-fix fade vs the XAG leg, CPER z40 stress, and COPPER/GOLD z40
        (CuAu). A twin of N140 is FAIL_CLONE even if the mean clears 23.34.

Replacement (only if N141 is a twin of N140; rules frozen here, before any PnL):
  N142-slot USDCHF_USDJPY_XS (NEW_FAMILY BK) — haven-vs-haven basis, not a
  metal and not crude. ratio USDCHF/USDJPY z40 thr ±1.5, both legs,
  15:30→21:00. Gate 5.37 = 3 × (RT_CHF 1.01 + RT_JPY 0.78), both in COSTS.
  Swap 0. Binding clone bar vs DXY z40, EURJPY z40, USDJPY ret5, USDMXN ret5
  (N137), and the XAU/UKOIL z40 just rejected. If that bar trips, FAIL_CLONE
  and do not fish a third family.

Train trades only: entry date in 2021-01-01..2023-12-31. No 2024+ prices
in the signal. z uses ddof=0.
"""
from __future__ import annotations
import gzip, io, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n140_n141_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
MIN_N = 150
GATE_140 = 10.62
GATE_141 = 23.34
GATE_REPL = 5.37  # 3 * (1.01 + 0.78); used only on the twin-replacement path
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
    return s[~s.index.duplicated(keep="last")].sort_index().dropna()


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


def screen_xs(a: pd.DataFrame, b: pd.DataFrame, h0, m0, h1, m1, name_a="a", name_b="b"):
    """z40 of close_a/close_b. +1 = a cheap → long a short b. Trade next session."""
    ca = daily_close_22(a)
    cb = daily_close_22(b)
    both = pd.concat([ca.rename("a"), cb.rename("b")], axis=1).dropna()
    ratio = (both["a"] / both["b"]).rename("ratio")
    z40 = zscore(ratio, 40)
    pos = pd.Series(0.0, index=ratio.index)
    pos[z40 > 1.5] = -1.0
    pos[z40 < -1.5] = 1.0
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


def ratio_z_pos(sym_a, sym_b, cache, window=40, thr=1.5):
    if sym_a not in cache:
        cache[sym_a] = load_m5(sym_a)
    if sym_b not in cache:
        cache[sym_b] = load_m5(sym_b)
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


def level_z_pos(sym, window, thr, stress=True):
    """stress=True: z>+thr → -1 (short the rich level). fade of a ratio uses the same sign."""
    s = load_daily_close(sym)
    s = s[(s.index >= TRAIN_START - pd.Timedelta(days=window * 3)) & (s.index <= TRAIN_END)]
    z = zscore(s, window)
    pos = pd.Series(0.0, index=s.index)
    pos[z > thr] = -1.0
    pos[z < -thr] = 1.0
    return z, pos


def align(z, pos, index):
    return z.reindex(index, method="ffill"), pos.reindex(index, method="ffill").fillna(0.0)


def on_idx(pos, index):
    return pos.reindex(index).fillna(0.0)


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


def trade_pos(trades, leg="side") -> pd.Series:
    return pd.Series(
        {pd.Timestamp(t["date"]): float(t[leg]) for t in trades}, dtype=float
    ).sort_index()


def impulse_fade(df, h0, m0, h1, m1, thr, fade: bool) -> pd.Series:
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


def ukoil_ovn_pos(uk: pd.DataFrame, daily: pd.Series) -> pd.Series:
    g = uk.copy()
    g["day"] = g["time"].dt.normalize()
    pos = pd.Series(0.0, index=daily.index)
    days = list(daily.index)
    for i in range(1, len(days)):
        day = days[i]
        cref = float(daily.iloc[i - 1])
        gd = g[g["day"] == day]
        if gd.empty or cref <= 0:
            continue
        b = first_bar_at(gd, day, 8, 0, 15)
        if b is None:
            continue
        gap = 1e4 * (float(b["close"]) / cref - 1.0)
        if gap >= 40:
            pos.loc[day] = 1.0
        elif gap <= -40:
            pos.loc[day] = -1.0
    return pos


def ret5_pos(df: pd.DataFrame, thr: float) -> tuple[pd.Series, pd.Series]:
    c = daily_close_22(df)
    ret5 = 1e4 * (c / c.shift(5) - 1.0)
    pos = pd.Series(0.0, index=c.index)
    pos[ret5 >= thr] = 1.0
    pos[ret5 <= -thr] = -1.0
    return ret5, pos


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
                else "BELOW_stress_1.5x (info only; catalog states no separate stress gate)"
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
    if hit and summary["verdict"] == "PASS_may_PREREG":
        summary["verdict"] = "FAIL_CLONE"
        summary["notes"] += " | CLONE of " + ",".join(hit) + " — no PREREG (mean had cleared)"
    elif hit:
        summary["verdict"] = "FAIL_CLONE" if summary["verdict"] != "UNDERPOWERED" else "FAIL_CLONE"
        # UNDERPOWERED that is also a clone is still a clone, not a soft pass.
        if "CLONE" not in summary["notes"]:
            summary["notes"] += " | CLONE of " + ",".join(hit) + " — no PREREG"
        summary["verdict"] = "FAIL_CLONE"
    return summary


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cache = {}
    for sym in ("XAUUSD", "XAGUSD", "UKOILcash", "USOILcash"):
        cache[sym] = load_m5(sym)

    t140, ratio140, z140, pos140, meta140 = screen_xs(
        cache["XAUUSD"], cache["UKOILcash"], 15, 30, 21, 0, "xau", "ukoil"
    )
    t141, ratio141, z141, pos141, meta141 = screen_xs(
        cache["XAGUSD"], cache["UKOILcash"], 15, 30, 21, 0, "xag", "ukoil"
    )

    z_bw, pos_bw = ratio_z_pos("UKOILcash", "USOILcash", cache, 40, 1.5)
    z_xa, pos_xa = ratio_z_pos("XAUUSD", "XAGUSD", cache, 40, 1.5)
    # N75 is one-sided z20 of ln(XAU/XAG) < -1 → long gold / short silver (= +1 on the ratio).
    ca = daily_close_22(cache["XAUUSD"])
    cag = daily_close_22(cache["XAGUSD"])
    both_m = pd.concat([ca.rename("a"), cag.rename("g")], axis=1).dropna()
    ln_r = np.log(both_m["a"] / both_m["g"])
    z20 = zscore(ln_r, 20)
    pos75 = pd.Series(0.0, index=ln_r.index)
    pos75[z20 < -1.0] = 1.0

    z_sg, pos_sg = daily_ratio_z_pos("SLV", "GLD", 40, 1.0)
    z_ck, pos_ck = daily_ratio_z_pos("HEATOIL_F", "BRENT_F", 60, 0.5)
    z_gas, pos_gas = level_z_pos("UNG", 40, 1.5)
    z_pplt, pos_pplt = level_z_pos("PPLT", 40, 1.5)
    z_cper, pos_cper = level_z_pos("CPER", 40, 1.5)
    z_cuau, pos_cuau = daily_ratio_z_pos("COPPER_F", "GOLD_F", 40, 1.5)

    n95 = impulse_fade(cache["XAUUSD"], 8, 0, 11, 0, 25.0, fade=False)
    n10 = impulse_fade(cache["XAUUSD"], 10, 30, 12, 0, 20.0, fade=True)
    n82 = impulse_fade(cache["XAGUSD"], 8, 0, 10, 30, 35.0, fade=True)
    ovn = ukoil_ovn_pos(cache["UKOILcash"], daily_close_22(cache["UKOILcash"]))

    side140 = trade_pos(t140)
    side141 = trade_pos(t141)
    xau_leg = side140
    uk_leg_140 = -side140
    xag_leg = side141
    uk_leg_141 = -side141

    def bundle(z_c, pos_c, peers):
        out = {}
        for name, z_p, pos_p, binding in peers:
            if z_p is not None and not z_p.index.equals(pos_c.index):
                z_p, pos_p = align(z_p, pos_p, pos_c.index)
            elif z_p is None:
                pos_p = on_idx(pos_p, pos_c.index)
            rec = clone_pair(name, z_c, pos_c, z_p, pos_p)
            rec["binding"] = binding
            out[name] = rec
        return out

    c140 = bundle(z140, pos140, [
        ("BRENT_WTI_N136", z_bw, pos_bw, True),
        ("XAU_XAG_z40", z_xa, pos_xa, True),
        ("N75_XAU_XAG_onesided", None, pos75, True),
        ("SILVER_GOLD_N113", z_sg, pos_sg, True),
        ("CRACK_N101", z_ck, pos_ck, True),
        ("GAS_UNG_N112", z_gas, pos_gas, True),
        ("PPLT_N129", z_pplt, pos_pplt, True),
    ])
    c140["N95_XAU_LonNY_vs_XAU_leg"] = clone_pair(
        "N95", None, xau_leg, None, on_idx(n95, xau_leg.index)
    )
    c140["N95_XAU_LonNY_vs_XAU_leg"]["binding"] = True
    c140["N10_XAU_fade_vs_XAU_leg"] = clone_pair(
        "N10", None, xau_leg, None, on_idx(n10, xau_leg.index)
    )
    c140["N10_XAU_fade_vs_XAU_leg"]["binding"] = True
    c140["UKOIL_OVN_vs_UK_leg"] = clone_pair(
        "N80", None, uk_leg_140, None, on_idx(ovn, uk_leg_140.index)
    )
    c140["UKOIL_OVN_vs_UK_leg"]["binding"] = True
    # CPER / CuAu are binding for N141 only. Reported on N140 so the twin
    # decision is not the only place they are measured.
    z_cper_a, pos_cper_a = align(z_cper, pos_cper, pos140.index)
    z_cuau_a, pos_cuau_a = align(z_cuau, pos_cuau, pos140.index)
    c140["CPER_diag"] = clone_pair("CPER", z140, pos140, z_cper_a, pos_cper_a)
    c140["CPER_diag"]["binding"] = False
    c140["CuAu_diag"] = clone_pair("CuAu", z140, pos140, z_cuau_a, pos_cuau_a)
    c140["CuAu_diag"]["binding"] = False

    c141 = bundle(z141, pos141, [
        ("N140_XAU_UKOIL", z140, pos140, True),
        ("BRENT_WTI_N136", z_bw, pos_bw, True),
        ("XAU_XAG_z40", z_xa, pos_xa, True),
        ("N75_XAU_XAG_onesided", None, pos75, True),
        ("SILVER_GOLD_N113", z_sg, pos_sg, True),
        ("CRACK_N101", z_ck, pos_ck, True),
        ("GAS_UNG_N112", z_gas, pos_gas, True),
        ("PPLT_N129", z_pplt, pos_pplt, True),
        ("CPER_N117", z_cper, pos_cper, True),
        ("CuAu_COPPER_GOLD", z_cuau, pos_cuau, True),
    ])
    c141["N82_XAG_fade_vs_XAG_leg"] = clone_pair(
        "N82", None, xag_leg, None, on_idx(n82, xag_leg.index)
    )
    c141["N82_XAG_fade_vs_XAG_leg"]["binding"] = True
    c141["UKOIL_OVN_vs_UK_leg"] = clone_pair(
        "N80", None, uk_leg_141, None, on_idx(ovn, uk_leg_141.index)
    )
    c141["UKOIL_OVN_vs_UK_leg"]["binding"] = True

    s140 = verdict(
        t140, GATE_140, "N140", "XAUUSD+UKOILcash",
        "XAU_UKOIL_XS z40/±1.5 both legs 15:30→21:00; gate 10.62 = 3*(0.83+2.71); swap 0; NEW_FAMILY BI; RTs in COSTS",
    )
    s140["meta"] = meta140
    s140["rt_in_costs"] = True
    apply_clone(s140, c140)
    s140["clone"] = c140

    s141 = verdict(
        t141, GATE_141, "N141", "XAGUSD+UKOILcash",
        "XAG_UKOIL_XS z40/±1.5 both legs 15:30→21:00; gate 23.34 = 3*(5.07+2.71); swap 0; NEW_FAMILY BJ; RTs in COSTS",
    )
    s141["meta"] = meta141
    s141["rt_in_costs"] = True
    apply_clone(s141, c141)
    s141["clone"] = c141
    twin = bool(c141["N140_XAU_UKOIL"]["clone"])
    s141["twin_of_N140"] = twin

    replacement = None
    if twin:
        cache["USDCHF"] = load_m5("USDCHF")
        cache["USDJPY"] = load_m5("USDJPY")
        cache["EURJPY"] = load_m5("EURJPY")
        cache["USDMXN"] = load_m5("USDMXN")
        cache["DXYcash"] = load_m5("DXYcash")
        t_r, ratio_r, z_r, pos_r, meta_r = screen_xs(
            cache["USDCHF"], cache["USDJPY"], 15, 30, 21, 0, "chf", "jpy"
        )
        z_dxy, pos_dxy = ratio_z_pos("DXYcash", "DXYcash", cache, 40, 1.5) if False else (None, None)
        dxy_c = daily_close_22(cache["DXYcash"])
        z_dxy = zscore(dxy_c, 40)
        pos_dxy = pd.Series(0.0, index=dxy_c.index)
        pos_dxy[z_dxy > 1.5] = -1.0
        pos_dxy[z_dxy < -1.5] = 1.0
        z_ej, pos_ej = ratio_z_pos("EURJPY", "EURJPY", cache) if False else (None, None)
        ej = daily_close_22(cache["EURJPY"])
        z_ej = zscore(ej, 40)
        pos_ej = pd.Series(0.0, index=ej.index)
        pos_ej[z_ej > 1.5] = -1.0
        pos_ej[z_ej < -1.5] = 1.0
        ret_j, pos_j = ret5_pos(cache["USDJPY"], 40.0)
        ret_m, pos_m = ret5_pos(cache["USDMXN"], 150.0)
        c_r = bundle(z_r, pos_r, [
            ("DXY_z40", z_dxy, pos_dxy, True),
            ("EURJPY_z40", z_ej, pos_ej, True),
            ("N140_XAU_UKOIL", z140, pos140, True),
            ("USDJPY_ret5", ret_j, pos_j, True),
            ("USDMXN_ret5_N137", ret_m, pos_m, True),
        ])
        s_r = verdict(
            t_r, GATE_REPL, "N142_slot", "USDCHF+USDJPY",
            "REPLACEMENT after N141 twin: USDCHF_USDJPY_XS z40/±1.5 both legs 15:30→21:00; gate 5.37 = 3*(1.01+0.78); swap 0; NEW_FAMILY BK; RTs in COSTS; not metal-oil",
        )
        s_r["meta"] = meta_r
        s_r["rt_in_costs"] = True
        s_r["triggered_because"] = "N141 twin of N140"
        apply_clone(s_r, c_r)
        s_r["clone"] = c_r
        replacement = {"summary": s_r, "trades": t_r}

    pd.DataFrame(t140).to_csv(OUT / "n140_trades_train.csv", index=False)
    pd.DataFrame(t141).to_csv(OUT / "n141_trades_train.csv", index=False)
    if replacement is not None:
        pd.DataFrame(replacement["trades"]).to_csv(OUT / "n142_slot_usdchf_usdjpy_trades_train.csv", index=False)

    def pub(s):
        return {k: v for k, v in s.items() if k != "clone"}

    summary = {
        "N140": pub(s140),
        "N141": pub(s141),
        "N140_clones": c140,
        "N141_clones": c141,
        "replacement": None if replacement is None else pub(replacement["summary"]),
        "replacement_clones": None if replacement is None else replacement["summary"]["clone"],
        "gates": {"N140": GATE_140, "N141": GATE_141, "replacement_if_twin": GATE_REPL},
        "clone_rule": {"abs_z_corr_ge": Z_CLONE, "sign_agree_ge": AGREE_CLONE, "cover_ge": COVER_CLONE},
        "train": "2021-01-01..2023-12-31 entry dates only",
        "min_n": MIN_N,
        "swap": 0,
        "session": "15:30-21:00 CET",
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
        "# D-092.1 N140/N141 pre-screen (train 2021–2023)\n\n"
        + line("N140 XAU_UKOIL_XS", s140)
        + line("N141 XAG_UKOIL_XS", s141)
    )
    if replacement is not None:
        md += line("REPL USDCHF_USDJPY_XS", replacement["summary"])
    md += "\nClone detail is in prescreen.json. No thr-grid. No 2024+ selection.\n"
    (OUT / "prescreen.md").write_text(md)
    print(json.dumps({
        "N140": pub(s140),
        "N140_clones": {k: {kk: vv for kk, vv in v.items()} for k, v in c140.items()},
        "N141": pub(s141),
        "N141_clones": c141,
        "replacement": None if replacement is None else pub(replacement["summary"]),
        "replacement_clones": None if replacement is None else replacement["summary"]["clone"],
    }, indent=2, default=str))


if __name__ == "__main__":
    main()
