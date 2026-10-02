#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N138 GER40_UK100_XS + N139 JP225_HK50_ASIA_XS.

Freeze (no thr-grid, no soft gate, no swap-credit alpha):
  N138: ratio GER40/UK100 z40 thr ±1.5 basis fade, BOTH legs,
        entry next session 15:30 CET, flat ≤21:00. Gate 6.42 bp
        = 3 × (RT_GER 0.72 + RT_UK est 1.42). Swap 0 (session-flat).
        UK100 RT is NOT in COSTS_FTMO.csv.
  N139: ratio JP225/HK50 z40 thr ±1.5 basis fade, BOTH legs,
        entry next session 03:00 CET, flat ≤08:00. Gate 12.42 bp
        = 3 × (RT_JP est 1.51 + RT_HK est 2.63). Swap 0.
        Neither RT is in COSTS_FTMO.csv.

Clone bar (precommitted, same numeric cut as n136; decided before the run):
  FAIL_CLONE if |z Pearson| ≥ 0.90, or
  (sign agreement on both-active ≥ 0.85 AND both-active/candidate-active ≥ 0.70).
  N138 binding peers: US100/US500 ratio z40; GER/FRA, UK/FRA, EU50/GER, EU50/UK
  ratio z40 (EU index basis twins); N103 GER 08–12 impulse sign vs GER-leg;
  N107 UK 08–12 impulse sign vs UK-leg.
  N139 binding peers: GER40/UK100 ratio z40; JP/AUS and HK/AUS ratio z40;
  N105 JP Tokyo-AM impulse vs JP-leg; N108 AUS Asia-AM impulse vs JP-leg;
  N64 HK50 ret20<0 short vs HK-leg (diag+binding if the numeric bar trips).
Train trades only: entry date in 2021-01-01..2023-12-31. No 2024+ prices
in the signal. z uses ddof=0.
"""
from __future__ import annotations
import gzip, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n138_n139_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
MIN_N = 150
GATE_138 = 6.42
GATE_139 = 12.42
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


def by_day(df: pd.DataFrame) -> dict:
    d = df.copy()
    d["day"] = d["time"].dt.normalize()
    return {day: g for day, g in d.groupby("day", sort=False)}


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
                "side": int(side),  # +1 long A / short B
                f"{name_a}_bp": r_a,
                f"{name_b}_bp": r_b,
                "bruto_bp": r_a + r_b,
                "z40": None if not np.isfinite(z40.loc[sig_day]) else round(float(z40.loc[sig_day]), 4),
            }
        )
    meta = {"n_signal_days": n_sig, "n_skip_missing_bar": n_skip_bar}
    return trades, ratio, z40, pos, meta


def ratio_pos(sym_a: str, sym_b: str, cache: dict):
    if sym_a not in cache:
        cache[sym_a] = load_m5(sym_a)
    if sym_b not in cache:
        cache[sym_b] = load_m5(sym_b)
    ca = daily_close_22(cache[sym_a])
    cb = daily_close_22(cache[sym_b])
    both = pd.concat([ca.rename("a"), cb.rename("b")], axis=1).dropna()
    ratio = both["a"] / both["b"]
    z40 = zscore(ratio, 40)
    pos = pd.Series(0.0, index=ratio.index)
    pos[z40 > 1.5] = -1.0
    pos[z40 < -1.5] = 1.0
    return z40, pos


def impulse_side(df: pd.DataFrame, h0, m0, h1, m1, thr=40.0, fallback=None) -> pd.Series:
    """Same-day morning impulse sign. +1 continuation long. 0 if |move|<thr or bars missing."""
    groups = by_day(df)
    pos = {}
    for day, g in groups.items():
        b0 = first_bar_at(g, day, h0, m0, 15)
        if b0 is None and fallback is not None:
            fh0, fm0, fh1, fm1 = fallback
            t0 = day + pd.Timedelta(hours=fh0, minutes=fm0)
            t1 = day + pd.Timedelta(hours=fh1, minutes=fm1)
            win = g[(g["time"] >= t0) & (g["time"] <= t1)]
            b0 = win.iloc[0] if len(win) else None
        b1 = first_bar_at(g, day, h1, m1, 15)
        if b0 is None or b1 is None:
            continue
        if b1["time"] <= b0["time"]:
            continue
        p0 = float(b0["close"])
        p1 = float(b1["close"])
        if p0 <= 0 or p1 <= 0:
            continue
        move = 1e4 * (p1 / p0 - 1.0)
        if move >= thr:
            pos[day] = 1.0
        elif move <= -thr:
            pos[day] = -1.0
    return pd.Series(pos, dtype=float).sort_index()


def hk_tsmom_pos(df: pd.DataFrame) -> pd.Series:
    """N64: ret20<0 → SHORT for the next 10 sessions, non-overlapping. Position on each hold day = -1."""
    c = daily_close_22(df)
    dates = list(c.index)
    pos = pd.Series(0.0, index=c.index)
    i = 20
    while i + 10 < len(dates):
        c_t = float(c.iloc[i])
        c_lb = float(c.iloc[i - 20])
        if c_lb <= 0 or c_t <= 0:
            i += 1
            continue
        ret20 = c_t / c_lb - 1.0
        if ret20 < 0:
            for k in range(1, 11):
                pos.iloc[i + k] = -1.0
            i += 10
        else:
            i += 1
    return pos


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


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cache = {}
    for sym in (
        "GER40cash", "UK100cash", "JP225cash", "HK50cash",
        "US100cash", "US500cash", "FRA40cash", "EU50cash",
        "US30cash", "AUS200cash",
    ):
        cache[sym] = load_m5(sym)

    t138, ratio138, z138, pos138, meta138 = screen_xs(
        cache["GER40cash"], cache["UK100cash"], 15, 30, 21, 0, "ger", "uk"
    )
    t139, ratio139, z139, pos139, meta139 = screen_xs(
        cache["JP225cash"], cache["HK50cash"], 3, 0, 8, 0, "jp", "hk"
    )

    # --- N138 clones ---
    z_us, pos_us = ratio_pos("US100cash", "US500cash", cache)
    z_gf, pos_gf = ratio_pos("GER40cash", "FRA40cash", cache)
    z_uf, pos_uf = ratio_pos("UK100cash", "FRA40cash", cache)
    z_eg, pos_eg = ratio_pos("EU50cash", "GER40cash", cache)
    z_eu, pos_eu = ratio_pos("EU50cash", "UK100cash", cache)

    # Basket side on the TRADE date (long GER = +1). Signal-day z stays on its own index.
    side138 = trade_pos(t138, "side")
    # GER-leg sign == basket side; UK-leg sign == -basket side
    ger_leg = side138
    uk_leg = -side138

    def on_idx(pos, index):
        # Sparse impulse series omit inactive days. Fill 0 so cover is
        # both-active / candidate-active, not 1.0 by construction.
        return pos.reindex(index).fillna(0.0)

    n103 = impulse_side(cache["GER40cash"], 8, 0, 12, 0, 40.0)
    n107 = impulse_side(cache["UK100cash"], 8, 0, 12, 0, 40.0)
    # other EU session continuations (same 40bp morning impulse, own index)
    fra_am = impulse_side(cache["FRA40cash"], 8, 0, 12, 0, 40.0)
    eu_am = impulse_side(cache["EU50cash"], 8, 0, 12, 0, 40.0)

    c138 = {
        "US100_US500_z40": clone_pair("US100/US500", z138, pos138, z_us, pos_us),
        "GER_FRA_z40": clone_pair("GER/FRA", z138, pos138, z_gf, pos_gf),
        "UK_FRA_z40": clone_pair("UK/FRA", z138, pos138, z_uf, pos_uf),
        "EU50_GER_z40": clone_pair("EU50/GER", z138, pos138, z_eg, pos_eg),
        "EU50_UK_z40": clone_pair("EU50/UK", z138, pos138, z_eu, pos_eu),
        "N103_GER_AM_vs_GER_leg": clone_pair("N103", None, ger_leg, None, on_idx(n103, ger_leg.index)),
        "N107_UK_AM_vs_UK_leg": clone_pair("N107", None, uk_leg, None, on_idx(n107, uk_leg.index)),
        "FRA_AM_vs_GER_leg": clone_pair("FRA_AM", None, ger_leg, None, on_idx(fra_am, ger_leg.index)),
        "EU50_AM_vs_GER_leg": clone_pair("EU50_AM", None, ger_leg, None, on_idx(eu_am, ger_leg.index)),
    }
    # Also align signal-day basket pos (not only trade-day) vs impulse on the signal day.
    c138["N103_vs_signal_day_pos"] = clone_pair("N103_sigday", None, pos138, None, on_idx(n103, pos138.index))
    c138["N107_vs_signal_day_UK"] = clone_pair("N107_sigday", None, -pos138, None, on_idx(n107, pos138.index))

    clone138 = any(v["clone"] for v in c138.values())

    s138 = verdict(
        t138, GATE_138, "N138", "GER40cash+UK100cash",
        "GER40_UK100_XS z40/±1.5 both legs 15:30→21:00; gate 6.42 = 3*(0.72+1.42 est); swap 0; NEW_FAMILY BG; UK100 RT not in COSTS",
    )
    s138["meta"] = meta138
    s138["clone"] = c138
    s138["rt_uk_in_costs"] = False
    if clone138:
        peers = [k for k, v in c138.items() if v["clone"]]
        s138["verdict"] = "FAIL_CLONE"
        s138["notes"] += " | CLONE of " + ",".join(peers) + " — no PREREG"

    # --- N139 clones ---
    z_ja, pos_ja = ratio_pos("JP225cash", "AUS200cash", cache)
    z_ha, pos_ha = ratio_pos("HK50cash", "AUS200cash", cache)
    n105 = impulse_side(
        cache["JP225cash"], 0, 0, 6, 0, 40.0, fallback=(0, 0, 1, 15)
    )
    n108 = impulse_side(
        cache["AUS200cash"], 1, 0, 7, 0, 40.0, fallback=(1, 0, 1, 30)
    )
    # Asia-morning impulse inside the same 03:00–06:00 window (session clone of the clock)
    jp_am = impulse_side(cache["JP225cash"], 3, 0, 6, 0, 40.0)
    hk_am = impulse_side(cache["HK50cash"], 3, 0, 6, 0, 40.0)
    n64 = hk_tsmom_pos(cache["HK50cash"])

    side139 = trade_pos(t139, "side")  # +1 long JP / short HK
    jp_leg = side139
    hk_leg = -side139

    c139 = {
        "GER_UK_z40": clone_pair("N138_ratio", z139, pos139, z138, pos138),
        "JP_AUS_z40": clone_pair("JP/AUS", z139, pos139, z_ja, pos_ja),
        "HK_AUS_z40": clone_pair("HK/AUS", z139, pos139, z_ha, pos_ha),
        "N105_JP_Tokyo_vs_JP_leg": clone_pair("N105", None, jp_leg, None, on_idx(n105, jp_leg.index)),
        "N108_AUS_Asia_vs_JP_leg": clone_pair("N108", None, jp_leg, None, on_idx(n108, jp_leg.index)),
        "JP_0300_0600_vs_JP_leg": clone_pair("JP_AM_03_06", None, jp_leg, None, on_idx(jp_am, jp_leg.index)),
        "HK_0300_0600_vs_HK_leg": clone_pair("HK_AM_03_06", None, hk_leg, None, on_idx(hk_am, hk_leg.index)),
        "N64_HK_TSMOM_vs_HK_leg": clone_pair("N64", None, hk_leg, None, n64),
    }
    clone139 = any(v["clone"] for v in c139.values())

    s139 = verdict(
        t139, GATE_139, "N139", "JP225cash+HK50cash",
        "JP225_HK50_ASIA_XS z40/±1.5 both legs 03:00→08:00; gate 12.42 = 3*(1.51+2.63 est); swap 0; NEW_FAMILY BH; RTs not in COSTS",
    )
    s139["meta"] = meta139
    s139["clone"] = c139
    s139["rt_in_costs"] = False
    if clone139:
        peers = [k for k, v in c139.items() if v["clone"]]
        s139["verdict"] = "FAIL_CLONE"
        s139["notes"] += " | CLONE of " + ",".join(peers) + " — no PREREG"
    elif s139["verdict"] == "PASS_may_PREREG":
        # precommitted: PREREG only after both RTs are in COSTS
        s139["verdict"] = "PASS_NO_PREREG_RT_UNMEASURED"
        s139["prereg_blocked_reason"] = (
            "VOORSTEL: PREREG only after both RTs are in COSTS_FTMO.csv; "
            "binding RT = max(est, U2) on each leg. Do not wake U2 on the estimate."
        )
    if s138["verdict"] == "PASS_may_PREREG":
        s138["verdict"] = "PASS_NO_PREREG_RT_UNMEASURED"
        s138["prereg_blocked_reason"] = (
            "VOORSTEL: PREREG only after UK100 RT is in COSTS_FTMO.csv; "
            "binding RT = max(1.42, U2). Do not wake U2 on the estimate."
        )

    pd.DataFrame(t138).to_csv(OUT / "n138_trades_train.csv", index=False)
    pd.DataFrame(t139).to_csv(OUT / "n139_trades_train.csv", index=False)
    summary = {
        "N138": s138,
        "N139": s139,
        "gates": {"N138": GATE_138, "N139": GATE_139, "not_the_2.34_us500_gate": True},
        "clone_rule": {"abs_z_corr_ge": Z_CLONE, "sign_agree_ge": AGREE_CLONE, "cover_ge": COVER_CLONE},
        "train": "2021-01-01..2023-12-31 entry dates only",
        "min_n": MIN_N,
    }
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2))

    def line(tag, s):
        return (
            f"- **{tag}**: N={s['n']} mean={s['mean_bruto_bp']} "
            f"med={s.get('median_bruto_bp')} gate={s['gate_bp']} → **{s['verdict']}** "
            f"years={s.get('years')} L/S={s.get('n_long_basket')}/{s.get('n_short_basket')} "
            f"stress={s.get('stress_note')} meta={s.get('meta')}\n"
        )

    (OUT / "prescreen.md").write_text(
        "# D-092.1 N138/N139 pre-screen (train 2021–2023)\n\n"
        + line("N138 GER40_UK100_XS", s138)
        + line("N139 JP225_HK50_ASIA_XS", s139)
        + "\nClone detail is in prescreen.json. No thr-grid. No 2024+ selection.\n"
    )
    print(json.dumps({
        "N138": {k: s138[k] for k in s138 if k != "clone"},
        "N138_clones": {k: v for k, v in c138.items()},
        "N139": {k: s139[k] for k in s139 if k != "clone"},
        "N139_clones": c139,
    }, indent=2))


if __name__ == "__main__":
    main()
