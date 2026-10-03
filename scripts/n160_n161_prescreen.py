#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N160 XAG NY-impulse fade + N161 XLK→US100 session-flat.

Gates frozen from COSTS_FTMO.csv before any train PnL.

  N160 XAGUSD RT 5.07 → gate 3× = 15.21 bp. One silver leg. Session-flat.
  N161 US100cash RT 0.66 → gate 3× = 1.98 bp. One index leg. Session-flat.

Swap in the gate is 0. Neither book is held overnight.
N161 is not the S2 hold=3d book. Lane-A day_t 2.05 is not a PASS.

Thresholds frozen. No thr-grid. No soft-pass.

N160 clone bar (precommitted + task): sign agree >= 0.85 AND cover >= 0.70
  vs N82 London-fade, XAG leg of N150, XAG leg of N141, N75 silver side,
  N113 SLV/GLD silver day-sign, CPER level z40. A clone is not a PASS.

N161 clone bar (precommitted): |z corr| >= 0.90 OR (agree >= 0.85 AND cover >= 0.70)
  vs SECTOR_DISP, XLE z40 fade, DBC z40 fade, XLF z40 fade, XLU/XLI z40 thr 0.5,
  UNG z40 stress. Task also binds the actual traded signal vs DEFENSIVE and vs N92.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n160_n161_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
MIN_N = 150
AGREE_CLONE = 0.85
COVER_CLONE = 0.70
Z_CLONE = 0.90

COSTS_RT = {"XAGUSD": 5.07, "US100cash": 0.66}
GATE_160 = 3.0 * COSTS_RT["XAGUSD"]  # 15.21
GATE_161 = 3.0 * COSTS_RT["US100cash"]  # 1.98

SECTORS = ["XLB", "XLE", "XLF", "XLI", "XLK", "XLP", "XLU", "XLV", "XLY"]


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


def screen_fade(df, sig, exit_hm, thr=40.0):
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
    series = pd.Series(pos, dtype=float).sort_index()
    return trades, series, meta


def impulse_sign(df, h0, m0, h1, m1, thr, fade=False) -> pd.Series:
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


def ratio_pos(cache, sym_a, sym_b, window=40, thr=1.5):
    """+1 = long A / short B (z < -thr). Signal dated on the 22:00 close day."""
    ca = daily_close_22(cache[sym_a])
    cb = daily_close_22(cache[sym_b])
    both = pd.concat([ca.rename("a"), cb.rename("b")], axis=1).dropna()
    ratio = both["a"] / both["b"]
    z = zscore(ratio, window)
    pos = pd.Series(0.0, index=ratio.index)
    pos[z > thr] = -1.0
    pos[z < -thr] = 1.0
    return z, pos


def known_before(pos: pd.Series) -> pd.Series:
    """Shift a close-of-day signal onto the next index day (no same-day lookahead)."""
    idx = list(pos.index)
    out = {}
    for i in range(len(idx) - 1):
        trade = idx[i + 1]
        if trade < TRAIN_START or trade > TRAIN_END:
            continue
        out[trade] = float(pos.iloc[i])
    s = pd.Series(out, dtype=float)
    return s[~s.index.duplicated(keep="last")].sort_index()


def level_z_pos(sym, window, thr):
    s = load_daily_close(sym)
    s = s[(s.index >= TRAIN_START - pd.Timedelta(days=window * 4)) & (s.index <= TRAIN_END)]
    z = zscore(s, window)
    pos = pd.Series(0.0, index=s.index)
    pos[z > thr] = -1.0
    pos[z < -thr] = 1.0
    return z, pos


def n75_silver_side(cache) -> pd.Series:
    """z20 of ln(XAU/XAG) < -1 → short silver (−1). No long-silver side. Dated on close day."""
    ca = daily_close_22(cache["XAUUSD"])
    cg = daily_close_22(cache["XAGUSD"])
    both = pd.concat([ca.rename("a"), cg.rename("g")], axis=1).dropna()
    z = zscore(np.log(both["a"] / both["g"]), 20)
    pos = pd.Series(0.0, index=z.index)
    pos[z < -1.0] = -1.0
    return pos


def slv_gld_silver_side():
    """N113: SLV/GLD z40. Silver day-sign = fade the ratio (z>+1 short silver, z<-1 long silver).
    That sign matches the US500 book (z>+1 short equity)."""
    a = load_daily_close("SLV")
    b = load_daily_close("GLD")
    ratio = (a / b).dropna()
    ratio = ratio[(ratio.index >= TRAIN_START - pd.Timedelta(days=180)) & (ratio.index <= TRAIN_END)]
    z = zscore(ratio, 40)
    pos = pd.Series(0.0, index=ratio.index)
    pos[z > 1.0] = -1.0
    pos[z < -1.0] = 1.0
    return z, pos


def sector_disp():
    frames = {s: load_daily_close(s) for s in SECTORS}
    rets = []
    for sym, s in frames.items():
        r = s.sort_index() / s.sort_index().shift(10) - 1.0
        rets.append(r.rename(sym))
    wide = pd.concat(rets, axis=1).dropna(how="any")
    disp = wide.std(axis=1, ddof=0)
    z = zscore(disp, 40)
    pos = pd.Series(0.0, index=z.index)
    pos[z > 1.0] = -1.0
    pos[z < -0.5] = 1.0
    return z, pos


def xlk_signal():
    xlk = load_daily_close("XLK")
    z = zscore(xlk, 120)
    d20 = xlk / xlk.shift(20) - 1.0
    pos = pd.Series(0.0, index=xlk.index)
    pos[(z > 0.5) & (d20 > 0)] = 1.0
    pos[(z < -0.5) & (d20 < 0)] = -1.0
    return z, pos, xlk


def screen_next_session(pos_signal: pd.Series, z: pd.Series, us: pd.DataFrame):
    """Signal on daily date t → US100 session on the next cash day that has M5.
    Entry first M5 >= 15:30, exit last M5 <= 21:00, same day. No overnight."""
    groups = by_day(us)
    days = sorted(d for d in groups if TRAIN_START <= d <= TRAIN_END)
    trades = []
    pos = {}
    n_sig = 0
    n_skip = 0
    sig = pos_signal.sort_index()
    for day in days:
        prior = sig[sig.index < day]
        if prior.empty:
            continue
        side = float(prior.iloc[-1])
        if side == 0.0 or not np.isfinite(side):
            continue
        # only the immediately preceding signal day (no stale multi-day carry)
        sig_day = prior.index[-1]
        if (day - sig_day).days > 5:
            continue
        n_sig += 1
        g = groups[day]
        ent = first_bar_at(g, day, 15, 30, 15)
        ex = last_bar_le(g, day, 21, 0)
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
        zv = z.reindex([sig_day]).iloc[0] if sig_day in z.index else np.nan
        trades.append(
            {
                "date": str(pd.Timestamp(day).date()),
                "signal_day": str(pd.Timestamp(sig_day).date()),
                "side": int(side),
                "z120": None if not np.isfinite(zv) else round(float(zv), 4),
                "entry": str(ent["time"]),
                "exit": str(ex["time"]),
                "bruto_bp": float(bruto),
            }
        )
    meta = {
        "n_signal_days_with_session": n_sig,
        "n_skip_missing_bar": n_skip,
        "n_trades": len(trades),
        "swap_bp": 0,
        "overnight": False,
        "hold": "session-flat 15:30→21:00 not 3d",
    }
    return trades, pd.Series(pos, dtype=float).sort_index(), meta


def ny2h_pos(df) -> pd.Series:
    """N92: sign of US100 15:30→17:30. Position dated that day. No threshold."""
    groups = by_day(df)
    pos = {}
    for day, g in groups.items():
        if day < TRAIN_START or day > TRAIN_END:
            continue
        b0 = first_bar_at(g, day, 15, 30, 15)
        b1 = first_bar_at(g, day, 17, 30, 15)
        if b0 is None or b1 is None or b1["time"] <= b0["time"]:
            continue
        p0, p1 = px(b0), px(b1)
        if p0 is None or p1 is None or p1 == p0:
            continue
        pos[day] = 1.0 if p1 > p0 else -1.0
    return pd.Series(pos, dtype=float).sort_index()


def clone_sign(name, cand: pd.Series, peer: pd.Series, binding=True, z_c=None, z_p=None) -> dict:
    c = cand.astype(float)
    # peer on candidate dates: exact date, else last peer date strictly before (no lookahead)
    p_raw = peer.sort_index().astype(float)
    aligned = []
    for dt, cv in c.items():
        if dt in p_raw.index:
            # same timestamp: use it only if the peer is an intraday same-day sign
            # Caller passes already-shifted peers when the peer is a close-of-day signal.
            aligned.append((dt, float(cv), float(p_raw.loc[dt])))
        else:
            prev = p_raw[p_raw.index < dt]
            if prev.empty:
                aligned.append((dt, float(cv), 0.0))
            else:
                aligned.append((dt, float(cv), float(prev.iloc[-1])))
    both = pd.DataFrame(aligned, columns=["date", "c", "p"]).set_index("date")
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
    need = ("XAGUSD", "XAUUSD", "US30cash", "UKOILcash", "US100cash")
    warm = TRAIN_START - pd.Timedelta(days=40)
    cache = {s: load_m5(s, warm, TRAIN_END) for s in need}

    def train_days(sym):
        t = cache[sym]["time"]
        m = (t >= TRAIN_START) & (t <= TRAIN_END)
        return int(t[m].dt.normalize().nunique())

    td = {s: train_days(s) for s in need}

    t160, pos160, meta160 = screen_fade(
        cache["XAGUSD"], sig=(15, 30, 17, 0), exit_hm=(21, 0), thr=40.0
    )
    meta160["train_days"] = td["XAGUSD"]
    meta160["session"] = "signal 15:30→17:00 entry at 17:00 flat 21:00 CET"
    meta160["rt_in_costs"] = True

    z_xlk, pos_xlk, _xlk = xlk_signal()
    t161, pos161, meta161 = screen_next_session(pos_xlk, z_xlk, cache["US100cash"])
    meta161["train_days"] = td["US100cash"]
    meta161["rt_in_costs"] = True
    meta161["lane_a_day_t"] = 2.05
    meta161["lane_a_day_t_is_not_a_pass"] = True

    # --- N160 peers ---
    n82 = impulse_sign(cache["XAGUSD"], 8, 0, 10, 30, 35.0, fade=True)
    _z150, pos150 = ratio_pos(cache, "XAGUSD", "US30cash", 40, 1.5)
    xag_leg_150 = known_before(pos150)  # +1 long XAG
    _z141, pos141 = ratio_pos(cache, "XAGUSD", "UKOILcash", 40, 1.5)
    xag_leg_141 = known_before(pos141)
    silver75 = known_before(n75_silver_side(cache))
    z_sg, pos_sg = slv_gld_silver_side()
    silver113 = known_before(pos_sg)
    z_cper, pos_cper = level_z_pos("CPER", 40, 1.5)
    cper_live = known_before(pos_cper)

    c160 = {
        "N82_XAG_LonAM_fade": clone_sign("N82_XAG_LonAM_fade", pos160, n82),
        "N150_XAG_leg": clone_sign("N150_XAG_leg", pos160, xag_leg_150),
        "N141_XAG_leg": clone_sign("N141_XAG_leg", pos160, xag_leg_141),
        "N75_silver_side": clone_sign("N75_silver_side", pos160, silver75),
        "N113_SLV_GLD_silver_daysign": clone_sign(
            "N113_SLV_GLD_silver_daysign", pos160, silver113, z_c=None, z_p=z_sg
        ),
        "CPER_z40_thr1.5": clone_sign("CPER_z40_thr1.5", pos160, cper_live, z_c=None, z_p=z_cper),
    }

    # --- N161 peers (signal-day z and day-sign; trade-day actual vs DEFENSIVE and N92) ---
    z_disp, pos_disp = sector_disp()
    z_xle, pos_xle = level_z_pos("XLE", 40, 1.0)
    z_dbc, pos_dbc = level_z_pos("DBC", 40, 1.0)
    z_xlf, pos_xlf = level_z_pos("XLF", 40, 1.5)
    xlu = load_daily_close("XLU")
    xli = load_daily_close("XLI")
    ratio_def = (xlu / xli).dropna()
    z_def = zscore(ratio_def, 40)
    pos_def = pd.Series(0.0, index=z_def.index)
    pos_def[z_def > 0.5] = -1.0
    pos_def[z_def < -0.5] = 1.0
    z_ung, pos_ung = level_z_pos("UNG", 40, 1.5)

    # signal-day comparison (pre-file style) on mom_confirm dates inside train
    sig_train = pos_xlk[(pos_xlk.index >= TRAIN_START) & (pos_xlk.index <= TRAIN_END)]
    c161_signal = {
        "SECTOR_DISP": clone_sign("SECTOR_DISP", sig_train, pos_disp, z_c=z_xlk, z_p=z_disp),
        "XLE_z40_fade_thr1.0": clone_sign("XLE_z40_fade_thr1.0", sig_train, pos_xle, z_c=z_xlk, z_p=z_xle),
        "DBC_z40_fade_thr1.0": clone_sign("DBC_z40_fade_thr1.0", sig_train, pos_dbc, z_c=z_xlk, z_p=z_dbc),
        "XLF_z40_fade_thr1.5": clone_sign("XLF_z40_fade_thr1.5", sig_train, pos_xlf, z_c=z_xlk, z_p=z_xlf),
        "XLU_XLI_z40_thr0.5": clone_sign("XLU_XLI_z40_thr0.5", sig_train, pos_def, z_c=z_xlk, z_p=z_def),
        "UNG_z40_stress_thr1.5": clone_sign("UNG_z40_stress_thr1.5", sig_train, pos_ung, z_c=z_xlk, z_p=z_ung),
    }
    # actual executed book vs DEFENSIVE (prior signal, same trade date) and vs N92 same session
    def_live = known_before(pos_def)
    n92 = ny2h_pos(cache["US100cash"])
    c161_trade = {
        "DEFENSIVE_XLU_XLI_trade": clone_sign("DEFENSIVE_XLU_XLI_trade", pos161, def_live, z_c=z_xlk, z_p=z_def),
        "N92_US100_NY2H_mom": clone_sign("N92_US100_NY2H_mom", pos161, n92),
    }
    c161 = {**c161_signal, **c161_trade}

    s160 = verdict(
        t160, GATE_160, "N160", "XAGUSD",
        "XAG_NY_IMPULSE_FADE ±40 15:30→17:00 entry 17:00 flat 21:00; "
        f"COSTS gate 3*{COSTS_RT['XAGUSD']}; swap 0; one silver leg; NEW_FAMILY CC",
        history_missing=td["XAGUSD"] < 150,
    )
    s160["meta"] = meta160
    s160["costs_rt"] = COSTS_RT["XAGUSD"]
    s160["rt_in_costs"] = True
    apply_clone(s160, c160)
    s160["clone"] = c160

    s161 = verdict(
        t161, GATE_161, "N161", "US100cash",
        "XLK_TECH_SECTOR_STRESS z120/thr0.5/mom_confirm → US100 session-flat 15:30→21:00; "
        f"COSTS gate 3*{COSTS_RT['US100cash']}; swap 0; NOT hold=3d; NOT overnight long; "
        "Lane-A day_t 2.05 is not a PASS; NEW_FAMILY CD; S2 51b24bf cycle_0147",
        history_missing=td["US100cash"] < 150,
    )
    s161["meta"] = meta161
    s161["costs_rt"] = COSTS_RT["US100cash"]
    s161["rt_in_costs"] = True
    s161["lane_a_day_t_not_a_pass"] = 2.05
    apply_clone(s161, c161)
    s161["clone"] = c161

    pd.DataFrame(t160).to_csv(OUT / "n160_trades_train.csv", index=False)
    pd.DataFrame(t161).to_csv(OUT / "n161_trades_train.csv", index=False)

    def pub(s):
        return {k: v for k, v in s.items() if k != "clone"}

    summary = {
        "N160": pub(s160),
        "N161": pub(s161),
        "N160_clones": c160,
        "N161_clones": c161,
        "gates": {"N160": round(GATE_160, 4), "N161": round(GATE_161, 4)},
        "costs_rt": COSTS_RT,
        "clone_rule": {
            "sign_agree_ge": AGREE_CLONE,
            "cover_ge": COVER_CLONE,
            "z_corr_ge": Z_CLONE,
            "N160": "sign×cover only (one-leg impulse; no ratio z)",
            "N161": "z-corr or sign×cover; actual trade vs DEFENSIVE and N92 is binding",
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
        "# D-092.1 N160/N161 pre-screen (train 2021–2023)\n\n"
        + line("N160 XAG_NY_IMPULSE_FADE", s160)
        + line("N161 XLK_TECH_SECTOR_STRESS session-flat", s161)
        + "\nGates from COSTS_FTMO.csv round-trips. Session-flat so swap=0 is in the gate. "
        + "No thr-grid. No 2024+ selection. No overnight. N161 is not a 3-day hold. "
        + "Lane-A day_t 2.05 is not a PASS.\n"
    )
    (OUT / "prescreen.md").write_text(md)
    print(json.dumps({"N160": pub(s160), "N161": pub(s161)}, indent=2, default=str))
    print("---CLONES160---")
    for k, v in c160.items():
        print(k, {kk: v[kk] for kk in ("z_corr_train", "sign_agree_both_active", "both_active_over_cand", "n_both_active", "n_cand_active", "clone", "binding")})
    print("---CLONES161---")
    for k, v in c161.items():
        print(k, {kk: v[kk] for kk in ("z_corr_train", "sign_agree_both_active", "both_active_over_cand", "n_both_active", "n_cand_active", "clone", "binding")})


if __name__ == "__main__":
    main()
