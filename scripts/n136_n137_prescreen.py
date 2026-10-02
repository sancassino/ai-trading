#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N136 BRENT_WTI_XS + N137 USDMXN_EM_CARRY_FADE.

Freeze (no thr-grid, no soft gate, no swap-credit alpha):
  N136: ratio UKOILcash/USOILcash z40 thr ±1.5 basis fade, BOTH legs,
        entry next session 15:30 CET, flat ≤21:00. Gate 18.15 bp
        = 3 × (RT_UK 2.71 + RT_US 3.34). Swap 0 (session-flat).
  N137: USDMXN ret5 ≥ +150 bp → SHORT next NY session 15:30→21:00.
        Gate 8.88 bp = 3 × RT_est 2.96. Swap 0. No long-USD leg.
        RT is NOT in COSTS_FTMO.csv — a cost PASS does not open PREREG
        until a COSTS row exists (binding RT = max(est, measured)).

Clone bar (precommitted, same numeric cut as n134; decided before the run):
  FAIL_CLONE if |z Pearson| ≥ 0.90, or
  (sign agreement on both-active ≥ 0.85 AND both-active/candidate-active ≥ 0.70).
  N136 peers: CRACK z60/thr±0.5 fade (HEATOIL_F/BRENT_F);
              UKOIL-OVN gap continuation |gap|≥40 at 08:00 (UK-leg sign).
  N136 vs N98 is structural (trade legs are the two crudes, not US100).
  N137 peers: ret5 of USDJPY, EURJPY, CADCHF, CADJPY, AUDCAD, AUDNZD, DXY.
              LO position (ret5>0 → +1) sign-agree vs N137 short-only.
Train trades only: entry date in 2021-01-01..2023-12-31. No 2024+ prices
in the signal. z uses ddof=0 (D-092.1 screen convention).
"""
from __future__ import annotations
import gzip, io, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n136_n137_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
MIN_N = 150
GATE_136 = 18.15
GATE_137 = 8.88
Z_CLONE = 0.90
AGREE_CLONE = 0.85
COVER_CLONE = 0.70


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


def load_m5(sym: str, end=TRAIN_END) -> pd.DataFrame:
    path = ROOT / "data" / "m5gz" / f"{sym}.csv.gz"
    with gzip.open(path, "rt") as f:
        first = f.readline()
        if not first.startswith("#"):
            f.seek(0)
        df = pd.read_csv(f, sep=";")
    df["time"] = pd.to_datetime(df["time"], format="%Y.%m.%d %H:%M")
    for c in ("open", "high", "low", "close"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["close"]).sort_values("time")
    return df[(df["time"] >= TRAIN_START) & (df["time"] <= end)].reset_index(drop=True)


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
    s = s[s > 0]
    return s


def zscore(sig: pd.Series, window: int) -> pd.Series:
    mu = sig.rolling(window, min_periods=window).mean()
    sd = sig.rolling(window, min_periods=window).std(ddof=0).replace(0, np.nan)
    return (sig - mu) / sd


def leg_ret_bp(g, day, side: int):
    b0 = first_bar_at(g, day, 15, 30, 15)
    b1 = last_bar_le(g, day, 21, 0)
    if b0 is None or b1 is None:
        return None
    if b1["time"] <= b0["time"]:
        return None
    p0 = float(b0["close"])
    p1 = float(b1["close"])
    if p0 <= 0 or p1 <= 0:
        return None
    return side * 1e4 * (p1 / p0 - 1.0)


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


def screen_n136(uk: pd.DataFrame, us: pd.DataFrame):
    cuk = daily_close_22(uk)
    cus = daily_close_22(us)
    both = pd.concat([cuk.rename("uk"), cus.rename("us")], axis=1).dropna()
    ratio = (both["uk"] / both["us"]).rename("brent_wti")
    z40 = zscore(ratio, 40)
    # +1 = brent cheap → long UK short US; -1 = brent rich → short UK long US
    pos = pd.Series(0.0, index=ratio.index)
    pos[z40 > 1.5] = -1.0
    pos[z40 < -1.5] = 1.0
    ukg = uk.copy()
    usg = us.copy()
    ukg["day"] = ukg["time"].dt.normalize()
    usg["day"] = usg["time"].dt.normalize()
    trades = []
    days = list(pos.index)
    for i in range(1, len(days)):
        sig_day = days[i - 1]
        day = days[i]
        if day < TRAIN_START or day > TRAIN_END:
            continue
        side = float(pos.loc[sig_day])
        if side == 0.0 or not np.isfinite(side):
            continue
        guk = ukg[ukg["day"] == day]
        gus = usg[usg["day"] == day]
        if guk.empty or gus.empty:
            continue
        # rich brent (side -1): short UK, long US. cheap (side +1): long UK, short US
        r_uk = leg_ret_bp(guk, day, int(side))
        r_us = leg_ret_bp(gus, day, int(-side))
        if r_uk is None or r_us is None:
            continue
        trades.append(
            {
                "date": str(pd.Timestamp(day).date()),
                "signal_day": str(pd.Timestamp(sig_day).date()),
                "side": int(side),  # +1 long UK / short US
                "uk_bp": r_uk,
                "us_bp": r_us,
                "bruto_bp": r_uk + r_us,
                "z40": None if not np.isfinite(z40.loc[sig_day]) else round(float(z40.loc[sig_day]), 4),
            }
        )
    return trades, ratio, z40, pos


def screen_n137(mx: pd.DataFrame):
    c = daily_close_22(mx)
    ret5 = (1e4 * (c / c.shift(5) - 1.0)).rename("ret5_bp")
    pos = pd.Series(0.0, index=c.index)
    pos[ret5 >= 150.0] = -1.0  # short USD/MXN
    g = mx.copy()
    g["day"] = g["time"].dt.normalize()
    trades = []
    days = list(pos.index)
    for i in range(1, len(days)):
        sig_day = days[i - 1]
        day = days[i]
        if day < TRAIN_START or day > TRAIN_END:
            continue
        side = float(pos.loc[sig_day])
        if side == 0.0 or not np.isfinite(side):
            continue
        gd = g[g["day"] == day]
        if gd.empty:
            continue
        bruto = leg_ret_bp(gd, day, int(side))
        if bruto is None:
            continue
        trades.append(
            {
                "date": str(pd.Timestamp(day).date()),
                "signal_day": str(pd.Timestamp(sig_day).date()),
                "side": int(side),
                "ret5_bp": None if not np.isfinite(ret5.loc[sig_day]) else round(float(ret5.loc[sig_day]), 4),
                "bruto_bp": bruto,
            }
        )
    return trades, ret5, pos


def ukoil_ovn_pos(uk: pd.DataFrame, daily: pd.Series) -> pd.Series:
    """N80-style: |gap|≥40 bp at 08:00 vs prior ≤22:00 close → continuation sign. UK leg only."""
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


def ret5_of_m5(sym: str) -> pd.Series:
    df = load_m5(sym)
    c = daily_close_22(df)
    return (1e4 * (c / c.shift(5) - 1.0)).rename(sym)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    uk = load_m5("UKOILcash")
    us = load_m5("USOILcash")
    mx = load_m5("USDMXN")

    t136, ratio, z40, pos136 = screen_n136(uk, us)
    t137, ret5_mx, pos137 = screen_n137(mx)

    # CRACK peer: HEATOIL/BRENT z60 thr ±0.5 fade. Position on the crack's own calendar.
    ho = load_daily_close("HEATOIL_F")
    br = load_daily_close("BRENT_F")
    crack = (ho / br).dropna()
    crack = crack[(crack.index >= TRAIN_START - pd.Timedelta(days=120)) & (crack.index <= TRAIN_END)]
    z60 = zscore(crack, 60)
    pos_crack = pd.Series(0.0, index=crack.index)
    pos_crack[z60 > 0.5] = -1.0
    pos_crack[z60 < -0.5] = 1.0
    # Map crack position onto the Brent/WTI session index by last crack print on or before that day
    # (no future). Then compare to N136 position (signal day, not trade day).
    crack_on_basis = pos_crack.reindex(pos136.index, method="ffill")
    z60_on_basis = z60.reindex(pos136.index, method="ffill")

    c_crack = clone_pair("CRACK_z60", z40, pos136, z60_on_basis, crack_on_basis)

    # UKOIL-OVN: compare UK-leg sign on the TRADE day to that day's gap-continuation sign.
    # Candidate position for the clone test is the UK leg side indexed by trade date.
    uk_daily = daily_close_22(uk)
    ovn = ukoil_ovn_pos(uk, uk_daily)
    uk_side_trade = pd.Series(
        {pd.Timestamp(t["date"]): float(t["side"]) for t in t136}, dtype=float
    ).sort_index()
    # inactive days explicit 0 so cover is vs candidate-active only (trade days already active)
    c_ovn = clone_pair("UKOIL_OVN_gap", None, uk_side_trade, None, ovn)

    # N98 structural note: oil morning impulse vs USOIL leg sign. Not a FAIL bar
    # (different instrument). Reported only.
    usg = us.copy()
    usg["day"] = usg["time"].dt.normalize()
    oil_am = {}
    for day, g in usg.groupby("day"):
        b0 = first_bar_at(g, day, 8, 0, 15)
        b1 = first_bar_at(g, day, 12, 0, 15)
        if b0 is None or b1 is None:
            continue
        if float(b0["close"]) <= 0:
            continue
        oil_am[day] = 1e4 * (float(b1["close"]) / float(b0["close"]) - 1.0)
    oil_am = pd.Series(oil_am).sort_index()
    us_side = pd.Series(
        {pd.Timestamp(t["date"]): float(-t["side"]) for t in t136}, dtype=float
    )
    c_n98 = clone_pair("N98_USOIL_AM_diag_not_binding", None, us_side, None, oil_am.where(oil_am.abs() >= 40, 0.0).apply(np.sign))

    s136 = verdict(
        t136, GATE_136, "N136", "UKOILcash+USOILcash",
        "BRENT_WTI_XS z40/±1.5 both legs session-flat; gate 18.15 = 3*(2.71+3.34); swap 0; NEW_FAMILY BE",
    )
    s136["clone"] = {"CRACK": c_crack, "UKOIL_OVN": c_ovn, "N98_diag": c_n98}
    s136["clone"]["N98_diag"]["binding"] = False
    s136["clone"]["N98_diag"]["note"] = "N136 does not trade US100; diag only"
    if c_crack["clone"] or c_ovn["clone"]:
        s136["verdict"] = "FAIL_CLONE"
        s136["notes"] += " | CLONE of barred CRACK and/or UKOIL-OVN — no PREREG"

    # level corr of the two ratios (extra, binding via z already)
    lvl = ratio.to_frame("bw").join(crack.rename("crack"), how="inner").dropna()
    lvl = lvl[(lvl.index >= TRAIN_START) & (lvl.index <= TRAIN_END)]
    s136["ratio_level_corr_vs_crack"] = None if len(lvl) < 30 else round(float(lvl["bw"].corr(lvl["crack"])), 4)

    # N137 peers
    peer_names = ["USDJPY", "EURJPY", "CADCHF", "CADJPY", "AUDCAD", "AUDNZD"]
    peer_clones = {}
    any_fx = False
    for sym in peer_names:
        r = ret5_of_m5(sym)
        p = pd.Series(0.0, index=r.index)
        p[r > 0] = 1.0  # 5d LO carry+mom side (barred family)
        # z-like: the ret5 series itself is the comparable signal
        rep = clone_pair(sym + "_ret5", ret5_mx, pos137, r, p)
        peer_clones[sym] = rep
        if rep["clone"]:
            any_fx = True
    dxy = load_daily_close("DXY")
    dxy_ret5 = (1e4 * (dxy / dxy.shift(5) - 1.0)).rename("DXY")
    dxy_pos = pd.Series(0.0, index=dxy_ret5.index)
    dxy_pos[dxy_ret5 > 0] = 1.0
    rep_dxy = clone_pair("DXY_ret5", ret5_mx, pos137, dxy_ret5, dxy_pos)
    peer_clones["DXY"] = rep_dxy
    if rep_dxy["clone"]:
        any_fx = True

    s137 = verdict(
        t137, GATE_137, "N137", "USDMXN",
        "USDMXN ret5≥150bp SHORT only session-flat; gate 8.88 est (not in COSTS); swap 0; NEW_FAMILY BF",
    )
    s137["clone"] = peer_clones
    s137["rt_in_costs"] = False
    s137["prereg_blocked_reason"] = None
    if any_fx:
        s137["verdict"] = "FAIL_CLONE"
        s137["notes"] += " | CLONE of barred G10 LO / DXY — no PREREG"
    elif s137["verdict"] == "PASS_may_PREREG":
        s137["verdict"] = "PASS_NO_PREREG_RT_UNMEASURED"
        s137["prereg_blocked_reason"] = (
            "VOORSTEL: PREREG only after RT is in COSTS_FTMO.csv; binding RT = max(8.88/3, U2). "
            "Do not wake U2 on the estimate."
        )

    pd.DataFrame(t136).to_csv(OUT / "n136_trades_train.csv", index=False)
    pd.DataFrame(t137).to_csv(OUT / "n137_trades_train.csv", index=False)
    summary = {
        "N136": s136,
        "N137": s137,
        "gates": {"N136": GATE_136, "N137": GATE_137, "not_the_2.34_us500_gate": True},
        "clone_rule": {"abs_z_corr_ge": Z_CLONE, "sign_agree_ge": AGREE_CLONE, "cover_ge": COVER_CLONE},
        "train": "2021-01-01..2023-12-31 entry dates only",
    }
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2))

    def line(tag, s):
        return (
            f"- **{tag}**: N={s['n']} mean={s['mean_bruto_bp']} "
            f"med={s.get('median_bruto_bp')} gate={s['gate_bp']} → **{s['verdict']}** "
            f"years={s.get('years')} L/S={s.get('n_long_basket')}/{s.get('n_short_basket')} "
            f"stress={s.get('stress_note')}\n"
        )

    (OUT / "prescreen.md").write_text(
        "# D-092.1 N136/N137 pre-screen (train 2021–2023)\n\n"
        + line("N136 BRENT_WTI_XS", s136)
        + line("N137 USDMXN_EM_CARRY_FADE", s137)
        + "\nClone detail is in prescreen.json. No thr-grid. No 2024+ selection.\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
