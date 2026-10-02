#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N158 USOIL NY-impulse fade + N159 GER40 Europe-close fade.

Gates frozen from COSTS_FTMO.csv before any train PnL.

  N158 USOILcash RT 3.34 → gate 3× = 10.02 bp. One oil leg. Session-flat.
  N159 GER40cash RT 0.72 → gate 3× = 2.16 bp. One index leg. Session-flat.

Swap in the gate is 0. Neither book is held overnight (USOIL short swap is 24.53).

Thresholds frozen at ±40 bp. No thr-grid. No soft-pass.

Clone bar (precommitted in the VOORSTEL; sign only — these books have no ratio z):
  FAIL_CLONE if sign agree >= 0.85 AND cover >= 0.70.
  A clone is not a PASS.

N158 binding peers (trade-date side):
  N22 UKOIL Lon-AM fade day-sign, N43 UKOIL NY-open continuation,
  N80 UKOIL overnight-gap continuation, N98 USOIL morning sign,
  N136 USOIL leg, N155 UKOIL leg, CRACK equity day-sign.
  An overnight-oil clone is FAIL_CLONE.

N159 binding peers (trade-date side):
  GER leg of N156, GER leg of N149, GER leg of N154, GER leg of N138,
  N103 GER-AM impulse sign, negative of N40 continuation,
  N21 GER afternoon-fade day-sign (GER40-session clone).
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n158_n159_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
MIN_N = 150
AGREE_CLONE = 0.85
COVER_CLONE = 0.70

COSTS_RT = {
    "USOILcash": 3.34,
    "GER40cash": 0.72,
}
GATE_158 = 3.0 * COSTS_RT["USOILcash"]  # 10.02
GATE_159 = 3.0 * COSTS_RT["GER40cash"]  # 2.16


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


def by_day(df: pd.DataFrame) -> dict:
    d = df.copy()
    d["day"] = d["time"].dt.normalize()
    return {day: g for day, g in d.groupby("day", sort=False)}


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


def px(bar):
    if bar is None:
        return None
    p = float(bar["close"])
    return p if p > 0 else None


def impulse_bp(g, day, h0, m0, h1, m1):
    b0 = first_bar_at(g, day, h0, m0, 15)
    b1 = first_bar_at(g, day, h1, m1, 15)
    if b0 is None or b1 is None or b1["time"] <= b0["time"]:
        return None, None, None
    p0, p1 = px(b0), px(b1)
    if p0 is None or p1 is None:
        return None, None, None
    return 1e4 * (p1 / p0 - 1.0), b0, b1


def screen_fade(df, sig, entry, exit_hm, thr=40.0, entry_is_signal_end=False):
    """Same-day fade. side +1 = long. sig=(h0,m0,h1,m1). entry=(h,m) unless entry_is_signal_end."""
    groups = by_day(df)
    trades = []
    pos = {}
    n_impulse = 0
    n_skip = 0
    h0, m0, h1, m1 = sig
    xh, xm = exit_hm
    for day in sorted(groups):
        if day < TRAIN_START or day > TRAIN_END:
            continue
        g = groups[day]
        move, _b0, b1 = impulse_bp(g, day, h0, m0, h1, m1)
        if move is None or abs(move) < thr:
            continue
        n_impulse += 1
        side = -1 if move > 0 else 1
        if entry_is_signal_end:
            ent = b1
        else:
            eh, em = entry
            ent = first_bar_at(g, day, eh, em, 15)
        ex = last_bar_le(g, day, xh, xm)
        if ent is None or ex is None or ex["time"] <= ent["time"]:
            n_skip += 1
            continue
        p_ent, p_ex = px(ent), px(ex)
        if p_ent is None or p_ex is None:
            n_skip += 1
            continue
        bruto = side * 1e4 * (p_ex / p_ent - 1.0)
        # overnight guard: exit must be the same calendar day as entry
        if pd.Timestamp(ex["time"]).normalize() != pd.Timestamp(ent["time"]).normalize():
            n_skip += 1
            continue
        pos[day] = float(side)
        trades.append(
            {
                "date": str(pd.Timestamp(day).date()),
                "side": int(side),
                "impulse_bp": round(float(move), 4),
                "entry": str(ent["time"]),
                "exit": str(ex["time"]),
                "bruto_bp": float(bruto),
            }
        )
    meta = {
        "n_impulse_days": n_impulse,
        "n_skip_missing_bar": n_skip,
        "n_trades": len(trades),
        "swap_bp": 0,
        "overnight": False,
    }
    series = pd.Series(pos, dtype=float).sort_index()
    return trades, series, meta


def impulse_sign(df, h0, m0, h1, m1, thr, fade=False) -> pd.Series:
    """Same-day sign. fade=True → opposite of the impulse (the trade side)."""
    groups = by_day(df)
    pos = {}
    for day, g in groups.items():
        if day < TRAIN_START or day > TRAIN_END:
            continue
        move, _, _ = impulse_bp(g, day, h0, m0, h1, m1)
        if move is None or abs(move) < thr:
            continue
        s = 1.0 if move > 0 else -1.0
        pos[day] = -s if fade else s
    return pd.Series(pos, dtype=float).sort_index()


def ukoil_ovn_pos(uk: pd.DataFrame) -> pd.Series:
    """N80: |gap|>=40 bp at 08:00 vs prior <=22:00 close → continuation that day."""
    daily = daily_close_22(uk)
    g = uk.copy()
    g["day"] = g["time"].dt.normalize()
    pos = {}
    days = list(daily.index)
    for i in range(1, len(days)):
        day = days[i]
        if day < TRAIN_START or day > TRAIN_END:
            continue
        cref = float(daily.iloc[i - 1])
        gd = g[g["day"] == day]
        if gd.empty or cref <= 0:
            continue
        b = first_bar_at(gd, day, 8, 0, 15)
        if b is None:
            continue
        gap = 1e4 * (float(b["close"]) / cref - 1.0)
        if gap >= 40:
            pos[day] = 1.0
        elif gap <= -40:
            pos[day] = -1.0
    return pd.Series(pos, dtype=float).sort_index()


def ratio_pos(cache, sym_a, sym_b, window=40, thr=1.5):
    """Signal-day position. +1 = long A / short B (z < -thr)."""
    ca = daily_close_22(cache[sym_a])
    cb = daily_close_22(cache[sym_b])
    both = pd.concat([ca.rename("a"), cb.rename("b")], axis=1).dropna()
    ratio = both["a"] / both["b"]
    z = zscore(ratio, window)
    pos = pd.Series(0.0, index=ratio.index)
    pos[z > thr] = -1.0
    pos[z < -thr] = 1.0
    return z, pos


def to_trade_date(pos: pd.Series) -> pd.Series:
    """Signal on index day t is the side held on the next index day."""
    idx = list(pos.index)
    out = {}
    for i in range(len(idx) - 1):
        trade = idx[i + 1]
        if trade < TRAIN_START or trade > TRAIN_END:
            continue
        out[trade] = float(pos.iloc[i])
    s = pd.Series(out, dtype=float)
    return s[~s.index.duplicated(keep="last")].sort_index()


def crack_trade_pos():
    ho = load_daily_close("HEATOIL_F")
    br = load_daily_close("BRENT_F")
    crack = (ho / br).dropna()
    crack = crack[(crack.index >= TRAIN_START - pd.Timedelta(days=180)) & (crack.index <= TRAIN_END)]
    z60 = zscore(crack, 60)
    pos = pd.Series(0.0, index=crack.index)
    pos[z60 > 0.5] = -1.0
    pos[z60 < -0.5] = 1.0
    return to_trade_date(pos)


def clone_sign(name, cand: pd.Series, peer: pd.Series, binding=True) -> dict:
    """Agree/cover on the candidate's trade dates. Peer 0 or missing = not active."""
    c = cand.astype(float)
    p = peer.reindex(c.index).fillna(0.0)
    active = c[c != 0]
    both_on = active[p.reindex(active.index).fillna(0.0) != 0]
    pp = p.reindex(both_on.index)
    agree = float((both_on == pp).mean()) if len(both_on) else None
    cover = float(len(both_on) / len(active)) if len(active) else None
    is_clone = (
        agree is not None
        and cover is not None
        and agree >= AGREE_CLONE
        and cover >= COVER_CLONE
    )
    return {
        "peer": name,
        "sign_agree_both_active": None if agree is None else round(agree, 4),
        "both_active_over_cand": None if cover is None else round(cover, 4),
        "n_cand_active": int(len(active)),
        "n_both_active": int(len(both_on)),
        "clone": bool(is_clone and binding),
        "clone_raw": bool(is_clone),
        "binding": binding,
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
            "n_long": int(sum(1 for t in trades if t["side"] > 0)),
            "n_short": int(sum(1 for t in trades if t["side"] < 0)),
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


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    need = (
        "USOILcash", "UKOILcash", "GER40cash", "US100cash", "US30cash",
        "XAUUSD", "EURUSD", "UK100cash",
    )
    warm = TRAIN_START - pd.Timedelta(days=120)
    cache = {s: load_m5(s, warm, TRAIN_END) for s in need}

    def train_days(sym):
        t = cache[sym]["time"]
        m = (t >= TRAIN_START) & (t <= TRAIN_END)
        return int(t[m].dt.normalize().nunique())

    td = {s: train_days(s) for s in need}

    t158, pos158, meta158 = screen_fade(
        cache["USOILcash"],
        sig=(15, 30, 17, 0),
        entry=(17, 0),
        exit_hm=(21, 0),
        thr=40.0,
        entry_is_signal_end=True,
    )
    t159, pos159, meta159 = screen_fade(
        cache["GER40cash"],
        sig=(12, 0, 15, 0),
        entry=(15, 30),
        exit_hm=(17, 30),
        thr=40.0,
        entry_is_signal_end=False,
    )
    meta158["train_days"] = td["USOILcash"]
    meta158["session"] = "signal 15:30→17:00 entry at 17:00 flat 21:00 CET"
    meta158["rt_in_costs"] = True
    meta159["train_days"] = td["GER40cash"]
    meta159["session"] = "signal 12:00→15:00 entry 15:30 flat 17:30 CET"
    meta159["rt_in_costs"] = True

    # --- peers, trade-date sides ---
    n22 = impulse_sign(cache["UKOILcash"], 9, 0, 12, 0, 40.0, fade=True)
    n43 = impulse_sign(cache["UKOILcash"], 15, 30, 16, 0, 50.0, fade=False)
    n80 = ukoil_ovn_pos(cache["UKOILcash"])
    n98 = impulse_sign(cache["USOILcash"], 8, 0, 12, 0, 40.0, fade=False)
    _, pos136 = ratio_pos(cache, "UKOILcash", "USOILcash")  # +1 long UK / short US
    usoil_leg_136 = to_trade_date(-pos136)
    _, pos155 = ratio_pos(cache, "US30cash", "UKOILcash")  # +1 long US30 / short UK
    ukoil_leg_155 = to_trade_date(-pos155)
    crack = crack_trade_pos()

    _, pos156 = ratio_pos(cache, "XAUUSD", "GER40cash")  # +1 long XAU / short GER
    ger_156 = to_trade_date(-pos156)
    _, pos149 = ratio_pos(cache, "EURUSD", "GER40cash")  # +1 long EUR / short GER
    ger_149 = to_trade_date(-pos149)
    _, pos154 = ratio_pos(cache, "US100cash", "GER40cash")  # +1 long US100 / short GER
    ger_154 = to_trade_date(-pos154)
    _, pos138 = ratio_pos(cache, "GER40cash", "UK100cash")  # +1 long GER / short UK
    ger_138 = to_trade_date(pos138)
    n103 = impulse_sign(cache["GER40cash"], 8, 0, 12, 0, 40.0, fade=False)
    n40 = impulse_sign(cache["GER40cash"], 9, 30, 12, 0, 40.0, fade=False)
    n21 = impulse_sign(cache["GER40cash"], 9, 0, 16, 30, 50.0, fade=True)
    n9 = impulse_sign(cache["GER40cash"], 9, 0, 10, 30, 40.0, fade=True)

    c158 = {
        "N22_UKOIL_LonAM_fade": clone_sign("N22_UKOIL_LonAM_fade", pos158, n22),
        "N43_UKOIL_NY_cont": clone_sign("N43_UKOIL_NY_cont", pos158, n43),
        "N80_UKOIL_OVN": clone_sign("N80_UKOIL_OVN", pos158, n80),
        "N98_USOIL_morning": clone_sign("N98_USOIL_morning", pos158, n98),
        "N136_USOIL_leg": clone_sign("N136_USOIL_leg", pos158, usoil_leg_136),
        "N155_UKOIL_leg": clone_sign("N155_UKOIL_leg", pos158, ukoil_leg_155),
        "CRACK_z60": clone_sign("CRACK_z60", pos158, crack),
    }
    c159 = {
        "N156_GER_leg": clone_sign("N156_GER_leg", pos159, ger_156),
        "N149_GER_leg": clone_sign("N149_GER_leg", pos159, ger_149),
        "N154_GER_leg": clone_sign("N154_GER_leg", pos159, ger_154),
        "N138_GER_leg": clone_sign("N138_GER_leg", pos159, ger_138),
        "N103_GER_AM": clone_sign("N103_GER_AM", pos159, n103),
        "neg_N40_continuation": clone_sign("neg_N40_continuation", pos159, -n40),
        "N21_GER_afternoon_fade": clone_sign("N21_GER_afternoon_fade", pos159, n21),
        "N9_GER_morning_fade_info": clone_sign("N9_GER_morning_fade_info", pos159, n9, binding=False),
    }

    s158 = verdict(
        t158, GATE_158, "N158", "USOILcash",
        "USOIL_NY_IMPULSE_FADE ±40 15:30→17:00 entry 17:00 flat 21:00; "
        f"COSTS gate 3*{COSTS_RT['USOILcash']}; swap 0; one leg; NEW_FAMILY CA",
        history_missing=td["USOILcash"] < 150,
    )
    s158["meta"] = meta158
    s158["costs_rt"] = COSTS_RT["USOILcash"]
    s158["rt_in_costs"] = True
    apply_clone(s158, c158)
    s158["clone"] = c158

    s159 = verdict(
        t159, GATE_159, "N159", "GER40cash",
        "GER40_EUROPE_CLOSE_FADE ±40 12:00→15:00 entry 15:30 flat 17:30; "
        f"COSTS gate 3*{COSTS_RT['GER40cash']}; swap 0; one leg; NEW_FAMILY CB",
        history_missing=td["GER40cash"] < 150,
    )
    s159["meta"] = meta159
    s159["costs_rt"] = COSTS_RT["GER40cash"]
    s159["rt_in_costs"] = True
    apply_clone(s159, c159)
    s159["clone"] = c159

    pd.DataFrame(t158).to_csv(OUT / "n158_trades_train.csv", index=False)
    pd.DataFrame(t159).to_csv(OUT / "n159_trades_train.csv", index=False)

    def pub(s):
        return {k: v for k, v in s.items() if k != "clone"}

    summary = {
        "N158": pub(s158),
        "N159": pub(s159),
        "N158_clones": c158,
        "N159_clones": c159,
        "gates": {"N158": round(GATE_158, 4), "N159": round(GATE_159, 4)},
        "costs_rt": COSTS_RT,
        "clone_rule": {
            "sign_agree_ge": AGREE_CLONE,
            "cover_ge": COVER_CLONE,
            "z_corr": "not used; one-leg books have no ratio z (VOORSTEL bar is sign×cover)",
        },
        "train": "2021-01-01..2023-12-31 entry dates only",
        "min_n": MIN_N,
        "swap": 0,
        "no_thr_grid": True,
        "no_2024_in_signal": True,
        "no_inline_replacement": True,
        "gate_source": "COSTS_FTMO.csv roundtrip_intraday_bp; session-flat so swap=0",
        "train_days": td,
    }
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2, default=str))

    def line(tag, s):
        return (
            f"- **{tag}**: N={s['n']} mean={s['mean_bruto_bp']} "
            f"med={s.get('median_bruto_bp')} gate={s['gate_bp']} "
            f"→ **{s['verdict']}** years={s.get('years')} "
            f"L/S={s.get('n_long')}/{s.get('n_short')} "
            f"hits={s.get('clone_hits')} meta={s.get('meta')}\n"
        )

    md = (
        "# D-092.1 N158/N159 pre-screen (train 2021–2023)\n\n"
        + line("N158 USOIL_NY_IMPULSE_FADE", s158)
        + line("N159 GER40_EUROPE_CLOSE_FADE", s159)
        + "\nGates from COSTS_FTMO.csv round-trips. Session-flat so swap=0 is in the gate. "
        + "No thr-grid. No 2024+ selection. No overnight. No second leg.\n"
    )
    (OUT / "prescreen.md").write_text(md)
    print(json.dumps({"N158": pub(s158), "N159": pub(s159)}, indent=2, default=str))
    print("---CLONES158---")
    for k, v in c158.items():
        print(k, {kk: v[kk] for kk in ("sign_agree_both_active", "both_active_over_cand", "n_both_active", "clone", "binding")})
    print("---CLONES159---")
    for k, v in c159.items():
        print(k, {kk: v[kk] for kk in ("sign_agree_both_active", "both_active_over_cand", "n_both_active", "clone", "binding")})


if __name__ == "__main__":
    main()
