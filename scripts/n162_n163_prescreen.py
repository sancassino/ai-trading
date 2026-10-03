#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N162 US500 cash-close fade + N163 AUD NY-impulse fade.

Gates frozen from COSTS_FTMO.csv before any train PnL. Honest RT equals the filed gate.

  N162 US500cash RT 0.78 → gate 3× = 2.34 bp. One index leg. Session-flat. Swap 0.
  N163 AUDUSD RT 1.22 → gate 3× = 3.66 bp. One FX major. Session-flat. Swap 0.
       Not the US500 2.34 gate.

Thresholds frozen (±25 / ±20). No thr-grid. No soft-pass. N<150 is UNDERPOWERED.

Clone bar (filed future bar, sign agree >= 0.85 AND cover >= 0.70):
  N162 vs N24, N92, N87, N159, N161 US100 side, and the barred US30/US100
       same-window fade (not a separate screen).
  N163 vs N92, N91 AUD sign, N146 AUD leg, N84 AUDNZD AUD-leg, the AUD
       Asia-range fade used as the GS02 proxy (00:00→07:00 ±20), and the
       barred NZDUSD same-window fade.
A clone is not a PASS.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n162_n163_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
MIN_N = 150
AGREE_CLONE = 0.85
COVER_CLONE = 0.70

COSTS_RT = {"US500cash": 0.78, "AUDUSD": 1.22}
GATE_162 = 3.0 * COSTS_RT["US500cash"]  # 2.34 filed; honest matches
GATE_163 = 3.0 * COSTS_RT["AUDUSD"]  # 3.66 filed; honest matches; not the US500 gate
FILED_GATE = {"N162": 2.34, "N163": 3.66}


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


def screen_fade(df, sig, exit_hm, thr):
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
        ent = b1
        ex = last_bar_le(g, day, xh, xm)
        if ent is None or ex is None or ex["time"] <= ent["time"]:
            n_skip += 1
            continue
        if pd.Timestamp(ex["time"]).normalize() != pd.Timestamp(ent["time"]).normalize():
            n_skip += 1
            continue
        p_ent, p_ex = px(ent), px(ex)
        if p_ent is None or p_ex is None:
            n_skip += 1
            continue
        bruto = side * 1e4 * (p_ex / p_ent - 1.0)
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
    return trades, pd.Series(pos, dtype=float).sort_index(), meta


def impulse_sign(df, h0, m0, h1, m1, thr, fade=True) -> pd.Series:
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


def ny2h_pos(df) -> pd.Series:
    """N92: sign of US100 15:30→17:30. No threshold. Continuation, not fade."""
    return impulse_sign(df, 15, 30, 17, 30, thr=0.0, fade=False)


def gap_fade_us30(df, thr=30.0) -> pd.Series:
    """N87: gap vs prior <=22:00 close. Open = first M5 of the day at or before 07:05 CET.
    |gap| > 30 bp → fade. Filed VOORSTEL_PRESCREEN_N87."""
    groups = by_day(df)
    days = sorted(groups)
    pos = {}
    for day in days:
        if day < TRAIN_START or day > TRAIN_END:
            continue
        prevs = [d for d in days if d < day]
        if not prevs:
            continue
        prev = prevs[-1]
        cref = last_bar_le(groups[prev], prev, 22, 0)
        t_cut = day + pd.Timedelta(hours=7, minutes=5)
        early = groups[day][groups[day]["time"] <= t_cut]
        if cref is None or early.empty:
            continue
        c0, o = px(cref), px(early.iloc[0])
        if c0 is None or o is None:
            continue
        gap = 1e4 * (o / c0 - 1.0)
        if abs(gap) <= thr:
            continue
        pos[day] = -1.0 if gap > 0 else 1.0
    return pd.Series(pos, dtype=float).sort_index()


def known_before(pos: pd.Series) -> pd.Series:
    idx = list(pos.index)
    out = {}
    for i in range(len(idx) - 1):
        trade = idx[i + 1]
        if trade < TRAIN_START or trade > TRAIN_END:
            continue
        out[trade] = float(pos.iloc[i])
    s = pd.Series(out, dtype=float)
    return s[~s.index.duplicated(keep="last")].sort_index()


def ratio_pos(cache, sym_a, sym_b, window=40, thr=1.5):
    ca = daily_close_22(cache[sym_a])
    cb = daily_close_22(cache[sym_b])
    both = pd.concat([ca.rename("a"), cb.rename("b")], axis=1).dropna()
    ratio = both["a"] / both["b"]
    z = zscore(ratio, window)
    pos = pd.Series(0.0, index=ratio.index)
    pos[z > thr] = -1.0  # short A
    pos[z < -thr] = 1.0  # long A
    return pos


def n91_aud_sign(df) -> pd.Series:
    """N91 long-only: ret5 > 0 → long AUD next day. No short leg."""
    closes = daily_close_22(df)
    ret5 = closes / closes.shift(5) - 1.0
    pos = pd.Series(0.0, index=closes.index)
    pos[ret5 > 0] = 1.0
    return known_before(pos)


def n84_aud_leg(df) -> pd.Series:
    """N84: |AUDNZD vs MA20| >= 40 bp at 08:00 → fade. AUD leg sign = cross sign
    (short AUDNZD = short AUD). Same CET day."""
    closes = daily_close_22(df)
    groups = by_day(df)
    pos = {}
    for day, g in groups.items():
        if day < TRAIN_START or day > TRAIN_END:
            continue
        prior = closes[closes.index < day]
        if len(prior) < 20:
            continue
        ma20 = float(prior.iloc[-20:].mean())
        b = first_bar_at(g, day, 8, 0, 15)
        p = px(b)
        if p is None or ma20 <= 0:
            continue
        stretch = 1e4 * (p / ma20 - 1.0)
        if abs(stretch) < 40:
            continue
        pos[day] = -1.0 if stretch > 0 else 1.0
    return pd.Series(pos, dtype=float).sort_index()


def xlk_us100_pos(us: pd.DataFrame) -> pd.Series:
    """N161 traded US100 side: XLK z120/thr 0.5/mom_confirm, next session 15:30→21:00."""
    xlk = load_daily_close("XLK")
    z = zscore(xlk, 120)
    d20 = xlk / xlk.shift(20) - 1.0
    sig = pd.Series(0.0, index=xlk.index)
    sig[(z > 0.5) & (d20 > 0)] = 1.0
    sig[(z < -0.5) & (d20 < 0)] = -1.0
    groups = by_day(us)
    days = sorted(d for d in groups if TRAIN_START <= d <= TRAIN_END)
    pos = {}
    for day in days:
        prior = sig[sig.index < day]
        if prior.empty:
            continue
        side = float(prior.iloc[-1])
        if side == 0.0 or not np.isfinite(side):
            continue
        sig_day = prior.index[-1]
        if (day - sig_day).days > 5:
            continue
        g = groups[day]
        ent = first_bar_at(g, day, 15, 30, 15)
        ex = last_bar_le(g, day, 21, 0)
        if ent is None or ex is None or ex["time"] <= ent["time"]:
            continue
        pos[day] = float(side)
    return pd.Series(pos, dtype=float).sort_index()


def clone_sign(name, cand: pd.Series, peer: pd.Series, binding=True) -> dict:
    """Exact calendar-day overlap only.

    Every peer passed in is already dated on the trade day (intraday sign,
    or a close signal shifted by known_before). Carrying the previous active
    day onto a day the peer did not trade inflates cover to 1 and is not the
    pre-file agree/cover definition.
    """
    c = cand.astype(float)
    p_raw = peer.sort_index().astype(float)
    # duplicate index guard
    p_raw = p_raw[~p_raw.index.duplicated(keep="last")]
    aligned = []
    for dt, cv in c.items():
        if dt in p_raw.index:
            aligned.append((dt, float(cv), float(p_raw.loc[dt])))
        else:
            aligned.append((dt, float(cv), 0.0))
    both = pd.DataFrame(aligned, columns=["date", "c", "p"]).set_index("date")
    active = both[both["c"] != 0]
    both_on = active[active["p"] != 0]
    agree = float((both_on["c"] == both_on["p"]).mean()) if len(both_on) else None
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
        "filed_gate_bp": FILED_GATE[label],
        "honest_gate_replaced_filed": abs(float(gate) - FILED_GATE[label]) > 1e-9,
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
        "US500cash",
        "US30cash",
        "US100cash",
        "GER40cash",
        "AUDUSD",
        "NZDUSD",
        "AUDNZD",
        "XAUUSD",
    )
    warm = TRAIN_START - pd.Timedelta(days=120)
    cache = {s: load_m5(s, warm, TRAIN_END) for s in need}

    def train_days(sym):
        t = cache[sym]["time"]
        m = (t >= TRAIN_START) & (t <= TRAIN_END)
        return int(t[m].dt.normalize().nunique())

    td = {s: train_days(s) for s in need}

    t162, pos162, meta162 = screen_fade(
        cache["US500cash"], sig=(19, 0, 20, 30), exit_hm=(21, 0), thr=25.0
    )
    meta162["train_days"] = td["US500cash"]
    meta162["session"] = "signal 19:00→20:30 entry at 20:30 flat 21:00 CET"
    meta162["rt_in_costs"] = True
    meta162["thr"] = 25.0

    t163, pos163, meta163 = screen_fade(
        cache["AUDUSD"], sig=(15, 30, 17, 0), exit_hm=(21, 0), thr=20.0
    )
    meta163["train_days"] = td["AUDUSD"]
    meta163["session"] = "signal 15:30→17:00 entry at 17:00 flat 21:00 CET"
    meta163["rt_in_costs"] = True
    meta163["thr"] = 20.0
    meta163["gate_is_not_us500"] = True

    n24 = impulse_sign(cache["US500cash"], 15, 30, 18, 0, 40.0, fade=True)
    n92 = ny2h_pos(cache["US100cash"])
    n87 = gap_fade_us30(cache["US30cash"], 30.0)
    n159 = impulse_sign(cache["GER40cash"], 12, 0, 15, 0, 40.0, fade=True)
    n161 = xlk_us100_pos(cache["US100cash"])
    us30_twin = impulse_sign(cache["US30cash"], 19, 0, 20, 30, 25.0, fade=True)
    us100_twin = impulse_sign(cache["US100cash"], 19, 0, 20, 30, 25.0, fade=True)

    c162 = {
        "N24_US500_AM_fade": clone_sign("N24_US500_AM_fade", pos162, n24),
        "N92_US100_NY2H_mom": clone_sign("N92_US100_NY2H_mom", pos162, n92),
        "N87_US30_gap_fade": clone_sign("N87_US30_gap_fade", pos162, n87),
        "N159_GER40_EU_close_fade": clone_sign("N159_GER40_EU_close_fade", pos162, n159),
        "N161_US100_side": clone_sign("N161_US100_side", pos162, n161),
        "US30_same_window_twin_BARRED": clone_sign(
            "US30_same_window_twin_BARRED", pos162, us30_twin
        ),
        "US100_same_window_twin_BARRED": clone_sign(
            "US100_same_window_twin_BARRED", pos162, us100_twin
        ),
    }

    n91 = n91_aud_sign(cache["AUDUSD"])
    n146 = known_before(ratio_pos(cache, "AUDUSD", "XAUUSD", 40, 1.5))
    n84 = n84_aud_leg(cache["AUDNZD"])
    asia = impulse_sign(cache["AUDUSD"], 0, 0, 7, 0, 20.0, fade=True)
    nzd_twin = impulse_sign(cache["NZDUSD"], 15, 30, 17, 0, 20.0, fade=True)

    c163 = {
        "N92_US100_NY2H_mom": clone_sign("N92_US100_NY2H_mom", pos163, n92),
        "N91_AUD_sign": clone_sign("N91_AUD_sign", pos163, n91),
        "N146_AUD_leg": clone_sign("N146_AUD_leg", pos163, n146),
        "N84_AUDNZD_AUD_leg": clone_sign("N84_AUDNZD_AUD_leg", pos163, n84),
        "GS02_AUD_Asia_0000_0700_thr20": clone_sign(
            "GS02_AUD_Asia_0000_0700_thr20", pos163, asia
        ),
        "NZD_same_window_twin_BARRED": clone_sign(
            "NZD_same_window_twin_BARRED", pos163, nzd_twin
        ),
    }

    s162 = verdict(
        t162,
        GATE_162,
        "N162",
        "US500cash",
        "US500_CASH_CLOSE_FADE ±25 19:00→20:30 entry 20:30 flat 21:00; "
        f"COSTS gate 3*{COSTS_RT['US500cash']} honest=filed; swap 0; one index; NEW_FAMILY CE",
        history_missing=td["US500cash"] < 150,
    )
    s162["meta"] = meta162
    s162["costs_rt"] = COSTS_RT["US500cash"]
    s162["rt_in_costs"] = True
    apply_clone(s162, c162)
    s162["clone"] = c162

    s163 = verdict(
        t163,
        GATE_163,
        "N163",
        "AUDUSD",
        "AUDUSD_NY_IMPULSE_FADE ±20 15:30→17:00 entry 17:00 flat 21:00; "
        f"COSTS gate 3*{COSTS_RT['AUDUSD']} honest=filed; NOT the US500 2.34 gate; "
        "swap 0; one major; NEW_FAMILY CF",
        history_missing=td["AUDUSD"] < 150,
    )
    s163["meta"] = meta163
    s163["costs_rt"] = COSTS_RT["AUDUSD"]
    s163["rt_in_costs"] = True
    apply_clone(s163, c163)
    s163["clone"] = c163

    pd.DataFrame(t162).to_csv(OUT / "n162_trades_train.csv", index=False)
    pd.DataFrame(t163).to_csv(OUT / "n163_trades_train.csv", index=False)

    def pub(s):
        return {k: v for k, v in s.items() if k != "clone"}

    summary = {
        "N162": pub(s162),
        "N163": pub(s163),
        "N162_clones": c162,
        "N163_clones": c163,
        "gates": {"N162": round(GATE_162, 4), "N163": round(GATE_163, 4)},
        "filed_gates": FILED_GATE,
        "honest_replaced_filed": {
            "N162": False,
            "N163": False,
        },
        "costs_rt": COSTS_RT,
        "clone_rule": {
            "sign_agree_ge": AGREE_CLONE,
            "cover_ge": COVER_CLONE,
            "twins": "US30/US100 19:00→20:30 ±25 and NZD 15:30→17:00 ±20 are binding barred twins, not separate screens",
            "GS02_proxy": "AUD 00:00→07:00 ±20 fade (the pre-file Asia-range check; GS02 has no separate frozen clock in this repo)",
        },
        "train": "2021-01-01..2023-12-31 entry dates only",
        "min_n": MIN_N,
        "swap": 0,
        "no_thr_grid": True,
        "no_2024_in_signal": True,
        "no_inline_replacement": True,
        "gate_source": "COSTS_FTMO.csv roundtrip_intraday_bp; session-flat so swap=0; honest gate equals filed",
        "train_days": td,
        "spec_vs_task": {
            "N162": "filed matches task: gate 2.34, 19:00→20:30 flat 21:00, thr ±25, US30/US100 twin barred",
            "N163": "filed matches task: gate 3.66 own cost gate not US500 2.34, 15:30→17:00 flat 21:00, thr ±20, NZD twin barred",
        },
    }
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2, default=str))

    def line(tag, s):
        return (
            f"- **{tag}**: N={s['n']} mean={s['mean_bruto_bp']} "
            f"med={s.get('median_bruto_bp')} gate={s['gate_bp']} "
            f"filed={s['filed_gate_bp']} honest_replaced={s['honest_gate_replaced_filed']} "
            f"→ **{s['verdict']}** years={s.get('years')} "
            f"L/S={s.get('n_long')}/{s.get('n_short')} "
            f"hits={s.get('clone_hits')} meta={s.get('meta')}\n"
        )

    md = (
        "# D-092.1 N162/N163 pre-screen (train 2021–2023)\n\n"
        + line("N162 US500_CASH_CLOSE_FADE", s162)
        + line("N163 AUDUSD_NY_IMPULSE_FADE", s163)
        + "\nGates from COSTS_FTMO.csv round-trips. Honest RT equals the filed gate "
        + "(N162 2.34; N163 3.66, not the US500 gate). Session-flat so swap=0. "
        + "No thr-grid. No 2024+ selection. No overnight. No soft-pass. "
        + "Twins are barred and are in the clone bar.\n"
    )
    (OUT / "prescreen.md").write_text(md)
    print(json.dumps({"N162": pub(s162), "N163": pub(s163)}, indent=2, default=str))
    print("---CLONES162---")
    keys = (
        "sign_agree_both_active",
        "both_active_over_cand",
        "n_both_active",
        "n_cand_active",
        "clone",
        "binding",
    )
    for k, v in c162.items():
        print(k, {kk: v[kk] for kk in keys})
    print("---CLONES163---")
    for k, v in c163.items():
        print(k, {kk: v[kk] for kk in keys})


if __name__ == "__main__":
    main()
