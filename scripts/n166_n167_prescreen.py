#!/usr/bin/env python3
"""D-092.1 TRAIN-ONLY pre-screen: N166 LQD→US500 session-flat + N167 EWY→EURUSD session-flat.

Lane-B map of S2 cycle_2344 @ 885090b. Lane-A day_t is not a PASS.
Not a 3-day hold. Not overnight US100.

Gates frozen from COSTS_FTMO.csv before any train PnL.

  N166 US500cash RT 0.78 → gate 3× = 2.34 bp. Honest RT really is 0.78
       (not a guessed 2.34). One index leg. Session-flat. Swap nights = 0.
  N167 EURUSD RT 0.63 → gate 3× = 1.89 bp. Not the US500 2.34 gate.
       Session-flat so swap nights = 0 are inside the gate.
       Short-side swap credit (−0.14 bp) is not alpha and is not subtracted.

Thresholds frozen (z120 / thr 0.5). No thr-grid. No soft-pass. N<150 is UNDERPOWERED.

Clone bar (harness): |z corr| >= 0.90 OR (agree >= 0.85 AND cover >= 0.70).
Also FAIL_CLONE if agree >= 0.98 on >= 30 both-active days (agree≈1.00 with a dead sibling),
even if mean clears the gate.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/R2/n166_n167_prescreen"
TRAIN_START = pd.Timestamp("2021-01-01")
TRAIN_END = pd.Timestamp("2023-12-31 23:59:59")
MIN_N = 150
AGREE_CLONE = 0.85
COVER_CLONE = 0.70
Z_CLONE = 0.90
AGREE_EXACT = 0.98
EXACT_MIN_N = 30

COSTS_RT = {"US500cash": 0.78, "EURUSD": 0.63}
SWAP = {
    "US500cash": {"long": 1.36, "short": 0.81},
    "EURUSD": {"long": 1.13, "short": -0.14},
}
GATE_166 = 3.0 * COSTS_RT["US500cash"]  # 2.34 honest
GATE_167 = 3.0 * COSTS_RT["EURUSD"]  # 1.89 honest; not 2.34
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


def mom_confirm_pos(sym: str, window=120, thr=0.5):
    s = load_daily_close(sym)
    z = zscore(s, window)
    d20 = s / s.shift(20) - 1.0
    pos = pd.Series(0.0, index=s.index)
    pos[(z > thr) & (d20 > 0)] = 1.0
    pos[(z < -thr) & (d20 < 0)] = -1.0
    return z, pos, s


def z_level_pos(sym: str, window=120, thr=0.5):
    """S2 z_level: z>+thr long, z<-thr short. Same sign, not a fade."""
    s = load_daily_close(sym)
    z = zscore(s, window)
    pos = pd.Series(0.0, index=s.index)
    pos[z > thr] = 1.0
    pos[z < -thr] = -1.0
    return z, pos, s


def stress_buy_pos(sym: str, window=40, thr=1.5):
    s = load_daily_close(sym)
    z = zscore(s, window)
    pos = pd.Series(0.0, index=s.index)
    pos[z > thr] = -1.0
    pos[z < -thr] = 1.0
    return z, pos


def fade_level_pos(sym: str, window=40, thr=1.0):
    return stress_buy_pos(sym, window, thr)


def screen_next_session(pos_signal: pd.Series, z: pd.Series, book: pd.DataFrame, zkey="z120"):
    """Signal on daily date t → session on the next cash day that has M5.
    Entry first M5 >= 15:30, exit last M5 <= 21:00, same day. No overnight."""
    groups = by_day(book)
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
                zkey: None if not np.isfinite(zv) else round(float(zv), 4),
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
        "swap_nights": 0,
        "overnight": False,
        "hold": "session-flat 15:30→21:00 not 3d",
    }
    return trades, pd.Series(pos, dtype=float).sort_index(), meta


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


def lo_ret_pos(close: pd.Series, lookback: int) -> pd.Series:
    ret = close / close.shift(lookback) - 1.0
    pos = pd.Series(0.0, index=close.index)
    pos[ret > 0] = 1.0
    return pos


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


def defensive_pos():
    xlu = load_daily_close("XLU")
    xli = load_daily_close("XLI")
    ratio = (xlu / xli).dropna()
    z = zscore(ratio, 40)
    pos = pd.Series(0.0, index=z.index)
    pos[z > 0.5] = -1.0
    pos[z < -0.5] = 1.0
    return z, pos


def eqw_pos():
    a = load_daily_close("SPX_EQW")
    b = load_daily_close("SPX")
    ratio = (a / b).dropna()
    z = zscore(ratio, 40)
    pos = pd.Series(0.0, index=z.index)
    pos[z > 1.5] = -1.0
    pos[z < -1.5] = 1.0
    return z, pos


def dxy_inverse_mom():
    s = load_daily_close("DXY")
    z = zscore(s, 120)
    d20 = s / s.shift(20) - 1.0
    pos = pd.Series(0.0, index=s.index)
    pos[(z > 0.5) & (d20 > 0)] = -1.0
    pos[(z < -0.5) & (d20 < 0)] = 1.0
    return z, pos


def ratio_fade(close_a, close_b, window=40, thr=1.5):
    both = pd.concat([close_a.rename("a"), close_b.rename("b")], axis=1).dropna()
    ratio = both["a"] / both["b"]
    z = zscore(ratio, window)
    pos = pd.Series(0.0, index=ratio.index)
    pos[z > thr] = -1.0
    pos[z < -thr] = 1.0
    return z, pos


def clone_sign(name, cand: pd.Series, peer: pd.Series, binding=True, z_c=None, z_p=None) -> dict:
    c = cand.astype(float)
    p_raw = peer.sort_index().astype(float)
    aligned = []
    for dt, cv in c.items():
        if dt in p_raw.index:
            pv = p_raw.loc[dt]
            pv = float(pv.iloc[0] if hasattr(pv, "iloc") else pv)
            aligned.append((dt, float(cv), pv))
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
    if (
        agree is not None
        and agree >= AGREE_EXACT
        and len(both_on) >= EXACT_MIN_N
    ):
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


def verdict(trades, gate, rt, label, instrument, notes, history_missing=False):
    n = len(trades)
    base = {
        "id": label,
        "instrument": instrument,
        "n": n,
        "mean_bruto_bp": None,
        "netto_bp": None,
        "gate_bp": round(float(gate), 4),
        "rt_bp": rt,
        "verdict": "FAIL",
        "notes": notes,
    }
    if history_missing or n == 0:
        base["verdict"] = "DIAG_FAIL"
        return base
    arr = np.array([t["bruto_bp"] for t in trades], dtype=float)
    mean = float(arr.mean())
    # Session-flat: one RT, zero swap nights. Credits are not added.
    netto = mean - rt
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
    dates = pd.to_datetime([t["date"] for t in trades])
    span_y = float((dates.max() - dates.min()).days) / 365.25 if len(dates) else 0.0
    base.update(
        {
            "mean_bruto_bp": round(mean, 4),
            "netto_bp": round(netto, 4),
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
            "trade_span_years": round(span_y, 2),
        }
    )
    return base


def apply_clone(summary, clones):
    hit = [k for k, v in clones.items() if v.get("clone") and v.get("binding", True)]
    summary["clone_hits"] = hit
    if hit and summary["verdict"] != "DIAG_FAIL":
        summary["verdict"] = "FAIL_CLONE"
        if "CLONE" not in summary["notes"]:
            summary["notes"] += " | CLONE of " + ",".join(hit) + " — no PREREG"
    return summary


def hist_years(s: pd.Series) -> float:
    if len(s) < 2:
        return 0.0
    return float((s.index.max() - s.index.min()).days) / 365.25


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    warm = TRAIN_START - pd.Timedelta(days=80)
    cache = {
        s: load_m5(s, warm, TRAIN_END)
        for s in ("US500cash", "EURUSD", "GBPUSD", "NZDUSD", "EURJPY", "USDCHF", "USDJPY", "USDCAD")
    }

    def train_days(sym):
        t = cache[sym]["time"]
        m = (t >= TRAIN_START) & (t <= TRAIN_END)
        return int(t[m].dt.normalize().nunique())

    td = {s: train_days(s) for s in cache}

    z_lqd, pos_lqd, px_lqd = mom_confirm_pos("LQD", 120, 0.5)
    z_ewy, pos_ewy, px_ewy = z_level_pos("EWY", 120, 0.5)
    t166, pos166, meta166 = screen_next_session(pos_lqd, z_lqd, cache["US500cash"])
    t167, pos167, meta167 = screen_next_session(pos_ewy, z_ewy, cache["EURUSD"])
    meta166["train_days"] = td["US500cash"]
    meta167["train_days"] = td["EURUSD"]
    meta166["rt_in_costs"] = True
    meta167["rt_in_costs"] = True
    meta166["lane_a_day_t"] = 4.218
    meta167["lane_a_day_t"] = 2.597
    meta166["lane_a_day_t_is_not_a_pass"] = True
    meta167["lane_a_day_t_is_not_a_pass"] = True
    meta166["signal_hist_years"] = round(hist_years(px_lqd), 2)
    meta167["signal_hist_years"] = round(hist_years(px_ewy), 2)
    meta166["d094a"] = "LQD daily history >= 5y through 2023; train book is 2021-2023"
    meta167["d094a"] = "EWY daily history >= 5y through 2023; train book is 2021-2023"
    meta167["swap_credit_not_alpha"] = True
    meta167["swap_short_bp_not_in_gate"] = SWAP["EURUSD"]["short"]
    meta167["swap_long_bp_not_in_gate_because_zero_nights"] = SWAP["EURUSD"]["long"]

    # --- N166 peers (dead siblings). Signal-day and the mapped trade book. ---
    z_xlk, pos_xlk, _ = mom_confirm_pos("XLK", 120, 0.5)
    z_hyg, pos_hyg, _ = mom_confirm_pos("HYG", 120, 0.5)
    z_def, pos_def = defensive_pos()
    z_xle, pos_xle = fade_level_pos("XLE", 40, 1.0)
    z_dbc, pos_dbc = fade_level_pos("DBC", 40, 1.0)
    z_xlf, pos_xlf = stress_buy_pos("XLF", 40, 1.5)
    z_qual, pos_qual = stress_buy_pos("QUAL", 40, 1.5)
    z_mtum, pos_mtum = stress_buy_pos("MTUM", 40, 1.5)
    z_eqw, pos_eqw = eqw_pos()
    z_disp, pos_disp = sector_disp()

    sig_lqd = pos_lqd[(pos_lqd.index >= TRAIN_START) & (pos_lqd.index <= TRAIN_END)]
    peers_166_sig = {
        "N161_XLK_mom_z120": (pos_xlk, z_xlk),
        "HYG_mom_z120": (pos_hyg, z_hyg),
        "DEFENSIVE_XLU_XLI_z40": (pos_def, z_def),
        "XLE_z40_fade_thr1.0": (pos_xle, z_xle),
        "SECTOR_DISP": (pos_disp, z_disp),
        "DBC_z40_fade_thr1.0": (pos_dbc, z_dbc),
        "XLF_z40_stress_thr1.5": (pos_xlf, z_xlf),
        "QUAL_z40_stress_thr1.5": (pos_qual, z_qual),
        "MTUM_z40_stress_thr1.5": (pos_mtum, z_mtum),
        "EQW_z40_stress_thr1.5": (pos_eqw, z_eqw),
    }
    c166 = {}
    for name, (p, z) in peers_166_sig.items():
        c166[name + "_signal"] = clone_sign(name + "_signal", sig_lqd, p, z_c=z_lqd, z_p=z)
        c166[name + "_trade"] = clone_sign(
            name + "_trade", pos166, known_before(p), z_c=z_lqd, z_p=z
        )

    # --- N167 peers ---
    z_eem, pos_eem = stress_buy_pos("EEM", 40, 1.5)
    z_ewz, pos_ewz = stress_buy_pos("EWZ", 40, 1.5)
    z_dxy, pos_dxy = dxy_inverse_mom()
    c_eur = daily_close_22(cache["EURUSD"])
    c_usdjpy = daily_close_22(cache["USDJPY"])
    c_eurjpy = daily_close_22(cache["EURJPY"])
    c_gbp = daily_close_22(cache["GBPUSD"])
    c_nzd = daily_close_22(cache["NZDUSD"])
    c_usdcad = daily_close_22(cache["USDCAD"])
    c_usdchf = daily_close_22(cache["USDCHF"])
    pos_l60_eur = lo_ret_pos(c_eur, 60)
    pos_l60_jpy = lo_ret_pos(c_usdjpy, 60)
    pos_l60_ej = lo_ret_pos(c_eurjpy, 60)
    z_gbpnzd, pos_gbpnzd = ratio_fade(c_gbp, c_nzd, 40, 1.5)
    z_eurcad, pos_eurcad = ratio_fade(c_eur, c_usdcad, 40, 1.5)
    z_ejchf, pos_ejchf = ratio_fade(c_eurjpy, c_usdchf, 40, 1.5)

    sig_ewy = pos_ewy[(pos_ewy.index >= TRAIN_START) & (pos_ewy.index <= TRAIN_END)]
    peers_167 = {
        "L60_EURUSD_LO": (pos_l60_eur, None),
        "L60_USDJPY_LO": (pos_l60_jpy, None),
        "L60_EURJPY_LO": (pos_l60_ej, None),
        "N131_DXY_inverse_mom": (pos_dxy, z_dxy),
        "N152_GBP_NZD": (pos_gbpnzd, z_gbpnzd),
        "N153_EUR_CAD": (pos_eurcad, z_eurcad),
        "N151_EURJPY_USDCHF": (pos_ejchf, z_ejchf),
        "EEM_stress_z40": (pos_eem, z_eem),
        "EWZ_stress_z40": (pos_ewz, z_ewz),
        "LQD_mom_z120": (pos_lqd, z_lqd),
    }
    c167 = {}
    for name, (p, z) in peers_167.items():
        c167[name + "_signal"] = clone_sign(name + "_signal", sig_ewy, p, z_c=z_ewy, z_p=z)
        c167[name + "_trade"] = clone_sign(
            name + "_trade", pos167, known_before(p), z_c=z_ewy, z_p=z
        )

    s166 = verdict(
        t166, GATE_166, COSTS_RT["US500cash"], "N166", "US500cash",
        "LQD_IG_CREDIT_STRESS z120/thr0.5/mom_confirm → US500 session-flat 15:30→21:00; "
        f"honest COSTS gate 3*{COSTS_RT['US500cash']}={GATE_166:.2f} (RT really is 0.78, not a guess); "
        "swap nights 0; NOT hold=3d; NOT overnight US100; Lane-A day_t 4.22 is not a PASS; "
        "NEW_FAMILY CI; S2 885090b cycle_2344",
        history_missing=td["US500cash"] < 150,
    )
    s166["meta"] = meta166
    s166["costs_rt"] = COSTS_RT["US500cash"]
    s166["gate_source"] = "honest COSTS_FTMO.csv roundtrip_intraday_bp 0.78 × 3 = 2.34"
    s166["filed_gate_note"] = "2.34 matches the book US500 gate because honest RT is 0.78; not a guessed substitute"
    s166["rt_in_costs"] = True
    s166["lane_a_day_t_not_a_pass"] = 4.218
    apply_clone(s166, c166)
    s166["clone"] = c166

    s167 = verdict(
        t167, GATE_167, COSTS_RT["EURUSD"], "N167", "EURUSD",
        "EWY_KOREA_STRESS z120/thr0.5/z_level → EURUSD session-flat 15:30→21:00; "
        f"honest COSTS gate 3*{COSTS_RT['EURUSD']}={GATE_167:.2f} (not the US500 2.34 gate); "
        "swap nights 0 inside the gate; short swap credit -0.14 is not alpha; "
        "NOT hold=3d; Lane-A day_t 2.60 is not a PASS; NEW_FAMILY CJ; S2 885090b cycle_2344",
        history_missing=td["EURUSD"] < 150,
    )
    s167["meta"] = meta167
    s167["costs_rt"] = COSTS_RT["EURUSD"]
    s167["gate_source"] = "honest COSTS_FTMO.csv roundtrip_intraday_bp 0.63 × 3 = 1.89; swap nights 0; credit not subtracted"
    s167["swap"] = {
        "nights": 0,
        "long_bp": SWAP["EURUSD"]["long"],
        "short_bp_credit": SWAP["EURUSD"]["short"],
        "in_gate_bp": 0.0,
        "credit_treated_as_alpha": False,
    }
    s167["rt_in_costs"] = True
    s167["lane_a_day_t_not_a_pass"] = 2.597
    apply_clone(s167, c167)
    s167["clone"] = c167

    pd.DataFrame(t166).to_csv(OUT / "n166_trades_train.csv", index=False)
    pd.DataFrame(t167).to_csv(OUT / "n167_trades_train.csv", index=False)

    def pub(s):
        return {k: v for k, v in s.items() if k != "clone"}

    summary = {
        "N166": pub(s166),
        "N167": pub(s167),
        "N166_clones": c166,
        "N167_clones": c167,
        "gates": {"N166": round(GATE_166, 4), "N167": round(GATE_167, 4)},
        "costs_rt": COSTS_RT,
        "clone_rule": {
            "sign_agree_ge": AGREE_CLONE,
            "cover_ge": COVER_CLONE,
            "z_corr_ge": Z_CLONE,
            "agree_exact_ge": AGREE_EXACT,
            "agree_exact_min_n": EXACT_MIN_N,
        },
        "train": "2021-01-01..2023-12-31 entry dates only",
        "min_n": MIN_N,
        "swap_nights": 0,
        "no_thr_grid": True,
        "no_2024_in_signal": True,
        "no_inline_replacement": True,
        "s2_ref": "885090b results/strateeg2_prescreen/cycle_2344",
        "train_days": td,
        "trial_count_unchanged": 471,
    }
    (OUT / "prescreen.json").write_text(json.dumps(summary, indent=2, default=str))

    def line(tag, s):
        return (
            f"- **{tag}**: N={s['n']} mean={s['mean_bruto_bp']} netto={s.get('netto_bp')} "
            f"med={s.get('median_bruto_bp')} gate={s['gate_bp']} "
            f"→ **{s['verdict']}** years={s.get('years')} span={s.get('trade_span_years')} "
            f"L/S={s.get('n_long')}/{s.get('n_short')} "
            f"hits={s.get('clone_hits')} meta={s.get('meta')}\n"
        )

    md = (
        "# D-092.1 N166/N167 pre-screen (train 2021–2023)\n\n"
        "S2 `885090b` cycle_2344. Lane-A day_t is not a PASS. Not hold=3d. Not overnight US100.\n\n"
        + line("N166 LQD_IG_CREDIT_STRESS → US500 session-flat", s166)
        + line("N167 EWY_KOREA_STRESS → EURUSD session-flat", s167)
        + "\nGates from COSTS_FTMO.csv round-trips. N166 honest RT 0.78 × 3 = 2.34 "
        + "(the engine's US500 cost really is 2.34, not a guess). "
        + "N167 honest RT 0.63 × 3 = 1.89, not the US500 gate. "
        + "Session-flat so swap nights = 0 are inside the gate. "
        + "EURUSD short swap credit −0.14 is not alpha and is not subtracted. "
        + "No thr-grid. No 2024+ selection.\n"
    )
    (OUT / "prescreen.md").write_text(md)
    print(json.dumps({"N166": pub(s166), "N167": pub(s167)}, indent=2, default=str))
    print("---CLONES166---")
    for k, v in c166.items():
        flag = "CLONE" if v["clone"] else ""
        print(k, {kk: v[kk] for kk in ("z_corr_train", "sign_agree_both_active", "both_active_over_cand", "n_both_active", "n_cand_active")}, flag)
    print("---CLONES167---")
    for k, v in c167.items():
        flag = "CLONE" if v["clone"] else ""
        print(k, {kk: v[kk] for kk in ("z_corr_train", "sign_agree_both_active", "both_active_over_cand", "n_both_active", "n_cand_active")}, flag)


if __name__ == "__main__":
    main()
